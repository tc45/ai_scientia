from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.dates import MonthArchiveView
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from .models import Post, Comment
from datetime import datetime
from django.contrib import messages

class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get featured posts first, if not enough, get most liked posts
        featured_posts = list(Post.objects.filter(status=1, featured=True)[:3])
        if len(featured_posts) < 3:
            additional_posts = list(Post.objects.filter(
                status=1, 
                featured=False
            ).order_by('-likes')[:3-len(featured_posts)])
            featured_posts.extend(additional_posts)
        
        context['featured_posts'] = featured_posts
        
        # Archive data - group by year and month
        posts_by_date = Post.objects.filter(status=1).dates('created_on', 'month', order='DESC')
        archive_dates = []
        for date in posts_by_date:
            archive_dates.append({
                'year': date.year,
                'month': date.strftime('%m'),
                'month_name': date.strftime('%B')
            })
        context['archive_dates'] = archive_dates
        
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(
            status=1
        ).exclude(
            id=self.object.id
        ).order_by('-created_on')[:5]
        return context

class PostArchiveView(MonthArchiveView):
    queryset = Post.objects.filter(status=1)
    date_field = "created_on"
    allow_future = False
    month_format = '%m'
    template_name = 'blog/post_archive.html' 

def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        try:
            comment = Comment.objects.create(
                post=post,
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                body=request.POST.get('body'),
                active=True  # You might want to set this to False if you want to moderate comments
            )
            messages.success(request, 'Your comment has been added successfully!')
        except Exception as e:
            messages.error(request, 'There was an error posting your comment. Please try again.')
    
    return redirect('blog:post_detail', slug=slug) 