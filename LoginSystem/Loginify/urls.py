from . import views
from django.urls import path


urlpatterns = [path('hello/', views.hello, name="hello"),
               path('signup/', views.signup, name="signup"),
               path('login/', views.login, name="login"),
               path('users/', views.get_all_users, name='get_all_users'),
               path('users/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
               path('users/update/<str:email>/', views.update_user, name='update_user'),
               path('users/delete/<str:email>/', views.delete_user, name='delete_user'),
               path('createPostman/', views.create_user_postman, name="create_user_postman")]
