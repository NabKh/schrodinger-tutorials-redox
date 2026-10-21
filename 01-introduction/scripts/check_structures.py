"""List title, formula, total charge, electron count and suggested multiplicity
for every structure in a Maestro (.mae, .maegz) or SD file.

Run with the Python that ships with the Schrödinger suite:

    & "$S\\run" scripts\\check_structures.py results\\bq_prepped.maegz results\\bq_radicals.mae   (Windows)
    $SCHRODINGER/run scripts/check_structures.py results/bq_prepped.maegz results/bq_radicals.mae  (Linux)

Used in Session 1 after LigPrep (A4 and B3) to confirm that no state lost or gained
a proton. The electron count is the sum of the atomic numbers minus the total charge;
an odd count means an unpaired electron, so the lowest multiplicity is 2.
"""
import sys
from collections import Counter

from schrodinger import structure

HILL_FIRST = ("C", "H")


def formula(st):
    counts = Counter(atom.element for atom in st.atom)
    order = [e for e in HILL_FIRST if e in counts] + sorted(e for e in counts if e not in HILL_FIRST)
    return "".join(f"{e}{counts[e] if counts[e] > 1 else ''}" for e in order)


def main(paths):
    print(f"{'title':<24}{'formula':<12}{'charge':>7}{'electrons':>11}{'multiplicity':>14}")
    for path in paths:
        for st in structure.StructureReader(path):
            charge = st.formal_charge
            n_el = sum(atom.atomic_number for atom in st.atom) - charge
            mult = 2 if n_el % 2 else 1
            print(f"{st.title:<24}{formula(st):<12}{charge:>7}{n_el:>11}{mult:>14}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
