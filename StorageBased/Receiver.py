import socket

udpIP = "127.0.0.1"
udpPort = 5005
defaultHiddenBits = 4

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
sock.bind((udpIP, udpPort))

while True:

    asciiValue = 0

    data = sock.recvfrom(1024)  # buffer size is 1024 bytes
    realData = data[0].decode('UTF-8')

    print(realData)
    if realData == "fin":
        break

    secretMessage = len(realData) % pow(2, 4)
    asciiValue += secretMessage * pow(2, 4)

    data = sock.recvfrom(1024)  # buffer size is 1024 bytes
    realData = data[0].decode('UTF-8')

    if realData == "fin":
        break

    secretMessage = len(realData) % pow(2, 4)
    asciiValue += secretMessage

    print(chr(asciiValue))
