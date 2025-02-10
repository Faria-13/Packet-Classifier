import capture
import cleaner_tcpdump
import statmaker
import numpy_populator
import goodneural
import cleaner_tshark

def main():
    print("\n\n Welcome to Faria's version of Wireshark \n\n")
    
    while True:
        # Display menu options
        print("\nPlease choose an option:")
        print("1. Start the capture process")
        print("2. Clean the tcpdump output")
        print("3. Display packet statistics")
        print("4. Run the neural network")
        print("Q. Quit the program")

        # Get the user’s choice
        choice = input("Enter your choice (1/2/3/4/Q): ").strip().lower()

        # Execute corresponding functions based on user input
        if choice == '1':
            capture.main()
        elif choice == '2':
            cleaner_tshark.main()
        elif choice == '3':
            print("SORRYYY")
            
        elif choice == '4':
            cleaner_tcpdump.main()
            numpy_populator.preprocessor_main(128, cleaner_tcpdump.mega_cleaned_file_list, cleaner_tcpdump.X_test_file_list, cleaner_tcpdump.Y_test_file_list)
            goodneural.main()

        elif choice == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please select a valid option (1/2/3/4/Q).")

if __name__ == "__main__":
    main()
