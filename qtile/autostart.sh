#!/bin/bash

picom -b --config ~/.config/picom/picom.conf &
feh --bg-scale ~/wallpapers/first.png &
xrandr --output HDMI-1 --same-as eDP-1 --scale 0.852x0.852 &
