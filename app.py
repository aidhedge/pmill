import os
import sys
from flask import Flask
from flask import jsonify
from flask import request
import json
from pmill import Pmill
import redis



# LOG = Logger()
app = Flask(__name__)




@app.route("/ping")
def ping():
    return "Pong!"

@app.route("/read", methods=['GET'])
def readFromRedis():
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    return r.get('foo')


@app.route("/", methods=['GET'])
def index():
    return 'Lightsail test'

@app.route("/write", methods=['GET'])
def writeToRedis():
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    r.set('foo', 'bar')
    
@app.route("/testo", methods=['GET'])
def simulate():
    try:
        pm = Pmill()
        pm.executeNotebook()
        res = pm.getOutput()
        return res
    except:
        e = sys.exc_info()[0]
        return str(e), 500

if __name__ == "__main__":
    # port = int(os.environ.get('PORT'))
    app.debug = True
    app.run(debug=True, host='0.0.0.0', port=5000)







