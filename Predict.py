import torch
from torchvision import models, transforms
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Your class names — update as per your model
class_names = ['Clear Cell', 'Endmoetri', 'Mucinous', 'Non Cancerous', 'Serous']

# Load your model architecture (adjust if you use a different one)
model = models.vgg13_bn(pretrained=False)
num_features = model.classifier[6].in_features
model.classifier[6] = torch.nn.Linear(num_features, len(class_names))

# Load checkpoint and fix state_dict keys (strip prefix if needed)
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

# Define torchvision transforms for model input
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Your preprocessing function for the cell image (updated with color fix)
def preprocess_cell_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, threshold1=30, threshold2=100)
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(edges, kernel, iterations=1)
    result_image = cv2.bitwise_or(image, image, mask=dilated_image)
    return result_image

def predict_single_image(model, image_path, device):
    # Load original image as PIL for display
    original_image = Image.open(image_path).convert('RGB')

    # Preprocess image (OpenCV BGR NumPy array)
    processed_image = preprocess_cell_image(image_path)
    if processed_image is None:
        raise FileNotFoundError(f"Image not found or could not be processed: {image_path}")

    # Convert processed BGR image to RGB PIL image for model input and display
    image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    pil_processed_image = Image.fromarray(image_rgb)

    # Transform processed image to tensor and normalize
    input_tensor = transform(pil_processed_image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output, dim=1)
        predicted_idx = torch.argmax(probs, dim=1).item()
        confidence = probs[0, predicted_idx].item()

    return original_image, pil_processed_image, predicted_idx, confidence

if __name__ == "__main__":
    image_path = r'C:\Users\Asus\Desktop\MedicalProject\nnnn.png'

    original_img, processed_img, pred_idx, conf = predict_single_image(model, image_path, device)

    # Plot original and processed images side by side with prediction
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    axs[0].imshow(original_img)
    axs[0].set_title('Original Image')
    axs[0].axis('off')

    axs[1].imshow(processed_img)
    axs[1].set_title(f'Processed Image\nPredicted: {class_names[pred_idx]} ({conf*100:.2f}%)')
    axs[1].axis('off')

    plt.tight_layout()
    plt.show()
