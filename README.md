# Ideas app

Social network app to create and share ideas

## Run app


Start docker compose services:

```sudo docker compose up```

## Usage

### Register a user and verify account
To register a user specify username, email and password:

```
mutation RegisterUser1 {
  register(
    email: "user1@email.com",
    username: "user1",
    password1: "mypass1234",
    password2: "mypass1234",
  ) {
    success,
    errors,
  }
}
```

After posting this mutation, an email will be sent with a link containing a verification token. It looks like this:
`eyJ1c2VybmFtZSI6InVzZXIxIiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1tckid:4l4nB3FYWs0UHnxDwPN9wEpIMMkmQ01JiWDFM2FQoWA`

NOTE: As of the current version of this project, email is sent to console stdout.

Use it to verify the user just created with:

```
mutation VerifyAccount {
  verifyAccount(token: "<token>") {
    success,
    errors
  }
}
```

### Login
You can log in with an email using this mutation:

```
mutation TokenAuth {
  tokenAuth(email: "user1@email.com", password: "mypass1234") {
    success
    errors
    token {
      payload {
        origIat
        exp
      }
      token
    }
    user {
      isActive
      username
      email
      status {
        verified
      }
    }
  }
}
```

It will return the authentication token that our mobile app can use.

Additionally, we can view other info such as:
    -Token info: date when the token was originally issued and expiration time.
    -Account info: Username, email, verification state, etc.
    -Check if tokenAuth operation was succesful and view the errors that may have occurred.

### Retrieve data for the currently authenticated user

```
 query Me {
      me{
        username
        verified
      }
    }
```

Make sure to add the token in the headers like so:

`{"authorization": "JWT <token>"}`

### Reset password
A user can reset its password by receiving a password reset email:

```
mutation PasswordResetEmail {
  sendPasswordResetEmail(email:"user1@email.com") {
    errors
  }
}
```

This email will contain a link with a token that should be used to later reset the user's password:

```
mutation PasswordReset {
  passwordReset(token:"<token>", newPassword1:"mypassword0123", newPassword2:"mypassword0123" ){
    errors
  }
}
```

### Create an Idea

A logged in user can create an idea by using:

```
mutation CreateIdea {
  createIdea(input:{title:"DIY project" text:"social network for sharing ideas" visibility:PUBLIC}) {
    __typename
      ... on OperationInfo { messages { message } }
      ... on IdeaType {
        title
        text
        visibility
      }
  }
}
```

Visibility is optional. If not provided it will default to PROTECTED, meaning only you and your followers
will be able to see your ideas.

### Modify visibility of an idea

The visibility of an idea can be changed to PUBLIC, PROTECTED or PRIVATE.
This operation requires the user to be authenticated.

```
mutation ModifyIdea {
  changeIdeaVisibility(input:{id:3 visibility:PRIVATE}) {
    __typename
      ... on OperationInfo { messages { message } }
      ... on IdeaType {
        id
        title
        text
        visibility
      }
  }
}
```

### View my ideas

A logged in user can view their ideas with this query:

```
query MyIdeas {
  myIdeas {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        text
        title
        visibility
      }
    }
  }
}
```

Results are returned paginated. This would avoid saturating the server in case there were a big amount of items to be returned.
Instead of returning them all at once, they would be sectioned in pages that the user could freely navigate through. 

This is using strawberry's relay implementation. Check out the [docs](https://strawberry.rocks/docs/guides/relay) for
more info on how they work.

## Development

### Ruff and pre-commit

You can install a precommit that runs ruff previous to making a commit.

You just have to:
1. Install the following packages with your prefered python package manager (pip, pipx, etc.):
  - pre-commit package
  - ruff package
2. Install the configured pre-commit hook in your .git directory using:
```pre-commit install```

pre-commit hooks are configured at `.pre-commit-config.yaml`

### Some useful docker commands

If needed to rebuild any of the services configured in docker-compose, use:

```sudo docker compose build --no-cache <service>```

You can also run any application inside a container by using:

```sudo docker compose run web django-admin startproject ideasapp .```