import sys
import random
import os.path
from subprocess import Popen, PIPE, check_output
import subprocess
import csv
import time
import datetime


class SpeedMonitor:
    def __init__(self, speedtest, out_dir):
        self.speedtest = speedtest
        self.out_dir = out_dir
        self.out_f = None
        self.out_p = ""

    def server_file(self):
        subprocess.run(["mkdir", "-p", self.out_dir])
        return os.path.join(self.out_dir, "servers.csv")

    def get_servers(self):
        srv_f = self.server_file()
        if not os.path.isfile(srv_f):
            with open(srv_f, "w") as f:
                p = Popen([self.speedtest, "-L", "-f", "csv"], stdout=f)
                p.wait()
        ss = []
        with open(srv_f, newline='') as f:
            reader = csv.reader(f)
            for l in reader:
                ss.append(l[0])
        ss.pop(0)
        return ss

    def print_header(self):
        print("Writing header")
        subprocess.run([
            "echo",
            '"server name","server id","latency","jitter","packet loss","download","upload","download bytes","upload bytes","share url","start time","end time"'
        ],
                       stdout=self.out_f)

    def single(self, server):
        print(f"ID: {server}...", end='', flush=True)
        start = time.time_ns()
        args = [self.speedtest, "-f", "csv", "-s", server]
        p = Popen(args, stdout=PIPE, stderr=PIPE)
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
            out = f"{out.decode('utf-8').strip()},\"{start}\",\"{end}\""
            subprocess.run(
                ["echo", out],
                stdout=self.out_f)  # echoing to get immediate results
            print(f"DONE, Time: {(end-start)/1000000000:.2f}s")
            return

    def all(self, server_list):
        l = len(server_list)
        for i, server in enumerate(server_list):
            print(f"{i+1}/{l} ", end=' ')
            self.single(server)

    def update_out_file(self):
        p = os.path.join(self.out_dir, f"{datetime.datetime.now().date()}.csv")
        if self.out_p != p:
            if self.out_f:
                self.out_f.close()
                self.out_f = None
        self.out_p = p
        if not self.out_f:
            header = False
            if not os.path.isfile(self.out_p):
                print("Out file does not exist yet.")
                header = True
            self.out_f = open(self.out_p, "a")
            if header:
                self.print_header()
        return self.out_f

    @staticmethod
    def pretty_time():
        return datetime.datetime.now().time().isoformat(timespec="seconds")

    def run(self):
        server_list = self.get_servers()
        while True:
            print(f"Started at {SpeedMonitor.pretty_time()}")
            self.update_out_file()
            self.all(server_list)
            print(f"Finished at {SpeedMonitor.pretty_time()}")


if __name__ == "__main__":
    SpeedMonitor(sys.argv[1], sys.argv[2]).run()