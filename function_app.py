import azure.functions as func
import logging
import json 
import openai
import os
from azure.storage.blob import BlobClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="TriggerProcessingBonds")
def TriggerProcessingBonds(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        # Initialize BlobClient
        blob = BlobClient(account_url="https://bondprocessing.blob.core.windows.net",
                          container_name="spreadsheet",
                          blob_name="Bond Master File.xlsx.json",
                          credential="eyLhe8ZPYGZovt+BlpXu4syIzRUVmh9J+T3UGKzczeRqW6iAnXfAUHgLrCtJ6cz2zWinLP9dzpGe+ASt494OPQ==")
        
        # Test access to the blob (check if the blob exists)
        blob_properties = blob.get_blob_properties()
        logging.info(f"Blob found: {blob_properties}")

        # Optionally, read blob contents (useful for larger debugging)
        blob_data = blob.download_blob().readall()
        logging.info(f"Blob content: {blob_data[:100]}")  # Log only the first 100 characters

        return func.HttpResponse(f"Successfully accessed blob: {blob_properties.name}", status_code=200)

    except Exception as e:
        logging.error(f"Failed to access blob: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)