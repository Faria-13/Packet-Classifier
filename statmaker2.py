from collections import defaultdict

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

            # Skip empty or too-short lines
            if len(packet_hex) < 28:  #cannot contain a ethernet header or information
                continue

            total_packets += 1

            try:
                # EtherType is bytes 12–13 → hex chars 24–28
                ether_type = int(packet_hex[24:28], 16)

                # STP
                llc = packet_hex[28:34]  # 3 bytes → 6 hex chars
                if llc == "424203":
                    counters["STP"] += 1
                    continue

                # ARP
                if ether_type == 0x0806:
                    counters["ARP"] += 1
                    continue

                # IPv4
                if ether_type == 0x0800:
                    # IP protocol field = byte 23 → hex chars 46–48
                    protocol = int(packet_hex[46:48], 16)

                    if protocol == 1:
                        counters["ICMP"] += 1
                    elif protocol == 6:
                        counters["TCP"] += 1
                    elif protocol == 17:
                        counters["UDP"] += 1
                    else:
                        counters["Other"] += 1

            except ValueError:
                counters["Other"] += 1

    # ---- Print statistics ----
    print("\nPacket statistics for:", filename)
    print("Total packets:", total_packets)
    print()

    for pkt_type, count in counters.items():
        percent = (count / total_packets * 100) if total_packets else 0
        print(f"{pkt_type:6}: {count:6} ({percent:6.2f}%)")


def classifier(packet_hex):
    # Minimum Ethernet header check (14 bytes = 28 hex chars)
    if len(packet_hex) < 28:
        return "Other"

    # EtherType or Length field
    ether_type_hex = packet_hex[24:28]
    ether_type_int = int(ether_type_hex, 16)

    # Ethernet II frames
  
    if ether_type_int == 0x0800:  # IPv4
        # Need enough bytes to read protocol field
        if len(packet_hex) < 48:
            return "Other"

        protocol_hex = packet_hex[46:48]
        protocol = int(protocol_hex, 16)

        if protocol == 1:
            return "ICMP"
        elif protocol == 6:
            return "TCP"
        elif protocol == 17:
            return "UDP"

    elif ether_type_int == 0x0806:  # ARP
        return "ARP"

   
    else:
        # Need LLC header
        
        llc = packet_hex[28:34]  # 3 bytes → 6 hex chars
        if llc == "424203":
            return "STP"
        
    return "Other"


#statmaker("cleaned_datasets/mixed_cleaned.txt") #Packet-Classifier-\cleaned_datasets\mixed_cleaned.txt
