"""Copy the structure(s) with a given title from one structure file to another.

    & "$S\\run" scripts\\extract_entry.py results\\bq_prepped.maegz bq_QH2 results\\bq_QH2.mae
    $SCHRODINGER/run scripts/extract_entry.py results/bq_prepped.maegz bq_QH2 results/bq_QH2.mae

Used in Session 1, section C2, to take the prepared hydroquinone out of the LigPrep
output for the Epik runs; File > Export Structures in Maestro does the same.
"""
import sys

from schrodinger import structure


def main(src, title, dst):
    n = 0
    with structure.StructureWriter(dst) as writer:
        for st in structure.StructureReader(src):
            if st.title == title:
                writer.append(st)
                n += 1
    if n == 0:
        sys.exit(f"no structure titled {title!r} in {src}")
    print(f"wrote {n} structure(s) titled {title} to {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
