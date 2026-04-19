import torch
import torch.nn as nn
import torchvision.models as models
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import os

CHECKPOINT_PATH = 'ml/checkpoints/best_checkpoint.pth'
EXPORT_DIR = 'ml/exports'


def load_best_model():
    model = models.efficientnet_b0(pretrained=True)
    model.classifier = nn.Linear(model.classifier.in_features, num_classes)  # Update the classifier
    checkpoint = torch.load(CHECKPOINT_PATH)
    model.load_state_dict(checkpoint['model_state_dict'])
    return model


def evaluate_model(model, test_loader):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predictions = torch.max(outputs, 1)
            all_preds.extend(predictions.numpy())
            all_labels.extend(labels.numpy())

    acc = np.sum(np.array(all_preds) == np.array(all_labels)) / len(all_labels)
    class_report = classification_report(all_labels, all_preds)
    return acc, class_report


def plot_confusion_matrix(all_labels, all_preds):
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.savefig('ml/exports/confusion_matrix.png')
    plt.close()


def export_model(model):
    torch.save(model.state_dict(), 'weather_classifier.pth')
    try:
        scripted_model = torch.jit.script(model)
        scripted_model.save('weather_classifier_scripted.pt')
    except Exception as e:
        print(f'Error during TorchScript export: {e}')
    class_names = ['class1', 'class2', 'class3']  # Replace with your actual class names
    with open('ml/exports/class_names.txt', 'w') as f:
        for name in class_names:
            f.write(f'{name}\n')
