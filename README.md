# Deskbooker

Small tool for booking a desk for multiple days on Deskbird

## Installation

Resolve dependencies via [poetry](https://python-poetry.org/):
```console
poetry install
```

I have just set up an alias to run it from wherever.
```deskbooker='~/dev/deskbooker/.venv/bin/python ~/dev/deskbooker/deskbooker/deskbooker.py'```

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

### Daily runner

I have set up a cronjob that runs ```daily_runner.py``` every morning at 8:55. If i'm connected to one of the office WIFIs it checks me in, if not it cancels my booking.

Make sure you have added the name(s) of your office WIFIs to your .env file seperated by "```,```"

```console
crontab -e
```

Add

```55 8 * * 1-5 [path_to_deskbooker]/.venv/bin/python [path_to_deskbooker]/deskbooker/daily_runner.py```
to run it monday-friday at 8:55.
