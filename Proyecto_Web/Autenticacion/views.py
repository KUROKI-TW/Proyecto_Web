from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.contrib import messages
import random
from Blog.models import Post
from django.contrib.auth.models import User

# Formulario personalizado de registro
class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    respuesta_captcha = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Respuesta'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clase CSS a todos los campos
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

class VRegistro(View):
    def generar_captcha(self, request):
        """Genera una operación matemática simple y guarda la respuesta en sesión"""
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operacion = random.choice(['+', '-'])
        
        if operacion == '+':
            respuesta = num1 + num2
            pregunta = f"{num1} + {num2} = ?"
        else:
            # Asegurar que el resultado no sea negativo
            num1, num2 = max(num1, num2), min(num1, num2)
            respuesta = num1 - num2
            pregunta = f"{num1} - {num2} = ?"
        
        # Guardar AMBOS en sesión
        request.session['captcha_respuesta'] = respuesta
        request.session['captcha_pregunta'] = pregunta
        return pregunta

    def get(self, request):
        form = FormularioRegistro()
        pregunta = self.generar_captcha(request)
        return render(request, "registro.html", {
            "form": form,
            "pregunta_captcha": pregunta
        })

    def post(self, request):
        # IMPORTANTE: NO generar nuevo captcha al inicio del POST
        form = FormularioRegistro(request.POST)
        
        # Recuperar la respuesta correcta del captcha generado en el GET
        respuesta_correcta = request.session.get('captcha_respuesta')
        
        if form.is_valid():
            # Verificar respuesta del captcha
            respuesta_usuario = form.cleaned_data.get('respuesta_captcha')
            
            if respuesta_usuario != respuesta_correcta:
                messages.error(request, f"Respuesta matemática incorrecta. La respuesta correcta era {respuesta_correcta}. Intenta de nuevo.")
                # Generar NUEVO captcha solo si falló
                pregunta = self.generar_captcha(request)
                return render(request, "registro.html", {
                    "form": form,
                    "pregunta_captcha": pregunta
                })
            
            # Crear usuario sin guardar aún
            usuario = form.save(commit=False)
            usuario.email = form.cleaned_data['email']
            usuario.save()
            
            # Asignar permisos para el modelo Post
            try:
                content_type = ContentType.objects.get_for_model(Post)
                permisos = Permission.objects.filter(
                    content_type=content_type,
                    codename__in=['add_post', 'change_post', 'delete_post', 'view_post']
                )
                usuario.user_permissions.add(*permisos)
                messages.success(request, f"✅ Permisos asignados correctamente: {', '.join([p.codename for p in permisos])}")
            except Exception as e:
                messages.warning(request, f"Usuario creado pero hubo un error asignando permisos: {e}")
            
            # Loguear usuario automáticamente
            login(request, usuario)
            messages.success(request, f"🎉 Registro exitoso. Bienvenido {usuario.username}!")
            return redirect('Home')
        else:
            # Si hay errores en el formulario, regenerar captcha
            pregunta = self.generar_captcha(request)
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            
            return render(request, "registro.html", {
                "form": form,
                "pregunta_captcha": pregunta
            })

def logaut(request):
    """Cierra la sesión del usuario actual"""
    logout(request)
    return redirect('Home')

def logear(request):
    """Maneja el inicio de sesión"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombreU = form.cleaned_data.get("username")
            contraU = form.cleaned_data.get("password")
            usuario = authenticate(username=nombreU, password=contraU)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                messages.error(request, "Usuario no válido")
        else:
            messages.error(request, "Información incorrecta")
    
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})
