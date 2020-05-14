from fbchat import log, Client
from fbchat.models import *
import requests
import json


# To do: Weather, Time, Reminder (to do), 
# Subclass fbchat.Client and override required methods
class Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

#         log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        user_id = message_object.author
        
        # If you're not the author, echo
        if author_id != self.uid:
#             self.send(message_object, thread_id=thread_id, thread_type = thread_type)
            thread_id_Bianca = '100003009160741'
            thread_id_Alex = '100000904110441'
            
            cere_vremea = 0
            
            if 'botule' in message_object.text.lower() and 'vremea' in message_object.text.lower():
                cere_vremea = 1
#                 self.send(Message(text = 'E cald afara'), thread_id = thread_id_Alex, thread_type = thread_type)
#                 self.send(Message(text = 'E cald afara'), thread_id = thread_id_Bianca, thread_type = thread_type)
            
            if thread_id == thread_id_Bianca:
                message_object.text = "Bianca - " + message_object.text
                self.send(message_object, thread_id = thread_id_Alex , thread_type = thread_type)
                if cere_vremea == 1:
                    oras = message_object.text.strip('?').split('la ')[1]
                    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + oras + "&appid=d00e3b645e7b14cceb37659193a27d72")
                    data = json.loads(response.text)
                    temp = data['main']['temp']
                    temp = temp - 273.15
                    self.send(Message(text = 'Sunt ' + str(temp) + ' grade la ' + oras), thread_id = thread_id_Alex, thread_type = thread_type)
                    self.send(Message(text = 'Sunt ' + str(temp) + ' grade la ' + oras), thread_id = thread_id_Bianca, thread_type = thread_type)
            else:
                message_object.text = "Alex - " + message_object.text
                self.send(message_object, thread_id = thread_id_Bianca , thread_type = thread_type)
                if cere_vremea == 1:
                    oras = message_object.text.strip('?').split('la ')[1]
                    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + oras + "&appid=d00e3b645e7b14cceb37659193a27d72")
                    data = json.loads(response.text)
                    temp = data['main']['temp']
                    temp = temp - 273.15
                    self.send(Message(text = 'Sunt ' + str(temp) + ' grade la ' + oras), thread_id = thread_id_Alex, thread_type = thread_type)
                    self.send(Message(text = 'Sunt ' + str(temp) + ' grade la ' + oras), thread_id = thread_id_Bianca, thread_type = thread_type)

client = Bot("email", "password")
client.listen()