"""Summarise a Jaguar optimisation + frequency output (.out) and rebuild G by hand.

Usage:  python summarise_job.py job.out [job2.out ...]
A line that is not found in the output is printed as NOT FOUND: find it by hand (Ctrl+F) and
check whether the job ended early or the wording differs in this Jaguar version.
"""

import re
import sys
from pathlib import Path

HARTREE_KCAL = 627.5095
MISSING = "NOT FOUND"


def last(pattern, text, cast=str):
    hits = re.findall(pattern, text, re.MULTILINE)
    return cast(hits[-1]) if hits else None


def frequencies(text):
    """Frequencies, symmetry labels and IR intensities of every block; labels '?' if not printed."""
    freqs, syms, ints = [], [], []
    for block in re.finditer(r"^  frequencies(.*)\n((?:  (?!frequencies).*\n)*)", text, re.MULTILINE):
        f = [float(x) for x in block.group(1).split()]
        rest = block.group(2)
        s = re.search(r"^  symmetries(.*)$", rest, re.MULTILINE)
        i = re.search(r"^  intensities(.*)$", rest, re.MULTILINE)
        freqs += f
        syms += s.group(1).split() if s else ["?"] * len(f)
        ints += [float(x) for x in i.group(1).split()] if i else [0.0] * len(f)
    return freqs, syms, ints


def show(value):
    return MISSING if value is None else value


def summarise(path):
    t = Path(path).read_text(errors="replace")
    stoich = last(r"Stoichiometry:\s+(\S+)", t) or ""
    natoms = sum(int(n or 1) for _, n in re.findall(r"([A-Z][a-z]?)(\d*)", stoich)) or None
    freqs, syms, _ = frequencies(t)
    scfe = re.findall(r"^\s*SCFE:.*?(-?\d+\.\d+) hartrees", t, re.MULTILINE)
    # the final energy is the last SCFE line; SCFE lines count every SCF, so they can exceed the geometry steps
    e = float(scfe[-1]) if scfe else None
    zpe = last(r"The zero point energy \(ZPE\):\s+(-?\d+\.\d+)", t, float)
    g_table = last(r"^  total\s+\S+\s+\S+\s+\S+\s+\S+\s+(-?\d+\.\d+)", t, float)
    g_tot = last(r"Total Gibbs free energy, Gtot \(Htot - T\*S\):\s+(-?\d+\.\d+)", t, float)
    charge = last(r"net molecular charge:\s+(-?\d+)", t)
    mult = last(r"^  multiplicity:\s+(\d+)", t)
    s2 = last(r"<S\*\*2> \.\.\.\s+(\S+)", t)
    seconds = last(r"Total elapsed time:\s+(\d+)", t, int)
    point_group = show(last(r"Molecular Point Group:\s+(\S+)", t))
    point_group_used = show(last(r"Point Group used:\s+(\S+)", t))
    rows = [
        ("job", Path(path).stem),
        ("stoichiometry", stoich or MISSING),
        ("level", show(last(r"SCF calculation type:\s+(\S+)", t))),
        ("basis", show(last(r"basis set:\s+(\S+)", t))),
        ("solvent", last(r"Solvent:\s+(\S+)", t) or "none found (gas phase?)"),
        ("charge / multiplicity", f"{show(charge)} / {show(mult)}"),
        ("electrons", show(last(r"number of electrons\.+\s+(\d+)", t))),
        ("<S**2> (ideal S(S+1))", s2 if s2 else ("no <S**2> line (closed shell?)" if mult in (None, "1") else MISSING)),
        ("point group (used)", f"{point_group} ({point_group_used})"),
        ("smallest eigenvalue of S", show(last(r"smallest eigenvalue of S:\s+(\S+)", t))),
        ("SCFE lines (>= geometry steps)", len(scfe)),
        ("optimisation converged", "yes" if "Geometry optimization complete" in t else "NO (or not an optimisation)"),
        ("final energy E (Eh)", show(e)),
        ("vibrations (expected 3N-6)", f"{len(freqs)} ({3 * natoms - 6 if natoms else '?'})"),
        ("imaginary frequencies", show(last(r"Number of imaginary frequencies:\s+(\d+)", t))),
        ("lowest three (cm-1)", ", ".join(f"{f:.1f} {s}" for f, s in zip(freqs[:3], syms[:3])) or MISSING),
        ("quasi-harmonic floor", last(r"minimum value of\s+(\S+ cm\^-1)", t) or "no Quasi-Harmonic line found"),
        ("rotational symmetry number", show(last(r"rotational symmetry number:\s+(\d+)", t))),
        ("T, P", show(last(r"(T =\s+\S+ K, P = \S+ atm)", t))),
        ("ZPE (kcal/mol)", show(zpe)),
        ("G_thermal from table (kcal/mol)", show(g_table)),
        ("Gtot printed (Eh)", show(g_tot)),
        ("wall time (h)", f"{seconds / 3600:.2f}" if seconds is not None else MISSING),
    ]
    for k, v in rows:
        print(f"  {k:32s} {v}")
    if None not in (e, zpe, g_table, g_tot):
        g_hand = e + (zpe + g_table) / HARTREE_KCAL
        print(
            f"  {'G = E + (ZPE + G_table)/627.5095':32s} {g_hand:.6f} Eh "
            f"(differs from printed by {(g_hand - g_tot) * HARTREE_KCAL:+.3f} kcal/mol)"
        )
    else:
        print(f"  {'G rebuilt by hand':32s} {MISSING}: E, ZPE, the total row or Gtot is missing")
    print()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        summarise(p)
