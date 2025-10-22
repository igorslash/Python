"""Telegram-бот для взаимодействия с Insurance AI Agent.

Для запуска:
    1. токен у @BotFather в Telegram.
    2. Установите переменную окружения: export TELEGRAM_BOT_TOKEN='your_token'
    3. Выполните: python telegram_bot.py

Бот реагирует только на текстовые сообщения
и возвращает структурированный ответ.
"""

import os
import logging
import asyncio
from typing import Any, Dict
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from agent import InsuranceAgent


# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Инициализация агента (один на всё приложение)
AGENT = InsuranceAgent()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает входящее текстовое сообщение от пользователя."""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    user_id = update.effective_user.id
    logger.info(f"Получено сообщение от {user_id}: {user_text[:50]}...")

    try:
        # Обработка через агент
        result: Dict[str, Any] = AGENT.process(text=user_text)

        # Формируем человекочитаемый ответ
        response = _format_response(result)

    except Exception as e:
        logger.exception("Ошибка при обработке сообщения")
        response = (
            "Извините, произошла ошибка при обработке вашего запроса. "
            "Попробуйте переформулировать сообщение."
        )

    # Отправляем ответ
    await update.message.reply_text(response, parse_mode="Markdown")


def _format_response(result: Dict[str, Any]) -> str:
    """Преобразует результат агента в человекочитаемый формат для Telegram."""
    task = result["task"]
    data = result["result"]
    lang = result["language"]

    if task == "insurance_recommendation":
        product = data.get("product")
        if not product:
            return "❌ Не удалось подобрать страховку по вашему запросу."
        alt_count = len(data.get("alternatives", []))
        resp = (
            f"✅ *Рекомендуемый продукт:*\n"
            f"*{product['name']}* (`{product['id']}`)\n"
            f"{product['description']}\n"
            f"Цена: от {product['price_range'][0]} до "
            f"{product['price_range'][1]} {product['currency']}\n"
        )
        if alt_count > 0:
            resp += f"\nℹ️ Найдено ещё {alt_count} альтернатив(а)."
        return resp

    elif task == "sentiment_analysis":
        sentiment = data["sentiment"]
        score = data["score"]
        emoji = {"positive": "😊", "negative": "😞", "neutral": "😐"}.get(sentiment, "❓")
        return f"{emoji} Тональность: *{sentiment}* (уверенность: {score:.2f})"

    elif task == "support_classification":
        label = data["label"]
        score = data["score"]
        labels_ru = {
            "insurance": "страховка",
            "support": "техподдержка",
            "complaint": "жалоба",
            "other": "прочее",
        }
        category = labels_ru.get(label, label)
        return f"📥 Категория обращения: *{category}* ({score:.2f})"

    elif task == "ner":
        entities = data.get("entities", [])
        if not entities:
            return "🔍 Сущности не найдены."
        items = [f"`{e['text']}` → `{e['label']}`" for e in entities[:5]]
        return "🔤 Найденные сущности:\n" + "\n".join(items)

    else:
        return f"⚙️ Обработано как `{task}` (язык: {lang})"


async def main() -> None:
    """Запускает Telegram-бота."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise EnvironmentError(
            "Переменная окружения TELEGRAM_BOT_TOKEN не установлена."
        )

    application = Application.builder().token(token).build()

    # Обрабатываем только текст
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен. Ожидание сообщений...")
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())