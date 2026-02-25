import matplotlib.pyplot as plt

# --- DATA ---
rtt_sizes = [1, 100, 200, 400, 800, 1000]
rtt_times = [0.00013, 0.00012, 0.00011, 0.00015, 0.00018, 0.00012]

tput_sizes = [1024, 2048, 4096, 8192, 16384, 32768]
tput_vals = [72386.36, 149577.43, 264866.60, 545470.57, 831645.51, 1451994.30]

delay_vals = [0, 0.05, 0.1]
delay_rtt = [0.00012, 0.05033, 0.10026]  # For 1000 bytes
delay_tput = [1451994.30, 5193.00, 2610.32]  # For 32768 bytes

# --- GRAPH 1: RTT vs Size ---
plt.figure(figsize=(8, 5))
plt.plot(rtt_sizes, rtt_times, marker="o", linestyle="-", color="b")
plt.title("Mean RTT vs. Message Size (Delay = 0)")
plt.xlabel("Message Size (Bytes)")
plt.ylabel("Mean RTT (Seconds)")
plt.grid(True)
plt.savefig("graph1_rtt.png")
plt.close()

# --- GRAPH 2: Throughput vs Size ---
plt.figure(figsize=(8, 5))
plt.plot(tput_sizes, tput_vals, marker="s", linestyle="-", color="g")
plt.title("Mean Throughput vs. Message Size (Delay = 0)")
plt.xlabel("Message Size (Bytes)")
plt.ylabel("Throughput (kbps)")
plt.grid(True)
plt.savefig("graph2_tput.png")
plt.close()

# --- GRAPH 3: Effect of Server Delay ---
fig, ax1 = plt.subplots(figsize=(8, 5))

color = "tab:red"
ax1.set_xlabel("Server Delay (Seconds)")
ax1.set_ylabel("Mean RTT for 1000 Bytes (Seconds)", color=color)
ax1.plot(delay_vals, delay_rtt, marker="o", color=color, label="RTT")
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:blue"
ax2.set_ylabel("Throughput for 32768 Bytes (kbps)", color=color)
ax2.plot(delay_vals, delay_tput, marker="s", color=color, label="Throughput")
ax2.tick_params(axis="y", labelcolor=color)

plt.title("Effect of Server Delay on RTT and Throughput")
fig.tight_layout()
plt.grid(True)
plt.savefig("graph3_delay.png")
plt.close()

print("Graphs successfully saved as PNG files!")
