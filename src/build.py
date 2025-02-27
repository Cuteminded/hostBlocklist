import time

title = "Lizzys Blocklist"
description = "A list of annoying spam domains"
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
    domains.sort(key=len)

def readme():
    lines = []
    lines.append("# {0}".format(title))
    lines.append("{0}<br>".format(description))
    lines.append("Number of Domains: {0}<br>".format(len(domains)))
    lines.append("Last modified: {0}<br>".format(time.strftime("%d-%m-%Y")))
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
    hosts()
    readme()
    adguard()
    adblock()
main()
