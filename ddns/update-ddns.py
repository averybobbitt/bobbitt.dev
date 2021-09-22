import os
import sys
import json
import requests
import blessings

term = blessings.Terminal()

HOSTS_FILE = f"{os.path.abspath(os.path.dirname(sys.argv[0]))}/hostnames.json"
IP_ADDRESS = requests.get("https://api.ipify.org").text
# IP_ADDRESS = "test_not_real_ip"

with open(HOSTS_FILE) as f:
    hosts = json.load(f)

for host in hosts:
    # Set variables
    usr = hosts[host]["username"]
    pwd = hosts[host]["password"]
    domain = hosts[host]["hostname"]

    # Make request
    print(term.bold(term.white((f"\nChanging IP for {domain}..."))))
    request = requests.post(
        f"https://{usr}:{pwd}@domains.google.com/nic/update?hostname={domain}&myip={IP_ADDRESS}"
    ).text

    # Print output based on result
    if request == f"nochg {IP_ADDRESS}":
        print(term.green((f"The IP for {domain} has not changed.")))
    elif request == f"good {IP_ADDRESS}":
        print(term.green((f"The IP for {domain} is now {IP_ADDRESS}")))
    elif request == f"nohost":
        print(term.red((f"The domain {domain} does not exist.")))
    elif request == f"badauth":
        print(term.red((f"The username and password are not correct.")))
    elif request == f"notfqdn":
        print(
            term.red((f"The hostname {domain} is not a fully-qualified domain name."))
        )
    elif request == f"badagent":
        print(term.red((f"This script is sending bad requests.")))
    elif request == f"abuse":
        print(term.red((f"DDNS for {domain} has been blocked for abuse.")))
    elif request == f"911":
        print(term.red((f"An error has occured on Google's end.")))
