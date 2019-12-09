from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from .models import Data
import datetime
from django.core import serializers
import json

# Create your views here.
def index(request):
  template_name = "index.html" # templates以下のパスを書く
  return render(request,template_name)

def table(request):
    return render(request, 'table.html', {})

def sql_post(request):
  HttpResponse(json.dumps({'name': name}), content_type="application/json")
  
  d = {'id': '1'}
  
  return JsonResponse(d)
  '''

  date = datetime.datetime.now()
  name = request.POST.get('name')
  lux = request.POST.get('lux')
  temp_outside = request.POST.get('temp_outside')
  temp_max = request.POST.get('temp_max')
  temp_min = request.POST.get('temp_min')
  temp_gap = request.POST.get('temp_gap')
  temp_self = request.POST.get('temp_self')
  weather = request.POST.get('weather')
  Sunday = request.POST.get('Sunday')
  Monday = request.POST.get('Monday')
  Tuesday = request.POST.get('Tuesday')
  Wednesday = request.POST.get('Wednesday')
  Thursday = request.POST.get('Thursday')
  Friday = request.POST.get('Friday')
  Saturday = request.POST.get('Saturday')
  timezone_00_03 = request.POST.get('timezone_00_03')
  timezone_03_06 = request.POST.get('timezone_03_06')
  timezone_06_09 = request.POST.get('timezone_06_09')
  timezone_09_12 = request.POST.get('timezone_09_12')
  timezone_12_15 = request.POST.get('timezone_12_15')
  timezone_15_18 = request.POST.get('timezone_15_18')
  timezone_18_21 = request.POST.get('timezone_18_21')
  timezone_21_24 = request.POST.get('timezone_21_24')
  work_time = request.POST.get('work_time')
  actual_work_time = request.POST.get('actual_work_time')
  efficiency = request.POST.get('efficiency')
  data = Data.objects.create(date = date,
                              name=name, 
                              lux = lux,
                              temp_outside = temp_outside,
                              temp_max = temp_max,
                              temp_min = temp_min,
                              temp_gap = temp_gap,
                              temp_self = temp_self,
                              weather = weather,
                              Sunday = Sunday,
                              Monday = Monday,
                              Tuesday = Tuesday,
                              Wednesday = Wednesday,
                              Thursday = Thursday,
                              Friday = Friday,
                              Saturday = Saturday,
                              timezone_00_03 = timezone_00_03,
                              timezone_03_06 = timezone_03_06,
                              timezone_06_09 = timezone_06_09,
                              timezone_09_12 = timezone_09_12,
                              timezone_12_15 = timezone_12_15,
                              timezone_15_18 = timezone_15_18,
                              timezone_18_21 = timezone_18_21,
                              timezone_21_24 = timezone_21_24,
                              work_time = work_time,
                              actual_work_time = actual_work_time,
                              efficiency =efficiency)
  d = {
      'id': data.id,
  }
  return JsonResponse(d)
  '''
