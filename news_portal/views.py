# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post, Comment


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'create_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'
    queryset = Post.objects.filter(author__user__username='SaitBakh')



class PostDetail(DetailView): # детальная информация конкретного поста
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'

class CommListView(ListView):
    model = Comment
    template_name = 'flatpages/post.html'
    context_object_name = 'comment'


