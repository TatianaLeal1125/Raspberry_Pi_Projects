import os
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

email_user = 'example_email_user@gmail.com'
email_sender = 'example_email_sender@gmailcom'
password_sender = 'Password of example_email_sender@gmailcom'
body = 'Message of body email'
subject = 'Subject of email'
path = '/home/pi/'
filename_path = '/home/pi/example.jpg' #Replace this filename_path with other file
server_email = 'smtp.gmail.com'

def header(email_user,email_sender,subject,body):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_user
    msg['Subject'] = subject
    msg.attach(MIMEText(body,'plain'))
    return msg

def file_send(filename_path,path):
    path, name = filename_path.split(path)
    main, sub = name.split('.')
    attach_files = MIMEBase(main,sub)
    attach_files.set_payload(open(filename_path,'rb').read())
    encoders.encode_base64(attach_files)
    attach_files.add_header('Content-Disposition','attachment; filename=%s' % main+'.'+sub)
    return attach_files

def send_email(server_email,email_user,email_sender,password_sender,text):
    server = smtplib.SMTP(server_email,587)
    server.starttls()
    server.login(email_sender,password_sender)
    server.sendmail(email_sender,email_user,text)
    print('Email sent')
    server.quit()

if __name__ == '__main__':
    m = header(email_user,email_sender,subject,body)
    m.attach(file_send(filename_path,path))
    text = m.as_string()
    send_email(server_email,email_user,email_sender,password_sender,text)

