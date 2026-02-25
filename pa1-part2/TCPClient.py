import time
from socket import *

serverName = input("Input host name or IP: ")
serverPort = int(input("Input port number: "))

measurement_type = input("Measurement type (rtt/tput): ")
num_probes = int(input("Number of probes: "))
msg_size = int(input("Message size (bytes): "))
server_delay = int(input("Server delay (ms): "))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

setup_msg = f"s {measurement_type} {num_probes} {msg_size} {server_delay}\n"

#Send CSP Message
clientSocket.sendall(setup_msg.encode())

def recv_line(sock, buf):
    while b"\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            return None, buf
        buf += chunk
    line, buf = buf.split(b"\n", 1)
    return line.decode(errors="replace"), buf

# Receive Server Response
buf = b""
response, buf = recv_line(clientSocket, buf)
print("Server response:", response)

# Check Response
if response.startswith("200 OK"):
    print("CSP successful, now MP:")

    total_rtt = 0.0
    total_tput = 0.0

    for seq in range(1, num_probes + 1):

        payload = "a" * msg_size
        probe_msg = f"m {seq} {payload}\n"

        t_start = time.perf_counter()

        clientSocket.sendall(probe_msg.encode())

        echo, buf = recv_line(clientSocket, buf)

        t_end = time.perf_counter()

        rtt = t_end - t_start
        total_rtt += rtt

        if measurement_type == "rtt":
            print(f"Probe {seq} RTT: {rtt:.6f} seconds")
        if measurement_type == "tput":
            tput_bps = (msg_size * 8) / rtt
            total_tput += tput_bps
            print(f"Probe {seq} throughput: {tput_bps/1e6:.3f} Mbps")

    if measurement_type == "rtt":
        avg_rtt = total_rtt / num_probes
        print(f"\nAverage RTT: {avg_rtt:.6f} seconds")

    if measurement_type == "tput":
        print(f"\nAverage Throughput: {(total_tput/num_probes)/1e6:.3f} Mbps")

else:
    print("CSP failed.")

clientSocket.close()