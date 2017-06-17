from django.db import models
import datetime
# Create your models here.

class State(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	class Meta:
		unique_together = ('name',) 

class City(models.Model):
	name = models.CharField(max_length=100)
	state = models.ForeignKey(State, related_name="state_name",blank=False)

	def __str__(self):
		return self.name
	class Meta:
		unique_together = ('name','state',)

class Fuel(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class DailyRate(models.Model):
	fuel = models.ForeignKey(Fuel, related_name="fuel_name")
	city = models.ForeignKey(City, related_name="city_name")
	price = models.FloatField(default=0)
	date = models.DateField(default=datetime.date.today)

	def __str__(self):
		return self.city.name +' '+ self.fuel.name + ' '+str(self.price)
	class Meta:
		unique_together = ('fuel','city',)
