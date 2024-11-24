import argparse
import requests
import time
import random
from collections import defaultdict

# List of 50 common User-Agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 Edge/15.15063",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 Edge/16.16299",
]

def load_text_file(file_path):
    """Read the contents of a text file."""
    with open(file_path, 'r') as file:
        return file.read()

def replace_random_numbers(content):
    """Replace $$$ with random 3-digit numbers."""
    return content.replace('$$$', str(random.randint(100, 999)))

def parse_request_line(request_line):
    """Parse the request line (method, path, and protocol) from text1.txt."""
    parts = request_line.split()
    method = parts[0]
    path = parts[1]
    protocol = parts[2]
    return method, path, protocol

def parse_headers(header_lines):
    """Parse the header lines into a dictionary."""
    headers = {}
    for line in header_lines:
        if ':' in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
    return headers

def load_request_data(header_file, body_file, target_url):
    """Load the request data from header and body files, replacing $$$ with random numbers."""
    # Load header and body content
    header_content = load_text_file(header_file)
    body_content = load_text_file(body_file)
    
    # Replace $$$ with random numbers in the header and body
    header_content = replace_random_numbers(header_content)
    body_content = replace_random_numbers(body_content)
    
    # Split the header content into lines
    header_lines = header_content.strip().splitlines()
    
    # Parse the request line to get method, path, and protocol
    method, path, protocol = parse_request_line(header_lines[0])
    
    # Parse headers into a dictionary
    headers = parse_headers(header_lines[1:])
    
    # Construct the full URL
    url = f"{target_url}{path}"
    
    return method, url, headers, body_content

def send_request(method, url, headers, body):
    """Send the HTTP request based on the chosen method."""
    headers['User-Agent'] = random.choice(USER_AGENTS)
    
    if method == "POST":
        response = requests.post(url, headers=headers, data=body)
    elif method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=body)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    elif method == "PATCH":
        response = requests.patch(url, headers=headers, data=body)
    elif method == "HEAD":
        response = requests.head(url, headers=headers)
    elif method == "OPTIONS":
        response = requests.options(url, headers=headers)
    elif method == "TRACE":
        response = requests.request("TRACE", url, headers=headers)
    elif method == "CONNECT":
        response = requests.request("CONNECT", url, headers=headers)
    else:
        print(f"Unsupported method: {method}")
        return None
    
    return response

def main():
    """Main function to execute the script."""
    parser = argparse.ArgumentParser(description='Send HTTP requests based on input files.')
    parser.add_argument('-H', '--header', required=True, help='Path to the header file (text1.txt)')
    parser.add_argument('-r', '--request-body', required=True, help='Path to the body file (text2.txt)')
    parser.add_argument('-target', '--target-url', required=True, help='The target base URL (e.g., https://example.com)')
    parser.add_argument('-x', '--requests', type=int, required=True, help='Number of requests to send')

    args = parser.parse_args()

    status_codes = defaultdict(int)
    start_time = time.time()

    for _ in range(args.requests):
        method, url, headers, body = load_request_data(args.header, args.request_body, args.target_url)
        
        # Random sleep between 2 and 3 seconds
        time.sleep(random.uniform(2, 3))
        
        # Send request
        response = send_request(method, url, headers, body)
        if response:
            status_codes[response.status_code] += 1
    
    end_time = time.time()
    total_time = end_time - start_time

    # Output the results
    print(f"Total requests sent: {args.requests}")
    for status_code, count in status_codes.items():
        print(f"Status code {status_code}: {count} times")
    print(f"Total time: {total_time:.2f} seconds")

if __name__ == '__main__':
    main()
