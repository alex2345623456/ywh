import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

def run_command(request_file, target, x, payload=None, payload2=None):
    if payload and payload2:
        command = f"python3 intruder.py -r {request_file} -target {target} -x {x} -p \"{payload}\" -p2 \"{payload2}\""
    elif payload:
        command = f"python3 intruder.py -r {request_file} -target {target} -x {x} -p \"{payload}\""
    else:
        command = f"python3 intruder.py -r {request_file} -target {target} -x {x}"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def process_output(outputs):
    status_codes = []
    for output in outputs:
        for line in output.splitlines():
            if "Status code" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    status_code = parts[1].strip()
                    status_codes.append(status_code)
    counter = Counter(status_codes)
    total = sum(counter.values())
    print(f"Number of successfully sent requests: {total} times")
    for code, count in counter.items():
        time_label = "time" if count == 1 else "times"
        print(f"Status code {code}: {count} {time_label}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--request", required=True)
    parser.add_argument("-target", required=True)
    parser.add_argument("-x", required=True, type=int)
    parser.add_argument("-t", required=True, type=int)
    parser.add_argument("-p", nargs='?', default=None)
    parser.add_argument("-p2", nargs='?', default=None)
    args = parser.parse_args()

    payloads = []
    payloads2 = []

    if args.p:
        with open(args.p, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]
    if args.p2:
        with open(args.p2, "r") as f2:
            payloads2 = [line.strip() for line in f2 if line.strip()]
    
    if args.p and args.p2:
        if len(payloads) != len(payloads2):
            print("Error: The number of lines in payload and payload2 files must be the same.")
            return
        payload_pairs = list(zip(payloads, payloads2))
    elif args.p:
        payload_pairs = [(payload, None) for payload in payloads]
    else:
        payload_pairs = [(None, None)] * args.t

    outputs = []
    with ThreadPoolExecutor(max_workers=args.t) as executor:
        futures = []
        for i in range(args.t):
            payload, payload2 = payload_pairs[i % len(payload_pairs)]
            futures.append(executor.submit(run_command, args.request, args.target, args.x, payload, payload2))
        for future in futures:
            outputs.append(future.result())

    process_output(outputs)

if __name__ == "__main__":
    main()
