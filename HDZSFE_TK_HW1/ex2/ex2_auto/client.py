import socket
import select
import sys
import time
import math

def avg(low, high):
    r = (low + high) / 2
    return int(r)


host = 'localhost'
port = int(sys.argv[1]) # take number from standard input
buffer = 1024

low = 1
high = 100
sent = 50

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

s.connect((host,port))

# connect to the server
# try:
#     s.connect((host,port))
# except:
#     print("Cannot connect to the server")
#     sys.exit()


inputs = [s]

s.send(">50\n".encode())
print("Sent message to server: ------> >50")


# run
while 1:
    rdb,_,_ = select.select(inputs, [], [])
    for sock in rdb:
        if sock == s:
            data = sock.recv(buffer).decode("utf-8")

            if not data:
                print("Disconnected")
                sys.exit()

            
            if data == "You win" or data == "You lose":
                if data== "You win":
                    print("You win")
                    sys.exit()
                else:
                    print("You lose")
                    sys.exit()
            else:
                # details
                print("Data from server: " + data)
                print("upper bound: " + str(high))
                print("lower bound: " + str(low))

                try:
                    if (low + 1) != high:
                        if data == "Yes":
                            # change lwb
                            low = sent
                            
                            sent = math.ceil((low + high) / 2)
                            msg = ">" + str(sent) + "\n"
                            sock.send(msg.encode())
                            print("Sent message to server: ------> %s" % msg)
                        if data == "No":
                            # change lwb
                            high= sent
                            
                            sent = math.ceil((low + high) / 2)
                            msg = ">" + str(sent) + "\n"
                            sock.send(msg.encode())
                            print("Sent message to server: ------> %s" % msg)
                        
                        time.sleep(1)
                    else:
                        msg = "=" + str(high) + "\n"
                        sock.send(msg.encode())
                        print("Sent message to server: ------> %s" % msg)
                        time.sleep(1)
                except:
                    print("Bad format error")
                    break;