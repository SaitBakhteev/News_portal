from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    raiting=models.IntegerField(default=0)

    def update_rating(self): #обновление рейтинга автора по трем критериям

        # Расчет рейтинга постов автора
        _raiting=Post.objects.filter(author_id=self.id).values('raiting')
        post_raiting=0
        for pst in _raiting:
            post_raiting +=pst['raiting']
        post_raiting *=3 # утроенное значение суммы рейтингов постов

        # Расчет рейтинга комментов автора
        _raiting = Comment.objects.filter(user_id=self.user.id).values('raiting')
        comm_raiting=0
        for cmt in _raiting:
            comm_raiting +=cmt['raiting']

        # Расчет суммы рейтингов комментов к статьям автора
        _raiting = Comment.objects.filter(post__author=self).values('raiting')
        comm_posts_raiting=0
        for cmt_pst in _raiting:
            comm_posts_raiting +=cmt_pst['raiting']

        self.raiting=post_raiting+comm_raiting+comm_posts_raiting
        self.save()

class Category(models.Model):
    category=models.CharField(max_length=100, unique=True) # тематика поста



class Post(models.Model):
    news = 'NS'
    article = 'AL'
    post_type = [(news, 'Новости'),  # список названий типа поста
                 (article, 'Статья')]

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    postType = models.CharField(choices=post_type, default=news, max_length=2) # тип поста (новость/статья)
    create_time = models.DateTimeField(auto_now_add=True)  # дата добавления поста
    category=models.ManyToManyField(Category, through='PostCategory')
    title=models.CharField(max_length=100) #заголовок поста
    content=models.TextField(blank=True) # содержание поста
    raiting=models.IntegerField(default=0) # рейтинг поста

    def __str__(self):
        return f'{self.title}, {self.author.user.username}'

    # Увеличение и уменьшение рейтинга поста
    def like(self):
        self.raiting += 1
        self.save()
    def dislike(self):
        self.raiting -= 1
        self.save()

    def preview(self): # предварительный просмотр статьи
        return f'{self.content[:124:]}......'

class PostCategory(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_text=models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    raiting=models.IntegerField(default=0)

    # Увеличение и уменьшение рейтинга комментариев
    def like(self):
        self.raiting += 1
        self.save()
    def dislike(self):
        self.raiting -= 1
        self.save()


# Create your models here.
