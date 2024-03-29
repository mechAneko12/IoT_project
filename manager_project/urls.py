"""manager_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('manager.urls')),
    path('table/', views.table, name='table'),
    path("table/sql_get/",  views.sql_get, name = "sql_get"),
    path("table/tree_get/",  views.tree_get, name = "tree_get"),

    path("table/ml_get/",  views.ml_get, name = "ml_get"),

    #path("sql_post/", views.sql_post, name = "sql_post"),
    path('analysis/', views.analysis, name='analysis'),
]
