from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('space/<slug:slug>/', views.space_detail_view, name='space_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('demo-login/<str:role>/', views.demo_login_view, name='demo_login'),
    path('logout/', views.logout_view, name='logout'),
]
