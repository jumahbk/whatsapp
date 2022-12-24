import requests
from flask import Flask,request,json
from heyoo import WhatsApp
from urllib.parse import unquote
from datetime import datetime
import urllib.request, json 

response = requests.get('https://www.medartclinics.com/tttt.bin')

days = [
'الأثنين',
'الثلاثاء',
'الاربعاء', 
'الخميس',
'الجمعة',
'السبت',
'الأحد'
]


keytoken = unquote(requests.get('https://www.medartclinics.com/tttt.bin').text)
def send_message(message, keytoken, name, mobile):
  
    response = requests.get('https://www.medartclinics.com/tttt.bin')
    messenger = WhatsApp(keytoken,  phone_number_id='105367738941421')
    r = messenger.send_templatev2("profiloupdate", mobile, '[{"type": "body","parameters": [{ "type": "text","text": "'+name+'"}]}]', "ar")
    if "error" in r:
        print("Error")
        return 'Failed'
    else :
        print(r)
        d = r['messages'][0]['id']
        print(d)
        return d
    
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':

       return 'ok'
    else:
       pId = request.args.get('pId')
       name = request.args.get('name')

       mobile =request.args.get('mobile')
       if(mobile != None):


            payload = {
                    'aptId': '' +str(id),
                    'patId': '' + str(pId),
                    'dateSent': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                    'waid': '1',
                    'mobile': '' + mobile,
                    
                    'respond':'0',
                    'accept':'0'
                }
            res = requests.post('http://192.168.2.102/whatsappreminders/isDuplicate', data=payload)
            d = send_message('test2',keytoken, name, mobile )
            payload['waid']= d
         

               
       return "Done"

if __name__ == '__main__':

    app.run(port=9001, host='0.0.0.0')
