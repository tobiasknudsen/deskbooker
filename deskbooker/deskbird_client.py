import json
from datetime import datetime

import requests

from desk_map import DESKS

from .auth import get_access_token


class DeskbirdClient:
    access_token = None
    refresh_token = None
    token_key = None
    resource_id = None
    zone = None
    zone_item_id = None
    workspace_id = None

    def __init__(
        self,
        refresh_token,
        token_key,
        resource_id,
        zone,
        desk_id,
        workspace_id,
    ):
        self.refresh_token = refresh_token
        self.token_key = token_key
        self.resource_id = resource_id
        self.zone = zone
        self.zone_item_id = self.get_zone_item_id(desk_id)
        self.workspace_id = workspace_id

        self.access_token = get_access_token(self.token_key, self.refresh_token)

    def set_desk(self, desk_id: str):
        if self.zone in DESKS and desk_id in DESKS[self.zone]:
            self.zone_item_id = DESKS[self.zone][desk_id]

    def set_zone(self, zone: str):
        if zone in DESKS.keys():
            self.zone = zone

    def get_zone_item_id(self, desk_id):
        return DESKS[self.zone][desk_id]

    def book_desk(self, date):
        url = "https://web.deskbird.app/api/v1.1/user/bookings"
        body = {
            "internal": True,
            "isAnonymous": False,
            "isDayPass": True,
            "resourceId": self.resource_id,
            "zoneItemId": self.zone_item_id,
            "workspaceId": self.workspace_id,
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        start_time = end_time = date
        start_time = start_time.replace(hour=9)
        end_time = end_time.replace(hour=17)
        body["bookingStartTime"] = int(start_time.timestamp() * 1000)
        body["bookingEndTime"] = int(end_time.timestamp() * 1000)

        return requests.post(url, headers=headers, data=json.dumps(body))

    def get_bookings(self, limit=10):
        url = (
            "https://app.deskbird.com/api/v1.1/user/bookings"
            f"?upcoming=true&skip=0&limit={limit}"
        )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        return requests.get(url, headers=headers)

    def checkin(self):
        url = (
            f"https://app.deskbird.com/api/v1.1/workspaces/"
            f"{self.workspace_id}/checkIn"
        )
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
            if (
                datetime.fromtimestamp(int(booking["bookingStartTime"] / 1000)).date()
                == datetime.today().date()
            ):
                if booking["checkInStatus"] == "checkedIn":
                    print("Already checked in!")
                    return
                else:
                    body["bookingId"] = booking["id"]
                    response = requests.post(
                        url, headers=headers, data=json.dumps(body)
                    )
                    print("Checked in!")
                    return response
        print("You don't have any valid bookings")
