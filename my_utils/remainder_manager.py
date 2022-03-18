from crontab import CronTab
from datetime import datetime
from Assistant import Assistant

import pickle
import subprocess
import datetime
import os

from google_reminder_api_wrapper import ReminderApi

def set_local_remainder(dt, body):
    cron = CronTab(user='jafarabbas33')
    cmd = f'export DISPLAY=":0" XDG_RUNTIME_DIR="/run/user/1000"; /home/jafarabbas33/bin/notifier "title=Reminder" "body={body}" "icon=dialog-information"'
    job = cron.new(command=cmd)
    job.setall(dt)
    cron.write()
    Assistant.logger.info(f'Setting reminder for {dt} with command: {cmd}')

def check_reminder():
    api = ReminderApi()
    reminders = api.list().get('task')

    if reminders != None:
        for reminder in reminders:
            due_date = reminder.get('dueDate')
            time = due_date['time']
            
            dt = datetime.datetime(due_date['year'], due_date['month'], due_date['day'], time['hour'], time['minute'], time['second'])

            set_local_remainder(dt, reminder.get('title'))
            api.delete(reminder.get('taskId').get('serverAssignedId'))
