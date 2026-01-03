import time

title = "Lizzys Blocklist"
description = "A list of annoying spam domains to help users block unwanted content."
homepage = "https://github.com/cuteminded/hostBlocklist"

domains = []

def readDomains():
    with open('domains.txt', 'r') as domainsFile:
        uniqueDomains = list(dict.fromkeys(domainsFile))
        for domain in uniqueDomains:
            domains.append(domain.strip())

def writeDomains():
    with open('domains.txt', 'w') as file:
        for line in domains:
            file.write(f"{line}\n")

def addPrefix():
    for domain in domains.copy():
        domains.append("www.{0}".format(domain))
    domains.sort(key=len)

def readme():
    lines = []
    lines.append("# {0}".format(title))
    lines.append(" ")
    lines.append("{0}<br>".format(description))
    lines.append(" ")
    lines.append("## Domains")
    lines.append("Number of Domains: {0}<br>".format(len(domains)))
    lines.append("Last modified: {0}<br>".format(time.strftime("%d-%m-%Y")))
    lines.append(" ")
    lines.append("## Usage")
    lines.append(" ")
    lines.append("You can use this blocklist to enhance your ad-blocker, firewall, or DNS filtering system. To integrate this list, follow these steps:")
    lines.append("1. Download the latest blocklist from this repository.")
    lines.append("2. Add the domains to your preferred blocking tool (e.g., Pi-hole, AdGuard, uBlock Origin, or custom DNS configurations).")
    lines.append("3. Enjoy a cleaner browsing experience!")
    lines.append(" ")
    lines.append("## Contributing")
    lines.append(" ")
    lines.append("If you want to contribute to this blocklist, please submit a pull request with your changes. Your help is much appreciated!")

    with open("../README.md", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def hosts():
    lines = []
    lines.append("# Title: {0}".format(title))
    lines.append("# Expires: 1 day")
    lines.append("# Description: {0}".format(description))
    lines.append("# Homepage: {0}".format(homepage))
    lines.append("# Syntax: Hosts (including possible subdomains)")
    lines.append("# Number of entries: {0}".format(len(domains)))
    lines.append("#")
    for domain in domains:
        lines.append("0.0.0.0 {0}".format(domain))
    with open("../hosts.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def adguard():
    lines = []
    lines.append("!")
    lines.append("! Title: {0}".format(title))
    lines.append("! Expires: 1 day")
    lines.append("! Description: {0}".format(description))
    lines.append("! Homepage: {0}".format(homepage))
    lines.append("!")
    lines.append("")
    for domain in domains:
        lines.append("127.0.0.1 {0}".format(domain))
    with open("../adguard.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def adblock():
    lines = []
    lines.append("[Adblock Plus]")
    lines.append("! Title: {0}".format(title))
    lines.append("! Expires: 1 day")
    lines.append("! Description: {0}".format(description))
    lines.append("! Homepage: {0}".format(homepage))
    lines.append("! Syntax: AdBlock")
    lines.append("! Number of entries: {0}".format(len(domains)))
    lines.append("!")
    lines.append("")
    for domain in domains:
        lines.append("||{0}^".format(domain))
    with open("../adblock.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def main():
    readDomains()
    writeDomains()
    addPrefix()
    hosts()
    readme()
    adguard()
    adblock()
main()
