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

    while True:
        connectionSocket, addr = serverSocket.accept()
        print(f"Created a connection with {addr}")
        # This is the dedicated socket
        payload = connectionSocket.recv(1024).decode()
        parsed = payload.split(" ")
        # <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
        protocol_phase = parsed[0]
        measurement_type = parsed[1]
        num_probes = parsed[2]
        message_size = parsed[3]
        server_delay = parsed[4]

        print(
            f"protocol phase: {protocol_phase}\nmeasurement type: {measurement_type}\nnumber of probes: {num_probes}\nmessage size: {message_size}\nserver delay: {server_delay}"
        )

        # capitalizedSentence = payload.upper()
        # Check if the connection is valid.
        connectionSocket.send(capitalizedSentence.encode())
        connectionSocket.close()
        print("Closed a connection")
except KeyboardInterrupt:
    print("Closing server...")
except OSError as e:
    print("Error: ", e)
except Exception as e:
    print("Some error:", e)
