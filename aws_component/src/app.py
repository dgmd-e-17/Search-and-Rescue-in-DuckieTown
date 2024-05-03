# Sid: Import Flask and Python Libraries 
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from PIL import Image, ImageDraw
from dotenv import load_dotenv
# Sid: Import AWS Libraries 
import boto3
import torch
# Sid: Import MASK R-CNN Deep Learning Model Libraries
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.transforms import functional as F


# Sid: Target for refactor / removal 
import requests
import json
import torchvision
import cv2
import numpy as np
from datetime import datetime

# Sid: Load dotenv items
load_dotenv()

# Sid: Load the Mask R-CNN neural network model
model = maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Sid: Define the list of COCO classes for Mask R-CNN
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
    'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A', 'handbag',
    'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
    'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
    'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
    'N/A', 'dining table', 'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Sid: AWS credentials and region
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

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

    # Sid: Define AWS ReKognition disaster labels to flag for deeper review
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

            # Sid: Iterate through detected labels and determine if any exist in disaster categories 
            disaster_detected = any(label['name'] in disaster_labels for label in labels)

            # Sid: Append analysis results to the list and publish to index html
            results.append({
                'image_key': image_key,
                'last_modified': last_modified.strftime('%Y-%m-%d %H:%M:%S'),
                'disaster_detected': disaster_detected,
                'labels': labels
            })

        # Sid: Render the index.html and pass results to Jinja to populate table
        return render_template('index.html', results=results)

    # Sid: Exception handling 
    except Exception as e:
        return jsonify({'error': str(e)}), 500





# Sid: Define application route for analyze_image.html and MASK R-CNN image analysis 
@app.route("/analyze_image", methods=["GET"])
def analyze_image():
    
    # Sid: Core logic to redirect user to analyze_image page, downloand image from s3 and analyze using MASK R-CNN
    try:
        # Sid: Extract the url param from request 
        image_key_param = request.args.get('image_key')

        # Sid: Define the local path to store the downloaded image in the project stattc/captures folder and assign the original file name
        local_file_path = os.path.join("static", "captures", image_key_param)

        # Sid: Download the selected image from S3 based on bucket name, image name and store it in local folder 
        s3_client.download_file(bucket_name, image_key_param, local_file_path)

        # Sid: Assign variable to store and open the image
        img = Image.open(local_file_path)

        # Sid: Define image tensor variable to store converted image as PyTensor for CNN deep learning and object detection
        img_tensor = F.to_tensor(img)

        # Sid: Perform inference analysis on converted Py Tensor image
        with torch.no_grad():
            prediction = model([img_tensor])

        # Sid: Initialize an array to store detected labels
        labels = []

        # Sid: Draw bounding boxes on the image
        draw = ImageDraw.Draw(img)
        # Sid: Loop through predicted image labels and scores
        for idx, score in enumerate(prediction[0]['scores']):
            # Sid: If prediction score is above 50%, execute following bounding on image
            if score > 0.5:  
                # Sid: Extract the bounding boxes coordinates from the list of detected boxes from Py Tensor and store as list 
                bbox = prediction[0]['boxes'][idx].tolist()
                # Sid: Extract the class index for the detected label
                class_idx = prediction[0]['labels'][idx].item()
                # Sid: Map the class index to the category name in the COCO dictionary 
                class_name = COCO_INSTANCE_CATEGORY_NAMES[class_idx]
                # Sid: Draw rectanges around detected objects 
                draw.rectangle(bbox, outline="orange", width=3)
                # Sid: Print COCO category name in the top left of the bounding box 
                draw.text((bbox[0], bbox[1]), class_name, fill="red")
                # Sid: Add label names to label array 
                labels.append(class_name)

        # Sid: Save the analyzed image and add s3 to the begining of the filname 
        analyzed_image_filename = "s3_" + image_key_param  
        # Sid: Store the analyzed image in the captures folder
        analyzed_image_path = os.path.join("static", "captures", analyzed_image_filename)
        # Sid: Save the image in the defined path
        img.save(analyzed_image_path)
        # Sid: Remove the extra static from the file path to allow for publish of statis file path in the html file
        analyzed_image_path = os.path.relpath(analyzed_image_path, "static")

        # Sid: Render page, analyzed image and and detected labels to display them in the browser
        return render_template("analyze_image.html", analyzed_image_path=analyzed_image_path, labels=labels)
    
    # Sid: Error handling
    except Exception as e:
        return jsonify({'error': str(e)}), 500





# Sid: Flask App Main Runtime statement
if __name__ == "__main__":
    app.run(debug=True)
