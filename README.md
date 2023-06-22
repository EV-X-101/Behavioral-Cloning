# Behavioral Cloning (BC) 🚘
This project implements a behavioral cloning algorithm for a self-driving car using deep learning techniques. The car is able to drive autonomously using a trained model that predicts the steering angle and throttle based on input images from a front-facing camera.

## Data Preprocessing 📊
The first part of the project is the data_preprocessing.py script, which is responsible for processing the training data. The training data consists of images captured from a front-facing camera, along with corresponding steering and throttle values. The script reads the images and preprocesses them by resizing, cropping, and normalizing them to feed them into the model. The script also splits the data into training and validation sets and saves them as NumPy arrays. Finally, the script trains a deep-learning model using the training data and saves the model weights and architecture for future use.

## Model Architecture 🧠
The model architecture used in this project is a convolutional neural network (CNN) with several layers (5) of convolution and pooling, followed by fully connected layers. The model takes in a single input image and outputs two values, the steering angle and throttle, which are used to control the car. The model is trained using the Adam optimizer and mean squared error (MSE) loss function.

## Driving the Car 🚗
The drive.py script is used to drive the car using the trained model. The script reads the model weights and architecture from the saved files and uses them to make predictions on input images from the car's camera. The script sends the predicted steering angle and throttle values to the car's actuators to control its movement.

### Training Data 🛣️

The Road Data folder under the Training folder contains the training data used to train the model. The folder includes images and corresponding steering, throttle values, movement direction, and speed.

### Dependencies 📦

The following dependencies are required to run the project:
    numpy
    matplotlib
    tensorflow
    keras
    Pillow==8.3.1
    opencv-python==4.5.3.56
You can install these dependencies using the requirements.txt file provided in the project

### Usage 🚀

To train the model, run the data_preprocessing.py script as follows:
    
    python data_preprocessing.py

To drive the car using the trained model, run the drive.py script as follows:
   
    python drive.py

   
