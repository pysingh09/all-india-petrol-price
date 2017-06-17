from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from mainapp.models import State, City
import json
from django.core.serializers.json import DjangoJSONEncoder
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

	
