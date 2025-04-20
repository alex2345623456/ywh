import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
import itertools
from collections import Counter

def run_command(request_file, target, x, payload=None):
    if payload:
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
    args = parser.parse_args()

    payloads = []
    if args.p:
        with open(args.p, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]
    payload_cycle = itertools.cycle(payloads) if payloads else None

    outputs = []
    with ThreadPoolExecutor(max_workers=args.t) as executor:
        if payload_cycle:
            futures = [executor.submit(run_command, args.request, args.target, args.x, next(payload_cycle)) for _ in range(args.t)]
        else:
            futures = [executor.submit(run_command, args.request, args.target, args.x) for _ in range(args.t)]
        for future in futures:
            outputs.append(future.result())

    process_output(outputs)

if __name__ == "__main__":
    main()
