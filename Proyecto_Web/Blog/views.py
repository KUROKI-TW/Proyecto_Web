from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from Blog.models import Post, Categoria, Comentario, Like
from .forms import FormularioPost, FormularioComentario


def post(request):
    posts = Post.objects.all().order_by('-created').select_related('autor').prefetch_related(
        'categoria', 'likes', 'comentarios'
    ).annotate(
        likes_count=Count('likes', filter=Q(likes__es_like=True)),
        dislikes_count=Count('likes', filter=Q(likes__es_like=False)),
    )
    queryset = request.GET.get("buscar")
    if queryset:
        posts = posts.filter(titulo__icontains=queryset)
    return render(request, "blog.html", {"Post": posts})

def detalle_post(request, post_id):
    post_individual = get_object_or_404(
        Post.objects.select_related('autor').prefetch_related('categoria', 'comentarios'),
        id=post_id
    )
    form_comentario = FormularioComentario()
    return render(request, "detalle_post.html", {
        "post": post_individual,
        "form_comentario": form_comentario
    })

def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categoria=categoria).order_by('-created')
    return render(request, "categorias.html", {"Categoria": categoria, "Post": posts})

# ====== PERMISOS PARA CREAR POSTS (HTML) ======

@permission_required('Blog.add_post', raise_exception=True)
@login_required
def AgregarPost(request):
    if request.method == 'POST':
        formulario = FormularioPost(request.POST, request.FILES)
        if formulario.is_valid():
            instance = formulario.save(commit=False)
            instance.autor = request.user
            instance.save()
            
            nueva = request.POST.get('nueva_categoria', '').strip().lower()
            if nueva:
                cat, created = Categoria.objects.get_or_create(
                    nombre__iexact=nueva,
                    defaults={'nombre': nueva.capitalize()}
                )
                instance.categoria.add(cat)
                messages.success(request, f'Categoría "{cat.nombre}" asignada.')
            
            return redirect('Blog')
    else:
        formulario = FormularioPost()
    
    return render(request, "agregar_post.html", {"form": formulario})

@login_required
def EditarPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.autor:
        messages.error(request, 'No tienes permiso para editar este post.')
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
                messages.success(request, f'Categoría "{cat.nombre}" actualizada.')
            
            return redirect('detalle_post_url', post_id=post.id)
    else:
        formulario = FormularioPost(instance=post)
    
    return render(request, 'editar_post.html', {'form': formulario, 'post': post})

@login_required
def EliminarPost(request, post_id):
    post_a_borrar = get_object_or_404(Post, id=post_id)
    if request.user == post_a_borrar.autor:
        post_a_borrar.delete()
        messages.success(request, 'Post eliminado.')
    else:
        messages.error(request, 'No puedes eliminar este post.')
    return redirect('Blog')

# ====== VISTAS AJAX CON 403 FUERTE ======

@require_POST
def ToggleLike(request, post_id):
    """Vista AJAX: verifica autenticación MANUALMENTE y devuelve 403."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=403)
    
    post = get_object_or_404(Post, id=post_id)
    es_like = request.POST.get('es_like') == 'true'
    
    like, created = Like.objects.get_or_create(
        post=post, usuario=request.user, defaults={'es_like': es_like}
    )
    
    if not created:
        if like.es_like == es_like:
            like.delete()
        else:
            like.es_like = es_like
            like.save()
    
    return JsonResponse({
        'likes': post.likes.filter(es_like=True).count(),
        'dislikes': post.likes.filter(es_like=False).count()
    })

@require_POST
def AgregarComentario(request, post_id):
    """Vista AJAX: verifica autenticación MANUALMENTE y devuelve 403."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=403)
    
    post = get_object_or_404(Post, id=post_id)
    contenido = request.POST.get('contenido', '').strip()
    
    if not contenido:
        return JsonResponse({'error': 'Comentario vacío'}, status=400)
    
    comentario = Comentario.objects.create(
        post=post,
        autor=request.user,
        contenido=contenido,
        aprobado=True
    )
    
    return JsonResponse({
        'success': True,
        'id': comentario.id,
        'autor': comentario.autor.username,
        'contenido': comentario.contenido,
        'creado': comentario.creado.strftime('%d %b %Y %H:%M')
    })