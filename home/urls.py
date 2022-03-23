from django.contrib import admin
from django.urls import path 
from home import views

urlpatterns = [
    path('', views.index, name='home'),

    path('about/', views.about, name='about'),
    path('uploads/',views.send_files, name="uploads"),
    path('payment/', views.payment, name="payment"),
    path('singup', views.handleSignup, name="handleSignup"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('order', views.handelOrder, name="handelOrder")
    
    
]
