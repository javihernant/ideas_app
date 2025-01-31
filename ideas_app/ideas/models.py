from django.db import models
from django.conf import settings
from django_choices_field import TextChoicesField

USER = settings.AUTH_USER_MODEL


class Idea(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"
        PROTECTED = "protected", "Protected"

    title = models.CharField(max_length=128, null=True)
    text = models.CharField(max_length=255)
    user = models.ForeignKey(
        USER,
        blank=False,
        null=False,
        related_name="ideas",
        on_delete=models.CASCADE,
    )
    visibility = TextChoicesField(
        choices_enum=Visibility,
        default=Visibility.PROTECTED,
    )
    pub_date = models.DateTimeField(null=True)
