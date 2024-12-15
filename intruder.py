import argparse
import requests
from collections import Counter
import random
import time

# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
]

def parse_request_file(request_file):
    with open(request_file, 'r') as file:
        data = file.read()

    # Split header and body at the separator '~~~'
    if '~~~' not in data:
        raise ValueError("Invalid format: Missing separator '~~~' in the request file.")

    header_and_body = data.split('~~~')

    # Header section is before the separator
    headers_section = header_and_body[0].strip()

    # Body section is after the separator
    body_section = header_and_body[1].strip() if len(header_and_body) > 1 else None

    # Extract the request line and headers
    request_lines = headers_section.splitlines()
    request_line = request_lines[0]  # The first line is the request line
    headers = {line.split(": ")[0]: line.split(": ")[1] for line in request_lines[1:]}

    # Split the request line into method, path, and protocol
    method, path, protocol = request_line.split()

    return method, path, protocol, headers, body_section

def generate_random_number():
    return random.randint(100, 999)  # Generate a random 3-digit number

def replace_placeholder(text, placeholder, replacement):
    while placeholder in text:
        text = text.replace(placeholder, replacement, 1)  # Replace one occurrence at a time
    return text

def random_user_agent():
    return random.choice(USER_AGENTS)  # Select a random user agent from the list

def send_request(target_url, method, path, headers, body=None, payload_value=None):
    url = target_url + path

    # Randomly select a User-Agent for the request
    headers["User-Agent"] = random_user_agent()

    # Replace $$$ and PAYLOAD in header and body with random numbers and payload value
    headers = {key: replace_placeholder(replace_placeholder(value, '$$$', str(generate_random_number())), 'PAYLOAD', payload_value) for key, value in headers.items()}
    if body:
        body = replace_placeholder(replace_placeholder(body, '$$$', str(generate_random_number())), 'PAYLOAD', payload_value)

    # Send the request based on the selected method
    method = method.upper()
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=body)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=body)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    elif method == 'PATCH':
        response = requests.patch(url, headers=headers, data=body)
    elif method == 'HEAD':
        response = requests.head(url, headers=headers)
    elif method == 'OPTIONS':
        response = requests.options(url, headers=headers)
    elif method == 'TRACE':
        response = requests.request("TRACE", url, headers=headers)
    elif method == 'CONNECT':
        response = requests.request("CONNECT", url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response

def main():
    parser = argparse.ArgumentParser(description='HTTP request sender')
    parser.add_argument('-r', '--request', required=True, help='Path to the request file')
    parser.add_argument('-target', '--target', required=True, help='Target URL (e.g., https://example.com)')
    parser.add_argument('-x', '--requests_count', type=int, default=1, help='Number of requests to send')
    parser.add_argument('-p', '--payload', help='Payload value to replace PAYLOAD placeholder')  # Payload is now optional
    parser.add_argument('-vr', '--view_response', action='store_true', help='Show response body in output')  # New argument
    args = parser.parse_args()

    # Parse the request file
    try:
        method, path, protocol, headers, body = parse_request_file(args.request)
    except ValueError as e:
        print(f"Error parsing request file: {e}")
        return

    # Statistics for tracking status code counts
    status_codes = []

    print(f"Sending {args.requests_count} requests to {args.target}{path}...")

    # Send the specified number of requests
    for _ in range(args.requests_count):
        # If no payload is provided, just pass None to avoid replacing PAYLOAD
        payload_value = args.payload if args.payload else None
        response = send_request(args.target, method, path, headers, body, payload_value=payload_value)

        # Random sleep between 2 and 3 seconds
        time.sleep(random.uniform(2, 3))

        # Track status code
        status_codes.append(response.status_code)

        # Show response body if --view_response is set
        if args.view_response:
            print(f"Response Body:\n{response.text}\n")

    # Count frequency of each status code
    status_code_counts = Counter(status_codes)

    # Print the results
    print(f"Total sent requests: {args.requests_count}")
    for status_code, count in status_code_counts.items():
        print(f"Status code {status_code}: {count} times")

if __name__ == '__main__':
    main()
