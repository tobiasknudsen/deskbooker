# Deskbooker

Small tool for booking a desk for multiple days on Deskbird

## Installation


```console
poetry install
```

Create a .env file with the following

- TOKEN_KEY
    - The included in the POST call to ```https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key=[TOKEN_KEY]``` when you sign in.
- REFRESH_TOKEN
    - The included in the response of the POST call to ```https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key=[TOKEN_KEY]``` when you sign in.
- RESOURCE_ID
- WORKSPACE_ID
- ZONE_ITEM_ID (not required)

\* check the network traffic on web.deskbird.app to find the correct values for your user and the desk you want to book.

## Usage

Make sure the virtual enviroment is activated

Book multiple days
```console
deskbooker book --to 1970.01.01 --from 1970.01.30 --zone Growth --desk 18
```

Check in today
```console
deskbooker checkin
```
