import math, typing
import util

def scrape(token: str, channel_id: int, number_messages: int, loop_finished_callback: typing.Callable[[int, int], None] | None = None):
    client = util.DiscordClient(token)
    number_loops = math.ceil(util.round_up(number_messages, 50) / 50)

    data: list[dict] = []

    prev_message_id = 0
    messages = client.retrieve_messages(channel_id)
    
    message_count = 0
    loop_count = 0
    
    stop = False
    while not stop:
        for message in messages:
            prev_message_id = message["id"]

            data.append({
                "content": message["content"],
                "message_id": message["id"],
                "author_id": message["author"]["id"],
                "author_username": message["author"]["username"],
                "author_discriminator": message["author"]["discriminator"],
                "timestamp": message["timestamp"],
                "attachments": message["attachments"],
                "mentions": message["mentions"]
            })

            data[message_count]["reactions"] = []

            if "reactions" in message:
                data[message_count]["reactions"] = message["reactions"]

                for reaction_i, reaction in enumerate(data[message_count]["reactions"]):
                    data[message_count]["reactions"][reaction_i] = {
                        "name": reaction["emoji"]["name"],
                        "count": reaction["count"]
                    }
            for attachment_i, attachment in enumerate(data[message_count]["attachments"]):
                try:
                    data[message_count]["attachments"][attachment_i] = attachment["url"]
                except:
                    data[message_count]["attachments"][attachment_i] = attachment

            for mention_i, mention in enumerate(data[message_count]["mentions"]):
                data[message_count]["mentions"][mention_i] = {
                    "id": mention["id"],
                    "username": mention["username"],
                    "discriminator": mention["discriminator"]
                }

            message_count += 1

            if message_count >= number_messages:
                stop = True
                break

        messages = client.retrieve_messages_before(channel_id, prev_message_id)

        if loop_finished_callback:
            loop_finished_callback(loop_count, number_loops)

        loop_count += 1

        if loop_count >= number_loops:
            stop = True
    
    return data