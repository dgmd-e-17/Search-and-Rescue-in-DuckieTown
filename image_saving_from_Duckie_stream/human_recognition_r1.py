from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "yolo.h5")) # update this to the path of the YOLO model file you downloaded
detector.loadModel()

for filename in os.listdir(execution_path):
    if filename.endswith(".jpg"):
        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , filename), output_image_path=os.path.join(execution_path , "detected_" + filename))
        for eachObject in detections:
            if eachObject["name"] == "person":
                print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])