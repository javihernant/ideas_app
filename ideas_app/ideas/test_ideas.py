import pytest

# from strawberry.aiohttp.test.client import GraphQLTestClient
from strawberry_django.test.client import TestClient
from ..users.models import CustomUser
from gqlauth.core.utils import app_settings


@pytest.mark.django_db(transaction=True)
def test_create_idea(db):
    client = TestClient("/api/")
    mutation = """
    mutation CreateIdea ($title:String $text:String!) {
        createIdea(input:{title:$title text:$text visibility:PUBLIC}) {
            ... on OperationInfo { messages { message } }
            ... on IdeaType {
                title
                text
                visibility
            }
        }
    }
    """

    title = "test idea"
    text = "this is an idea"
    user = CustomUser.objects.create(
        username="myusername",
        email="myemail@example.com",
        password="mypassword",
        is_active=True,
    )
    token = app_settings.JWT_PAYLOAD_HANDLER(user).token
    res = client.query(
        mutation, {"title": title, "text": text}, {"Authorization": f"JWT {token}"}
    )

    assert res.data["createIdea"] == {
        "title": title,
        "text": text,
        "visibility": "PUBLIC",
    }
