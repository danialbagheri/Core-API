from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone

from blog.models import BlogPost
from product.models import Product


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name=_('email address'),
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    favorite_products = models.ManyToManyField(
        to=Product,
        blank=True,
    )

    bookmarked_blogposts = models.ManyToManyField(
        to=BlogPost,
        blank=True,
    )

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.id:
            self.email = self.email.lower()
            return super().save(*args, **kwargs)

        self.date_joined = timezone.now()
        for valid_domain in settings.VALID_STAFF_EMAIL_DOMAINS:
            if self.email.endswith(valid_domain):
                self.is_staff = True
                break
        return super(User, self).save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email
