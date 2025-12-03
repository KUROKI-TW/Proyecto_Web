from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import Post, Categoria
from .forms import FormularioPost
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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

@login_required
def AgregarPost(request):
    if request.method == 'POST':
        formulario = FormularioPost(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            instance.autor = request.user
            instance.save()
            formulario.save_m2m()
            nueva = request.POST.get('nueva_categoria', '').strip().lower()
            if nueva:
                cat, created = Categoria.objects.get_or_create(
                    nombre__iexact=nueva,
                    defaults={'nombre': nueva.capitalize()}
                )
                instance.categoria.add(cat)
            return redirect('Blog')
    else:
        formulario = FormularioPost()
    return render(request, 'agregar_post.html', {'form': formulario})

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

@login_required
def EditarPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.autor:
        return redirect('detalle_post_url', post_id=post.id)
    if request.method == 'POST':
        formulario = FormularioPost(request.POST, request.FILES, instance=post)
        if formulario.is_valid():
            formulario.save()
            nueva = request.POST.get('nueva_categoria', '').strip().lower()
            if nueva:
                cat, created = Categoria.objects.get_or_create(
                    nombre__iexact=nueva,
                    defaults={'nombre': nueva.capitalize()}
                )
                post.categoria.add(cat)
            return redirect('detalle_post_url', post_id=post.id)
    else:
        formulario = FormularioPost(instance=post)
    return render(request, 'editar_post.html', {'form': formulario, 'post': post})