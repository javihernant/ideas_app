from typing import cast, Iterable
import strawberry
from strawberry import Info, UNSET
import strawberry_django
from .types import IdeaType, IdeaInput, IdeaVisibilityInput
from .models import Idea
from django.core.exceptions import PermissionDenied
from django.db.models import F
from strawberry_django.relay import ListConnectionWithTotalCount
from django.utils import timezone


@strawberry.type
class IdeasMutation:
    # handle_django_errors allow to handle common django errors, such as ValidationError, PermissionDenied and ObjectDoesNotExist
    @strawberry_django.mutation(handle_django_errors=True)
    def create_idea(self, info: Info, input: IdeaInput) -> IdeaType:
        user = info.context["request"].user
        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")

        new_idea = Idea(text=input.text, user=user, title=input.title)
        if input.visibility is not UNSET:
            new_idea.visibility = input.visibility
        new_idea.pub_date = timezone.now()
        new_idea.save()
        return cast(IdeaType, new_idea)

    @strawberry_django.mutation(handle_django_errors=True)
    def change_idea_visibility(
        self, info: Info, input: IdeaVisibilityInput
    ) -> IdeaType:
        user = info.context["request"].user
        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")
        idea = Idea.objects.filter(pk=input.id).get()
        if idea.user.id != user.id:
            raise PermissionDenied("User does not have permission to modify this idea")
        idea.visibility = input.visibility
        idea.save()
        return cast(IdeaType, idea)


@strawberry.type
class IdeasQuery:
    # @strawberry_django.field(pagination=True)
    @strawberry_django.connection(
        ListConnectionWithTotalCount[IdeaType],
    )
    def my_ideas(self, info: Info) -> Iterable[Idea]:
        user = info.context["request"].user
        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")
        ideas = Idea.objects.filter(user=user).order_by(
            F("pub_date").desc(nulls_last=True)
        )
        return ideas
