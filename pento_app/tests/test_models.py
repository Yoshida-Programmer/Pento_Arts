from django.http import response
from django.test import TestCase, Client, client
from django.contrib.auth import get_user_model
from django.urls.base import reverse_lazy
from ..models import CustomUser, Post


class TimeLineTestCase(TestCase):

    """未ログイン時のステータスコード『302』"""
    def test_index(self):
       client = Client()
       response = client.get('/')
       self.assertEqual(response.status_code, 302)

    """テストユーザー生成"""
    def test_loggedin_index(self):
        client = Client()
        self.test_user = get_user_model().objects.create_user(
            username = 'test0',
            email = 'test0@example.com',
            password = 'password' )

        #ログイン時のステータスコード『200』
        client.login(email = 'test0@example.com',password = 'password')   
        response = client.get('/')
        self.assertEqual(response.status_code, 200) 

        #最新の投稿を取得し、テストユーザーの投稿であることをチェック
        client.post('/create/', {'text':'テスト投稿', 'photo':''})
        latest_post = Post.objects.latest('created_at')
        self.assertEqual(latest_post.text, 'テスト投稿')