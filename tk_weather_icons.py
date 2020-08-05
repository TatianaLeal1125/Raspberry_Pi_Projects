import os
import urllib.request

day = ['01d.png','02d.png','03d.png','04d.png',
       '09d.png','10d.png','11d.png','13d.png','50d.png']

night = ['01n.png','02n.png','03n.png','04n.png',
       '09n.png','10n.png','11n.png','13n.png','50n.png']


day_big = ['01d@2x.png','02d@2x.png','03d@2x.png','04d@2x.png',
       '09d@2x.png','10d@2x.png','11d@2x.png','13d@2x.png','50d@2x.png']

night_big = ['01n@2x.png','02n@2x.png','03n@2x.png','04n@2x.png',
       '09n@2x.png','10n@2x.png','11n@2x.png','13n@2x.png','50n@2x.png']

url_icons = 'http://openweathermap.org/img/wn/'
img_dir = '/home/pi/img/'

if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    print('dir created')

#Get the day weather icons
for name in day_big:
    file_name = img_dir + name
    if not os.path.exists(file_name):
        urllib.request.urlretrieve(url_icons+name,file_name)

#Get the night weather icons
for name in night_big:
    file_name = img_dir + name
    if not os.path.exists(file_name):
        urllib.request.urlretrieve(url_icons+name,file_name)