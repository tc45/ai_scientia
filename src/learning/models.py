from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from .constants import ICON_CHOICES
from django.utils.safestring import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", default="fas fa-book")
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def icon_display(self):
        return mark_safe(f'<i class="{self.icon}"></i> {self.name}')
    icon_display.short_description = 'Name'

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(help_text="A brief summary of the tutorial", blank=True, null=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='tutorials/thumbnails/', null=True, blank=True)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tutorials'
    )
    is_featured = models.BooleanField(default=False)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    estimated_time = models.CharField(
        max_length=50, 
        help_text="e.g., '2 hours', '30 minutes'",
        blank=True,
        null=True,
        default='1 hour'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    icon = models.CharField(
        max_length=50, 
        choices=ICON_CHOICES,
        help_text="FontAwesome icon class",
        default="fas fa-book"
    )
    
    class Meta:
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('learning:tutorial_detail', args=[self.slug]) 

    def can_edit(self, user):
        return user.is_superuser or user == self.author

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if Tutorial.objects.filter(slug=base_slug).exists():
                base_slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            self.slug = base_slug
        super().save(*args, **kwargs)

class UserProgress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)
    progress_percent = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'tutorial'] 