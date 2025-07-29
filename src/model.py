import cv2
import torch
from ultralytics import YOLO
import numpy as np
from PIL import Image
import torchvision.transforms as T
import torchvision.models as models
from sklearn.metrics import accuracy_score


yolo_model = YOLO('yolov8n.pt')

mobilenet = models.mobilenet_v3_small(pretrained=True)
mobilenet.eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mobilenet.to(device)

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def get_mobilenet_embedding(image):
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = mobilenet(img)
    return embedding

def get_object_crop(image, target_class):
    results = yolo_model(image)
    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) == target_class:  
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                return image[y1:y2, x1:x2]  
    return None

def generate_target_embedding(ref_image_paths, target_class):
    embeddings = []
    for path in ref_image_paths:
        ref_image = cv2.imread(path)
        if ref_image is None:
            raise FileNotFoundError(f"Image not found at {path}")
        
        object_crop = get_object_crop(ref_image, target_class)
        if object_crop is not None:
            embedding = get_mobilenet_embedding(object_crop)
            embeddings.append(embedding)
        else:
            print(f"No object of class {target_class} found in {path} — skipping.")
    
    if len(embeddings) == 0:
        raise ValueError(f"No valid object crops found for class {target_class} in reference images.")
    return torch.mean(torch.stack(embeddings), dim=0)

def cosine_similarity(emb1, emb2):
    return torch.nn.functional.cosine_similarity(emb1, emb2, dim=1).item()

def evaluate_accuracy(val_image_paths, val_labels, target_class, target_embedding, threshold=0.8):
    predictions = []
    true_labels = []
    
    for path, label in zip(val_image_paths, val_labels):
        image = cv2.imread(path)
        if image is None:
            print(f"Image not found at {path} — skipping.")
            continue
        
        object_crop = get_object_crop(image, target_class)
        if object_crop is not None:
            embedding = get_mobilenet_embedding(object_crop)
            similarity = cosine_similarity(embedding, target_embedding)
            prediction = 1 if similarity > threshold else 0  
            predictions.append(prediction)
            true_labels.append(label)
        else:
            print(f"No object of class {target_class} found in {path} — skipping.")
    
    if not predictions:
        print("No valid detections in validation set.")
        return 0.0
    
    accuracy = accuracy_score(true_labels, predictions)
    return accuracy

class_names = yolo_model.names

print("Available classes:", list(class_names.values()))
target_class_name = input("Enter the class to detect (e.g., person, car, dog): ").lower()
target_class = None
for cls_id, cls_name in class_names.items():
    if cls_name.lower() == target_class_name:
        target_class = cls_id
        break

if target_class is None:
    raise ValueError(f"Class '{target_class_name}' not found in YOLOv8 model.")

ref_image_paths = [
    r"D:\VS CODE\128 Technology Internship\Project\mahad1.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad2.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad3.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad4.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad5.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad6.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad7.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad8.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad9.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\mahad10.jpg"
]

val_image_paths = [
    r"D:\VS CODE\128 Technology Internship\Project\val_mahad1.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\val_mahad2.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\val_other1.jpg",
    r"D:\VS CODE\128 Technology Internship\Project\val_other2.jpg"
]
val_labels = [1, 1, 0, 0] 
target_embedding = generate_target_embedding(ref_image_paths, target_class)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = yolo_model(frame)
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            if int(box.cls[0]) == target_class:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                object_crop = frame[y1:y2, x1:x2]
                
                embedding = get_mobilenet_embedding(object_crop)
                
                similarity = cosine_similarity(embedding, target_embedding)
                if similarity > 0.8:
                    label = f"Known {class_names[target_class]}"
                    color = (0, 255, 0)
                else:
                    label = f"Unknown {class_names[target_class]}"
                    color = (0, 0, 255)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow('Object Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()