#!/usr/bin/env python3

import signal
import requests

import hwhelper

def main():
    
    # Setup

    exit = hwhelper.exit
    signal.signal(signal.SIGINT, hwhelper.signal_handler)

    args = hwhelper.get_args(user=False)
    hdrs = hwhelper.get_headers(token=args.token)
    HOST=args.hostname

    # Verify

    print(f"\nThis action will access HomeWizard device \"{HOST}\"" )
    hwhelper.verify()

    # List users

    print("Retrieving user list...\n")
    try:
        response = requests.get(f"https://{HOST}/api/user", headers=hdrs, timeout=5, verify=False)
    except requests.exceptions.Timeout:
        exit(f"ERROR: Timeout connecting to device \"{HOST}\", exiting...")
    except Exception as e:
        print("Unexpected error:")
        print(e)
        exit("Exiting...")

    print("Captured result:\n")
    print(response.text)
    if response is not None and response.status_code != 200:
        print("\nUnexpected response, please consult the capture result")


if __name__ == '__main__':
    main()
    print("\nScript finished\n")
