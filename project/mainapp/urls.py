from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_states/', views.get_states),
    url(r'^get_cities/', views.get_cities),
    url(r'^get_rate/', views.get_rate),
    url(r'^get_nearest/', views.nearest_city),
    url(r'^get_hpcl/', views.hpcl),

]