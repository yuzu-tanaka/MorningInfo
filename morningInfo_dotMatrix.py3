#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import datetime
import sys
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import pdb

from getJSON2 import *

dotMatrixSize = (64,32)

class senser:
    def __init__(self):
        #pdb.set_trace()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12,GPIO.IN)
        self.status = 0
        self.offOnTime = time.time()
        self.onOffTime = time.time()
    def checkStatus2(self):
        laps = time.time() - self.onOffTime
        if laps > 300:
            statusNow = GPIO.input(12)
            if statusNow == 1:
                self.status = statusNow
                return 1
            else:
                return 0
        else:
            #self.status = statusNow
            return 0
        pass
        
    def checkStatus(self):
        statusNow = GPIO.input(12)
        if statusNow == 1:
           self.offOnTime = time.time()
           self.status = statusNow
           return 1
        elif statusNow == 0 and statusNow != self.status:
           self.onOffTime = time.time()
           self.status = statusNow
           return 1
        elif statusNow == 0 and statusNow == self.status:
           laps = time.time() - self.onOffTime
           #print(laps)
           if laps > 300:
               self.status = statusNow
               return 0
           else:
               self.status = statusNow
               return 1
        else:
           return 1


class dotMatrix:
    def __init__(self):
        self.misakiFont = ImageFont.truetype(
          "/home/pi/Develop/MorningInfo/fonts/misaki_gothic.ttf",8)
        self.misakiFont10 = ImageFont.truetype(
          "/home/pi/Develop/MorningInfo/fonts/misaki_gothic.ttf",10)
        self.bitmapFont = ImageFont.load(
          "/home/pi/Develop/MorningInfo/fonts/shnm6x12a.pil")
        self.bitmapBoldFont = ImageFont.load(
          "/home/pi/Develop/MorningInfo/fonts/shnm6x12ab.pil")
        self.img = Image.new("RGBA", dotMatrixSize)
        #self.canvas = ImageDraw.Draw(img)
        self.img_size = np.array(self.img.size) 
        self.colorWhite = (255,255,255)
        self.colorRed = (255,0,0)
        self.colorGreen = (0,255,0)
        self.colorBlue = (0,0,255)
        self.colorOrange = (255,127,0)
        self.firstTime = 0
        self.tempText = ""

        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.parallel = 1
        options.brightness = 80
        options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

        self.matrix = RGBMatrix(options = options)

    def clearCanvas(self):
        self.img = Image.new("RGBA", dotMatrixSize)
        #self.canvas = ImageDraw.Draw(img)
    
    def drawText(self,text,pos):
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text(pos,text,self.colorOrange,font=self.bitmapFont)
    def drawTrain(self,pos = (30,25)):
        respT = getTrainDelay()
        retText = ''
        for train in respT[0]:
            if train == '湘南新宿ライン': retText+='S'
            if train == '東海道線': retText+='T'
            if train == '横須賀線': retText+='Y'
            if train == '京浜東北線': retText+='K'
        if retText != '':
            pos = (64 - len(retText)*3,25)
            self.draw = ImageDraw.Draw(self.img)
            self.draw.text(pos,retText,self.colorRed,font=self.misakiFont)


    def drawTemp(self,pos = (0,25)):
        d = datetime.today()
        def outputText():
            respW = getWether('140010')
            #respT = getTrainDelay()
            day = respW['day']
            message = respW['message']
            telop = respW['telop']
            icon = '/static/wetherIcons/'+ respW['icon'] + '.png'
            tempeMax = respW['max'] if respW['max'] != None else '-'
            tempeMin = respW['min'] if respW['min'] != None else "-"
            
            self.tempText = tempeMin + " / " + tempeMax
            #~ return self.tempText
        
        if self.firstTime  == 0:
            #~ text = outputText()
            outputText()
            self.firstTime  = 1
        elif int(d.strftime("%M"))%15 == 0 and d.strftime("%S") ==0:
        #elif int(d.strftime("%M"))%15 == 0:
            #~ text = outputText()
            outputText()
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text(pos,self.tempText,self.colorOrange,font=self.misakiFont)

    def drawTime(self,pos = (20,10)):# pos = (24,0)
        #~ d = datetime.datetime.today()
        d = datetime.today()
        timeT = d.strftime("%H:%M")
        self.draw = ImageDraw.Draw(self.img)
        for i,t in enumerate(timeT):
            self.draw.text((pos[0]+7*i,pos[1]),t,self.colorOrange,font=self.bitmapBoldFont)
        '''
        if len(d.strftime("%H"))==2:
            timeH = d.strftime("%H")[0]+""+d.strftime("%H")[1]
        else:
            timeH = d.strftime("%H")
        if len(d.strftime("%M"))==2:
            timeM = d.strftime("%M")[0]+""+d.strftime("%M")[1]
        else:
            timeM = d.strftime("%M")    
        timeT = timeH + ":" + timeM
        #if d.second%2 == 0: timeT += "."
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text(pos,timeT,self.colorOrange,font=self.bitmapBoldFont)
        '''
    def drawDate(self,pos = (0,0)):
        #~ d = datetime.datetime.today()
        d = datetime.today()
        monthT = d.strftime("%b")
        dayT = d.strftime("%d")
        self.draw = ImageDraw.Draw(self.img)
        #self.draw.text(pos,monthT,self.colorOrange,font=self.bitmapFont)
        #self.draw.text((pos[0],(32-pos[1])/2),dayT,self.colorOrange,font=self.bitmapFont)
        monthDayT = monthT +" " + dayT
        self.draw.text(pos,monthDayT,self.colorOrange,font=self.misakiFont)
    def drawMatrix(self):
        self.matrix.SetImage(self.img.convert('RGB'))

