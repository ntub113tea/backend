from django.core.management.base import BaseCommand
from myapp.models import Customer  # 导入你的自定义用户模型
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create a custom superuser'

    def handle(self, *args, **options):
        id = input("Enter id(phonenumber): ")
        password = input("Enter password: ")
        name = input("Enter name: ")
        sex = input("Enter sex: ")
        age = input("Enter age: ")




        Customer.objects.create_superuser(
            customer_id = id,
            password=password,
            customer_name = name,
            sex = sex,
            age = age,
            is_staff=True,
            is_superuser=True,
            date_joined=timezone.now()
        )

        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))