#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import sys
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

dotMatrixSize = (64,32)

class dotMatrix:
    def __init__(self):
        self.misakiFont = ImageFont.truetype(
          "/home/pi/Develop/fonts/misaki_gothic.ttf",8)
        self.bitmapFont = ImageFont.load(
          "/home/pi/Develop/fonts/shnm6x12a.pil")
        self.bitmapBoldFont = ImageFont.load(
          "/home/pi/Develop/fonts/shnm6x12ab.pil")
        self.img = Image.new("RGBA", dotMatrixSize)
        #self.canvas = ImageDraw.Draw(img)
        self.img_size = np.array(self.img.size) 
        self.colorWhite = (255,255,255)
        self.colorRed = (255,0,0)
        self.colorGreen = (0,255,0)
        self.colorBlue = (0,0,255)
        self.colorOrange = (255,127,0)

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
    def drawTime(self,pos = (24,0)):
        d = datetime.datetime.today()
        timeT = d.strftime("%H:%M")
        if d.second%2 == 0: timeT += "."
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text(pos,timeT,self.colorOrange,font=self.bitmapBoldFont)
    def drawDate(self,pos = (5,0)):
        d = datetime.datetime.today()
        monthT = d.strftime("%m")
        dayT = d.strftime("%d")
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text(pos,monthT,self.colorOrange,font=self.bitmapFont)
        self.draw.text((pos[0],(32-pos[1])/2),dayT,self.colorOrange,font=self.bitmapFont)
    def drawMatrix(self):
        self.matrix.SetImage(self.img.convert('RGB'))

DM = dotMatrix()

print("Press CTRL-C to stop.")
while True:
    try:
        d = datetime.datetime.today()
        date = u'%s年%s月%s日' % (d.year, d.month, d.day)
        hour = u'%s:%s:%s' % (d.hour, d.minute, d.second)
        dh = d.strftime("%Y-%m-%d %H:%M:%S")
        hour2 = d.strftime("%H:%M:%S")
        DM.clearCanvas()
        #DM.drawText(hour2,[2,2])
        DM.drawTime()
        DM.drawDate()
        
        DM.drawMatrix()
        time.sleep(1)
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
