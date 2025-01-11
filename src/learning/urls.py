from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.index, name='index'),
    path('tutorial/<slug:slug>/', views.TutorialDetailView.as_view(), name='tutorial_detail'),
] 