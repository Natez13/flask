from crypt import methods
from app import app
from flask import jsonify, request,abort,make_response
from functools import wraps
from auth import token_required,api_company_req
from Connect import connection
#API's de Location

@app.route('/api/v1/location',methods=['GET'])
@token_required
@api_company_req
def getM_location(current_company_api_key,current_company_id,current_user):
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Location"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            loactions = []
            for i in rows:
                    location = {}
                    location["company_id "] = i["company_id"]
                    location["location_name "] = i["location_name"]
                    location["location_country "] = i["location_country"]
                    location["location_city"] = i["location_city"]
                    location["location_meta"] = i["location_meta"]
                    loactions.append(location)
            
            return jsonify(loactions)
            
        except:
            return make_response('Locations not exist',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)

@app.route('/api/v1/location/id/',methods=['GET'])
@token_required
@api_company_req
def getU_location(current_company_api_key,current_company_id,current_user):
    location_id = request.args.get('location_id')
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Location Where ID="+location_id
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            loactions = []
            location = {}
            for i in rows:
                    location["company_id "] = i["company_id"]
                    location["location_name "] = i["location_name"]
                    location["location_country "] = i["location_country"]
                    location["location_city"] = i["location_city"]
                    location["location_meta"] = i["location_meta"]
                    loactions.append(location)

            return jsonify(loactions)
        except:
            return make_response('Locations not exist or id is invalid',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)

@app.route('/api/v1/location_update/id/',methods=['PUT'])
@token_required
#@api_company_req current_company_api_key,current_company_id,
def Update_location(current_user):
    json = request.json
    location_id  = json['location_id']
    location_name  = json['location_name']
    location_country  = json['location_country']
    location_city  = json['location_city']
    location_meta  = json['location_meta']
    
    try:
        sql = f"UPDATE Location SET location_name='{location_name}', location_country='{location_country}', location_city='{location_city}', location_meta='{location_meta}'  WHERE ID={location_id}"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('Locations updated',200)
    except:
        return make_response('Locations not exist or id is invalid',500,)


@app.route('/api/v1/location_delete/id/',methods=['DELETE'])
@token_required
#@api_company_req current_company_api_key,current_company_id,
def Delete_location(current_user):
    json = request.json
    location_id  = json['location_id']
    
    try:
        sql = f"DELETE FROM Location WHERE ID={location_id}"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('Locations deleted',200)
    except:
        return make_response('Locations not exist or id is invalid',500,)


@app.route('/api/v1/location_insert',methods=['POST'])
@token_required
#@api_company_req current_company_api_key,current_company_id,
def Insert_location(current_user):
    json = request.json
    company_id  = json['company_id']
    location_name  = json['location_name']
    location_country  = json['location_country']
    location_city  = json['location_city']
    location_meta  = json['location_meta']
    
    try:
        sql = f"Insert into Location (company_id, location_name, location_country, location_city, location_meta) VALUES('{company_id}','{location_name}','{location_country}','{location_city}','{location_meta}')"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('Locations Insert',200)
    except:
        return make_response('Locations not exist or id is invalid',500,)