from . import models
from strawberry import auto, relay, ID
import strawberry_django


@strawberry_django.type(models.Idea)
class IdeaType(relay.Node):
    id: relay.GlobalID
    title: auto
    text: auto
    visibility: auto


@strawberry_django.input(models.Idea)
class IdeaInput:
    title: auto
    text: auto
    visibility: auto


@strawberry_django.input(models.Idea)
class IdeaVisibilityInput:
    id: ID
    visibility: models.Idea.Visibility
