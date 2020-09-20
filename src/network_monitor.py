import sys
import random
import os.path
from subprocess import Popen, PIPE, check_output
import subprocess
import csv
import time
import datetime

SPEEDTEST_PATH = sys.argv[1]
OUTPUT_DIR = sys.argv[2]


def server_file():
    subprocess.run(["mkdir", "-p", OUTPUT_DIR])
    return os.path.join(OUTPUT_DIR, "servers.csv")


def get_servers():
    srv_f = server_file()
    if not os.path.isfile(srv_f):
        with open(srv_f, "w") as f:
            p = Popen([SPEEDTEST_PATH, "-L", "-f", "csv"], stdout=f)
            p.wait()
    ss = []
    with open(srv_f, newline='') as f:
        reader = csv.reader(f)
        for l in reader:
            ss.append(l[0])
    ss.pop(0)
    return ss


def speedtest(f, server):
    print(f"ID: {server}...", end='', flush=True)
    start = time.time_ns()
    p = Popen([SPEEDTEST_PATH, "-f", "csv", "-s", server],
              stdout=PIPE,
              stderr=PIPE)
    try:
        out, err = p.communicate(timeout=60)
    except TimeoutError:
        print("TIMEOUT")
        return
    end = time.time_ns()
    if err:
        print("ERROR, Message:")
        print(err.decode("utf-8"))
        return
    else:
        out = f"{out.strip()}, {start}, {end}"
        subprocess.run(["echo", out],
                       stdout=f)  # echoing to get immediate results
        print(f"DONE, Time: {(end-start)/1000000000:.2f}s")
        return


def speedtest_list(f, server_list):
    l = len(server_list)
    for i, server in enumerate(server_list):
        print(f"{i+1}/{l} ", end=' ')
        speedtest(f, server)


def out_file():
    return os.path.join(OUTPUT_DIR, f"{datetime.datetime.now().date()}.csv")


def pretty_time():
    return datetime.datetime.now().time().isoformat(timespec="seconds")


def run():
    server_list = get_servers()
    while True:
        print(f"Started at {pretty_time()}")
        with open(out_file(), "a") as f:
            speedtest_list(f, server_list)
        print(f"Finished at {pretty_time()}")


if __name__ == "__main__":
    run()