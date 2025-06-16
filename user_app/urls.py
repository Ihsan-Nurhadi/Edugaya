from django.urls import path
from user_app import views
app_name = 'user_app'
urlpatterns = [
    path('',views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('student', views.student, name='student'),
    path('teacher', views.teacher, name='teacher'),
    path('dashboard', views.teacherdashboard, name='dashboard'),
]
