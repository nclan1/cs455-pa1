import argparse
from socket import *

# set up parser
parser = argparse.ArgumentParser(
    description="Python script acting as the client to perform RTT and Throughput measurement."
)

parser.add_argument(
    "--host",
    help="The hostname / IP address to connect to. Default: localhost",
    default="localhost",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    help="The port number to connect to. Default: 9090.",
    default=9090,
)

parser.add_argument(
    "-ms",
    "--measurement-type",
    help="Specify whether to compute the RTT (Round Trip Time) or throughput.",
    choices=["rtt", "tput"],
    required=True,
)

parser.add_argument(
    "-n",
    "--probes",
    type=int,
    help="Number of measurement probes that the server should expect to receive",
    required=True,
)

parser.add_argument(
    "-s", "--size", type=int, help="Size of the probe's payload in bytes", required=True
)

parser.add_argument(
    "-d",
    "--delay",
    type=int,
    help="Amount of time that the server should wait before echoing the message back. Default: 0",
    default=0,
)

args = parser.parse_args()
# print(args)

# start the socket connection
try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((args.host, args.port))

    # after setting up the connection, send a message with the following format
    # <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n

    # ----------------FIRST STEP----------------
    init_message = f"s {args.measurement_type} {args.probes} {args.size} {args.delay}\n"
    # print(f"sending: {init_message}")
    client_socket.send(init_message.encode())
    received_test = client_socket.recv(1024)
    print("From Server:", received_test.decode())


except ConnectionRefusedError:
    print(f"Could not connect to {args.host}:{args.port}")
except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()

# modifiedSentence = clientSocket.recv(1024)
# print("From Server:", modifiedSentence.decode())
