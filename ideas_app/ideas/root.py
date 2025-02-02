from typing import cast, Iterable
import strawberry
from strawberry import Info, UNSET
import strawberry_django
from .types import IdeaType, IdeaInput, IdeaVisibilityInput
from .models import Idea
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import F, Q
from strawberry_django.relay import ListConnectionWithTotalCount
from django.utils import timezone
from ..users.models import CustomUser


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

    @strawberry_django.mutation(handle_django_errors=True)
    def delete_idea(self, info: Info, idea_id: strawberry.ID) -> IdeaType:
        user = info.context["request"].user
        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")
        idea = Idea.objects.get(pk=idea_id)
        if idea.user.id != user.id:
            raise PermissionDenied("User does not have permission to delete this idea")

        idea_pk = idea.pk
        idea.delete()
        idea.pk = idea_pk
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

    @strawberry_django.connection(
        ListConnectionWithTotalCount[IdeaType],
    )
    def get_user_ideas(self, info: Info, user_id: int) -> Iterable[Idea]:
        user = info.context["request"].user
        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")

        if user.id == user_id:
            raise PermissionDenied("User cannot search his own ideas")

        user_exists = CustomUser.objects.filter(pk=user_id).exists()
        if not user_exists:
            raise ValidationError("error searching user. User does not exist")

        queryset = Idea.objects.filter(user=user_id).filter(
            visibility=Idea.Visibility.PUBLIC
        )
        is_following = (
            user.following.filter(followed=user_id).filter(is_accepted=True).count() > 0
        )
        if is_following:
            queryset |= Idea.objects.filter(user=user_id).filter(
                visibility=Idea.Visibility.PROTECTED
            )
        return queryset

    @strawberry_django.connection(
        ListConnectionWithTotalCount[IdeaType],
    )
    def my_timeline(self, info: Info) -> Iterable[Idea]:
        user = info.context["request"].user
        if not user or not user.is_authenticated or not user.is_active:
            raise PermissionDenied("No user logged in")

        my_ideas = Idea.objects.filter(user=user.id)
        following_ids = user.following.filter(is_accepted=True).values_list(
            "followed", flat=True
        )
        following_users_ideas = Idea.objects.filter(
            user__in=list(following_ids)
        ).filter(
            Q(visibility=Idea.Visibility.PUBLIC)
            | Q(visibility=Idea.Visibility.PROTECTED)
        )
        queryset = (my_ideas | following_users_ideas).order_by(
            F("pub_date").desc(nulls_last=True)
        )
        return queryset
