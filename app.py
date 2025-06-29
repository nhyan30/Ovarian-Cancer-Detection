from flask import Flask, request, jsonify
import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np
import io

app = Flask(__name__)

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Class names
class_names = ['Clear Cell', 'Endmoetri', 'Mucinous', 'Non Cancerous', 'Serous']

# Model setup
model = models.vgg13_bn(pretrained=False)
num_features = model.classifier[6].in_features
model.classifier[6] = torch.nn.Linear(num_features, len(class_names))

# Load weights
checkpoint = torch.load('vgg19_finetuned_best.pth', map_location=device)
new_state_dict = {}
for k, v in checkpoint.items():
    if k.startswith('vgg13_bn.'):
        new_key = k[len('vgg13_bn.'):]
    else:
        new_key = k
    new_state_dict[new_key] = v
model.load_state_dict(new_state_dict)
model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def preprocess_cell_image_opencv(image_np):
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, threshold1=30, threshold2=100)
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(edges, kernel, iterations=1)
    result_image = cv2.bitwise_or(image_np, image_np, mask=dilated_image)
    return result_image

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image_np = np.array(image)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    processed_np = preprocess_cell_image_opencv(image_np)
    processed_rgb = cv2.cvtColor(processed_np, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(processed_rgb)

    input_tensor = transform(pil_img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        confidence = probs[0, pred_idx].item()

    return jsonify({
        "class": class_names[pred_idx],
        "confidence": round(confidence * 100, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
