from crypt import methods
from app import app
from flask import jsonify, request,abort,make_response
from functools import wraps
from auth import token_required,api_company_req
from Connect import connection
from uuid import uuid4
import jwt
#API's de sensor

@app.route('/api/v1/sensor',methods=['GET'])
@token_required
@api_company_req
def getM_sensor(current_company_api_key,current_company_id,current_user):
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Sensor"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            Sensors = []
            for i in rows:
                    sensor = {}
                    sensor["sensor_id "] = i["sensor_id"]
                    sensor["location_id "] = i["location_id"]
                    sensor["sensor_name "] = i["sensor_name"]
                    sensor["sensor_category "] = i["sensor_category"]
                    sensor["sensor_api_key"] = i["sensor_api_key"]
                    sensor["sensor_meta"] = i["sensor_meta"]
                    Sensors.append(sensor)

            return jsonify(Sensors)
        except:
            return make_response('sensors not exist',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)


@app.route('/api/v1/sensor/id/',methods=['GET'])
@token_required
@api_company_req
def getU_sensor(current_company_api_key,current_company_id,current_user):
    sensor_id = request.args.get('sensor_id')
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Sensor Where sensor_id="+sensor_id
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            Sensors = []
            sensor = {}
            for i in rows:
                    sensor["sensor_id "] = i["sensor_id"]
                    sensor["location_id "] = i["location_id"]
                    sensor["sensor_name "] = i["sensor_name"]
                    sensor["sensor_category "] = i["sensor_category"]
                    sensor["sensor_api_key"] = i["sensor_api_key"]
                    sensor["sensor_meta"] = i["sensor_meta"]
                    Sensors.append(sensor)

            return jsonify(Sensors)
        except:
            return make_response('sensors not exist or id is invalid',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)

@app.route('/api/v1/sensor_update/id/',methods=['PUT'])
@token_required
# @api_company_req current_company_api_key,current_company_id,
def Update_sensor(current_user):
    json = request.json
    sensor_id  = json['sensor_id']
    sensor_name  = json['sensor_name']
    sensor_category  = json['sensor_category']
    sensor_meta  = json['sensor_meta']
    
    try:
        sql = f"UPDATE Sensor SET sensor_name='{sensor_name}', sensor_category='{sensor_category}', sensor_meta='{sensor_meta}'  WHERE sensor_id={sensor_id}"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('sensors updated',200)
    except:
        return make_response('sensors not exist or id is invalid',500,)


@app.route('/api/v1/sensor_delete/id/',methods=['DELETE'])
@token_required
# @api_company_req current_company_api_key,current_company_id,
def Delete_sensor(current_user):
    json = request.json
    sensor_id  = json['sensor_id']
    
    try:
        sql = f"DELETE FROM Sensor WHERE sensor_id={sensor_id}"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('sensors deleted',200)
    except:
        return make_response('sensors not exist or id is invalid',500,)


@app.route('/api/v1/sensor_insert',methods=['POST'])
@token_required
# @api_company_req current_company_api_key,current_company_id,
def Insert_sensor(current_user):
    json = request.json
    location_id  = json['location_id']
    sensor_name  = json['sensor_name']
    sensor_category   = json['sensor_category']
    sensor_api_key  = uuid4()
    sensor_meta  = json['sensor_meta']

    try:
        #Insercion 
        sql = f"Insert into Sensor (location_id, sensor_name, sensor_category, sensor_api_key, sensor_meta) VALUES('{location_id}','{sensor_name}','{sensor_category}','{sensor_api_key}','{sensor_meta}')"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
     
        return make_response('sensors Inserted',200)
    except:
        return make_response('sensors info is invalid',500,)