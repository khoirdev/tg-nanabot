"""
Модуль для генерации изображений
Поддерживает различные API для генерации картинок
"""
import os
import asyncio
import logging
from typing import Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Класс для генерации изображений"""
    
    def __init__(self):
        self.output_dir = Path(__file__).parent.parent / "images"
        self.output_dir.mkdir(exist_ok=True)
        
        # Настройки генерации
        self.api_type = os.getenv('IMAGE_API_TYPE', 'placeholder')  # placeholder, openai, stability, replicate, gemini, nanobanana
        self.api_key = os.getenv('IMAGE_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')
        
        logger.info(f"ImageGenerator инициализирован с API типом: {self.api_type}")
    
    async def generate(self, prompt: str, user_id: int) -> Optional[str]:
        """
        Генерирует изображение по текстовому описанию
        
        Args:
            prompt: Текстовое описание желаемого изображения
            user_id: ID пользователя для организации файлов
        
        Returns:
            Путь к сгенерированному изображению или None в случае ошибки
        """
        try:
            # Генерируем уникальное имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{user_id}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Выбираем метод генерации в зависимости от API типа
            if self.api_type in ['gemini', 'nanobanana']:
                await self._generate_gemini(prompt, filepath)
            elif self.api_type == 'openai':
                await self._generate_openai(prompt, filepath)
            elif self.api_type == 'stability':
                await self._generate_stability(prompt, filepath)
            elif self.api_type == 'replicate':
                await self._generate_replicate(prompt, filepath)
            else:
                # Placeholder - создаем простую заглушку
                await self._generate_placeholder(prompt, filepath)
            
            return str(filepath) if filepath.exists() else None
        
        except Exception as e:
            logger.error(f"Ошибка при генерации изображения: {e}", exc_info=True)
            return None
    
    async def _generate_placeholder(self, prompt: str, filepath: Path):
        """Создает placeholder изображение (для тестирования)"""
        from PIL import Image, ImageDraw, ImageFont
        
        # Создаем простое изображение с текстом
        img = Image.new('RGB', (512, 512), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Пытаемся использовать системный шрифт
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Разбиваем текст на строки
        words = prompt.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < 450:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Рисуем текст по центру
        y = 200
        for line in lines[:5]:  # Максимум 5 строк
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (512 - text_width) // 2
            draw.text((x, y), line, fill='black', font=font)
            y += 40
        
        # Сохраняем изображение
        img.save(filepath)
        logger.info(f"Placeholder изображение создано: {filepath}")
    
    async def _generate_openai(self, prompt: str, filepath: Path):
        """Генерация через OpenAI DALL-E API"""
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.api_key)
            
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Скачиваем изображение
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        with open(filepath, 'wb') as f:
                            f.write(await resp.read())
                        logger.info(f"Изображение сгенерировано через OpenAI: {filepath}")
            
        except ImportError:
            logger.error("Библиотека openai не установлена")
            await self._generate_placeholder(prompt, filepath)
        except Exception as e:
            logger.error(f"Ошибка при генерации через OpenAI: {e}")
            await self._generate_placeholder(prompt, filepath)
    
    async def _generate_stability(self, prompt: str, filepath: Path):
        """Генерация через Stability AI API"""
        try:
            import stability_sdk.client
            from stability_sdk import client
            
            stability_api = client.StabilityInference(
                key=self.api_key,
                verbose=True,
            )
            
            answers = stability_api.generate(prompt=prompt)
            
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == client.generation.FINISH_REASON_SUCCESS:
                        with open(filepath, 'wb') as f:
                            f.write(artifact.binary)
                        logger.info(f"Изображение сгенерировано через Stability AI: {filepath}")
                        return
            
            await self._generate_placeholder(prompt, filepath)
        
        except ImportError:
            logger.error("Библиотека stability-sdk не установлена")
            await self._generate_placeholder(prompt, filepath)
        except Exception as e:
            logger.error(f"Ошибка при генерации через Stability AI: {e}")
            await self._generate_placeholder(prompt, filepath)
    
    async def _generate_replicate(self, prompt: str, filepath: Path):
        """Генерация через Replicate API"""
        try:
            import replicate
            
            output = replicate.run(
                "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                input={"prompt": prompt}
            )
            
            # Скачиваем изображение
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(output[0]) as resp:
                    if resp.status == 200:
                        with open(filepath, 'wb') as f:
                            f.write(await resp.read())
                        logger.info(f"Изображение сгенерировано через Replicate: {filepath}")
        
        except ImportError:
            logger.error("Библиотека replicate не установлена")
            await self._generate_placeholder(prompt, filepath)
        except ImportError:
            logger.error("Библиотека replicate не установлена")
            await self._generate_placeholder(prompt, filepath)
        except Exception as e:
            logger.error(f"Ошибка при генерации через Replicate: {e}")
            await self._generate_placeholder(prompt, filepath)
    
    async def _generate_gemini(self, prompt: str, filepath: Path):
        """Генерация через Google Gemini API (Nano Banana / Imagen через Gemini)"""
        try:
            from google import genai
            from google.genai import types
            import asyncio
            
            # Проверяем наличие API ключа
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY не установлен в переменных окружения")
            
            logger.info(f"Используется API ключ: {self.api_key[:10]}...{self.api_key[-5:] if len(self.api_key) > 15 else '***'}")
            
            # Инициализируем клиент с API ключом
            client = genai.Client(api_key=self.api_key)
            
            # Используем Gemini модель с поддержкой генерации изображений
            # gemini-2.5-flash-image - быстрая модель для генерации изображений
            # gemini-3-pro-image-preview - профессиональная модель с расширенными возможностями
            if self.api_type == 'nanobanana':
                model_name = 'gemini-2.5-flash-image'  # Nano Banana
            else:
                model_name = 'gemini-3-pro-image-preview'  # Nano Banana Pro
            
            logger.info(f"Генерация изображения через Gemini API с моделью: {model_name}, промпт: {prompt}")
            
            # Генерируем изображение через Gemini API с указанием модальностей ответа
            # Метод generate_content может быть синхронным, поэтому запускаем в executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model=model_name,
                    contents=[prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE'],
                        image_config=types.ImageConfig(
                            aspect_ratio='1:1',  # Можно изменить: "1:1", "16:9", "9:16", "4:3", "3:4"
                            image_size='1K'  # Можно изменить: "1K", "2K", "4K" (только для gemini-3-pro-image-preview)
                        )
                    )
                )
            )
            
            logger.info(f"Получен ответ от API, количество частей: {len(response.parts) if response.parts else 0}")
            
            # Обрабатываем части ответа
            image_found = False
            for part in response.parts:
                if part.text is not None:
                    logger.info(f"Текстовый ответ от API: {part.text}")
                elif part.inline_data is not None:
                    # Получаем изображение из inline_data
                    try:
                        image = part.as_image()
                        if image:
                            image.save(filepath)
                            logger.info(f"Изображение успешно сгенерировано через Gemini API и сохранено: {filepath}")
                            image_found = True
                            break
                        else:
                            logger.warning("Метод as_image() вернул None")
                    except Exception as e:
                        logger.error(f"Ошибка при получении изображения через as_image(): {e}")
                        # Пытаемся альтернативный способ
                        try:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # Сохраняем напрямую из inline_data
                                import base64
                                from PIL import Image
                                from io import BytesIO
                                
                                image_data = part.inline_data.data
                                if isinstance(image_data, str):
                                    # Если это base64 строка
                                    image_bytes = base64.b64decode(image_data)
                                else:
                                    image_bytes = image_data
                                
                                img = Image.open(BytesIO(image_bytes))
                                img.save(filepath)
                                logger.info(f"Изображение сохранено через альтернативный метод: {filepath}")
                                image_found = True
                                break
                        except Exception as e2:
                            logger.error(f"Ошибка при альтернативном сохранении: {e2}")
            
            if not image_found:
                raise ValueError("API не вернул изображений в ответе")
        
        except ImportError:
            logger.error("Библиотека google-genai не установлена. Установите: pip install google-genai")
            await self._generate_placeholder(prompt, filepath)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Ошибка при генерации через Gemini API: {e}", exc_info=True)
            logger.error(f"Тип ошибки: {type(e).__name__}, Детали: {str(e)}")
            
            # Проверяем, является ли это ошибкой доступа
            if "403" in error_msg or "Forbidden" in error_msg or "permission" in error_msg.lower():
                logger.error(
                    "⚠️ ОШИБКА ДОСТУПА: Ваш API ключ не имеет разрешения на использование моделей генерации изображений.\n"
                    "Возможные решения:\n"
                    "1. Убедитесь, что API ключ создан в Google AI Studio (https://aistudio.google.com/apikey)\n"
                    "2. Проверьте, что модели генерации изображений доступны в вашем регионе\n"
                    "3. Возможно, требуется включить billing в Google Cloud Console\n"
                    "4. Попробуйте использовать другой API для генерации изображений (OpenAI DALL-E, Stability AI, Replicate)"
                )
            
            # Используем placeholder только в крайнем случае
            logger.warning("Переключение на placeholder режим из-за ошибки API")
            await self._generate_placeholder(prompt, filepath)
