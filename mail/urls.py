from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('uploadjson/', views.uploadfiles, name='uploadfile'),
    path('extractor/', views.EmailExtractor, name='EmailExtractor'),
    path('sendmail/', views.sendmail, name='sendmail'),
    path('about/', views.About, name='about'),
]
