from fbchat import log, Client
from fbchat.models import *
import requests
import json

# To do: Weather, Time, Reminder (to do), 
# Subclass fbchat.Client and override required methods

addresses = {}
got_login = 0

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
        if 'botule' in message_object.text.lower() and 'vremea' in message_object.text.lower():
                cere_vremea = 1
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

client = Bot("mralgadoro@yahoo.com", "Blackreaper1999")
client.listen()
