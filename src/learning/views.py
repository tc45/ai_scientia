from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Tutorial, Category

def index(request):
    categories = Category.objects.all()
    getting_started = Tutorial.objects.filter(category__name='Getting Started', is_published=True)[:5]
    knowledge_base = Tutorial.objects.filter(category__name='Knowledge Base', is_published=True)[:5]
    demos = Tutorial.objects.filter(category__name='Demos', is_published=True)[:5]
    
    context = {
        'categories': categories,
        'getting_started': getting_started,
        'knowledge_base': knowledge_base,
        'demos': demos,
    }
    return render(request, 'learning/index.html', context)

class TutorialDetailView(DetailView):
    model = Tutorial
    template_name = 'learning/tutorial_detail.html'
    context_object_name = 'tutorial' 