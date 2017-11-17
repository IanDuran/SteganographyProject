import socket, timeit

udpIP = "127.0.0.1"
udpPort = 5005
defaultHiddenBits = 4

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
sock.bind((udpIP, udpPort))

start = 0
first = True

while True:

    #  Final ascii character to print
    asciiValue = 0

    #  Receive data and get the actual string from it
    data = sock.recvfrom(1024)  # buffer size is 1024 bytes
    if first:
        start = timeit.timeit()
        first = False
    realData = data[0].decode('UTF-8')

    #  if message is fin then program ends
    if realData == "fin":
        break

    #  Get length of message % 16 and multiply it by 16( or "move" the bits 4 spaces to the right)
    secretMessage = len(realData) % pow(2, 4)
    asciiValue += secretMessage * pow(2, 4)

    #  Receive data and get the actual string from it
    data = sock.recvfrom(1024)  # buffer size is 1024 bytes
    realData = data[0].decode('UTF-8')

    #  if message is fin then program ends
    if realData == "fin":
        break

    # Get length of message % 16 and add it to the total ascii value
    secretMessage = len(realData) % pow(2, 4)
    asciiValue += secretMessage

    print(chr(asciiValue), asciiValue)

end = timeit.timeit()
print("Execution time: " + str(end - start))
