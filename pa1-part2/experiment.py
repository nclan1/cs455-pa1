import csv
import re
import subprocess
import time
from pathlib import Path

"""
Instead of manually running the client for every message size and delay combination,
the script repeatedly executes the TCP client with different parameters, 
captures the printed average RTT or throughput results, and stores them in a CSV file.
"""

RTT_SIZES = [1, 100, 200, 400, 800, 1000]
TPUT_SIZES = [1024, 2048, 4096, 8192, 16384, 32768]

DELAYS_TO_RUN_MS = [0, 50, 100]

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 58001
DEFAULT_PROBES = 10

AVG_RTT_RE = re.compile(r"Average RTT:\s*([0-9.]+)\s*seconds", re.IGNORECASE)
AVG_TPUT_RE = re.compile(r"Average Throughput:\s*([0-9.]+)\s*Mbps", re.IGNORECASE)


def run_client_once(host, port, mtype, probes, msg_size, delay_ms):
    """
    Runs TCPClient.py once by feeding stdin.
    Returns dict with parsed averages.
    """
    stdin_data = "\n".join([
        str(host),
        str(port),
        str(mtype),
        str(probes),
        str(msg_size),
        str(delay_ms),
        ""
    ])

    p = subprocess.run(
        ["python3", "TCPClient.py"],
        input=stdin_data,
        text=True,
        capture_output=True
    )

    out = p.stdout + "\n" + p.stderr

    if p.returncode != 0:
        raise RuntimeError(f"TCPClient.py failed (code {p.returncode}). Output:\n{out}")

    # Parse averages
    avg_rtt_s = None
    avg_tput_mbps = None

    m1 = AVG_RTT_RE.search(out)
    if m1:
        avg_rtt_s = float(m1.group(1))

    m2 = AVG_TPUT_RE.search(out)
    if m2:
        avg_tput_mbps = float(m2.group(1))

    if mtype == "rtt" and avg_rtt_s is None:
        raise RuntimeError(f"Could not parse Average RTT from output:\n{out}")
    if mtype == "tput" and avg_tput_mbps is None:
        raise RuntimeError(f"Could not parse Average Throughput from output:\n{out}")

    return {
        "avg_rtt_s": avg_rtt_s,
        "avg_tput_mbps": avg_tput_mbps,
        "raw_output": out,
    }


def start_server_local(port):
    """
    Starts TCPserver.py locally and feeds the port to stdin.
    Requires that TCPserver.py prompts for port (your version does).
    """
    proc = subprocess.Popen(
        ["python3", "TCPserver.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    assert proc.stdin is not None
    proc.stdin.write(f"{port}\n")
    proc.stdin.flush()

    # Give it a moment to bind/listen
    time.sleep(0.5)
    return proc


def stop_process(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()


def main():
    host = input(f"Server host [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST
    port_s = input(f"Server port [{DEFAULT_PORT}]: ").strip()
    port = int(port_s) if port_s else DEFAULT_PORT

    probes_s = input(f"Probes per size (>=10) [{DEFAULT_PROBES}]: ").strip()
    probes = int(probes_s) if probes_s else DEFAULT_PROBES

    # Only auto-start server if running locally
    start_server = (host in ("127.0.0.1", "localhost"))
    server_proc = None

    if start_server:
        print("Starting local TCPserver.py ...")
        server_proc = start_server_local(port)
        print("Server started.")
    else:
        print("Not starting server (non-local host). Make sure TCPserver.py is already running.")

    rows = []
    try:
        for delay_ms in DELAYS_TO_RUN_MS:
            # RTT sweep
            for sz in RTT_SIZES:
                res = run_client_once(host, port, "rtt", probes, sz, delay_ms)
                avg_rtt_ms = res["avg_rtt_s"] * 1000.0
                rows.append([delay_ms, "rtt", sz, probes, avg_rtt_ms, "", ""])
                print(f"[delay={delay_ms}ms] RTT size={sz}B avg={avg_rtt_ms:.3f} ms")

            # Throughput sweep
            for sz in TPUT_SIZES:
                res = run_client_once(host, port, "tput", probes, sz, delay_ms)
                avg_tput_mbps = res["avg_tput_mbps"]
                rows.append([delay_ms, "tput", sz, probes, "", avg_tput_mbps, avg_tput_mbps * 1000.0])
                print(f"[delay={delay_ms}ms] TPUT size={sz}B avg={avg_tput_mbps:.3f} Mbps")

        out_csv = Path(f"results_via_client_probes{probes}.csv")
        with out_csv.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "server_delay_ms",
                "measurement_type",
                "msg_size_bytes",
                "num_probes",
                "avg_rtt_ms",
                "avg_tput_mbps",
                "avg_tput_kbps",
            ])
            w.writerows(rows)

        print(f"\nWrote CSV: {out_csv}")

    finally:
        if server_proc is not None:
            print("Stopping server...")
            stop_process(server_proc)
            print("Server stopped.")


if __name__ == "__main__":
    main()