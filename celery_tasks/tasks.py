from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

#使用celery发送邮件

#创建一个Celery对象
app=Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/5')

#创建任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮件'''
    subject = '天天生鲜欢迎信息'
    message = ''
    #发件人
    sender = settings.EMAIL_FROM
    #接收邮件的列表
    receiver = [to_email]
    html_message = '<h1>%s,欢迎你成为天天生鲜的会员</h1>请点击下面的连接激活你的帐号</br><a href="http://127.0.0.1:8000/user/active/%s">%s</a>'%(username,token,token)
    send_mail(subject,message,sender,receiver,html_message=html_message)
    time.sleep(5)

