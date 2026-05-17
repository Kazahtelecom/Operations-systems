#!/usr/bin/env python3
"""
Linux FS AI Agent with Telegram Bot
Финальный проект по курсу "Операционные системы", КазНУ 2026
Author: kz444gron
Date: Май 2026

Особенности:
- Умный fallback между моделями (2.5 → 2.0 → 1.5)
- Автоматический retry при ошибках API
- Защита от галлюцинаций путей
- 8 инструментов для работы с файловой системой
"""

import os
import glob
import shutil
import subprocess
import logging
import time
from datetime import datetime
from functools import wraps
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== НАСТРОЙКА ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== КОНФИГУРАЦИЯ МОДЕЛЕЙ ==========
# Приоритет моделей: сначала 2.5 Flash, затем fallback
MODELS_PRIORITY = [
    "gemini-2.5-flash",   # Самая новая, но строгие лимиты
    "gemini-2.0-flash",   # Хороший баланс
    "gemini-1.5-flash"    # Самая стабильная
]

# ========== 1. ИНСТРУМЕНТЫ ==========

def find_files(directory: str, pattern: str = "*") -> dict:
    """Найти файлы по шаблону в директории (рекурсивно)."""
    try:
        full_pattern = os.path.join(directory, "**", pattern)
        matches = glob.glob(full_pattern, recursive=True)
        limited = matches[:30]
        return {
            "found": len(matches),
            "shown": len(limited),
            "files": limited
        }
    except Exception as e:
        return {"error": str(e)}

def read_file(path: str, max_chars: int = 4000) -> dict:
    """Прочитать содержимое текстового файла."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_chars)
        return {
            "path": path,
            "size": os.path.getsize(path),
            "content": content,
            "truncated": os.path.getsize(path) > max_chars
        }
    except Exception as e:
        return {"error": str(e)}

def disk_usage(path: str = "/") -> dict:
    """Получить информацию об использовании диска."""
    try:
        total, used, free = shutil.disk_usage(path)
        return {
            "path": path,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "percent_used": round((used / total) * 100, 1)
        }
    except Exception as e:
        return {"error": str(e)}

def file_info(path: str) -> dict:
    """Получить метаданные файла (inode, права, размер)."""
    try:
        stat = os.stat(path)
        return {
            "path": path,
            "size_bytes": stat.st_size,
            "inode": stat.st_ino,
            "permissions": oct(stat.st_mode)[-3:],
            "uid": stat.st_uid,
            "gid": stat.st_gid,
            "links": stat.st_nlink,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def list_directory(path: str = ".") -> dict:
    """Показать содержимое директории."""
    try:
        items = os.listdir(path)
        files = []
        dirs = []
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item + "/")
            else:
                files.append(item)
        return {
            "path": path,
            "directories": sorted(dirs)[:20],
            "files": sorted(files)[:20],
            "total_items": len(items)
        }
    except Exception as e:
        return {"error": str(e)}

def system_logs(limit: int = 30, unit: str = None) -> dict:
    """Получить системные логи через journalctl."""
    try:
        cmd = ["journalctl", "-n", str(limit), "--no-pager"]
        if unit:
            cmd.extend(["-u", unit])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        logs = result.stdout.split('\n')[:limit]
        return {
            "unit": unit or "system",
            "lines": len(logs),
            "logs": logs
        }
    except Exception as e:
        return {"error": str(e)}

def process_info() -> dict:
    """Получить топ-10 процессов по использованию CPU."""
    try:
        result = subprocess.run(
            ["ps", "aux", "--sort=-%cpu"],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        header = lines[0] if lines else ""
        processes = lines[1:11] if len(lines) > 1 else []
        return {
            "header": header,
            "processes": processes
        }
    except Exception as e:
        return {"error": str(e)}

def create_file(path: str, content: str, force: bool = False) -> dict:
    """
    Создать новый файл с указанным содержимым.
    Если файл существует и force=False — вернёт предупреждение.
    """
    try:
        if os.path.exists(path) and not force:
            return {
                "warning": f"Файл {path} уже существует!",
                "suggestion": "Используйте force=True для перезаписи или выберите другое имя"
            }
        
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            return {"error": f"Директория {directory} не существует. Создайте её сначала."}
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "message": f"✅ Файл {path} успешно создан",
            "path": path,
            "size": len(content),
            "lines": content.count('\n') + 1
        }
    except PermissionError:
        return {"error": f"Нет прав на запись в {path}"}
    except Exception as e:
        return {"error": str(e)}

TOOLS = [find_files, read_file, disk_usage, file_info, list_directory, system_logs, process_info, create_file]

# ========== 2. УМНЫЙ FALLBACK С RETRY ==========

def call_with_retry_and_fallback(contents, config, max_retries_per_model=2):
    """
    Пытается вызвать модели по очереди:
    - Сначала gemini-2.5-flash (с ретраями)
    - Если не получилось → gemini-2.0-flash
    - Если и так → gemini-1.5-flash
    """
    last_error = None
    
    for model_idx, model_name in enumerate(MODELS_PRIORITY):
        for attempt in range(max_retries_per_model + 1):
            try:
                logger.info(f"🔄 Попытка {attempt + 1} с моделью {model_name}")
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )
                
                logger.info(f"✅ Успех с моделью {model_name}")
                return response, model_name
                
            except Exception as e:
                error_str = str(e)
                logger.warning(f"❌ Ошибка с {model_name}: {error_str[:100]}")
                last_error = e
                
                # Если ошибка 429 (лимит) или 503 (перегрузка) — ждём и ретраим
                if "429" in error_str or "503" in error_str:
                    wait_time = (attempt + 1) * 5  # 5, 10, 15 секунд
                    logger.info(f"⏳ Ждём {wait_time} сек перед ретраем...")
                    time.sleep(wait_time)
                    continue
                else:
                    # Другие ошибки — сразу переключаем модель
                    break
        
        logger.info(f"📉 Переключаемся на следующую модель (было: {model_name})")
        time.sleep(2)  # Пауза между сменой модели
    
    # Если все модели не сработали
    raise Exception(f"Все модели недоступны. Последняя ошибка: {last_error}")

# ========== 3. НАСТРОЙКА GEMINI CLIENT ==========
API_KEY = os.environ.get("G_API_KEY")
if not API_KEY:
    raise ValueError("❌ Переменная окружения G_API_KEY не установлена!")

client = genai.Client(api_key=API_KEY)

# Флаг для отслеживания текущей модели (для логов)
current_model = MODELS_PRIORITY[0]

SYSTEM_INSTRUCTION = f"""
Ты — экспертный AI-агент, специализированный на диагностике и управлении файловой системой Linux.
Твоя цель — помогать пользователю (kz444gron) в рамках учебного курса "Операционные системы" и не только  (КазНУ 2026).

