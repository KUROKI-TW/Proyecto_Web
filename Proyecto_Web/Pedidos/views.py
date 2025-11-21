from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pedido, LineaPedido
from Carro.carro import Carro
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

@login_required(login_url="Autenticacion/logear")
def procesar_pedido(request):
    pedido = Pedido.objects.create(user = request.user)
    carro = Carro(request)
    lienas_pedidos = list()
    for key, value in carro.carro.items():
        lienas_pedidos.append(LineaPedido(
            producto_id = key,
            cantidad = value["cantidad"],
            user = request.user,
            pedido = pedido,
        ))

    LineaPedido.objects.bulk_create(lienas_pedidos)

    enviarMail(
        pedido = pedido,
        lienasPedidos= lienas_pedidos,
        nombreUsuario= request.user.username,
        emailUsuario = request.user.ermail
    )

    messages.success(request, "Pedido realizado exitosamente")
    return redirect("../tienda")

def enviarMail(**kwars):
    asunto = "Gracias por su compra"
    mensaje = render_to_string("pedido.html",{
        "pedido": kwars.get("pedido"),
        "lienasPedidos": kwars.get("lienasPedidos"),
        "nombreUsuario": kwars.get("nombreUsuario"),
    })
    mensajeTexto = strip_tags(mensaje)
    emailFrom = "victor56927467@gmail.com"
    destinatario = kwars.get("emailUsuario")

    send_mail(asunto,mensajeTexto,emailFrom,[destinatario],html_message=mensaje)
