import capture
import cleaner_tcpdump
import statmaker
import linux_cleaner_tcpdump
import numpy_populator
import goodneural
import cleaner_tshark
import newstatmaker

def main():
    print("\n\n Welcome to Faria's version of Wireshark \n\n")
    
    while True:
        # Display menu options
        print("\nPlease choose an option:")
        print("1. Start the capture process")
        print("2. Clean the tcpdump output")
        print("3. Display packet statistics")
        print("4. Run the neural network on a linux machine")
        print("5. Run the neural network on a Windows machine")
        print("Q. Quit the program")

        # Get the user’s choice
        choice = input("Enter your choice (1/2/3/4/5/5Q): ").strip().lower()

        # Execute corresponding functions based on user input
        if choice == '1':
            capture.main()
        elif choice == '2':
            cleaner_tcpdump.main()
        elif choice == '3':
            newstatmaker.main()
            
        elif choice == '4':
            linux_cleaner_tcpdump.main()
            numpy_populator.preprocessor_main(128, linux_cleaner_tcpdump.mega_cleaned_file_list, linux_cleaner_tcpdump.X_test_file_list, linux_cleaner_tcpdump.Y_test_file_list)
            goodneural.main()
        
        elif choice == '5':
            cleaner_tcpdump.main()
            numpy_populator.preprocessor_main(86, cleaner_tcpdump.mega_cleaned_file_list, cleaner_tcpdump.X_feature_file_list, cleaner_tcpdump.Y_label_file_list)
            goodneural.main()

        elif choice == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please select a valid option (1/2/3/4/Q).")

if __name__ == "__main__":
    main()
