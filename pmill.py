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
            's3://ah-papermill/input/{0}.ipynb'.format(self.nbInputFileName),
            's3://ah-papermill/output/{0}.ipynb'.format(self.uuid),
            parameters=self.parameters,
            log_output=True,
            progress_bar=True,
            report_mode=False
        )

    def getS3(self):
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', default=None),
            aws_secret_access_key=os.getenv(
                'AWS_SECRET_ACCESS_KEY', default=None)
        )
        return s3

    def getFileContent(self, filepath):
        s3 = self.getS3()
        content_object = s3.Object('ah-papermill', filepath)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        return json.loads(file_content)

    def getOutput(self):
        output = dict()

        filepath = 'output/{0}.ipynb'.format(self.uuid)
        data = self.getFileContent(filepath)

        output.update(nb=data)

        output_cell = [d for d in data["cells"] if d['metadata']
                       ['tags'] == ['calculation_result']][0]
        outputs = output_cell['outputs']

        for out in outputs:
            out['data']['text/plain'][0] = out['data']['text/plain'][0].replace(
                "'", "\"")
            self.result.append(json.loads(out['data']['text/plain'][0]))
        output.update(result=self.result)

        return json.dumps(output)

    def getParameters(self):
        parameters = dict()
        filepath = 'input/{0}.ipynb'.format(self.nbInputFileName)
        data = self.getFileContent(filepath)

        parameters_cell = [d for d in data["cells"]
                           if d['metadata']['tags'] == ['parameters']][0]
        parameters = parameters_cell['source']

        return json.dumps(parameters)
