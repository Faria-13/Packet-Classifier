
import datetime
import torch
import numpy as np
import goodneural
import numpy_populator
import cleaner_tcpdump

OUTPUT_FILE = "experiment_results.txt"
TEST_FILE_LIST =["datasets/master.txt", "datasets/newtcp.txt" ,"datasets/test2.txt"]  

cleaner_tcpdump.main(TEST_FILE_LIST)  # Clean the test files first

x_trainer_file = "numpy/master_features.npy"
y_trainer_file = "numpy/master_labels.npy"

x_test_file_list = ["numpy/master_features.npy", "numpy/newtcp_features.npy", "numpy/test2_features.npy"]
y_test_file_list = ["numpy/master_labels.npy", "numpy/newtcp_labels.npy", "numpy/test2_labels.npy"]



# Parameter grid
feature_list = [128, 64]
iterations_list = [100, 400, 500, 1000]
hidden_nodes_list = [10, 28, 64, 128]
alpha_list = [0.001, 0.0001, 0.00001]
batch_sizes = [128, 64]

classes = 5

with open(OUTPUT_FILE, "a") as f:

    for batch_size in batch_sizes:
        for features in feature_list:
            #for each feature size, we gotta size up the matrices
            numpy_populator.preprocessor_main(features, TEST_FILE_LIST)
            #load the x and y train once matrices are the right size 
            X_train = torch.from_numpy(
                np.load(x_trainer_file).T
                ).float()

            Y_labels = torch.from_numpy(np.load(y_trainer_file)).long()

            for hidden_nodes in hidden_nodes_list:
                for iterations in iterations_list:
                    for alpha in alpha_list:
                    

                        print("\nRunning experiment...\n")

                        accuracy_list = goodneural.gen_net_mlp_main(X_train, Y_labels, x_test_file_list,y_test_file_list, features,
                                                          iterations, hidden_nodes, classes, alpha, batch_size )

                        line = (
                            f"features={features}, "
                            f"iterations={iterations}, "
                            f"hidden_nodes={hidden_nodes}, "
                            f"alpha={alpha}, "
                            f"batch_size={batch_size}, "
                            f"accuracy={accuracy_list}\n"

                        )

                        f.write(line)
                        f.flush()

                        print("Saved:", line)




