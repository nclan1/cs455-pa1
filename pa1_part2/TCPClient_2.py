import argparse
from socket import *

# set up parser
parser = argparse.ArgumentParser(
    description="Python Client acting as a server to perform RTT and Throughput Measurements"
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
    help="The port number to connect to. Default: 9090",
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
    help="Number of measurement probes that the server should expect to receive",
)

# parser.add_argument("-ms", "--measurement-type")

# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((serverName, serverPort))


# after setting up the connection, send a message with the following format
# <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
#
# measurement_type = input("Input 'rtt' or 'tput': ")
# num_probes = input("Input number of probes: ")
# msg_size = int(input("Input bytes in payload: "))
# server_delay = int(input("Input amount of time server shoudl wait: (default 0)"), 0)

# clientSocket.send(TODO HERE)
# modifiedSentence = clientSocket.recv(1024)
# print("From Server:", modifiedSentence.decode())
# clientSocket.close()
#
args = parser.parse_args()
