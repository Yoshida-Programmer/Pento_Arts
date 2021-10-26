from django.contrib import admin
from .models import CustomUser,Connection
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin import AdminSite
from . import models

#マイページ表示
class MyAdminSite(AdminSite):
    site_header = 'マイページ'
    site_title = 'マイページ'
    index_title = 'ホーム'
    site_url = None
    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active

mypage_site = MyAdminSite(name="mypage")

admin.site.register(CustomUser)
admin.site.register(Connection)



