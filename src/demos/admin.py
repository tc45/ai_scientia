from django.contrib import admin
from django import forms
from .models import Demo, DemoCategory, SubCategory, SampleFormModel, Tag
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect

class DemoCategoryForm(forms.ModelForm):
	class Meta:
		model = DemoCategory
		fields = ('name', 'slug', 'description', 'icon', 'order')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class SubCategoryInline(admin.TabularInline):
	model = SubCategory
	extra = 0
	show_change_link = False
	fields = ('sub_category_display', 'actions')
	readonly_fields = ('sub_category_display', 'actions')

	def sub_category_display(self, obj):
		return obj.name
	sub_category_display.short_description = 'Sub-Category'

	def actions(self, obj):
		edit_url = reverse('admin:demos_subcategory_change', args=[obj.id])
		delete_url = reverse('admin:demos_subcategory_delete', args=[obj.id])
		return format_html(
			'<a class="button" href="{}">Edit</a> <a class="button" href="{}">Delete</a>',
			edit_url, delete_url
		)
	actions.short_description = 'Actions'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(parent_category__isnull=False)

	def get_formset(self, request, obj=None, **kwargs):
		formset = super().get_formset(request, obj, **kwargs)
		if 'name' in formset.form.base_fields:
			formset.form.base_fields['name'].widget.attrs['style'] = 'width: 200px;'
		return formset

@admin.register(DemoCategory)
class DemoCategoryAdmin(admin.ModelAdmin):
	form = DemoCategoryForm
	list_display = ('icon_with_name', 'slug', 'order')
	prepopulated_fields = {'slug': ('name',)}
	search_fields = ('name',)
	ordering = ['order', 'name']
	fields = ('name', 'slug', 'description', 'icon', 'order')
	inlines = [SubCategoryInline]

	def icon_with_name(self, obj):
		return mark_safe(f'<i class="{obj.icon}"></i> {obj.name}')
	icon_with_name.short_description = 'Name'
	icon_with_name.admin_order_field = 'name'
	icon_with_name.allow_tags = True

	def response_add(self, request, obj, post_url_continue=None):
		if "_addanother" in request.POST:
			return HttpResponseRedirect(reverse('admin:demos_subcategory_add') + f'?parent_category={obj.id}')
		return super().response_add(request, obj, post_url_continue)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'parent_category')
	search_fields = ('name',)
	ordering = ['name']

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
	list_display = ('title', 'get_category_breadcrumbs', 'author', 'difficulty_level', 'is_featured', 'is_published', 'use_cases')
	list_filter = ('is_published', 'is_featured', 'category', 'difficulty_level', 'created_on', 'use_cases')
	search_fields = ('title', 'content', 'summary', 'tags')
	prepopulated_fields = {'slug': ('title',)}
	date_hierarchy = 'created_on'
	list_editable = ['is_featured', 'is_published']
	autocomplete_fields = ['author']

	def get_category_breadcrumbs(self, obj):
		if isinstance(obj.category, SubCategory):
			return obj.category.get_category_tree()
		return obj.category.name
	get_category_breadcrumbs.short_description = 'Category'

class SampleFormModelForm(forms.ModelForm):
	multi_line_choice_field = forms.MultipleChoiceField(
		choices=[
			('line1', 'Line 1'),
			('line2', 'Line 2'),
			('line3', 'Line 3'),
		],
		widget=forms.CheckboxSelectMultiple,
		help_text="Select from multiple lines"
	)

	class Meta:
		model = SampleFormModel
		fields = '__all__'

@admin.register(SampleFormModel)
class SampleFormModelAdmin(admin.ModelAdmin):
	form = SampleFormModelForm
	list_display = ('id', 'char_field', 'choice_field', 'date_field', 'datetime_field', 'decimal_field', 'email_field', 'float_field', 'integer_field', 'slug_field', 'url_field', 'boolean_field', 'null_boolean_field', 'time_field', 'duration_field', 'file_field', 'image_field', 'positive_integer_field', 'positive_small_integer_field', 'small_integer_field', 'big_integer_field', 'generic_ip_address_field', 'uuid_field')
	search_fields = ('char_field', 'email_field', 'url_field')
	ordering = ['id']
	fields = ('char_field', 'choice_field', 'date_field', 'datetime_field', 'decimal_field', 'email_field', 'float_field', 'integer_field', 'slug_field', 'text_field', 'url_field', 'boolean_field', 'null_boolean_field', 'time_field', 'duration_field', 'file_field', 'image_field', 'positive_integer_field', 'positive_small_integer_field', 'small_integer_field', 'big_integer_field', 'generic_ip_address_field', 'uuid_field', 'multi_line_text_field', 'multi_line_choice_field', 'tags')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
