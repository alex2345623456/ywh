import argparse
import requests
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
]

def parse_request_file(request_file):
    with open(request_file, 'r') as file:
        data = file.read()
    if '~~~' in data:
        header_section, body_section = data.split('~~~', 1)
    else:
        parts = data.split('\n\n', 1)
        header_section = parts[0]
        body_section = parts[1] if len(parts) > 1 else None
    header_section = header_section.strip()
    body_section = body_section.strip() if body_section else None
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

def replace_placeholders(text, payload1, payload2, payload3):
    if text is None:
        return None
    text = text.replace('$$$', str(generate_random_number()))
    if payload1 is not None:
        text = text.replace('PAYLOAD1', payload1)
    if payload2 is not None:
        text = text.replace('PAYLOAD2', payload2)
    if payload3 is not None:
        text = text.replace('PAYLOAD3', payload3)
    return text

def random_user_agent():
    return random.choice(USER_AGENTS)

def send_request(target_url, method, path, headers, body=None, payload1=None, payload2=None, payload3=None):
    path = replace_placeholders(path, payload1, payload2, payload3)
    url = target_url + path
    headers = {key: replace_placeholders(value, payload1, payload2, payload3) for key, value in headers.items()}
    headers["User-Agent"] = random_user_agent()
    body = replace_placeholders(body, payload1, payload2, payload3)
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
            return None
    except requests.RequestException:
        return None
    return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request', required=True)
    parser.add_argument('-target', '--target', required=True)
    parser.add_argument('-x', '--requests_count', type=int, default=1)
    parser.add_argument('-p', '--payload')
    parser.add_argument('-p2', '--payload2')
    parser.add_argument('-p3', '--payload3')
    args = parser.parse_args()
    try:
        method, path, protocol, headers, body = parse_request_file(args.request)
    except ValueError:
        return
    for _ in range(args.requests_count):
        payload1 = args.payload if args.payload else None
        payload2 = args.payload2 if args.payload2 else None
        payload3 = args.payload3 if args.payload3 else None
        response = send_request(args.target, method, path, headers, body, payload1, payload2, payload3)
        time.sleep(random.uniform(2, 3))
        if response is not None:
            print(f"Status code: {response.status_code}")

if __name__ == '__main__':
    main()