SS = senser()
DM = dotMatrix()
laps1 = time.time()

print("Press CTRL-C to stop.")
while True:
    
    try:
        #~ d = datetime.datetime.today()
        #d = datetime.today()
        #date = u'%s年%s月%s日' % (d.year, d.month, d.day)
        #hour = u'%s:%s:%s' % (d.hour, d.minute, d.second)
        #dh = d.strftime("%Y-%m-%d %H:%M:%S")
        #hour2 = d.strftime("%H:%M:%S")
        #DM.clearCanvas()
        #DM.drawText(hour2,[2,2])
        
        DM.clearCanvas()

        DM.drawTime()
        DM.drawDate()
        #DM.drawTemp()
        #DM.drawTrain()
        if SS.checkStatus() == 0: DM.clearCanvas() #
        DM.drawMatrix()
        time.sleep(10)

        '''
        laps2 = time.time()
        if laps2 - laps1 >= 60:
            DM.drawTime()
            DM.drawDate()

            DM.drawTemp()
            if SS.checkStatus() == 0: DM.clearCanvas() #
            laps1 = laps2
        else:
            if SS.checkStatus() == 0: DM.clearCanvas() #
            DM.drawMatrix()
        time.sleep(1)
        '''
    except KeyboardInterrupt:
        sys.exit(0)

'''    
    
def draw_text_at_center(img, text):
  draw = ImageDraw.Draw(img)
  #draw.font = ImageFont.truetype(
  #  "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 20)
  #draw.font = ImageFont.truetype(
  #  "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 10) 
  #draw.font = ImageFont.truetype(
  #  "/home/pi/Develop/fonts/misaki_gothic.ttf",8)
  misakiFont = ImageFont.truetype(
    "/home/pi/Develop/fonts/misaki_gothic.ttf",8)
  
  #BMFont = ImageFont.load("/home/pi/Develop/fonts/shnm6x12a.pil")
  img_size = np.array(img.size) 
  #txt_size = np.array(draw.font.getsize(text))
  txt_size = np.array(misakiFont.getsize(text))
  #pos = (img_size - txt_size) / 2
  #print(pos)
  #draw.text(pos, text, (255, 255, 255))
  draw.text([2,3],text,(255,255,255),font=misakiFont)
  #draw.text([2,3],text,(255,255,255),font=BMFont)
  return img


img = Image.new("RGBA", (64, 32))
d = datetime.datetime.today()
text = u"７月５日\n20:18"
date = u'%s年%s月%s日\n' % (d.year, d.month, d.day)
hour = u'%s時%s分%s.%s秒n' % (d.hour, d.minute, d.second, d.microsecond)
dh = d.strftime("%Y-%m-%d %H:%M:%S")
image = draw_text_at_center(img, date)

#if len(sys.argv) < 2:
#    sys.exit("Require an image argument")
#else:
#    image_file = sys.argv[1]

#image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
'''
