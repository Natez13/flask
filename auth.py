from crypt import methods
import sqlite3
from app import app
from flask import jsonify, request,abort,make_response
from datetime import datetime
from uuid import uuid4
import uuid
import jwt
from functools import wraps

def connection():
    conn = sqlite3.connect('./db/AEdb.db')
    conn.row_factory = sqlite3.Row
    return conn

# Servicio de Auntentificacion de Usuario y API's

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        current_user = {}
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], verify=True, algorithms=['HS256'])
            user_t=data['user']
            sql = f"SELECT * FROM Admin WHERE Username='{user_t}'"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            for i in rows:
                current_user['username'] = i["Username"]
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
        
    return decorator

def api_company_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        api_key = None
        current_company_id = {}
        current_company_api_key = {}
        if 'company_api_key' in request.headers:
            api_key = request.headers['company_api_key']
        if not api_key:
            return jsonify({'message': 'a valid company_api_key is missing'})
        try:
            sql = f"SELECT * FROM Company Where company_api_key='{api_key}'"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            if rows:
                for j in rows:
                    current_company_id = j["ID"]
                    current_company_api_key= j["company_api_key"]
            else:
                return jsonify({'message': 'company_api_key is invalid'})
        except:
            return jsonify({'message': 'company_api_key is invalid'})
        return f(current_company_api_key,current_company_id, *args, **kwargs)
        
    return decorator

def api_sensor_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        api_key = None
        current_sensor_api_key = {}
        current_sensor_id = {}
        if 'sensor_api_key' in request.headers:
            api_key = request.headers['sensor_api_key']
        if not api_key:
            return jsonify({'message': 'a valid sensor_api_key is missing'})
        try:
            sql = f"SELECT * FROM Sensor Where sensor_api_key='{api_key}'"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            if rows:
                for j in rows:
                    current_sensor_id = j["sensor_id"] 
                    current_sensor_api_key= j["sensor_api_key"] 
            else:
                return jsonify({'message': 'sensor_api_key is invalid'})
        except:
            return jsonify({'message': 'sensor_api_key is invalid'})
        return f(current_sensor_api_key,current_sensor_id, *args, **kwargs)
        
    return decorator
