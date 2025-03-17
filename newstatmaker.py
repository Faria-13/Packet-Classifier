import os
from collections import defaultdict
import capture

def extract_packet_info(packet_hex):
    ethernet_header_length = 14 * 2  # 14 bytes, each byte is 2 hex characters
    ip_header_start = ethernet_header_length
    total_length_hex = packet_hex[ip_header_start + 4:ip_header_start + 8]
    total_length = int(total_length_hex, 16)
    protocol_hex = packet_hex[ip_header_start + 18:ip_header_start + 20]      
    protocol = int(protocol_hex, 16)
    return protocol, total_length

def classifier(hex_string):
    ether_type_hex = hex_string[24:28]
    ether_type_int = int(ether_type_hex, 16)
    
    if ether_type_int == 0x0800:  # IPv4
        protocol_hex = hex_string[46:48]
        protocol = int(protocol_hex, 16)
        if protocol == 1:
            icmp_type_hex = hex_string[68:70]
            icmp_type = int(icmp_type_hex, 16)
            return "ICMP Reply" if icmp_type == 0 else "ICMP Request" if icmp_type == 8 else "ICMP Other"
        else:
            return "Not an ICMP packet"
    elif ether_type_int == 0x0806:  # ARP
        arp_opcode_hex = hex_string[40:44]
        arp_opcode = int(arp_opcode_hex, 16)
        return "ARP Request" if arp_opcode == 1 else "ARP Reply" if arp_opcode == 2 else "ARP Other"
    return "Unknown Packet Type"

def format_packet_hex(packet_hex, length=128):
    return packet_hex[:length].ljust(length, '0')

def save_packet_to_file(packet_hex, filename):
    with open(filename, 'a') as file:
        file.write(f"{format_packet_hex(packet_hex)}\n")

def analyze_packets_from_file(filename):
    protocol_distribution = defaultdict(int)
    packet_sizes = []
    packet_counters = {"ICMP Reply": 0, "ICMP Request": 0, "ARP Request": 0, "ARP Reply": 0}
    
    output_dir = "megacleaned_datasets"
    os.makedirs(output_dir, exist_ok=True)
    
    filename1 = filename.split('/')[1] 
    filename1 = filename1.split(".")[0]
    filename1 = filename1.split("_")[0]  #getting just the name
    
    output_file = os.path.join(output_dir, f"{filename1}megacleaned.txt")
    if not os.path.exists(output_file):
        open(output_file, 'w').close()
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    for i in range(0, len(lines), 2):
        timestamp = lines[i].strip()
        packet_hex = lines[i + 1].strip()
        protocol, packet_size = extract_packet_info(packet_hex)
        classic = classifier(packet_hex)
        
        if classic in packet_counters:
            packet_counters[classic] += 1
            save_packet_to_file(packet_hex, output_file)
        
        protocol_distribution[protocol] += 1
        packet_sizes.append(packet_size)
    
    total_packets = len(packet_sizes)
    avg_packet_size = sum(packet_sizes) / total_packets if total_packets > 0 else 0
    max_packet_size = max(packet_sizes, default=0)
    min_packet_size = min(packet_sizes, default=0)
    
    protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
    protocol_percentage = {
        protocol_map.get(proto, f"Unknown({proto})"): (count / total_packets) * 100
        for proto, count in protocol_distribution.items()
    }
    
    print(f"Total Packets: {total_packets}")
    print(f"Average Packet Size: {avg_packet_size:.2f} bytes")
    print(f"Max Packet Size: {max_packet_size} bytes")
    print(f"Min Packet Size: {min_packet_size} bytes")
    for packet_type, count in packet_counters.items():
        print(f"{packet_type}: {count}")
    print(f"Selected Packets have been saved to {output_file}\n")


def main():
    # Process all packet files in cleaned_datasets
    dataset_dir = "cleaned_datasets"
    # os.makedirs(dataset_dir, exist_ok=True)

    
    for filename in capture.capture_file_list:    #read off the capture files only 
        print("AAAAAAAAAA", filename)
        filename = filename.split('/')[1] 
        filename = filename.split(".")[0]
        # file_path = os.path.join(dataset_dir, filename)
        file_path = os.path.join(dataset_dir, f"{os.path.basename(filename)}_cleaned.txt")
        print(file_path)
        if os.path.isfile(file_path):
            print("YESS")
            analyze_packets_from_file(file_path)

# main()
