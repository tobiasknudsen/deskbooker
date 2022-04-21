# Deskbooker

Small tool for booking a desk for multiple days on Deskbird

## Installation


```console
poetry install
```

Create a .env file with the following

- TOKEN_KEY
- REFRESH_TOKEN
- RESOURCE_ID
- ZONE_ITEM_ID
- WORKSPACE_ID

\* check the network traffic on web.deskbird.app to find the correct values for your user and the desk you want to book.

## Usage

Make sure the virtual enviroment is activated

Book multiple days
```console
deskbooker book --to 1970.01.01 --from 1970.01.30
```

Check in today
```console
deskbooker checkin
```