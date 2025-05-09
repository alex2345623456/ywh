import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import math

def run_command(request_file, target, x, payload=None, payload2=None, payload3=None):
    command = f"python3 intruder.py -r {request_file} -target {target} -x {x}"
    if payload:
        command += f" -p \"{payload}\""
    if payload2:
        command += f" -p2 \"{payload2}\""
    if payload3:
        command += f" -p3 \"{payload3}\""
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

def repeat_to_length(lst, target_length):
    if not lst:
        return [None] * target_length
    repeat_times = math.ceil(target_length / len(lst))
    extended = (lst * repeat_times)[:target_length]
    return extended

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--request", required=True)
    parser.add_argument("-target", required=True)
    parser.add_argument("-x", required=True, type=int)
    parser.add_argument("-t", required=True, type=int)
    parser.add_argument("-p", nargs='?', default=None)
    parser.add_argument("-p2", nargs='?', default=None)
    parser.add_argument("-p3", nargs='?', default=None)
    args = parser.parse_args()

    payloads = []
    payloads2 = []
    payloads3 = []

    if args.p:
        with open(args.p, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]
    if args.p2:
        with open(args.p2, "r") as f2:
            payloads2 = [line.strip() for line in f2 if line.strip()]
    if args.p3:
        with open(args.p3, "r") as f3:
            payloads3 = [line.strip() for line in f3 if line.strip()]

    max_length = max(len(payloads), len(payloads2), len(payloads3), 1)
    payloads = repeat_to_length(payloads, max_length)
    payloads2 = repeat_to_length(payloads2, max_length)
    payloads3 = repeat_to_length(payloads3, max_length)

    outputs = []
    with ThreadPoolExecutor(max_workers=args.t) as executor:
        futures = []
        for i in range(max_length):
            futures.append(executor.submit(
                run_command,
                args.request,
                args.target,
                args.x,
                payloads[i],
                payloads2[i],
                payloads3[i]
            ))
        for future in futures:
            outputs.append(future.result())

    process_output(outputs)

if __name__ == "__main__":
    main()
