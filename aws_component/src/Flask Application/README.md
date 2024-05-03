This folder structure contains the Flask application which provides the following capabilities:
- User interface / dashboard to view all s3 images loaded by robot swarm
- Python code invoke AWS ReKognition AI services to analyze all images in the bucket for disaster scenarios. These results are posted in the index.html page with associated meta information
- Upon user request, will further analyze the image using MASK R-CNN neural network for object detection, classification and bounding box action for user analysis 
