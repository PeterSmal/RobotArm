import cv2
from ultralytics import YOLO
 
class ObjectDetection:
    def __init__(self, model_path='./yolo-Weights/yolov8n.pt'):
        self.model = YOLO(model_path)
 
    def detect_objects(self, frame):
        # Resize frame for faster processing (optional)
        img_resized = cv2.resize(frame, (640, 480))
       
        # Perform object detection
        results = self.model(img_resized, stream=True)
 
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box
                class_id = int(box.cls[0])  # Get class id of the detected object
                confidence = box.conf[0]  # Get confidence score
               
                # Draw bounding box on the frame
                cv2.rectangle(img_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
               
                # Draw label with confidence score
                label = f"{self.model.names[class_id]}: {confidence:.2f}"
                cv2.putText(img_resized, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
 
        return img_resized, results  # Return the processed image and the detection results