"""Summarise a Jaguar optimisation + frequency output (.out) and rebuild G by hand.

Usage:  python summarise_job.py job.out [job2.out ...]
"""

import re
import sys
from pathlib import Path

HARTREE_KCAL = 627.5095


def last(pattern, text, cast=str):
    hits = re.findall(pattern, text, re.MULTILINE)
    return cast(hits[-1]) if hits else None


def frequencies(text):
    freqs, syms, ints = [], [], []
    for block in re.findall(r"^  frequencies(.*)\n  symmetries(.*)\n  intensities(.*)$", text, re.MULTILINE):
        freqs += [float(x) for x in block[0].split()]
        syms += block[1].split()
        ints += [float(x) for x in block[2].split()]
    return freqs, syms, ints


def summarise(path):
    t = Path(path).read_text(errors="replace")
    stoich = last(r"Stoichiometry:\s+(\S+)", t) or ""
    natoms = sum(int(n or 1) for _, n in re.findall(r"([A-Z][a-z]?)(\d*)", stoich)) or None
    freqs, syms, _ = frequencies(t)
    e = last(r"^\s*SCFE:.*?(-?\d+\.\d+) hartrees", t, float)
    zpe = last(r"The zero point energy \(ZPE\):\s+(-?\d+\.\d+)", t, float)
    g_table = last(r"^  total\s+\S+\s+\S+\s+\S+\s+\S+\s+(-?\d+\.\d+)", t, float)
    g_tot = last(r"Total Gibbs free energy, Gtot \(Htot - T\*S\):\s+(-?\d+\.\d+)", t, float)
    charge = last(r"net molecular charge:\s+(-?\d+)", t)
    mult = last(r"^  multiplicity:\s+(\d+)", t) or "1 (not printed)"
    pg = last(r"Molecular Point Group:\s+(\S+)", t)
    pg_used = last(r"Point Group used:\s+(\S+)", t)
    hours = int(last(r"Total elapsed time:\s+(\d+)", t) or 0) / 3600
    rows = [
        ("job", Path(path).stem),
        ("stoichiometry", stoich),
        ("level", last(r"SCF calculation type:\s+(\S+)", t)),
        ("basis", last(r"basis set:\s+(\S+)", t)),
        ("solvent", last(r"Solvent:\s+(\S+)", t) or "none (gas phase)"),
        ("charge / multiplicity", f"{charge} / {mult}"),
        ("electrons", last(r"number of electrons\.+\s+(\d+)", t)),
        ("<S**2> (ideal S(S+1))", last(r"<S\*\*2> \.\.\.\s+(\S+)", t) or "closed shell"),
        ("point group (used)", f"{pg} ({pg_used})"),
        ("smallest eigenvalue of S", last(r"smallest eigenvalue of S:\s+(\S+)", t)),
        ("geometry steps", len(re.findall(r"^\s*SCFE:", t, re.MULTILINE))),
        ("optimisation converged", "yes" if "Geometry optimization complete" in t else "NO"),
        ("final energy E (Eh)", e),
        ("vibrations (expected 3N-6)", f"{len(freqs)} ({3 * natoms - 6 if natoms else '?'})"),
        ("imaginary frequencies", last(r"Number of imaginary frequencies:\s+(\d+)", t)),
        ("lowest three (cm-1)", ", ".join(f"{f:.1f} {s}" for f, s in zip(freqs[:3], syms[:3]))),
        ("quasi-harmonic floor", last(r"minimum value of\s+(\S+ cm\^-1)", t) or "not applied"),
        ("rotational symmetry number", last(r"rotational symmetry number:\s+(\d+)", t)),
        ("T, P", last(r"(T =\s+\S+ K, P = \S+ atm)", t)),
        ("ZPE (kcal/mol)", zpe),
        ("G_thermal from table (kcal/mol)", g_table),
        ("Gtot printed (Eh)", g_tot),
        ("wall time (h)", f"{hours:.2f}"),
    ]
    for k, v in rows:
        print(f"  {k:32s} {v}")
    if None not in (e, zpe, g_table, g_tot):
        g_hand = e + (zpe + g_table) / HARTREE_KCAL
        print(
            f"  {'G = E + (ZPE + G_table)/627.5095':32s} {g_hand:.6f} Eh "
            f"(differs from printed by {(g_hand - g_tot) * HARTREE_KCAL:+.3f} kcal/mol)"
        )
    print()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        summarise(p)
