#!/usr/bin/env python3
# -*- coding: utf-8 -*-
isDebug = True

import time
from datetime import datetime as dt
import sys
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import pdb

#from getJSON2 import *
from GetWeather import *
from GetTrain import *

WT = getWeather()
TR = train()
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
        self.misakiFontS = ImageFont.truetype(
          "./fonts/misaki_gothic.ttf",6)
        self.misakiFont = ImageFont.truetype(
          "./fonts/misaki_gothic.ttf",8)
        self.misakiFont10 = ImageFont.truetype(
          "./fonts/misaki_gothic.ttf",10)
        self.bitmapFont = ImageFont.load(
          "./fonts/shnm6x12a.pil")
        self.bitmapBoldFont = ImageFont.load(
          "./fonts/shnm6x12ab.pil")
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
        
    def drawTrain(self,pos = (25,0)):
        d1 = dt.now()
        d2 = TR.getLastUpdate()
        if isDebug:
            print("d1:", d1)
            print("d2:", d2)
        if d2 != None:
            diffTime = d1 - d2
            if isDebug: print("diffTime-seconds", diffTime.seconds)
            if diffTime.seconds >= 600: # 10分以上の時間差があれば、天気予報をアップデート
                if isDebug: print('10分以上経ったから電車を更新')
                TR.updateTrainDelay()
        else:
            if isDebug: print('Noneだから電車を更新')
            TR.updateTrainDelay()
        respT = TR.trainStatus
        retText = ''
        for train in respT[0]:
            if train == '湘南新宿ライン': retText+='S'
            if train == '東海道線': retText+='T'
            if train == '横須賀線': retText+='Y'
            if train == '京浜東北線': retText+='K'
        if retText != '':
            pos = (64 - len(retText)*5,0)
            self.draw = ImageDraw.Draw(self.img)
            self.draw.text(pos,retText,self.colorRed,font=self.misakiFont)

    def drawWeather(self,pos = (0,25)):
        d1 = dt.now()
        d2 = WT.getLastUpdate()
        if isDebug: 
            print("d1:", d1)
            print("d2:", d2)
        if d2 != None:
            diffTime = d1 - d2
            if isDebug: print("diffTime-seconds", diffTime.seconds)
            if diffTime.seconds >= 10800: # ３時間以上の時間差があれば、天気予報をアップデート
                if isDebug: print('３時間以上経ったからを更新')
                WT.update()
        else:
            if isDebug: print('Noneだから天気を更新')
            WT.update()
        if isDebug:
            print("LastUpdate:",WT.getLastUpdate())
            print("今日の天気",WT.detail[0])
            print("今日の最低気温",WT.temperatureMin[0])
            print("今日の最高気温",WT.temperatureMax[0])
            print("今日の降水確率",WT.chanceOfRain[0])
            print("明日の天気",WT.detail[1])
            print("明日の最低気温",WT.temperatureMin[1])
            print("明日の最高気温",WT.temperatureMax[1])
            print("明日の降水確率",WT.chanceOfRain[1])
                                    


        if d1.hour >= 15:
            weatherText = WT.detail[1]
            tempText = WT.temperatureMin[1]
            tempText += '/'+ WT.temperatureMax[1]
            tempText += ' '+ str(WT.chanceOfRain[1]) + '%'
        else:
            weatherText = WT.detail[0]
            tempText = WT.temperatureMin[0]
            tempText += '/'+ WT.temperatureMax[0]
            tempText += ' '+ str(WT.chanceOfRain[0]) + '%'
        self.draw = ImageDraw.Draw(self.img)
        #self.draw.text(pos,weatherText,self.colorOrange,font=self.misakiFont)
        #self.draw.text((0,20),tempText,self.colorOrange,font=self.misakiFont)
        self.draw.text(pos,tempText + weatherText,self.colorOrange,font=self.misakiFont)

    def drawTime(self,pos = (5,10)):# pos = (24,0)
        #~ d = datetime.datetime.today()
        d = dt.today()
        timeT = d.strftime("%H:%M:%S")
        self.draw = ImageDraw.Draw(self.img)
        for i,t in enumerate(timeT):
            self.draw.text((pos[0]+7*i,pos[1]),t,self.colorOrange,font=self.bitmapBoldFont)

    def drawDate(self,pos = (0,0)):
        #~ d = datetime.datetime.today()
        d = dt.today()
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
        
        DM.clearCanvas()

        DM.drawTime()
        DM.drawDate()
        DM.drawTrain()
        DM.drawWeather()
        if SS.checkStatus() == 0: DM.clearCanvas() #
        DM.drawMatrix()
        time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)

