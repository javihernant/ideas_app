import strawberry
from gqlauth.user.queries import UserQueries
from gqlauth.core.middlewares import JwtSchema
from gqlauth.user import arg_mutations as mutations

from .types import User


@strawberry.type
class Query:
    me: User = UserQueries.me


@strawberry.type
class Mutation:
    token_auth = mutations.ObtainJSONWebToken.field
    register = mutations.Register.field
    verify_account = mutations.VerifyAccount.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field
    password_reset = mutations.PasswordReset.field


schema = JwtSchema(query=Query, mutation=Mutation)
