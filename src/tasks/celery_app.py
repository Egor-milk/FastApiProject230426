from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks" #путь к таскам
    ]
)

celery_instance.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_today_checkin",
        "schedule": crontab(hour=8, minute=0),
    }
}
#  celery -A src.tasks.celery_app:celery_instance beat -l INFO