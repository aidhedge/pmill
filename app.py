import os
import sys
from flask import Flask
from flask import jsonify
from flask import request
import json
from pmill import Pmill




# LOG = Logger()
app = Flask(__name__)

@app.route("/routes", methods=['GET'])
def routes_info():
    """Print all defined routes and their endpoint docstrings

    This also handles flask-router, which uses a centralized scheme
    to deal with routes, instead of defining them as a decorator
    on the target function.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        try:
            if rule.endpoint != 'static':
                if hasattr(app.view_functions[rule.endpoint], 'import_name'):
                    import_name = app.view_functions[rule.endpoint].import_name
                    obj = import_string(import_name)
                    routes.append({rule.rule: "%s\n%s" % (",".join(list(rule.methods)), obj.__doc__)})
                else:
                    routes.append({rule.rule: app.view_functions[rule.endpoint].__doc__})
        except Exception as exc:
            routes.append({rule.rule: 
                           "(%s) INVALID ROUTE DEFINITION!!!" % rule.endpoint})
            route_info = "%s => %s" % (rule.rule, rule.endpoint)
            app.logger.error("Invalid route: %s" % route_info, exc_info=True)
            # func_list[rule.rule] = obj.__doc__

    return jsonify(code=200, data=routes)

@app.route("/ping")
def ping():
    return "Pong!"

@app.route("/", methods=['GET'])
def index():
    return 'Aidhedge Papermill'



@app.route("/get-parameters", methods=['GET'])
def getParametersFromNotebook():
   
    pm = Pmill(
        nbInputFileName='input'
    )
    res = pm.getParameters()
    return res



@app.route("/run-notebook", methods=['GET','POST'])
def runNotebook():
    nbName = request.form['nbName']
    parameters = request.form['parameters']
    pm = Pmill(
        parameters=json.loads(parameters),
        nbInputFileName=nbName
    )
    pm.executeNotebook()
    res = pm.getOutput()
    return res
    # except:
    #     e = sys.exc_info()[0]
    #     return str(e), 500

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True, host='0.0.0.0', port=5000)







