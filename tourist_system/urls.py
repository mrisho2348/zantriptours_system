from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.views.i18n import set_language
from tourist_system import settings
from tourOrderingApp.views import logout_user
admin.site.logout = logout_user
from django.views.static import serve

urlpatterns = [
    path('', include('tourOrderingApp.urls')),
    path('Hod/', include('tourist_system.admin_urls')),
    path('Tourist/', include('tourist_system.tourist_urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    re_path(r'^admin/', include('admin_honeypot.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('tourist_system/', admin.site.urls),
    path('i18n/', set_language, name='set_language'),  # Add language switcher URL pattern
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': settings.DEBUG,
    }),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    
admin.site.login = 'custom_login'
admin.site.index_title = "Zan Trip & Tours"
admin.site.site_header = "Zan Trip & Tours"
admin.site.site_title = "Zan Trip & Tours"        
