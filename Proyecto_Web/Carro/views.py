# views.py (Corregido)
from django.shortcuts import render, redirect
from .carro import *
from Tienda.models import Producto

def agregarP(request, producto_id):
    carro = Carro(request)
    producto = Producto.objects.get(id = producto_id)
    carro.agregar(producto)
    return redirect("tienda:tienda") 


def eliminarP(request, producto_id):
    carro = Carro(request)
    producto = Producto.objects.get(id = producto_id)
    carro.eliminar(producto)
    return redirect("tienda:tienda")


def restarPro(request, producto_id):
    carro = Carro(request)
    producto = Producto.objects.get(id = producto_id)
    carro.restarP(producto)
    return redirect("tienda:tienda")


def limpiarC(request, producto_id):
    carro = Carro(request)
    carro.limpiarCarro()
    return redirect("tienda:tienda")


