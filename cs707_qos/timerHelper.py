from datetime import date
import datetime
from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler()
sched.start()

# Define the function that is to be executed
def my_job(text):
    print text

# The job will be executed on November 6th, 2009
exec_date = date(2009, 11, 6)

# Store the job in a variable in case we want to cancel it
job = sched.add_date_job(my_job, exec_date, ['text'])

# The job will be executed on November 6th, 2009 at 16:30:05
job = sched.add_date_job(my_job, datetime(2009, 11, 6, 16, 30, 5), ['text'])