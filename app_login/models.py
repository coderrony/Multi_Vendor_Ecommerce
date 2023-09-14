from django.db import models

# to create a custom user model and admin panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.utils.translation import gettext_lazy as _

# to automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class MyUserManager(BaseUserManager):
    # a custom manager to deal with emails as unique identifier
    def create_user(self, email, password, **extra_fields):
        #  creates and saves a user with a give email and password

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(_("staff status"),
                                   default=False,
                                   help_text=_("Designates whether the user can log in this site"))

    is_active = models.BooleanField(_("active"),
                                    default=True,
                                    help_text=_(
        "Designates whether the user should be treated as active. unselect this instead of deleting accounts"))

    USERNAME_FIELD = 'email'
    object = MyUserManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username + "s Profile"

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == "":
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
