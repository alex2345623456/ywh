import subprocess
import time
import argparse
import sys

def run_command(request_file, target_url, x_value, t_value):
    # Record the start time before executing the command
    start_time = time.time()

    # Command to run with the provided arguments
    command = [
        'python3', 'autointruder.py',
        '-r', request_file,
        '-x', str(x_value),
        '-t', str(t_value),
        '-target', target_url
    ]
    
    # Run the autointruder.py command and capture its output
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print the output of autointruder.py
    print("Output from autointruder.py:")
    print(result.stdout)
    
    # Print any error output if available
    if result.stderr:
        print("Error:")
        print(result.stderr)

    # Run the anonsurf change command to change the IP
    print("Running the anonsurf change command...")
    result = subprocess.run(['sudo', 'anonsurf', 'change'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print the output from anonsurf change
    print("Output from anonsurf change:")
    print(result.stdout)
    
    # Print any error output from anonsurf if available
    if result.stderr:
        print("Error:")
        print(result.stderr)

    # Record the end time after the command execution
    end_time = time.time()

    # Calculate the duration of command execution
    duration = end_time - start_time
    print(f"Command finished. Duration: {duration:.2f} seconds\n")

def main():
    # Setup the argument parser
    parser = argparse.ArgumentParser(description="A script to repeatedly run a set of commands.")
    parser.add_argument('-r', '--request', required=True, help="The request file (e.g., request.txt)")
    parser.add_argument('-x', '--x_value', type=int, required=True, help="The value for the -x option")
    parser.add_argument('-t', '--t_value', type=int, required=True, help="The value for the -t option")
    parser.add_argument('-target', '--target_url', required=True, help="The target URL")
    parser.add_argument('-s', '--sleep', type=int, default=1, help="Delay in seconds between commands.")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    print(f"Script started with a {args.sleep} second delay. Press Ctrl+C to stop.")
    try:
        # Run the command in an infinite loop
        while True:
            run_command(args.request, args.target_url, args.x_value, args.t_value)
            # Wait for the specified time before running the command again
            time.sleep(args.sleep)
    except KeyboardInterrupt:
        # Handle the interruption gracefully when the user presses Ctrl+C
        print("\nScript was stopped by the user.")
        sys.exit(0)

# Ensure the script runs when executed directly
if __name__ == "__main__":
    main()
