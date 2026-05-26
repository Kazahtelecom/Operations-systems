#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from datetime import datetime
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === ПРОВЕРКА КЛЮЧЕЙ ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.environ.get("G_API_KEY")

if not BOT_TOKEN or not GEMINI_KEY:
    print("❌ Ошибка: установи переменные TELEGRAM_BOT_TOKEN и G_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_KEY)
MODEL = "gemini-2.5-flash"
MAX_STEPS = 10

# === ИНСТРУМЕНТЫ ===
def get_time() -> dict:
    return {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def system_info() -> dict:
    return {"os": subprocess.getoutput("uname -a"), "hostname": os.uname().nodename}

def process_list() -> dict:
    result = subprocess.run(["ps", "aux", "--sort=-%cpu"], capture_output=True, text=True, timeout=5)
    return {"top_processes": result.stdout.split('\n')[1:6]}

def disk_usage(path: str = "/") -> dict:
    import shutil
    try:
        total, used, free = shutil.disk_usage(path)
        gb = 1024**3
        return {
            "total_gb": round(total / gb, 2),
            "used_gb": round(used / gb, 2),
            "free_gb": round(free / gb, 2)
        }
    except Exception as e:
        return {"error": str(e)}
def find_files(directory: str, pattern: str) -> dict:
    import glob
    matches = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
    return {"files": matches[:10]}

def read_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return {"content": f.read(2000)}

def file_info(path: str) -> dict:
    st = os.stat(path)
    return {"size": st.st_size, "inode": st.st_ino}

def create_file(path: str, content: str) -> dict:
    with open(path, 'w') as f:
        f.write(content)
    return {"created": path}

def find_large_files(directory: str, min_mb: int = 10) -> dict:
    result = subprocess.run(f"find {directory} -type f -size +{min_mb}M 2>/dev/null | head -10", shell=True, capture_output=True, text=True, timeout=10)
    return {"files": result.stdout.strip().split('\n') if result.stdout else []}

TOOLS = {
    "get_time": get_time,
    "system_info": system_info,
    "process_list": process_list,
    "disk_usage": disk_usage,
    "find_files": find_files,
    "read_file": read_file,
    "file_info": file_info,
    "create_file": create_file,
    "find_large_files": find_large_files
}

# === ТЕЛЕГРАМ БОТ ===
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = []
    await update.message.reply_text("🤖 Linux FS AI Agent\n/help — команды\n/tools — список инструментов")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔧 Примеры:\n"
        "• Который час?\n"
        "• Информация о системе\n"
        "• Покажи топ процессов\n"
        "• Сколько места на диске?\n"
        "• Найди .py файлы"
    )

async def tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🛠 Доступно {len(TOOLS)} инструментов: {', '.join(TOOLS.keys())}")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = []
    await update.message.reply_text("🧹 История очищена")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    config = types.GenerateContentConfig(
        tools=list(TOOLS.values()),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
        system_instruction=(
            "Ты — Linux ассистент. У тебя есть инструменты. "
            "Когда пользователь спрашивает время — вызови get_time. "
            "Когда спрашивает информацию о системе — вызови system_info. "
            "Когда спрашивает процессы — вызови process_list. "
            "Когда спрашивает диск — вызови disk_usage. "
            "Никогда не говори 'я не могу' — просто вызови нужный инструмент!"
        )
    )

    history = user_sessions.get(user_id, [])
    history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_text)]))

    try:
        response = client.models.generate_content(model=MODEL, contents=history, config=config)
        await update.message.reply_text(response.text)
        user_sessions[user_id] = history + [response.candidates[0].content]
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)[:200]}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("tools", tools_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
