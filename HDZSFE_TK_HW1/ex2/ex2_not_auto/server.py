from random import randint
import socket
import select
import sys
import time

# HDZSFE PANTA Wittawin
# HW1.2

# simple odd even function
def check_less(goal, guess):
    return int(goal) > int(guess);

def check_more(goal, guess):
    return int(goal) < int(guess);

def check_equal(goal, guess):
        return int(goal) == int(guess)

def main():
    goal0 = randint(1, 100)
    goal = str(goal0)
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
                            signal = data[0]
                            guess = data[1:data.index("\n")]
                            if signal == '=':
                                if check_equal(goal, guess):
                                    sock.send("You win".encode())
                                    print("(%s,%s) won the game!" % (i,p))
                                    print("Everyone left the server")
                                    s.close();
                                if not check_equal(goal, guess):
                                    sock.send("You lose".encode())
                                    sock.send("\nWould you like to continue? Yes/No".encode())
                                    answer = sock.recv(buffer).decode("utf-8")
                                    if answer[:answer.index("\n")] == 'Yes':
                                        sock.send("You can have a second chance!".encode())
                                        continue;
                                    if answer[:answer.index("\n")] == 'No':
                                        msg = "[" + record[(i,p)] + " left the server" + "]"
                                        print(msg)
                                        del record[(i,p)]
                                        inputs.remove(sock)
                                        sock.close()
                                        continue;
                            if signal == "<":
                                if check_more(goal, guess):
                                    sock.send("Yes".encode())
                                else:
                                    sock.send("No".encode())
                            if signal == ">":
                                if check_less(goal, guess):
                                    sock.send("Yes".encode())
                                else:
                                    sock.send("No".encode())
                        except:
                            sock.send("Not a correct form".encode())

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