This cronjob folder is only needed in pythonanywhere free hosting
here we needed separate scripts which will be executed by pythonanywhere daily at one time
we have two scheduled tasks in our app in cronjob_handlers.py which apscheduler in wsgi.py execute
but in pythonanywhere background threading of scheduler not supported
so instead we only using  one scheduled task as we are limited to it and give path to Schedule Task feature to our file.