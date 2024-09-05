import azure.functions as func
import logging
import json
import os
import openai
from azure.storage.blob import BlobClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="TriggerProcessingBonds")
def TriggerProcessingBonds(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Access the OpenAI API key from environment variables
        OpenAIKey = os.getenv('OpenAIKey')
        if not openai_api_key:
            logging.error("OpenAI API key not found in environment variables.")
            return func.HttpResponse("OpenAI API key is missing.", status_code=500)
        
        # Initialize the BlobClient
        blob = BlobClient(account_url="https://bondprocessing.blob.core.windows.net",
                          container_name="spreadsheet",
                          blob_name="Bond Master File.xlsx.json",
                          credential="eyLhe8ZPYGZovt+BlpXu4syIzRUVmh9J+T3UGKzczeRqW6iAnXfAUHgLrCtJ6cz2zWinLP9dzpGe+ASt494OPQ==")
        
        # Download the blob content as JSON
        blob_data = blob.download_blob().readall()
        logging.info(f"Blob content: {blob_data[:100]}")  # Log only the first 100 characters for debugging
        
        # Parse the JSON content from the blob
        json_data = json.loads(blob_data)

        
        # Get the user input from the request body
        try:
            req_body = req.get_json()
            user_input = req_body.get("user_input", "")
        except ValueError:
            logging.error("Invalid request body.")
            return func.HttpResponse("Invalid request body. Please provide valid JSON.", status_code=400)
        
        # Combine bond data with user input to send to OpenAI API
        openai_prompt = {
            "user_input": user_input,
            "bond_data": blob_data
        }
        
        # Call the OpenAI API
        openai.api_key = OpenAIKey
        response = openai.Completion.create(
            engine="gpt-4o",
            prompt=f"Process the following bond data and user input: {json.dumps(openai_prompt)}",
        )
        
        # Extract the OpenAI response
        openai_response = response['choices'][0]['text']
        logging.info(f"OpenAI response: {openai_response}")
        
        # Return the OpenAI response
        return func.HttpResponse(openai_response, status_code=200)

    except Exception as e:
        logging.error(f"Failed to process: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)