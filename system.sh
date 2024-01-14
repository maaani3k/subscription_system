#!/bin/bash

echo "****Notification system start****";
python /home/pi/projects/subscription_system/gen.py;
sleep 3;
ls -latr | grep debtor.txt;
sleep 3
python /home/pi/projects/subscription_system/sms.py debtor.txt
