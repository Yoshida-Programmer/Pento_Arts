from __future__ import absolute_import
from django.conf import settings

from django.core.checks import messages
from django.contrib import messages
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.messages.views import SuccessMessageMixin

from .models import CustomUser, Post, Like, Connection
from .forms import ProfileForm, PostForm
from .helpers import get_current_user

User = get_user_model()

"""プロフィール編集ページ"""
class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'edit.html'
    success_url = 'edit'
    success_message = 'プロフィールを更新しました。'

    def get_object(self):
        return self.request.user

"""プロフィール画面"""
class ProifileDetail(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'detail.html'

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProifileDetail, self).get_context_data(**kwargs)
        username = self.kwargs['username']
        context['username'] = username
        context['user'] = get_current_user(self.request)
        context['following'] = Connection.objects.filter(follower__username=username).count()
        context['follower'] = Connection.objects.filter(following__username=username).count()

        if username is not context['user'].username:
            result = Connection.objects.filter(follower__username=context['user'].username).filter(following__username=username)
            context['connected'] = True if result else False

        return context

"""フォロー"""
@login_required
def follow_view(request, *args, **kwargs):

    try:
        follower = CustomUser.objects.get(username=request.user.username)
        following = CustomUser.objects.get(username=kwargs['username'])
    except CustomUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('pento_app:index'))

    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
    else:
        _, created = Connection.objects.get_or_create(follower=follower, following=following)

        if (created):
            messages.success(request, '{}をフォローしました'.format(following.username))
        else:
            messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('pento_app:detail', kwargs={'username': following.username}))

"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):
    
    try:
        follower = CustomUser.objects.get(username=request.user.username)
        following = CustomUser.objects.get(username=kwargs['username'])
        if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(following.username))
    except CustomUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('pento_app:index'))
    except Connection.DoesNotExist:
        messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('pento_app:detail', kwargs={'username': following.username}))

"""インデックス（全ユーザー表示）"""
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        return posts

"""タイムライン表示"""
class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    success_url = reverse_lazy('pento_app:index')

    #投稿成功時の処理
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました。')
        return super(CreateView, self).form_valid(form)

    #投稿失敗時の処理
    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました。')
        return redirect('pento_app:timeline')

"""投稿削除"""
class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('pento_app:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            messages.success(self.request, '削除しました。')
            return super().delete(request, *args, **kwargs)

"""『いいね』機能"""
class LikeView(LoginRequiredMixin, generic.View):
    model = Like

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        like = Like(user=self.request.user,post=post)
        like.save()
        like_count = Like.objects.filter(post=post).count()
        data = {'message': '『いいね』しました',
                'like_count': like_count}
        return JsonResponse(data)

"""他ユーザーからのアクセスを制限"""
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser

"""退会機能"""
class UserDeleteView(OnlyYouMixin, generic.DeleteView):
    template_name = "delete.html"
    success_url = reverse_lazy("account_login")
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'

"""ユーザー詳細設定"""
class SettingListView(TemplateView):
    template_name = "settings.html"



edit = ProfileEdit.as_view()
detail = ProifileDetail.as_view()
index = IndexView.as_view()
create = CreateView.as_view()
delete = DeleteView.as_view()
settings = SettingListView.as_view()
userdelete = UserDeleteView.as_view()
like = LikeView.as_view()





