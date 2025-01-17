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
		category_q = Q()
		for cat in categories:
			if '-' in cat:  # This is a subcategory
				# Get parent category and check if it's in the filter
				parent_slug = cat.split('-')[0]
				if parent_slug not in categories:
					# Only add subcategory if parent isn't selected
					category_q |= Q(category__subcategories__slug=cat)
			else:  # This is a parent category
				category_q |= Q(category__slug=cat)
		demos = demos.filter(category_q).distinct()
	
	# Apply search filter
	if search:
		demos = demos.filter(
			Q(title__icontains=search) |
			Q(summary__icontains=search) |
			Q(content__icontains=search)
		).distinct()
	
	# Apply use case filter
	use_cases = request.GET.getlist('use_cases[]', [])
	if use_cases and 'all' not in use_cases:
		demos = demos.filter(use_cases__in=use_cases)
	
	# Annotate demos with category information
	demos = demos.select_related('category', 'subcategory', 'author')

	# Add can_edit flag for authenticated users
	if request.user.is_authenticated:
		for demo in demos:
			demo.can_edit = demo.can_edit(request.user)
			
			# If the demo's category is a subcategory, get its parent
			if '-' in demo.category.slug:
				parent_slug = demo.category.slug.split('-')[0]
				try:
					parent = DemoCategory.objects.get(slug=parent_slug)
					demo.category.name = f"{parent.name} > {demo.category.name}"
				except DemoCategory.DoesNotExist:
					pass

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
