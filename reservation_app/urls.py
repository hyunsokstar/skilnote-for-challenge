from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('accounts2.urls')),
    path('accounts/', include('allauth.urls')),
    # path('logout/', auth_views.LogoutView, name = 'logout', kwargs = {'next_page' : settings.LOGIN_URL}),
    # re_path(r'^logout/$', auth_views.LogoutView, name = 'logout', kwargs = {'next_page' : settings.LOGIN_URL}),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('blog/', include('blog.urls')),
    path('', include('remote_control.urls')),
    path('todo/', include('todo.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('bestlec/', include('bestlec.urls')),
    path('management/', include('management.urls')),
    path('challenge/', include('challenge.urls')),
    path('board/', include('board.urls')),
    path('pd/', include('pd.urls')),
    path('skilblog/', include('skilblog.urls')),
    path('wm/', include('wm.urls')),
    path('skilnote2/', include('skilnote2.urls')),
    path('skilnote3/', include('skilnote3.urls')),
    path('skilnote4/', include('skilnote4.urls')),
]

if settings.DEBUG:
   urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   import debug_toolbar
   urlpatterns += [
      path ('__debug__/', include (debug_toolbar.urls)),
   ]
