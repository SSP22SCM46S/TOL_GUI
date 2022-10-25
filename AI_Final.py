# Neural network and camera imports
import cv2 as cv
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import csv
import pandas as pd

# Servo imports
import RPi.GPIO as GPIO
import time

# Neural Network initialization
model = models.alexnet().eval()
model.classifier[6] = torch.nn.Linear(4096, 1081)
model.load_state_dict(torch.load('alexnet_weights_best_acc.tar', map_location = torch.device('cpu'))['model'])
model.eval()

# Servo initialization
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

plants = []

# First position
p.start(2.5)
time.sleep(3)
# Capture image 1
cam = cv.VideoCapture(0)
image = cam.read()[1]
cv.imwrite("image_1.png", image)
img_1 = Image.open('image_1.png')

# Prepare image 1 for neural network
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485, 0.456, 0.0406], std = [0.229, 0.224, 0.225]),
])

input_tensor = preprocess(img_1)
input_batch = input_tensor.unsqueeze(0)

with torch.no_grad():
    output = model(input_batch)

probabilities_1 = torch.nn.functional.softmax(output[0], dim = 0)

# Find the highest likelihood for image 1
index_1 = torch.argmax(probabilities_1)

# Find tree for the highest likelihood
df = pd.read_csv('labels.csv', encoding='iso-8859-1')
plants.append(df.iloc[index_1.item(), 1])

# Second position
p.ChangeDutyCycle(5.5)
time.sleep(3)
# Capture image 2
image = cam.read()[1]
cv.imwrite("image_2.png", image)
img_2 = Image.open('image_2.png')

# Prepare image 2 for neural network 
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485, 0.456, 0.0406], std = [0.229, 0.224, 0.225]),
])

input_tensor = preprocess(img_2)
input_batch = input_tensor.unsqueeze(0)

with torch.no_grad():
    output = model(input_batch)

probabilities_2 = torch.nn.functional.softmax(output[0], dim = 0)

# Find the highest likelihood for image 2
index_2 = torch.argmax(probabilities_2)

# Find tree for the highest likelihood
plants.append(df.iloc[index_2.item(), 1])

# Third position
p.ChangeDutyCycle(9.25)
time.sleep(3)
# Capture image 3
image = cam.read()[1]
cv.imwrite("image_3.png", image)
img_3 = Image.open('image_3.png')

# Prepare image 3 for neural network
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485, 0.456, 0.0406], std = [0.229, 0.224, 0.225]),
])

input_tensor = preprocess(img_3)
input_batch = input_tensor.unsqueeze(0)

with torch.no_grad():
    output = model(input_batch)

probabilities_3 = torch.nn.functional.softmax(output[0], dim = 0)

# Find the highest likelihood for image 3
index_3 = torch.argmax(probabilities_3)

# Find tree for the highest likelihood
plants.append(df.iloc[index_3.item(), 1])

# Fourth position
p.ChangeDutyCycle(12.5)
time.sleep(3)
# Capture image 4
image = cam.read()[1]
cv.imwrite("image_4.png", image)
img_4 = Image.open('image_4.png')

# Prepare image 4 for neural network
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485, 0.456, 0.0406], std = [0.229, 0.224, 0.225]),
])

input_tensor = preprocess(img_4)
input_batch = input_tensor.unsqueeze(0)

with torch.no_grad():
    output = model(input_batch)

probabilities_4 = torch.nn.functional.softmax(output[0], dim = 0)

# Find the highest likelihood for image 4
index_4 = torch.argmax(probabilities_4)

# Find tree for the highest likelihood
plants.append(df.iloc[index_4.item(), 1])

# Return to inital position
p.ChangeDutyCycle(2.5)
time.sleep(3)

p.stop()
GPIO.cleanup()

print(plants)