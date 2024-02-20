#!/bin/bash

echo "****Notification system start****";
#python /home/pi/projects/subscription_system/gen.py;
sleep 5;
ls -latr | grep debtor.txt;
sleep 5;
python /home/pi/projects/subscription_system/sms.py debtor.txt
