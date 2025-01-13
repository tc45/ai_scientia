from django.contrib import admin
from django.db import models
from django.contrib.auth import get_user_model
from .models import Tutorial, Category, UserProgress
from .widgets import IconSelectWidget
from django.utils.safestring import mark_safe


class LearningAdminBase(admin.ModelAdmin):
    """
    Base admin class for learning models to centralize static files
    """
    class Media:
        css = {
            'all': (
                'admin/css/vendor/select2/select2.min.css',
                'admin/css/autocomplete.css',
                'css/icon-select.css',
            )
        }
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/vendor/select2/select2.full.min.js',
            'js/icon-select.js',
        )

@admin.register(Tutorial)
class TutorialAdmin(LearningAdminBase):
    list_display = ('title', 'category', 'author', 'difficulty_level', 'is_featured', 'is_published')
    list_filter = ('is_published', 'is_featured', 'category', 'difficulty_level', 'created_on')
    search_fields = ('title', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    list_editable = ['is_featured', 'is_published']
    autocomplete_fields = ['author']
    filter_horizontal = ['prerequisites']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'icon':
            kwargs['widget'] = IconSelectWidget()
        elif db_field.name == 'author':
            kwargs['queryset'] = get_user_model().objects.filter(is_staff=True)
        elif db_field.name == 'prerequisites':
            kwargs['queryset'] = Tutorial.objects.filter(is_published=True).exclude(id=kwargs.get('obj', None).id if kwargs.get('obj') else None)
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(Category)
class CategoryAdmin(LearningAdminBase):
    list_display = ('icon_with_name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ['order', 'name']

    def icon_with_name(self, obj):
        return mark_safe(f'<i class="{obj.icon}"></i> {obj.name}')
    icon_with_name.short_description = 'Name'
    icon_with_name.admin_order_field = 'name'
    icon_with_name.allow_tags = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'icon':
            kwargs['widget'] = IconSelectWidget()
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(UserProgress)
class UserProgressAdmin(LearningAdminBase):
    list_display = ('user', 'tutorial', 'completed', 'last_accessed')
    list_filter = ('completed', 'last_accessed')
    search_fields = ('user__username', 'tutorial__title')
    raw_id_fields = ['user', 'tutorial'] 