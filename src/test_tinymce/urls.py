from django.urls import path
from . import views

urlpatterns = [
	path('', views.landing_page, name='landing_page'),
	path('editor/', views.tinymce_editor, name='tinymce_editor'),
	path('editor/<int:pk>/', views.tinymce_editor, name='tinymce_edit'),
	path('success/', views.tinymce_success, name='tinymce_success'),
	path('ckeditor/', views.ckeditor_editor, name='ckeditor_editor'),
	path('ckeditor/<int:pk>/', views.ckeditor_editor, name='ckeditor_edit'),
	path('ckeditor/success/', views.ckeditor_success, name='ckeditor_success'),
]