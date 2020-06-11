import calendar
from flask import Flask
from flask import request
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/Calendar')
def calendar(): 
    name = request.args.get('name', None)
    dictionary = request.args.get('dict', None)
    dictionary = json.loads(dictionary)
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    text_cal = calendar.HTMLCalendar(firstweekday = 0)
    year = currentYear
    month = currentMonth
    return text_cal.formatmonth(year, month) + "Evenimente: " + dictionary

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 443)
