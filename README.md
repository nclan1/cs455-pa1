## 1. Start the Server

Open a terminal and run:

```
python TCPserver.py
```

Enter the port number when prompted (e.g., 58001).

The server will begin listening for incoming TCP connections.

## 2. Run the Client

Open a second terminal and run:

```
python TCPClient.py
```

Enter the following when prompted:

Host name or IP (e.g., csa1.bu.edu or localhost)

Port number (same as server)

Measurement type (rtt or tput)

Number of probes (e.g., 10)

Message size (in bytes)

Server delay (in milliseconds)

The client will send the probes and display the average RTT or throughput.

## 3. Run Automated Experiments

To automatically run all required experiments and generate a CSV file:
```
python experiment.py
```

This script executes the client for all required payload sizes and server delay values, collects the results, and writes them to a CSV file.

## 4. Generate Graphs

After experiments complete, generate plots by running:
```
python graph.py
```

This will produce the required RTT and throughput graphs, as well as additional delay comparison plots.