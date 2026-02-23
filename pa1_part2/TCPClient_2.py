from socket import *

serverName = input("Input host name or IP: ")
# serverName = "127.0.0.1"
serverPort = int(input("Input port number: "))
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# TODO: refactor to use argparse? could be useful

# after setting up the connection, send a message with the following format
# <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
#
measurement_type = input("Input 'rtt' or 'tput': ")
num_probes = input("Input number of probes: ")
msg_size = int(input("Input bytes in payload: "))
server_delay = int(input("Input amount of time server shoudl wait: (default 0)"), 0)

# clientSocket.send(TODO HERE)
modifiedSentence = clientSocket.recv(1024)
print("From Server:", modifiedSentence.decode())
clientSocket.close()
