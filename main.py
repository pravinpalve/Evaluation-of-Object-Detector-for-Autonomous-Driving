import numpy as np
import os
import pravin_functions as pravin
threshold=0
folders = ["labels", "predictions"]
folder_loc = "D:/MASTERS/ACADEMICS/RADAR LIDAR/KITTI_Selection/KITTI_Selection/"

data = {} #create empty dictionaries
labels = {}
predictions = {}
 # Data reading
for folder in folders:
    pth = folder_loc + folder
    f = os.listdir(pth)
    for file in f:                             
        pth = folder_loc + folder + "/" + file 
        arr = np.loadtxt(pth, delimiter=",")
        if(folder == "labels"):
            labels[file[:6]] = arr
        if(folder == "predictions"):
            predictions[file[:6]] = arr
########## END OF READING LOOPS ###################
            
# data storage
for no in labels.keys():
    data[no] = [labels[no], predictions[no]]   # data[key][0] = labels  /// data[key][1] = predictions

#calculation for IOU
for key in data.keys():
    path_bev = "D:/MASTERS/ACADEMICS/RADAR LIDAR/KITTI_Selection/KITTI_Selection/bev/" + key + ".png"
    arr_labels = []
    arr_predictions = []
    text_arr = []
    (labels, predictions) = data[key]
    if(len(predictions) == 0):
        labels = [labels]
    print("\n \n Displayed Image ", key)
    false_neg_arr = []
    for lab in range(len(labels)):
        try:
            if(False): continue     # required conditions can be inserted here
            else:
                (lab_cx,lab_cy,lab_w,lab_l) = (data[key][0][lab][1:5])    # rectangle point values for predicted
                (im,re) = (data[key][0][lab][5:])
                r_lab = pravin.calculate_angle(im,re)
                rotn_labels = pravin.polygon_to_endpoints(pravin.rotate_rectangle(lab_cx,lab_cy,lab_w,lab_l,r_lab))  
                (lab_p1,lab_p2,lab_p3,lab_p4) = (rotn_labels[i] for i in range(len(rotn_labels))) 
                best_fit_iou = 0
                for pred in range(len(predictions)): 
                    if(len(predictions) != 0):        
                        try:
                            if(data[key][1][pred][6]<threshold): continue   # required conditions can be inserted here #edited for confidence values
                            else:
                                (pr_cx,pr_cy,pr_w,pr_l) = (data[key][1][pred][0:4])
                                (im,re) = (data[key][1][pred][4:6])
                                r_pred = pravin.calculate_angle(im,re)            
                                rotn_predictions = pravin.polygon_to_endpoints(pravin.rotate_rectangle(pr_cx,pr_cy,pr_w,pr_l,r_pred))
                                (pr_p1,pr_p2,pr_p3,pr_p4) = (rotn_predictions[i] for i in range(len(rotn_predictions)))                                                         ##
                                        
                                new_iou = pravin.total_bounding_area_points(lab_p1,lab_p2,lab_p3,lab_p4,pr_p1,pr_p2,pr_p3,pr_p4)[2]
                                
                                if(new_iou > best_fit_iou):
                                    best_fit_iou = new_iou
                        except:
                            pass

                if(best_fit_iou < 0.5):
                    false_neg_arr.append(new_iou)
                #if(best_fit_iou > 0):
                text_arr.append(round(best_fit_iou, 2))
        except:
            pass

############# PRINTING VALUES ##########
    true_positives = len([k for k in text_arr if(k>=0.50)])
    print(text_arr)
    false_positives = len(predictions) - true_positives
    false_negatives = len(false_neg_arr)
    print("True Positives: ", true_positives, "\n", "False Positives ", false_positives, "\n", "False Negatives: ", false_negatives)
    if(true_positives+false_positives != 0):
        precision = round(true_positives / (true_positives+false_positives),2)
    else:
        precision = 0.0

    if(true_positives + false_negatives != 0):
        recall_value = round(true_positives / (true_positives + false_negatives),2)
    else:
        recall_value = 0.0
    print("Precision: ", precision, "\n", "Recall Value: ", recall_value)

############################## PLOTTING ##################################

    for pred in range(len(predictions)):      # looping for predictions // red
        try:
            if(data[key][1][pred][6]>threshold): continue
            else:
                (pr_cx,pr_cy,pr_w,pr_l) = (data[key][1][pred][0:4])
                (im,re) = (data[key][1][pred][4:6])
                r_pred = pravin.calculate_angle(im,re)
                # Plotting #
                rotn_predictions = pravin.rotate_rectangle(pr_cx,pr_cy,pr_w,pr_l,r_pred)
                arr_predictions.append(rotn_predictions)
        except:
            print("Prediction Loop not executed for ", key)
    for lab in range(len(labels)):   
        if(len(predictions) != 0):
            (lab_cx,lab_cy,lab_w,lab_l) = (data[key][0][lab][1:5])
            (im,re) = (data[key][0][lab][5:])
            r_lab = pravin.calculate_angle(im,re)
            rotn_labels = pravin.rotate_rectangle(lab_cx,lab_cy,lab_w,lab_l,r_lab)
            arr_labels.append(rotn_labels)
        else:
            (lab_cx,lab_cy,lab_w,lab_l) = (labels[0][1:5])
            (im,re) = (labels[0][5:])
            r_lab = pravin.calculate_angle(im,re)
            rotn_labels = pravin.rotate_rectangle(lab_cx,lab_cy,lab_w,lab_l,r_lab)
            arr_labels.append(rotn_labels)
    print("arr_labels:", len(arr_labels))
    # print(arr_labels)
    print("arr_predictions", len(arr_predictions))
    # print(arr_predictions)
    print("Text array: ", len(text_arr))
    nlabs=len(labels)
    print("number of labels=", nlabs)
    pravin.display_bounding_boxes_2(path_bev, arr_labels, arr_predictions, title = key, text_1 = text_arr, text_2= [precision, recall_value, true_positives, false_positives, false_negatives, key,nlabs])


