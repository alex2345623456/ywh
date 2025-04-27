import argparse
import threading
import requests
import urllib.parse

URL = "https://auth.globus-baumarkt.de/authz-srv/authz"
PARAMS = {
    "approval_prompt": "auto",
    "shop_source": "login",
    "ui_locales": "de",
    "user_origin": "shop",
    "scope": "openid offline_access email profile groups",
    "response_type": "code",
    "redirect_uri": "https://www.globus-baumarkt.de/account/sso_return",
    "client_id": "e36f12d0-319e-4f6c-9995-f02627b2e21c",
    "state": "8c1d5baf6954480e8cf2db9ecef28d11"
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.globus-baumarkt.de/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}

lock = threading.Lock()

def send_request():
    try:
        response = requests.get(URL, params=PARAMS, headers=HEADERS, allow_redirects=False)
        if response.status_code == 302:
            location = response.headers.get("Location", "")
            parsed_url = urllib.parse.urlparse(location)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            request_id = query_params.get("requestId", [None])[0]
            if request_id:
                with lock:
                    with open("requestId.txt", "a") as f:
                        f.write(request_id + "\n")
    except:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=int, default=1)
    args = parser.parse_args()

    with open("requestId.txt", "w") as f:
        pass

    threads = []
    for _ in range(args.t):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
