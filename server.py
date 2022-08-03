import requests
import os
import json
from heyoo import WhatsApp
from flask import Flask, request
from urllib.parse import unquote
import smtplib, ssl

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
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"

    data = request.get_json()
    
    #print(                message = data['messages'][0]['context']['id'])
 #   print(data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            
            message_type = messenger.get_message_type(data)

            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
            #    print(f"{name} with this {mobile} number sent  {message}")
                #messenger.send_message(f"شكراً لتواصلك مع خدمة الرد الالي بعيادات ميد آرت فرع الخبر", mobile)
                print(messenger.send_template("welcome", mobile,"ar"))

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
            #    print(message_response)

            elif message_type == "button":
                message_response = messenger.preprocess(data)

          #      message_response = messenger.get_message(data)
                originalId = message_response['messages'][0]['context']['id']
                userAnswer = message_response['messages'][0]['button']['payload']
                accept = 'True'
                print(originalId)
               # print(message_response['messages'][0]['button']['payload'])
                print(userAnswer)
                if userAnswer == 'الغاء الموعد':
                    accept = 'False'
                    messenger.send_message(f"تم استلام طلبكم بالغاء الموعود  و سيتم التواصل معكم لتاكيد الالغاء", mobile)
                elif  userAnswer == "طلب او تعديل موعد":
                      messenger.send_message(f"شكراً لتواصلكم، تم اخطار مركز الاتصال و سيتم التواصل معكم في اقرب فرصة ", mobile)
                      text = "Appointment Request : " + mobile
                      whom = 'Sara2006!'
                      port = 465  
                      context = ssl.create_default_context()
                      with smtplib.SMTP_SSL("smtp.banderjumah.com", port, context=context) as server:
                          server.login("bander@medartclinics.com", whom)
                          server.sendmail('bander@medartclinics.com', 'contact-kh@medartclinics.com', text)

                elif  userAnswer == "للحصول على موقع العيادة":
                      messenger.send_location("26.2840119","50.1994742","Medart Clinics","Dhahran Street", mobile )
                elif  userAnswer == "اخر العروض":
                      messenger.send_message(f"يمكنك الحصول على العروض الحاليه من خلال الرابط:", mobile)

                      messenger.send_message(f"https://www.medartclinics.com/ar/khobar-offers-instagram/", mobile)

                else:
                    messenger.send_message(f"شكراً لتأكيدكم الموعد، نتطلع لخدمتكم", mobile)

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
                print(f"Message : {delivery}")
            else:
               print("No new message")
    return "ok" 


if __name__ == "__main__":
    app.run(port=5000)