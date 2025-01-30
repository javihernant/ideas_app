import strawberry
from gqlauth.user.queries import UserQueries, UserType
from gqlauth.user import arg_mutations as mutations


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
