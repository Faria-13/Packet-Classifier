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
import statmaker2

numpy_dir="numpy"
cleaned_dir="cleaned_datasets"



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
    icmp_ctr = 0
    arp_ctr = 0
    tcp_ctr = 0
    udp_ctr = 0
    stp_ctr = 0
    ctr = 0


    # Read the file and classify
    with open(X_outfile, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        packet_hex = lines[i].strip()  # Hex data
        classic = statmaker2.classifier(packet_hex)  # Get the packet class

        # Assign class based on classifier result
        if classic == 'ICMP':
            traffic_class_int = 0
            icmp_ctr += 1
        elif classic == 'TCP':
            traffic_class_int = 1
            tcp_ctr += 1
        elif classic == 'ARP':
            traffic_class_int = 2
            arp_ctr += 1
        elif classic == 'UDP':
            traffic_class_int = 3
            udp_ctr += 1

        elif classic == 'STP':
            traffic_class_int = 4
            stp_ctr += 1        
        else:
            continue  # Skip unknown classes


        
        Y[ctr]=int(traffic_class_int)   #making into integer                  #Places the value of the ground truth into the proper Y index
        ctr=ctr+1  #Overall ctr

    print("Some label counters:", icmp_ctr, tcp_ctr, arp_ctr, udp_ctr, stp_ctr)

    print ("Y shape after labelling:", Y.shape)
    # return Y_one_hot
    return Y
    

def preprocessor_main(features):

    os.makedirs(numpy_dir, exist_ok=True)

    X_cols = features
    Y_cols = 1

    cleaned_files = sorted(
        os.path.join(cleaned_dir, f)
        for f in os.listdir(cleaned_dir)
        if f.endswith("_cleaned.txt")
    )

    for X_source_file in cleaned_files:
        base = os.path.splitext(os.path.basename(X_source_file))[0]
        base = base.replace("_cleaned", "")

        X_features_file = os.path.join(
            numpy_dir, f"{base}_features.npy"
        )
        Y_labels_file = os.path.join(
            numpy_dir, f"{base}_labels.npy"
        )

        print("\nInput file             :", X_source_file)
        print("Normalized feature file:", X_features_file)
        print("Output label file      :", Y_labels_file)

        X_rows, Y_rows = num_rows(X_source_file)

        X, Y = numpy_X_Y(X_rows, X_cols, X_source_file, Y_rows, Y_cols)
        X_normalized = mean_normalize(X, features)
        Y = fields_and_labels(X_source_file, Y)

        #so that the y labels match the length of predictions
        Y = Y.squeeze()   # (N,1) → (N,)


        np.save(X_features_file, X_normalized)
        np.save(Y_labels_file, Y)

    print("NumPy preprocessing complete")











