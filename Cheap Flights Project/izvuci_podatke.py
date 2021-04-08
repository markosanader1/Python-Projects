import requests
from datetime import datetime
import os
from twilio.rest import Client

class PreuzmiPodatke():
    def __init__(self):
        self.podaci = {}

    # def datum_leta(self, dan, mesec, godina, za_dana, za_meseci, za_godine):
    #     sada = datetime(year=godina, month=mesec, day=dan)
    #     date_from = sada.strftime("%d/%m/%Y")
    #     do = datetime(year=za_godine, month=za_meseci, day=za_dana)
    #     date_to = do.strftime("%d/%m/%Y")
    #     self.dict = {"search from": date_from, "search to": date_to}
    #     return self.dict

    def termin_i_cena(self):
        date_from = input("Import date in the format dd/mm/yyyy, for example 10/02/2021:\nWhich date do you want to travel? ")
        date_to = input("Import date in the format dd/mm/yyyy, for example 10/02/2021:\nUntil which date to search flights? ")
        maks_cena = int(input("What is the maximum price you want to pay? $"))
        self.dict = {"search from": date_from, "search to": date_to, "maximum price":maks_cena}
        return self.dict


    def preuzmi_podatke(self, dictionary, skracenica):
        url = "https://tequila-api.kiwi.com/v2/search"
        header = {"apikey":"P2g91cc90plohdtMAFhDs9cRkc6-QmVX"}
        parametri={
            "fly_from": skracenica,
            "fly_to": '',
            "date_from": dictionary["search from"],
            "date_to": dictionary["search to"],
            "flight_type": "round",
            "one_for_city": 1,
            "price_to" : dictionary["maximum price"]
        }
        response = requests.get(url=url, headers=header, params= parametri)
        try:
            podaci_o_letu = response.json()["data"][0]
        except IndexError:
            print("There is no flight for given criteria!")
        else:
            city_from=podaci_o_letu['cityFrom']
            city_to=podaci_o_letu['cityTo']
            fly_to=podaci_o_letu['flyTo']
            fly_from=podaci_o_letu['flyFrom']
            local_departure=podaci_o_letu['local_departure']
            local_arrival = podaci_o_letu['local_arrival']
            price = podaci_o_letu['price']
            self.podaci={"city from":city_from,
                         "city to":city_to,
                         "fly to":fly_to,
                         "fly from":fly_from,
                         "local departure time":local_departure,
                         "local arrival time": local_arrival,
                         "price":price,
                         }

            account_sid = os.environ.get("ACCOUNT_SID")
            auth_token = os.environ.get("AUTH_TOKEN")
            phone_to = os.environ.get("PHONE_TO")
            phone_from = os.environ.get("PHONE_FROM")
            # account_sid = "AC26a95202bb8f01be0e538a9987d6cc6e"
            # auth_token = "cfad4d869aea65ff70efbdf6c5fbd252"
            # phone_to = "+381637031045"
            # phone_from = "+13194063102"


            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=f"Low price alert: Only ${self.podaci['price']} to fly from {self.podaci['city from']} to "
                     f"{self.podaci['city to']} from {self.podaci['local departure time']} to  "
                     f"{self.podaci['local arrival time']}.",
                from_=phone_from,
                to=phone_to
            )

            print(message.sid)
            return self.podaci
