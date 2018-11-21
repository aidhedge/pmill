import papermill as pm
import json
import uuid
import boto3
import os



class Pmill(object):

    def __init__(self, nbInputFileName=None, parameters=None):
        self.result = list()
        self.uuid = '{}-{}'.format(nbInputFileName, str(uuid.uuid1()))
        self.parameters = parameters
        self.nbInputFileName = nbInputFileName
        self.notebook = None
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

    def getS3(self):
        s3 = boto3.resource(
        's3', 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', default=None),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', default=None)
        )

        filepath = 'output/'+self.uuid+'.ipynb'
        print(filepath)
        content_object = s3.Object('ah-papermill', filepath)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        return json_content

    def getOutput(self):
        output = dict()
        data = self.getS3()
        output.update(nb = data)
        # with open('output.ipynb') as f:
        #     data = json.load(f)

        output_cell = [d for d in data["cells"] if d['metadata']['tags'] == ['calculation_result']][0]
        outputs = output_cell['outputs']

        for out in outputs:
            out['data']['text/plain'][0] = out['data']['text/plain'][0].replace("'","\"")
            self.result.append(json.loads(out['data']['text/plain'][0]))
        output.update(result = self.result)
        
        return json.dumps(output)




