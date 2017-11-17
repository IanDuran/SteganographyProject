import socket, threading, timeit

udpIP = "127.0.0.1"
udpPort = 5005
udpPort2 = 5006

value = 0
power = 7
first = True
start = 0
message = ""


def listen(host, port):

    global value
    global power
    global first
    global start
    global message
    lock = threading.Lock()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
    sock.bind((host, port))

    while True:
        data = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if first:
            lock.acquire()
            start = timeit.timeit()
            first = False
            lock.release()

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
            message = message + chr(value)
            power = 7
            value = 0

        lock.release()


t1 = threading.Thread(target=listen,args=('localhost', udpPort))
t2 = threading.Thread(target=listen,args=('localhost', udpPort2))

t1.start()
t2.start()

t1.join()
t2.join()

end = timeit.timeit()
print("Execution time: " + str(end - start))
print(message)
