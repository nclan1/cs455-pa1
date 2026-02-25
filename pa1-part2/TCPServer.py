from socket import *

def recv_bytes(conn):
    data = b""
    # newline is out delimiter and receive up to 1024 bytes
    while b"\n" not in data:
        chunk = conn.recv(1024)
        if not chunk:
            return None
        data += chunk
    line, _rest = data.split(b"\n", 1)
    return line.decode(errors="replace")

serverPort = int(input("Input port number: "))
serverSocket = socket(AF_INET, SOCK_STREAM)

try:
    serverSocket.bind(("", serverPort))
except OSError as e:
    print("Error: ", e)
    exit(1)

serverSocket.listen(1)
print("The server is ready to receive on port", serverPort)

try:
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Created a connection from", addr)

        # receive message
        line = recv_bytes(connectionSocket)
        if line is None:
            connectionSocket.close()
            continue

        parts = line.strip().split()

        valid = True
        if len(parts) != 5:
            valid = False
        else:
            phase, mtype, nprobes_s, msgsize_s, delay_s = parts
            if phase != "s":
                valid = False
            if mtype not in ("rtt", "tput"):
                valid = False
            try:
                nprobes = int(nprobes_s)
                msgsize = int(msgsize_s)
                delay = int(delay_s)
                if nprobes <= 0 or msgsize < 0 or delay < 0:
                    valid = False
            except ValueError:
                valid = False

        # response
        if valid:
            print(f"CSP succesfultype={mtype}, probes={nprobes}, msg_size={msgsize}, delay={delay}")
            connectionSocket.sendall(b"200 OK: Ready")
            # keep connection open (next phase later)
        else:
            connectionSocket.sendall(b"404 ERROR: Invalid Connection Setup Message")
            connectionSocket.close()
            print("invalid CSP")

except KeyboardInterrupt:
    print("Closing server...")
finally:
    serverSocket.close()