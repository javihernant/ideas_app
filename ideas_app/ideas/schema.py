# from typing import cast
# import strawberry
# from strawberry import Info
# from gqlauth.core.middlewares import JwtSchema
# import strawberry_django
# from .types import (
#     IdeaType
# )
# from . import models
# from gqlauth.core.types_ import GQLAuthError, GQLAuthErrors

# @strawberry.type
# class Mutation:
#     @strawberry_django.mutation(handle_django_errors=True)
#     def create_idea(self, info: Info, text: str) -> IdeaType:
#         user = info.context["request"].user

#         if not user.is_authenticated:
#             raise GQLAuthError(code=GQLAuthErrors.UNAUTHENTICATED)
#         return user
#         # return cast(IdeaType, new_idea)

# @strawberry.type
# class Query:
#     ideas: IdeaType = strawberry_django.field()

# schema = JwtSchema(query=Query, mutation=Mutation)
