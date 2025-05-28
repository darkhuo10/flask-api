from flask import make_response, request, session
import json
from __main__ import app
from common.functions import Encoder, delete_session, sanitize_input
from controllers import waiter_controller


@app.route("/register",methods=['POST'])
def register_user():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        if "username" in login_json and "legal_name" in login_json and "password" in login_json and "profile" in login_json and "email" in login_json:
            username = sanitize_input(login_json['username'])
            legal_name = sanitize_input(login_json['legal_name'])
            password = sanitize_input(login_json['password'])
            profile = sanitize_input(login_json['profile'])
            email = sanitize_input(login_json['email'])
            if isinstance(username, str) and isinstance(legal_name, str) and isinstance(password, str) and isinstance(profile, str) and len(username) < 50 and len(password) < 50:
                respuesta,code= waiter_controller.register_user(username, legal_name, password, email)
            else:
                respuesta={"status":"Bad parameters"}
                code=401
        else:
            respuesta={"status":"Bad request"}
            code=401
    else:
        respuesta={"status":"Bad request"}
        code=401
    response= make_response(json.dumps(respuesta, cls=Encoder), code)
    return response

@app.route("/login", methods=["POST"])
def login():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        user_json = request.json
        username = user_json.get("username")
        password = user_json.get("password")
        
        ret, code = waiter_controller.login_user(username, password)
        
        if ret.get("status") == "OK":
            session["user_id"] = ret["user"]["id"]
        
    else:
        ret = {"status": "Bad request"}
        code = 401
    
    return json.dumps(ret), code

@app.route("/logout",methods=['GET'])
def logout():
    try:
        delete_session()
        ret={"status":"OK"}
        code=200
    except:
        ret={"status":"ERROR"}
        code=500
    response=make_response(json.dumps(ret),code)
    return response