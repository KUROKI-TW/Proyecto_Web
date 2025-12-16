from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def ajax_login_required(view_func):
    """
    Decorador que devuelve 403 para AJAX si no está autenticado,
    pero redirige para peticiones normales (HTML).
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Petición AJAX: devuelve 403
                return JsonResponse({'error': 'No autenticado'}, status=403)
            else:
                # Petición normal: redirige
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
        return view_func(request, *args, **kwargs)
    return wrapper