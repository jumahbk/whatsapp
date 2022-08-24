import requests
import os
import json
from heyoo import WhatsApp
from flask import Flask, request
from urllib.parse import unquote
import smtplib, ssl
from datetime import datetime
app = Flask(__name__)

# Load .env file

response = requests.get('https://www.medartclinics.com/tttt.bin')

keytoken = unquote(requests.get('https://www.medartclinics.com/tttt.bin').text)


messenger = WhatsApp(keytoken,

phone_number_id='105367738941421')
VERIFY_TOKEN = "test"


@app.route("/", methods=["GET", "POST"])
def hook():
   # print("got it")
    if request.method == "GET":
        if request.args.get("mobile"):
            return   messenger.send_templatev2("appointment_request", "555862924", '[{"type": "body","parameters": [{ "type": "text","text": "'+request.args.get("mobile")+'"}]}]', "ar")

        return 'shit'

   
    return "ok" 


if __name__ == "__main__":
    app.run(port=7000)