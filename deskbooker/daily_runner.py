import os
import subprocess

from deskbird_client import DeskbirdClient
from dotenv import load_dotenv

load_dotenv()

try:
    office_wifis = os.environ["OFFICE_WIFIS"].split(",")
except KeyError:
    print("Can't find OFFICE_WIFIS in .env file")
    raise SystemExit


def get_wifi_info():
    process = subprocess.Popen(
        [
            (
                "/System/Library/PrivateFrameworks/Apple80211.framework"
                "/Versions/Current/Resources/airport"
            ),
            "-I",
        ],
        stdout=subprocess.PIPE,
    )
    out, err = process.communicate()
    process.wait()

    wifi_info = {}
    for line in out.decode("utf-8").split("\n"):
        if ": " in line:
            key, val = line.split(": ")
            key = key.replace(" ", "")
            val = val.strip()

            wifi_info[key] = val

    return wifi_info


db_client = DeskbirdClient(
    refresh_token=os.environ["REFRESH_TOKEN"],
    token_key=os.environ["TOKEN_KEY"],
    resource_id=os.environ["RESOURCE_ID"],
    zone_item_id=os.environ["ZONE_ITEM_ID"] if "ZONE_ITEM_ID" in os.environ else None,
    workspace_id=os.environ["WORKSPACE_ID"],
)


wifi_info = get_wifi_info()


if wifi_info["SSID"] in office_wifis:
    print("At the office! Checking in....")
    db_client.checkin()
else:
    print("Not at the office. Canceling booking...")
    db_client.cancel_booking()
