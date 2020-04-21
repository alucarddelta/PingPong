from flask import jsonify, request
from app import app, models, db
from sqlalchemy import and_
from sqlalchemy.exc import OperationalError
from marshmallow import ValidationError
import re
from typing import List, Dict, Tuple, Optional, Union, Type, Any
import app.schema as schema
import uuid
from functools import wraps
from os import environ
from datetime import datetime, timedelta


def return_result(result: Union[Dict, None]) -> Tuple[Union[str, None], int]:
    """ Helper function to reduce code repetition in routes

    Args:
        result: Dict on which to perform an existence check

    Returns:
        Tuple (str, int): json string and http status code
    """
    if result:
        return jsonify({"__args": request.args, "data": result}), 200
    else:
        return jsonify({"__args": request.args, "data": None}), 200


@app.route('/')
def route_default() -> Tuple[str, int]:
    return jsonify({"message": "hello",
                    "data": None}), 200

@app.route('/home', methods=['GET'])
def route_home_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:

    try:
        core = schema.get.Core().dump(db.session.query(models.Core).get(1))
        if core == {}:
            core = {"heading":None, "subheading":None}
        data =  schema.get.Request(many=True).dump(db.session.query(models.Request).all())
        if len(data) != 0:
            for x in data:
                del x['request_result']
        return return_result({"core":{"heading":core['heading'], "subheading":core['subheading']}, "menu" : data})

    except OperationalError as err:
        return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

@app.route('/app/home', methods=['POST'])
def route_home_post() -> Tuple[str, int]:

    data = request.get_json()
    if data:
        try:
            thing = schema.post.Core().load(data)
            db.session.add(thing)
            db.session.commit()
            return return_result(schema.get.Core().dump(thing))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422
        except OperationalError as err:
            return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

@app.route('/request', methods=['GET'])
@app.route('/request/<int:xid>', methods=['GET'])
def route_request_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:

    try:
        if xid:
            thing = db.session.query(models.Request).get(xid)
            if thing:
                return return_result(schema.get.Request().dump(thing))
            else:
                return jsonify({"error": "Could not find Thing '{}'".format(xid),
                                "data": None}), 404
        else:
            
            return return_result(schema.get.Request(many=True).dump(db.session.query(models.Request).all()))
    except OperationalError as err:
        return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

##############################
######## APP ONLY ############
##############################

@app.route('/app/get_request', methods=['GET'])
def route_app_get_request_get():
    data =  schema.get.Request(many=True).dump(db.session.query(models.Request).filter(models.Request.enabled==True).all())
    return return_result(data)

@app.route('/app/request', methods=['GET'])
@app.route('/app/request/<int:xid>', methods=['GET'])
def route_app_request_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:

    try:
        if xid:         
            data = schema.get.Request().dump(db.session.query(models.Request).get(xid))
            if data:
                datavalue = []
                last_hour_date_time = datetime.utcnow() - timedelta(hours = 1)
                last_day_date_time = datetime.utcnow() - timedelta(days = 1)
                last_week_date_time = datetime.utcnow() - timedelta(days = 7)

                datavalue = []
                last_hour = []
                last_day = []
                last_week = []
                if data['request_result'] != []:
                    time_now = datetime.strptime(data['request_result'][-1]['date_created'], '%Y-%m-%dT%H:%M:%S+00:00')
                    time_day = time_now - timedelta(hours = 12)
                    data['time_now'] = int(time_now.timestamp() * 1000)
                    data['time_day'] = int(time_day.timestamp() * 1000)
                for y in data['request_result']:
                    datetime_object = datetime.strptime(y['date_created'], '%Y-%m-%dT%H:%M:%S+00:00')
                    hour = last_hour_date_time < datetime_object
                    day = last_day_date_time < datetime_object
                    week = last_week_date_time < datetime_object
                    millisec = int(datetime_object.timestamp() * 1000)
                    datavalue.append([millisec, y['value']])
                    if hour == True:
                        last_hour.append(y['value'])
                    if day == True:
                        last_day.append(y['value'])
                    if week == True:
                        last_week.append(y['value'])

                if len(data['request_result']) != 0:
                    if data['request_result'][-1]['value'] == 0.0:
                        online = False
                    else:
                        online = True
                else:
                    online = False
                if last_hour != []:
                    data['hour_low'] = min(last_hour)
                    data['hour_high'] = max(last_hour)
                hour_s = []
                hour_f = []
                for z in last_hour:
                    if float(z) == 0.0:
                        hour_f.append(z)
                    else:
                        hour_s.append(z)
                data['hour_successful'] = len(hour_s)
                data['hour_fail'] = len(hour_f)
                if last_day != []:
                    data['day_low'] = min(last_day)
                    data['day_high'] = max(last_day)
                day_s = []
                day_f = []
                for z in last_day:
                    if float(z) == 0.0:
                        day_f.append(z)
                    else:
                        day_s.append(z)
                data['day_successful'] = len(day_s)
                data['day_fail'] = len(day_f)
                if last_week != []:
                    data['week_low'] = min(last_week)
                    data['week_high'] = max(last_week)
                week_s = []
                week_f = []
                for z in last_week:
                    if float(z) == 0.0:
                        week_f.append(z)
                    else:
                        week_s.append(z)
                data['week_successful'] = len(week_s)
                data['week_fail'] = len(week_f)

                data['online'] = bool()
                data['online'] = online
                data['chartformat'] = []
                data['chartformat'] = datavalue
                del data['request_result']
                return return_result(data)

            else:
                return jsonify({"error": "Could not find Thing '{}'".format(xid),
                                "data": None}), 404
        else:
            data =  schema.get.Request(many=True).dump(db.session.query(models.Request).filter(models.Request.visible==True).all())
            datavalue = []
            last_hour_date_time = datetime.utcnow() - timedelta(hours = 1)
            last_day_date_time = datetime.utcnow() - timedelta(days = 1)
            last_week_date_time = datetime.utcnow() - timedelta(days = 7)

            for x in data:
                datavalue = []
                last_hour = []
                last_day = []
                last_week = []
                for y in x['request_result']:
                    datetime_object = datetime.strptime(y['date_created'], '%Y-%m-%dT%H:%M:%S+00:00')
                    hour = last_hour_date_time < datetime_object
                    day = last_day_date_time < datetime_object
                    week = last_week_date_time < datetime_object
                    if hour == True:
                        millisec = int(datetime_object.timestamp() * 1000)
                        datavalue.append([millisec, y['value']])
                        last_hour.append(y['value'])
                    if day == True:
                        last_day.append(y['value'])
                    if week == True:
                        last_week.append(y['value'])

                if len(x['request_result']) != 0:
                    if x['request_result'][-1]['value'] == 0.0:
                        online = False
                    else:
                        online = True
                else:
                    online = False
                if last_day != []:
                    x['day_low'] = min(last_day)
                    x['day_high'] = max(last_day)
                day_s = []
                day_f = []
                for z in last_day:
                    if float(z) == 0.0:
                        day_f.append(z)
                    else:
                        day_s.append(z)
                x['day_successful'] = len(day_s)
                x['day_fail'] = len(day_f)
                if last_week != []:
                    x['week_low'] = min(last_week)
                    x['week_high'] = max(last_week)
                else:
                    x['no_data'] = True
                week_s = []
                week_f = []
                for z in last_week:
                    if float(z) == 0.0:
                        week_f.append(z)
                    else:
                        week_s.append(z)
                x['week_successful'] = len(week_s)
                x['week_fail'] = len(week_f)

                x['online'] = bool()
                x['online'] = online
                x['chartformat'] = []
                x['chartformat'] = datavalue
                del x['request_result']
            return return_result(data)
    except OperationalError as err:
        return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

