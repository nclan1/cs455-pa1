import argparse
import time
from socket import *

# set up parser
parser = argparse.ArgumentParser(
    description="Python script acting as the client to perform RTT and Throughput measurement."
)

parser.add_argument(
    "--host",
    help="The hostname / IP address to connect to. (Default: localhost)",
    default="localhost",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    help="The port number to connect to. (Default: 9090)",
    default=9090,
)

parser.add_argument(
    "-ms",
    "--measurement-type",
    help="Specify whether to compute the RTT (Round Trip Time) or throughput. (Required)",
    choices=["rtt", "tput"],
    required=True,
)

parser.add_argument(
    "-n",
    "--probes",
    type=int,
    help="Number of measurement probes that the server should expect to receive. (Required)",
    required=True,
)

parser.add_argument(
    "-s",
    "--size",
    type=int,
    help="Size of the probe's payload in bytes. (Required)",
    required=True,
)

parser.add_argument(
    "-d",
    "--delay",
    type=int,
    help="Amount of time that the server should wait before echoing the message back. (Default: 0)",
    default=0,
)


def recv_until_newline(sock):
    """
    helper fxn, read from scoket until newline, return none if connection close
    """
    buffer = ""
    while True:
        try:
            chunk = sock.recv(4096).decode("utf-8")
            if not chunk:
                return None

            buffer += chunk

            if "\n" in buffer:
                message, rest = buffer.split("\n", 1)
                return message
        except Exception as e:
            print(f"Error reading: {e}")
            return None


args = parser.parse_args()
# print(args)


def get_fixed_lorem(target_bytes):
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100
    byte_data = lorem.encode("utf-8")
    # Return exactly the amount needed, padded with spaces if too short
    return byte_data[:target_bytes].ljust(target_bytes, b" ")


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
    received_msg = client_socket.recv(1024).decode()

    if received_msg == "200 OK: READY":
        # ----------------SECOND STEP----------------
        print("Got OK, prepping measurement phase...")
        # <PROTOCOL PHASE><WS><PROBE SEQUENCE NUMBER><WS><PAYLOAD>\n
        seq_num = 1
        payload = get_fixed_lorem(args.size).decode("utf-8")
        while seq_num <= args.probes:
            probe_message = f"m {seq_num} {payload}\n"
            # starting timer
            start_time = time.time()

            # send probe
            client_socket.send(probe_message.encode())
            print(f"sent message number {seq_num}, waiting for echo...")

            # wait for echo
            echoed_msg = recv_until_newline(client_socket)

            # stop time
            end_time = time.time()

            if echoed_msg:
                rtt = end_time - start_time
                print(f"Received echo for sequence {seq_num}. RTT: {rtt:.5f} seconds")
            else:
                print("failed to receive echo.")
            seq_num += 1


except ConnectionRefusedError:
    print(f"Could not connect to {args.host}:{args.port}")
except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()

# modifiedSentence = clientSocket.recv(1024)
# print("From Server:", modifiedSentence.decode())
