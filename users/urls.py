from strawberry.django.views import AsyncGraphQLView

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .schema import schema

urlpatterns = [
    path("graphql", csrf_exempt(AsyncGraphQLView.as_view(schema=schema))),
]