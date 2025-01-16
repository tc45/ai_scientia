from django import forms
from .models import TinyMCEContent, CKEditorContent

class TinyMCEContentForm(forms.ModelForm):
    """
    Form for creating and editing TinyMCE content.
    """
    class Meta:
        model = TinyMCEContent
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'tinymce-editor'}),
        }

class CKEditorContentForm(forms.ModelForm):
    """
    Form for creating and editing CKEditor content.
    """
    class Meta:
        model = CKEditorContent
        fields = ['title', 'content']