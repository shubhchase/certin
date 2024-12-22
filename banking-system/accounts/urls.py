from django.conf import settings
from django.urls import include, path

from .views import UserRegistrationView, LogoutView, UserLoginView
from . import views

from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),
    # path('captcha/', include('captcha.urls')),
    path('update-email/', views.update_email, name='update_email'),
    path('update-password/', views.update_password, name='update_password'),
    path('delete-account/<int:user_id>/', views.delete_account, name='delete_account'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)