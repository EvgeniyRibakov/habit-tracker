from celery import shared_task
from django.utils import timezone
from .models import Habit, Profile
from telegram_bot.bot import send_telegram_message
import asyncio


@shared_task
def send_habit_reminders():
    now = timezone.now()
    current_time = now.time()
    habits = Habit.objects.filter(time__hour=current_time.hour, time__minute=current_time.minute)
    for habit in habits:
        days_since_creation = (now.date() - habit.created_at.date()).days
        if days_since_creation % habit.periodicity == 0:
            try:
                profile = Profile.objects.get(user=habit.user)
                if profile.telegram_id:
                    message = f"Reminder: Time to {habit.action} at {habit.place}!"
                    asyncio.run(send_telegram_message(profile.telegram_id, message))
            except Profile.DoesNotExist:
                print(f"No profile found for user {habit.user.username}")
