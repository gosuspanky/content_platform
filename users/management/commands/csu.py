import os

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание superuser"""

    def handle(self, *args, **options):
        user = User.objects.create(
            phone="79999999998",
            email="admin@sky.pro",
            password='artur290195',
            first_name="Admin",
            last_name="Admin",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            id=0,
        )
        user.set_password(os.getenv("ADMIN_PASSWORD"))
        user.save()
        print("Суперпользователь создан успешно!")
