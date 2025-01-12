from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.urls import reverse_lazy
from .models import Tutorial, Category, UserProgress
from .forms import TutorialForm

def index(request):
    categories = Category.objects.annotate(tutorial_count=Count('tutorial'))
    
    featured_tutorials = Tutorial.objects.filter(
        is_published=True,
        is_featured=True
    ).select_related('category', 'author')[:3]
    
    tutorials = Tutorial.objects.filter(
        is_published=True
    ).select_related('category', 'author')
    
    if request.user.is_authenticated:
        for tutorial in tutorials:
            tutorial.can_edit = tutorial.can_edit(request.user)
        for tutorial in featured_tutorials:
            tutorial.can_edit = tutorial.can_edit(request.user)
            tutorial.user_progress = UserProgress.objects.filter(
                user=request.user,
                tutorial=tutorial
            ).first()
    
    difficulty_levels = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    
    context = {
        'categories': categories,
        'featured_tutorials': featured_tutorials,
        'tutorials': tutorials,
        'difficulty_levels': difficulty_levels,
    }
    return render(request, 'learning/index.html', context)

class TutorialDetailView(DetailView):
    model = Tutorial
    template_name = 'learning/tutorial_detail.html'
    context_object_name = 'tutorial' 

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'learning/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tutorials'] = Tutorial.objects.filter(
            category=self.object,
            is_published=True
        ).select_related('category')
        return context 

class TutorialEditView(LoginRequiredMixin, UpdateView):
    model = Tutorial
    form_class = TutorialForm
    template_name = 'learning/tutorial_edit.html'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.can_edit(request.user):
            return HttpResponseForbidden("You don't have permission to edit this tutorial")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.object.get_absolute_url()

def tutorial_filter(request):
    """
    Filter tutorials based on difficulty levels, categories, and search query.
    """
    difficulties = request.GET.getlist('difficulties[]', [])
    categories = request.GET.getlist('categories[]', [])
    search = request.GET.get('search', '').strip()
    
    tutorials = Tutorial.objects.filter(
        is_published=True
    ).select_related('category', 'author')
    
    # Apply difficulty filter
    if difficulties and 'all' not in difficulties:
        tutorials = tutorials.filter(difficulty_level__in=difficulties)
    
    # Apply category filter
    if categories:
        tutorials = tutorials.filter(category__slug__in=categories)
    
    # Apply search filter
    if search:
        tutorials = tutorials.filter(
            Q(title__icontains=search) |
            Q(summary__icontains=search) |
            Q(content__icontains=search)
        )
    
    # Add can_edit flag for authenticated users
    if request.user.is_authenticated:
        for tutorial in tutorials:
            tutorial.can_edit = tutorial.can_edit(request.user)
    
    context = {
        'tutorials': tutorials,
    }
    return render(request, 'learning/partials/tutorial_list.html', context)

def tutorial_search(request):
    query = request.GET.get('q', '')
    tutorials = Tutorial.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(content__icontains=query),
        is_published=True
    ).select_related('category', 'author')

    if request.user.is_authenticated:
        for tutorial in tutorials:
            tutorial.can_edit = tutorial.can_edit(request.user)

    context = {'tutorials': tutorials}
    return render(request, 'learning/partials/tutorial_list.html', context) 