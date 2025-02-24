import argparse
import json
import os
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None



# Use the base URL of your deployed Langflow instance
BASE_URL = os.environ.get("LANGFLOW_API_URL", "https://astra.datastax.com/langflow/b9fc9396-12de-4ab5-bb0a-ac397c854d0f")
BASE_API_URL = f"{BASE_URL}/api/v1/process"  # Note the change from /run to /process
FLOW_ID = os.environ.get("LANGFLOW_FLOW_ID", "37cae1da-25bb-49dc-a1a0-a632d8c0e87d")

# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "TextInput-Wuf7F": {},
  "ChatInput-oKG8X": {},
  "MemoryComponent-DyBIp": {},
  "ChatOutput-l9oIa": {},
  "AstraDB-fOMVZ": {},
  "OpenAIEmbeddings-Vzqrl": {},
  "File-WQTYc": {},
  "AstraDBSearch-1VIPH": {},
  "GroqModel-TLpDz": {},
  "Prompt-AiMeD": {}
}
def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    # Use BASE_API_URL directly, don't append endpoint
    api_url = BASE_API_URL
    
    print(f"Debug - API URL: {api_url}")
    
    payload = {
        "inputs": {
            "text": message
        },
        "flow_id": endpoint,  # Use the endpoint parameter as the flow_id
        "tweaks": tweaks or {}
    }
    
    print(f"Debug - Payload: {payload}")
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    print(f"Debug - Headers: {headers}")
    
    response = requests.post(api_url, json=payload, headers=headers)
    print(f"Debug - Response status: {response.status_code}")
    print(f"Debug - Response content: {response.text}")
    
    response.raise_for_status()  # This will raise an exception for HTTP errors
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        api_key=args.api_key
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
