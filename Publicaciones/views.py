from django.shortcuts import render, redirect, get_object_or_404
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required
from .models import Publicacion
from Usuarios.models import UsuarioPersonalizado

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('lista_publicaciones')
    else:
        form = PublicacionForm()
    
    return render(request, 'publicaciones/crear_publicacion.html', {'form': form})

def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion')
    return render(request, 'publicaciones/lista_publicaciones.html', {
        'publicaciones': publicaciones
    })

def publicaciones_por_usuario(request, username):
    usuario = get_object_or_404(UsuarioPersonalizado, username=username)
    publicaciones = Publicacion.objects.filter(autor=usuario).order_by('-fecha_publicacion')
    return render(request, 'publicaciones/publicaciones_usuario.html', {
        'usuario': usuario,
        'publicaciones': publicaciones
    })
