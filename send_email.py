#!/usr/bin/env python
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import sys

from craigslist import getCraigslistPosts

yesterday = date.today() - timedelta(1)
yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)

emailMessage = getCraigslistPosts(yesterday)

CREDENTIALS = {
    "smtp_server": os.environ.get('smtp_server'),
    "smtp_port": os.environ.get('smtp_port'),
    "smtp_username": os.environ.get('smtp_username'),
    "smtp_password": os.environ.get('smtp_password'),

    "email_from": os.environ.get('email_from'),
    "email_to": os.environ.get('email_to'),
}

# set up the SMTP server
try:
    server = smtplib.SMTP(host=CREDENTIALS['smtp_server'], port=CREDENTIALS['smtp_port'])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(CREDENTIALS['smtp_username'], CREDENTIALS['smtp_password'])
    print('Successful SMTP connection.')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily Craigslist Report"
    msg['From'] = CREDENTIALS['email_from']
    msg['To'] = CREDENTIALS['email_to']

    part1 = MIMEText(emailMessage, 'plain')
    part2 = MIMEText(emailMessage, 'html')

    msg.attach(part1)
    msg.attach(part2)
    server.sendmail(CREDENTIALS['email_from'], CREDENTIALS['email_to'], msg.as_string())
    print('Message Sent!')

except Exception as e:
    print('Exception: ')
    print(e)
    sys.exit(1)

server.quit()