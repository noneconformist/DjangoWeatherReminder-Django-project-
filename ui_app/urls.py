from django.urls import path

from . import views

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions list'),
    path('add/', views.subscription_add, name='subscription_add'),
    path('delete/', views.subscription_delete, name='subscription_delete'),
]
