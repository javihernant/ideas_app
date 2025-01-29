from strawberry import auto
import strawberry_django

from .models import CustomUser
from gqlauth.user.types_ import UserType


@strawberry_django.type(CustomUser)
class User(UserType):
    username: auto
