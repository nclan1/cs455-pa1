import argparse
from socket import *

parser = argparse.ArgumentParser(
    description="Python script to set up the server to perform RTT and Throughput measurements."
)

parser.add_argument(
    "--host",
    help="The hostname / IP address to set up server. Default: localhost",
    default="localhost",
)

parser.add_argument(
    "-p",
    "--port",
    type=int,
    help="The port number to set up server at. Default: 9090.",
    default=9090,
)

args = parser.parse_args()

# "" means listening on all available network interface
try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((args.host, args.port))
    serverSocket.listen(1)
    print(f"The server is ready to receive on {args.host}:{args.port}")
except OSError as e:
    print("Error: ", e)


try:
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Created a connection...")
        # This is the dedicated socket
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()
        print("Closed a connection")
except KeyboardInterrupt:
    print("Closing server...")
except Exception as e:
    print("Some error:", e)
