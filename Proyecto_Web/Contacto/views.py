from django.shortcuts import render, redirect
from .forms import FormularioContacto
from django.core.mail import EmailMessage

def contactos(request):
    formularioContacto = FormularioContacto()
    if request.method == "POST":
        formularioContacto = FormularioContacto(data=request.POST)
        if formularioContacto.is_valid():
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            contenido = request.POST.get("contenido")
            emailE = EmailMessage("Mensaje desde app Django","el usuario{} con la direccion {} dice: \n\n {} ".format(nombre,email,contenido),"",["kurokitw89@gmail.com"],reply_to=[email])
            try:
                emailE.send()
                return redirect("/contactos/?ok")
            except:
                return redirect("/contactos/?no")
    return render(request, "contactos.html", {'mi_formulario': formularioContacto})
