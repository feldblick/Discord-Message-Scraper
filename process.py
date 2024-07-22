import json, os
import util

class Processor:
    def __init__(self, input_file: str, output_file: str) -> None:
        self._input_file = input_file
        self._output_file = output_file

    def read(self):
        with open(f"output/scraper/{self._input_file}", "r") as f:
            self._json: list[dict] = json.load(f)

    def save(self):
        if not os.path.exists("output/processor"):
            os.makedirs("output/processor")

        with open(f"output/processor/{self._output_file}", "w") as f:
            json.dump(self._json, f, indent = 4)

    def replace_timestamp(self):
        for i, message in enumerate(self._json.copy()):
            self._json[i]["timestamp"] = util.utc_to_local(message["timestamp"])

    def replace_mentions(self):
        users = {}

        for message in self._json:
            users[message["author_id"]] = f"{message["author_username"]}{f"#{message["author_discriminator"]}" if int(message["author_discriminator"]) else ""}"

        for i, message in enumerate(self._json.copy()):
            if message["mentions"]:
                for k, v in users.items():
                    self._json[i]["content"] = self._json[i]["content"].replace(f"<@{k}>", f"@{v}")
