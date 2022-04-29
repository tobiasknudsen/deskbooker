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

Token key can be fetched from the request when you login with SSO:
```
https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key=[TOKEN_KEY]
```

And refresh token is in the response.

workspace_id and resource_id is fetched from the request that is made when you book a table. 

## Usage

Make sure the virtual enviroment is activated

Book multiple days
```console
deskbooker book --to 1970.01.30 --from 1970.01.01 --zone Growth --desk 18
```

or if you have ZONE_ITEM_ID in your .env file

```console
deskbooker book --to 1970.01.30 --from 1970.01.01
```

Check in today
```console
deskbooker checkin
```
