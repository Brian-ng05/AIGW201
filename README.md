# AI Pest Detection Chatbot

A local AI-powered chatbot integrated with a machine learning model for classifying agricultural pests. Users can interact with the chatbot in English and upload images to identify pests and receive handling advice. The system uses **Streamlit** for the interface and a locally hosted **LLM (Ollama)** for responses.

---

## Objectives

- Build an AI chatbot with a **web interface**  
- Develop a **pest classification ML model**  
- Design a **data pipeline** for preprocessing and augmentation  
- Integrate the chatbot with the ML model for **context-aware responses**  

---

## Dataset

The project uses the **worms4 dataset** from Kaggle with labeled images of common agricultural pests:

| Pest Class       | Number of Images |
|-----------------|----------------|
| Cabbage Worm     | 86             |
| Corn Earworm     | 125            |
| Cutworm          | 149            |
| Fall Armyworm    | 134            |

The dataset was chosen for its relevance to real-world pest detection and sufficient size for model training and evaluation.

---

## Data Pipeline

1. **Data Cleaning**: Verify images using PIL, remove corrupted files.  
2. **Dataset Split**: 70% training, 20% validation, 10% test.  
3. **Preprocessing & Augmentation**: Resize to 224×224 pixels; apply rotation, shift, zoom, flip, brightness adjustment.  
4. **Batching**: Batch size of 32 during training and evaluation.  

---

## Machine Learning Model

- **Base Model**: EfficientNetB0 pretrained on ImageNet, frozen weights.  
- **Custom Head**:  
  - Input preprocessing (`efficientnet.preprocess_input`)  
  - Global Average Pooling  
  - Dropout (0.5)  
  - Dense layer with 4 neurons and softmax activation  

**Training Settings**:  
- Optimizer: Adam (lr=0.001)  
- Loss: Categorical Crossentropy with label smoothing 0.1  
- Metric: Accuracy  
- Input size: 224×224×3, batch size: 32  
- Early stopping on `val_loss`, patience = 3  
- Class weights applied (1.2 for classes 0 & 2, 1 for classes 1 & 3)  
- Max epochs: 20  

---

## Evaluation

- Test accuracy: **≈90%** across all four pest classes  
- Training and validation loss curves show stable convergence  
- Data augmentation, class weighting, and early stopping improve robustness  

---

## Function Implementation

Integration is handled via **backend orchestration**:

1. User uploads an image → backend calls `predict_image` to classify the pest.  
2. Predicted label passed to LLM via `get_bot_response` for advice.  
3. **Conversation memory** maintains context for follow-up interactions.  

This simulates tool use: the ML model acts as a “tool” guiding LLM responses without direct function calls from the LLM.

---

## Installation

### Python Version
- Python 3.12.6 (or any 3.12+)

### Step 1:
git clone https://github.com/Brian-ng05/AIGW201.git
cd AIGW201

### Step 3:
pip install -r requirements.txt
#### Ensure worms_model.h5 is in the project root

### Step 3
streamlit run app.py


## Authors

- [@Nguyen Quoc Bao](https://github.com/Brian-ng05)
