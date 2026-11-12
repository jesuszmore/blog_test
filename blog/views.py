from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView

from .forms import PostForm
from .models import Post, Visita


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def post_list(request):
    posts = (
        Post.objects.filter(publicado=True)
        .annotate(total_visitas=Count('visitas'))
        .order_by('-creado')
    )
    page = Paginator(posts, 6).get_page(request.GET.get('page'))
    return render(request, 'blog/post_list.html', {'page': page, 'posts': page.object_list})


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.annotate(total_visitas=Count('visitas')),
        slug=slug,
        publicado=True,
    )
    Visita.objects.create(
        post=post,
        ip=_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
    )
    post.total_visitas += 1
    return render(request, 'blog/post_detail.html', {'post': post})


def popular_posts(request):
    posts = (
        Post.objects.filter(publicado=True)
        .annotate(total_visitas=Count('visitas'))
        .order_by('-total_visitas', '-creado')
    )
    page = Paginator(posts, 6).get_page(request.GET.get('page'))
    return render(request, 'blog/popular_posts.html', {'page': page, 'posts': page.object_list})


def about(request):
    return render(request, 'blog/about.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        self.object = form.save()
        messages.success(self.request, '¡Post publicado correctamente!')
        return super().form_valid(form)
