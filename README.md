THIS code was created on December 2023 for a purpose of tracking status of yt subscription payment
Code written in python
gen2.py is a 2.0 v of a soft that will provide 2 files of debtor.txt and logg it into phone_mapping.json so you have a data updated independently from each run
you can youse system.sh for a cron job or load it to background in a loop depending on the conditions you need
you need to create a phone_data.py file with a JSON format to load the phone numbers as an input data to your system

**INITIAL RUN**

1. Create phone_data.py in JSON format and declare budget for each phone number
2. Run gen.py that will charge contributor with hardcoded amount of money for subscribtion and cache the results in phone_mapping.json
3. Trigger system.sh script that generates verboose output out of sms.py after process comletes.

**JOB**

1. You can set the background timeout of the script in infinite loop and uncomment /gen.py step that creates a debtor file for you
