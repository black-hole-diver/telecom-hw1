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
    buffer = 1024
    port = int(sys.argv[1]) # get port number from argv[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ucp connection to connect to proxy
    s.bind(('localhost', port))

    #s.listen(10) # 10 connections max

    print("\nSERVER WORKING\n")

    while 1:

        data1, addr_client = s.recvfrom(buffer) # receive data
        print("Gotten message from (%s)" % (repr(addr_client)))
        print(data1.decode("utf-8"))
        try:
            # get text
            data = data1.decode("utf-8")
            data_enter = data[:data.index("\n")]

            # send text
            try:
                if int(data) == 0:
                    s.sendto("Number is zero".encode(), addr_client)
                else:
                    if is_even(int(data)):
                        s.sendto("Number is EVEN".encode(), addr_client)
                    elif not is_even(int(data)):
                        s.sendto("Number is ODD".encode(), addr_client)
            except:
                s.sendto("Text is not convertible to integer".encode(), addr_client) # not numeric

        except:
            # some unexpected error / disconnection from server
            print("Client left the server (error)")
            continue
    s.close()

if __name__ == "__main__":
    main() # run main