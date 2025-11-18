def importeTotal(request):
    total = 0
    carro_data = request.session.get("carro", {})
    for key, value in carro_data.items():
        try:
            total = total + (float(value["precio"]) * value["cantidad"])
        except (ValueError, TypeError):
            pass
    return {"importeTotal": total}