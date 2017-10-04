import socket, threading

udpIP = "127.0.0.1"
udpPort = 5005
udpPort2 = 5006

value = 0
power = 7


def listen(host, port):

    global value
    global power
    lock = threading.Lock()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
    sock.bind((host, port))

    while True:
        data = sock.recvfrom(1024)  # buffer size is 1024 bytes
        realData = data[0].decode('UTF-8')

        #  print("In port ", port, " message: ", realData)

        #  if message is fin then program ends
        if realData == "fin":
            break

        #  Get lock to safely change shared variables
        lock.acquire()

        #  If message came through udpPort2 then it is a 1
        if port == 5006:
            value += pow(2, power)

        power -= 1

        #  Byte completed reset all values
        if power == -1:
            print(chr(value), value)
            power = 7
            value = 0

        lock.release()


threading.Thread(target=listen,args=('localhost', udpPort)).start()
threading.Thread(target=listen,args=('localhost', udpPort2)).start()
