import requests
from flask import Flask,request,json
from heyoo import WhatsApp
from urllib.parse import unquote

response = requests.get('https://www.medartclinics.com/tttt.bin')

keytoken = unquote(requests.get('https://www.medartclinics.com/tttt.bin').text)
def send_message(message, keytoken):

    response = requests.get('https://www.medartclinics.com/tttt.bin')
    messenger = WhatsApp(keytoken,  phone_number_id='103290435735343')
    r = messenger.send_templatev2("appointment_remainder", "966555862924", '[{"type": "body","parameters": [{ "type": "text","text": "your-text-string"},{"type": "text","text": "your-text-string"},  { "type": "text","text": "your-text-string"}]}]', "ar")
    print(r)
    





app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
       send_message('test1',keytoken)
       return 'ok'
    else:
        send_message('test2',keytoken)
        return 'ok'
 
if __name__ == '__main__':

    app.run(port=5001)
