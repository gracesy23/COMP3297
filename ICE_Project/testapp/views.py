from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
   today = datetime.datetime.now().date()
   return render(request, "hello.html", {"today" : today})