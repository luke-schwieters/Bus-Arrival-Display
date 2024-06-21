#Written From RasberryPi and 2.9im EPD
#Author Luke Schwieters
import requests
import json
import datetime
import sys, os, time, traceback
#Directory To E-Paper Drivers
picdir = "/dir/to/pic"
libdir = "/dir/to/lib"

if os.path.exists(libdir): sys.path.append(libdir)
#Import Specifec epaper driver
from waveshare_epd import epd2in9b_V3
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

black = 0
white = 1

#response_API = '[{"RouteID":20556,"Arrivals":[{"RouteID":20556,"StopID":5102606,"VehicleID":7751,"StopId":5102606,"VehicleId":7751,"ArriveTime":"2:40 PM","RouteId":20556,"Direction":0,"SchedulePrediction":false,"IsLayover":false,"Rules":[],"ScheduledTime":null,"SecondsToArrival":5.7578263,"IsLastStop":false,"OnBreak":false,"ScheduledArriveTime":null,"ScheduledMinutes":0,"TripId":4526650,"BusName":"1145","VehicleName":"1145","RouteName":"1 Mall via Hospital","Minutes":0,"Time":"0"},{"RouteID":20556,"StopID":5102606,"VehicleID":5691,"StopId":5102606,"VehicleId":5691,"ArriveTime":"2:53 PM","RouteId":20556,"Direction":0,"SchedulePrediction":false,"IsLayover":false,"Rules":[],"ScheduledTime":null,"SecondsToArrival":805.1238166,"IsLastStop":false,"OnBreak":false,"ScheduledArriveTime":null,"ScheduledMinutes":0,"TripId":4526594,"BusName":"110","VehicleName":"110","RouteName":"1 Mall via Hospital","Minutes":13,"Time":"13"},{"RouteID":20556,"StopID":5102606,"VehicleID":7752,"StopId":5102606,"VehicleId":7752,"ArriveTime":"3:08 PM","RouteId":20556,"Direction":0,"SchedulePrediction":false,"IsLayover":false,"Rules":[],"ScheduledTime":null,"SecondsToArrival":1705.1238152,"IsLastStop":false,"OnBreak":false,"ScheduledArriveTime":null,"ScheduledMinutes":0,"TripId":4526671,"BusName":"1146","VehicleName":"1146","RouteName":"1 Mall via Hospital","Minutes":28,"Time":"28"}]},{"RouteID":20557,"Arrivals":[{"RouteID":20557,"StopID":5102606,"VehicleID":5694,"StopId":5102606,"VehicleId":5694,"ArriveTime":"2:42 PM","RouteId":20557,"Direction":0,"SchedulePrediction":false,"IsLayover":false,"Rules":[],"ScheduledTime":null,"SecondsToArrival":148.174814,"IsLastStop":false,"OnBreak":false,"ScheduledArriveTime":null,"ScheduledMinutes":0,"TripId":4526943,"BusName":"1112","VehicleName":"1112","RouteName":"11 Student Services","Minutes":2,"Time":"2"},{"RouteID":20557,"StopID":5102606,"VehicleID":5694,"StopId":5102606,"VehicleId":5694,"ArriveTime":"3:17 PM","RouteId":20557,"Direction":0,"SchedulePrediction":false,"IsLayover":false,"Rules":[],"ScheduledTime":null,"SecondsToArrival":2257.1238129,"IsLastStop":false,"OnBreak":false,"ScheduledArriveTime":null,"ScheduledMinutes":0,"TripId":4526944,"BusName":"1112","VehicleName":"1112","RouteName":"11 Student Services","Minutes":38,"Time":"38"}]}]'

#Define a Class for each bus
class Bus:
    def __init__(self, number, Minutes, ArriveTime):
        self.number = number
        self.Minutes = Minutes

        self.ArriveTime = ArriveTime[0:len(ArriveTime)-3:1]

    def getText(self):
        if self.number == 20557:
            cherry = "Cherry in {} mins ({})"
            return cherry.format(self.Minutes,self.ArriveTime)
        elif self.number == 20556:
            red = "Red in {} mins ({})"
            return red.format(self.Minutes,self.ArriveTime)
        else:
            purple = "Purple in {} mins ({})"
            return purple.format(self.Minutes,self.ArriveTime)
        
    
    
    def __str__(self):
        if self.number == 20557:
            return f"Cherry in {self.Minutes} mins ({self.ArriveTime})"
        elif self.number == 20556:
            return f"Red in {self.Minutes} mins ({self.ArriveTime})"
        else:
            return f"Purple in {self.Minutes} mins ({self.ArriveTime})"
        
    def __eq__(self,other):
        return self.Minutes == other.Minutes
    def __lt__(self, other):
        return self.Minutes < other.Minutes
    
