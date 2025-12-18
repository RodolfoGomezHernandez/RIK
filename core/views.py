from django.shortcuts import render

def home(request):
    # Renderizamos base.html temporalmente para probar el diseño
    return render(request, 'base.html')
    return render(request, 'home.html')