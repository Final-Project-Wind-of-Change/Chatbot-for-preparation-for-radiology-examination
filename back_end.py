import json


from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse

import time
import requests
import operator

from pymongo import MongoClient



###################################################


app = Flask(__name__)
api = Api(app,
          default="Dentist timeslot",  # Default namespace
          title="Dentist appointment",  # Documentation Title
          description="This is assignment1 of COMP9322.")  # Documentation Description

dentist_model = api.model('Dentist', {
    'name': fields.String,
    'location': fields.String,
    'specialization': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('order', choices=list(column for column in dentist_model.keys()))



@api.route('/Dentist')
class DentistsList(Resource):
    @api.response(201, 'Created')
    @api.response(200, 'OK')
    @api.response(404, 'Error')
    @api.doc(description="This is a default setting to add dentist information, customers cannot access this part.")
    @api.expect(dentist_model, validate=True)
    def post(self):
        dentist = request.json
        collection_id = dentist['name'] + '_information'

        client = MongoClient(host=mongo_host, port=mongo_port)
        db = client[db_name]

        cidlist = db.list_collection_names()
        if collection_id in cidlist:
            return {"location": "/collections/{}".format(collection_id)}, 200
        # check if the given identifier does not exist

        format_col = {}
        format_col['collection_id'] = dentist['name'] + '_information'  # problem with collection_id, how to create it automatically
        format_col['name'] = dentist['name']
        format_col['location'] = dentist['location']
        format_col['specialization'] = dentist['specialization']
        format_col['9'] = 0
        format_col['10'] = 0
        format_col['11'] = 0
        format_col['12'] = 0
        format_col['13'] = 0
        format_col['14'] = 0
        format_col['15'] = 0
        format_col['16'] = 0
        format_col['17'] = 0
        # Create formatted collections

        c = db[collection_id]
        c.insert_many([format_col])
        # Store formatted collections in the mlab.

        # 6.Return location, collection_id, creation_time, indicator
        return {"location": "/collections/{}".format(collection_id),
                "collection_id": "{}".format(collection_id),
                "creation_time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time.time())),
                "name": "{}".format(dentist['name'])}, 201


    @api.response(200, 'OK')
    @api.doc(description="This part is to give all avialable timeslots of every dentists.Retrieve the list of all available dentists")
    def get(self):
        client = MongoClient(host=mongo_host, port=mongo_port)
        db = client[db_name]

        cidlist = db.list_collection_names()
        dontlike = ['objectlabs-system.admin.collections', 'system.indexes', 'objectlabs-system']
        cidlist2 = []
        for i in cidlist:
            if i not in dontlike:
                cidlist2.append(i)

        l = []
        for collection_id in cidlist2:
            c = db[collection_id]
            list1 = list(c.find())
            list2 = list1[0]
            del list2['_id']
            del list2['collection_id']
            l.append(list2)
        return l, 200


@api.route('/GetDentistinfo/<string:id>')
@api.param('id', 'The name of dentist')
class Dentists(Resource):
    @api.response(404, 'Collection was not found')
    @api.response(200, 'Successful')
    @api.doc(description="To give dentist's information about location and specialization by dentist's name.")
    def get(self, id):
        collection_id = id + '_information'
        client = MongoClient(host=mongo_host, port=mongo_port)
        db = client[db_name]

        try:
            c = db[collection_id]
            list1 = list(c.find())
            list2 = list1[0]
            dentist_info = {}
            dentist_info['name'] = list2['name']
            dentist_info['location'] = list2['location']
            dentist_info['specialization'] = list2['specialization']
            return dentist_info, 200
        except IndexError:
            return "Collection was not found.", 404

@api.route('/Gettimeslotsofdentist/<string:id>')
@api.param('id', 'The collection identifier')
class Timeslots(Resource):
    @api.response(404, 'Collection was not found')
    @api.response(200, 'Successful')
    @api.doc(description="To give available timeslots of specific dentist by dentist's name.")
    def get(self, id):
        collection_id = id + '_information'
        print(collection_id)

        client = MongoClient(host=mongo_host, port=mongo_port)
        db = client[db_name]

        try:
            c = db[collection_id]
            list1 = list(c.find())
            list2 = list1[0]
            del list2['_id']
            del list2['location']
            del list2['specialization']
            del list2['collection_id']
            return list2, 200
        except IndexError:
            return "Collection was not found.", 404

@api.route('/Reserve/<string:id>/<string:timeslot>')
@api.param('id', 'The name of dentist')
@api.param('timeslot', 'the timeslot')
class Timeslots(Resource):
    @api.response(404, 'Collection was not found.')
    @api.response(200, 'OK')
    @api.doc(description="To reserve a timeslot of specific dentist by dentist's name and timeslot number.")
    def get(self, id, timeslot):

        collection_id = id + '_information'
        client = MongoClient(host=mongo_host, port=mongo_port)
        db = client[db_name]

        try:
            c = db[collection_id]
            list1 = list(c.find())
            list2 = list1[0]
            del list2['_id']

        except IndexError:
            return "Collection was not found.", 404
        #get info

        c = db[collection_id]
        c.drop()
        #delete info
        timeslot = str(timeslot)

        timenumber = timeslot
        list2[timenumber] = 1
        c = db[collection_id]
        c.insert_many([list2])
        #post new info


        return {"name": "Dr.{}".format(id),
                "time":"{}".format(timeslot)}, 200


@api.route('/Cancel/<string:id>/<string:timeslot>')
@api.param('id', 'The name of dentist')
@api.param('timeslot', 'the timeslot')
class Timeslots(Resource):
    @api.response(404, 'Collection was not found.')
    @api.response(200, 'OK')
    @api.doc(description="To cancel a timeslot of specific dentist by dentist's name and timeslot number.")
    def get(self, id, timeslot):

        collection_id = id + '_information'
        client = MongoClient(host=mongo_host, port=mongo_port)
        db = client[db_name]

        try:
            c = db[collection_id]
            list1 = list(c.find())
            list2 = list1[0]
            del list2['_id']
        except IndexError:
            return "Collection was not found.", 404
        #get info


        c = db[collection_id]
        c.drop()
        #delete info

        timenumber = str(timeslot)
        list2[timenumber] = 0
        c = db[collection_id]
        c.insert_many([list2])
        #post new info


        return {"name": "Dr.{}".format(id),
                "time":"{}".format(timeslot)}, 200



if __name__ == '__main__':
    db_name = 'k_database'
    mongo_port = 25912
    mongo_host = 'mongodb://Zanlai:hzl13579@ds125912.mlab.com:25912/k_database'

    # run the application
    app.run(debug=True, port=8888)
