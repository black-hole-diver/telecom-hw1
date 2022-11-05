import socket
import select
import sys

def close_all(inputs):
    for s in inputs:
        s.close();

port_server = int(sys.argv[1])
port_proxy = int(sys.argv[2])


server_addr = ('localhost', port_server)

print("PROXY SERVER IS RUNNING")

# socket to server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket for client
proxy_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

inputs = [server]
server.bind(('localhost', port_proxy))
server.setblocking(False)
server.listen(10) # 10 clients at time


while 1:
    
    readable, writable, exceptional = select.select(inputs, [], [])
    
    for s in readable:
        # new client
        if s == server:
            client, client_addr = s.accept()
            inputs.append(client)
            print("Connected: ", client_addr)
        
        # get data / send data
        else:
            # get data
            data = s.recv(1024)
            
            # bad data
            if not data:
                print("Client quit")
                inputs.remove(s)
                s.close()
                
            # good
            else:
                print("Received from a client: {}".format(data.decode("utf-8")))
                data2 = data.decode("utf-8")
                data_enter = data2[:data2.index("\n")]
                if data_enter == 'quit':
                    close_all(inputs)
                    proxy_client.close();
                proxy_client.sendto(data, server_addr) # send data to server (ucp)
                print("Send data to the server")
                sendtoclient, _ = proxy_client.recvfrom(1024)
                print("Get respond to client")
                s.send(sendtoclient) # send to a client