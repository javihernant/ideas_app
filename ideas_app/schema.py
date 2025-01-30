import strawberry
from gqlauth.core.middlewares import JwtSchema

# from .ideas.root import (IdeasMutation, IdeasQuery)
from .users.root import UsersMutation, UsersQuery


@strawberry.type
class Mutation(UsersMutation): ...


@strawberry.type
class Query(UsersQuery): ...


# # This is essentially the same as strawberries schema though it
# # injects the user to `info.context["request"].user`
schema = JwtSchema(query=Query, mutation=Mutation)
