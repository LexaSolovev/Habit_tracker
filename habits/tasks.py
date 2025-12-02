from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import Habit
import requests
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_reminder():
    """Отправка напоминаний в Telegram"""
    now = timezone.now()
    current_time = now.time()

    # Находим привычки, которые нужно выполнить сейчас
    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    )

    for habit in habits:
        if habit.user.telegram_chat_id:
            message = create_reminder_message(habit)
            send_telegram_message(habit.user.telegram_chat_id, message)


def create_reminder_message(habit):
    """Создание сообщения для напоминания"""
    base_message = f"🔔 Напоминание о привычке!\n\nЯ буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}"

    if habit.reward:
        base_message += f"\n\nВознаграждение: {habit.reward}"
    elif habit.related_habit:
        base_message += f"\n\nПосле этого: {habit.related_habit.action}"

    base_message += f"\n\nВремя на выполнение: {habit.estimated_duration} секунд"
    return base_message


def send_telegram_message(chat_id, message):
    """Отправка сообщения через Telegram Bot API"""
    bot_token = settings.TELEGRAM_BOT_TOKEN

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        logger.info(f"Message sent to {chat_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
