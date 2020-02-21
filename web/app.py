"""
Registration of a user 0 tokens
Each user get 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentece on out databae for 1 token
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db     = client.SentencesDatabase
users  = db["Users"]

class Register(Resource):
    def post(self):
        # Step 1 is to get posted data by the user
        posted_data = request.get_json()

        # Get the data
        username = posted_data["username"]
        password = posted_data["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8') ,bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username":username,
            "Password":hashed_pw,
            "Sentence":"",
            "Tokens":6
        })

        ret_json = {
            "status":200,
            "msg":"You successfully signed up for the Api"
        }

        return jsonify(ret_json)

def verifyPw(username,password):
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    return bcrypt.hashpw(password.encode('utf8'),hashed_pw)==hashed_pw

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    print(tokens)
    return tokens

class Store(Resource):
    def post(self):
        # Step 1 get the posted data
        posted_data = request.get_json()

        # Step 2 is to read the data
        username = posted_data["username"]
        password = posted_data["password"]
        senteces = posted_data["senteces"]

        # Step 3 verify the username pw match
        correct_pw = verifyPw(username,password)

        if not correct_pw:
            ret_json = {
                "status":302
            }
            return jsonify(ret_json)
        
        # Step 4 verify user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            ret_json = {
                "status":301
            }
            return jsonify(ret_json)
        # Step 5 store the sentence , take one token away and return 200 ok
        users.update({
            "Username":username
        },{
            "$set":{
                "Sentence":senteces,
                "Tokens":num_tokens-1
            }
        })
        ret_json = {
            "status":200,
            "msg":"Sentence saved successfully"
        }
        return jsonify(ret_json)

class Get(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]

        correct_pw = verifyPw(username,password)

        if not correct_pw:
            ret_json = {
                "status":302
            }
            return jsonify(ret_json)
            
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            ret_json = {
                "status":301
            }
            return jsonify(ret_json)
        
        #MAKE THE USER PAY!
        users.update({
            "Username":username
        },{
            "$set":{
                "Tokens":num_tokens-1
            }
        })

        sentence = users.find({
            "Username":username
        })[0]["Sentence"]

        ret_json = {
            "status":200,
            "sentence":sentence
        }
        return jsonify(ret_json)


api.add_resource(Register,'/register')
api.add_resource(Store,'/store')
api.add_resource(Get,'/get')


if __name__ == "__main__":
    app.run(host='0.0.0.0')

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({},{"$set":{"num_of_users":new_num}})
        return str("Hello user {}".format(str(new_num)))


def check_posted_data(posted_data, function_name):
    if(function_name == "add" or function_name == "subtract" or function_name == "multiply"):
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        else:
            return 200
    elif(function_name == "division"):
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        elif int(posted_data["y"]==0):
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        #If I am here, then the resource Add was requested using the method post
        #Step 1: Get posted data
        posted_data = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = check_posted_data(posted_data,"add")

        if(status_code!=200):
            ret_json = {
                'Message':'An error happened',
                'Status Code': status_code
            }
            return ret_json

        #if i am here, then status_code == 200
        x,y = posted_data["x"],posted_data["y"]

        #Step 2: Add the posted data
        ret = int(x) + int(y)
        ret_map = {
            'Message':ret,
            'Status Code': status_code
        }
        return jsonify(ret_map)

class Subtract(Resource):
    def post(self):
        #If I am here, then the resource Subtract was requested using the method post
        #Step 1: Get posted data
        posted_data = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = check_posted_data(posted_data,"subtract")

        if(status_code!=200):
            ret_json = {
                'Message':'An error happened',
                'Status Code': status_code
            }
            return ret_json

        #if i am here, then status_code == 200
        x,y = posted_data["x"],posted_data["y"]

        #Step 2: Add the posted data
        ret = int(x) - int(y)
        ret_map = {
            'Message':ret,
            'Status Code': status_code
        }
        return jsonify(ret_map)

class Multiply(Resource):
    def post(self):
        #If I am here, then the resource Multiply was requested using the method post
        #Step 1: Get posted data
        posted_data = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = check_posted_data(posted_data,"multiply")

        if(status_code!=200):
            ret_json = {
                'Message':'An error happened',
                'Status Code': status_code
            }
            return ret_json

        #if i am here, then status_code == 200
        x,y = posted_data["x"],posted_data["y"]

        #Step 2: Add the posted data
        ret = int(x) * int(y)
        ret_map = {
            'Message':ret,
            'Status Code': status_code
        }
        return jsonify(ret_map)
    
class Divide(Resource):
    def post(self):
        #If I am here, then the resource Division was requested using the method post
        #Step 1: Get posted data
        posted_data = request.get_json()
        #Step 1b: Verify validity of posted data
        status_code = check_posted_data(posted_data,"division")

        if(status_code!=200):
            ret_json = {
                'Message':'An error happened',
                'Status Code': status_code
            }
            return ret_json

        #if i am here, then status_code == 200
        x,y = posted_data["x"],posted_data["y"]

        #Step 2: Add the posted data
        ret = int(x) / int(y)
        ret_map = {
            'Message':ret,
            'Status Code': status_code
        }
        return jsonify(ret_map)


api.add_resource(Add,"/add")
api.add_resource(Subtract,"/subtract")
api.add_resource(Multiply,"/multiply")
api.add_resource(Divide,"/division")
api.add_resource(Visit,"/hello")

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
"""