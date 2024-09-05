import azure.functions as func
import logging
import json
import os
from azure.storage.blob import BlobClient
import google.generativeai as genai

genai.configure(api_key=os.environ["API_KEY"])

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="TriggerProcessingBonds")
def TriggerProcessingBonds(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        try:
            req_body = req.get_json()
            user_input = req_body.get("user_input", "")
        except ValueError:
            logging.error("Invalid request body.")
            return func.HttpResponse("Invalid request body. Please provide valid JSON.", status_code=400)

        # Initialize the BlobClient
        blob = BlobClient(account_url="https://bondprocessing.blob.core.windows.net",
                          container_name="spreadsheet",
                          blob_name="Bond Master File.xlsx.json",
                          credential="eyLhe8ZPYGZovt+BlpXu4syIzRUVmh9J+T3UGKzczeRqW6iAnXfAUHgLrCtJ6cz2zWinLP9dzpGe+ASt494OPQ==")
        
        blob_data = blob.download_blob().readall()
        logging.info(f"Raw blob content: {blob_data[:100]}")  # Log first 100 characters for debugging
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"User input: {user_input}\n\nBond Data: {blob_data}"
        response = model.generate_content("Write a story about a magic backpack.")

        return func.HttpResponse(response.text, status_code=200)

    except Exception as e:
        logging.error(f"Failed to process: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)