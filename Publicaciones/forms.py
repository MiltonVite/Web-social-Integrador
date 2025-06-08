from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la publicación (opcional)',
                'style': 'width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'post-input',
                'rows': 2,
                'placeholder': '¿Qué estás pensando?',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px;'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'margin-top: 10px;'
            }),
        }



