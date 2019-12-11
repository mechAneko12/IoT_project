from django.urls import path
from . import views

urlpatterns = [
  path("",views.index,name="index"),
  #path("",views.mainjs,name="main.js"),
  #path("",views.stylecss,name="style.css"),
  path("sql_post/", views.sql_post, name = "sql_post"),
  path("sql_update/", views.sql_update, name = "sql_update"),
  #path("table/sql_get/", views.sql_get, name = "sql_get"),
]