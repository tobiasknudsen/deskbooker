# Deskbooker

Small tool for booking a desk for multiple days on Deskbird

## Installation

Resolve dependencies via [poetry](https://python-poetry.org/):
```console
poetry install
```
This will also create a script so deskbooker can be run as an executable.

Create a .env file with the following

```
TOKEN_KEY=AIzaSyCJG2vthfqCzIEfbY343MABk46DAuvncRQ
REFRESH_TOKEN=AIwUaOl4PgvgD-[...]
RESOURCE_ID=0000
WORKSPACE_ID=000
ZONE_ITEM_ID=00000 (not required)
```

\* check the network traffic on web.deskbird.app to find the correct values for your user and the desk you want to book.

TOKEN_KEY can be fetched from the request when you login with SSO:
```
https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key=[TOKEN_KEY]
```

And REFRESH_TOKEN is in the response.

WORKSPACE_ID and RESOURCE_ID is fetched from the request that is made when you book a table.

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

Cancel todays booking
```console
deskbooker cancel
```

See all current bookings
```console
deskbooker bookings
```
