import os
import cleaner_tcpdump
import numpy_populator
import goodneural
import statmaker2   

DATASET_DIR = "datasets"



def list_dataset_files():
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith(".txt")]
    files.sort()

    print("\nAvailable datasets:\n")
    for i, f in enumerate(files, 1):
        print(f"[{i}] {f}")

    return files


def parse_selection(selection, files):
    """
    Supports:
    1
    1,3,5
    2-6
    1,3-5
    """
    chosen = set()

    parts = selection.split(",")

    for part in parts:
        part = part.strip()

        if "-" in part:
            start, end = map(int, part.split("-"))
            for i in range(start, end + 1):
                chosen.add(files[i-1])
        else:
            chosen.add(files[int(part)-1])

    return [os.path.join(DATASET_DIR, f) for f in sorted(chosen)]




def clear_directory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)




def main():
    TEST_FILE_LIST = []
    TRAINING_FILE_LIST = []
    clear_directory("cleaned_datasets")       #this clears the cleaned datasets folder every time you start the program
    print("\n\n🚀 Welcome to Faria's Packet Classifier Toolkit\n")

    

    while True:

        print("\nMenu:")
        print("1. Select training dataset")
        print("2. Select testing dataset")
        print("3. Show packet statistics")
        print("4. Train neural network (Windows)")
        
        print("Q/q. Quit")

        choice = input("\nChoice: ").strip().lower()


        if choice == '1':
            files = list_dataset_files()
            sel = input("\nSelect a file: ")
            TRAINING_FILE_LIST = parse_selection(sel, files)

            print("\nSelected training file:")
            for f in TRAINING_FILE_LIST:
                print("  ", f)

        elif choice == '2':
            files = list_dataset_files()
            sel = input("\nSelect test files (ex 1,3-5): ")
            TEST_FILE_LIST = parse_selection(sel, files)
            TEST_FILE_LIST = set(TEST_FILE_LIST)  # remove duplicates if any

            print("\nSelected testing file:")
            for f in list(TEST_FILE_LIST):
                print("  ", f)

        elif choice == '3':
            print("Printing all the lists for debugging")
            print("Test file list:", TEST_FILE_LIST)
            print("Training file list:", TRAINING_FILE_LIST)

            
            combo_set = set(TRAINING_FILE_LIST + TEST_FILE_LIST)
            if  len(combo_set) == 0:
                print("Select datasets first (option 1)")
                continue
            
            print("\nCleaning datasets...\n")

            cleaner_tcpdump.main(list(combo_set))

            print("\nDatasets cleaned...\n")

            print("\nRunning statistics...\n")
            for cleaned_file in cleaner_tcpdump.CLEANED_FILE_LIST:
                
                statmaker2.statmaker(cleaned_file)

        elif choice == '4':
            if not TEST_FILE_LIST and not TRAINING_FILE_LIST:
                print("⚠️ Select both datasets first (option 1)")
                continue
            
            combo_set = set(TRAINING_FILE_LIST + TEST_FILE_LIST)
            cleaner_tcpdump.main(list(combo_set))

            numpy_populator.preprocessor_main(128, TRAINING_FILE_LIST)

        


        elif choice == 'q':
            print("Bye ")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
