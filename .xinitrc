#!/bin/bash
        #Turn off Power saver and Screen Blanking
        #xset -dpms
        xset s 0 0
        xset s noblank
        xset s noexpose
        xset dpms 0 0 0

	# turn off mouse pointer
	unclutter -idle 5 -root &

        #Execute MorningInfo 
        echo "Start MorningInfo"
        cd /home/pi/MorningInfo

        python3 displayOnOff.py &
        python3 app.py &
        sleep 5s

        #Execute window manager for full screen
        #exec matchbox-window-manager  -use_titlebar no &

        #Execute Browser with options
        chromium-browser --noerrdialogs --kiosk --incognito http://0.0.0.0:5000 
