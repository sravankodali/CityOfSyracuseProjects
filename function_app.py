import azure.functions as func
import logging
import json
import os
from azure.storage.blob import BlobClient


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="TriggerProcessingBonds")
def TriggerProcessingBonds(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Initialize the BlobClient
        blob = BlobClient(account_url="https://bondprocessing.blob.core.windows.net",
                          container_name="spreadsheet",
                          blob_name="Bond Master File.xlsx.json",
                          credential="your_blob_credential_here")
        
        blob_data = blob.download_blob().readall()
        logging.info(f"Raw blob content: {blob_data[:100]}")  # Log first 100 characters for debugging
        

        return func.HttpResponse(response, status_code=200)

    except Exception as e:
        logging.error(f"Failed to process: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)