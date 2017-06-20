import kronos
import requests
import json


from mainapp.models import State, City, DailyRate, Fuel, FuelCompany
from mainapp.constants import state_code



def request_fuel(state_name,provider_obj,response_data,fuel_obj):
    # import pdb;pdb.set_trace()
    for data in response_data:
        for key in data:
            city_name,price = key, data[key]
        try:
            price = float(data[key])
        except Exception as e:
            price = 0
        state_obj,is_new_state = State.objects.get_or_create(name=state_name)
        city_obj,is_created = City.objects.get_or_create(name=city_name.lower(),state=state_obj)
        rate_entry,is_update = DailyRate.objects.update_or_create(fuel=fuel_obj,city=city_obj, provider=provider_obj,price=price)
        if is_update:
            print("inserted")
        else:
            print("updated")





@kronos.register('0 7 * * *')
def get_latest_fuel_rate():
    fuel_list = ['p','d']
    for item in fuel_list:
        for state in state_code:
            for key in state:
                print key
                response = requests.post(url="https://fuelprice.p.mashape.com/",
                  headers={
                    "X-Mashape-Key": "jx4BiSi6U0mshgp6QifRhbg3YwAAp11sx6CjsnXQNhDiDnjalX",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                  },
                  data=(json.dumps({'fuel':item,'state':key}))
                )
                response =  json.loads(response.text)
                # # import pdb;pdb.set_trace()
                hp_provider = FuelCompany.objects.get(name='hp')
                iocl_provider = FuelCompany.objects.get(name='iocl')
                fuel_obj, is_created_new_obj = Fuel.objects.get_or_create(name=response['fuel'].lower())
                request_fuel(response['state'].lower(),hp_provider,response['prices']['hp'],fuel_obj)
                request_fuel(response['state'].lower(),iocl_provider,response['prices']['iocl'],fuel_obj)

