from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('archive/<int:year>/<str:month>/', views.PostArchiveView.as_view(), name='archive'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
] 