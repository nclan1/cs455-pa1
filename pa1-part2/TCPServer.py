from socket import *
import time

def recv_bytes(conn, buf):
    while b"\n" not in buf:
        chunk = conn.recv(4096)
        if not chunk:
            return None, buf
        buf += chunk
    line, buf = buf.split(b"\n", 1)
    return line.decode(errors="replace"), buf

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
        buf = b""
        line, buf = recv_bytes(connectionSocket,buf)
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
            connectionSocket.sendall(b"200 OK: Ready\n")
            
            expected_seq = 1

            for _ in range(nprobes):
                mp_line,buf = recv_bytes(connectionSocket,buf)
                if mp_line is None:
                    connectionSocket.close()
                    break

                parts = mp_line.split(" ", 2)
                if len(parts) != 3:
                    connectionSocket.sendall(b"404 ERROR: Invalid Measurement Message\n")
                    connectionSocket.close()
                    break

                phase, seq_s, payload = parts

                # phase check
                if phase != "m":
                    connectionSocket.sendall(b"404 ERROR: Invalid Measurement Message\n")
                    connectionSocket.close()
                    break

                # seq number check
                try:
                    seq = int(seq_s)
                except ValueError:
                    connectionSocket.sendall(b"404 ERROR: Invalid Measurement Message\n")
                    connectionSocket.close()
                    break

                if seq != expected_seq or seq > nprobes:
                    connectionSocket.sendall(b"404 ERROR: Invalid Measurement Message\n")
                    connectionSocket.close()
                    break

                # payload size check (bytes)
                if len(payload.encode()) != msgsize:
                    connectionSocket.sendall(b"404 ERROR: Invalid Measurement Message\n")
                    connectionSocket.close()
                    break

                # delay then echo back same line (with newline)
                if delay > 0:
                    time.sleep(delay / 1000.0)

                connectionSocket.sendall((mp_line + "\n").encode())

                expected_seq += 1
            
            term_line, buf = recv_bytes(connectionSocket, buf)

            if term_line == "t":
                connectionSocket.sendall(b"200 OK: Closing Connection\n")
            else:
                connectionSocket.sendall(b"404 ERROR: Invalid Connection Termination Message\n")

            connectionSocket.close()
            
        else:
            connectionSocket.sendall(b"404 ERROR: Invalid Connection Setup Message\n")
            connectionSocket.close()
            print("invalid CSP")

except KeyboardInterrupt:
    print("Closing server...")
finally:
    serverSocket.close()