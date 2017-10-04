import socket, sys, time

udpIP = "127.0.0.1"
udpPort = 5005
udpPort2 = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP

#  Iterator to know which message we are sending
it = 1

#  If there is no file end program
if len(sys.argv) > 1:
    with open(sys.argv[1]) as mesFile:
        for line in mesFile:

            #  If end of file finish transmission
            if len(line) == 1:
                break

            #  Remove the new line character
            value = ord(line[:-1])
            print(value)
            power = 7

            for i in range(0, 8):

                #  If bit is one then send through udpPort2
                if value >= pow(2, power):
                    message = "Mensaje " + str(it)
                    sock.sendto(message.encode('utf-8'), (udpIP, udpPort2))
                    value -= pow(2, power)
                    #  print(udpPort2)

                #  Otherwise send through udpPort
                else:
                    message = "Mensaje " + str(it)
                    sock.sendto(message.encode('utf-8'), (udpIP, udpPort))
                    #  print(udpPort)

                #  Give a little bit of time to the receiver
                time.sleep(0.05)
                power -= 1
                it += 1

    print("Message Sent")
    sock.sendto("fin".encode('utf-8'), (udpIP, udpPort))
    sock.sendto("fin".encode('utf-8'), (udpIP, udpPort2))
