from django.core.management.base import BaseCommand
from learning.models import Tutorial
from django.utils.text import slugify
import uuid

class Command(BaseCommand):
    help = 'Fix missing slugs in tutorials'

    def handle(self, *args, **kwargs):
        tutorials = Tutorial.objects.filter(slug='')
        for tutorial in tutorials:
            base_slug = slugify(tutorial.title)
            if Tutorial.objects.filter(slug=base_slug).exists():
                base_slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            tutorial.slug = base_slug
            tutorial.save()
            self.stdout.write(self.style.SUCCESS(f'Fixed slug for tutorial: {tutorial.title}')) 