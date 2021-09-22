from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre-nos/', views.about, name='about'),
    path('contato/', views.contato, name='contato'),
    path('cadastro/', views.cadastro, name='cadastro'),
]
