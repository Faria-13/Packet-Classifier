import os
import numpy_populator
import statmaker
# import statmaker
import goodneural
import menu



cleaned_dataset_dir="cleaned_datasets/"
CLEANED_FILE_LIST=[]


def parse_packet_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        hex_data = ""

        for line in infile:
            line = line.strip()

            if line.startswith("+---------+"):
                continue

            # new packet starts
            if "," in line and "ETHER" in line:

                # flush previous packet
                if hex_data:
                    clean_hex = hex_data.replace("|", "").replace(" ", "").lower()
                    if clean_hex.startswith('0'):
                        clean_hex = clean_hex[1:]
                    clean_hex = format_packet_hex(clean_hex)
                    outfile.write(clean_hex + "\n")

                hex_data = ""   # reset
                continue

            # accumulate hex lines only
            hex_data += line

        # flush final packet
        if hex_data:
            clean_hex = hex_data.replace("|", "").replace(" ", "").lower()
            if clean_hex.startswith('0'):
                clean_hex = clean_hex[1:]
            clean_hex = format_packet_hex(clean_hex)
            outfile.write(clean_hex + "\n")




def format_packet_hex(packet_hex, length=goodneural.features):
    
    if len(packet_hex) > length:
        return packet_hex[:length]
    # Pad with '0's if shorter than 128 characters, new function unlocked wooohooo
    return packet_hex.ljust(length, '0')

def format_timestamp(timestamp):
    # Convert '2024-10-20 20:33:11.440718' to '20:33:11,440,718'
 
    date_time, microseconds = timestamp.split('.')
    time_part = date_time.split()[1]  # '20:33:11'
    
    formatted_timestamp = time_part + ',' + microseconds[:3] + ',' + microseconds[3:]
    return formatted_timestamp


def format_hex_data(hex_data):
    # Return the hex data as a continuous string
    return hex_data.lower()


def main(file_list):
    file_list_len = len(file_list)
   

    if not os.path.exists(cleaned_dataset_dir):
        os.makedirs(cleaned_dataset_dir)



    for i in range(file_list_len):
        file1= file_list[i]
        file_name_only = os.path.basename(file1)     #just get the filename, not the relative path

        cleaned_file_name = cleaned_dataset_dir + file_name_only.split(".")[0] + "_cleaned.txt"
        
        CLEANED_FILE_LIST.append(cleaned_file_name)

        if not os.path.exists(cleaned_file_name):
        #make the clean file 
            with open(cleaned_file_name, 'w') as file:
                pass  # just Create the file 
            print(f"Empty file created: {cleaned_file_name}")
            

            
        #process_tcpdump_output(file1, cleaned_file_name)    #make sure you feed the relative path in here
        #statmaker.analyze_packets_from_file(file1, cleaned_file_name)  # Analyze and clean the packets
        parse_packet_file(file1, cleaned_file_name)


       

      

# main()

# numpy_populator.preprocessor_main(128)
# goodneural.main()


 








