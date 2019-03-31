from django.shortcuts import render

def hello(request):
   return render(request, "testapp/template/hello.html", {})