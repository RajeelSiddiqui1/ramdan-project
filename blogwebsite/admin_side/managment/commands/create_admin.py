from django.core.management.base import BaseCommand
from admin_side.models import Admin

class Command(BaseCommand):
    help = 'Creates initial admin user'

    def handle(self, *args, **options):
        email = 'rajeelsiddiqui3@gmail.com'
        password = '123'
        
        if not Admin.objects.filter(email=email).exists():
            Admin.objects.create(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin: {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin with email {email} already exists'))