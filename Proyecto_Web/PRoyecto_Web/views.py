from django.shortcuts import render, HttpResponse
#from django.conf import settings
from Servicios.models import Servicio


def home(request):
    return render(request, "home.html")





