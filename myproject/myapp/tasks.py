# myapp/tasks.py
from celery import shared_task
from addingBot.main import main

@shared_task
def start_bot_recording(id):
    main(id)
