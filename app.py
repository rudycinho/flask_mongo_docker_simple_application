from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)