@app.route('/app/request', methods=['POST'])
def route_request_post() -> Tuple[str, int]:

    data = request.get_json()
    if data:
        try:
            thing = schema.post.Request().load(data)
            db.session.add(thing)
            db.session.commit()
            return return_result(schema.get.Request().dump(thing))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422
        except OperationalError as err:
            return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

@app.route('/app/request', methods=['PUT'])
@app.route('/app/request/<int:xid>', methods=['PUT'])
def route_request_put(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:

    data = request.get_json()
    if xid == None:
        xid = data['xid']

    if data:
        try:
            thing = db.session.query(models.Request).get(xid)
            if thing:
                thing = schema.put.Request().load(data,
                                                instance=thing)
                db.session.add(thing)
                db.session.commit()
                return return_result(schema.get.Request().dump(thing))
            else:
                return jsonify({"error": "Could not find Request '{}'".format(xid),
                                "data": None}), 404
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 409 if "name" in err.messages.keys() else 422
        except OperationalError as err:
            return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

@app.route('/app/request/<int:xid>', methods=['DELETE'])
def route_request_delete(xid: int) -> Tuple[str, int]:
    try:
        thing = db.session.query(models.Request).get(xid)
        if thing:
            db.session.delete(thing)
            db.session.commit()
            return jsonify({"message": "Deleted Request '{}'".format(xid),
                            "data": None}), 200
        else:
            return jsonify({"error": "Could not find Request '{}'".format(xid),
                            "data": None}), 404
    except OperationalError as err:
        return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

@app.route('/app/heartbeat_send', methods=['GET'])
def route_app_heartbeat_send_get():

    try: 
         return return_result(schema.get.Heartbeat_Send(many=True).dump(db.session.query(models.Heartbeat_Send).filter(models.Heartbeat_Send.enabled==True).all()))
    except OperationalError as err:
        return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

@app.route('/app/request_result', methods=['POST'])
def route_request_result_post():

    data = request.get_json()
    if data:
        try:
            thing = schema.post.Request_Result().load(data)
            db.session.add(thing)
            db.session.commit()
            return return_result(schema.get.Request_Result().dump(thing))
        except ValidationError as err:
            #print(err.messages)
            return jsonify({"error": err.messages,
                            "data": None}), 422
        except OperationalError as err:
            return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

@app.route('/app/heartbeat_recieve/beat', methods=['POST'])
def route_heartbeat_recieve_post() -> Tuple[str, int]:

    data = request.get_json()
    if data:
        try:
            thing = db.session.query(models.Heartbeat_Receive).filter(models.Heartbeat_Receive.token == data['token'])

            thing = schema.post.Heartbeat_Receive().load(data)
            db.session.add(thing)
            db.session.commit()
            return return_result(schema.get.Heartbeat_Receive().dump(thing))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422
        except OperationalError as err:
            return jsonify({"message": "Could not connect to database: {}".format(err)}), 500

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

@app.route('/app/config/service', methods=['GET'])
def route_config_service_get():

    try:
        data =  schema.get.Request(many=True).dump(db.session.query(models.Request).all())
        if len(data) != 0:
            for x in data:
                del x['request_result']
        return jsonify({"data": data}), 200

    except OperationalError as err:
        return jsonify({"message": "Could not connect to database: {}".format(err)}), 500