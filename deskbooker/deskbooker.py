#!/usr/bin/env python
import argparse
import json
import os
from datetime import datetime

import dateutil.parser
from deskbird_client import DeskbirdClient
from dotenv import load_dotenv
from prettytable import PrettyTable

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
    choices=["book", "checkin", "bookings", "cancel"],
    help="Function name",
)
arg_parser.add_argument("-f", "--from", dest="from_date", help="From date")
arg_parser.add_argument("-t", "--to", dest="to_date", help="To date")
arg_parser.add_argument("-d", "--desk", dest="desk_number", help="Desk number")
arg_parser.add_argument("-z", "--zone", dest="zone", help="Set zone")


def checkin(args):
    db_client.checkin()


def cancel(args):
    db_client.cancel_booking()


def bookings(args):
    bookings = json.loads(db_client.get_bookings(limit=30).text)
    bookings_table = PrettyTable(["Date", "Zone", "Desk", "Check-in"])

    for booking in bookings["results"]:
        booking_list = [
            datetime.fromtimestamp(int(booking["bookingStartTime"] / 1000)).date(),
            booking["workspace"]["name"],
            f"{booking['resource']['name']} {booking['zoneItemName']}",
            "✅" if booking["checkInStatus"] == "checkedIn" else "❌",
        ]
        bookings_table.add_row(booking_list)
    print(bookings_table)


def book(args):
    try:
        from_date = dateutil.parser.parse(args.from_date)
    except dateutil.parser._parser.ParserError:
        arg_parser.error(f"{args.from_date} is not a valid date format")
    try:
        to_date = dateutil.parser.parse(args.to_date)
    except dateutil.parser._parser.ParserError:
        arg_parser.error(f"{args.to_date} is not a valid date format")

    if (args.zone is None) != (args.desk_number is None):
        print("either of the following arguments are required: -z/--zone, -d/--desk")
        return
    if args.zone is not None and args.desk_number is not None:
        try:
            db_client.set_zone_item_id(zone_name=args.zone, desk_id=args.desk_number)
        except KeyError as e:
            arg_parser.error(e)
    response = db_client.book_desk(from_date=from_date, to_date=to_date)
    data_response = json.loads(response.text)
    bookings = [
        booking["booking"] for booking in data_response["data"]["successfulBookings"]
    ] + data_response["data"]["failedBookings"]
    bookings = sorted(bookings, key=lambda booking: booking["bookingStartTime"])
    for booking in bookings:
        if "errorMessage" in booking:
            print(
                " | ".join(
                    [
                        "❌",
                        str(
                            datetime.fromtimestamp(
                                booking["bookingStartTime"] / 1000
                            ).date()
                        ),
                        str(booking["errorMessage"]),
                    ]
                )
            )
        else:
            print(
                " | ".join(
                    [
                        "✅",
                        str(
                            datetime.fromtimestamp(
                                booking["bookingStartTime"] / 1000
                            ).date()
                        ),
                        str(booking["bookingStatus"]),
                    ]
                )
            )


def main():
    try:
        args = arg_parser.parse_args()
        if args.function_name == "checkin":
            checkin(args)
        elif args.function_name == "cancel":
            cancel(args)
        elif args.function_name == "bookings":
            bookings(args)
        elif args.function_name == "book":
            book(args)
        return 0
    except KeyboardInterrupt:
        print("Stopping...")


if __name__ == "__main__":
    main()
