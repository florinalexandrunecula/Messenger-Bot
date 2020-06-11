import calendar
from flask import Flask
from flask import request
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/Calendar')
def calendar_user():
    name = request.args.get('name', None)
    dictionary = request.args.get('dict', None)
    dicti = json.loads(dictionary)
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    text_cal = calendar.HTMLCalendar(firstweekday = 0)
    year = currentYear
    month = currentMonth
    
    items = dicti.items()

    if len(items) > 0:
        param = "Evenimente: <br/>"
        for item in items:
            param += f" La data de {item[0]} aveti urmatoarele examene: "

            for exam in item[1]:
                param += f"{exam}, "
            param += "<br/>"
    else:
        param = "Nu aveti evenimente in aceasta luna<br/>"

    
    return text_cal.formatmonth(year, month) + param

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 443)
