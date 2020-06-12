from django.shortcuts import render
from django.views.generic import View
from .models import Data
from rest_framework.views import APIView
from rest_framework.response import Response



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request, format=None):
        tempdata=Data.objects.values('temperature_surface')
        ghidata=Data.objects.values('ghi')
        timedata=Data.objects.values('time')

        temp_list = []
        for key in tempdata:
            temp_list.append(key['temperature_surface'])

        ghi_list = []
        for key in ghidata:
            ghi_list.append(key['ghi'])

        time_list = []
        for key in timedata:
            time_list.append(key['time'])

        data={
            'Temp':temp_list,
            'GHI':ghi_list,
            'Time': time_list,
        }

        return Response(data)


class HomeView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'charts.html',{})
