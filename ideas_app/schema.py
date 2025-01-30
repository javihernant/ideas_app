import strawberry
from gqlauth.core.middlewares import JwtSchema

from .ideas.root import IdeasMutation
from .users.root import UsersMutation, UsersQuery


@strawberry.type
class Mutation(UsersMutation, IdeasMutation): ...


@strawberry.type
class Query(UsersQuery): ...


# # This is essentially the same as strawberries schema though it
# # injects the user to `info.context["request"].user`
schema = JwtSchema(query=Query, mutation=Mutation)
