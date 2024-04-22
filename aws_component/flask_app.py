# Sid: Import Flask and Python Libraries 
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os
import json
import boto3


# Sid: AWS credentials and region (read them from env variable)
AWS_ACCESS_KEY_ID = 'key'
AWS_SECRET_ACCESS_KEY = 'key'
AWS_REGION_NAME = 'us-east-1'

# Sid: Project s3 bucket name
bucket_name = "harvard-e17-robotics"

# Sid: Initialize Boto3 client for Rekognition
rekognition_client = boto3.client('rekognition',
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  region_name=AWS_REGION_NAME)


# Sid: Initialize Boto3 client for s3
s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION_NAME)



####################################### Create Flask Application #######################################
app = Flask(__name__)




# Sid: Create Index / Home Page Route Logic
@app.route("/")
def home():

    # Sid: Define disaster labels to flag for deeper review
    disaster_labels = [
        'Fire', 'Smoke', 'Explosion', 'Flood', 'Earthquake',
        'Hurricane', 'Tornado', 'Tsunami', 'Volcano', 'Hazard',
        'Emergency', 'Accident', 'Terrorism', 'Riot', 'Gunshot'
    ]

    # Sid: Core logic to query the bucket and list all avaiable images
    try:
        # Sid: List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Sid: Initialize a list to store analysis results
        results = []

        # Sid: Iterate through each object in the bucket
        for obj in response.get('Contents', []):
            image_key = obj['Key']
            last_modified = obj['LastModified']

            # Sid Call AWS Rekognition API to analyze the image
            response = rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': image_key
                    }
                },
                MaxLabels=10,
                MinConfidence=70
            )

            # Sid: Extract detected labels from response
            labels = [{'name': label['Name'], 'confidence': label['Confidence']} for label in response['Labels']]

            disaster_detected = any(label['name'] in disaster_labels for label in labels)

            # Sid: Append analysis results to the list and publish to index html
            results.append({
                'image_key': image_key,
                'last_modified': last_modified.strftime('%Y-%m-%d %H:%M:%S'),
                'disaster_detected': disaster_detected,
                'labels': labels
            })

        return render_template('index.html', results=results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500





# Sid: Flask App Main Runtime statement
if __name__ == "__main__":
    app.run(debug=True)