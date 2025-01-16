from django.shortcuts import render, get_object_or_404, redirect
from .models import TinyMCEContent, CKEditorContent
from .forms import TinyMCEContentForm, CKEditorContentForm

def tinymce_editor(request, pk=None):
    """
    View for creating and editing content using TinyMCE editor.
    """
    instance = None
    if pk:
        instance = get_object_or_404(TinyMCEContent, pk=pk)
    
    if request.method == 'POST':
        form = TinyMCEContentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('tinymce_success')
    else:
        form = TinyMCEContentForm(instance=instance)
    
    return render(request, 'test_tinymce/editor.html', {'form': form})

def tinymce_success(request):
    """
    Success page after content submission.
    """
    return render(request, 'test_tinymce/success.html')

def ckeditor_editor(request, pk=None):
    """
    View for creating and editing content using CKEditor.
    """
    instance = None
    if pk:
        instance = get_object_or_404(CKEditorContent, pk=pk)
    
    if request.method == 'POST':
        form = CKEditorContentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('ckeditor_success')
    else:
        form = CKEditorContentForm(instance=instance)
    
    return render(request, 'test_tinymce/ckeditor_editor.html', {'form': form})

def ckeditor_success(request):
    """
    Success page after CKEditor content submission.
    """
    return render(request, 'test_tinymce/ckeditor_success.html')

def landing_page(request):
	"""
	View for the landing page with links to TinyMCE and CKEditor.
	"""
	return render(request, 'test_tinymce/landing_page.html')