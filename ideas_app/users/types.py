from . import models
from strawberry import auto, relay
import strawberry_django


@strawberry_django.type(models.UserConnection)
class UserConnectionType(relay.Node):
    follower: auto
    followed: auto
    is_accepted: auto
