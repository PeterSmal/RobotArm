import cv2
from ultralytics import YOLO
 
class ObjectDetection:
    def __init__(self, model_path='./yolo-Weights/yolov8n.pt', confidence_threshold=0.5, resize_frame=True):
        try:
            self.model = YOLO(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
 
        self.target_classes = ["car", "motorcycle", "airplane"]
        self.confidence_threshold = confidence_threshold
        self.resize_frame = resize_frame
 
    def detect_objects(self, frame):
        # Optionally resize frame for faster processing
        img_resized = cv2.resize(frame, (640, 480)) if self.resize_frame else frame
 
        # Perform object detection
        results = self.model(img_resized, stream=True)
        detected_objects = []  # List to store detected target objects
 
        # Process each result and filter by confidence and target classes
        for r in results:
            if r is not None:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                    class_id = int(box.cls[0])              # Class ID
                    confidence = float(box.conf[0])         # Confidence score
 
                    if confidence < self.confidence_threshold:
                        continue  # Skip low-confidence detections
 
                    class_name = self.model.names[class_id] # Class name
 
                    # Filter for specific target objects
                    if class_name in self.target_classes:
                        # Draw bounding box and label
                        cv2.rectangle(img_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f"{class_name}: {confidence:.2f}"
                        cv2.putText(img_resized, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
 
                        # Append to detected objects list
                        detected_objects.append({
                            "class": class_name,
                            "confidence": confidence,
                            "bbox": (x1, y1, x2, y2)
                        })
 
        return img_resized, detected_objects  # Return processed image and detected target objects