import argparse
import requests
from collections import Counter
import random
import time

# List of common user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 Edge/16.16299"
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

def replace_placeholder_with_random_number(text, placeholder='$$$'):
    while placeholder in text:
        random_number = generate_random_number()
        text = text.replace(placeholder, str(random_number), 1)  # Replace one occurrence at a time
    return text

def random_user_agent():
    return random.choice(USER_AGENTS)  # Select a random user agent from the list

def send_request(target_url, method, path, headers, body=None):
    url = target_url + path
    
    # Randomly select a User-Agent for the request
    headers["User-Agent"] = random_user_agent()

    # Replace $$$ in header and body with random numbers
    headers = {key: replace_placeholder_with_random_number(value) for key, value in headers.items()}
    if body:
        body = replace_placeholder_with_random_number(body)

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
        response = send_request(args.target, method, path, headers, body)

        # Random sleep between 2 and 3 seconds
        time.sleep(random.uniform(2, 3))

        status_codes.append(response.status_code)

    # Count frequency of each status code
    status_code_counts = Counter(status_codes)

    # Print the results
    print(f"Total sent requests: {args.requests_count}")
    for status_code, count in status_code_counts.items():
        print(f"Status code {status_code}: {count} times")

if __name__ == '__main__':
    main()
