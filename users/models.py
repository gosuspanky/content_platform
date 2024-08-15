from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class UserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        """
        Create a new user with the given phone number, password, and any additional fields.

        Parameters:
            phone (str): The phone number of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields that can be passed to create the user.

        Returns:
            User: The newly created user object.
        """
        if not phone:
            raise ValueError('The phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Creates a superuser with the given phone, password, and any extra fields.

        :param phone: The phone number of the superuser
        :param password: The password for the superuser
        :param **extra_fields: Additional fields for the superuser
        :return: The created superuser
        :raises ValueError: If is_staff or is_superuser is not True
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model for the authentication app.
    """

    objects = UserManager()

    username = models.CharField(max_length=50, **NULLABLE, unique=True, verbose_name='Username')
    phone = models.CharField(max_length=25, unique=True, verbose_name='Phone number')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Avatar')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


from django.db import models

# Create your models here.
