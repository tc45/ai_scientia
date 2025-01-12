from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    excerpt = models.TextField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(0, "Draft"), (1, "Published")], default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    featured = models.BooleanField(default=False, help_text="Select to display this post in the featured section")
    
    class Meta:
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['-created_on']),
            models.Index(fields=['status', '-created_on']),
            models.Index(fields=['featured', '-created_on']),
        ]
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
        
    def number_of_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_on']
        
    def __str__(self):
        return f'Comment {self.body} by {self.name}' 