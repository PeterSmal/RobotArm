import cv2
from ultralytics import YOLO

class ObjectDetection:
    def __init__(self, model_path='./yolo-Weights/yolov8n.pt'):
        self.model = YOLO(model_path)
        self.target_classes = ["car", "motorcycle"]  # Define target classes here

    def detect_objects(self, frame):
        # Resize frame for faster processing (optional)
        img_resized = cv2.resize(frame, (640, 480))

        # Perform object detection
        results = self.model(img_resized, stream=True)
        detected_objects = []  # List to store detected target objects

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                class_id = int(box.cls[0])              # Class ID
                confidence = float(box.conf[0])         # Confidence score
                class_name = self.model.names[class_id] # Class name

                # Filter for specific target objects
                if class_name in self.target_classes:
                    # Draw bounding box and label
                    cv2.rectangle(img_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{class_name}: {confidence:.2f}"
                    cv2.putText(img_resized, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    # Append to detected objects list
                    detected_objects.append({
                        "class": class_name,
                        "confidence": confidence,
                        "bbox": (x1, y1, x2, y2)
                    })

        return img_resized, detected_objects  # Return processed image and detected target objects
