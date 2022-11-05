import socket
import select
import sys

def main():
    host = 'localhost'
    port = int(sys.argv[1]) # take number from standard input
    buffer = 1024

    name = input("Enter your name: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to the server
    try:
        s.connect((host,port))
    except:
        print("Cannot connect to the server")
        sys.exit()
    
    s.send(name.encode()) # send the name

    # run
    while 1:
        # inputs are s (server) and standard input
        inputs = [sys.stdin, s]
        readable, writable, exceptional = select.select(inputs, [], [])

        for sock in readable:
            # get data from server
            if sock == s:
                data = sock.recv(buffer).decode("utf-8")
                if not data:
                    print("Disconnected")
                    sys.exit()
                else:
                    print("Message from server: %s" %data)
            # get data from standard input -> send to server s
            else:
                print("Sent message to server: ------>")
                msg=sys.stdin.readline()
                s.send(msg.encode())

if __name__ == "__main__":
    main();