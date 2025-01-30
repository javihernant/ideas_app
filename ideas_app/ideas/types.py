from . import models
from strawberry import auto
import strawberry_django


@strawberry_django.type(models.Idea)
class IdeaType:
    id: auto
    title: auto
    text: auto
    visibility: auto


@strawberry_django.input(models.Idea)
class IdeaInput:
    title: auto
    text: auto
    visibility: auto
