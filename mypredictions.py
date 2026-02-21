

def packet_choice(predictions):
    print("Predicted classes:", predictions[:10])


    packet_type = "No match"
    packet_ctr = 0
    icmp_ctr, tcp_ctr, arp_ctr, udp_ctr = 0, 0, 0, 0
    stp_ctr = 0

    # # Ensure predictions are integers (class labels)
    # predictions = predictions.argmax(dim=1).cpu().numpy()

    # predictions = predictions.argmax(axis=1) 

    for i in predictions:
        if i == 0:
            packet_type = "ICMP"
            icmp_ctr += 1
        elif i == 1:
            packet_type = "TCP"
            tcp_ctr += 1
        elif i == 2:
            packet_type = "ARP"
            arp_ctr+=1
        elif i == 3:
            packet_type = "UDP"
            udp_ctr +=1
        elif i == 4:
            packet_type = "STP"
            stp_ctr += 1

        packet_ctr += 1

    # Summary of packet classification
    print()
    print("Total packets :", packet_ctr)
    print("0-ICMP  packets :", icmp_ctr)
    print("1-TCP  packets :", tcp_ctr)
    print("2-ARP  packets :", arp_ctr)
    print("3-UDP  packets :", udp_ctr)
    print("4-STP  packets :", stp_ctr)




def accuracy(predictions, y_test):

    print("First 20 predictions:", predictions[:20])
    print("First 20 labels     :", y_test[:20])
    accuracy_count = 0
    total  = predictions.shape[0]
    for i in range(total):
        if int(predictions[i]) == int(y_test[i]):   #changed this to be a single list
            accuracy_count += 1

    print("\nTotal Predictions:", total, "Accuracy Count:", accuracy_count)
    print("\nAccuracy of Predictions:", accuracy_count/total)

    accuracy_rate = accuracy_count/total

    return accuracy_rate


