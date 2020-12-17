from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework import generics
import pandas as pd
from math import radians, cos, sin, asin, sqrt


class CustomResponse():
    def successResponse(self, data={}, status=status.HTTP_200_OK, description="SUCCESS"):
        return Response(
            {
                "success": True,
                "errorCode": 0,
                "description": description,
                "info": data
            }, status=status)

    def errorResponse(self, data={}, description="ERROR", errorCode=1, status=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "success": False,
                "errorCode": errorCode,
                "description": description,
                "info": data
            }, status=status)


class GetValueBasedOnState(generics.ListAPIView):
    def get(self, request):
        state = request.GET.get("state")
        gas = request.GET.get("gas")

        gasObj = GasDetails.objects.filter(
            state=state, gas=gas)
        res = []
        for gs in gasObj:
            dic = {
		   "date": gs.date,
		   "state":gs.state,
                
		   "value": gs.value
                
               
            }
            res.append(dic)
	
        if not res:
            return CustomResponse().errorResponse(description="No such detail to display")
        else:
            return CustomResponse().successResponse(res, description="Displayed the details")

class getGasByDate(generics.ListAPIView):
    def get(self, request):
        date = request.GET.get("date")
        gas = request.GET.get("gas")

        gasObj = GasDetails.objects.filter(date=date, gas=gas)
        res = []
        for gs in gasObj:
            dic = {
                "State": gs.state,
                "Value": gs.value
            }
            res.append(dic)
        if not res:
            return CustomResponse().errorResponse(description="No such detail to display")
        else:
            return CustomResponse().successResponse(res, description="Displayed the details")


class GetGasInDateRange(generics.ListAPIView):
    def get(self, request):
        startDate = request.GET.get("startDate")
        endDate = request.GET.get("endDate")
        gas = request.GET.get("gas")
        gasObj = GasDetails.objects.filter(
            gas=gas, date__range=[startDate, endDate]).order_by('date')
        res = []
        for gs in gasObj:
            dic = {
                "Date": gs.date,
                "Gas": gas,
                "Value": gs.value,
                "State": gs.state
            }
            res.append(dic)

        if not res:
            return CustomResponse().errorResponse(description="No such detail to display")
        else:
            return CustomResponse().successResponse(res, description="Displayed the details")

class GetNearestData(generics.ListAPIView):

    def dist(lat1, long1, lat2, long2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
        # haversine formula
        dlon = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers is 6371
        km = 6371* c
        return km

    def get(self,request):
        lat = request.GET.get("lat")
        lon = request.GET.get('lon')
        gas = request.GET.get('gas')
        low = 999999
        value = 0
        df = pd.DataFrame.from_records(
        LiveDetails.objects.filter(gas=gas).values_list('lat', 'lon', 'gas', 'value') )
        # sdd = pd.DataFrame.from_records(
        # GasDetails.objects.all().values_list('state', 'value', 'gas', 'date') )
        for i in range(0,len(df)):
            distance = dist(lat,lon,df[0][i],df[1][i])
            if distance < low:
                low = distance
                value = df[3][i]

        res = {'con':value,'gas':gas,'lat':lat,'lon':lon}

        return CustomResponse.successResponse(res, description="success")
