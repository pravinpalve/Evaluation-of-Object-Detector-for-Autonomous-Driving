# Evaluation-of-an-Object-Detector-for-Autonomous-Driving
In this project, we aim to assess the accuracy of an object detector built using complex YOLO by comparing the predictions with ground truths. In simple terms, it is pretty similar to checking an answer sheet (Predictions) of a Student (Object Detector) and scoring it by comparing it with the answer key (Ground truth labels). 

 The aim of the task also includes calculating precision and recall values for each scene, which will define factors for the evaluation of the object detector. To consider a detection to be TP, the condition is IOU ≥ 0.5. In this report, we will discuss the steps involved in data handling, plotting and calculations followed by the presentation of the results

The term IOU-Intersection of Union is an important concept and some background reading is suggested to new readers.

# main.py 
Contains main code

#pravin_functions
Contains diffrent functions which are imported and used in main.py
