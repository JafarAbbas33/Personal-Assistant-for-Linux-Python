# from crontab import CronTab
from datetime import datetime
import pickle


def save_and_load(file_name, data = None):
    if data == None:
        with open(file_name, 'rb') as f:
            return(pickle.loads(f.read()))
    
    with open(file_name, 'wb') as f:
        f.write(pickle.dumps(data))


def check_remainder():
    time_diff = datetime(2022, 3, 12, 12, 59) - datetime.now()
    pass



def create_job():
    cron = CronTab(user='jafarabbas33')
    if __name__ == '__main__':
        job = cron.new(command='mkdir ~/Desktop/main')
    else:
        job = cron.new(command='mkdir ~/Desktop/not_main')
    job.setall(datetime(2022, 3, 12, 12, 5))
    cron.write()

def delete_job():
    cron = CronTab(user='jafarabbas33')
    for job in cron:
        print(job)
    
##    cron.remove( job )
##    cron.remove_all('echo')
##    cron.remove_all(comment='foo')
##    cron.remove_all(time='*/2')
##
##
##    cron = CronTab(user='jafarabbas33')
##    job = cron.new(command='echo hello_world2')
##    job.setall(datetime(2022, 3, 12, 12, 5))
##    cron.write()

#delete_job()
#create_job()
        
if __name__ == '__main__':
    check_remainder()
