import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # Parse the incoming JSON payload
    try:
        body = json.loads(event['body'])
        filename = body['filename']
    except (KeyError, TypeError, ValueError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request'})
        }

    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Specify your bucket name
    bucket_name = 'harvard-e17-robotics'

    try:
        # Generate a presigned URL for uploading
        presigned_url = s3_client.generate_presigned_url('put_object',
                                                         Params={'Bucket': bucket_name, 'Key': filename},
                                                         ExpiresIn=3600)  # URL expires in 1 hour
        return {
            'statusCode': 200,
            'body': json.dumps({'url': presigned_url})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }