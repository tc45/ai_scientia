from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from .constants import ICON_CHOICES
from django.utils.text import slugify

class DemoCategory(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True, null=True)
	icon = models.CharField(
		max_length=50, 
		choices=ICON_CHOICES, 
		help_text="FontAwesome icon class", 
		default="fas fa-flask"
	)
	order = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'demo categories'
		ordering = ['order', 'name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_category_tree(self):
		"""
		Returns a string representing the category hierarchy.
		"""
		tree = [self.name]
		parent = self.parent_category
		while parent:
			tree.append(parent.name)
			parent = parent.parent_category
		return " > ".join(reversed(tree))

class SubCategory(models.Model):
	name = models.CharField(max_length=200)
	parent_category = models.ForeignKey(DemoCategory, on_delete=models.CASCADE, related_name='subcategories')

	def __str__(self):
		return self.name

	def get_category_tree(self):
		"""
		Returns a string representing the category hierarchy.
		"""
		tree = [self.name]
		parent = self.parent_category
		while parent:
			tree.append(parent.name)
			parent = parent.parent_category
		return " > ".join(reversed(tree))

class Demo(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	category = models.ForeignKey(DemoCategory, on_delete=models.CASCADE)
	summary = models.TextField(help_text="A brief summary of the demo", blank=True, null=True)
	content = models.TextField()
	thumbnail = models.ImageField(upload_to='demos/thumbnails/', null=True, blank=True)
	author = models.ForeignKey(
		get_user_model(), 
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='demos'
	)
	is_featured = models.BooleanField(default=False)
	difficulty_level = models.CharField(
		max_length=20,
		choices=[
			('beginner', 'Beginner'),
			('intermediate', 'Intermediate'),
			('advanced', 'Advanced')
		],
		default='beginner'
	)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	is_published = models.BooleanField(default=False)
	icon = models.CharField(
		max_length=50, 
		choices=ICON_CHOICES,
		help_text="FontAwesome icon class",
		default="fas fa-flask"
	)
	tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for the demo")
	use_cases = models.CharField(
		max_length=50,
		choices=[
			('business', 'Business'),
			('technical', 'Technical'),
			('educational', 'Educational')
		],
		default='technical'
	)
	estimated_time = models.CharField(max_length=20, blank=True, null=True, help_text="Estimated time to complete the demo")
	
	class Meta:
		ordering = ['-created_on']
		
	def __str__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse('demos:demo_detail', args=[self.slug]) 

	def can_edit(self, user):
		return user.is_superuser or user == self.author

class Tag(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class SampleFormModel(models.Model):
	char_field = models.CharField(max_length=100, help_text="CharField for text input")
	choice_field = models.CharField(max_length=50, choices=[('option1', 'Option 1'), ('option2', 'Option 2')], help_text="ChoiceField for selecting an option")
	date_field = models.DateField(help_text="DateField for date input")
	datetime_field = models.DateTimeField(help_text="DateTimeField for date and time input")
	decimal_field = models.DecimalField(max_digits=5, decimal_places=2, help_text="DecimalField for decimal numbers")
	email_field = models.EmailField(help_text="EmailField for email input")
	float_field = models.FloatField(help_text="FloatField for floating point numbers")
	integer_field = models.IntegerField(help_text="IntegerField for integer numbers")
	slug_field = models.SlugField(help_text="SlugField for URL slugs")
	text_field = models.TextField(help_text="TextField for large text input")
	url_field = models.URLField(help_text="URLField for URL input")
	boolean_field = models.BooleanField(default=False, help_text="BooleanField for true/false values")
	null_boolean_field = models.BooleanField(null=True, blank=True, help_text="BooleanField for true/false/null values")
	time_field = models.TimeField(null=True, blank=True, help_text="TimeField for time input")
	duration_field = models.DurationField(null=True, blank=True, help_text="DurationField for time duration")
	file_field = models.FileField(upload_to='uploads/', null=True, blank=True, help_text="FileField for file uploads")
	image_field = models.ImageField(upload_to='images/', null=True, blank=True, help_text="ImageField for image uploads")
	positive_integer_field = models.PositiveIntegerField(null=True, blank=True, help_text="PositiveIntegerField for positive integers")
	positive_small_integer_field = models.PositiveSmallIntegerField(null=True, blank=True, help_text="PositiveSmallIntegerField for small positive integers")
	small_integer_field = models.SmallIntegerField(null=True, blank=True, help_text="SmallIntegerField for small integers")
	big_integer_field = models.BigIntegerField(null=True, blank=True, help_text="BigIntegerField for large integers")
	generic_ip_address_field = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=True, blank=True, help_text="GenericIPAddressField for IPv4/IPv6 addresses")
	uuid_field = models.UUIDField(null=True, blank=True, help_text="UUIDField for universally unique identifiers")
	multi_line_text_field = models.TextField(null=True, blank=True, help_text="Multi-line text input")
	tags = models.ManyToManyField(Tag, blank=True, help_text="Select tags for this item")

	def __str__(self):
		return f"SampleFormModel {self.id}"
