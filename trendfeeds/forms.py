from django import forms
from .models import InteracaoUsuario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = InteracaoUsuario
        fields = ['comentario']  # Só queremos o campo de comentário