from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    url(r'^$',views.login,name='login'),
    url('logout/', views.logout, name='logout'),
    url('redirecting/', views.redirecting, name='redirecting'),

]