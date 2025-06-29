# 🧬 Ovarian Cancer Detection

This project aims to **detect ovarian cancer and its subtypes** using deep learning models applied to histopathology images. We experimented with multiple architectures, including custom CNNs and pre-trained models such as **VGG19, VGG16, and VGG13bn**, to classify cancer subtypes effectively.

## 📂 Dataset

We used the publicly available **Ovarian Cancer & Subtypes Dataset (Histopathology)** from Kaggle:  
🔗 [Dataset Link](https://www.kaggle.com/datasets/bitsnpieces/ovarian-cancer-and-subtypes-dataset-histopathology)

- The dataset contains histopathological image samples for different subtypes of ovarian cancer.
- Each image is labeled according to one of five cancer subtype classes:
  - Class 0
  - Class 1
  - Class 2
  - Class 3
  - Class 4

## 🧠 Models Used

We trained and evaluated the following deep learning models:

1. **Custom CNN (Baseline)**
   - Simple convolutional neural network designed from scratch.
2. **VGG19**
   - Transfer learning using the VGG19 architecture.
3. **VGG16**
   - A lighter VGG variant with good accuracy and faster training time.
4. **VGG13bn**
   - VGG13 with batch normalization layers added for better convergence.

Each model was trained and validated using the same data splits for a fair performance comparison.

## 📊 Evaluation Metrics

We used a variety of evaluation tools to assess model performance, including:

- **Confusion Matrix**
- **Accuracy, Precision, Recall, and F1-score**
- **ROC-AUC Curves for each class**

### 📈 Example ROC Curve Output
![download](https://github.com/user-attachments/assets/b7a7752f-a78c-419a-9f18-7339734083f2)


### 🖼️ Example Prediction Visualization
Each test image is displayed along with its predicted and actual labels for visual verification:

![download](https://github.com/user-attachments/assets/e33e9233-8d60-4557-b440-6713d369188f)