#initalize the EPD
epd = epd2in9b_V3.EPD()
# print("INIT")
epd.init()
time.sleep(2)
# print("Clear")
epd.Clear()
time.sleep(10)
# print("done")
#Start Loop
while True:
    try:
        weather_API = requests.get('https://api.weatherapi.com/v1/current.json?q=....')
        response_API = requests.get('https://mycyride.com/stop/3570/arrivals')
    except:
        print("Get Error Weather")
    #Parse Weather Data
    try:
        weather_data = json.loads(weather_API.text)
        Temp  = int(weather_data["current"]["temp_f"])
        condtext = weather_data["current"]["condition"]["text"]
    except:
        print("Execpt: WeatehrJson")
        Temp = "N/A"
        condtext = "N/A"
    # print(int(Temp))

    #Get DateTime
    realtime = datetime.datetime.now()
    rateHour = realtime.strftime("%H")
    h = realtime.strftime("%I")
    m = realtime.strftime("%M")
    d = realtime.strftime("%a")
    dm = realtime.strftime("%d")
    if(int(dm) % 10 == 1):
        de = "st"
    elif(int(dm) % 10 == 2):
        de = "nd"
    elif(int(dm) % 10 == 3):
        de = "rd"
    else:
        de = "th"

    timedisplay = (f"{h}:{m}")
    datedisplay = (f"{d}, {dm}{de}")
    print(timedisplay)

    #Parse Bus API JSON 
    busList = []
    try:
        data = json.loads(response_API.text)

        for x in range(len(data)):
            for y in range(len(data[x]['Arrivals'])):
                # print(data[x]['Arrivals'][y]['Minutes'])
                busList.append(Bus(data[x]['Arrivals'][y]['RouteID'],data[x]['Arrivals'][y]['Minutes'],data[x]['Arrivals'][y]['ArriveTime']))

        busList.sort()
    except:
        print("Execpt: Busjson")
        pass
    
    #Printing to EPD
    try:


        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


        HBlackimage = Image.new('1', (epd.height, epd.width), 255)
        HRYimage = Image.new('1', (epd.height, epd.width), 255)
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRYimage)
        i = 0
        for x in busList:
            i+=24
            if(i > 96):
                break
            route = x.getText()
            # print(route)
            if (x.Minutes <= 5):
                drawred.text((2, i), route , font = font24, fill = 0)
                # print("red")
            else:
                drawblack.text((2,i), route , font = font24, fill = 0)
                # print("black")
        
        

        drawblack.text((3, 0), datedisplay , font = font18, fill = 0)
        drawblack.text((110, 0), str(Temp) , font = font18, fill = 0)
        drawblack.text((137, 1), "F" , font = font15, fill = 0)
        drawblack.text((129, -5), "o" , font = font15, fill = 0)
        drawblack.text((153, 1), condtext , font = font15, fill = 0)
        drawblack.text((250, 0), timedisplay , font = font18, fill = 0)
        drawblack.rectangle([(0,0),(295,19)],outline = black)
        drawblack.line((249, 0, 249, 19), fill = 0)
        drawblack.line((100, 0, 100, 19), fill = 0)
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        time.sleep(1)
    


    except IOError as e:
        print(e)

    except KeyboardInterrupt:
        print("ctrl + c:")
        epd2in9b_V3.epdconfig.module_exit()
        exit()
    #Create a sleep cycle to stop refresh, when now buses present
    rate = int(1)
    if len(busList) == 0:
        rate = int(10)
        print("BusList empty, rate 10")
    if int(rateHour) < 6:
        rate = int(60)
        print("Time, rate 60")

    #Set REf
    time.sleep(int(rate) * 60)