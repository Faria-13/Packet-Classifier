import os
import capture
import numpy_populator
import cleaner_tshark
import statmaker
import goodneural

cleaned_file_list = []
mega_cleaned_file_list = ['megacleaned_datasets/arpRepmega_cleaned.txt',
                          'megacleaned_datasets/arpbroadcastmega_cleaned.txt',
                          'megacleaned_datasets/icmpmega_cleaned.txt']
X_test_file_list = ['numpyy/arpRep_features.npy' ,'numpyy/arpbroadcast_features.npy', 'numpyy/icmp_features.npy' ]
Y_test_file_list = ['numpyy/arpRep_labels.npy','numpyy/arpbroadcast_labels.npy', 'numpyy/icmp_labels.npy']


capture_file_list = [r'datasets/arpRep.txt', r'datasets/arpbroadcast.txt',
                     r'datasets/icmp.txt']


def process_tcpdump_output(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        lines = infile.readlines()
        timestamp = None
        hex_data = ""

        for line in lines:
            line = line.strip()
            # Check if the line starts with a timestamp (starts with a date-like format)
            if len(line) > 24 and line[4] == '-' and line[7] == '-' and line[10] == ' ':
                if timestamp and hex_data:
                    # Write the previous packet's timestamp and hex data
                    formatted_hex = format_hex_data(hex_data)
                    outfile.write(f"{timestamp}\n{formatted_hex}\n")

                # Grab the new timestamp and reset hex data
                timestamp = format_timestamp(line[:26])  # First 26 characters are the timestamp
                hex_data = ""  # Reset hex data for the new packet

            # Grab the hex data
            elif line.startswith('0x'):
                hex_data += line[7:].replace(' ', '')  # Remove the offset and colon and replace spaces

        # Write the last packet if it exists
        if timestamp and hex_data:
            formatted_hex = format_hex_data(hex_data)
            print("writing")
            print(outfile)
            outfile.write(f"{timestamp}\n{formatted_hex}\n")


def format_timestamp(timestamp):
    # Convert '2024-10-20 20:33:11.440718' to '20:33:11,440,718'
    date_time, microseconds = timestamp.split('.')
    time_part = date_time.split()[1]  # '20:33:11'
    
    formatted_timestamp = time_part + ',' + microseconds[:3] + ',' + microseconds[3:]
    return formatted_timestamp


def format_hex_data(hex_data):
    # Return the hex data as a continuous string
    return hex_data.lower()


def main():
    raw_file_list_len = len(capture_file_list)
    print("AAAAAAAAA ", capture_file_list)
   
    cleaned_dataset_dir = "cleaned_datasets/"
    mega_cleaned_dataset_dir = "megacleaned_datasets/"
    numpy_dir = "numpyy/"

    if not os.path.exists(cleaned_dataset_dir):
        os.makedirs(cleaned_dataset_dir)

    if not os.path.exists(numpy_dir):
        os.makedirs(numpy_dir)

    if not os.path.exists(mega_cleaned_dataset_dir):
        os.makedirs(mega_cleaned_dataset_dir)

    for i in range(raw_file_list_len):
        original_capture_file1 = capture_file_list[i]
        print("BOOOO ", original_capture_file1)
        original_capture_file = original_capture_file1.split('/')[1]  # Getting just the filename
    
        cleaned_file_name = cleaned_dataset_dir + original_capture_file.split(".")[0] + "_cleaned.txt"
        mega_cleaned_file_name = mega_cleaned_dataset_dir + original_capture_file.split(".")[0] + "mega_cleaned.txt"
        x_features_file_name = numpy_dir + original_capture_file.split(".")[0] + "_features.npy"
        y_label_file_name = numpy_dir + original_capture_file.split(".")[0] + "_labels.npy"
        print(mega_cleaned_file_name)

        if not os.path.exists(mega_cleaned_file_name):
            # Make the clean file
            with open(cleaned_file_name, 'w') as file:
                pass  # just Create the file 
            cleaned_file_list.append(cleaned_file_name)
            print(f"Empty file created: {cleaned_file_name}")

            # Make the mega clean file
            with open(mega_cleaned_file_name, 'w') as file:
                pass  # just Create the file 
            mega_cleaned_file_list.append(mega_cleaned_file_name)
            print(f"Empty file created: {mega_cleaned_file_name}")

            # Make the numpy X features files
            with open(x_features_file_name, 'w') as file:
                pass  
            X_test_file_list.append(x_features_file_name)
            print(f"Empty file created: {x_features_file_name}")

            # Make the numpy Y labels file
            with open(y_label_file_name, 'w') as file:
                pass  # Create the file without writing any content
            Y_test_file_list.append(y_label_file_name)
            print(f"Empty file created: {y_label_file_name}")

        original_capture_file1 = original_capture_file1.replace('Networking-Research-Hub/', '')  # For Linux file paths
        print("JJJJJJJJ", cleaned_file_name)
        #process_tcpdump_output(original_capture_file1, cleaned_file_name)  # This one for tcpdump captures only
        cleaner_tshark.parse_packet_file(original_capture_file1, cleaned_file_name)

        statmaker.analyze_packets_from_file(cleaned_file_name, mega_cleaned_file_name)   # This puts the only 4 classes in the mega cleaned file



