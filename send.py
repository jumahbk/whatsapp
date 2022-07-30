import requests
from flask import Flask,request,json
from heyoo import WhatsApp
from urllib.parse import unquote
from datetime import datetime

response = requests.get('https://www.medartclinics.com/tttt.bin')

days = [
'الأثنين',
'الثلاثاء',
'الاربعاء',
'الخميس',
'الجمعة',
'السبت'
'الأحد'
]


keytoken = unquote(requests.get('https://www.medartclinics.com/tttt.bin').text)
def send_message(message, keytoken, dayname, time, date, morning):
    fullTime = str(time) + ' ' + morning
    response = requests.get('https://www.medartclinics.com/tttt.bin')
    messenger = WhatsApp(keytoken,  phone_number_id='103290435735343')
    r = messenger.send_templatev2("appointment_remainder", "966555862924", '[{"type": "body","parameters": [{ "type": "text","text": "'+fullTime+'"}, { "type": "text","text": "'+dayname+'"},{ "type": "text","text": "'+str(date)+'"}]}]', "ar")
    print(r)
    





app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
       date = request.args.get('aptDate')
       print(date)
       
       send_message('test1',keytoken)
       return 'ok'
    else:
       r = requests.get('http://192.168.2.102/appointments')
       data = r.json()
       print(data[0]['id'])
       for c in data:
           id = c['id']
           dayDate = c['appDate']
           dayDate = dayDate.replace("T", " ")
           time = c['fromTime']
           time = time.replace("T", " ")
           mobile = c['mobile']
           patId = c['patientId']
           print(str(c['id']))
           date_object = datetime.strptime(dayDate, '%Y-%m-%d %H:%M:%S')
           time_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
           isPm = time_object.strftime("%I:%M %p").endswith('PM')
           morning = 'صباحاً'
           if(isPm):
            morning = 'مساءً'
           send_message('test2',keytoken, days[0], time_object.strftime("%H:%M"), date_object.date(),morning )
       return str(r.json())
       # date = request.args.get('$aptDate')
       # print('Hello=')
       # print(date)
       # datetime_object = datetime.strptime(date, '%d/%m/%y %H:%M')
       # print(datetime_object.weekday())
       # print(days[datetime_object.weekday()])
      #  isPm = datetime.today().strftime("%I:%M %p").endswith('PM')
      #  print('is PM')
      #  morning = 'صباحاً'
      #  if(isPm):
      #      morning = 'مساءً'
       # print(isPm)
       # send_message('test2',keytoken, days[datetime_object.weekday()], datetime_object.strftime("%H:%M"), datetime_object.date(),morning )
        # 'ok'
 
if __name__ == '__main__':

    app.run(port=5001)
