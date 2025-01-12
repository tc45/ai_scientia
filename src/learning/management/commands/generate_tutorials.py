from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from learning.models import Tutorial, Category
from utils.openai_utils import OpenAIContentGenerator
import random

class Command(BaseCommand):
    help = 'Generate sample tutorials using OpenAI'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin_user = User.objects.filter(is_superuser=True).first()
        
        if not admin_user:
            self.stdout.write(self.style.ERROR('No admin user found'))
            return
            
        # Ensure we have basic categories
        categories = {
            'Getting Started': 'Basic concepts and fundamentals',
            'Machine Learning': 'Core machine learning concepts and applications',
            'Deep Learning': 'Neural networks and deep learning architectures',
            'Natural Language Processing': 'Text processing and language models',
            'Computer Vision': 'Image processing and visual AI',
            'Reinforcement Learning': 'Learning through interaction and rewards'
        }
        
        for name, desc in categories.items():
            Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'icon': 'fas fa-brain'
                }
            )
            
        generator = OpenAIContentGenerator()
        difficulty_levels = ['beginner', 'intermediate', 'advanced']
        
        tutorial_topics = [
            "Introduction to AI",
            "Python for Machine Learning",
            "Neural Networks Basics",
            "Natural Language Processing",
            "Computer Vision Fundamentals",
            "Deep Learning Architecture",
            "Reinforcement Learning",
            "AI Ethics",
            "Data Preprocessing",
            "Model Evaluation",
            "Transfer Learning",
            "GANs and Creative AI",
            "AI in Healthcare",
            "AI for Business",
            "Edge AI Computing",
            "AI Security",
            "AutoML",
            "AI Project Management",
            "MLOps Basics",
            "AI Research Methods"
        ]
        
        for topic in tutorial_topics:
            difficulty = random.choice(difficulty_levels)
            category = Category.objects.order_by('?').first()
            
            self.stdout.write(f"Generating tutorial for: {topic}")
            
            content = generator.generate_blog_post(
                title=topic,
                topic=f"{topic} for {difficulty} level students"
            )
            
            if content['content']:
                try:
                    tutorial = Tutorial.objects.create(
                        title=topic,
                        category=category,
                        content=content['content'],
                        summary=content['excerpt'],
                        difficulty_level=difficulty,
                        estimated_time=f"{random.randint(1, 4)} hours",
                        is_published=True,
                        author=admin_user
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created tutorial: {topic}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create tutorial {topic}: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to generate content for: {topic}')) 