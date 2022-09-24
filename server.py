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
    print(request.args.get("hub.verify_token"))
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        print("Bad request")
        return "bad"
    data = request.get_json()
    
    #print(                message = data['messages'][0]['context']['id'])
 #   print(data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            

#"Id,Date,Mobile,Content,Sent"
            payload = {
                    #'aptId': '' +str(id),
                # 'patId': '' + str(patId),
                'Date': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
         
                'mobile': '' + mobile,
                    
                'Content':str(data),
                'Sent': 'False'
            }
            res = requests.post('http://192.168.2.102/whatsapplogs/create', data=payload)
            print(res.text)






            message_type = messenger.get_message_type(data)

            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
            #    print(f"{name} with this {mobile} number sent  {message}")
                #messenger.send_message(f"شكراً لتواصلك مع خدمة الرد الالي بعيادات ميد آرت فرع الخبر", mobile)
                print(messenger.send_template("welcome", mobile,"ar"))
                messenger.send_templatev2("user_text", "966555862924", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"},{ "type": "text","text": "'+message+'"}]}]', "ar")
                messenger.send_templatev2("user_text", "966557779388", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"},{ "type": "text","text": "'+message+'"}]}]', "ar")
                messenger.send_templatev2("user_text", "966500768855", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"},{ "type": "text","text": "'+message+'"}]}]', "ar")

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
            #    print(message_response)

            elif message_type == "button":
                message_response = messenger.preprocess(data)

          #      message_response = messenger.get_message(data)
                originalId = message_response['messages'][0]['context']['id']
                userAnswer = message_response['messages'][0]['button']['payload']
                accept = 'True'
                respond = 0
                print(originalId)
               # print(message_response['messages'][0]['button']['payload'])
                print(userAnswer)
                if userAnswer == 'الغاء الموعد':
                    accept = 'False'
                    respond = 1
                    messenger.send_message(f"تم استلام طلبكم بالغاء الموعد  و سيتم التواصل معكم لتاكيد الالغاء", mobile)
                    r = messenger.send_templatev2("appointment_cancel", "966555862924", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"}]}]', "ar")
                    r = messenger.send_templatev2("appointment_cancel", "966557779388", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"}]}]', "ar")

                elif  userAnswer == "طلب او تعديل موعد":
                      r = messenger.send_templatev2("appointment_request", "966555862924", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"}]}]', "ar")
                      r = messenger.send_templatev2("appointment_request", "966557779388", '[{"type": "body","parameters": [{ "type": "text","text": "'+mobile+'"}]}]', "ar")

                      messenger.send_message(f"شكراً لتواصلكم، تم اخطار مركز الاتصال و سيتم التواصل معكم في اقرب فرصة ", mobile)
                elif  userAnswer == "للحصول على موقع العيادة":
                      messenger.send_location("26.2840119","50.1994742","Medart Clinics","Dhahran Street", mobile )
                elif  userAnswer == "اخر العروض":
                      messenger.send_message(f"يمكنك الحصول على العروض الحاليه من خلال الرابط:", mobile)

                      messenger.send_message(f"https://www.medartclinics.com/ar/khobar-offers-instagram/", mobile)

                else:
                    messenger.send_message(f"شكراً لتأكيدكم الموعد، نتطلع لخدمتكم", mobile)
                    respond = 1
                if(respond > 0):
                    payload = {
                    #'aptId': '' +str(id),
                # 'patId': '' + str(patId),
                #   'dateSent': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                    'waid': originalId,
                    #'mobile': '' + mobile,
                    
                    'responded':'True',
                    'accept': accept
                    }
                    res = requests.post('http://192.168.2.102/whatsappreminders/updateResponse', data=payload)
                    print(res.text)
            else:
                pass
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery} data {data}")
            else:
               print("No new message")
    return "ok" 


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')