#pings a host every 60 seconds to see if it's online
#if host goes down (Request Timed out) it will send you a email
#smtp server manually set for GMAIL, change as necessary

import os
import smtplib
import time
import datetime
from sys import platform

#email variables
from_email_address = input('type in your gmail address (e.g. bighickjohnson@gmail.com): ')
to_email_address = from_email_address
smtp_server = 'smtp.gmail.com'
smtp_port = 587
email_password = input('type in your gmail password or app-specific password: ')

#query user for hostname to monitor
hostname = input('type in the IP address or hostname of the device to monitor: ')

#check operating system using platform module
operating_system=''

if platform == "linux" or platform == "linux2":
    operating_system = 'linux'
elif platform == "darwin":
    operating_system = 'osx'
elif platform == 'win32':
    operating_system = 'windows'

#function to ping hostname based on operating system, returns network status
def check_ping():
    if operating_system == 'windows':
        response = os.system("ping /n 1 " + hostname)
    elif operating_system == 'osx' or operating_system == 'linux':
        response = os.system("ping -c 1 " + hostname)
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    return pingstatus

#function to send email alert
def send_email_alert():
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(from_email_address, email_password)

    subject = hostname + " is offline"
    body = "Device " + hostname + " is offline, go check it out!!"
    msg = "Subject: " + subject + "\n" + "To: " + to_email_address + "\n\n" + body

    server.sendmail(from_email_address, to_email_address, msg)
    server.quit()
    now = datetime.datetime.now()
    print(now.strftime("[%Y-%m-%d %H:%M:%S]") + ' Email has been sent!!!')

while True:
    status = check_ping()
    now = datetime.datetime.now()
    if status == "Network Active":
        print(now.strftime("[%Y-%m-%d %H:%M:%S]") + ' Host is up, no action necessary')
        time.sleep(60)

    if status == "Network Error":
        print(now.strftime("[%Y-%m-%d %H:%M:%S]") + ' Host is down, sending email alert...')
        send_email_alert()
        print(now.strftime("[%Y-%m-%d %H:%M:%S]") + ' quitting script...')
        exit()
