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
    CAPTURE_FILE_LIST = []
    clear_directory("cleaned_datasets")       #this clears the cleaned datasets folder every time you start the program
    print("\n\n🚀 Welcome to Faria's Packet Classifier Toolkit\n")

    

    while True:

        print("\nMenu:")
        print("1. Select datasets")
        print("2. Show packet statistics")
        print("3. Train neural network (Windows)")
        print("Q/q. Quit")

        choice = input("\nChoice: ").strip().lower()


        if choice == '1':
            files = list_dataset_files()
            sel = input("\nSelect files (ex 1,3-5): ")
            CAPTURE_FILE_LIST = parse_selection(sel, files)

            print("\nSelected:")
            for f in CAPTURE_FILE_LIST:
                print("  ", f)

        elif choice == '2':
            if  len(CAPTURE_FILE_LIST) == 0:
                print("Select datasets first (option 1)")
                continue
            
            print("\nCleaning datasets...\n")

            cleaner_tcpdump.main(CAPTURE_FILE_LIST)

            print("\nDatasets cleaned...\n")

            print("\nRunning statistics...\n")
            for cleaned_file in cleaner_tcpdump.CLEANED_FILE_LIST:
                
                statmaker2.statmaker(cleaned_file)

        elif choice == '3':
            if not CAPTURE_FILE_LIST:
                print("⚠️ Select datasets first (option 1)")
                continue

            cleaner_tcpdump.main(CAPTURE_FILE_LIST)

            numpy_populator.preprocessor_main(128)

            goodneural.main()


        elif choice == 'q':
            print("Bye ")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
