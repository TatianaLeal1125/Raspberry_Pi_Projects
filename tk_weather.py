from datetime import datetime,timedelta
from PIL import Image, ImageTk
import tkinter as tk
import requests
import pytz

root = tk.Tk()

HEIGHT =500#600
WIDTH = 600#900

image_dia = tk.PhotoImage(file='clima5.png')
image_noche = tk.PhotoImage(file='clima3.png')

bg_day = '#ffffcc'#'#e6f2ff'#
bg_night = '#e6ccff'

def test_funtion(entry):
    print("This is the entry:",entry)

def  format_response(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        hum = weather['main']['humidity']
        press = weather['main']['pressure']
        zone = int(weather['timezone'])

        sunrise = datetime.utcfromtimestamp(int(weather['sys']['sunrise'])) + timedelta(seconds=zone)
        tsunrise = sunrise.strftime("%H:%M")
        tsunr = (int(sunrise.strftime('%H'))*3600)+(int(sunrise.strftime('%M'))*60)+int(sunrise.strftime('%S'))

        sunset = datetime.utcfromtimestamp(int(weather['sys']['sunset'])) + timedelta(seconds=zone)
        tsunset = sunset.strftime("%H:%M")
        tsuns = (int(sunset.strftime('%H'))*3600)+(int(sunset.strftime('%M'))*60)+int(sunset.strftime('%S'))

        timeconv = datetime.utcfromtimestamp(int(weather['dt'])) + timedelta(seconds=zone)
        time = timeconv.strftime('%H:%M %-d %b %Y')
        tt = (int(timeconv.strftime('%H'))*3600)+(int(timeconv.strftime('%M'))*60)+int(timeconv.strftime('%S'))
        #t = int(tt)

        print(tsunr,tt,tsuns)
        #print(t,tsuns)
        if tt < tsuns and tt >= tsunr:
            background_label['image'] = image_dia
            label['bg'] = bg_day
            weather_icon['bg'] = bg_day
            print('dia')
        else:
            background_label['image'] = image_noche
            label['bg'] = bg_night
            weather_icon['bg'] = bg_night
            print('noche')

        final_str = 'Weather in \n{}\n\nLocal time: {}\nConditions: {}\nTemperature: {} °C\nHumidity: {} %\nPressure: {} hPa\nSunrise: {}\nSunset: {}'.format(name,time,desc,temp,hum,press,tsunrise,tsunset)
        #'City: %s\nCondditions: %s\nTemperature (ºC): %s\nHumidity (%): %s\nPressure (hPa): %s\nSunrise: %s\nSunset: %s'%(name,desc,temp,hum,press,tsunrise,tsunset)

    except:
        final_str = 'There was a problem receiving the information'

    return final_str

def get_weather(city):
    weather_key = '3df162c4455cc11780527a93b7cc4295'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID':weather_key, 'q':city, 'units':'metric'}
    response = requests.get(url,params=params)
    weather = response.json()
    print(weather)
    label['text'] = format_response(weather)

    icon_name = weather['weather'][0]['icon']
    open_image(icon_name)

def open_image(icon):
    size = int(lower_frame.winfo_height()*0.3)
    img =  ImageTk.PhotoImage(Image.open('/home/pi/img/'+icon+'@2x.png').resize((size,size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw',image=img)
    weather_icon.image = img
    print(icon)

canvas = tk.Canvas(root,height=HEIGHT,width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='clima1.png')
background_label = tk.Label(root,image=background_image)
background_label.place(relwidth=1,relheight=1)

frame = tk.Frame(root,bg='#6666ff', bd=5)
frame.place(relx=0.1,rely=0.1,relwidth=0.75,relheight=0.1)

entry = tk.Entry(frame,font=40)
entry.place(relwidth=0.65, relheight=1)

bt = tk.Button(frame,text='Get Weather', bg='white',
               command= lambda: get_weather(entry.get()))
bt.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = tk.Frame(root, bg='#6666ff', bd=10)
lower_frame.place(relx=0.1, rely=0.25, relwidth=0.75, relheight=0.65)

label = tk.Label(lower_frame, font=('ms serif',11),bg='white',anchor='w',justify='left')
label.place(relwidth=1, relheight=1)

weather_icon = tk.Canvas(label, bg='white', highlightthickness=0)
weather_icon.place(relx=0.75,rely=0.25,relwidth=1,relheight=0.5)

root.mainloop()
