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

# Receive Server Response
response = clientSocket.recv(1024).decode()
print("Server response:", response)

# Check Response
if response.startswith("200 OK"):
    print("CSP successful. Ready for Measurement Phase.")
else:
    print("CSP failed.")

clientSocket.close()