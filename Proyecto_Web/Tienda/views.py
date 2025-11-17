from django.shortcuts import render, get_object_or_404
from .models import Producto, CategoriaP

def tienda(request):
    producto = Producto.objects.all()
    return render(request, "tienda.html", {"Producto": producto})


def categoriaP(request, categoriap_id):
    categoriaP = CategoriaP.objects.get(id = categoriap_id)
    producto = CategoriaP.objects.filter(categoriaP = categoriaP)
    return render(request,"categorias.html",{"CategoriaP": CategoriaP, "Producto": producto})

