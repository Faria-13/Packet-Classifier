import math
import time
import numpy as np
import torch
import pdb
import sys
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data_utils
from torch.utils.data import Dataset, DataLoader
from mypredictions import *
#import seaborn as sns
#import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.image.AxesImage
from datetime import datetime
import cleaner_tcpdump
import os.path

ERROR = 1e-5

def gen_net_mlp_main(X_train, Y_labels,X_test_file_list, Y_test_file_list, num_features, iterations, hidden_nodes, classes, alpha, batch_size):#, train_loader):
    

    batch_size=batch_size
    D_in=num_features
    H2=hidden_nodes
    H1=2*hidden_nodes
    print("Model options:",num_features, iterations, hidden_nodes, classes, alpha, batch_size)
  
    iteration_ctr=0
    D_out=classes 
    epochs=iterations
    alpha=alpha
    max_iter=20
    train=data_utils.TensorDataset(X_train, Y_labels)
    train_loader=data_utils.DataLoader(train, batch_size=batch_size,shuffle=False)

    net_model=torch.nn.Sequential(
    torch.nn.Linear(D_in, H1),
    torch.nn.ReLU(),
    torch.nn.Linear(H1,H2),
    torch.nn.ReLU(),

    # torch.nn.Linear(H1,H2),
    # torch.nn.ReLU(),
    torch.nn.Linear(H2, D_out),       
    torch.nn.Softmax(dim=1)
    )
    
    #
    dtype=torch.float

    use_cuda=torch.cuda.is_available()
    device=torch.device("cuda:0" if use_cuda else "cpu")
    print("Device:",device)
    x=X_train
    print("Shape of x",x.size())
    y=Y_labels
    print("Shape of y",y.size())
    print()
    
    loss_array=torch.zeros(epochs,1)
    tick=datetime.now()

    # loss_fn=torch.nn.MSELoss(reduction='sum')
    loss_fn = torch.nn.CrossEntropyLoss()

    optimizer=optimizer_pick(1,net_model,alpha)
        
    epoch_ctr=0
    for epoch in range(epochs):
        batch_ctr=0
        for i, data in enumerate(train_loader,1):
            inputs, targets = data
            inputs=inputs.float()
              

            # y_pred=net_model((inputs).float())

        
            # loss=loss_fn(y_pred, targets.float())

            y_pred = net_model(inputs)
            loss = loss_fn(y_pred, targets.long())  # Use .long() to ensure targets are integer type

            time=str(datetime.now())  
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            #print("     Batch ctr:",batch_ctr)
            batch_ctr=batch_ctr+1
                               
        loss_array[epoch]=loss.item()
        
        epoch_ctr=epoch_ctr+1

        # break statement
        if loss.item() < ERROR:
            print(datetime.now(),"Loss for epoch:", epoch, loss.item())
            break

    #print("Counters:",epoch_ctr*batch_ctr)
    
    torch.save(net_model.state_dict(),'params.pt')
    tock=datetime.now()
    delta_time=tock-tick
    print()
    print("Done with general training. Total time:",delta_time)

    #print(tick)
    #print(tock)
    print()
    print("Starting to test datasets.")
    #plt.figure()
    #plt.ion()
    #plt.plot(loss_array)
    #plt.ylabel('cost')
    #plt.xlabel('iterations (per hundreds)')
    #plt.title("General Loss")
    #plt.savefig('gen.png')
    #plt.show()
    tcp_packet_list_list=[]
    #print(len(X_test_file_list))
    #runs=len(X_test_file_list)
    for l in range(len(X_test_file_list)):
        X_test=X_test_file_list[l]
        Y_test=Y_test_file_list[l]

        print(X_test)
        print(Y_test)
        X_test=np.load(X_test)
        X_test=np.transpose(X_test)
        X_test=torch.from_numpy(X_test).float()
        
        Y_test=np.load(Y_test)
        Y_test=np.transpose(Y_test)
        Y_test=torch.from_numpy(Y_test)
        Y_test_labels=torch.zeros(X_test.shape[0],classes)

        print("Shape of X_test:", X_test.shape)
        print("Shape of Y_test:", Y_test.shape)
        y_test_pred=net_model(X_test)
        
        predicted=torch.zeros(X_test.shape[0])
        
        for i in range(X_test.shape[0]):
            place=torch.argmax(y_test_pred[i])
            #if i < 100:
            #    print(place)
            predicted[i]=place
        predicted_numpy=predicted.numpy()

        packet_choice(predicted_numpy)
        accuracy(predicted_numpy, Y_test)

        #tcp_packet_list_list.append(tcp_packet_list)

    #return tcp_packet_list_list

def optimizer_pick(choice,net_model,alpha):

    optimizer=torch.optim.Adam(net_model.parameters(),lr=alpha) #Same as next Adam
    
    print("Optimizer:",optimizer)
    print()
    return optimizer


def main():
    features = 86
    iterations = 500  # At 401, the general accuracy is above 99.9%
    alpha = 1e-6
    hidden_nodes = 28
    classes = 4  #only 4 for now 
    batch_size = 128
    num_data_files = 3

   
    X_train = torch.randn(1000, features)  # Example training data with 128 features
    Y_labels = torch.randint(0, classes, (1000,))  # Example labels (0 to 3 for 4 classes)
   

    X_test_file_list = [cleaner_tcpdump.X_feature_file_list[2]]
    Y_test_file_list = [cleaner_tcpdump.Y_label_file_list[2]]
 
    # Call the function with these parameters
    gen_net_mlp_main(X_train, Y_labels, X_test_file_list, Y_test_file_list,
                    num_features=features, iterations=iterations, hidden_nodes=hidden_nodes, 
                    classes=classes, alpha=alpha, batch_size=batch_size)


# main()
