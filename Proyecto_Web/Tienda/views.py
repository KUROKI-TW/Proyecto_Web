from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, CategoriaP
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .forms import FormularioProducto
from django.core.exceptions import PermissionDenied

def tienda(request):
    productos = Producto.objects.all()
    queryset = request.GET.get("buscar")
    if queryset:
        productos = productos.filter(
            Q(nombre__icontains=queryset) | Q(descripcion__icontains=queryset)
        )
    return render(request, "tienda.html", {"productos": productos})


def categoriaP(request, categoriap_id):
    categoriaP = CategoriaP.objects.get(id = categoriap_id)
    producto = CategoriaP.objects.filter(categoriaP = categoriaP)
    return render(request,"categorias.html",{"CategoriaP": CategoriaP, "Producto": producto})


def AgregarProductos(request):
    if not request.user.has_perm('Tienda.add_producto'):
        raise PermissionDenied   # 403 Forbidden
    if request.method == 'POST':
        producto = FormularioProducto(request.POST, request.FILES)
        if producto.is_valid():
            instance = producto.save(commit=False)
            instance.vendedor = request.user
            instance.save()
            producto.save_m2m()
            return redirect('tienda:tienda')
    else:
        producto = FormularioProducto()
    return render(request, "agregar_producto.html", {"producto": producto})

def EliminarProducto(request, producto_id):
    producto_a_borrar = get_object_or_404(Producto, id=producto_id)
    if request.user == producto_a_borrar.vendedor:
        producto_a_borrar.delete()
    return redirect('tienda:tienda')

def listaPost(request):
    producto = Producto.objects.all() 
    busqueda = request.GET.get("buscar") 
    if busqueda:
        articulos = articulos.filter(Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda))

    return render(request, "tienda.html", {"Articulos": articulos})