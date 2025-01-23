from django.contrib.auth.models import User
from django.db import models


class Articles(models.Model):
    # заголовок статьи, может быть пустым и пустой по умолчанию
    title = models.TextField(blank=True, default='')
    # ссылка на изображение
    imgURL = models.URLField(blank=True, default='')
    # текст статьи
    body = models.TextField(blank=True, default='')
    # привязка статьи к пользователю
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # В class Meta мы указываем имя таблицы в БД для данной модели.
    class Meta:
        db_table = 'articles'