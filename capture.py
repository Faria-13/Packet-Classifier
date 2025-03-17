import os
import subprocess

capture_file_list = []

def list_interfaces():
    """Lists network interfaces using tcpdump -D command"""
    try:
        result = subprocess.run(['tcpdump', '-D'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error fetching interfaces")
            return []
        
        # Parse and display interfaces
        interfaces = []
        for line in result.stdout.splitlines():
            parts = line.split(".")
            if len(parts) > 1:
                interfaces.append(parts[1].strip())
        return interfaces

    except Exception as e:
        print(f"Error: {e}")
        print("OOPS")
        return []

import subprocess

def capture_traffic(interface, output_file, num_of_packets, num_of_files):
    
    dataset_dir = "datasets/"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)


    try:
        print(f"Capturing traffic on {interface}... Press Ctrl+C to stop.")
        
        # Split the interface string to handle multiple words if necessary
        interface = interface.split()
        num_of_packets = num_of_packets//num_of_files
        print(num_of_packets)
        print(interface[0])
        
        for i in range(num_of_files):

        # Define the tcpdump capture command
            capture_command = ['sudo','tcpdump', '-xx', '-tttt', '-i', interface[0], '-c', str(num_of_packets)]
            new_output_file = dataset_dir + output_file + str(i+1) + '.txt'
            print("AAAAAAAAAAA ", new_output_file)
            capture_file_list.append(new_output_file)
        # Open the output file in write mode to save the tcpdump output
            with open(new_output_file, 'w') as file:
                # Start the tcpdump process and redirect stdout to the file
                process = subprocess.Popen(capture_command, stdout=file, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stderr:
                    print(f"tcpdump error: {stderr.decode()}")
                # try:
                #     # Wait for the process to finish or until keyboard interrupt (Ctrl+C)
                #     process.wait()
                # except KeyboardInterrupt:
                #     print("\nCapture stopped.")
                #     process.terminate()
        
        print(f"Output saved to {capture_file_list}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    print("Listing available network interfaces...\n")
    interfaces = list_interfaces()
    
    if not interfaces:
        print("No interfaces found or an error occurred.")
        return
    
    # Display options to the user
    for index, iface in enumerate(interfaces):
        print(f"{index + 1}: {iface}")
    
    try:
        
        choice = int(input("\nEnter the number of the interface to capture on: ")) - 1
        if choice < 0 or choice >= len(interfaces):
            print("Invalid choice. Exiting.")
            return
        
        # Ask the user for the output filename
        output_file = input("Enter the name of the output file (e.g., foobar.txt): ")
        
        if not output_file:
            print("Invalid file name. Exiting.")
            return
        output_file = output_file.split(".")[0]
        print("SPLITTING  ", output_file)
        num_of_packets = int(input ("How many packets do you want captured? "))

        num_of_files = int(input ("How many files do you want them to be in (i.e 1,2,3): "))

        # function call
        capture_traffic(interfaces[choice], output_file, num_of_packets, num_of_files)

        print(f"{num_of_packets} packets have been saved to {output_file}")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")




