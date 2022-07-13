import os
import json
from heyoo import WhatsApp
from flask import Flask, request


app = Flask(__name__)

# Load .env file

messenger = WhatsApp('EAAHlPsvlZAjABAFga1efGt53S7LJzQu9AfsIvBs8fpXvyz9RIZAkA4ORvJ5OmZBCv1gSBoeKwOAbMCm5z3CunhBcZBG4soByv7q3ae0sBJXrn1hJbUcWLVcEXEZAMCzaokmkMgYy5Ibc5s6qOad2U1lT7mq5SagOwHmJqwwJZA2g4q0dIbgO60wpNVVHeTYCSmGTGD6tKoImaVW8ClQq02',

phone_number_id='103290435735343')
VERIFY_TOKEN = "Test"


@app.route("/", methods=["GET", "POST"])
def hook():
    print("got it")
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"

    data = request.get_json()
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            message_type = messenger.get_message_type(data)

            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                print(f"{name} with this {mobile} number sent  {message}")
                messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                print(message_response)

            else:
                pass
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"


if __name__ == "__main__":
    app.run(port=5000, debug=True,host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'))