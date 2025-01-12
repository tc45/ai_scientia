from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post
from django.utils.text import slugify
from datetime import datetime, timedelta
from utils.openai_utils import OpenAIContentGenerator
import random
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
	help = 'Generates sample blog posts and sets up Blog Writer group'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.content_generator = OpenAIContentGenerator()

	def create_blog_writer_group(self):
		# Create Blog Writer group
		blog_writer_group, created = Group.objects.get_or_create(name='Blog Writer')
		
		# Get content type for Post model
		content_type = ContentType.objects.get_for_model(Post)
		
		# Add relevant permissions
		permissions = Permission.objects.filter(
			content_type=content_type,
			codename__in=['add_post', 'change_post', 'view_post', 'delete_post']
		)
		blog_writer_group.permissions.add(*permissions)
		
		return blog_writer_group

	def generate_sample_post(self, author, index):
		if not settings.OPENAI_API_KEY:
			self.stdout.write(
				self.style.WARNING(
					"No OpenAI API key found. Using placeholder content instead."
				)
			)
			return self.generate_placeholder_post(author, index)
		
		topics = ['Machine Learning', 'Neural Networks', 'Computer Vision', 
				 'Natural Language Processing', 'Robotics', 'Deep Learning',
				 'Reinforcement Learning', 'AI Ethics', 'Data Science', 
				 'AI Applications']
		
		# Select the topic first
		topic = random.choice(topics)
		
		# Generate title variations
		title_templates = [
			"Understanding {topic}: A Comprehensive Guide",
			"The Future of {topic} in 2024",
			"How {topic} is Transforming Industries",
			"Best Practices in {topic}",
			"{topic}: From Theory to Practice"
		]
		
		# Select and format title
		title = random.choice(title_templates).format(topic=topic)
		
		# Create unique title if it already exists
		if Post.objects.filter(title=title).exists():
			title = f"{title} ({index})"

		# Generate content using OpenAI
		try:
			generated_content = self.content_generator.generate_blog_post(
				title=title,
				topic=topic
			)
			
			if not generated_content['content']:
				self.stdout.write(self.style.WARNING(f"Failed to generate content for {title}"))
				return None
				
		except Exception as e:
			self.stdout.write(self.style.ERROR(f"Error generating content: {e}"))
			return None

		# Generate random date within last 2 years
		days_ago = random.randint(0, 730)
		created_date = datetime.now() - timedelta(days=days_ago)
		
		# Randomly decide if post should be featured (make ~20% of posts featured)
		is_featured = random.random() < 0.2
		
		try:
			post = Post.objects.create(
				title=title,
				slug=slugify(title),
				author=author,
				content=generated_content['content'],
				excerpt=generated_content['excerpt'],
				status=1,  # Published
				created_on=created_date,
				featured=is_featured
			)
			
			# Randomly add likes
			num_likes = random.randint(0, 50)
			users = User.objects.all()[:num_likes]
			post.likes.add(*users)
			
			self.stdout.write(self.style.SUCCESS(f"Created post: {title}"))
			return post
			
		except Exception as e:
			self.stdout.write(self.style.ERROR(f"Error creating post: {e}"))
			return None

	def generate_placeholder_post(self, author, index):
		"""Generate a post with placeholder content when OpenAI is not available"""
		topics = ['Machine Learning', 'Neural Networks', 'Computer Vision', 
				 'Natural Language Processing', 'Robotics', 'Deep Learning',
				 'Reinforcement Learning', 'AI Ethics', 'Data Science', 
				 'AI Applications']
		
		topic = random.choice(topics)
		title = f"Sample Post about {topic} ({index})"
		
		post = Post.objects.create(
			title=title,
			slug=slugify(title),
			author=author,
			content=f"""
# {title}

## Introduction
This is a sample blog post about {topic}.

## Main Content
This is placeholder content because OpenAI API key is not configured.

## Conclusion
This is a conclusion about {topic}.
			""",
			excerpt=f"A sample post about {topic}",
			status=1,
			created_on=datetime.now() - timedelta(days=random.randint(0, 730)),
			featured=random.random() < 0.2
		)
		
		# Add random likes
		num_likes = random.randint(0, 50)
		users = User.objects.all()[:num_likes]
		post.likes.add(*users)
		
		self.stdout.write(self.style.SUCCESS(f"Created placeholder post: {title}"))
		return post

	def handle(self, *args, **kwargs):
		# Create superuser if it doesn't exist
		if not User.objects.filter(username='admin').exists():
			User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
		
		# Create Blog Writer group
		blog_writer_group = self.create_blog_writer_group()
		
		# Create sample author if it doesn't exist
		author, created = User.objects.get_or_create(
			username='sample_author',
			defaults={
				'email': 'author@example.com',
				'is_staff': True
			}
		)
		if created:
			author.set_password('author123')
			author.save()
			blog_writer_group.user_set.add(author)
		
		# Generate 10 sample posts
		successful_posts = 0
		for i in range(10):
			if self.generate_sample_post(author, i):
				successful_posts += 1
		
		self.stdout.write(
			self.style.SUCCESS(
				f"Successfully generated {successful_posts} sample blog posts"
			)
		) 