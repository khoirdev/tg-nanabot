#!/bin/bash
# Скрипт для запуска бота Nanobanana

cd "$(dirname "$0")"
source venv/bin/activate
python src/bot.py
