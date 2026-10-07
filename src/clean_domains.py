#!/usr/bin/env python3
import argparse
import codecs
import ipaddress
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

try:
    import dns.exception
    import dns.rdatatype
    import dns.resolver
except ImportError:
    sys.exit("Install dnspython first: python3 -m pip install dnspython")


def normalize_domain(value):
    """Normalize domain names. Leave invalid or unsupported entries unchanged."""
    try:
        domain = value.encode("idna").decode("ascii").lower()
    except UnicodeError:
        return None
    if domain.endswith("."):
        domain = domain[:-1]
    if len(domain) > 253 or "." not in domain:
        return None
    try:
        ipaddress.ip_address(domain)
        return None
    except ValueError:
        pass
    label_pattern = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    if not all(re.fullmatch(label_pattern, label) for label in domain.split(".")):
        return None
    return domain + "."


def check_domain(domain, resolvers):
    for resolver in resolvers:
        try:
            # A missing NS record does not mean the domain is gone.
            resolver.resolve(domain, "NS", search=False, raise_on_no_answer=False)
            return False, "name exists in DNS"
        except dns.resolver.NXDOMAIN as error:
            responses = list(error.responses().values())
            # An alias may still exist even if its target is gone.
            if not responses or any(response.answer for response in responses):
                return False, "uncertain response or alias found, keeping domain"
            if not all(
                any(rr.rdtype == dns.rdatatype.SOA for rr in response.authority)
                for response in responses
            ):
                return False, "NXDOMAIN without an SOA record, keeping domain"
        except (dns.exception.DNSException, OSError) as error:
            return False, f"check failed ({type(error).__name__}), keeping domain"
    return True, "both DNS providers returned NXDOMAIN"


def save_result(path, original, updated):
    """Replace the file using a temporary file."""
    if path.read_bytes() != original:
        raise RuntimeError("The file changed during the check. Nothing saved.")
    mode = stat.S_IMODE(path.stat().st_mode)
    temp_fd, temp_name = tempfile.mkstemp(prefix=path.name + ".tmp-", dir=path.parent)
    try:
        with os.fdopen(temp_fd, "wb") as output:
            output.write(updated)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temp_name, mode)
        if path.read_bytes() != original:
            raise RuntimeError("The file changed while saving. Original file left in place.")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", default="domains.txt", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Preview removals without changing the file")
    args = parser.parse_args()
    path = args.file.resolve(strict=True)
    original = path.read_bytes()
    bom = codecs.BOM_UTF8 if original.startswith(codecs.BOM_UTF8) else b""
    lines = original[len(bom):].decode("utf-8").splitlines(keepends=True)

    resolvers = []
    for nameserver in ("1.1.1.1", "8.8.8.8"):
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [nameserver]
        resolver.timeout = 2
        resolver.lifetime = 5
        resolvers.append(resolver)

    kept = []
    cache = {}
    removed = 0
    for number, line in enumerate(lines, start=1):
        value = line.strip()
        if not value or value.startswith("#"):
            kept.append(line)
            continue
        domain = normalize_domain(value)
        if domain is None:
            delete, reason = False, "invalid or unsupported format, keeping entry"
        else:
            if domain not in cache:
                cache[domain] = check_domain(domain, resolvers)
            delete, reason = cache[domain]
        action = "REMOVE" if delete else "KEEP"
        print(f"[{number}/{len(lines)}] {action} {value}: {reason}", flush=True)
        if delete:
            removed += 1
        else:
            kept.append(line)

    if args.dry_run:
        print(f"\nPreview complete. Lines to remove: {removed}. Nothing changed.")
    elif removed:
        updated = bom + "".join(kept).encode("utf-8")
        save_result(path, original, updated)
        print(f"\nDone. Lines removed from {path}: {removed}.")
    else:
        print("\nDone. Nothing removed. File unchanged.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nCancelled.")
    except (OSError, UnicodeError, RuntimeError) as error:
        sys.exit(f"Error: {error}")
