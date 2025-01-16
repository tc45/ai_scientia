from django.shortcuts import render, get_object_or_404
from .models import Demo, DemoCategory, SubCategory
from django.http import JsonResponse
from django.db.models import Q

def index(request):
	"""
	Render the index page for the demos app.

	Args:
		request: The HTTP request object.

	Returns:
		HttpResponse: The rendered index page.
	"""
	categories = DemoCategory.objects.all()
	subcategories = SubCategory.objects.select_related('parent_category').all()
	featured_demos = Demo.objects.filter(is_featured=True)[:3]
	demos = Demo.objects.all()

	# Ensure the user has the permission to edit demos
	can_edit_demos = request.user.is_authenticated and request.user.has_perm('demos.change_demo')

	context = {
		'categories': categories,
		'subcategories': subcategories,
		'featured_demos': featured_demos,
		'demos': demos,
		'difficulty_levels': [
			('beginner', 'Beginner'),
			('intermediate', 'Intermediate'),
			('advanced', 'Advanced')
		],
		'use_cases': [
			('business', 'Business'),
			('technical', 'Technical'),
			('educational', 'Educational')
		],
		'can_edit_demos': can_edit_demos,
	}
	return render(request, 'demos/index.html', context)

def demo_filter(request):
	"""
	Filter demos based on difficulty levels, categories, and search query.
	"""
	difficulties = request.GET.getlist('difficulties[]', [])
	categories = request.GET.getlist('categories[]', [])
	search = request.GET.get('search', '').strip()
	
	demos = Demo.objects.filter(is_published=True).select_related('category', 'author')
	
	# Apply difficulty filter
	if difficulties and 'all' not in difficulties:
		demos = demos.filter(difficulty_level__in=difficulties)
	
	# Apply category filter
	if categories:
		demos = demos.filter(category__slug__in=categories)
	
	# Apply search filter
	if search:
		demos = demos.filter(
			Q(title__icontains=search) |
			Q(summary__icontains=search) |
			Q(content__icontains=search)
		)
	
	# Add can_edit flag for authenticated users
	if request.user.is_authenticated:
		for demo in demos:
			demo.can_edit = demo.can_edit(request.user)
	
	use_cases = request.GET.getlist('use_cases[]', [])
	
	# Apply use case filter
	if use_cases:
		demos = demos.filter(use_cases__in=use_cases)
	
	context = {
		'demos': demos,
	}
	return render(request, 'demos/partials/demo_list.html', context)

def demo_detail(request, slug):
	"""
	Render the detail page for a specific demo.

	Args:
		request: The HTTP request object.
		slug: The slug of the demo to display.

	Returns:
		HttpResponse: The rendered detail page for the demo.
	"""
	demo = get_object_or_404(Demo, slug=slug)
	context = {
		'demo': demo,
	}
	return render(request, 'demos/demo_detail.html', context)

def category_detail(request, slug):
	"""
	Render the detail page for a specific category.

	Args:
		request: The HTTP request object.
		slug: The slug of the category to display.

	Returns:
		HttpResponse: The rendered detail page for the category.
	"""
	category = get_object_or_404(DemoCategory, slug=slug)
	demos = Demo.objects.filter(category=category)
	context = {
		'category': category,
		'demos': demos,
	}
	return render(request, 'demos/category_detail.html', context)
