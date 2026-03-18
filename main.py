import argparse
import subprocess
import random
import re

def get_current_mac(interface):
    result = subprocess.check_output(["ip", "link", "show", interface]).decode()
    mac = re.search(r"link/ether ([0-9a-f:]{17})", result)
    if mac:
        return mac.group(1)
    return None

def change_mac(interface, new_mac):
    subprocess.call(["sudo", "ip", "link", "set", interface, "down"])
    subprocess.call(["sudo", "ip", "link", "set", interface, "address", new_mac])
    subprocess.call(["sudo", "ip", "link", "set", interface, "up"])

def random_mac():
    mac = [0x02, random.randint(0x00,0x7f),
           random.randint(0x00,0xff),
           random.randint(0x00,0xff),
           random.randint(0x00,0xff),
           random.randint(0x00,0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def main():
    parser = argparse.ArgumentParser(description="MAC Address Spoofer CLI Tool")

    parser.add_argument("-i","--interface", help="Network interface", required=True)
    parser.add_argument("-r","--random", action="store_true", help="Generate random MAC")
    parser.add_argument("-s","--set", help="Set custom MAC address")
    parser.add_argument("--show", action="store_true", help="Show current MAC")

    args = parser.parse_args()

    if args.show:
        mac = get_current_mac(args.interface)
        print("Current MAC:", mac)

    elif args.random:
        new_mac = random_mac()
        print("Random MAC:", new_mac)
        change_mac(args.interface, new_mac)

    elif args.set:
        print("Changing MAC to:", args.set)
        change_mac(args.interface, args.set)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
