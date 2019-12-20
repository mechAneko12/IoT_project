from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from .models import Data
import datetime
from django.core import serializers
import json
import numpy as np
import urllib.request

# Create your views here.
def index(request):
  template_name = "index.html" # templates以下のパスを書く
  return render(request,template_name)

def table(request):
    return render(request, 'table.html', {})

def analysis(request):
    return render(request, 'analysis.html', {})

def ml_get(request):
  #d = {"d": "a"}
  #return JsonResponse(d)
  data =  {
          "GlobalParameters": {
  }
      }

  body = str.encode(json.dumps(data))

  url = 'https://japaneast.services.azureml.net/workspaces/3927cd49e366419c8a640b70fc10e558/services/1e413a7026f64a929bff123a396fbf4d/execute?api-version=2.0&details=true'
  api_key = 'iSjyfHHP5YNIoTUNoK6P2NdEqCy6WUcTEEb6FW8CYfbGzv2sMdZpEjhpCJSirbTz744nTCrbVYH3A5fopSNrrw==' # Replace this with the API key for the web service
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

  req = urllib.request.Request(url, body, headers) 

  response = urllib.request.urlopen(req)

  result = response.read()
  d = json.loads(result.decode())

  j = {"d1": d["Results"]["output1"]["value"]["Values"][0][0], "d2": d["Results"]["output1"]["value"]["Values"][1][0]}
  return JsonResponse(j)


def tree_get(request):
  da = Data.objects.all()
  data = []
  target = []
  for h in da:
    day = []
    day.append(h.lux)
    day.append(h.temp_outside)
    day.append(h.temp_max)
    day.append(h.temp_min)
    day.append(h.temp_gap)
    day.append(h.temp_self)
    day.append(h.weather)
    day.append(h.Sunday)
    day.append(h.Monday)
    day.append(h.Tuesday)
    day.append(h.Wednesday)
    day.append(h.Thursday)
    day.append(h.Friday)
    day.append(h.Saturday)
    day.append(h.timezone_00_03)
    day.append(h.timezone_03_06)
    day.append(h.timezone_06_09)
    day.append(h.timezone_09_12)
    day.append(h.timezone_12_15)
    day.append(h.timezone_15_18)
    day.append(h.timezone_18_21)
    day.append(h.timezone_21_24)
    data.append(day)
    if h.efficiency >= 0.8:
      target.append(1)
    else:
      target.append(0)
    #target.append(h.efficiency)
  data = np.array(data)
  target = np.array(target)
  d = {"data": data, "target": target, 'target_names': np.array(["bad","good"], dtype='<U10'), 'feature_names': ['lux','temp_outside','temp_max','temp_min','temp_gap','temp_self','weather','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','timezone_00_03','timezone_03_06','timezone_06_09','timezone_09_12','timezone_12_15','timezone_15_18','timezone_18_21','timezone_21_24']}
  
  clf = tree.DecisionTreeClassifier(max_depth=5)
  clf = clf.fit(d["data"], d["target"])
  #predicted = clf.predict(d["data"])
  #print(sum(predicted == d["target"]) / len(d["target"]))
  #print(predicted)
  print(clf.tree_.feature)
  n = len(clf.tree_.feature)
  max_good = 0
  index = 0
  for i in range(n-1,-1,-1):
      if clf.tree_.feature[i] == -2:
          if clf.tree_.value[i][0][1] > max_good:
              max_good = clf.tree_.value[i][0][1]
              index = i

  t = []
  while index !=0:
      l = []
      for j in range(0,n):
          if clf.tree_.children_left[j] == index:
              l.append (j)
              l.append(clf.tree_.feature[j])
              l.append(clf.tree_.threshold[j])
              l.append(1)
              index = j
              break
          if clf.tree_.children_right[j] == index:
              l.append (j)
              l.append(clf.tree_.feature[j])
              l.append(clf.tree_.threshold[j])
              l.append(-1)
              index = j
              break
      t.append(l)

  print(t)
  s = ""
  s2 = "また、"
  week = ["日曜日","月曜日","火曜日","水曜日","木曜日","金曜日","土曜日"]
  time = ["0時から3時の時間帯","3時から6時の時間帯","6時から9時の時間帯","9時から12時の時間帯","12時から15時の時間帯","15時から18時の時間帯","18時から21時の時間帯","21時から24時の時間帯"]
  for k in range(len(t)-1,-1,-1):
      if t[k][1] == 0:
          s3 = ""
          if t[k][3] == 1:
              s3 += "以下"
          else:
              s3 += "以上"
          s += "照度は"+str(t[k][2])+s3 + "、"
      elif t[k][1] == 2:
          s3 = ""
          if t[k][3] == 1:
              s3 += "以下"
          else:
              s3 += "以上"
          s += "部屋の最高温度は"+str(math.floor(t[k][2]*10)/10)+s3 + "、"
      elif t[k][1] == 3:
          s3 = ""
          if t[k][3] == 1:
              s3 += "以下"
          else:
              s3 += "以上"
          s += "部屋の最低温度は"+str(math.floor(t[k][2]*10)/10)+s3 + "、"
      elif t[k][1] == 4:
          s3 = ""
          if t[k][3] == 1:
              s3 += "以上"
          else:
              s3 += "以下"
          s += "室内外の温度差は"+str(math.floor(t[k][2]*10)/10)+s3 + "、"
      elif t[k][1] == 6:
          s3 = ""
          if t[k][3] == 1:
              s3 += "雨の日、"
          else:
              s3 += "晴れの日、"
          s2 += s3
      elif t[k][1]>= 7 and t[k][1]<= 13:
          s3 = ""
          if t[k][3] == 1:
              s3 += "以外、"
          else:
              s3 += "、"
          s2 += week[t[k][1]-7] + s3
      elif t[k][1]>= 14:
          s3 = ""
          if t[k][3] == 1:
              s3 += "以外、"
          else:
              s3 += "、"
          s2 += time[t[k][1]-14] + s3
  s = s[:-1]
  s2 = s2[:-1]
  s += "が良いでしょう。"
  if len(s2)>= 5:
      s2 += "が最適です。"
      s += s2
  d = {"list": str(t), "d": s}
  return JsonResponse(d)

