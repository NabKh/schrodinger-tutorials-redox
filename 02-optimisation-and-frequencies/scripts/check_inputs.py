"""Check charge, multiplicity and electron count of Jaguar input files before submitting.

Usage:  python check_inputs.py <file.in or folder> [...]
The expected charge and multiplicity of each job are read from ../inputs/states.csv.
A new job needs a new row there (job,family,charge,multiplicity,...), or it is reported as FAIL.
"""

import csv
import re
import sys
from pathlib import Path

SYMBOLS = (
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn "
    "Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce "
    "Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn"
).split()
Z = {s: i for i, s in enumerate(SYMBOLS, 1)}
STATES = Path(__file__).resolve().parent.parent / "inputs" / "states.csv"


def read_input(path):
    text = path.read_text(errors="replace")
    gen = re.search(r"&gen\s*\n(.*?)\n\s*&", text, re.DOTALL | re.IGNORECASE).group(1)
    kw = {}
    for line in gen.splitlines():
        line = line.split("#")[0].split("!")[0]  # drop comments
        kw.update({k.lower(): v for k, v in re.findall(r"(\w+)\s*=\s*(\S+)", line)})
    zmat = re.search(r"&zmat\s*\n(.*?)\n\s*&", text, re.DOTALL | re.IGNORECASE).group(1)
    elements = []
    for line in zmat.splitlines():
        if line.strip():
            label = re.match(r"[A-Za-z]+", line.split()[0]).group()  # C1, CL1, Cl1 -> C, Cl, Cl
            symbol = label[:2].capitalize() if label[:2].capitalize() in Z else label[0].upper()
            elements.append(symbol)
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
            problems.append(f"expected molchg={want['charge']} multip={want['multiplicity']} ({want['note']})")
    else:
        problems.append("not in states.csv: add a row for this job")
    iuhf = kw.get("iuhf")
    if mult > 1:
        shell = "open shell, " + ("unrestricted (iuhf=1)" if iuhf == "1" else f"iuhf={iuhf or '2 (default)'}")
    else:
        shell = "closed shell" + (f", iuhf={iuhf}" if iuhf else "")
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
