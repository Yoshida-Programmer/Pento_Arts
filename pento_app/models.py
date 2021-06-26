from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.utils import timezone
from django.urls import reverse

#ユーザーモデル（公開ユーザー情報用にカスタマイズ）
class CustomUser(AbstractUser):
    description = models.TextField(verbose_name='プロフィール', null=True, blank=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True, upload_to='images/')
    thumbnail = ImageSpecField(source='photo', processors=[ResizeToFill(256,256)], format='JPEG', options={'quality': 60})
    email = models.EmailField('メールアドレス', unique = True)

    def get_absolute_url(self):
        return reverse('pento_app:detail', kwargs={'username': self.username})

    class Meta:
        verbose_name_plural = 'CustomUser'

#タイムラインモデル
class Post(models.Model):
    author = models.ForeignKey('pento_app.CustomUser', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='本文')
    photo = models.ImageField(verbose_name='写真', blank=True, null=True, upload_to='images/')
    post_photo = ImageSpecField(source='photo', processors=[ResizeToFit(1080,1080)], format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def get_like(self):
        likes = Like.objects.filter(post=self)
        return [like.user for like in likes]

#『いいね』モデル
class Like(models.Model):
    user = models.ForeignKey('pento_app.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    #ユーザーが重複して『いいね』を押せないよう設定する
    class Meta:
        unique_together = ('user', 'post')

#フォローモデル
class Connection(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)
