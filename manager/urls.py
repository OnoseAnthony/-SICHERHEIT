from django.urls import path
from manager import views


#Template Tagging
app_name = 'manager'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/logout/', views.user_logout, name='user_logout'),

    path('passwords-list/', views.PasswordsListView.as_view(), name='password_change_list'),
    path('create-password/', views.PasswordCreateView.as_view(), name='password_add'),
    path('password/<int:pk>/', views.PasswordUpdateView.as_view(), name='password_change'),
    path('password/<int:pk>/delete/', views.PasswordDeleteView.as_view(), name='password_delete'),

]
