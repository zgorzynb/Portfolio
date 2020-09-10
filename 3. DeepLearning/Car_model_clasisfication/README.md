# Car Model Classification

The repository contains full code allowing training of the neural network, whose task will be to classify the car model (196 classes). 
During the training, the [Cars Dataset](https://ai.stanford.edu/~jkrause/cars/car_dataset.html) data set was used.

## Dependencies:
- Python 3.x
- Tensorflow-gpu 2.1
- Keras-gpu 2.3.1
- CUDA 10

## How to run?
To run the project, place the database in "Images" folder and run Train.ipynb file.  
It is possible to replace the model (three models are implemented).  
To predict class for single image, you can use Test.ipynb.

## Network Results

Model   | Accuracy       | Loss function
:----------:|------------------------:|-----------------------:
ResNet50 | 82% | 0.75 
MobileNet | 74% | 0.76 
Own model | 61% | 1.18 
