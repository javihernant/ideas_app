# Ideas app

Social network app to create and share ideas

## Run app

Using docker compose:
```sudo docker compose up```

If needed to rebuild any of the services configured in docker-compose, use:
```sudo docker compose build --no-cache <service>```

You can also run any application inside a container by using:
```sudo docker compose run web django-admin startproject ideasapp .```

##Considerations
- Uses [strawberry-django-auth](https://github.com/nrbnlulu/strawberry-django-auth) for authentication, that provides an authentication token to be used by the mobile app.

## Usage

### Register a user and verify account
To register a user specify username, email and password:
```
mutation {
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
mutation {
  verifyAccount(token: "<token>") {
    success,
    errors
  }
}
```

### Login
You can log in with an email using this mutation:

```
mutation {
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
 query{
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
mutation {
  sendPasswordResetEmail(email:"user1@email.com") {
    errors
  }
}
```
This email will contain a link with a token that should be used to later reset the user's password:

```
mutation {
  passwordReset(token:"<token>", newPassword1:"mypassword0123", newPassword2:"mypassword0123" ){
    errors
  }
}
```