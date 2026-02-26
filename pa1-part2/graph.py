import matplotlib.pyplot as plt

# The data here is hardcoded, but are based from the csv file generated from graph.py

# RTT (ms) vs payload size (bytes)
rtt_sizes = [1, 100, 200, 400, 800, 1000]

rtt_0ms = [0.043, 0.043, 0.083, 0.094, 0.127, 0.046]
rtt_50ms = [50.257, 50.281, 50.346, 50.251, 50.310, 50.268]
rtt_100ms = [100.304, 100.323, 100.326, 100.339, 100.374, 100.376]

# Throughput (Mbps) vs payload size (bytes)
tput_sizes = [1024, 2048, 4096, 8192, 16384, 32768]

tput_0ms = [402.496, 882.907, 1373.052, 1966.6, 2508.907, 4091.127]
tput_50ms = [0.326, 0.651, 1.304, 2.597, 5.205, 10.392]
tput_100ms = [0.163, 0.327, 0.653, 1.306, 2.612, 5.222]


def plot_rtt_delay0():
    plt.figure()
    plt.plot(rtt_sizes, rtt_0ms, marker="o")
    plt.xlabel("Message size (bytes)")
    plt.ylabel("Mean RTT (ms)")
    plt.title("TCP RTT vs Message Size (SERVER_DELAY=0 ms)")
    plt.grid(True)
    plt.savefig("rtt_delay0.png", dpi=200, bbox_inches="tight")
    plt.close()


def plot_tput_delay0():
    plt.figure()
    plt.plot(tput_sizes, tput_0ms, marker="o")
    plt.xlabel("Message size (bytes)")
    plt.ylabel("Mean Throughput (Mbps)")
    plt.title("TCP Throughput vs Message Size (SERVER_DELAY=0 ms)")
    plt.grid(True)
    plt.savefig("tput_delay0.png", dpi=200, bbox_inches="tight")
    plt.close()


def plot_rtt_compare_delays():
    plt.figure()
    plt.plot(rtt_sizes, rtt_0ms, marker="o", label="0 ms")
    plt.plot(rtt_sizes, rtt_50ms, marker="o", label="50 ms")
    plt.plot(rtt_sizes, rtt_100ms, marker="o", label="100 ms")
    plt.xlabel("Message size (bytes)")
    plt.ylabel("Mean RTT (ms)")
    plt.title("RTT vs Message Size (Effect of SERVER_DELAY)")
    plt.grid(True)
    plt.legend()
    plt.savefig("rtt_compare_delays.png", dpi=200, bbox_inches="tight")
    plt.close()

delays_ms = [0, 50, 100]

def plot_delay_sweep_for_size():
    """
    X-axis: server delay (ms)
    Y1: RTT (ms)
    Y2: Throughput (Mbps)
    Uses 32K throughput and 1000B RTT (largest RTT size measured).
    """

    rtt_1000_by_delay = [rtt_0ms[-1], rtt_50ms[-1], rtt_100ms[-1]]
    tput_32k_by_delay = [tput_0ms[-1], tput_50ms[-1], tput_100ms[-1]]

    fig, ax1 = plt.subplots(figsize=(7, 5))

    rtt_line = ax1.plot(
        delays_ms,
        rtt_1000_by_delay,
        color="tab:blue",
        marker="o",
        linewidth=2,
        label="RTT (ms)"
    )

    ax1.set_xlabel("Server Delay (ms)")
    ax1.set_ylabel("Mean RTT (ms)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlim(min(delays_ms), max(delays_ms))
    ax1.set_ylim(0, max(rtt_1000_by_delay) * 1.1)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # ---- Throughput axis ----
    ax2 = ax1.twinx()

    tput_line = ax2.plot(
        delays_ms,
        tput_32k_by_delay,
        color="tab:red",
        marker="s",
        linewidth=2,
        linestyle="--",
        label="Throughput (Mbps)"
    )

    ax2.set_ylabel("Mean Throughput (Mbps)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    ax2.set_ylim(0, max(tput_32k_by_delay) * 1.1)

    # ---- Combined Legend ----
    lines = rtt_line + tput_line
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc="best")

    plt.title("Effect of Server Delay on RTT and Throughput (32K payload)")
    plt.tight_layout()
    plt.savefig("delay_sweep_32K.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    # Required plots
    plot_rtt_delay0()
    plot_tput_delay0()

    plot_delay_sweep_for_size()

    print("Wrote: rtt_delay0.png, tput_delay0.png, rtt_compare_delays.png, tput_compare_delays.png")