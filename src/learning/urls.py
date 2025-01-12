from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.index, name='index'),
    path('tutorial/<slug:slug>/', views.TutorialDetailView.as_view(), name='tutorial_detail'),
    path('tutorial/<slug:slug>/edit/', views.TutorialEditView.as_view(), name='tutorial_edit'),
    path('filter/', views.tutorial_filter, name='tutorial_filter'),
    path('search/', views.tutorial_search, name='tutorial_search'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
] 