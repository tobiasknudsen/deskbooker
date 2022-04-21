#!/usr/bin/env python
import argparse
import sys
from dateutil import parser
import json
import os
from datetime import timedelta
from dotenv import load_dotenv
from .deskbird_client import Deskbird_client

load_dotenv()


db_client = Deskbird_client(
    refresh_token=os.environ["REFRESH_TOKEN"],
    token_key=os.environ["TOKEN_KEY"],
    resource_id=os.environ["RESOURCE_ID"],
    zone_item_id=os.environ["ZONE_ITEM_ID"],
    workspace_id=os.environ["WORKSPACE_ID"],
)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("function", type=str, help="Function name")
arg_parser.add_argument("-f", "--from", dest="from_date", help="From date")
arg_parser.add_argument("-t", "--to", dest="to_date", help="To date")


def main():
    args = arg_parser.parse_args()
    if args.function == "checkin":
        db_client.checkin()
    elif args.function == "book":
        if args.from_date is None or args.to_date is None:
            arg_parser.error("book requires --from and --to")
        try:
            from_date = parser.parse(args.from_date)
        except Exception:
            arg_parser.error(f"{args.from_date} is not a valid date format")
        try:
            to_date = parser.parse(args.to_date)
        except Exception:
            arg_parser.error(f"{args.to_date} is not a valid date format")
        current_date = from_date
        while current_date <= to_date:
            if current_date.weekday() < 5:
                response = db_client.book_desk(current_date)
                if response.status_code != 201:
                    print(
                        " | ".join(
                            [
                                str(current_date.date()),
                                str(response.status_code),
                                response.reason,
                                json.loads(response.text)["message"],
                            ]
                        )
                    )
                else:
                    print(
                        " | ".join(
                            [
                                str(current_date.date()),
                                str(response.status_code),
                                response.reason,
                                "Desk is booked!",
                            ]
                        )
                    )
            current_date = current_date + timedelta(days=1)
    else:
        print(f"{args.function} is not a function")
    return 0


if __name__ == "__main__":
    globals()[sys.argv[1]]()
