from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkin_list, name='checkin_list'),
    path('new/', views.checkin_create, name='checkin_create'),
    path('<int:pk>/edit/', views.checkin_edit, name='checkin_edit'),
    path('<int:pk>/delete/', views.checkin_delete, name='checkin_delete'),
]
