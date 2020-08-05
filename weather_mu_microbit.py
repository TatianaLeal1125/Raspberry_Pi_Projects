# Write your code here :-)
from microbit import *

sun = Image('00000:'
        '00900:'
        '09990:'
        '00900:'
        '00000:')

few_clouds = Image('05050:'
         '55555:'
         '05050:'
         '00000:'
         '00000:')

broken_clouds = Image('70007:'
         '77077:'
         '70007:'
         '00700:'
         '07770:')

scattered_clouds = Image('07000:'
         '77700:'
         '07070:'
         '00777:'
         '00070:')

shower = Image('07070:'
         '77777:'
         '40404:'
         '04040:'
         '40404:')

rain = Image('06060:'
         '66666:'
         '06060:'
         '30303:'
         '03030:')

thunder = Image('70700:'
         '07070:'
         '00707:'
         '07070:'
         '70700:')

snow = Image('70707:'
         '07070:'
         '70707:'
         '07070:'
         '70707:')

mist = Image('11111:'
         '33333:'
         '11111:'
         '33333:'
         '11111:')

moon = Image('00777:'
         '07770:'
         '07700:'
         '07770:'
         '00777:')

weather = {'01d':sun, '01n':moon, '02d':few_clouds, '02n':few_clouds,
        '03d':scattered_clouds, '03n':scattered_clouds,'04d':broken_clouds,
        '04n':broken_clouds,'09d':shower,'09n':shower,'10d':rain,'10n':rain,
        '11d':thunder,'11n':thunder,'13d':snow,'13n':snow,'50d':mist,'50n':mist}

def get_sensor_data():
    a, b = button_a.was_pressed(), button_b.was_pressed()
    print(a, b)

while True:
    sleep(5)
    get_sensor_data()
    try:
        bytestring = uart.readline()
        print(bytestring)
        s = str(bytestring,'utf-8')[0:-3]
        icon= weather[s]
        display.show(icon)
    except:
        pass


