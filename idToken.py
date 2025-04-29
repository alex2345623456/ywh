import requests
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

session = requests.Session()
session.trust_env = False

def signup(email):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyBP5V3Jkn2vcWvOP9Dg7MEClljUkDtk4a4"
    payload = {
        "returnSecureToken": True,
        "email": email,
        "password": "Alex@2345678",
        "clientType": "CLIENT_TYPE_WEB"
    }
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://webapp.monisnap.com"
    }
    try:
        response = session.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return (email, data['idToken'])
    except:
        pass
    return (email, None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True)
    parser.add_argument("-t", "--threads", type=int, default=10)
    args = parser.parse_args()

    try:
        with open(args.path, "r") as f:
            emails = [line.strip() for line in f if line.strip()]
    except:
        return

    results = [None] * len(emails)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_index = {executor.submit(signup, email): idx for idx, email in enumerate(emails)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                result = future.result()
                results[idx] = result
            except:
                results[idx] = (emails[idx], None)

    with open("email.txt", "w") as f_email, open("idToken.txt", "w") as f_token:
        for email, idToken in results:
            f_email.write((email or "") + "\n")
            f_token.write((idToken or "") + "\n")

if __name__ == "__main__":
    main()
