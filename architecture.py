import capture
import cleaner_tcpdump
import statmaker
import csvmaker


def main():
    print("\n\n Welcome to Faria's version of Wireshark \n\n")
    
    while True:
        # Display menu options
        print("\nPlease choose an option:")
        print("1. Start the capture process")
        print("2. Clean the tcpdump output")
        print("3. Display packet statistics")
        print("4. Parse packets into a CSV file")
        print("Q. Quit the program")

        # Get the user’s choice
        choice = input("Enter your choice (1/2/3/4/Q): ").strip().lower()

        # Execute corresponding functions based on user input
        if choice == '1':
            capture.main()
        elif choice == '2':
            cleaner_tcpdump.main()
        elif choice == '3':
            statmaker.analyze_packets_from_file("cleaned_foobar.txt")
        elif choice == '4':
            csvmaker.parse_packets("cleaned_foobar.txt", "foobar_csv.csv")
        elif choice == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please select a valid option (1/2/3/4/Q).")

# if __name__ == "__main__":
#     main()


# preprocessor_main(128,cleaned_file_list,X_test_file_list,Y_test_file_list)


