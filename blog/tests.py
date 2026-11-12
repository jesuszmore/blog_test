from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post, Visita


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester', password='secreto123'
        )
        self.post = Post.objects.create(
            titulo='Mi primer post',
            resumen='Un resumen breve',
            contenido='Contenido del post',
            autor=self.user,
        )

    def test_listado_muestra_posts_publicados(self):
        Post.objects.create(
            titulo='Borrador', resumen='r', contenido='c',
            autor=self.user, publicado=False,
        )
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi primer post')
        self.assertNotContains(response, 'Borrador')

    def test_slug_se_genera_automaticamente(self):
        segundo = Post.objects.create(
            titulo='Mi primer post', resumen='r', contenido='c', autor=self.user,
        )
        self.assertEqual(self.post.slug, 'mi-primer-post')
        self.assertEqual(segundo.slug, 'mi-primer-post-2')

    def test_detalle_registra_visita(self):
        url = reverse('blog:post_detail', args=[self.post.slug])
        self.client.get(url)
        self.client.get(url)
        self.assertEqual(Visita.objects.filter(post=self.post).count(), 2)

    def test_populares_ordena_por_visitas(self):
        otro = Post.objects.create(
            titulo='Post popular', resumen='r', contenido='c', autor=self.user,
        )
        Visita.objects.create(post=otro)
        Visita.objects.create(post=otro)
        response = self.client.get(reverse('blog:popular_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'][0], otro)

    def test_about_responde(self):
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)

    def test_crear_post_requiere_login(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_usuario_autenticado_crea_post(self):
        self.client.login(username='tester', password='secreto123')
        response = self.client.post(reverse('blog:post_create'), {
            'titulo': 'Post nuevo',
            'resumen': 'Resumen nuevo',
            'contenido': 'Contenido nuevo',
        })
        self.assertEqual(response.status_code, 302)
        nuevo = Post.objects.get(titulo='Post nuevo')
        self.assertEqual(nuevo.autor, self.user)
