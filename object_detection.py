import cv2
from ultralytics import YOLO

class ObjectDetection:
    def __init__(self, model_path='./yolo-Weights/yolov8n.pt'):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)  # Access the camera

        # Set the resolution for the camera
        self.cap.set(3, 640)
        self.cap.set(4, 480)

    def detect_objects(self):
        success, img = self.cap.read()  # Read from the camera feed

        if not success:
            print("Failed to capture image")
            return None, None

        results = self.model(img, stream=True)  # Use YOLO to detect objects

        detected_objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box
                class_id = int(box.cls[0])  # Get class id of the detected object
                confidence = box.conf[0]  # Get confidence score
                detected_objects.append({
                    'class_id': class_id,
                    'confidence': confidence,
                    'bounding_box': (x1, y1, x2, y2)
                })
        return img, detected_objects

    def release(self):
        """Release the video capture object."""
        self.cap.release()
        cv2.destroyAllWindows()
