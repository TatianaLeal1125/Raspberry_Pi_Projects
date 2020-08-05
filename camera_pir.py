from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import picamera
import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN_LED = 27
PIN_BUZZER = 3
pir = MotionSensor(4)

GPIO.setup(PIN_LED,GPIO.OUT)
GPIO.setup(PIN_BUZZER,GPIO.OUT)
GPIO.output(PIN_BUZZER,GPIO.LOW)
GPIO.output(PIN_LED,GPIO.LOW)

#wait a calibration time
print('Motion sensor is being configured')
pir.wait_for_no_motion()
print('Ready')

def photo_camera():

    outsider_path = '/home/pi/outsider/'

    if not os.path.exists(outsider_path):
        os.makedirs(outsider_path)
        print('Directory created')

    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        GPIO.output(PIN_BUZZER,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(PIN_BUZZER,GPIO.LOW)
        for i, filename in enumerate(camera.capture_continuous(outsider_path+'image{timestamp:%Y-%m-%d %H:%M:%S}',format='jpeg')):
            print('Capture image{0}'.format(filename))
            if i == 5:
                break
            time.sleep(2)
        camera.close()
try:

    while True:

        pir.wait_for_motion()
        print('Motion detected')
        GPIO.output(PIN_LED,GPIO.HIGH)
	photo_camera()
        pir.wait_for_no_motion()
        print('Wait for motion')
        GPIO.output(PIN_LED,GPIO.LOW)

finally:
    print('This is the finally')
    pir.close()

