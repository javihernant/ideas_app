from django.db import models

# # # Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True, blank=False, max_length=254, verbose_name="email address"
    )

    USERNAME_FIELD = "email"  # e.g: "username", "email"
    EMAIL_FIELD = "email"  # e.g: "email", "primary_email"
    REQUIRED_FIELDS = ["username"]


class UserConnection(models.Model):
    followed = models.ForeignKey(
        CustomUser,
        blank=False,
        null=False,
        related_name="followers",
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        CustomUser,
        blank=False,
        null=False,
        related_name="following",
        on_delete=models.CASCADE,
    )
    is_accepted = models.BooleanField(default=False)
