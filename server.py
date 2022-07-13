import os
import json
from heyoo import WhatsApp
from flask import Flask, request


app = Flask(__name__)

# Load .env file

messenger = WhatsApp('EAAHlPsvlZAjABAH9tpUMbtX0xZA6gnCVaGzrS26HrAdBR46WChbZBWWsA7gRfj3qG7dWiufgZCrCPdvZAxcUJkpZBYBZAJGsWi3lS7Jsbwnkqc0drHWhrLCZAKFYinVVIR27Vg8brRK1HwCDXzJ5ywNDIlpp0DBxA8IOp1fDE4CCkkaYnqNFIJvtQxzn4jTCSCZAyYw5lxsyK4ZB8phx2lMhjZC',

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