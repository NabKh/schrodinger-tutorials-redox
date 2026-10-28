"""Check charge, multiplicity and electron count of Jaguar input files before submitting.

Usage:  python check_inputs.py <file.in or folder> [...]
The expected charge and multiplicity of each job are read from ../inputs/states.csv.
"""

import csv
import re
import sys
from pathlib import Path

Z = {"H": 1, "C": 6, "N": 7, "O": 8, "F": 9, "S": 16, "Cl": 17, "Br": 35}
STATES = Path(__file__).resolve().parent.parent / "inputs" / "states.csv"


def read_input(path):
    text = path.read_text()
    gen = re.search(r"&gen\s*\n(.*?)\n&", text, re.DOTALL).group(1)
    kw = dict(line.strip().split("=", 1) for line in gen.splitlines() if "=" in line)
    zmat = re.search(r"&zmat\s*\n(.*?)\n&", text, re.DOTALL).group(1)
    elements = [
        re.match(r"[A-Z][a-z]?", line.split()[0]).group() for line in zmat.splitlines() if line.strip()
    ]
    return kw, elements


def check(path, states):
    kw, elements = read_input(path)
    job = path.stem
    if kw.get("molchg") == "??" or kw.get("multip") == "??":
        return f"{job:18s} TODO   molchg/multip still '??' - fill them in"
    charge, mult = int(kw.get("molchg", 0)), int(kw.get("multip", 1))
    n_el = sum(Z[e] for e in elements) - charge
    unpaired = mult - 1
    problems = []
    if (n_el - unpaired) % 2:
        problems.append(f"{n_el} electrons cannot have multiplicity {mult}")
    if job in states:
        want = states[job]
        if (charge, mult) != (int(want["charge"]), int(want["multiplicity"])):
            problems.append(
                f"expected molchg={want['charge']} multip={want['multiplicity']} ({want['note']})"
            )
    else:
        problems.append("not in states.csv")
    shell = "open shell, unrestricted (iuhf default)" if mult > 1 else "closed shell"
    status = "FAIL" if problems else "ok"
    line = f"{job:18s} {status:6s} {len(elements):3d} atoms  N={n_el:4d}  molchg={charge:+d}  multip={mult}  {shell}"
    return line + "".join(f"\n{'':25s}-> {p}" for p in problems)


def main(args):
    states = {row["job"]: row for row in csv.DictReader(STATES.open())}
    files = []
    for arg in args:
        p = Path(arg)
        files += sorted(p.rglob("*.in")) if p.is_dir() else [p]
    for f in files:
        if not re.search(r"\.\d\d\.in$", f.name):  # skip Jaguar restart files (name.01.in)
            print(check(f, states))


if __name__ == "__main__":
    main(sys.argv[1:] or ["."])
