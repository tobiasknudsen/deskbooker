import json
from datetime import datetime, timedelta

import requests
from auth import get_access_token


class DeskbirdClient:
    access_token = None
    refresh_token = None
    token_key = None
    resource_id = None
    zone_item_id = None
    workspace_id = None
    API_BASE_URL = "https://app.deskbird.com/api/v1.1"
    APP_BASE_URL = "https://web.deskbird.app/api/v1.1"

    def __init__(
        self,
        refresh_token,
        token_key,
        resource_id,
        workspace_id,
        zone_item_id=None,
    ):
        self.refresh_token = refresh_token
        self.token_key = token_key
        self.resource_id = resource_id
        self.workspace_id = workspace_id
        self.zone_item_id = zone_item_id
        self.access_token = get_access_token(self.token_key, self.refresh_token)

    def set_zone_item_id(self, zone_name, desk_id):
        url = (
            f"{self.API_BASE_URL}/internalWorkspaces/"
            f"{self.workspace_id}/zones?internal"
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = json.loads(requests.get(url=url, headers=headers).text)
        for zone in response["results"]:
            if zone_name == zone["name"]:
                for desk in zone["availability"]["zoneItems"]:
                    if desk_id == desk["name"].split(" ")[-1]:
                        self.zone_item_id = desk["id"]
                        return
                raise KeyError(f"desk_id: {desk_id} not found in {zone_name}")
        raise KeyError(f"zone_name: {zone_name} does not exists")

    def book_desk(self, from_date, to_date):
        url = f"{self.API_BASE_URL}/multipleDayBooking"
        if not self.zone_item_id:
            raise Exception("ZONE_ITEM_ID missing from environment")
        body = {
            "bookings": [],
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        current_date = from_date
        while current_date <= to_date:
            if current_date.weekday() < 5:
                start_time = end_time = current_date
                start_time = start_time.replace(hour=9)
                end_time = end_time.replace(hour=17)
                body["bookings"].append(
                    {
                        "internal": True,
                        "isAnonymous": False,
                        "isDayPass": True,
                        "resourceId": self.resource_id,
                        "zoneItemId": self.zone_item_id,
                        "workspaceId": self.workspace_id,
                        "bookingStartTime": int(start_time.timestamp() * 1000),
                        "bookingEndTime": int(end_time.timestamp() * 1000),
                    }
                )
            current_date = current_date + timedelta(days=1)

        return requests.post(url, headers=headers, data=json.dumps(body))

    def get_bookings(self, limit=10):
        url = f"{self.API_BASE_URL}/user/bookings?upcoming=true&skip=0&limit={limit}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        return requests.get(url, headers=headers)

    def checkin(self):
        url = f"{self.API_BASE_URL}/workspaces/{self.workspace_id}/checkIn"
        body = {
            "isInternal": True,
            "resourceId": self.resource_id,
            "workspaceId": self.workspace_id,
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        bookings = json.loads(self.get_bookings().text)
        for booking in bookings["results"]:
            is_today = (
                datetime.fromtimestamp(int(booking["bookingStartTime"] / 1000)).date()
                == datetime.today().date()
            )
            if is_today:
                if booking["checkInStatus"] == "checkedIn":
                    print(
                        f"Already checked in to {booking['zoneItemName']}"
                        f" in {booking['resource']['name']}!"
                    )
                    return
                else:
                    body["bookingId"] = booking["id"]
                    response = requests.post(
                        url, headers=headers, data=json.dumps(body)
                    )
                    print("Checked in!")
                    return response
        print("You don't have any valid bookings")

    def cancel_booking(self, date=datetime.today().date()):
        body = {
            "workspaceId": self.workspace_id,
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        bookings = json.loads(self.get_bookings().text)
        for booking in bookings["results"]:
            is_correct_date = (
                datetime.fromtimestamp(int(booking["bookingStartTime"] / 1000)).date()
                == date
            )
            if is_correct_date:
                body["userId"] = booking["userId"]
                url = f"{self.API_BASE_URL}/user/bookings/{booking['id']}/cancel"
                response = requests.put(url=url, headers=headers, data=json.dumps(body))
                print(f"{date} canceled")
                return response
        print(f"You don't have a booking on {date}")
