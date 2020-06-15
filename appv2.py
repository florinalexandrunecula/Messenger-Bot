from fbchat import log, Client
from fbchat.models import *
import requests
import json
import calendar
from flask import Flask
from flask import request
import pyshorteners

users = []
got_login = 0  # Only one login at the time (daca mai multi se logheaza in acelasi timp crapa)


class User():
    
    
    def __init__(self, id="", name="", calendar_link="", calendar={}):
        '''
        initializam un obiect de tip user, 
        folosind argumentele date
        Argumente:
                    id -> id-ul user-ului
                    nume -> numele user-ului
                    calendar_link -> link-ul catre pagina calendarului
                    calendar -> calendarul care initial nu contine niciun eveniment
        '''
        self.id = id
        self.name = name
        self.calendar_link = calendar_link
        self.calendar = calendar

    def add_event(self, event_name, date):
        '''
        Argumente: event_name -> numele evenimentului
                   date -> data evenimentului
        
        '''
        
        
        if date in self.calendar:
            # daca data aleasa exista, adaugam evenimentul
            self.calendar[date].append(event_name)
        else:
            # daca data aleasa nu exista o adaugam impreuna cu evenimentul
            self.calendar[date] = [event_name]
            
    def set_name(self, name):
        self.name = name



def get_addresses():
    ''' 
        returneaza un array care contine
        toate id-urile utilizatorilor
    '''
    addresses = []
    for user in users:
        addresses.append(user.id)

    return addresses


def get_user(id):
    '''
        returneaza user-ul avand id-ul id, dat ca parametru 
    
    '''
    for user in users:
        if user.id == id:
            return user


def get_user_by_name(name):
    '''
        returneaza user-ul avand numele name, dat ca parametru 
    
    '''
    for user in users:
        if user.name.lower() == name:
            return user
        return -1


