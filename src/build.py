import time

domains = []

def readDomains():
    with open('domains.txt', 'r') as domainsFile:
        for domain in domainsFile:
            domains.append(domain.strip())
    domains.sort(key=len)

def readme():
    lines = []
    lines.append("# Lizzys Blocklist")
    lines.append("List of annoying domains<br>")
    lines.append("Number of Domains: {}<br>".format(len(domains)))
    lines.append("Last modified: {}<br>".format(time.strftime("%d-%m-%Y")))
    lines.append("```")
    for domain in domains:
        lines.append("0.0.0.0 {0}".format(domain))
    lines.append("```")
    with open("../README.md", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def hosts():
    lines = []
    lines.append("# Title: Lizzys Blocklist")
    lines.append("# Expires: 1 day")
    lines.append("# Description: A list of annoying spam domains")
    lines.append("# Homepage: https://github.com/FzzyLizzyy/hostBlocklist")
    lines.append("# Syntax: Hosts (including possible subdomains)")
    lines.append("# Number of entries: {}".format(len(domains)))
    lines.append("#")
    for domain in domains:
        lines.append("0.0.0.0 {0}".format(domain))
    with open("../hosts.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def adguard():
    lines = []
    lines.append("!")
    lines.append("! Title: Lizzys Blocklist")
    lines.append("! Expires: 1 day")
    lines.append("! Description: A list of annoying spam domains")
    lines.append("! Homepage: https://github.com/FzzyLizzyy/hostBlocklist")
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
    lines.append("! Title: Lizzys Blocklist")
    lines.append("! Expires: 1 day")
    lines.append("! Description: A list of annoying spam domains")
    lines.append("! Homepage: https://github.com/FzzyLizzyy/hostBlocklist")
    lines.append("! Syntax: AdBlock")
    lines.append("! Number of entries: {}".format(len(domains)))
    lines.append("!")
    lines.append("")
    for domain in domains:
        lines.append("||{0}^".format(domain))
    with open("../adblock.txt", "w") as file:
        for line in lines:
            file.write(f"{line}\n")

def main():
    readDomains()
    hosts()
    readme()
    adguard()
    adblock()

main()
