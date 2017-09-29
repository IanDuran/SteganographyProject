import socket, sys

udpIP = "127.0.0.1"
udpPort = 5005
defaultHiddenBits = 4

if len(sys.argv) > 1:  # Get the amount of hidden bits from arguments
    hiddenBits = sys.argv[1]
else:  # Use default hidden bits
    hiddenBits = defaultHiddenBits

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP

while True:

    message = input("Enter message to transmit: ")

    if message == "fin":
        break

    while True:
        secretMessage = input("Enter a valid secret message number: ")

        # Secret message is only valid if it is a number and can be created from the hidden bits
        if secretMessage.isdigit() and int(secretMessage) < pow(2, hiddenBits):
            break

    # If length of message is less than the secret message then we can only add chars
    if len(message) <= int(secretMessage):
        spacesToAdd = int(secretMessage) - len(message)
        for i in range(0, spacesToAdd):
            message = message + " "

    else:
        residue = len(message) % pow(2, hiddenBits)
        difference = residue - int(secretMessage)

        # Based on the difference you do one of to things
        if abs(difference) < pow(2, hiddenBits) / 2:

            # if difference is negative we append to the message the amount needed
            if difference < 0:
                for i in range(0, abs(difference)):
                    message = message + " "

            # if difference is positive we delete enough characters
            else:
                message = message[:-difference]
        else:

            # if difference is negative we delete enough characters
            if difference < 0:
                message = message[:-((pow(2,hiddenBits) - int(secretMessage)) + residue)]

            # if difference is positive we append to the message the amount needed
            else:
                for i in range(0, (pow(2,hiddenBits) - residue) + int(secretMessage)):
                    message = message + " "

    print(len(message) % 16, message)

    sock.sendto(message.encode('utf-8'), (udpIP, udpPort))

sock.sendto(message.encode('utf-8'), (udpIP, udpPort))
