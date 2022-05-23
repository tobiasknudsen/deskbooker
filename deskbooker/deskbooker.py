#!/usr/bin/env python
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

import dateutil.parser
from dotenv import load_dotenv
from prettytable import PrettyTable

from .deskbird_client import DeskbirdClient

load_dotenv()


db_client = DeskbirdClient(
    refresh_token=os.environ["REFRESH_TOKEN"],
    token_key=os.environ["TOKEN_KEY"],
    resource_id=os.environ["RESOURCE_ID"],
    zone_item_id=os.environ["ZONE_ITEM_ID"] if "ZONE_ITEM_ID" in os.environ else None,
    workspace_id=os.environ["WORKSPACE_ID"],
)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "function_name",
    type=str,
    choices=["book", "checkin", "bookings"],
    help="Function name",
)
arg_parser.add_argument("-f", "--from", dest="from_date", help="From date")
arg_parser.add_argument("-t", "--to", dest="to_date", help="To date")
arg_parser.add_argument("-d", "--desk", dest="desk_number", help="Desk number")
arg_parser.add_argument("-z", "--zone", dest="zone", help="Set zone")


def main():
    try:
        args = arg_parser.parse_args()
        if args.function_name == "checkin":
            db_client.checkin()
        elif args.function_name == "bookings":
            bookings = json.loads(db_client.get_bookings(limit=30).text)
            bookings_table = PrettyTable(["Date", "Zone", "Desk", "Check-in"])

            for booking in bookings["results"]:
                booking_list = [
                    datetime.fromtimestamp(
                        int(booking["bookingStartTime"] / 1000)
                    ).date(),
                    booking["resource"]["groupName"],
                    f"{booking['resource']['name']} {booking['zoneItemName']}",
                    "✅" if booking["checkInStatus"] == "checkedIn" else "❌",
                ]
                bookings_table.add_row(booking_list)
            print(bookings_table)
        elif args.function_name == "book":
            if args.from_date is None or args.to_date is None:
                arg_parser.error("book requires --from and --to")
            try:
                from_date = dateutil.parser.parse(args.from_date)
            except dateutil.parser._parser.ParserError:
                arg_parser.error(f"{args.from_date} is not a valid date format")
            try:
                to_date = dateutil.parser.parse(args.to_date)
            except dateutil.parser._parser.ParserError:
                arg_parser.error(f"{args.to_date} is not a valid date format")
            if (args.zone is None) != (args.desk_number is None):
                print("Both zone and desk_number is not present.")
                return
            if args.zone is not None and args.desk_number is not None:
                try:
                    db_client.set_zone_item_id(
                        zone_name=args.zone, desk_id=args.desk_number
                    )
                except KeyError as e:
                    arg_parser.error(e)
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
        return 0
    except KeyboardInterrupt:
        print("Stopping...")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
