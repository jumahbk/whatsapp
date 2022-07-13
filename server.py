import os
import json
from heyoo import WhatsApp
from flask import Flask, request


app = Flask(__name__)

# Load .env file

messenger = WhatsApp('EAAHlPsvlZAjABAOEfd1bBtf5ZBDtxyquQ0rCL7MxfN4OZADYWdpScUTyKVwM6pd99QhIKE07uim2FKhJnAgmNERCO2s5c03iM7HLJQooXphqi0eYgjJCOeKazjGtZCngW124oVQ7aPIuYBfyJt1vOoNagvCx0HOQZB0zkf172hclN4tDUuuWvFhAT8M88JKmcvJbaN8kWRTAAiky5CM6A',
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