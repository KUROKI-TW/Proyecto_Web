from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import Post, Categoria
from .forms import FormularioPost
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

def post(request):
    posts = Post.objects.all().order_by('-created')
    queryset = request.GET.get("buscar")
    if queryset:
        posts = posts.filter(titulo__icontains=queryset)
    return render(request, "blog.html", {"Post": posts})

def detalle_post(request, post_id):
    # Busca el post por su ID, o devuelve un error 404 si no existe
    post_individual = get_object_or_404(Post, id=post_id)
    return render(request, "detalle_post.html", {"post": post_individual})

def categoria(request, categoria_id):
    categoria = Categoria.objects.get(id = categoria_id)
    post = Post.objects.filter(categoria = categoria)
    return render(request,"categorias.html",{"Categoria": Categoria, "Post": post})

@permission_required('Blog.add_post', raise_exception=True)
def AgregarPost(request):
    if request.method == 'POST':
        formulario = FormularioPost(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            instance.autor = request.user
            instance.save()
            formulario.save_m2m()
            return redirect('Blog')
    else:
        formulario = FormularioPost()
    return render(request, "agregar_post.html", {"form": formulario})

def EliminarPost(request, post_id):
    post_a_borrar = get_object_or_404(Post, id=post_id)
    if request.user == post_a_borrar.autor:
        post_a_borrar.delete()
    return redirect('Blog')


def listaPost(request):
    # Obtenemos todos primero
    post = Post.objects.all() 
    busqueda = request.GET.get("buscar") 
    if busqueda:
        articulos = articulos.filter(Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda))

    return render(request, "blog.html", {"Articulos": articulos})