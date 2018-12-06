#!/bin/bash


sudo python /home/pi/project/stage1_3/pitft_display.py &
sudo wget -O /home/pi/project/stage2/satellites0a.txt 'https://www.celestrak.com/NORAD/elements/active.txt'
sudo wget -O /home/pi/project/stage2/satellites0b.txt 'https://www.celestrak.com/NORAD/elements/active.txt'
sudo python /home/pi/project/stage2/whats_up_there.py &
python /home/pi/project/stage4/led_matrix.py
