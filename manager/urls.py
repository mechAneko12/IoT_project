from django.urls import path
from . import views

urlpatterns = [
  path("",views.index,name="index"),
  #path("",views.mainjs,name="main.js"),
  #path("",views.stylecss,name="style.css"),
]