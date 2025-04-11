from django.urls import path
from .views import register, profile, update_form_user, address_form, map_view, search_users, user_profile, photo
from django.contrib.auth import views as auth_view
from django.urls import path
from .views import nearby_users, address_form

urlpatterns = [
    # registro e login
    path('Cadastro/', register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('users/profile/<int:user_id>/', user_profile, name='user-profile'),

    # Perfis
    path('profile/', profile, name='profile'),  # Perfil do usuário logado
    path('profile/<int:user_id>/', profile, name='user-profile'),
    
    # Outras rotas
    path('update/', update_form_user, name='update_form'),
    path('update/foto/', photo, name='update_form_photo'),
    path('meu-endereco/', address_form, name='user-address'),
    path('mapa/', map_view, name='map-page'),
    path('api/nearby-users/', nearby_users, name='nearby-users'),
    path('api/search-users/', search_users, name='search-users'),
    # recuperar senha
    path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
