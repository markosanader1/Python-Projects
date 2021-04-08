'''This is a code that sends API request to http://api.open-notify.org/iss-now.json, for information about current position of International Space Station (ISS). 
Code than compares current latitude and longitude of the ISS and cordinates of the chosen plase(MY_LAT and MY_LONG are set to the cordinates of Belgrade, Serbia).
The code also requests the information about when the sun rises and sets at current day.It sends an API request to "https://api.sunrise-sunset.org/json" for information 
about sunrise and sunset.If the ISS is close to current position, and if it is night, the code uses smptplib module to send an email to the user,informing him that ISS is close.''' 

import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 44.786568 # Your latitude
MY_LONG = 20.448921 # Your longitude

MY_EMAIL = os.environ.get("EMAIL")
MY_PASSWORD = os.environ.get("PASSWORD")

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
hour = time_now.hour

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


while True:
    time.sleep(60)
    if hour > sunset or hour < sunrise:
        if abs(iss_latitude - MY_LAT) < 5 and abs(iss_longitude - MY_LONG) < 5:

            connection = smtplib.SMTP("smtp.gmail.com", port=587)
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: ISS is close!\n\nLook up!")
            connection.close()


