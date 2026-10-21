"""Summarise the states returned by Epik: one line per output structure with its
title, total charge, electron count and every Epik property stored on it.

Run with the Python that ships with the Schrödinger suite:

    & "$S\\run" scripts\\list_epik_states.py results\\bq_QH2_epik_wide.maegz
    $SCHRODINGER/run scripts/list_epik_states.py results/bq_QH2_epik_wide.maegz

Used in Session 1, section C, to fill in the worksheet: how many states each run
returned, which charges, and that the electron count never changes. Property names
differ between Epik releases, so the script prints every property whose name
contains "epik" instead of assuming specific names.
"""
import sys

from schrodinger import structure


def main(paths):
    for path in paths:
        print(f"== {path}")
        rows = []
        for st in structure.StructureReader(path):
            n_el = sum(atom.atomic_number for atom in st.atom) - st.formal_charge
            props = {k: v for k, v in st.property.items() if "epik" in k.lower()}
            rows.append((st.formal_charge, st.title, n_el, props))
        rows.sort(key=lambda r: -r[0])
        electron_counts = {r[2] for r in rows}
        for charge, title, n_el, props in rows:
            print(f"  charge {charge:+d}  electrons {n_el}  {title}")
            for k, v in sorted(props.items()):
                print(f"      {k} = {v}")
        print(f"  {len(rows)} structures; charges {sorted({r[0] for r in rows}, reverse=True)}; "
              f"electron count {'constant' if len(electron_counts) == 1 else 'CHANGES'} ({sorted(electron_counts)})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
