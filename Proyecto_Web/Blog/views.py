from django.shortcuts import render, get_object_or_404
from Blog.models import Post, Categoria

def post(request):
    post = Post.objects.all()
    return render(request, "blog.html", {"Post": post})

def detalle_post(request, post_id):
    # Busca el post por su ID, o devuelve un error 404 si no existe
    post_individual = get_object_or_404(Post, id=post_id)
    return render(request, "detalle_post.html", {"post": post_individual})

def categoria(request, categoria_id):
    categoria = Categoria.objects.get(id = categoria_id)
    post = Post.objects.filter(categoria = categoria)
    return render(request,"categorias.html",{"Categoria": Categoria, "Post": post})