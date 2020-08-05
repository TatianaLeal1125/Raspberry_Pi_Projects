from gpiozero import MotionSensor
import quickstart as qs
import email_test as mail
import RPi.GPIO as GPIO
import picamera
import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN_LED = 27
pir = MotionSensor(4)

GPIO.setup(PIN_LED,GPIO.OUT)
GPIO.output(PIN_LED,GPIO.LOW)

name_folder = 'Surveillance'
mime = "mimeType='application/vnd.google-apps.folder' and name='{0}'"
mimeType = mime.format(name_folder)

email_user = 'example_email_user@gmail.com'
email_sender = 'example_email_sender@gmailcom'
password_sender = 'Password of example_email_sender@gmailcom'
subject = 'Surveillance'
body = 'Surveillance script test'
server_mail = 'smtp.gmail.com'

#wait a calibration time
print('Motion sensor is being configured')
pir.wait_for_no_motion()
print('Ready')

def photo_camera(service,id_folder):

    outsider_path = '/home/pi/outsider/'

    if not os.path.exists(outsider_path):
        os.makedirs(outsider_path)
        print('Directory created')

    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        time.sleep(1)
		time_stamp = '{timestamp:%Y-%m-%d %H:%M:%S}'+'.jpg'
		module_camera = camera.capture_continuous(outsider_path+time_stamp)
        for i, filename in enumerate(module_camera):
            name = filename.split('.jpg')
            qs.file_in_folder(service,filename,id_folder,outsider_path)
            msg.attach(mail.file_send(filename,outsider_path))
            print('Capture {0}'.format(filename))
            if i == 1:
                break
            time.sleep(2)
        name_video = name[0]+'.h264'
        camera.start_recording(name_video)
        camera.wait_recording(5)
        camera.stop_recording()
        qs.file_in_folder(service,name_video,id_folder,outsider_path)
        msg.attach(mail.file_send(name_video,outsider_path))
        camera.close()
        text = msg.as_string()
        mail.send_email(server_mail,email_user,email_sender,password_sender,text)

def create_folder_drive(service,mimeType,namefolder):
    flag, id_folder = qs.query_files(service,mimeType)
    if flag:
        print('Folder exists')
    else:
        id_folder = qs.create_folder(service,namefolder)
    return id_folder

try:
    service = qs.main()
    id_folder = create_folder_drive(service,mimeType,name_folder)
    msg = mail.header(email_user,email_sender,subject,body)
    while True:

        pir.wait_for_motion()
        print('Motion detected')
        GPIO.output(PIN_LED,GPIO.HIGH)
        photo_camera(service,id_folder)
        pir.wait_for_no_motion()
        print('Wait for motion')
        GPIO.output(PIN_LED,GPIO.LOW)

finally:
    print('This is the finally')
    pir.close()

