from crypt import methods
from app import app
from flask import jsonify, request,abort,make_response
from auth import token_required,api_sensor_req,api_company_req
from Connect import connection
from datetime import datetime
from ast import literal_eval

#API's de sensors_data
@app.route('/api/v1/sensor_data/send',methods=['POST'])
@token_required
@api_sensor_req
def send_data(current_sensor_api_key,current_sensor_id,current_user,):
    json = request.json
    sensor_id  = json['sensor_id']
    temperature  = json['temperature']
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)

    if int(current_sensor_id) == int(sensor_id):
        try:
            sql = "INSERT INTO Sensor_data (sensor_id,measure_time, temperature) VALUES(?,?,?)"
            data = (sensor_id,ts,temperature)
            conn = connection()
            conn.execute(sql,data)
            conn.commit()
            conn.close()
            resp = jsonify('Insert Sucefully')
            resp.status_code = 201  
            return resp
        except:

            resp = jsonify('Error in Insert Sensor')
            resp.status_code = 400  
            return resp
    else:
        resp = jsonify('Sensor id not match with sensor_api_key')
        resp.status_code = 400  
        return resp


@app.route('/api/v1/sensor_data_delete/id/',methods=['DELETE'])
@token_required
# @api_company_req current_company_api_key,current_company_id,
def delete_data(current_user):
    json = request.json
    sensor_id  = json['sensor_id']
    from_date = json['from']
    to_date = json['to']
    try:
        sql = f"DELETE FROM Sensor_data WHERE sensor_id={sensor_id} and measure_time BETWEEN {from_date} and {to_date}"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('sensors data deleted',200)
    except:
        return make_response('sensors not exist or id is invalid',500,)


@app.route('/api/v1/sensor_data',methods=['GET'])
@token_required
@api_company_req
def get_data(current_company_api_key,current_company_id,current_user,):
    sensor_id = request.args.get('sensor_id')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    company_id = request.args.get('company_id')
    sensor_id_list = literal_eval(sensor_id)
    #counter = list()
    if int(current_company_id) == int(company_id):
        try:
            Sensors_data_collention = []
            for i in sensor_id_list:
                sql = f"SELECT * FROM Sensor_data Where sensor_id={i} and measure_time BETWEEN {from_date} and {to_date}"
                conn = connection()
                rv = conn.execute(sql)
                rows = rv.fetchall()
                conn.close()

                Sensors_data_id = []
                #counter.append(sql)
                for j in rows:
                    sensors_data = {}
                    sensors_data["sensor_id "] = j["sensor_id"]
                    sensors_data["measure_time "] = datetime.fromtimestamp(j["measure_time"])
                    sensors_data["temperature "] = j["temperature"]
                    Sensors_data_id.append(sensors_data)
                Sensors_data_collention.append(Sensors_data_id)
                        

            resp = jsonify(Sensors_data_collention)
            resp.status_code = 201  
            return resp
        except:

            resp = jsonify('Error to obtain info of the Sensor ')
            resp.status_code = 400  
            return resp
    else:
        resp = jsonify('Company id not match with company_api_key ')
        resp.status_code = 400  
        return resp

