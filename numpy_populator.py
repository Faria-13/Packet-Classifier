#This parser converts the packet to a single X feature vector based on user input.
#6-28-19
#This version runs like all of the others: using the first hex character through the
#number of features requested.
#This parser also uses packet_types.py along with the newer datasets based on 2500 packets
#for each protocol/type for training. For ex. 2500 ARP messages 

#from packet_types import *
import numpy as np
from datetime import datetime
import time
import os
import statmaker



def num_rows(X_outfile):
    X_rows=0
    Y_rows=0
    with open(X_outfile) as data:
        for line in data:
            X_rows=X_rows+1
            Y_rows=Y_rows+1
    return X_rows, Y_rows

def numpy_X_Y(X_rows, X_cols, X_outfile, Y_rows, Y_cols):
    count =0
    X=np.zeros((X_cols,X_rows))
    Y=np.zeros((Y_rows,Y_cols))
    i=0
    print("numpy_X_Y shapes:",X.shape, Y.shape)
    print ("X COLS", X_cols)
    with open(X_outfile) as traffic:
        for line in traffic:
            count +=1
            for j in range(X_cols):
                
                line = line.strip()
                X[j][i]=int(line[j-1],16)  #This is a problem with odd nos. due to '/n'
            i=i+1
    #X=X/16           #Normalizes X
    #print(X[:,0])
    return X,Y

def mean_normalize(X, features):
    X_normalized=np.zeros((X.shape[0],X.shape[1]))
    #ctr=0
    for i in range(X.shape[1]):
        X_sum=np.sum(X[:,i])
        X_mean=X_sum/features
        for j in range (X.shape[0]):
            X_normalized[j,i]=X[j,i]-X_mean
        #Y[i]=Y[ctr]/16
        #ctr=ctr+1
    return X_normalized


def fields_and_labels(X_outfile, Y, num_classes=4):
    icmp_req_ctr = 0
    icmp_reply_ctr = 0
    arp_req_ctr = 0
    arp_reply_ctr = 0
    ctr = 0


    # Read the file and classify
    with open(X_outfile, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        packet_hex = lines[i].strip()  # Hex data
        classic = statmaker.classifier(packet_hex)  # Get the packet class

        # Assign class based on classifier result
        if classic == 'ICMP Request':
            traffic_class_int = 0
            icmp_req_ctr += 1
        elif classic == 'ICMP Reply':
            traffic_class_int = 1
            icmp_reply_ctr += 1
        elif classic == 'ARP Request':
            traffic_class_int = 2
            arp_req_ctr += 1
        elif classic == 'ARP Reply':
            traffic_class_int = 3
            arp_reply_ctr += 1
        else:
            continue  # Skip unknown classes


        
        traffic_class_int=str(traffic_class_int)
        Y[ctr]=int(traffic_class_int)   #making into integer                  #Places the value of the ground truth into the proper Y index
        ctr=ctr+1

    print("Some label counters:", icmp_req_ctr, icmp_reply_ctr, arp_req_ctr, arp_reply_ctr)
    # return Y_one_hot
    return Y
    

def preprocessor_main(features,cleaned_file_list,X_feature_file_list,Y_label_file_list):

    X_rows=0
    Y_rows=0
    Y_cols=1
    X_cols=features
   

    for i in range(len(cleaned_file_list)):   #actually mega cleaned file list cuz thats what gets passed
        X_source_file=cleaned_file_list[i]
        X_features_file=X_feature_file_list[i]
        Y_labels_file=Y_label_file_list[i]

        print()
        print("Input file             :",X_source_file)
        print("Normalized feature file:",X_features_file)
        print("Output label file      :",Y_labels_file)
        print()

        #print("Calling num_rows")
        X_rows, Y_rows=num_rows(X_source_file)              #Used to help build numpy arrays

        #print("Calling numpy_X_Y")
        X,Y=numpy_X_Y(X_rows, X_cols, X_source_file, Y_rows, Y_cols)

        #print("Calling mean_normalized")
        X_normalized=mean_normalize(X, features)    #Currently not called for CNN    6-4-19 

        # if "w" in X_source_file:
        #     print("Calling wireshark fields and labels for:", X_source_file)
        #     Y=fields_and_labels(X_source_file, Y) #Processes source data to establish ground truth values.

        # else:
        #     print("Unknown file type.")

        Y = fields_and_labels(X_source_file, Y)
            
        np.save(Y_labels_file,Y)
        np.save(X_features_file,X_normalized)










