from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    resumen = models.CharField(max_length=300)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='posts/', blank=True)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(default=timezone.now)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_slug()
        super().save(*args, **kwargs)

    def _generate_slug(self):
        base = slugify(self.titulo) or 'post'
        slug = base
        numero = 2
        while Post.objects.filter(slug=slug).exists():
            slug = f'{base}-{numero}'
            numero += 1
        return slug

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


class Visita(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='visitas')
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-fecha']
        indexes = [models.Index(fields=['post', 'fecha'])]
        verbose_name = 'visita'
        verbose_name_plural = 'visitas'

    def __str__(self):
        return f'{self.post} - {self.fecha:%Y-%m-%d %H:%M}'
