from django.shortcuts import render

# Create your views here.
def index(request):
  template_name = "index.html" # templates以下のパスを書く
  return render(request,template_name)

def mainjs(request):
  template_name = "main.js" # templates以下のパスを書く
  return render(request,template_name)

def stylecss(request):
  template_name = "style.css" # templates以下のパスを書く
  return render(request,template_name)