import os
import capture

cleaned_file_list = []
X_test_file_list = []
Y_test_file_list = []

def parse_packet_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        lines = infile.readlines()

    
        timestamp = None
        hex_data = ""

        for line in lines:
            line = line.strip()

            if line.startswith("+---------+"):
                continue  # Skip the separator lines

            # If a line contains a timestamp
            if "," in line and "ETHER" in line:
                if timestamp and hex_data:             # this becomes true after the program has read both the lines
                    # Clean up the hex data by removing spaces and '|'
                    clean_hex = hex_data.replace("|", "").replace(" ", "").lower()
                    if clean_hex.startswith('0'):
                        clean_hex = clean_hex[1:]
                    outfile.write(f"{timestamp}\n{clean_hex}\n")

                # Reset for the next packet
                timestamp = line.split()[0]
                hex_data = ""              # the loop goes again and reads the next line, enters the else segment and grabs the hex
            else:
                # Grab the hex data 
                hex_data += line

        # After the loop, ensure the last packet is saved
        if timestamp and hex_data:
            clean_hex = hex_data.replace("|", "").replace(" ", "").lower()
            outfile.write(f"{timestamp}\n{clean_hex}\n")

# Call the function with input and output file paths
#parse_packet_file('icmptrial.txt', 'cleanedicmptrial.txt')

def main():
    raw_file_list_len = len(capture.capture_file_list)
    print("AAAAAAAAA ", capture.capture_file_list)
   
    cleaned_dataset_dir="cleaned_datasets/"
    numpy_dir="numpyy/"

    if not os.path.exists(cleaned_dataset_dir):
        os.makedirs(cleaned_dataset_dir)

    if not os.path.exists(numpy_dir): 
        os.makedirs(numpy_dir)

    for i in range(raw_file_list_len):
        original_capture_file1= capture.capture_file_list[i]
        original_capture_file = original_capture_file1.split("/")[1]
        cleaned_file_name = cleaned_dataset_dir + original_capture_file.split(".")[0] + "_cleaned.txt"
        x_features_file_name = numpy_dir + original_capture_file.split(".")[0] + "_features.npy"
        y_label_file_name = numpy_dir + original_capture_file.split(".")[0] + "_labels.npy"
        print(cleaned_file_name)

        if not os.path.exists(cleaned_file_name):
        #make the clean file 
            with open(cleaned_file_name, 'w') as file:
                pass  # just Create the file 
            cleaned_file_list.append(cleaned_file_name)
            print(f"Empty file created: {cleaned_file_name}")

        #make the numpy X features files 
            with open(x_features_file_name, 'w') as file:
                pass  
            X_test_file_list.append(x_features_file_name)
            print(f"Empty file created: {x_features_file_name}")

        #make the numpy Y labels file 
            with open(y_label_file_name, 'w') as file:
                pass  # Create the file without writing any content
            Y_test_file_list.append(y_label_file_name)
            print(f"Empty file created: {y_label_file_name}")
            
        parse_packet_file(original_capture_file1, cleaned_file_name)

