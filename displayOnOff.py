#encoding:utf-8
import RPi.GPIO as GPIO
import subprocess
import time

isDevelop = False #True
#isDevelop = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

f = open('text.txt', 'w') # 書き込みモードで開く

def xset_s_off():
  cmd = 'xset s off' # for Raspberry Pi official display
  subprocess.call( cmd, shell=True)

def hdmiOff():
  #cmd = 'tvservice -o' # for HDMI
  cmd = 'xset dpms force off' # for Raspberry Pi official display
  subprocess.call( cmd, shell=True)

def hdmiOn():
  #cmd = 'tvservice --preferred > /dev/null'
  #subprocess.call( cmd, shell=True)
  #cmd = 'fbset -depth 8; fbset -depth 32; xrefresh'
  cmd = 'xset dpms force on' # for Raspberry Pi official display
  subprocess.call( cmd, shell=True)
  print('Powering on HDMI')

#xset_s_off()
hdmiOff()
statGPIO = 0
retGPIO = 0
time1 = time.time()
time2 = time.time()
timeRaps = 10 if isDevelop == True else 600

print('Starting HDMI Control')
print('Develop Mode: ',isDevelop, 'time Raps: ',timeRaps)

while True:
  ret = GPIO.input(18)
  if ret == 1: retGPIO = 1
  time2 = time.time()
  time3 = time2 - time1
  if isDevelop == True: print("retGPIO: " + str(retGPIO),"statGPIO: " + str(statGPIO),"time3: " + str(time3))

  if retGPIO == 1 and retGPIO != statGPIO:
    hdmiOn()
    time1 = time.time()
    retGPIO = 0
    statGPIO = 1 
    f.writelines('HDMI ON  :' + str(time1)+'\n') # 引数の文字列をファイルに書き込む
  elif retGPIO == 0 and retGPIO != statGPIO and time3 >= timeRaps:
    hdmiOff()
    time1 = time.time()
    retGPIO = 0
    statGPIO = 0
    f.writelines('HDMI OFF :' + str(time1)+'\n') # 引数の文字列をファイルに書き込む
  elif retGPIO==1 and statGPIO==1 and time3 >= timeRaps:
    time1 = time.time()
    retGPIO = 0
    f.writelines('HDMI --- :' + str(time1)+'\n') # 引数の文字列をファイルに書き込む

