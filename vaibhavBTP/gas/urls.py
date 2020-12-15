from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [path("getValueBasedOnGasState/",
                    GetValueBasedOnState.as_view()),
               path("getValuesForDate/", getGasByDate.as_view()),
               path("getValueInARange/", GetGasInDateRange.as_view()), 
               path("getNearest/", GetNearestData.as_view())]
