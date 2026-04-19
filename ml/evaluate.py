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
NUM_CLASSES = 11  # <--- fixed: added num_classes globally
os.makedirs(EXPORT_DIR, exist_ok=True)

def load_best_model():
    model = models.efficientnet_b0(pretrained=False)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)
    checkpoint = torch.load(CHECKPOINT_PATH, map_location='cpu')
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
    return acc, class_report, all_labels, all_preds

def plot_confusion_matrix(all_labels, all_preds):
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.savefig(os.path.join(EXPORT_DIR, 'confusion_matrix.png'))
    plt.close()

def export_model(model, class_names):
    torch.save(model.state_dict(), os.path.join(EXPORT_DIR, 'weather_classifier.pth'))
    try:
        scripted_model = torch.jit.script(model)
        scripted_model.save(os.path.join(EXPORT_DIR, 'weather_classifier_scripted.pt'))
    except Exception as e:
        print(f'Error during TorchScript export: {e}')
    with open(os.path.join(EXPORT_DIR, 'class_names.txt'), 'w') as f:
        for name in class_names:
            f.write(f'{name}\n')

# Example usage (You should plug in your test data loader and actual class names)
if __name__ == '__main__':
    model = load_best_model()
    # You need to define your test_loader and class_names appropriately:
    # test_loader = ...
    # class_names = [...] (11 names in order)
    # # Example:
    # acc, class_report, labels, preds = evaluate_model(model, test_loader)
    # print(class_report)
    # plot_confusion_matrix(labels, preds)
    # export_model(model, class_names)
