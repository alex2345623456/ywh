import subprocess
import argparse

def run_command():
    command = r"curl -s -o /dev/null -w '%{redirect_url}\n' 'https://auth.globus-baumarkt.de/authz-srv/authz?approval_prompt=auto&shop_source=login&ui_locales=de&user_origin=shop&scope=openid+offline_access+email+profile+groups&response_type=code&redirect_uri=https%3A%2F%2Fwww.globus-baumarkt.de%2Faccount%2Fsso_return&client_id=e36f12d0-319e-4f6c-9995-f02627b2e21c&state=8c1d5baf6954480e8cf2db9ecef28d11' | sed -n 's/.*requestId=\([^&]*\).*/\1/p' > requestId.txt && sudo python3 loop.py -r request.txt -p requestId.txt -x 1 -t 28 -target https://auth.globus-baumarkt.de -delay 0.1-1 -loop 1"
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()

    if process.returncode == 0:
        print(stdout.decode().strip())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-loop", type=int, default=1)
    args = parser.parse_args()

    for _ in range(args.loop):
        run_command()

if __name__ == "__main__":
    main()
