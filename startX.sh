#!/bin/bash
	
        #Turn off Power saver and Screen Blanking
	#xset s off -dpms
	xset s off

	#Execute MorningInfo 
	echo "Start MorningInfo"
	cd /home/pi/MorningInfo

	python3 displayOnOff.py &
	python3 app.py &
	sleep 10s

	#Execute window manager for full screen
	exec matchbox-window-manager  -use_titlebar no &

	#Execute Browser with options
	chromium-browser --noerrdialogs --kiosk --incognito http://0.0.0.0:5000
