from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'resumen', 'contenido', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 12}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