КОНТЕКСТ ОКРУЖЕНИЯ:
- Текущий пользователь: kz444gron
- Домашняя директория: /home/kz444gron
- Рабочая область ОС: /home/kz444gron/os-kaznu-2026
- Структура курса: Папки hw01-07 (домашние задания) и lab01-08 (лабораторные работы).

ПРАВИЛА ПОВЕДЕНИЯ:
1. Язык: Всегда отвечай на русском языке. Тон профессиональный, лаконичный.
2. Пути: Если пользователь упоминает "домашнюю папку" или "папку курса", всегда используй полные абсолютные пути (/home/kz444gron/...).
3. Безопасность: 
   - Перед созданием файла (create_file) проверь список файлов в директории.
   - Если файл уже существует, ОБЯЗАТЕЛЬНО спроси подтверждение.
4. Прозрачность: Перед вызовом любого инструмента кратко напиши, что собираешься сделать.
5. Теория ОС: Если вопрос касается теории (процессы, потоки, дедлоки, inode), отвечай развернуто, опираясь на академические знания.
6. Оформление: Используй Markdown для оформления кода, путей и логов.

ДОСТУПНЫЕ ИНСТРУМЕНТЫ:
- find_files(directory, pattern) — поиск файлов по шаблону
- read_file(path, max_chars) — чтение содержимого файла
- disk_usage(path) — использование диска (df)
- file_info(path) — метаданные файла (inode, права)
- list_directory(path) — содержимое директории (ls)
- system_logs(limit, unit) — системные логи (journalctl)
- process_info() — топ процессов по CPU (ps aux)
- create_file(path, content, force) — создание файла (force=True для перезаписи)
"""

CONFIG = types.GenerateContentConfig(
    tools=TOOLS,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    system_instruction=SYSTEM_INSTRUCTION
)

# ========== 4. AGENT LOOP ==========
async def run_agent(user_input: str, history=None):
    """Запускает агента с историей диалога и умным fallback между моделями"""
    global current_model
    
    if history is None:
        history = []
    
    history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)]
    ))

    for step in range(8):
        try:
            # Вызываем API с ретраями и fallback между моделями
            response, used_model = call_with_retry_and_fallback(history, CONFIG)
            current_model = used_model
            
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
            return f"❌ Ошибка API: {str(e)[:200]}\n\n💡 Попробуйте позже или используйте другую команду.", history
        
        history.append(response.candidates[0].content)
        
        function_calls = []
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_calls.append(part.function_call)
        
        if not function_calls:
            return response.text, history
        
        tool_results = []
        for call in function_calls:
            logger.info(f"🔧 Вызов: {call.name}({call.args})")
            
            func = globals().get(call.name)
            if func:
                try:
                    result = func(**call.args)
                except Exception as e:
                    result = {"error": f"Ошибка выполнения: {str(e)}"}
            else:
                result = {"error": f"Инструмент {call.name} не найден"}
            
            tool_results.append(types.Part.from_function_response(
                name=call.name,
                response={"result": result}
            ))
        
        history.append(types.Content(role="user", parts=tool_results))
    
    return "⚠️ Превышено максимальное количество шагов.", history

# ========== 5. TELEGRAM BOT ==========
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = []
    await update.message.reply_text(
        "🤖 *Linux FS AI Agent*\n\n"
        "Я — AI-агент для диагностики операционной системы Linux.\n\n"
        f"✨ *Текущая модель:* `{current_model}`\n"
        "🔄 При ошибках автоматически переключаюсь на более стабильные версии.\n\n"
        "📋 *Команды:*\n"
        "/start — приветствие\n"
        "/help — подробная справка\n"
        "/tools — список инструментов\n"
        "/clear — очистить историю\n"
        "/model — показать текущую модель\n\n"
        "Просто напишите ваш вопрос на русском языке.",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 *Примеры запросов:*\n\n"
        "*Теория ОС:*\n"
        "• Что такое inode?\n"
        "• Объясни разницу между процессом и потоком\n"
        "• Что такое deadlock и как его избежать?\n\n"
        "*Работа с файлами:*\n"
        "• Найди все .py файлы в моей домашней директории\n"
        "• Покажи содержимое /etc/passwd\n"
        "• Сколько свободного места на диске?\n\n"
        "*Создание файлов:*\n"
        "• Создай в lab08 файл ai.py с содержимым print('Hello')\n\n"
        "*Анализ системы:*\n"
        "• Покажи топ процессов по CPU\n"
        "• Последние ошибки в системных логах ssh",
        parse_mode="Markdown"
    )

async def tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠️ *Доступные инструменты:*\n\n"
        "1. `find_files` — поиск файлов по шаблону\n"
        "2. `read_file` — чтение содержимого файла\n"
        "3. `disk_usage` — использование диска\n"
        "4. `file_info` — метаданные (inode, права)\n"
        "5. `list_directory` — содержимое папки\n"
        "6. `system_logs` — системные логи\n"
        "7. `process_info` — топ процессов по CPU\n"
        "8. `create_file` — создание файла\n\n"
        "⚠️ *Безопасность:* перед созданием файла проверяю, не существует ли он!",
        parse_mode="Markdown"
    )

async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать текущую активную модель"""
    await update.message.reply_text(
        f"✨ *Текущая модель:* `{current_model}`\n\n"
        f"📋 *Доступные модели в порядке приоритета:*\n"
        f"1. `{MODELS_PRIORITY[0]}` — самая новая (строгие лимиты)\n"
        f"2. `{MODELS_PRIORITY[1]}` — хороший баланс\n"
        f"3. `{MODELS_PRIORITY[2]}` — самая стабильная\n\n"
        f"🔄 При ошибках автоматически переключаюсь на следующую модель.",
        parse_mode="Markdown"
    )

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = []
    await update.message.reply_text("🧹 История диалога очищена!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    await update.message.chat.send_action(action="typing")
    
    history = user_sessions.get(user_id, [])
    
    try:
        response_text, new_history = await run_agent(user_text, history)
        user_sessions[user_id] = new_history
        
        if len(response_text) > 4000:
            for i in range(0, len(response_text), 4000):
                await update.message.reply_text(response_text[i:i+4000])
        else:
            await update.message.reply_text(response_text)
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"❌ Внутренняя ошибка: {str(e)[:200]}")

# ========== 6. ЗАПУСК ==========
def main():
    TELEGRAM_TOKEN = os.environ.get("TEL_TOKEN")
    if not TELEGRAM_TOKEN:
        print("❌ Переменная окружения TEL_TOKEN не установлена!")
        print("   export TEL_TOKEN='ваш_токен_от_BotFather'")
        return
    
    print("=" * 60)
    print("🤖 Linux FS AI Agent — Финальный проект КазНУ 2026")
    print("=" * 60)
    print(f"📋 Доступные модели (приоритет):")
    for i, model in enumerate(MODELS_PRIORITY, 1):
        print(f"   {i}. {model}")
    print(f"🛠️ Инструментов: {len(TOOLS)}")
    print(f"🔑 API Key: {'✅ OK' if API_KEY else '❌ MISSING'}")
    print(f"🤖 Bot Token: {'✅ OK' if TELEGRAM_TOKEN else '❌ MISSING'}")
    print("=" * 60)
    print("✅ Бот запущен!")
    print("=" * 60)
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("tools", tools_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("model", model_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
