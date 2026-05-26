"""
Nanobanana - Бот для генерации картинок
Основной модуль бота
"""
import os
import logging
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from image_generator import ImageGenerator

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class NanobananaBot:
    """Основной класс бота для генерации картинок"""
    
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
        
        self.image_generator = ImageGenerator()
        self.application = Application.builder().token(self.token).build()
        self._register_handlers()
    
    def _register_handlers(self):
        """Регистрация обработчиков команд и сообщений"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_message = (
            "Привет, сладкая! ❤️\n\n"
            "Опиши картинку, которую хочешь создать, как можно подробнее.\n\n"
            "Полезные советы по составлению запроса /help"
        )
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = (
            "📖 Справка по использованию бота:\n\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать эту справку\n\n"
            "💡 Как использовать:\n"
            "Отправь текстовое описание картинки, которую хочешь создать. "
            "Укажи максимум деталей и уточнений (подробное описание объекта, кто в фокусе, "
            "детально опиши сцену, что в кадре, какой фон, какие предметы, какое освещение, "
            "время суток, погода, настроение картинки, отсылки).\n\n"
            "🌐 Переводи на английский: Gemini лучше понимает английские промпты.\n\n"
            "🎨 Всегда указывай стиль: photorealistic/anime/painting.\n\n"
            "👤 Для портретов и людей:\n"
            "{запрос}, photorealistic portrait, detailed facial features, professional studio lighting, sharp eyes, high quality\n\n"
            "🛍️ Для продуктов и e-commerce:\n"
            "{запрос}, product photography, clean white background, professional lighting, high detail, commercial quality\n\n"
            "🎭 Для концепт-арта и креатива:\n"
            "{запрос}, concept art style, detailed composition, cinematic lighting, high quality\n\n"
            "⚡ Для быстрых/черновых генераций:\n"
            "{запрос}, clear composition, good lighting\n\n"
            "🎨 Стиль:\n"
            "• photorealistic — для реалистичных фото\n"
            "• anime style — для аниме\n"
            "• oil painting — для живописи\n"
            "• 3D render — для 3D графики\n\n"
            "✨ Качество:\n"
            "• high quality, detailed\n"
            "• sharp focus — четкие детали\n\n"
            "💡 Освещение:\n"
            "• professional lighting\n"
            "• natural light / studio lighting\n"
            "• golden hour / sunset"
        )
        await update.message.reply_text(help_text)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_message = update.message.text
        user_id = update.effective_user.id
        
        logger.info(f"Получен запрос от пользователя {user_id}: {user_message}")
        
        # Отправляем сообщение о начале генерации
        status_message = await update.message.reply_text(
            "🎨 Генерирую картинку... Пожалуйста, подожди."
        )
        
        try:
            # Генерируем изображение
            image_path = await self.image_generator.generate(user_message, user_id)
            
            if image_path and os.path.exists(image_path):
                # Отправляем сгенерированное изображение
                with open(image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"✨ Вот твоя картинка!\n📝 Запрос: {user_message}"
                    )
                await status_message.delete()
                logger.info(f"Картинка успешно сгенерирована для пользователя {user_id}")
            else:
                await status_message.edit_text(
                    "❌ Произошла ошибка при генерации картинки. Попробуй еще раз."
                )
                logger.error(f"Не удалось сгенерировать картинку для пользователя {user_id}")
        
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {e}", exc_info=True)
            error_msg = str(e)
            
            # Более информативное сообщение об ошибке доступа
            if "403" in error_msg or "Forbidden" in error_msg or "permission" in error_msg.lower():
                await status_message.edit_text(
                    "❌ Ошибка доступа к API генерации изображений.\n\n"
                    "Ваш API ключ не имеет разрешения на использование моделей генерации изображений Google.\n\n"
                    "Возможные решения:\n"
                    "• Проверьте настройки API ключа в Google AI Studio\n"
                    "• Убедитесь, что billing включен (если требуется)\n"
                    "• Попробуйте использовать другой API для генерации изображений"
                )
            else:
                await status_message.edit_text(
                    f"❌ Произошла ошибка: {error_msg[:100]}\n\nПожалуйста, попробуй позже."
                )
    
    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота Nanobanana...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot = NanobananaBot()
    bot.run()
