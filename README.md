# 🍌 Nanobanana - Бот для генерации картинок

Telegram-бот для генерации изображений по текстовому описанию.

## 🚀 Возможности

- Генерация изображений по текстовому описанию
- Поддержка различных API для генерации:
  - **Google Gemini Nano Banana** (по умолчанию) - быстрая генерация изображений
  - OpenAI DALL-E
  - Stability AI
  - Replicate
- Простой и интуитивный интерфейс
- Placeholder режим для тестирования без API ключей

## 📋 Требования

- Python 3.8+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- (Опционально) API ключ для выбранного сервиса генерации изображений

## 🛠️ Установка

1. Клонируйте репозиторий или создайте проект:
```bash
cd nanobanana
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
```

Отредактируйте файл `.env` и укажите:
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `IMAGE_API_TYPE` - тип API (nanobanana, gemini, openai, stability, replicate, placeholder)
- `GEMINI_API_KEY` - API ключ для Gemini/Nano Banana (если используется)
- `IMAGE_API_KEY` - API ключ для других сервисов (если требуется)

## 🎯 Использование

1. Запустите бота:
```bash
python src/bot.py
```

2. Найдите вашего бота в Telegram и отправьте команду `/start`

3. Отправьте текстовое описание картинки, которую хотите создать

## 🔧 Настройка API

### Google Imagen 4.0 (рекомендуется)
1. Получите API ключ на [Google AI Studio](https://aistudio.google.com/apikey)
2. Установите в `.env`:
   - `IMAGE_API_TYPE=nanobanana` (или `gemini`)
   - `GEMINI_API_KEY=your_gemini_api_key`
3. Используется модель `imagen-4.0-generate-001` для генерации высококачественных изображений

### Placeholder режим
Создает простые изображения с текстом. Не требует API ключей. Подходит для тестирования.

### OpenAI DALL-E
1. Установите библиотеку: `pip install openai`
2. Получите API ключ на [platform.openai.com](https://platform.openai.com)
3. Установите в `.env`:
   - `IMAGE_API_TYPE=openai`
   - `IMAGE_API_KEY=your_openai_api_key`

### Stability AI
1. Установите библиотеку: `pip install stability-sdk`
2. Получите API ключ на [platform.stability.ai](https://platform.stability.ai)
3. Установите в `.env`:
   - `IMAGE_API_TYPE=stability`
   - `IMAGE_API_KEY=your_stability_api_key`

### Replicate
1. Установите библиотеку: `pip install replicate`
2. Получите API токен на [replicate.com](https://replicate.com)
3. Установите в `.env`:
   - `IMAGE_API_TYPE=replicate`
   - `IMAGE_API_KEY=your_replicate_token`

## 📁 Структура проекта

```
nanobanana/
├── src/
│   ├── bot.py              # Основной файл бота
│   └── image_generator.py  # Модуль генерации изображений
├── images/                 # Директория для сгенерированных изображений
├── logs/                   # Директория для логов
├── config/                 # Конфигурационные файлы
├── .env.example           # Пример файла с переменными окружения
├── .gitignore             # Git ignore файл
├── requirements.txt       # Зависимости проекта
└── README.md              # Документация
```

## 🐛 Решение проблем

- **Бот не отвечает**: Проверьте правильность токена в `.env`
- **Ошибка генерации**: Убедитесь, что API ключ указан правильно и у вас есть доступ к выбранному сервису
- **Ошибки импорта**: Убедитесь, что все зависимости установлены (`pip install -r requirements.txt`)

## 📝 Лицензия

MIT

## 🤝 Вклад

Приветствуются любые улучшения и предложения!
