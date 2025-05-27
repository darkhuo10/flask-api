from flask import request, session, jsonify, make_response
import json
import decimal
from __main__ import app
from controllers import product_controller
from common.functions import Encoder, sanitize_input, prepare_response_extra_headers,admin_session_validate,user_session_validate

@app.route("/products",methods=["GET"])
def get_all_products():
    if user_session_validate:
        res, code= product_controller.get_all_products()
    else:
        res = {"status":"Forbidden"}
        code=403
    response= make_response(json.dumps(res, cls=Encoder), code)
    return response



@app.route("/product/<id>",methods=["GET"])
def get_product_by_id(id):
    id = sanitize_input(id)
    if isinstance(id, str) and len(id) < 64:
        res, code = product_controller.get_product_by_id(id)
    else:
        res = {"status":"Forbiden"}
        code = 403
    response = make_response(json.dumps(res, cls=Encoder), code)
    return response

@app.route("/product/create",methods=["POST"])
def create_product():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        product_json = request.json
        #Sanitize all the json
        ret,code=product_controller.create_product(json_to_product(product_json)) 
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

@app.route("/product/delete/<id>", methods=["DELETE"])
def delete_product(id):
    ret,code=product_controller.delete_product(id)
    return json.dumps(ret), code

@app.route("/product/update/<id>", methods=["PUT"])
def update_product(id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        product_json = request.json
        ret,code=product_controller.update_product(json_to_product(product_json), id)
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code