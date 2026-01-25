

def packet_choice(predictions):
    print("Predicted classes:", predictions[:10])


    packet_type = "No match"
    packet_ctr = 0
    icmp_req_ctr, icmp_rep_ctr, arp_req_ctr, arp_rep_ctr = 0, 0, 0, 0
    no_match_ctr = 0

    # # Ensure predictions are integers (class labels)
    # predictions = predictions.argmax(dim=1).cpu().numpy()

    # predictions = predictions.argmax(axis=1) 

    for i in predictions:
        if i == 0:
            packet_type = "ICMP Echo"
            icmp_req_ctr += 1
        elif i == 1:
            packet_type = "ICMP Reply"
            icmp_rep_ctr += 1
        elif i == 2:
            packet_type = "ARP Request"
            arp_req_ctr+=1
        elif i == 3:
            packet_type = "ARP Reply"
            arp_rep_ctr +=1
        else:
            packet_type = "Other"
            no_match_ctr += 1

        packet_ctr += 1

    # Summary of packet classification
    print()
    print("Total packets :", packet_ctr)
    print("0-ICMP req packets :", icmp_req_ctr)
    print("1-ICMP rep packets:", icmp_rep_ctr)
    print("2-ARP request packets :", arp_req_ctr)
    print("3-Arp reply packets :", arp_rep_ctr)
    print("Other packets :", no_match_ctr)




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


