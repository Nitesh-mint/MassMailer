from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('uploadjson/', views.uploadfiles, name='uploadfile'),
    path('about/', views.About, name='about'),
    path('sendmail/', views.sendmail, name='sendmail'),
]
