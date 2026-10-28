r"""Build every redox state of a molecule from its closed-shell parents and write one Jaguar input per state.

Run with the suite's Python (it needs the Schrodinger API and a license):
  & "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made
  & "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made --parents ..\01-introduction\results\bq_prepped.maegz
  & "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made --level gas --set dftname=PBE --set basis=6-31G**

Recipe columns (one row per state):
  job           name of the Jaguar job (and of the .in file)
  parent        closed-shell parent the state is made from; with --parents, the entry title in that file
  smiles        SMILES of the parent, used to build it in 3D when --parents is not given
  strip         hydrogens removed from the parent, separated by spaces:
                  O    the first H bonded to an O (in atom order), O:2 the second one; N likewise
                  17   atom 17 of the parent (the atom number shown in Maestro)
  charge        molchg of the state
  multiplicity  multip of the state

The atoms of a state are those of its parent minus the stripped hydrogens; the electrons are set
by the charge alone. Q*- shares the coordinates of Q; Q2- is made from QH2 minus both O-H
hydrogens (bq.csv), so it starts from the hydroquinone ring. The optimisation moves each state to
its own minimum. Every state with multiplicity > 1 gets iuhf=1 (unrestricted).
A SMILES carries no conformation (syn/anti, sulfonate orientation): look at states.maegz.
"""

import argparse
import csv
from pathlib import Path

from schrodinger import structure
from schrodinger.application.jaguar.input import JaguarInput

LEVELS = {
    # B3LYP-D3/def2-TZVPD in PBF water: the inputs in inputs/bq
    "production": dict(
        dftname="B3LYP-D3",
        basis="def2-TZVPD",
        isolv=2,
        solvent="water",
        nogas=2,
        igeopt=1,
        ifreq=1,
        irder=1,
        maxitg=200,
    ),
    # PBE/LACVP++** in PBF water: the inputs in inputs/live
    "live": dict(
        dftname="PBE",
        basis="LACVP++**",
        isolv=2,
        solvent="water",
        nogas=2,
        igeopt=1,
        ifreq=1,
        irder=1,
        maxitg=200,
    ),
    # B3LYP-D3/def2-TZVPD in the gas phase: the inputs in inputs/gas
    "gas": dict(dftname="B3LYP-D3", basis="def2-TZVPD", igeopt=1, ifreq=1, irder=1, maxitg=200),
}


def read_parents(rows, parents_file):
    if parents_file:
        parents = {}
        for st in structure.StructureReader(parents_file):
            if st.title in parents:
                raise SystemExit(f"{parents_file}: two entries titled {st.title}; keep one (LigPrep -s 1)")
            parents[st.title] = st
        return parents
    parents = {}
    for row in rows:
        if row["parent"] not in parents:
            st = structure.SmilesStructure(row["smiles"]).get3dStructure()
            st.title = row["parent"]
            parents[row["parent"]] = st
    return parents


def hydrogens_to_strip(st, strip):
    chosen = []
    for token in strip.split():
        if token.isdigit():
            index = int(token)
        else:
            element, _, nth = token.partition(":")
            candidates = [
                a.index for a in st.atom if a.element == "H" and any(b.element == element for b in a.bonded_atoms)
            ]
            free = [i for i in candidates if i not in chosen]
            if nth:
                index = candidates[int(nth) - 1]
            elif free:
                index = free[0]
            else:
                raise SystemExit(f"{st.title}: no H on {element} left for token {token!r}")
        if index in chosen:
            raise SystemExit(f"{st.title}: atom {index} listed twice in strip {strip!r}")
        if st.atom[index].element != "H":
            raise SystemExit(f"{st.title}: atom {index} is {st.atom[index].element}, not H")
        chosen.append(index)
    return chosen


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("recipe", help="CSV with job, parent, smiles, strip, charge, multiplicity")
    p.add_argument("--out", required=True, help="folder for the .in files")
    p.add_argument("--parents", help="structure file (.mae, .maegz, .sdf) with the parents, e.g. from LigPrep")
    p.add_argument("--level", choices=LEVELS, default="production")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="extra or changed &gen keyword")
    p.add_argument("--suffix", default="", help="appended to every job name, e.g. _pbe")
    args = p.parse_args()

    with open(args.recipe) as f:
        rows = list(csv.DictReader(f))
    parents = read_parents(rows, args.parents)
    genkeys = dict(LEVELS[args.level])
    for item in args.set:
        key, value = item.split("=", 1)
        genkeys[key] = int(value) if value.lstrip("-").isdigit() else value

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    writer = structure.StructureWriter(str(out / "states.maegz"))
    for row in rows:
        job = row["job"] + args.suffix
        charge, mult = int(row["charge"]), int(row["multiplicity"])
        st = parents[row["parent"]].copy()
        stripped = hydrogens_to_strip(st, row["strip"])
        st.deleteAtoms(stripped)
        st.title = job
        st.property["i_m_Spin_multiplicity"] = mult

        n_el = sum(a.atomic_number for a in st.atom) - charge
        if (n_el - (mult - 1)) % 2:
            raise SystemExit(f"{job}: {n_el} electrons cannot have multiplicity {mult}")

        jag = JaguarInput(structure=st, name=job)
        jag.setValues(genkeys)
        jag.setValues(dict(molchg=charge, multip=mult))  # after the structure, which sets them from formal charges
        if mult > 1:
            jag.setValues(dict(iuhf=1))
        jag.saveAs(str(out / f"{job}.in"))
        writer.append(st)
        removed = " ".join(str(i) for i in stripped) or "-"
        print(
            f"{job:16s} from {row['parent']:10s} H removed: {removed:8s} {st.atom_total:3d} atoms  N={n_el:4d}  molchg={charge:+d}  multip={mult}"
        )
    writer.close()
    print(f"wrote {len(rows)} inputs and states.maegz to {out}")


if __name__ == "__main__":
    main()
