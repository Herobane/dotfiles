#!/bin/sh

# Startup programs
xrandr -s 1920x1080 &
nitrogen --restore &
picom &
xscreensaver --no-splash &
/usr/bin/emacs --daemon &
# conky &

# Gets the property IDs of corresponding touchpad actions
TAP_ACTION=$(xinput list-props 13 | grep -i "Tapping Enabled (" | awk '{print $4}' | cut -c 2,3,4)
SCROLL_DIST=$(xinput list-props 13 | grep -i "Scrolling Enabled (" | awk '{print $5}'| cut -c 2,3,4)

# Enable tap-to-click with :
xinput set-prop 13 $TAP_ACTION 1

# Enables inverted two-fingers scrolling
xinput set-prop 13 $SCROLL_DIST 1