def sql_get(request):
  
  week =[request.POST.get('sun'),
        request.POST.get('mon'),
        request.POST.get('tue'),
        request.POST.get('wed'),
        request.POST.get('thu'),
        request.POST.get('fri'),
        request.POST.get('sat')]
  time =[]
  num = []
  column = []
  for i in range(7):
    data = Data.objects.filter(date_str = week[i])
    day = []
    n = 0
    if data.exists():
      
      for h in data:
        if h.name in column:
          pass
        else:
          column.append(h.name)
          
        n += 1
        day.append([h.name,h.actual_work_time,h.work_time-h.actual_work_time])
    else:
      day.append(['no',0,0])
    time.append(day)
    num.append(n)
    
  
  d = {"time": time,"num": num, "column": column}
  d = {"d": str(d)}
  #"sun": time[0], "mon": time[1],"tue": time[2],"wed": time[3], "thu": time[4], "fri": time[5], "sat": time[6]
  return JsonResponse(d)






def sql_post(request):
  '''
  return JsonResponse({"id": 1})
  d = str({"id": "1"})
  
  return HttpResponse(json.dumps(d), content_type="application/json")
  '''

  date = datetime.datetime.now()
  date_str = request.POST.get('date_str')
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
                              date_str = date_str,
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
      "id": data.id
  }
  return JsonResponse(d)

def sql_update(request):
  date = datetime.datetime.now()
  Id = request.POST.get('id')
  date_str = request.POST.get('date_str')
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
  data = Data.objects.filter(id = Id).update(name=name, 
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
  d ={"id": Id}
  return JsonResponse(d)

  '''
  d = {'id': Id}
  j = json.dumps(d)
  return HttpResponse(j)'''

  
