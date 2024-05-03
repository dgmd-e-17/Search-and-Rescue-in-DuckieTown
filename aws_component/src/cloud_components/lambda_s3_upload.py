# Sid: Import required libraries 
import json
import boto3
from botocore.exceptions import ClientError

# Sid: Define Lambda Event Handler Code
def lambda_handler(event, context):

    # Sid: Parse the incoming JSON payload from the robot
    try:
        # Sid: Extract payload information from the body
        body = json.loads(event['body'])
        # Sid: Extract the filename of image captured by the robot
        filename = body['filename']
    # Sid: Error Management for problematic requests 
    except (KeyError, TypeError, ValueError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request'})
        }

    # Sid: Initialize S3 client from AWS
    s3_client = boto3.client('s3')

    # Sid: Identify AWS bucket name
    bucket_name = 'harvard-e17-robotics'

    # Sid: Core logic to generate a pre-igned url for the robot to use to upload captured image into s3
    try:
        # Sid: Generate presigned URL for robot uploading which is an HTTP put request with one hour link upload window
        presigned_url = s3_client.generate_presigned_url('put_object',
                                                         Params={'Bucket': bucket_name, 'Key': filename},
                                                         ExpiresIn=3600) 
        # Sid: Return the response to the robot with code 200 and final url for image upload 
        return {
            'statusCode': 200,
            'body': json.dumps({'url': presigned_url})
        }
    # Sid: Error management which will return status code 500 for unsuccesful response 
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }