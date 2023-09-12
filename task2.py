#normalise
pip install torch
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Download the data, if not already on disk and load it as numpy arrays
lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
lfw_torched = torch.from_numpy(lfw_people.data)

X = torch.tensor(lfw_people.images,  device=device)
Y = torch.tensor(lfw_people.target, device=device)


# Verify the value range of X_train. No normalization is necessary in this case,
# as the input values already fall within the range of 0.0 to 1.0.
print("X_min:",X.min(),"X_train_max:", X.max())
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)
X_train = X_train[:, np.newaxis, :, :]
X_test = X_test[:, np.newaxis, :, :]
print("X_train shape:", X_train.shape)

#Hyper Parameters 
epochs = 8
batch_size = 42
learning_rate = 0.001

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)


train_loader = torch.utils.data.DataLoader(train_dataset, batch_size= batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size= batch_size)

target_names = lfw_people.target_names
n_classes = target_names.shape[0]

class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3)
        self.fc1 = nn.LazyLinear(120)
        self.fc2 = nn.LazyLinear(n_classes)

        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x= x.view(x.size(0), -1)
        x= F.relu(self.fc1(x))
        x= self.fc2(x)
        return x
        

model = ConvNet().to(device=device)
criteria = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
n_total_steps = len(train_loader)
for i in range (epochs):
    for i, (images, labels) in  enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        
        outputs = model(images)
        loss = criteria(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    
    #print (f'Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}')


with torch.no_grad():
    n_correct = 0
    n_samples = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        # max returns (value ,index)
        _, predicted = torch.max(outputs, 1)
        n_samples += labels.size(0)
        n_correct += (predicted == labels).sum().item()
        
    acc = 100.0 * n_correct / n_samples
    print(f'Accuracy of the network: {acc} %')

    