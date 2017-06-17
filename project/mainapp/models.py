from django.db import models

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

	class Meta:
		unique_together = ('name','state',)