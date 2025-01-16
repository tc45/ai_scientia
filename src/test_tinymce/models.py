from django.db import models
from ckeditor.fields import RichTextField

class TinyMCEContent(models.Model):
    """
    Model to store content created using TinyMCE editor.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "TinyMCE Content"
        verbose_name_plural = "TinyMCE Contents"

class CKEditorContent(models.Model):
    """
    Model to store content created using CKEditor.
    """
    title = models.CharField(max_length=200)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "CKEditor Content"
        verbose_name_plural = "CKEditor Contents"