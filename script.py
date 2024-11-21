import requests
import random
import time
import threading
import sys
import argparse
import os

# List of 25 random common user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS336x64; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
]

# Global counters
sent_requests = 0
response_200 = 0
response_429 = 0

# Function to handle request and process response
def send_request(url, headers, request_data, thread_id, count, total_requests):
    global sent_requests, response_200, response_429
    
    try:
        # Replace $$$ in headers and request data with the appropriate value
        headers = {k: v.replace("$$$", str(count).zfill(3)) for k, v in headers.items()}
        request_data = request_data.replace("$$$", str(count).zfill(3))
        
        # Choose a random User-Agent from the list
        headers["User-Agent"] = random.choice(user_agents)

        # Send the request
        response = requests.post(url, headers=headers, data=request_data)
        
        # Track the number of requests sent
        sent_requests += 1

        # Track response status
        if response.status_code == 200:
            response_200 += 1
            print(f"Request {count} from Thread-{thread_id} - Response 200")
        elif response.status_code == 429:
            response_429 += 1
            print(f"Request {count} from Thread-{thread_id} - Response 429 (Rate Limited)")
        else:
            print(f"Request {count} from Thread-{thread_id} - Response {response.status_code}")

    except Exception as e:
        print(f"Request {count} from Thread-{thread_id} failed with error: {str(e)}")

# Function to run the multiple requests in parallel
def run_requests(url, headers, request_data, total_requests, threads_count):
    print(f"Starting {total_requests} requests using {threads_count} threads...")
    threads = []
    count = 1

    start_time = time.time()

    # Create threads for concurrent requests
    for t in range(threads_count):
        thread = threading.Thread(target=request_worker, args=(url, headers, request_data, total_requests, t + 1, count))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print summary
    print(f"\nSent requests = {sent_requests}")
    print(f"Response 200 = {response_200}")
    print(f"Response 429 = {response_429}")
    print(f"Time = {elapsed_time:.2f} seconds.")

def request_worker(url, headers, request_data, total_requests, thread_id, count):
    while count <= total_requests:
        send_request(url, headers, request_data, thread_id, count, total_requests)
        count += 1
        time.sleep(random.uniform(2, 3))  # Random sleep between 2 and 3 seconds

# Argument parsing function
def parse_arguments():
    parser = argparse.ArgumentParser(description="Send HTTP POST requests with rate limiting handling.")
    parser.add_argument('-H', '--header', required=True, help="Path to the header file")  # Changed to -H
    parser.add_argument('-r', '--request', required=True, help="Path to the request file")
    parser.add_argument('-n', '--num_requests', type=int, required=True, help="Number of requests to send")
    parser.add_argument('-t', '--threads', type=int, required=True, help="Number of threads to use for parallel requests")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read header file
    with open(args.header, 'r') as f:
        headers = dict(line.strip().split(": ") for line in f.readlines() if line.strip())

    # Read request file
    with open(args.request, 'r') as f:
        request_data = f.read().strip()

    url = "https://api3.pentest.clicsante.ca/v3/profile/my-patient/new-delegated"  # Replace with your URL
    total_requests = args.num_requests
    threads_count = args.threads

    # Run the requests
    run_requests(url, headers, request_data, total_requests, threads_count)

if __name__ == '__main__':
    main()