class Bot(Client):

    
    def change_nickname(self, author_id, target_user, nickname):
        '''
        Aceasta functie este apelata atunci cand userul cu id-ul author_id
        schimba numele user-ului target_user
        
        schimba nickname-ul  userului care
        
        Argumente: author_id -> id-ul userului care schimba 
                   target_user ->userul al carui nume este schimbat
                   nickname -> noul nume
        '''
        
        target_user.set_name(nickname)
    
        # stabilim, in functie de cine schimba numele, ce mesaj trebuie afisat in conversatie
        if author_id == target_user.id:
            
            message = text = f"Ti-ai schimbat numele in {nickname}"
        else:
            message = text = f"{get_user(author_id).name} ti-a schimbat numele in {nickname}"

        # mesajul este trimis catre user-ul al carui nume a fost schimbat 
        self.send(Message(text=message), thread_id=target_user.id, thread_type=ThreadType.USER)

    def send_all(self, message, author_id=""):
        '''
        Mesajul 'message' este trimis catre toti userii, cu exceptia 
        celui cu id-ul author_id
        
        Argumente: message -> mesajul care trebuie trimis
                    author_id -> id-ul userului caruia nu-i este trimis mesajul
                    
        '''
        for user in users:
            if user.id != author_id:
                
                self.send(Message(text=message), thread_id=user.id, thread_type=ThreadType.USER)

            
    def change_color(self, color, author_id):
        
        '''
        In cadrul acestei functii este schimbata culoarea conversatiei 
        a userului cu id-ul author_id, astfel fiecare user isi poate alege culoarea dorita
        
        Argumente: author_id -> id-ul user-ului care doreste schimbarea
                             -> textul introdus de user care contine culoarea dorita
        
        '''
       
        # verificam culoarea pe care acesta o doreste
        if 'red' in color.lower():
            self.changeThreadColor(ThreadColor.RADICAL_RED, thread_id=author_id)
        elif 'blue' in color.lower():
            print("yessss")
            self.changeThreadColor(ThreadColor.MESSENGER_BLUE, thread_id=author_id)
        elif 'orange' in color.lower():
            self.changeThreadColor(ThreadColor.PUMPKIN, thread_id=author_id)
        elif 'coral' in color.lower():
            self.changeThreadColor(ThreadColor.LIGHT_CORAL, thread_id=author_id)
        elif 'rose' in color.lower():
            self.changeThreadColor(ThreadColor.BRILLIANT_ROSE, thread_id=author_id)




    
    def cere_vremea(self, message_object):
        
        '''
        Sunt trimise informatii despre vremea dintr-un oras cerut.
        
        Argumente: message_object -> mesajul trimis de user pentru a cere informatii despre vreme
        MESAJUL ar trebui sa fie de forma "botule... vremea.. la ORAS "
        
        
        
        '''

        # preluam orasul tinta
        oras = message_object.text.strip('?').split('la ')[1]
        
        # request la site pentru a prelua informatii despre vreme
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=" + oras + "&appid=d00e3b645e7b14cceb37659193a27d72")
        data = json.loads(response.text)
        
        # extragem temperatura
        temp = data['main']['temp']

        # aproximam temperatura la 2 zecimale
        temp = round(temp - 273.15, 2)
        
        # trimitem informatiile obtinute tuturor utilizatorilor
        for address in get_addresses():
            self.send(Message(text=f"Sunt {str(temp)} grade la {oras}"), thread_id=address, thread_type=ThreadType.USER)

            
    def cere_calendar(self, author_id):
        '''
        Arguments: author_id -> id-ul user-ului care cere calendarul cu evenimente
        
        Este trimis user-ului care cere calendarul, un link care duce catre
        afisarea calendarului lunii curente impreuna cu evenimentele adaugate de el pana atunci
        
        
        '''
        
        # formarea link-ului
        url = 'http://ec2-107-23-107-21.compute-1.amazonaws.com:443/Calendar?name=' + get_user(
            author_id).name + '&dict=' + str(get_user(author_id).calendar).replace('\'', "\"").replace(' ', '')
        
        # comprimarea link-ului
        s = pyshorteners.Shortener()
        generated_link = s.tinyurl.short(url)
        
        # trimiterea link-ului 
        self.send(Message(text=generated_link), thread_id=author_id, thread_type=ThreadType.USER)

    def add_event(self, event_name, date, user):
        ''' adaugarea unui eveniment de la o anumita data in calendarul unui user
        
            Argumente:
                    event_name -> numele evenimentului
                    date -> data evenimentului
                    user -> userul care adauga in calendar acest eveniment 
        '''
        user.add_event(event_name, date)

    def loginUser(self, author_id, message_object):
        
        '''
        Functia de login are rolul de a adauga un nou utilizator 
        in lista de utilizatori 
        
        Argumente:
            author_id -> id-ul asociat user-ului
            message_object -> mesajul trimis de acesta dupa login
        
        '''
        
        global users
        global got_login
        
        
        # user-ul a trimis un mesaj dar acesta este nou in conversatie
        if not got_login:
            
            # trimitem user-ului un mesaj de bun venit
            message = "Salut! Nu stiu inca cum te cheama. Care este numele tau?"
            self.send(Message(text=message), thread_id=author_id, thread_type=ThreadType.USER)
            got_login = True

        # user-ul este la al doilea mesaj trimis, care reprezinta numele sau
        elif got_login:

            
            got_login = False
            
            # preluam numele
            name = message_object.text
            
            # cream un user nou
            user = User(id=author_id, name=name)
            
            # il adaugam in lista de utilizatori
            users.append(user)
            
            # trimitem tuturor utilizatorilor inafara de acesta,
            # ca respectivul user a intrat in conversatie
            message = name + ' a intrat pe server! Hai sa-l salutam'
            self.send_all(message=message)


    def logoutUser(self, author_id):
        '''
        Prin aceasta functie eliminam din lista utilizatorilor, 
        user-ul care vrea sa iasa din conversatie
        
        Argumente: author_id -> id-ul user-ului care iese din conversatie
        
        '''
        global users
        
        # extragem userul cu id-ul respectiv
        user = get_user(author_id)
        name = user.name
        
        # il stergem din lista de utilizatori
        users.remove(user)
        
        # trimitem tuturor utilizatorilor ca acesta a parasit conversatia
        message = name + ' a parasit conversatia'
        self.send_all(message=message, author_id=author_id)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        
        '''
        Aceasta functie este apelata la trimiterea unui mesaj din partea unui utilizator
        
        Fiecarui utilizator ii este asociat un id (author_id)
        '''
        
        global addresses
        global users
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        if author_id != self.uid:
            
            # verificam daca user-ul se afla deja printre cei conectati
            
            if author_id not in get_addresses():
                # nu se afla deci trebuie sa-si faca login
                
                self.loginUser(author_id, message_object)

            else:
                
                # daca user-ul se afla deja in conversatie, mesajul lui va fi trimis catre toti ceilalti utilizatori
                self.send_all(message=get_user(author_id).name + " -> " + message_object.text, author_id=author_id)
                
                cere_vremea = False
                cere_calendar = False
                cere_logout = False
                change_nickname = False
                change_color = False


                # in functie de ce mesaj a dat user-ul, stabilim ce trebuie sa-i raspunda bot-ul
                if 'botule' in message_object.text.lower() and 'vremea' in message_object.text.lower():
                    ''' botule ..vremea .. la ORAS'''
                    # user-ul cere informatii despre vreme
                    cere_vremea = True
                    
                if 'botule' in message_object.text.lower() and 'calendar' in message_object.text.lower():
                    '''botule ... calendar '''
                    # user-ul cere informatii despre calendar
                    cere_calendar = True

                if 'botule' in message_object.text.lower() and 'logout' in message_object.text.lower():
                    '''botule .... logout'''
                    # user-ul vrea sa iasa din conversatie
                    cere_logout = True

                if 'botule' in message_object.text.lower() and 'eveniment' in message_object.text.lower():
                    '''botule ... eveniment .. data=DATA_EVENIMENT ... nume=NUME_EVENIMENT'''
                    # user-ul vrea sa adauge evenimente in calendar
                    cere_adauga_eveniment = True
                    
                    # extragem data si evenimentul
                    sir = message_object.text.lower()
                    sir2 = message_object.text.lower()
                    
                    data = sir.split('data=')
                    nume = sir.split('nume=')
                    
                    data = data[1].split(" ")
                    data2 = data[0] + data[1]
                    nume = nume[1]
                    
                    # adaugam evenimentul in calendar
                    self.add_event(nume, data2, get_user(author_id))

                # botule schimba nickname bianca new_nick
                if 'botule' in message_object.text.lower() and 'nickname' in message_object.text.lower():
                    '''botule .... nickname target_user NEW_NI'''
                    change_nickname = True

                    substring = message_object.text.split("nickname ")

                    # extragem numele user-ului caruia vrem sa-i schimbam numele
                    name = substring[1].split(" ")[0]
                    
                    # extragem porecla pe care vrem sa i-o dam 
                    nickname = substring[1].split(" ")[1]
                    
                    # gasim user-ul avand numele cautat
                    target = get_user_by_name(name.lower())
                    if target != -1:
                        self.change_nickname(author_id, target, nickname)
                    else:
                        # daca nu exista, trimitem celui care a initiat aceasta actiune, ca nu exista user-ul
                        self.send(Message(text="Userul ales nu exista"), thread_id=author_id,
                                  thread_type=ThreadType.USER)

                if 'botule' in message_object.text.lower() and 'new color' in message_object.text.lower():
                    ''' botule ... new color rose
                                             blue
                                             orange
                                             red
                                             coral
                    '''
                    
                    change_color = True
                    
                    # extragem textul corespunsator
                    color = message_object.text.split("new color ")[1]
                    self.change_color(color, author_id)
                    

                if cere_vremea:
                    self.cere_vremea(message_object)
                elif cere_calendar:
                    self.cere_calendar(author_id, thread_type)
                elif cere_logout:
                    self.logoutUser(author_id)


# email = input("email: ")
# password = input("password: ")

email = 'email'
password = 'password'
client = Bot(email, password)
client.listen()
