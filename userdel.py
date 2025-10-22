#!/usr/bin/env python3

import time
import signal
import urllib3
import requests

import hwhelper

def main():

    exit = hwhelper.exit
    signal.signal(signal.SIGINT, hwhelper.signal_handler)

    args = hwhelper.get_args()
    hdrs = hwhelper.get_headers(token=args.token)
    HOST=args.hostname
    USER=args.username
    TYPE="local"

    ################################
    # Verify
    ################################

    print(f"\nThis action will delete user \"{USER}\" on HomeWizard device \"{HOST}\"" )
    hwhelper.verify()

    ################################
    # Delete user
    ################################

    input(f"Press <enter> to request the deletion of user \"{USER}\": ")

    try:
        data = {"name": f"{TYPE}/{USER}"}
        response = requests.delete(f"https://{HOST}/api/user", json=data, headers=hdrs, timeout=5, verify=False)
    except requests.exceptions.Timeout:
        exit(f"ERROR: Timeout connecting to device \"{HOST}\", exiting...")
    except Exception as e:
        print("Unexpected error:")
        print(e)
        exit("Exiting...")

    print("\nCaptured result:\n")
    print(response.text)
    if response is not None and response.status_code == 204:
        print("\nUser deleted succesfully\n")
    else:
        print("\nUnexpected response, please consult the capture result\n")


if __name__ == '__main__':
    main()
    print("Script finished\n")
