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

    # Check if '~~~' is used as separator
    if '~~~' in data:
        header_section, body_section = data.split('~~~', 1)
    else:
        # Fallback: Use double newline (baris kosong) as separator
        parts = data.split('\n\n', 1)
        header_section = parts[0]
        body_section = parts[1] if len(parts) > 1 else None

    header_section = header_section.strip()
    body_section = body_section.strip() if body_section else None

    # Parse request line and headers
    lines = header_section.splitlines()
    request_line = lines[0]
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    method, path, protocol = request_line.split()
    return method, path, protocol, headers, body_section

def generate_random_number():
    return random.randint(100, 999)

def replace_placeholder(text, placeholder, replacement):
    while placeholder in text:
        text = text.replace(placeholder, replacement, 1)
    return text

def random_user_agent():
    return random.choice(USER_AGENTS)

def send_request(target_url, method, path, headers, body=None, payload_value=None):
    url = target_url + path
    headers["User-Agent"] = random_user_agent()

    headers = {
        key: replace_placeholder(replace_placeholder(value, '$$$', str(generate_random_number())), 'PAYLOAD', payload_value)
        for key, value in headers.items()
    }
    if body:
        body = replace_placeholder(replace_placeholder(body, '$$$', str(generate_random_number())), 'PAYLOAD', payload_value)

    method = method.upper()
    try:
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
    except requests.RequestException:
        return None

    return response

def main():
    parser = argparse.ArgumentParser(description='HTTP request sender')
    parser.add_argument('-r', '--request', required=True, help='Path to the request file')
    parser.add_argument('-target', '--target', required=True, help='Target URL (e.g., https://example.com)')
    parser.add_argument('-x', '--requests_count', type=int, default=1, help='Number of requests to send')
    parser.add_argument('-p', '--payload', help='Payload value to replace PAYLOAD placeholder')
    args = parser.parse_args()

    try:
        method, path, protocol, headers, body = parse_request_file(args.request)
    except ValueError as e:
        print(f"Error parsing request file: {e}")
        return

    for _ in range(args.requests_count):
        payload_value = args.payload if args.payload else None
        response = send_request(args.target, method, path, headers, body, payload_value=payload_value)
        time.sleep(random.uniform(2, 3))

        if response is not None:
            print(f"Status code: {response.status_code}")

if __name__ == '__main__':
    main()
