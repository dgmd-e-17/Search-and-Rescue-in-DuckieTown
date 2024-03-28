import argparse
import requests
import os
from datetime import datetime
import json

def upload_file_to_s3_via_presigned_url(filename):
    # Read server endpoint URL from environment variable
    server_endpoint = os.getenv('AWS_SERVER_ENDPOINT_URL')
    if not server_endpoint:
        print("Server endpoint URL environment variable (AWS_SERVER_ENDPOINT_URL) not set.")
        return

    # Logic to update the local image filename and insert a timestamp to ensure unique name in S3
    file_name = os.path.basename(filename)
    name, extension = os.path.splitext(file_name)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_file_name = f"{name}_{timestamp}{extension}"

    # Prepare the data payload as a dictionary
    data = {"body": json.dumps({"filename": new_file_name})}

    # Convert the Python dictionary to a JSON string
    data_json = json.dumps(data)

    # Set the appropriate HTTP headers for sending JSON
    headers = {'Content-Type': 'application/json'}

    # Send a POST request to the API Gateway endpoint
    response = requests.post(server_endpoint, data=data_json, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON to get the presigned URL
        presigned_url_response = response.json()
        presigned_url_body = json.loads(presigned_url_response['body'])
        presigned_url = presigned_url_body['url']

        # Confirm presigned URL is in the response payload
        if presigned_url:
            # Open local file and prepare to upload a file to S3
            with open(filename, 'rb') as file_data:
                upload_response = requests.put(presigned_url, data=file_data)

                # Confirm success / failure of file upload into S3
                if upload_response.status_code == 200:
                    print("File was uploaded successfully.")
                else:
                    print(f"Failed to upload file: {upload_response.text}")
        else:
            print('Presigned URL not found in the response.')
    else:
        print('Failed to obtain presigned URL:', response.text)

def main():
    parser = argparse.ArgumentParser(description='Upload a file to AWS S3 via a presigned URL.')
    parser.add_argument('filename', type=str, help='Path to the file to be uploaded')

    args = parser.parse_args()

    upload_file_to_s3_via_presigned_url(args.filename)

if __name__ == '__main__':
    main()
