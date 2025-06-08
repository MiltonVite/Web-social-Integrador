from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse

#BORRAR
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .forms import FormularioRegistro
from .models import UsuarioPersonalizado
from django.http import HttpResponse
#----------------------------

from WebSocial import settings
from .models import UsuarioPersonalizado, Estudiante, Docente, TokensVerificacion


def enviar_correo_verificacion(usuario, token):
    asunto = 'Verificación de cuenta'
    mensaje = f""" Hola {usuario.nombre} {usuario.apellido},
    Gracias por registrarte en nuestra plataforma. Para completar tu registro, necesitamos que verifiques tu cuenta.

    Por favor, verifica tu cuenta haciendo clic en el siguiente enlace:
    http://127.0.0.1:8000/activar/{token}/

    Este enlace es válido por 24 horas.

    Saludos.
    """

    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [usuario.email],
        fail_silently=False,
    )

def registro_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        carrera = request.POST.get('carrera')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo = request.POST.get('sexo')
        ubicacion = request.POST.get('ubicacion')
        tipo_usuario = 'Estudiante'
        anio_ingreso = request.POST.get('anio_ingreso')
        ciclo = request.POST.get('ciclo')
        dni = request.POST.get('dni')
        username = nombre + apellido + dni

        dominio = '@utp.edu.pe'
        if not email.endswith(dominio):
            error = f"El correo electrónico debe tener el dominio {dominio}."
            return render(request, 'Usuarios/registro_estudiante.html', {'error': error})

        if password != password2:
            error = "Las contraseñas no coinciden."
            return render(request, 'Usuarios/registro_estudiante.html', {'error': error})
        
        if UsuarioPersonalizado.objects.filter(email=email).exists():
            error = "El correo electrónico ya está en uso."
            return render(request, 'Usuarios/registro_estudiante.html', {'error': error})
        
        usuarioCreado = UsuarioPersonalizado.objects.create_user(
            username=username,
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            carrera=carrera,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            ubicacion=ubicacion,
            tipoUsuario=tipo_usuario,
            dni=dni,
            is_active=False
        )

        Estudiante.objects.create(
            usuario=usuarioCreado,
            carrera=carrera,
            anio_ingreso= anio_ingreso,
            ciclo=ciclo
        )

        token = TokensVerificacion.objects.create(
            usuario=usuarioCreado,
            token=default_token_generator.make_token(usuarioCreado),
            fecha_expiracion= timezone.now() + timezone.timedelta(hours=24)
        )

        enviar_correo_verificacion(usuarioCreado, token.token)

        return render(request, 'Usuarios/correo_enviado.html', {'email': email}) 
    else:
        return render(request, 'Usuarios/registro_estudiante.html')

def registro_profesor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo = request.POST.get('sexo')
        ubicacion = request.POST.get('ubicacion')
        tipo_usuario = 'Profesor'
        facultad_dirigido = request.POST.get('facultad_dirigido')
        carrera = request.POST.get('carrera')
        dni = request.POST.get('dni')
        username = nombre + apellido + dni


        if password != password2:
            error = "Las contraseñas no coinciden."
            return render(request, 'Usuarios/registro_profesor.html', {'error': error})
        
        if UsuarioPersonalizado.objects.filter(email=email).exists():
            error = "El correo electrónico ya está en uso."
            return render(request, 'Usuarios/registro_profesor.html', {'error': error})
        
        usuarioCreado = UsuarioPersonalizado.objects.create_user(
            username=username,
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            carrera=carrera,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            ubicacion=ubicacion,
            tipoUsuario=tipo_usuario,
            dni=dni,
            is_active=False
        )

        Docente.objects.create(
            usuario=usuarioCreado,
            facultadDirigido=facultad_dirigido            
        )

        token = TokensVerificacion.objects.create(
            usuario=usuarioCreado,
            token=default_token_generator.make_token(usuarioCreado),
            fecha_expiracion=timezone.now() + timedelta(hours=24)
        )

        enviar_correo_verificacion(usuarioCreado, token.token)

        return render(request, 'Usuarios/correo_enviado.html', {'email': email})
    else:
        return render(request, 'Usuarios/registro_profesor.html')


def activar_cuenta(request, token):
    try:
        token_obj = TokensVerificacion.objects.get(token=token)
    except TokensVerificacion.DoesNotExist:
        return render(request, 'Usuarios/error_activar_cuenta.html', {'error': 'Token inválido o expirado.'})

    if token_obj.fecha_expiracion < timezone.now():
        return render(request, 'Usuarios/error_activar_cuenta.html', {'error': 'Token expirado.'})

    usuario = token_obj.usuario
    usuario.is_active = True
    usuario.save()
    token_obj.delete()

    return render(request, 'Usuarios/cuenta_activada.html', {'success': 'Cuenta activada exitosamente.'})

def enviar_correo_prueba(request):
    send_mail(
        subject='Prueba de correo desde Django',
        message='Este es un correo de prueba enviado desde tu proyecto Django.',
        from_email=None,  # Usará DEFAULT_FROM_EMAIL
        recipient_list=['ssuarezvi5@ucvvirtual.edu.pe'],  # Cambia por el correo donde quieres recibirlo
        fail_silently=False,
    )
    return HttpResponse("Correo enviado correctamente.")

# BORRAR------------------------------------------------
def registrar_usuario(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Inactivar hasta que confirme el correo
            user.save()
            dominio = get_current_site(request).domain
            asunto = "Activa tu cuenta"
            mensaje = render_to_string('Usuarios/activacion_email.html', {
                'user': user,
                'dominio': dominio,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(asunto, mensaje, None, [user.email])
            return render(request, 'Usuarios/correo_enviado.html')
    else:
        form = FormularioRegistro()
    return render(request, 'Usuarios/registro.html', {'form': form})



def activar_usuario(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UsuarioPersonalizado.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UsuarioPersonalizado.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'usuarios/activacion_exitosa.html')
    else:
        return render(request, 'usuarios/activacion_fallida.html')
    


def enviar_correo_prueba(request):
    send_mail(
        subject='Prueba de correo desde Django',
        message='Este es un correo de prueba enviado desde tu proyecto Django.',
        from_email=None,  # Usará DEFAULT_FROM_EMAIL
        recipient_list=['ssuarezvi5@ucvvirtual.edu.pe'],  # Cambia por el correo donde quieres recibirlo
        fail_silently=False,
    )
    return HttpResponse("Correo enviado correctamente.")

# BORRAR------------------------------------------------