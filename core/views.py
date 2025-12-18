from django.shortcuts import render

def home(request):
    # Renderizamos la plantilla específica del home
    return render(request, 'home.html')