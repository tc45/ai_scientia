from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from .models import Post

class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(status=1).order_by('-likes')[:3]
        
        # Archive data
        context['dates'] = Post.objects.filter(status=1).dates('created_on', 'month', order='DESC')
        
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' 