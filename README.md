# Packet-Classifier-


menu.py - gives you options to choose training files, test files and train the model, 
        make sure you have a datasets/ directory with test files exported from wireshark

Once training and test files have been selected, 
Option 4 runs the model and does the following - 

---cleaner_tcpdump.main cleans up every file in those list to be just the hex lines only and saves them in a directory called cleaned_datasets (it will create it if you dont have it)

---numpy_populator.preprocessor_main takes in the training list and number of features (currently hadcoded to 128) and turns them into numpy arrays and saves them as features and labels files in the numpy/ directory (it will make it if you dont have it). It will also do the same for every file in the cleaned_datasets directory

    -- it saves test files in seperate lists to be used later 

    -- it makes a function call to goodneural.main and that function trains the model based on training file list, and tests it using the aforementioned two lists, and checks for accuracy. 