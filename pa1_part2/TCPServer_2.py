import argparse
import time
from socket import *
from threading import ExceptHookArgs

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

# "" means listening on all available network interface
try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((args.host, args.port))
    serverSocket.listen(1)
    print(f"The server is ready to receive on {args.host}:{args.port}")
    num_messages = 0

    while True:
        connectionSocket, addr = serverSocket.accept()
        print(f"Created a connection with {addr}")
        probe_start = 0

        # This is the dedicated socket
        # need to keep listening in a nestloop to this specific one or else will start listening to different one.
        while True:
            # print(f"Entered a loop for {addr}")
            payload = recv_until_newline(connectionSocket)
            if not payload:
                break
            # <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
            protocol_phase = payload[0]

            okay_message = "200 OK: READY"
            bad_message = "404 ERROR: Invalid Connection Setup Message"

            # SET UP PHASE
            if protocol_phase == "s":
                parsed = payload.split(" ")
                measurement_type = parsed[1]
                num_probes = parsed[2]
                message_size = parsed[3]
                server_delay = parsed[4]
                print("-" * 40)
                print(
                    f"protocol phase: {protocol_phase}\nmeasurement type: {measurement_type}\nnumber of probes: {num_probes}\nmessage size: {message_size}\nserver delay: {server_delay}"
                )
                print("-" * 40)
                connectionSocket.send(okay_message.encode())

            # MEASURING PHASE
            elif protocol_phase == "m":
                parsed = payload.split(" ", 2)
                # print(parsed)
                seq_num = int(parsed[1])
                payload = parsed[2]
                probe_start += 1
                if (seq_num > int(num_probes)) or (seq_num < 0):
                    print("Invalid sequence number, exiting...")
                    break
                if seq_num == probe_start:
                    print(f"echoing probe {seq_num}")

                    # wait for specified delay
                    time.sleep(float(server_delay))
                    echo_msg = f"{payload}\n"
                    connectionSocket.send(echo_msg.encode())

            else:
                print(f"Got bad message: {payload}")
                connectionSocket.send(bad_message.encode())

        print(f"exited from {addr}")
        connectionSocket.close()
        # capitalizedSentence = payload.upper()
        # Check if the connection is valid.
except KeyboardInterrupt:
    print("Closing server...")
except OSError as e:
    print("Error: ", e)
except Exception as e:
    print("Some error:", e)
