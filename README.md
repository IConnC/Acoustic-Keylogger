# Acoustic Keylogger
Acoustic keylogging, a form of side channel attack, represents a growing cybersecurity threat. This project introduces a lightweight, real-time Convolutional Neural Network (CNN) model designed for generalized acoustic keylogging on embedded systems with computational resource constraints. By utilizing a custom dataset, this model can predict keypresses from keyboard acoustic audio with a test accuracy of ~51% and precision of around ~82%. This project also consists of a keylogger, audio recorder, and data preprocessing component that allows for an accurate collection of training data for the acoustic keylogging model. This proof of concept emphasizes the need for further acoustic keylogging research for more robust safeguards against this type of side channel attack.

## data-collection
Contains methods for data collection from a microphone and a python based keylogger for the dataset

## data-manipulation
Processes the data collected from data-collection scripts and matches keypresses with their acoustic signatures

## training
model.ipynb contains the CNN model, training, and testing code for the project