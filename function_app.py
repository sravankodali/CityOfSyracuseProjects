import azure.functions as func
import logging
import json 
import openai
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Set up OpenAI API key
openai.api_key = os.getenv("OpenAIKey")

# Set up Azure Blob Storage connection string
connection_string = os.getenv("AzureWebJobsStorage")
container_name = "spreadsheet"
blob_name = "Bond Master File.xlsx.json"

@app.route(route="TriggerProcessingBonds")
def TriggerProcessingBonds(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )