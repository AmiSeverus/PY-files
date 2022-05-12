# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer
from .helpers import isint, isfloat


class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        data = request.data
        if "name" not in data or not data['name']:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        name = data['name']
        desc = NULL
        if 'desc' in data and data['desc']:
            desc = data['desc']
        Sensor(name=name, desc=desc).save()
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def patch(self, request, pk):
        if not isint(pk):
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sensor = Sensor.objects.get(pk = int(pk))
        except Exception as e: 
            return Response({'status': f'error: {e}'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        name = False
        desc = False
        if 'name' in data and data['name']:
            name = data['name']
            sensor.name = name
        if 'desc' in data:
            desc = data['desc']
            sensor.desc = desc
        if isinstance(name,bool) and isinstance(desc, bool):
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        sensor.save()
        return Response({'status': 'ok'})
    

class MeasurementView(APIView):
    def post(self, request):
        data = request.data
        if 'sensor' not in data or 'temperature' not in data:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        sensor_id = data['sensor']
        temp = data['temperature']
        if not sensor_id or not temp:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        if not isint(sensor_id) or not isfloat(temp):
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        sensor_id = int(sensor_id)
        temp = float(temp)
        try:
            Measurement(sensor_id=Sensor.objects.get(pk = sensor_id), temp=temp).save()
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        except Exception as e: 
            return Response({'status': f'error: {e}'}, status=status.HTTP_404_NOT_FOUND)