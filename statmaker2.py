from collections import defaultdict

# this is to have a understanding a test file, has to cleaned though 
def statmaker(filename):
    counters = {
        "ICMP": 0,
        "TCP": 0,
        "UDP": 0,
        "ARP": 0,
        "STP": 0,
        "Other": 0
    }

    total_packets = 0

    with open(filename, "r") as f:
        for line in f:
            packet_hex = line.strip().lower()
            if not packet_hex:
                continue
            total_packets += 1

            try:
                ether_type = int(packet_hex[24:28], 16)
                llc = packet_hex[28:34]

                # Check for STP first since it uses LLC and doesn't have a standard EtherType
                if llc == "424203":
                    pkt_type = "STP"

                elif ether_type == 0x0806:
                    pkt_type = "ARP"

                elif ether_type == 0x0800:  # IPv4
                    protocol = int(packet_hex[46:48], 16)

                    if protocol == 1:
                        pkt_type = "ICMP"
                    elif protocol == 6:
                        pkt_type = "TCP"
                    elif protocol == 17:
                        pkt_type = "UDP"
                    else:
                        pkt_type = "Other"

                else:
                    pkt_type = "Other"
                    print("Error processing packet:", packet_hex)

                counters[pkt_type] += 1

            except Exception:
                counters["Other"] += 1
                print("Error processing packet:", packet_hex)

    
    print(f"\nPacket statistics for: {filename}")
    print(f"Total packets: {total_packets}\n")

    for pkt_type, count in counters.items():
        percent = (count / total_packets * 100) if total_packets else 0
        print(f"{pkt_type:6}: {count:6} ({percent:6.2f}%)")


#this function is for parsing each line 

def classifier(packet_hex):
    ether_type_hex = packet_hex[24:28]
    ether_type_int = int(ether_type_hex, 16)

    llc = packet_hex[28:34]    #for stp
    if llc == "424203":
       
        return "STP"
    
    elif ether_type_int == 0x0800:  # IPv4
        protocol_hex = packet_hex[46:48]
        protocol = int(protocol_hex, 16)
        
        
        if protocol == 1:
            icmp_type_hex = packet_hex[68:70]
            return "ICMP"
        
        elif protocol == 17:        # UDP
            return "UDP"
        
        elif protocol == 6:   # TCP 
            return "TCP"
            
        
    elif ether_type_int == 0x0806:
        arp_opcode_hex = packet_hex[40:44]
        arp_opcode = int(arp_opcode_hex, 16)
        return "ARP"
    
    return "Other"


# statmaker("cleaned_datasets/lucky_cleaned.txt") 