import os
import sys
import time
import yaml
import signal
import argparse
import urllib3

config = {}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Signal
def signal_handler(sig, frame):
    print("\n\n...Aborted\n")
    sys.exit(0)

# Exit
def exit(msg):
    print(f"\n{msg}\n")
    time.sleep(1)
    os.kill(os.getppid(), signal.SIGTERM)

# Args
def get_args(user=True, token=True):
    args = argparse.ArgumentParser(description='HomeWizard user management')
    args.add_argument('--hostname', required=True, help='HomeWizard device hostname or IP')
    if user:
        args.add_argument('--username', required=True, help='Requested username')
    if token:
        args.add_argument('--token', required=True, help='Token for authorizing your request')
    return args.parse_args()

# Headers
def get_headers(token=None):
    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "2"
    }
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# Info
def verify():
    infotext = f"""Before continuing, make sure that:\n
- You are aware that using this tool is AT YOUR OWN RISK
- You have read https://api-documentation.homewizard.com/docs/v2/authorization
- Using the APIv2 is AT YOUR OWN RISK
"""
    print(infotext)
    agree = input("Type \"AGREE\" if you still want to continue: ")
    print("")
    if agree != "AGREE":
        exit("Verification failed")
    print("Note that you have AGREED to using this script at your own risk.\n")

# Config
def get_config():
    config = {}
    configfile = "homewizard-apiv2-exporter.yml"
    if os.path.isfile(configfile):
        with open(configfile, "r") as file:
            config = yaml.safe_load(file)
    else:
        exit(f"ERROR: Config file not found: {configfile}")
    return config