import azure.functions as func
import logging
import json
import os
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
from azure.storage.blob import BlobClient

# Pre-load the model and tokenizer outside the request function to avoid cold start delays
tokenizer = AutoTokenizer.from_pretrained("LargeWorldModel/LWM-Text-Chat-1M")
model = AutoModelForCausalLM.from_pretrained("LargeWorldModel/LWM-Text-Chat-1M")

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
        
        blob_data = blob.download_blob().readall().decode('utf-8').strip()
        logging.info(f"Raw blob content: {blob_data[:100]}")  # Log first 100 characters for debugging
        
        # Tokenize some prompt (example)
        prompt = "Your bond processing prompt here"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        # Generate a response using the model
        outputs = model.generate(**inputs, max_length=200)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return func.HttpResponse(response, status_code=200)

    except Exception as e:
        logging.error(f"Failed to process: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)