#!/bin/sh
echo "Start MorningInfo"
cd /home/pi/Develop/MornigInfo

python3 displayOnOff.py &
python3 app.py &
sleep 15s
chromium-browser --kiosk --incognito "http://0.0.0.0:5000" &
