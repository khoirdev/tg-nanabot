# Инструкция по загрузке проекта на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните:
   - Repository name: `nanobanana` (или другое имя на ваш выбор)
   - Description: "Telegram bot for image generation using Gemini API"
   - Выберите Public или Private
   - НЕ добавляйте README, .gitignore или license (они уже есть в проекте)
3. Нажмите "Create repository"

## Шаг 2: Добавьте remote и загрузите код

После создания репозитория GitHub покажет инструкции. Выполните следующие команды:

```bash
cd /home/workshopai/nanobanana

# Добавьте remote (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/nanobanana.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Загрузите код на GitHub
git push -u origin main
```

## Альтернативный способ через SSH

Если вы используете SSH ключи:

```bash
git remote add origin git@github.com:YOUR_USERNAME/nanobanana.git
git branch -M main
git push -u origin main
```

## Проверка

После загрузки проверьте, что:
- ✅ Файл `.env` НЕ загружен (он в .gitignore)
- ✅ Все остальные файлы проекта загружены
- ✅ README.md отображается на странице репозитория

## Важно!

⚠️ **Никогда не загружайте файл `.env` в репозиторий** - он содержит ваши личные API ключи!
Файл `.env.example` уже включен как шаблон для других разработчиков.
