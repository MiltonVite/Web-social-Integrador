from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('', views.lista_publicaciones, name='lista_publicaciones'),
    path('usuario/<str:username>/', views.publicaciones_por_usuario, name='publicaciones_usuario'),

]