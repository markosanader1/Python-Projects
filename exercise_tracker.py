'''This code utilizes the Natural Language Processing capabilities of the site: https://trackapi.nutritionix.com. User inputs type and a number of exercises he/she did today.
The code then sends a post request "to https://trackapi.nutritionix.com/v2/natural/exercise" containing necessary information about the user(height, weight, age...)
The code then extracts information about the type of exercise, its number, duration of exercising, and spent callories. 
The code then writes the obtained information to the Excel Table on www.sheety.com by post request.'''


import os
import requests
from datetime import datetime

APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]
SECRET_TOKEN = os.environ["SECRET_TOKEN"]

url = "https://trackapi.nutritionix.com/v2/natural/exercise"
unos = input('What did u do today?')

headers = {"x-app-id": APP_ID,
"x-app-key" : APP_KEY,
"Content-Type": "application/json",

}
body={
 "query":unos,
 "gender":"male",
 "weight_kg":85.00,
 "height_cm":187.00,
 "age":28
}
response = requests.post(url=url, headers=headers, json=body)
response.raise_for_status()
data = response.json()
print(data)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
# exercise = data['exercises'][0]['user_input']
# duration = data['exercises'][0]['met']
# calories = data['exercises'][0]['nf_calories']

vezbe=[_['name'].title() for _ in data["exercises"]]
print(vezbe)
print(data["exercises"])
sheety_url = "https://api.sheety.co/f8f57d2ac1288732b6a288759601be87/copyOfMyWorkouts/workouts"
for _ in data["exercises"]:
 dodatak = {
   "workout":
    {
    "date": today_date,
    "time": now_time,
    "exercise": _['name'],
    "duration":_['duration_min'],
    "calories":_['nf_calories']

  }
 }

 bearer_header = {"Authorization": f"Bearer {SECRET_TOKEN}",
                  "Content-Type":"application/json",
                  }
 response = requests.post(url=sheety_url, json=dodatak, headers=bearer_header)
 print(response.text)
