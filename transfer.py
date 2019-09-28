from flask import Flask, make_response, request, jsonify
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/webhook')
def hello():
    return 'Hello World!'

def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')
    para = req.get('queryResult').get('parameters')


    if action == "Get_alltime":
        url = "http://127.0.0.1:8888/Dentist"
        r = requests.get(url)
        json_r = r.json()
        textall = ''
        for i in json_r:
            print(i)
            freetime = ''
            if i['9'] == 0:
                freetime += ' 9:00-10:00'
            if i['10'] == 0:
                freetime += ' 10:00-11:00'
            if i['11'] == 0:
                freetime += ' 11:00-12:00'
            if i['12'] == 0:
                freetime += ' 12:00-13:00'
            if i['13'] == 0:
                freetime += ' 13:00-14:00'
            if i['14'] == 0:
                freetime += ' 14:00-15:00'
            if i['15'] == 0:
                freetime += ' 15:00-16:00'
            if i['16'] == 0:
                freetime += ' 16:00-17:00'
            textall = textall +i['name']+' is available during the following time period：'+freetime + '.' + '\n\n'

        return {'fulfillmentText': textall}






    if action == "Get_dentistinfo":
        name = para['dentistname']


        url = "http://127.0.0.1:8888/GetDentistinfo/" + name
        r = requests.get(url)
        json_r = r.json()

        text1 = "Dr." + json_r['name'] + ' is working at ' + json_r['location'] + ', and the specialization is ' + json_r['specialization']


        return {'fulfillmentText':text1 + ".Type dentist's name combined with 'timetable' to know this dentist's time. "}

    if action == "get_dentisttime":
        name = para['dentistname']

        url = "http://127.0.0.1:8888/Gettimeslotsofdentist/" + name
        r = requests.get(url)
        json_r = r.json()

        freetime =''
        if json_r['9'] == 0:
            freetime += ' 9:00-10:00'
        if json_r['10'] == 0:
            freetime += ' 10:00-11:00'
        if json_r['11'] == 0:
            freetime += ' 11:00-12:00'
        if json_r['12'] == 0:
            freetime += ' 12:00-13:00'
        if json_r['13'] == 0:
            freetime += ' 13:00-14:00'
        if json_r['14'] == 0:
            freetime += ' 14:00-15:00'
        if json_r['15'] == 0:
            freetime += ' 15:00-16:00'
        if json_r['16'] == 0:
            freetime += ' 16:00-17:00'


        return {'fulfillmentText':"Dr. "+json_r['name']+' is available during the following time period：'+freetime +
                '.Simply type "book+dentistname+timeslot". For example, type"book Mike 9" to book Dr Mike from 9:00 to 10:00am'}

    if action == "Get_reserve":
        print(para)


        url = "http://127.0.0.1:8888/Reserve/" + para['dentistname'] + '/' + para['timenumber']
        r = requests.get(url)
        json_r = r.json()
        print(json_r)
        booktime =''
        if para['timenumber']=='9':
            booktime = '9:00-10:00'
        if para['timenumber']=='10':
            booktime = '10:00-11:00'
        if para['timenumber']=='11':
            booktime = '11:00-12:00'
        if para['timenumber']=='12':
            booktime = '12:00-13:00'
        if para['timenumber']=='13':
            booktime = '13:00-14:00'
        if para['timenumber']=='14':
            booktime = '14:00-15:00'
        if para['timenumber']=='15':
            booktime = '15:00-16:00'
        if para['timenumber']=='16':
            booktime = '16:00-17:00'


        return {'fulfillmentText':'You have successfully booked Dr.' + para['dentistname'] + ' from ' + booktime}

    if action == "Cancel_dentisttime":
        print(para)


        url = "http://127.0.0.1:8888/Cancel/" + para['dentistname'] + '/' + para['timenumber']
        r = requests.get(url)
        json_r = r.json()
        print(json_r)
        booktime =''
        if para['timenumber']=='9':
            booktime = '9:00-10:00'
        if para['timenumber']=='10':
            booktime = '10:00-11:00'
        if para['timenumber']=='11':
            booktime = '11:00-12:00'
        if para['timenumber']=='12':
            booktime = '12:00-13:00'
        if para['timenumber']=='13':
            booktime = '13:00-14:00'
        if para['timenumber']=='14':
            booktime = '14:00-15:00'
        if para['timenumber']=='15':
            booktime = '15:00-16:00'
        if para['timenumber']=='16':
            booktime = '16:00-17:00'


        return {'fulfillmentText': 'You have successfully Cancelled the appointment with Dr.'
                                   + para['dentistname'] + ' from ' + booktime}



# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run(debug=True, port=5051)