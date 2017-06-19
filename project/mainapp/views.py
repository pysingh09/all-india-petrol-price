from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from models import State, City, DailyRate
import json
from django.core.serializers.json import DjangoJSONEncoder
from math import cos, asin, sqrt
import requests
from xml.dom import minidom
# Create your views here.

def get_states(request):
	data = State.objects.all().values('id','name')
	data = json.dumps(list(data), cls=DjangoJSONEncoder)
	return JsonResponse(data,safe=False)

def  get_cities(request):
	state_id = 14
	data = City.objects.filter(state_id=14).values('id','name')
	data = json.dumps(list(data), cls=DjangoJSONEncoder)
	return JsonResponse(data,safe=False)


def get_rate(request):
	city_id = 1
	fuel_id = 1
	data = DailyRate.objects.filter(city__id= city_id, fuel__id=fuel_id).values('price','date')
	data = json.dumps(list(data),cls=DjangoJSONEncoder)
	return JsonResponse(data,safe=False)




# use like that http://localhost:8000/app/get_nearest/?city=indore
def nearest_city(request):
        # city from get parameter
        cityName=request.GET['city']
        cities=[]

        City_obj=City.objects.get(name=cityName)
        All_city = City.objects.filter(state=City_obj.state)

        for cities_list in All_city:
        	if(cities_list.name!=cityName):
        		cities.append(cities_list.name)

        cities_distance={}

        
        resultFromGraphApi=requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+cityName+"&region=in").json()
        base_x=resultFromGraphApi['results'][0]['geometry']['location']['lat']
        base_y=resultFromGraphApi['results'][0]['geometry']['location']['lng']

        for value in cities:
                tempGraphApi=requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+value+"&region=in").json()
                temp_x=tempGraphApi['results'][0]['geometry']['location']['lat']
                temp_y=tempGraphApi['results'][0]['geometry']['location']['lng']
                cities_distance[value]=distaceBetweenTwoCity(base_x,base_y,temp_x,temp_y)       
        
        return JsonResponse(json.dumps(sorted(cities_distance.items(), key=lambda x: x[1])),safe=False)


def distaceBetweenTwoCity(lat1,lon1,lat2,lon2):
        p = 0.017453292519943295     #Pi/180
        a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a)) #2*R*asin...



def hpcl(request):
        cityName=request.GET['city']
        price=[]
        code_for={'Andhra Pradesh':'AP1?1497810068505','Arunachal Pradesh':0,'Assam':'AS?1497810198948','Bihar':'BR?1497810276248','Chhattisgarh':'CH?1497810328900','Goa':'GA?1497812837117','Gujarat':'GJ?1497812860178','Haryana':'HR?1497812895379','Himachal Pradesh':'HP?1497812917333','Jammu & Kashmir':'JK?1497812934641','Jharkhand':'JH?1497812956639','Karnataka':'KA?1497812980614','Kerala':'KL?1497812997418','Madhya Pradesh':'MP?1497781879','Maharashtra':'MH?1497813023545','Manipur':'MN?1497813059119','Meghalaya':'ML?1497813041741','Mizoram':'MZ?1497813076853','Nagaland':'NL?1497813094298','Odisha':'OR?1497813112243','Punjab':'PB?1497813129232','Rajasthan':'RJ?1497813142871','Sikkim':'SK?1497813159354','Tamil Nadu':'TN?1497813184980','Telangana':'TG?1497813208623','Tripura':'TR?1497813226232','Uttar Pradesh':'UP?1497813241485','Uttarakhand':'UT?1497813263160','West Bengal':'WB?1497813279542'}
        City_obj=City.objects.get(name=cityName)
        codeforGivenCity=code_for[str(City_obj.state)]
        
        result=requests.get("http://hproroute.hpcl.co.in/StateDistrictMap_4/fetchmshsdprice.jsp?param=T&statecode="+codeforGivenCity)
        xmldoc = minidom.parseString(result.text)
        itemlist = xmldoc.getElementsByTagName('marker')
        for s in itemlist:
                if (s.attributes['townname'].value.lower()==cityName.lower()):
                        price.append(s.attributes['ms'].value)
                        price.append(s.attributes['hsd'].value)
                        break




        
        return JsonResponse(price,safe=False)






'''
Function  to map all state string in db

'''
def pupulate_states():
	state_list = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal']
	model_obj = []
	for state in state_list:
		model_obj.append(State(name=state))
	State.objects.bulk_create(model_obj)

	print("populated")
	




	
