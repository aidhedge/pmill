import papermill as pm
import json

class Pmill(object):

    def __init__(self, nbInputUrl=None, parameters=None):
        self.nbInputUrl = nbInputUrl
        self.result = list()
        # self.nb_data = None

    def executeNotebook(self):
        pm.execute_notebook(
        'http://127.0.0.1:5000/input.ipynb',
        './output.ipynb',
        parameters = dict(alpha=100, ratio=10),
        log_output=True,
        progress_bar=True,
        report_mode=False
        )

    def getOutput(self):
        with open('output.ipynb') as f:
            data = json.load(f)

        output_cell = [d for d in data["cells"] if d['metadata']['tags'] == ['calculation_result']][0]
        outputs = output_cell['outputs']

        for out in outputs:
            out['data']['text/plain'][0] = out['data']['text/plain'][0].replace("'","\"")
            self.result.append(json.loads(out['data']['text/plain'][0]))

        return json.dumps(self.result)




