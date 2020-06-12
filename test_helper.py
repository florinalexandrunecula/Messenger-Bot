import pyshorteners

class User():
    def __init__(self, id="", name="", calendar_link="", calendar={}):
        self.id = id
        self.name = name
        self.calendar_link = calendar_link
        self.calendar = calendar

    def add_event(self, event_name, date):
        if date in self.calendar:
            self.calendar[date].append(event_name)
        else:
            self.calendar[date] = [event_name]

    def set_name(self, name):
        self.name = name


users = [User(123, 'cami')]


def cere_calendar(author_id):
    url = 'http://ec2-107-23-107-21.compute-1.amazonaws.com:443/Calendar?name=' + get_user(
        author_id).name + '&dict=' + str(get_user(author_id).calendar).replace('\'', "\"").replace(' ', '')
    s = pyshorteners.Shortener()
    generated_link = s.tinyurl.short(url)
    return generated_link



def get_user(id):
    for user in users:
        if user.id == id:
            return user

def change_nickname(author_id, target_user, nickname):
    target_user.set_name = nickname

    if author_id == target_user.id:
        message = text = f"Ti-ai schimbat numele in {nickname}"
    else:
        message = text = f"{get_user(author_id).name} ti-a schimbat numele in {nickname}"

    return message

def add_even(event_name, date, user):
    user.add_event(event_name, date)

def logoutUser(author_id):
    global users
    user = get_user(author_id)
    name = user.name
    users.remove(user)
    message = name + ' a parasit conversatia'
    return message


def loginUser( author_id, message_object):
    global users
    global got_login

    got_login = True
    if not got_login:
        message = "Salut! Nu stiu inca cum te cheama. Care este numele tau?"
        got_login = True

    elif got_login:
        got_login = False
        name = message_object
        user = User(id=author_id, name=name)
        users.append(user)
        message = name + ' a intrat pe server! Hai sa-l salutam'

    return message