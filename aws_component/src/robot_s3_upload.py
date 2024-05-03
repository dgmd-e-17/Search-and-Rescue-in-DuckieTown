# Sid: Import Flask and Python Libraries 
import requests
from datetime import datetime
import os
import json

# Sid: Project s3 bucket name
bucket_name = "harvard-e17-robotics"

# Sid: Input your local storage location
filename = "captures/image.png"

# Sid: Create file s3 naming
object_name = "capture.png"

# Sid: Current timestamp in the format YYYYMMDD-HHMMSS 
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# Sid: Split the object_name into name and extension
name, extension = object_name.rsplit('.', 1)

# Sid: Append the timestamp to the file name and add the extension back
object_name = f"{name}_{timestamp}.{extension}"


####################################### Create Flask Application #######################################

# Sid: Client Code for Robot upload into s3
def lambda_handler():

    # Sid: Establish API end point
    server_endpoint = 'https://r5l50m40ne.execute-api.us-east-1.amazonaws.com/prod/robotics_s3_presignedurl'

    # Sid: Logic to update the local image filename and insert a timestamp to ensure unique name in s3
    file_name = os.path.basename(filename)
    name, extension = os.path.splitext(file_name)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_file_name = f"{name}_{timestamp}{extension}"

    # Sid: Prepare the data payload as a dictionary
    data = {
        'filename': new_file_name
    }

    # Sid: Establish the body ofthe request as the file and key/value of the new filename
    data = {"body": json.dumps({"filename": new_file_name})}

    # Sid: Convert the Python dictionary to a JSON string
    data_json = json.dumps(data)

    # Sid: Set the appropriate HTTP headers for sending JSON
    headers = {'Content-Type': 'application/json'}

    # Sid: Send a POST request to the API Gateway endpoint
    response = requests.post(server_endpoint, data=data_json, headers=headers)

    # Sid: Check if the request was successful
    if response.status_code == 200:
        
        # Sid: Parse the response JSON to get the presigned URL
        presigned_url_response = response.json()
        presigned_url_body = json.loads(presigned_url_response['body'])
        presigned_url = presigned_url_body['url']

        # Sid: Confirm pre-signed url is in the response payload
        if presigned_url:
            
            # Sid: Open local file and prepare to upload a file to S3
            with open(filename, 'rb') as file_data:
                upload_response = requests.put(presigned_url, data=file_data)
                
                # Sid: Confirm success / failure of file upload into s3
                if upload_response.status_code == 200:
                    print("File was uploaded successfully.")
                else:
                    print(f"Failed to upload file: {upload_response.text}")
        
        # Sid: Return error message if pre-signed url not in response 
        else:
            print('Presigned URL not found in the response.')
    
    # Sid: Return error message if pre-signed url not in response 
    else:
        print('Failed to obtain presigned URL:', response.text)


