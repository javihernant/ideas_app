import strawberry
from strawberry import Info
import strawberry_django
from gqlauth.user.queries import UserQueries, UserType
from gqlauth.user import arg_mutations as mutations
from django.core.exceptions import PermissionDenied, ValidationError
from .models import UserConnection, CustomUser
from .types import UserConnectionType
from typing import cast


@strawberry.type
class UsersQuery:
    me: UserType = UserQueries.me


@strawberry.type
class UsersMutation:
    token_auth = mutations.ObtainJSONWebToken.field
    register = mutations.Register.field
    verify_account = mutations.VerifyAccount.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field
    password_reset = mutations.PasswordReset.field

    @strawberry_django.mutation(handle_django_errors=True)
    def request_follow(self, info: Info, follow_id: int) -> UserConnectionType:
        user = info.context["request"].user

        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")

        if user.id == follow_id:
            raise ValidationError("A user can not request to follow himself")

        follow_user = CustomUser.objects.get(pk=follow_id)
        existing_requests = (
            UserConnection.objects.filter(follower=user)
            .filter(followed=follow_user)
            .count()
        )
        if existing_requests > 0:
            raise ValidationError("User has already requested to follow that user")

        new_conn = UserConnection(followed=follow_user, follower=user)
        new_conn.save()
        return cast(UserConnectionType, new_conn)
