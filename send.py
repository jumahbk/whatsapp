
from flask import Flask,request,json
from heyoo import WhatsApp


def send_message(message):
    messenger = WhatsApp('EAAHlPsvlZAjABAHIlcbZBmztdo4IeaIqIW97Ug2ZALUnnlWBqbDMvzkxQiOrdcWFNZAcDGZCuUVGvo3zXH8sphJOWn1aZA3nDxhRrq6k10fOMkvnSQeOkwNrsrUdZA11zduKZCZCUN0t5udkTv4LZBysAT17zSgZBcKOeglQTt1rtxSKrsrNjWUpxD0',  phone_number_id='103290435735343')
    resposne = messenger.send_reply_button(
        recipient_id="966555862924",
        button={
            "type": "button",
            "body": {
                "text": "This is a test button"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "This is button 1"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "this is button 2"
                        }
                    }
                ]
            }
      },
    )





app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
       return 'ok'
    else:
        return 'ok'
 
if __name__ == '__main__':

    app.run(port=5001)







# from heyoo import WhatsApp
# messenger = WhatsApp('EAAHlPsvlZAjABAPGe9xuyCqBcMTRJUZBTvc69Sdtp2PumWNeTC2IFYvG1hKqMZAyxDkxpvDRIEgsyBPoG0M60MZBKx6hVfCbMR6V2ufTc15H128D8klrtvrJZAeCyuQ7ZAnSDk8JbC9sTAk9ieZCH9K77G9C56qj6DpDqQ9QEkcY2w8BSi6oAcHYKz5Y6CSlSgTniMJQzv3yAZDZD',  phone_number_id='103290435735343')
# resposne = messenger.send_reply_button(
#         recipient_id="966555862924",
#         button={
#             "type": "button",
#             "body": {
#                 "text": "This is a test button"
#             },
#             "action": {
#                 "buttons": [
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "b1",
#                             "title": "This is button 1"
#                         }
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "b2",
#                             "title": "this is button 2"
#                         }
#                     }
#                 ]
#             }
#       },
#     )
# print(resposne);
