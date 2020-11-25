from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework import generics


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
        date = request.GET.get("date")
        gas = request.GET.get("gas")

        gasObj = GasDetails.objects.filter(
            state=state, gas=gas, date=date).first()
        if not gasObj:
            return CustomResponse().errorResponse(description="No such gas present for the given values")
        dic = {
            "gasId": gasObj.gasId,
            "state": gasObj.state,
            "value": gasObj.value,
            "date": gasObj.date,
            "gas": gasObj.gas
        }
        return CustomResponse().successResponse(dic, description="Displayed the details")


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
