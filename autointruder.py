import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import os
import itertools

def run_command(request_file, target, x, payload=None):
    """
    This function constructs and runs the command using subprocess, and returns the command's output.
    """
    # Build the command to be executed
    if payload:
        command = f"python3 intruder.py -r {request_file} -target {target} -x {x} -p \"{payload}\""
    else:
        command = f"python3 intruder.py -r {request_file} -target {target} -x {x}"
    
    print(f"Running command: {command}")

    # Run the command via subprocess and capture the output
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout  # Return the output of the command
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the command: {e}")
        return ""


def process_output(output):
    """
    This function processes the output of the command to extract the status codes and their frequencies.
    """
    status_codes = []
    lines = output.splitlines()
    for line in lines:
        if "Status code" in line:
            # Extract status code and the number of occurrences from the output line
            parts = line.split(":")
            status_code = parts[0].strip().split()[-1]
            count = int(parts[1].strip().split()[0])
            status_codes.extend([status_code] * count)  # Add the status code the specified number of times

    return status_codes


def main():
    """
    Main function to handle argument parsing, executing the commands, and aggregating the results.
    """
    # Using argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Auto Intruder Script")
    parser.add_argument("-r", "--request", required=True, help="Path to the request.txt file")
    parser.add_argument("-target", required=True, help="Target URL for the intruder command")
    parser.add_argument("-x", required=True, type=int, help="Number of times to execute the intruder command")
    parser.add_argument("-t", required=True, type=int, help="Number of commands to run concurrently")
    parser.add_argument("-p", help="Path to the payload file", nargs='?', default=None)

    # Parse arguments
    args = parser.parse_args()

    # Read payloads from file if -p is provided
    if args.p:
        if not os.path.exists(args.p):
            print(f"Error: Payload file '{args.p}' does not exist.")
            exit(1)

        with open(args.p, "r") as payload_file:
            payloads = [line.strip() for line in payload_file if line.strip()]

        if len(payloads) < args.t:
            print("Warning: Number of payloads is less than number of threads. Payloads will be cycled.")
            
        # Create a cycle of payloads to ensure each thread gets a payload
        payload_cycle = itertools.cycle(payloads)
    else:
        payload_cycle = None  # No payloads to cycle through

    # Using ThreadPoolExecutor to run commands concurrently
    with ThreadPoolExecutor(max_workers=args.t) as executor:
        if payload_cycle:
            futures = [executor.submit(run_command, args.request, args.target, args.x, next(payload_cycle)) for _ in range(args.t)]
        else:
            futures = [executor.submit(run_command, args.request, args.target, args.x) for _ in range(args.t)]

        all_status_codes = []

        # Gather all the status codes from the output of each command
        for future in futures:
            output = future.result()  # Get the result (output) from each command
            status_codes = process_output(output)  # Process the output to get status codes
            all_status_codes.extend(status_codes)  # Add the status codes to the list

        # Count the frequency of each status code using Counter
        status_code_count = Counter(all_status_codes)

        # Print the final results
        print("Result")
        total_requests = len(all_status_codes)
        print(f"Total sent requests: {total_requests}")

        # Print each status code and its count
        for status_code, count in status_code_count.items():
            print(f"Status code {status_code}: {count} times")


if __name__ == "__main__":
    main()
