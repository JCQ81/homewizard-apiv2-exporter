#!/usr/bin/env python3

import time
import signal
import requests

import hwhelper

def main():

    # Setup

    exit = hwhelper.exit
    signal.signal(signal.SIGINT, hwhelper.signal_handler)

    args = hwhelper.get_args(token=False)
    hdrs = hwhelper.get_headers()
    HOST=args.hostname
    USER=args.username
    TYPE="local"

    # Verify

    print(f"\nThis action will create a user \"{USER}\" with token on HomeWizard device \"{HOST}\"" )
    hwhelper.verify()

    infotext = """The procedure consists of the following steps:
    1. Send pairing requests (which does this script for you every second)
    2. You press/hold the button on the HomeWizard device for 1 to 3 seconds
    3. If authorized, you will be given a token. Write this down!!!
    """
    print(infotext)

    # Create user and get token

    input("Press <enter> to start sending pairing requests: ")
    print("\nStart sending requests...\n")

    done = False
    showmsg = True
    response = None
    while not done:
        try:
            data = {"name": f"{TYPE}/{USER}"}
            response = requests.post(f"https://{HOST}/api/user", json=data, headers=hdrs, timeout=5, verify=False)
        except requests.exceptions.Timeout:
            exit(f"ERROR: Timeout connecting to device \"{HOST}\", exiting...")
        except Exception as e:
            print("Unexpected error:")
            print(e)
            exit("Exiting...")

        if showmsg:
            print("Now press/hold the button on the HomeWizard device for 1 to 3 seconds... ")
            showmsg = False

        if response is not None and response.status_code == 200:
            done = True
        else:
            time.sleep(1)

    print("\nCaptured result:\n")
    print(response.json())
    print("\nThe token is only given this once, STORE IT SAFELY !!\n")


if __name__ == '__main__':
    main()
    print("Script finished\n")
