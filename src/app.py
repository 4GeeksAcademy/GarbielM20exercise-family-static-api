"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/member/<int:member_id>', methods= ['DELETE'])
def delete_member(member_id):
    done = jackson_family.delete_member(member_id)
    if not done:
        response_body = {"message": "integrante de la familia no existe"}
        return response_body, 400
    response_body = {"done":True}
    return response_body, 400 

@app.route('/member',methods=["POST"])
def add_member ():
    request_body = request.json
    member = {"id": request_body.get("id") or jackson_family._generateId(),
              "first_name": request_body("first_name"),
              "age": request_body("age"),
              "lucky_numbers": request_body.get ( "lucky_numbers")}
    if not all (member.values()):
        response_body = {"mesage": "Faltan valores en su envio"}
        return response_body, 400
    response_body = jackson_family.add_member(member)
    return response_body, 200


@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


#def end POINT
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    result = jackson_family.get_member(member_id)
    if not result:
        response_body = {"mesage":"Integrante no encontrado"}
        return response_body, 400
    response_body = {"message":"Usuario enonctrado", 
                     "result": result[0]}
    return response_body, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
