from fbchat import log, Client
from fbchat.models import *
import requests
import json
import calendar
from flask import Flask
from flask import request

# To do: Time, Reminder (to do), 

#{
#    '100003009160741' : ['Alex', calendar]  
#}

# Login -> toate de pana acum
# Logout -> te sterge din dictionar

# Calendar
# E1 (15 iulie 2020): Examen BD
# E2 (): Examen

app = Flask(__name__)

@app.route('/MDS')
def calendar(): 
    name = request.args.get('name', None)
    '''
    text_cal = calendar.HTMLCalendar(firstweekday = 0)
    year = 2020
    month = 7
    dict = {'Examen Tap' : '26 iulie'}
    return text_cal.formatmonth(year, month) + "Evenimente: " + str(dict)
    '''
    return name

addresses = {}
got_login = 0 # Only one login at the time (daca mai multi se logheaza in acelasi timp crapa)

addresses = {}
got_login = 0 # Only one login at the time (daca mai multi se logheaza in acelasi timp crapa)

class Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        global got_login
        global addresses
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        
        if author_id != self.uid:
            if author_id not in addresses:
                if got_login == 0:
                    self.send(Message(text = "Salut! Nu stiu inca cum te cheama. Care este numele tau?"), thread_id = author_id, thread_type = thread_type)
                    got_login = 1
                elif got_login == 1:
                    got_login = 0
                    name = message_object.text
                    addresses[author_id] = name
                    for address in addresses:
                        self.send(Message(text = name + ' a intrat pe server! Hai sa-l salutam'), thread_id = address, thread_type = thread_type)
            else:
                cere_vremea = 0
                cere_calendar = 0
                if 'botule' in message_object.text.lower() and 'vremea' in message_object.text.lower():
                    cere_vremea = 1
                if 'botule' in message_object.text.lower() and 'calendar' in message_object.text.lower():
                    cere_calendar = 1
                for address in addresses:
                    if address != author_id:
                        self.send(Message(text = addresses[author_id] + ' - ' + message_object.text), thread_id = address, thread_type = thread_type)
                if cere_vremea == 1:
                    oras = message_object.text.strip('?').split('la ')[1]
                    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + oras + "&appid=d00e3b645e7b14cceb37659193a27d72")
                    data = json.loads(response.text)
                    temp = data['main']['temp']
                    temp = temp - 273.15
                    for address in addresses:
                        self.send(Message(text = 'Sunt ' + str(temp) + ' grade la ' + oras), thread_id = address, thread_type = thread_type)
                if cere_calendar = 1:
                    app.run(host = '0.0.0.0', port = 443)
                    url = 'http://107.23.107.21:443/MDS?name=' + addresses[author_id]
                    self.send(Message(text = url), thread_id = author_id, thread_type = thread_type)
                    
email = input("email: ")
password = input("password: ")
client = Bot(email, password)
client.listen()
