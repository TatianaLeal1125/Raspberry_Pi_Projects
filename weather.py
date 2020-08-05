
import pyowm 
from pyowm import timeutils
import serial
import time
import pytz
from datetime import timedelta, datetime

API_KEY = '3df162c4455cc11780527a93b7cc4295'
location = 'Mexico city, MX'

owm = pyowm.OWM(API_KEY)
mx = owm.weather_at_place(location)
temperature = mx.get_weather()

print(datetime.now().strftime('%A %B %-d %H:%M:%S'))
print('Current temperature in {} is {} celsius'.format(location,temperature.get_temperature('celsius')['temp'],datetime.now()))

fc = owm.three_hours_forecast(location)
f = fc.get_forecast()

#Get weather at a specific time. In this case, 8 hours after current time
tt= datetime.now() + timedelta(days=0, hours=8)
ww = fc.get_weather_at(tt)
temp = ww.get_temperature('celsius')['temp']
#print('The temperature at ' + tt.strftime('%Y-%m-%d %H:%M:%S')+' is '+ str(temp) +' C')

referenceTime = [datetime.fromtimestamp(int(t.get_reference_time())) for t in f]
rft =[rt.strftime("%A %B %-d, %Y %H:%M:%S") for rt in referenceTime]

time = [(datetime.strptime(t.get_reference_time(timeformat='iso'),"%Y-%m-%d %H:%M:%S+00") + timedelta(hours=-5)) for t in f]
timediff = [t.strftime("%Y-%m-%d %H:%M:%S+00") for t in time]
icons = [weather.get_weather_icon_name() for weather in f]

weather = {'01d':'sun','01n':'moon','02d':'few_clowds','02n':'few_clowds',
          '03d':'scattered_clouds','03n':'scattered_clous','04d':'broken_clouds',
          '04n':'broken_clouds','09':'shower','09n':'shower','10d':'rain','10n':'rain',
          '11d':'thunder','11n':'thunder','13d':'snow','13n':'snow','50d':'mist','50n':'mist'}

#print(icons)

PORT = '/dev/ttyACM0'
BAUD = 115200

s = serial.Serial(PORT)
s.baudrate = BAUD
s.parity = serial.PARITY_NONE
s.databits = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_ONE
s.readline()

icon = 0

while True:
    s.write(icons[icon%len(icons)].encode('utf-8'))
    data = s.readline().decode('utf-8')
    #print(data)
    data_list = data.rstrip().split(' ')
    try:
        a,b = data_list
        if a == 'True':
            icon +=1
            time_weather = rft[icon%len(icons)]
            weather_forecast = icons[icon%len(icons)]
            module = icon%len(icons)
            print(time_weather,weather[str(weather_forecast)],module)
        if b == 'True':
            icon -= 1
            time_weather = rft[icon%len(icons)]
            weather_forecast = icons[icon%len(icons)]
            module = icon%len(icons)
            print(time_weather,weather[str(weather_forecast)],module)
    except:
        pass
 
s.close()
