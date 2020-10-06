# MNIST

This jupyter notebook is dedicated to prepare machine learning algorithm for MNIST Dataset.

## Data
Dataset is available [here](https://www.kaggle.com/c/digit-recognizer).

## Results
### Simple Neural Network
Architecture:
```
self.linear1 = nn.Linear(28*28, 135)
self.linear2 = nn.Linear(135,65)
self.linear3 = nn.Linear(65,10)
```

Accuracy: 94% 

### Convolutional Neural Network
Architecture:
```
self.conv1 = nn.Conv2d(1, 20, 5, 1)
self.conv2 = nn.Conv2d(20, 50, 5, 1)
self.fc1 = nn.Linear(4*4*50, 500)
self.dropout1 = nn.Dropout(0.5)
self.fc2 = nn.Linear(500, 10)
```

Accuracy: 98.5% 

## Dependencies:
  - Python 3.x
  - Pandas
  - PyTorch
  - numpy

