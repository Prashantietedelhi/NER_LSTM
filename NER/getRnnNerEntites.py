from flask import Flask, jsonify
import sys
import json, requests
from flask_cors import CORS, cross_origin
from flask import json
from flask.globals import request
import evaluate

app = Flask(__name__)
CORS(app)


model=evaluate.loadmodel()




@app.route('/getRnnNerEntites', methods=['POST'])
@cross_origin()
def getRnnNerEntites():
    if request.method != 'POST':
        return json.dumps({"Status": "ERROR", "DATA": None, "Reason": "Only accept POST request"})
    if not request.headers['Content-Type'] == 'application/json':
        return json.dumps({"Status": "ERROR", "DATA": None, "Reason": "Only  accept Content-Type:application/json"})
    if not request.is_json:
        return json.dumps({"Status": "ERROR", "DATA": None,
                           "Reason": 'Expecting json data in the form {"data":"VALUE"}'})
    data = request.json
    print(data)
    if 'sentence' not in data:
        return json.dumps({"Status": "ERROR", "DATA": None, "Reason": 'Expecting key as data'})
    try:
        sentence = data['sentence']

    except Exception as e:
        return json.dumps({"Status": "ERROR", "DATA": None,
                           "Reason": 'Failed to parse: "data" should be str'})

    try:
        nerTerms = evaluate.apiRequest(sentence,model)
        print(nerTerms)
    except Exception as e:
        return json.dumps({'Status": "ERROR", "DATA": None, "Reason": "Internal server error'})

    return json.dumps({"Status": "SUCCESS", "DATA": nerTerms, "Reason": ""})





def startApis():

    if model!=None:
        app.run("0.0.0.0", port=(9999), debug=False, threaded=True)
        app.run()
    else:
        print("error in loading model ..!!!")
if __name__ == '__main__':
    startApis()