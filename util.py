import math, requests, json, datetime

def round_up(x: int, base: int):
    return int(base * math.ceil(x / base))

class DiscordClient:
    def __init__(self, token: str) -> None:
        self._auth = { "authorization": token }

        self._discord_url = "https://discord.com/api/v9"

    def retrieve_messages(self, channel_id: int) -> list:
        return json.loads(
            requests.get(f"{self._discord_url}/channels/{channel_id}/messages", headers = self._auth).text
        )

    def retrieve_messages_after(self, channel_id: int, after_id: int) -> list:
        return json.loads(
            requests.get(f"{self._discord_url}/channels/{channel_id}/messages?limit=50&after={after_id}", headers = self._auth).text
        )

    def retrieve_messages_before(self, channel_id: int, before_id: int) -> list:
        return json.loads(
            requests.get(f"{self._discord_url}/channels/{channel_id}/messages?limit=50&before={before_id}", headers = self._auth).text
        )

def utc_to_local(utc_time: str, format_str: str = "{m}/{d}/{y2} {h12}:{min}:{sec} {ampm}"):
    try: return parse_datetime(datetime.datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(), format_str)
    except: return parse_datetime(datetime.datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S%z").astimezone(), format_str)


def parse_datetime(datetime_: datetime.datetime, formatted: str):
    date_time_replace = {
        "{day}": "%d",
        "{month}": "%m",
        "{year2}": "%y",
        "{year4}": "%Y",
        "{second}": "%S",
        "{minute}": "%M",
        "{hour12}": "%I",
        "{hour24}": "%H",
        "{ampm}": "%p",

        "{d}": "%d",
        "{m}": "%m",
        "{y2}": "%y",
        "{y4}": "%Y",
        "{sec}": "%S",
        "{min}": "%M",
        "{h12}": "%I",
        "{h24}": "%H",
        "{ampm}": "%p",
    }
    
    for k, v in date_time_replace.items():
        formatted = formatted.replace(k, v)

    return datetime_.strftime(formatted)