import subprocess
import time
import argparse
import random
import requests
import re
from collections import defaultdict

total_stats = defaultdict(int)

def run_command(r, target, x, t):
    cmd1 = ['python3', 'autointruder.py', '-r', r, '-x', str(x), '-t', str(t), '-target', target]
    print(' '.join(cmd1))
    result1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = result1.stdout.strip()
    print(output)
    parse_stats(output)

    print('sudo anonsurf change')
    subprocess.run(['sudo', 'anonsurf', 'change'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("IP address:", requests.get('https://api.ipify.org').text)

def parse_stats(output):
    for line in output.splitlines():
        m_total = re.match(r'Number of successfully sent requests: (\d+)', line)
        m_code = re.match(r'Status code (\d+): (\d+) time', line)
        if m_total:
            total_stats['total'] += int(m_total.group(1))
        elif m_code:
            code = m_code.group(1)
            count = int(m_code.group(2))
            total_stats[code] += count

def parse_delay_range(delay):
    try:
        parts = delay.split('-')
        return (float(parts[0]), float(parts[1])) if len(parts) == 2 else (float(parts[0]), float(parts[0]))
    except:
        return 1.0, 1.0

def print_final_stats():
    print(f"Total number of successfully sent requests: {total_stats['total']} times")
    for code in sorted(k for k in total_stats if k != 'total'):
        label = "time" if total_stats[code] == 1 else "times"
        print(f"Status code {code}: {total_stats[code]} {label}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('-r', required=True)
    p.add_argument('-x', type=int, required=True)
    p.add_argument('-t', type=int, required=True)
    p.add_argument('-target', required=True)
    p.add_argument('-delay', default="1-1")
    a = p.parse_args()

    delay_min, delay_max = parse_delay_range(a.delay)

    try:
        while True:
            run_command(a.r, a.target, a.x, a.t)
            time.sleep(random.uniform(delay_min, delay_max))
    except KeyboardInterrupt:
        print_final_stats()
