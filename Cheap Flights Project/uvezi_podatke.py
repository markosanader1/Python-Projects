import requests
class IATA():
    def __init__(self):
       self.data={}

    def uvezi(self):
        city= input("From which city do you travel? ").title()
        headers={
             "apikey":"P2g91cc90plohdtMAFhDs9cRkc6-QmVX",
        }
        url="https://tequila-api.kiwi.com/locations/query"
        parameters={
            "term":city,
            "locale":"en-US",
            "location_types":"city",
            "limit":1,
        }
        response = requests.get(url=url, headers=headers, params=parameters)
        self.data= response.json()['locations'][0]['code']
        return self.data
