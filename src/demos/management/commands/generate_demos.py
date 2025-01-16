from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from demos.models import Demo, DemoCategory, SubCategory
from utils.openai_utils import OpenAIContentGenerator
import random
from django.utils.text import slugify
from django.db import IntegrityError

class Command(BaseCommand):
	help = 'Generate sample demos with multi-level categories and features'

	def handle(self, *args, **kwargs):
		User = get_user_model()
		admin_user = User.objects.filter(is_superuser=True).first()

		if not admin_user:
			self.stdout.write(self.style.ERROR('No admin user found'))
			return

		# Define categories and subcategories
		categories = {
			'Prompting': ['Agents', 'Context Management', 'Chain of Thought', 'Advanced Templates'],
			'Data Ingestion': ['RAG', 'APIs', 'Data Cleaning', 'Embedding Databases'],
			'Data Retrieval': ['Vector Search', 'Knowledge Graphs', 'Indexing', 'Semantic Search'],
			'Knowledge Management': ['Summarization', 'Question Answering', 'Multi-Modal Data', 'Document Parsing'],
			'Automation': ['Workflow Orchestration', 'Task Scheduling', 'Event-Driven Processes', 'Agentic Workflows'],
			'Interaction': ['Chatbots', 'Virtual Assistants', 'Conversational Agents', 'Feedback Loops'],
			'Deployment': ['Cloud Hosting', 'On-Premise Solutions', 'Containerization', 'CI/CD Pipelines'],
			'Integration': ['APIs and SDKs', 'Third-Party Tools', 'Custom Plugins', 'Data Connectors']
		}

		# Create categories and subcategories
		for parent_name, subcategories in categories.items():
			parent_category, _ = DemoCategory.objects.get_or_create(name=parent_name)
			for subcategory_name in subcategories:
				SubCategory.objects.get_or_create(name=subcategory_name, parent_category=parent_category)

		# Generate sample demos
		generator = OpenAIContentGenerator()
		difficulty_levels = ['beginner', 'intermediate', 'advanced']
		use_cases = ['business', 'technical', 'educational']

		demo_topics = [
			"Introduction to Prompting",
			"Advanced Agents with CrewAI",
			"Langchain for Context Management",
			"Chain of Thought Techniques",
			"Building Advanced Templates",
			"RAG with ChomaDB",
			"API Integration for Data Ingestion",
			"Data Cleaning Best Practices",
			"Embedding Databases Overview",
			"Vector Search Techniques",
			"Knowledge Graphs in AI",
			"Indexing Strategies",
			"Semantic Search Implementation",
			"Summarization Techniques",
			"Question Answering Systems",
			"Multi-Modal Data Processing",
			"Document Parsing with AI",
			"Workflow Orchestration with LangChain",
			"Task Scheduling in AI",
			"Event-Driven Processes",
			"Agentic Workflows",
			"Building Chatbots",
			"Virtual Assistants Development",
			"Conversational Agents",
			"Feedback Loops in AI",
			"Cloud Hosting for AI",
			"On-Premise AI Solutions",
			"Containerization for AI",
			"CI/CD Pipelines for AI",
			"APIs and SDKs Integration",
			"Third-Party Tools for AI",
			"Custom Plugins Development",
			"Data Connectors in AI"
		]

		for topic in demo_topics:
			difficulty = random.choice(difficulty_levels)
			use_case = random.choice(use_cases)
			category = DemoCategory.objects.order_by('?').first()
			tags = ', '.join(random.sample(['#Chatbot', '#Workflow', '#ChromaDB', '#Langchain', '#AI'], 2))

			self.stdout.write(f"Generating demo for: {topic}")

			content = generator.generate_blog_post(
				title=topic,
				topic=f"{topic} for {difficulty} level students"
			)

			if content['content']:
				try:
					# Generate a unique slug
					slug_base = slugify(topic)
					slug = slug_base
					counter = 1
					while Demo.objects.filter(slug=slug).exists():
						slug = f"{slug_base}-{counter}"
						counter += 1

					demo = Demo.objects.create(
						title=topic,
						slug=slug,
						category=category,
						content=content['content'],
						summary=content['excerpt'],
						difficulty_level=difficulty,
						is_published=True,
						author=admin_user,
						tags=tags,
						use_cases=use_case
					)
					self.stdout.write(self.style.SUCCESS(f'Created demo: {topic}'))
				except IntegrityError as e:
					self.stdout.write(self.style.ERROR(f'Failed to create demo {topic}: {str(e)}'))
				except Exception as e:
					self.stdout.write(self.style.ERROR(f'Failed to create demo {topic}: {str(e)}'))
			else:
				self.stdout.write(self.style.ERROR(f'Failed to generate content for: {topic}')) 