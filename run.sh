#!/bin/bash
# Skrip untuk menjalankan bot Nanobanana

cd "$(dirname "$0")"
source venv/bin/activate
python src/bot.py
