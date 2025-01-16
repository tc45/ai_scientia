from django.urls import path
from . import views

app_name = 'demos'

urlpatterns = [
	path('', views.index, name='index'),
	path('filter/', views.demo_filter, name='demo_filter'),
	path('<slug:slug>/', views.demo_detail, name='demo_detail'),
	path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]