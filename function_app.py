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
        openai.api_key = os.getenv("OpenAIKey")
        if not openai.api_key:
            logging.error("OpenAI API key not found in environment variables.")
            return func.HttpResponse("OpenAI API key is missing.", status_code=500)
        
        # Initialize the BlobClient
        blob = BlobClient(account_url="https://bondprocessing.blob.core.windows.net",
                          container_name="spreadsheet",
                          blob_name="Bond Master File.xlsx.json",
                          credential="eyLhe8ZPYGZovt+BlpXu4syIzRUVmh9J+T3UGKzczeRqW6iAnXfAUHgLrCtJ6cz2zWinLP9dzpGe+ASt494OPQ==")
        
        blob_data = blob.download_blob().readall().decode('utf-8').strip()
        logging.info(f"Raw blob content: {blob_data[:100]}")  # Log first 100 characters for debugging
        
        # Split by newlines to handle multiple JSON objects
        json_lines = blob_data.split("\n")
        processed_bonds = []
        
        # Parse each line as a separate JSON object
        for line in json_lines:
            try:
                bond = json.loads(line)
                processed_bonds.append(bond)
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {str(e)} for line: {line}")

        # Get the user input from the request body
        try:
            req_body = req.get_json()
            user_input = req_body.get("user_input", "")
        except ValueError:
            logging.error("Invalid request body.")
            return func.HttpResponse("Invalid request body. Please provide valid JSON.", status_code=400)

        # Combine the bond data and user input into a single text prompt
        prompt = f"User input: {user_input}\n\nBond Data:\n{json.dumps(processed_bonds, indent=2)}"
        logging.info(f"Generated prompt for OpenAI: {prompt}")

        # Call the OpenAI API using the new interface
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the OpenAI response
        openai_response = response['choices'][0]['message']['content']
        logging.info(f"OpenAI response: {openai_response}")
        
        # Return the OpenAI response
        return func.HttpResponse(openai_response, status_code=200)

    except Exception as e:
        logging.error(f"Failed to process: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)