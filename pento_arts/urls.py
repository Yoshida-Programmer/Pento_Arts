from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.models import Group

admin.site.site_title = '管理サイト（管理者用）'
admin.site.site_header = '管理サイト（管理者用）'
admin.site.index_title = 'メニュー'

app_name = 'pento_app'

urlpatterns = [
    path('staff-admin/', admin.site.urls),
    path('', include("pento_app.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/email/', RedirectView.as_view(pattern_name='pento_app:index')),
    path('accounts/inactive/', RedirectView.as_view(pattern_name='pento_app:index')),
    path('accounts/password/change/', RedirectView.as_view(pattern_name='pento_app:index')),
    path('accounts/confirm-email/', RedirectView.as_view(pattern_name='pento_app:index')),
    re_path(r'^accounts/confirm-email/[^/]+/', RedirectView.as_view(pattern_name='pento_app:index'), kwargs=None),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
