from collections import defaultdict

def extract_packet_info(packet_hex):
    
    
    ethernet_header_length = 14 * 2  # 14 bytes, each byte is 2 hex characters
    
    # IP header starts at byte 14 (i.e., at hex index 28)
    ip_header_start = ethernet_header_length

    
    # The total length field in IPv4 is 2 bytes (4 hex digits) after the differenciated services field
    # so to get that we start at IP header + 4 hex characters, and then add 4 more characters laters
    total_length_hex = packet_hex[ip_header_start + 4:ip_header_start + 8]
    total_length = int(total_length_hex, 16)  # Convert hex string to integer

    # Protocol field (1 byte, 2 hex digits) is at byte 9 of the IP header
    protocol_hex = packet_hex[ip_header_start + 18:ip_header_start + 20]      
    protocol = int(protocol_hex, 16)  # Convert hex string to integer (protocol number)

    return protocol, total_length

def classifier(hex_string):
    # Extract the EtherType field (bytes 12-13 in the Ethernet header, hex positions 24-27)
    ether_type_hex = hex_string[24:28]
    ether_type_int = int(ether_type_hex, 16)

    # Check for ICMP (0x0800) or ARP (0x0806)
    if ether_type_int == 0x0800:  # IPv4
        # Check the protocol field (hex positions 46-47)
        protocol_hex = hex_string[46:48]
        protocol = int(protocol_hex, 16)
        
        if protocol == 1:  # ICMP
            # Check the ICMP type field (byte 34 in the ICMP header, hex positions 68-69)
            icmp_type_hex = hex_string[68:70]
            icmp_type = int(icmp_type_hex, 16)
            
            if icmp_type == 0:
                #print("ICMP Reply")
                return "ICMP Reply"
            elif icmp_type == 8:
                #print("ICMP Req")
                return "ICMP Request"
            else:
                return "ICMP Other"
        else:
            return "Not an ICMP packet"
    
    elif ether_type_int == 0x0806:  # ARP
        # Check the ARP opcode (bytes 20-21 in the ARP header, hex positions 40-43)
        arp_opcode_hex = hex_string[40:44]
        arp_opcode = int(arp_opcode_hex, 16)
        
        if arp_opcode == 1:
            #print("ARP Request")
            return "ARP Request"
        elif arp_opcode == 2:
            #print("ARP Reply")
            return "ARP Reply"
        else:
            return "ARP Other"
    
    return "Unknown Packet Type"

def format_packet_hex(packet_hex, length=128):
    
    if len(packet_hex) > length:
        return packet_hex[:length]
    # Pad with '0's if shorter than 128 characters, new function unlocked wooohooo
    return packet_hex.ljust(length, '0')

def save_packet_to_file(packet_hex, filename):
    with open(filename, 'a') as file:
        formatted_packet_hex = format_packet_hex(packet_hex)
        file.write(f"{formatted_packet_hex}\n")

def analyze_packets_from_file(filename, selected_packet_file):
    protocol_distribution = defaultdict(int)
    packet_sizes = []

    packet_counters = {
    "ICMP Reply": 0,
    "ICMP Request": 0,
    "ARP Request": 0,
    "ARP Reply": 0
    }

    #selected_packet_file = "megacleanfoobar.txt"
    open(selected_packet_file, 'w').close()  # Open in 'w' mode to clear contents
    
    # Read the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Iterate over the file, two lines at a time (timestamp and packet hex)
    for i in range(0, len(lines), 2):
        timestamp = lines[i].strip()  # First line is the timestamp
        packet_hex = lines[i + 1].strip()  # Second line is the hex data

        # Extract protocol and size from the packet hex string
        protocol, packet_size = extract_packet_info(packet_hex)

        classic = classifier(packet_hex)
        
        
        if classic in ["ICMP Reply", "ICMP Request", "ARP Request", "ARP Reply"]:
            packet_counters[classic] += 1
            #print(classic)
            save_packet_to_file(packet_hex, selected_packet_file)
        
        # Count protocol occurrences
        protocol_distribution[protocol] += 1
        
        # Collect packet sizes
        packet_sizes.append(packet_size)
    
    # Calculate basic statistics for packet sizes
    total_packets = len(packet_sizes)
    total_size = sum(packet_sizes)
    avg_packet_size = total_size / total_packets if total_packets > 0 else 0
    max_packet_size = max(packet_sizes, default=0)
    min_packet_size = min(packet_sizes, default=0)

    # Protocol mapping for human-readable output
    protocol_map = {
        1: "ICMP",
        6: "TCP",
        17: "UDP"
    }
    
    # Calculate protocol distribution percentages
    protocol_percentage = {
        protocol_map.get(proto, f"Unknown({proto})"): (count / total_packets) * 100
        for proto, count in protocol_distribution.items()
    }

    # Print the results
    print(f"Total Packets: {total_packets}")
    print(f"Average Packet Size: {avg_packet_size:.2f} bytes")
    print(f"Max Packet Size: {max_packet_size} bytes")
    print(f"Min Packet Size: {min_packet_size} bytes")
    print("Protocol Distribution (percentage):")
    # for proto, percent in protocol_percentage.items():
    #     print(f"  {proto}: {percent:.2f}%")

    for packet_type, count in packet_counters.items():
        print(f"{packet_type}: {count}")
    
    print(f"\n\n Selected Packets have been saved to {selected_packet_file}")

# Call the function with the path to your file
#analyze_packets_from_file('cleaned_datasets\dataset2_cleaned.txt', 'megacleaned_datasets\dataset2mega_cleaned.txt')
