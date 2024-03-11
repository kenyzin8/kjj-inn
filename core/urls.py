from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', views.login, name='index'),
   path('dashboard/', views.dashboard, name='admin-dashboard'),
   path('login/', views.login, name='login'),
   path('logout/', views.logout_user, name='logout-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)