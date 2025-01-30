# @strawberry_django.type(model=USER_MODEL, filters=UserFilter)
# class UserQueries:
#     @strawberry_django.field(
#         description="Returns the current user if he is not anonymous."
#     )
#     def public_user(self, info: Info) -> Optional[UserType]:
#         user = get_user(info)
#         if not user.is_anonymous:
#             return user  # type: ignore
#         return None

#     @strawberry_django.field()
#     def me(self, info: Info) -> UserType:
#         user = get_user(info)
#         if not user.is_authenticated:
#             raise GQLAuthError(code=GQLAuthErrors.UNAUTHENTICATED)
#         return user  # type: ignore

#     @strawberry_django.type(model=USER_MODEL, filters=UserFilter)
