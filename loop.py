import subprocess
import time
import argparse
import random
import requests
import re
import os
from collections import defaultdict

total_stats = defaultdict(int)

def run_command(r, target, x, t, p=None, p2=None, p3=None):
    cmd = ['python3', 'autointruder.py', '-r', r]
    if p:
        cmd += ['-p', p]
    if p2:
        cmd += ['-p2', p2]
    if p3:
        cmd += ['-p3', p3]
    cmd += ['-x', str(x), '-t', str(t), '-target', target]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = result.stdout.strip()
    print(output)
    parse_stats(output)

    print('sudo anonsurf change')
    subprocess.run(['sudo', 'anonsurf', 'change'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ip = requests.get('https://api.ipify.org').text
    print(f"\033[92mIP address: {ip}\033[0m")

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
    print()
    print(f"Total number of successfully sent requests: {total_stats['total']} times")
    for code in sorted(k for k in total_stats if k != 'total'):
        label = "time" if total_stats[code] == 1 else "times"
        print(f"Status code {code}: {total_stats[code]} {label}")
    print()

def run_email_script(t):
    email_script_path = 'allemail.py'
    if os.path.exists(email_script_path):
        cmd_email = ['python3', email_script_path, '-t', str(t)]
        result_email = subprocess.run(cmd_email, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print(result_email.stdout.strip())

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('-r', required=True)
    p.add_argument('-x', type=int, required=True)
    p.add_argument('-t', type=int, required=True)
    p.add_argument('-target', required=True)
    p.add_argument('-delay', default="1-1")
    p.add_argument('-p')
    p.add_argument('-p2')
    p.add_argument('-p3')
    p.add_argument('-loop', type=int, default=None)
    a = p.parse_args()

    delay_min, delay_max = parse_delay_range(a.delay)
    loop_count = a.loop if a.loop else float('inf')

    try:
        for _ in range(loop_count):
            run_email_script(a.t)
            run_command(a.r, a.target, a.x, a.t, a.p, a.p2, a.p3)
            time.sleep(random.uniform(delay_min, delay_max))
    finally:
        print_final_stats()
