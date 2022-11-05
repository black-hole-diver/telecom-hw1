import socket
import select
import sys

# HDZSFE PANTA Wittawin
# HW1.1

# simple odd even function
def is_even(n):
    if n % 2 == 0:
        return True;
    if n % 2 == 1:
        return False;

def main():
    name = ""
    record = {} # dictionary
    inputs = []
    buffer = 1024
    port = int(sys.argv[1]) # get port number from argv[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', port))

    s.listen(10) # 10 connections max

    inputs.append(s) # add the server to the inputs
    print("\nSERVER WORKING\n")

    while 1:
        readable, writable, exceptionals = select.select(inputs, [], [])
        
        for sock in readable:
            # add new connection
            if sock == s:
                conn, addr = s.accept()
                name = conn.recv(buffer).decode("utf-8") # get name of the client
                inputs.append(conn) # get conn to the inputs
                record[addr]=""

                # name already exits
                if name in record.values():
                    conn.send("Username already taken".encode())
                    del record[addr]
                    inputs.remove(conn)
                    conn.close()
                    continue
                # new name
                else:
                    record[addr]=name
                    print("Cliet (%s,%s) connected" %addr, " [", record[addr],"]")
                    conn.send("Welcome to the room (Enter 'quit' to quit the server)".encode())

            # reply to text from sock
            # sock is already connected
            else:
                try:
                    # get text
                    data = sock.recv(buffer).decode("utf-8")
                    data_enter = data[:data.index("\n")]
                    i,p = sock.getpeername() # get sock name
                    print("Gotten message from (%s, %s)" % (i,p))
                    print(data)

                    # quiting
                    if data_enter == 'quit':
                        msg = "[" + record[(i,p)] + " left the server" + "]"
                        print(msg)
                        del record[(i,p)]
                        inputs.remove(sock)
                        sock.close()
                        continue;

                    # decide the number oddity
                    else:
                        try:
                            if int(data) == 0:
                                sock.send("Number is zero".encode())
                            else:
                                if is_even(int(data)):
                                    sock.send("Number is EVEN".encode())
                                elif not is_even(int(data)):
                                    sock.send("Number is ODD".encode())
                        except:
                            sock.send("Text is not convertible to integer".encode()) # not numeric

                except:
                    # some unexpected error / disconnection from server
                    i, p = sock.getpeername()
                    print("Client (%s,%s) left the server (error)" % (i,p))
                    del record[(i,p)]
                    inputs.remove(sock)
                    sock.close()
                    continue
    s.close()

if __name__ == "__main__":
    main() # run main