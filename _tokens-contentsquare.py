import requests
import random
import string
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor
import sys
import os

file_lock = threading.Lock()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
]

def suppress_output():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

def random_session_token(length=32):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_initial_csrf_token():
    url = "https://community.contentsquare.com/site/_tokens"
    params = {
        "name": "register",
        "yip_csrf_token": "placeholder"
    }
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("yip_csrf_token")
    except:
        pass
    return None

def send_request(yip_csrf_token):
    url = "https://community.contentsquare.com/site/_tokens"
    session_token = random_session_token()
    params = {
        "name": "register",
        "yip_csrf_token": yip_csrf_token
    }
    headers = {
        "Cookie": f"Session={session_token}; cookiePrivacyLevel=required",
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            token = json_data.get("_token", "")
            with file_lock:
                with open("session.txt", "a") as s_file, open("token.txt", "a") as t_file:
                    s_file.write(f"{session_token}\n")
                    t_file.write(f"{token}\n")
    except:
        pass

def main():
    suppress_output()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads", type=int, default=1)
    args = parser.parse_args()

    yip_csrf_token = get_initial_csrf_token()
    if not yip_csrf_token:
        return

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(send_request, yip_csrf_token) for _ in range(args.threads)]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
