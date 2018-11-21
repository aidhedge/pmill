import papermill as pm
import json
import uuid

class Pmill(object):

    def __init__(self, nbInputFileName=None, parameters=None):
        self.result = list()
        self.uuid = '{}-{}'.format(nbInputFileName, str(uuid.uuid1()))
        self.parameters = parameters
        self.nbInputFileName = nbInputFileName
        # self.nb_data = None

    def executeNotebook(self):
        pm.execute_notebook(
        's3://ah-papermill/input/'+self.nbInputFileName+'.ipynb',
        's3://ah-papermill/output/'+self.uuid+'.ipynb',
        parameters = self.parameters,
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




