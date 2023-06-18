from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signup/verify/<str:code>',views.activate_by_email,name="activate_email"),
    path('signout/', views.signout,name="signout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add/', views.add_work, name='add'),
    path('dashboard/del/<int:id>/', views.del_work, name='del_work'),
    path('dashboard/all', views.apply_filter, name='show_all'),
]
