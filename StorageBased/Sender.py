import socket, sys, time


def hide_message(payload, secret_information):
    # If length of message is less than the secret message then we can only add chars
    if len(payload) <= int(secret_information):
        spaces_to_add = int(secret_information) - len(payload)
        for i in range(0, spaces_to_add):
            payload = payload + " "

    else:
        residue = len(payload) % pow(2, hiddenBits)
        difference = residue - int(secret_information)

        # Based on the difference you do one of to things
        if abs(difference) < pow(2, hiddenBits) / 2:

            # if difference is negative we append to the message the amount needed
            if difference < 0:
                for i in range(0, abs(difference)):
                    payload = payload + " "

            # if difference is positive we delete enough characters
            else:
                payload = payload[:-difference]
        else:

            # if difference is negative we delete enough characters
            if difference < 0:
                payload = payload[:-((pow(2, hiddenBits) - int(secret_information)) + residue)]

            # if difference is positive we append to the message the amount needed
            else:
                for i in range(0, (pow(2, hiddenBits) - residue) + int(secret_information)):
                    payload = payload + " "

    print(len(payload) % 16, payload)

    return payload


udpIP = "127.0.0.1"
udpPort = 5005
defaultHiddenBits = 4

hiddenBits = defaultHiddenBits

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP

#  We are working from console
if len(sys.argv) == 1:
    while True:

        message = input("Enter message to transmit: ")

        #  Is message is fin then program ends
        if message == "fin":
            sock.sendto(message.encode('utf-8'), (udpIP, udpPort))
            break

        while True:
            secretMessage = input("Enter a valid secret message number: ")

            # Secret message is only valid if it is a number and can be created from the hidden bits
            if secretMessage.isdigit() and int(secretMessage) < pow(2, hiddenBits):
                break

        #  hide secret message in payload
        message = hide_message(message, secretMessage)

        #  send message
        sock.sendto(message.encode('utf-8'), (udpIP, udpPort))

#  We are working with a file
else:
    start = time.time()
    with open(sys.argv[1]) as mesFile:
        for line in mesFile:
            with open("messages.txt") as mes:
                for i, line2 in enumerate(mes):
                    if i == (int(line) - 1):
                        #  send message
                        sock.sendto(line2[:-1].encode('utf-8'), (udpIP, udpPort))
    print("Message Sent")
    sock.sendto("fin".encode('utf-8'), (udpIP, udpPort))
    end = time.time()
    print("Execution time: " + str(end - start) + " Init "+str(start) +" Fin" + str(end))





