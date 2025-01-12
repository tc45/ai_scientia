from django import forms
from .models import Tutorial
from .widgets import IconSelectWidget

class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = [
            'title', 'category', 'subtitle', 'summary', 
            'content', 'thumbnail', 'difficulty_level',
            'estimated_time', 'is_published', 'is_featured',
            'prerequisites', 'icon'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 20}),
            'summary': forms.Textarea(attrs={'rows': 3}),
            'prerequisites': forms.SelectMultiple(attrs={'class': 'select2'}),
            'icon': IconSelectWidget()
        } 