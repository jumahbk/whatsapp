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
def send_message(message, keytoken, dayname, time, date, morning, mobile):
    fullTime = str(time) + ' ' + morning
    response = requests.get('https://www.medartclinics.com/tttt.bin')
    messenger = WhatsApp(keytoken,  phone_number_id='105367738941421')
    r = messenger.send_templatev2("appointment_remainder", mobile, '[{"type": "body","parameters": [{ "type": "text","text": "'+fullTime+'"}, { "type": "text","text": "'+dayname+'"},{ "type": "text","text": "'+str(date)+'"}]}]', "ar")
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
       date = request.args.get('aptDate')
      # print(date)
       
       send_message('test1',keytoken)
       return 'ok'
    else:
       aptId = request.args.get('aptid')
       r = requests.get('http://192.168.2.102/appointments/?aptId='+str(aptId))
       data = r.json()
       print(data[0]['id'])
       index = 1
       for c in data:
           id = c['id']
           dayDate = c['appDate']

           dayDate = dayDate.replace("T", " ")
           time = c['fromTime']
           time = time.replace("T", " ")
           mobile = c['mobile']
           patId = c['patientId']
       #    print(str(c['id']))
           date_object = datetime.strptime(dayDate, '%Y-%m-%d %H:%M:%S')
           time_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
           dayIndex = date_object.weekday()
           isPm = time_object.strftime("%I:%M %p").endswith('PM')
           morning = 'صباحاً'
           if(isPm):
            morning = 'مساءً'

           payload = {
                'aptId': '' +str(id),
                'patId': '' + str(patId),
                'dateSent': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                'waid': '1',
                'mobile': '' + mobile,
                
                'respond':'0',
                'accept':'0'
            }
           res = requests.post('http://192.168.2.102/whatsappreminders/isDuplicate', data=payload)
           if index == 500:
            return 'done'
           index = index + 1
           if res.text.find("Dup") > -1:
                print("Continue")
           else:
             #   d = send_message('test2',keytoken, days[dayIndex], time_object.strftime("%H:%M"), date_object.date(),morning, mobile )
                payload['waid']= d
                res = requests.post('http://192.168.2.102/whatsappreminders/create', data=payload)
                print(payload)
       return "Done"
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

    app.run(port=9000)
