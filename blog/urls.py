from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('about/', views.about, name='about'),
    path('populares/', views.popular_posts, name='popular_posts'),
    path('post/nuevo/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
