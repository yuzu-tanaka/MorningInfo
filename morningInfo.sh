#!/bin/bash
logger -t Info "Start Morning Info"
cd /home/pi/MorningInfo
/usr/bin/python3 morningInfo.py
