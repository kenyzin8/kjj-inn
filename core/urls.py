from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('', views.login_user, name='index'),
   path('dashboard/', views.dashboard, name='admin-dashboard'),
   path('login/', views.login_user, name='login'),
   path('logout/', views.logout_user, name='logout-page'),
   path('user-management/', views.user_management, name='user-management'),
   path('user-management/add-user/', views.add_user, name='add-user'),
   path('user-management/update-user/', views.update_user, name='update-user'),
   path('user-management/delete-user/', views.delete_user, name='delete-user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)