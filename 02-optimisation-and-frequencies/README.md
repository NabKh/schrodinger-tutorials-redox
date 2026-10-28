# Session 2 · Geometry optimisation and harmonic frequencies in continuum solvent

*Jaguar input, submission and output, on 1,4-benzoquinone; what changes for AQDS, TEMPO and the indigo family*

Session 1 ended with a list of states, each with a charge and a multiplicity. Session 3 needs one Gibbs energy G per state, at a geometry that is a true minimum. This session produces and checks those numbers. You write Jaguar inputs, check them before they cost compute time, submit them from PowerShell or the VS Code terminal, and read the output line by line until you can rebuild G by hand. A gas-phase frequency calculation is then compared with the experimental IR spectrum, which is the only point in this course where a computed number meets a measured one directly.

The session is hands-on throughout: every step is done together, in pairs, on the files of this folder.

## Learning goals

1. Generate every redox state of a molecule from its closed-shell parents, with the right charge and multiplicity, and turn each into a Jaguar input, by script and in Maestro.
2. Justify a level of theory (functional, basis, solvation model) from cheaper levels and from the quantity that is needed, not from habit.
3. Explain every keyword of a Jaguar optimisation + frequency input and name what it controls physically.
4. Find a wrong charge or multiplicity in an input before submitting it, and explain why an electron count alone does not catch every error.
5. Submit, monitor and retrieve a Jaguar job from the command line.
6. Decide from the output whether a structure is a minimum: convergence criteria, 3N−6 frequencies, no imaginary mode, ⟨S²⟩ for radicals.
7. Rebuild G from E, ZPE and the thermal table; state the approximations behind it (quasi-harmonic, ideal gas at 1 atm, symmetry number) and correct to 1 mol/L.
8. Compare scaled harmonic frequencies with a gas-phase IR spectrum and judge what agreement means.

## Files

| file | used in |
|---|---|
| `worksheet.md` | predictions and results, filled in during the session |
| `inputs/states.csv` | S, A, B: charge and multiplicity of every job of the course |
| `inputs/recipes/` | S: for each family, which parent each state is made from, which H is removed, charge and multiplicity |
| `inputs/levels/` | L: benzoquinone in the gas phase at four more levels of theory (the level ladder) |
| `inputs/solvation/` | L: Q and Q²⁻ single points at one geometry with no solvent, PBF, SMD and C-PCM |
| `inputs/bq/` | A, C: benzoquinone states at the production level, B3LYP-D3/def2-TZVPD in PBF water; `_b3lyp` without D3 |
| `inputs/live/bq_Q_pbe.in`, `bq_QH2_pbe.in` | B: the jobs submitted during the session (PBE/LACVP++\*\*, PBF water) |
| `inputs/groups/` | A4: one input per group with `molchg=??` and `multip=??` |
| `inputs/broken/` | A3: three inputs with an error each |
| `inputs/gas/` | D: gas-phase Q and QH₂ for the IR comparison |
| `inputs/checks/` | D4: one-factor checks of the soft modes |
| `inputs/aqds/`, `inputs/tempo/`, `inputs/indigo/` | E and homework: the other redox families at the production level |
| `scripts/make_inputs.py` | S: parents → all states → one Jaguar input per state, plus `states.maegz` to open in Maestro |
| `scripts/check_inputs.py` | A3, A4: electron count, multiplicity parity, comparison with `states.csv` |
| `scripts/summarise_job.py` | C: the lines of a Jaguar output that decide whether a result is usable, and G rebuilt by hand |
| `scripts/ir_compare.py` | D: computed against experimental IR, with a scale factor; optional plot |
| `commands.ps1` (Windows), `commands.sh` (Linux) | S, L, B, C, D: every command of the session |

`make_inputs.py` uses the Schrödinger Python API and must be run with the suite's Python, `& "$S\run" scripts\make_inputs.py ...`. The other scripts need only Python 3 with `numpy` (and `matplotlib` for the plot); they run with the suite's Python, `& "$S\run" scripts\<name>.py ...`, or any Python with those packages. No output is in the repository. Every output named below is produced by running the corresponding input on the workstation: the production inputs of `inputs/bq/` into `results\bq\`, the others into the `results\` folder given in their step.

## How each step is written

Every hands-on step has the same four parts:

- **Input**: the file(s) it reads, with their path in this folder;
- **Command**: what you type, in PowerShell or the VS Code terminal (the same lines are in `commands.ps1`, under the section name of the step);
- **Expected**: what to check. Where theory fixes the answer (3N − 6 frequencies, 0 imaginary, ⟨S²⟩ = 0.75 for a doublet) it is given; numbers that only a run can give are left as ______, to be filled in from your own output;
- **Why**: what the step tests, and what you do if the result is not the expected one.

**Heavy for one molecule, light for all.** Optimisation + frequency jobs at the production level take hours, and longer for the larger molecules. They are run for benzoquinone only. Everything that costs seconds is done for all four families, so that each student has seen the states, inputs and outputs of the molecule of their project before starting it.

| step | benzoquinone | AQDS, TEMPO, indigo family |
|---|---|---|
| S · states → inputs (`make_inputs.py`) | in class, step S3 | in class, step S7 |
| S, A · check (`check_inputs.py`) | in class, step S4 | in class, step S7 |
| A · read the input | in class, step A1 | in class, step A4 (fill in one group input) |
| B · submit | live PBE job, ladder and solvation jobs | after the session, as the project |
| C · read an output (`summarise_job.py`) | `bq_Q.out`, `bq_QHrad.out`, `bq_QH2*.out` | after the session, on the group's own output (E) |
| D · IR | step D, after the gas-phase job | not part of the session: no gas-phase spectrum is used for them |

## Before the session

1. On the Windows workstation, in PowerShell: `$S = "C:\Program Files\Schrodinger2026-2"` and `$env:SCHRODINGER = $S` (without the second line `jsc hosts list` stops with "$SCHRODINGER must be defined"). Then `& "$S\jsc" hosts list` shows the compute hosts besides `localhost` (Session 1, B2). Write one down: it replaces `<host>` in every command below.
2. `& "$S\jsc" cert get <server>:<port>` has been run once (Session 1, Before the session, item 4).
3. Either PowerShell or the VS Code terminal opens in `C:\schrodinger-tutorials-redox\02-optimisation-and-frequencies`. In VS Code: File > Open Folder > the repository, then Terminal > New Terminal (PowerShell is the default shell on Windows).
4. `& "$S\run" scripts\check_inputs.py inputs\bq` prints one `ok` line per input.
5. Session 1's LigPrep output `..\01-introduction\results\bq_prepped.maegz` exists (Session 1, B3); if not, S3 builds the parents from SMILES.

## Time plan

| time | part | what you do |
|---|---|---|
| 0:00 | 0 · Goal | from states to G; what makes a G usable |
| 0:05 | S · States → inputs | one molecule, all its states, one input each: by script, then the same in Maestro |
| 0:30 | L · Level of theory | why B3LYP-D3/def2-TZVPD in PBF water: the ladder and the solvation comparison |
| 0:45 | A · The input | read `bq_Q.in` keyword by keyword; fix three broken inputs; fill in your group's input |
| 1:00 | B · Submit | submit the live job and one ladder or solvation job (benzoquinone only); monitor them |
| 1:10 | C · The output | read the benzoquinone production output; rebuild G |
| 1:40 | D · IR spectrum | scale, compare with the NIST gas-phase spectrum, judge the agreement |
| 1:55 | E · Other molecules | what changes for AQDS, TEMPO and indigo (read at home if time is short) |

## 0 · Goal (5 min)

For each state $i$ of Session 1 this session gives

$$G_i = E_\mathrm{el} + E_\mathrm{ZPE} + G_\mathrm{thermal}(298.15\ \mathrm{K}, 1\ \mathrm{atm}) + 1.89\ \mathrm{kcal/mol}$$

with $E_\mathrm{el}$ the electronic energy in PBF water at the optimised geometry, and $1.89 = RT\ln(24.46)$ kcal/mol the change of standard state from 1 atm to 1 mol/L. A G is usable only if

- the charge and multiplicity are those of the intended state (A),
- the geometry optimisation converged (C1),
- the structure is a minimum: 3N−6 real frequencies (C2),
- for a radical, the wavefunction is a doublet and not a mixture: ⟨S²⟩ close to 0.75 (C3),
- the lowest-G conformer was found, or the conformers were weighted (C5).

Two energies in Session 3 enter a pKa or a potential as differences. An error of 1.36 kcal/mol in one G moves a pKa by one unit; 23.06 kcal/mol is 1 V per electron.

## S · From one molecule to all its states, and to one Jaguar input per state (25 min)

Session 1 gave the states of each family as a list. Here we make them, for benzoquinone, from start to finish, with a script; then the same in Maestro. The other families follow the same steps (S6).

**S1 · The proton–electron grid.** Every state of benzoquinone is Q plus $n_\mathrm{H}$ protons and $n_e$ electrons. With the rules of Session 1, charge $= n_\mathrm{H} - n_e$ and multiplicity 2 if the electron count is odd:

| state | job | $n_\mathrm{H}$ | $n_e$ | formula | `molchg` | electrons | `multip` | made from | H removed |
|---|---|---|---|---|---|---|---|---|---|
| Q | `bq_Q` | 0 | 0 | C₆H₄O₂ | 0 | 56 | 1 | Q | none |
| Q•⁻ | `bq_Qradm` | 0 | 1 | C₆H₄O₂ | −1 | 57 | 2 | Q | none |
| QH• | `bq_QHrad` | 1 | 1 | C₆H₅O₂ | 0 | 57 | 2 | QH₂ | one O–H |
| QH⁻ | `bq_QHm` | 1 | 2 | C₆H₅O₂ | −1 | 58 | 1 | QH₂ | one O–H |
| QH₂ | `bq_QH2` | 2 | 2 | C₆H₆O₂ | 0 | 58 | 1 | QH₂ | none |
| Q²⁻ | `bq_Q2m` | 0 | 2 | C₆H₄O₂ | −2 | 58 | 1 | QH₂ | both O–H |

Two kinds of operation make every state from only two closed-shell **parents**, Q and QH₂:

- *removing a proton*: delete an H bonded to O (the atoms change);
- *adding an electron*: change `molchg` only (the atoms stay the same; the electrons are not in the structure file, they are set by the charge).

Q, Q•⁻ and Q²⁻ have the same atoms. Q²⁻ is nevertheless made from QH₂: Q²⁻ is the hydroquinone without its two protons, so its C–O bonds are expected to be phenolate single bonds rather than the C=O of Q, and the hydroquinone ring is the closer start. Check it after the run: r(C–O) in `bq_Q2m.out` against `bq_Q.out` and `bq_QH2.out` (final geometries). Either start should end in the same minimum; a start closer to it costs fewer geometry steps and is less likely to stop in a different one. The radicals are never passed through LigPrep, which adds hydrogens to them (Session 1, A5).

The whole grid is written in one file per family, `inputs/recipes/bq.csv`:

```
job,parent,smiles,strip,charge,multiplicity
bq_Q,bq_Q,O=C1C=CC(=O)C=C1,,0,1
bq_Qradm,bq_Q,O=C1C=CC(=O)C=C1,,-1,2
bq_QH2,bq_QH2,Oc1ccc(O)cc1,,0,1
bq_QHrad,bq_QH2,Oc1ccc(O)cc1,O,0,2
bq_QHm,bq_QH2,Oc1ccc(O)cc1,O,-1,1
bq_Q2m,bq_QH2,Oc1ccc(O)cc1,O O,-2,1
```

`strip` lists the hydrogens to delete: `O` is the first H bonded to an O, `O:2` the second, `O O` both; an integer is an atom number as shown in Maestro.

**S2 · The parents in 3D.** Two routes, both fine for a molecule this small:

1. *From Session 1*: the LigPrep output `..\01-introduction\results\bq_prepped.maegz` (Session 1, B3: `-i 0 -nt -s 1`, ionisation not changed, no tautomers, one stereoisomer). Its entries are titled `bq_Q`, `bq_QH2`, … from the second column of `bq_closed_shell.smi`; the script picks the parents by title.
2. *From the SMILES in the recipe*: the script builds each parent in 3D itself (`SmilesStructure(...).get3dStructure()` of the Schrödinger API).

**S3 · All states and all inputs, by script** (commands S3):

```powershell
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made
#  or, from the Session 1 LigPrep output:
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made --parents ..\01-introduction\results\bq_prepped.maegz
```

For each row the script copies the parent, deletes the listed hydrogens, checks that the electron count fits the multiplicity, writes `results\made\<job>.in` with the `&gen` keywords of the production level (section A1), and appends the structure to `results\made\states.maegz`. `molchg` and `multip` are set from the recipe *after* the structure: the Schrödinger API otherwise takes the charge from the formal charges of the atoms, and a deleted H leaves the O without a formal charge, so QH⁻ would silently become neutral (`setStructure`, `schrodinger/application/jaguar/input.py`). The same keywords at another level: `--level live` (PBE/LACVP++\*\*) or `--level gas`, and any single keyword with `--set`, for example `--set basis=6-31G**`.

*Expected:* one line per state, for example `bq_Q2m  from bq_QH2  H removed: 9 12  12 atoms  N=  58  molchg=-2  multip=1` (the atom numbers depend on how the parent was built), and `wrote 6 inputs`. Copy your lines into the worksheet (S1).

**S4 · Check before submitting.**

```powershell
& "$S\run" scripts\check_inputs.py results\made          # parity and states.csv: six ok lines
code --diff results\made\bq_Q2m.in inputs\bq\bq_Q2m.in    # same &gen, different starting coordinates
```

Open `results\made\states.maegz` in Maestro (File > Import Structures) and look at each state: is the right H gone, is the formula right? The given inputs in `inputs/bq/` were made the same way; they differ only in the starting coordinates, and the optimisation should take both to the same minimum.

**S5 · The same in Maestro.** For one state, then compare with the script:

1. File > Import Structures: `bq_prepped.maegz` from Session 1 (or draw the parent).
2. Derived state: copy the parent entry in the Project Table (UNVERIFIED menu wording in 2026-2: right-click > Duplicate), select the O–H hydrogen in the Workspace and delete it, rename the entry (`bq_QHm`). Removing a proton leaves an O with one bond and no formal charge: either set its formal charge to −1 or set the charge in step 3. Adding an electron needs no change to the structure at all.
3. Jaguar > Optimization (task search, as in Session 1, A6). Tabs:
   - *Molecule*: charge and spin multiplicity of the entry (`molchg`, `multip`).
   - *Theory*: B3LYP-D3, basis def2-TZVPD (`dftname`, `basis`).
   - *SCF*: defaults.
   - *Optimization*: maximum steps 200 (`maxitg`).
   - *Properties*: vibrational frequencies with IR intensities (`ifreq`, `irder`).
   - *Solvation*: PBF, water (`isolv=2`, `solvent`).
4. The gear menu > Write: writes the `.in` file without running it. Compare it with `results\made\bq_QHm.in` and run `check_inputs.py` on it.

The GUI is good for one state and for looking; the script is reproducible, and is what you use for 30 states. Either way, `check_inputs.py` is run before anything is submitted.

**S6 · The other families.** Same steps, other recipes in `inputs/recipes/`:

| family | parents (closed shell) | derived states | watch |
|---|---|---|---|
| AQDS, `aqds.csv` | `aq_Q` (−2), `aq_QH2` (−2) | Q•⁻ from Q; QH•, QH⁻ at O9 or O10, and Q²⁻, from QH₂ | the two SO₃⁻ give −2 to every state. `O:1` and `O:2` are the first and second O–H in atom order: check in `states.maegz` which one is at C9 and which at C10, and rename if needed. The 2,7-substitution makes the two sites different, so both are computed. |
| TEMPO, `tempo.csv` | `tp_Tp` (oxoammonium, +1), `tp_TH` (hydroxylamine), `tp_TH2p` (+1) | T• and T⁻ from TH, by removing the O–H | T• is a doublet with 87 electrons; the oxoammonium N=O⁺ is a closed shell. |
| indigo, `indigo.csv` | `di_D`, `di_I`, `di_L` (0, 2 and 4 N–H/O–H hydrogens) | D•⁻, D²⁻ from D; DH•, I⁻ (N–H removed) and I•⁻ from I; LH₃•, L⁻, L²⁻ (O–H removed) from L | which H is removed is a choice of tautomer: L⁻ with O⁻ and with N⁻ are different states with different G. The recipes take O–H for leucoindigo and N–H for indigo; the other choice is a homework question. |

**S7 · The light steps for every family** (commands S7). No job is submitted; each command takes seconds.

*Input:* `inputs/recipes/aqds.csv`, `tempo.csv`, `indigo.csv`; the given inputs in `inputs/aqds/`, `inputs/tempo/`, `inputs/indigo/`.

*Command:*

```powershell
foreach ($f in "aqds", "tempo", "indigo") {
    & "$S\run" scripts\make_inputs.py inputs\recipes\$f.csv --out results\made_$f
    & "$S\run" scripts\check_inputs.py results\made_$f inputs\$f
}
```

*Expected* for the given inputs (output of `check_inputs.py` on `inputs\aqds`, `inputs\tempo` and `inputs\indigo`; the `results\made_*` lines should give the same atoms, N, `molchg` and `multip`, and are filled in after the workstation run):

```
aq_Q               ok      30 atoms  N= 188  molchg=-2  multip=1  closed shell
aq_Q2m             ok      30 atoms  N= 190  molchg=-4  multip=1  closed shell
aq_QH2             ok      32 atoms  N= 190  molchg=-2  multip=1  closed shell
aq_QHm10           ok      31 atoms  N= 190  molchg=-3  multip=1  closed shell
aq_QHm9            ok      31 atoms  N= 190  molchg=-3  multip=1  closed shell
aq_QHrad10         ok      31 atoms  N= 189  molchg=-2  multip=2  open shell, unrestricted (iuhf default)
aq_QHrad9          ok      31 atoms  N= 189  molchg=-2  multip=2  open shell, unrestricted (iuhf default)
aq_Qradm           ok      30 atoms  N= 189  molchg=-3  multip=2  open shell, unrestricted (iuhf default)
tp_T               ok      29 atoms  N=  87  molchg=+0  multip=2  open shell, unrestricted (iuhf default)
tp_TH              ok      30 atoms  N=  88  molchg=+0  multip=1  closed shell
tp_TH2p            ok      31 atoms  N=  88  molchg=+1  multip=1  closed shell
tp_Tm              ok      29 atoms  N=  88  molchg=-1  multip=1  closed shell
tp_Tp              ok      29 atoms  N=  86  molchg=+1  multip=1  closed shell
di_D               ok      28 atoms  N= 134  molchg=+0  multip=1  closed shell
di_D2m             ok      28 atoms  N= 136  molchg=-2  multip=1  closed shell
di_DHrad           ok      29 atoms  N= 135  molchg=+0  multip=2  open shell, unrestricted (iuhf default)
di_Dradm           ok      28 atoms  N= 135  molchg=-1  multip=2  open shell, unrestricted (iuhf default)
di_I               ok      30 atoms  N= 136  molchg=+0  multip=1  closed shell
di_Im              ok      29 atoms  N= 136  molchg=-1  multip=1  closed shell
di_Iradm           ok      30 atoms  N= 137  molchg=-1  multip=2  open shell, unrestricted (iuhf default)
di_L               ok      32 atoms  N= 138  molchg=+0  multip=1  closed shell
di_L2m             ok      30 atoms  N= 138  molchg=-2  multip=1  closed shell
di_LH3rad          ok      31 atoms  N= 137  molchg=+0  multip=2  open shell, unrestricted (iuhf default)
di_Lm              ok      31 atoms  N= 138  molchg=-1  multip=1  closed shell
```

*Why:* read the table as the S1 grid of each family. Every proton removed lowers the atom count by one and the charge by one at the same N; every electron added raises N by one at the same atoms; odd N is a doublet. Two cases to look at in Maestro (`results\made_*\states.maegz`): the AQDS states at O9 and O10 (S6), and the four AQDS states with charge −3 and −4, which are the hardest to describe (E).

## L · Choosing the level of theory, from cheap to expensive (15 min)

The production level of this course is B3LYP-D3/def2-TZVPD in PBF water. It is not chosen because it is the most expensive level available, and it should not be accepted without a test. A level of theory is chosen for one quantity and one accuracy.

**L0 · The quantity and the target.** Session 3 uses differences of G between states: a pKa from a deprotonation, a potential from a reduction. The targets are 1.36 kcal/mol for one pKa unit and 23.06 kcal/mol per electron for 1 V, so 0.1 V for a 2e⁻ step is 4.6 kcal/mol. An approximation matters only if it changes such a *difference* by a comparable amount. That it changes the absolute energy is not enough.

**L1 · Which effect matters for a difference?** From the benzoquinone production outputs (`results\bq\`, B3LYP-D3/def2-TZVPD, PBF water), once they have run:

| effect | what to read | for the target |
|---|---|---|
| D3 dispersion | Gtot with and without D3: `bq_Q.out` against `bq_Q_b3lyp.out`, `bq_QH2.out` against `bq_QH2_b3lyp.out`; shifts ______ and ______ kcal/mol | change of the Q → QH₂ step: ______ kcal/mol = ______ V (2e⁻) |
| solvation | line `Solvation energy` in each output, Q, QH₂, QH•, QH⁻, Q²⁻: ______ kcal/mol | an error of 5 % in that of Q²⁻: ______ kcal/mol = ______ V (2e⁻) |

Prediction first: which of the two rows changes a *difference* more? The answer decides where the effort below goes, into the functional or into the solvation model.

**L2 · Functional: the ladder** (Jacob's ladder: GGA → hybrid → meta-GGA hybrid and range-separated hybrid). Q in the gas phase, optimisation and frequencies, each input changing one thing:

| rung | input | functional (type, from Jaguar's `levels_of_theory.csv`) | basis | r(C=O) (Å) | ν(C=O), harmonic (cm⁻¹) | lowest B3u (cm⁻¹) | wall time |
|---|---|---|---|---|---|---|---|
| 1 | `levels/bq_Q_pbe_631g.in` | PBE (GGA) | 6-31G\*\* | | | | |
| 2 | `levels/bq_Q_b3lyp_631g.in` | B3LYP (hybrid GGA) | 6-31G\*\* | | | | |
| 3 | `checks/bq_Q_gas_tzvp.in` | B3LYP-D3 | def2-TZVP | | | | |
| 4 | `gas/bq_Q_gas.in` | B3LYP-D3 | def2-TZVPD | | | | |
| 5 | `levels/bq_Q_m062x.in` | M06-2X-D3 (hybrid meta-GGA) | def2-TZVPD | | | | |
| 6 | `levels/bq_Q_wb97xd.in` | ωB97X-D (range-separated hybrid with dispersion) | def2-TZVPD | | | | |
| exp. | | | | | 1678 (gas, fundamental) | 109 | |

The table is filled in from the runs of these inputs (B5). How to read it:

- Steps 1 → 2 change the exchange (no exact exchange → part exact exchange). UNVERIFIED (general knowledge, not checked here): GGAs give too long bonds and too low frequencies, because of the self-interaction (delocalisation) error; hybrids reduce it.
- Steps 2 → 3 → 4 change the basis at a nearly fixed functional; 3 → 4 adds only the diffuse functions (L3).
- Steps 4 → 5 → 6 change the functional at a fixed basis. If 4, 5 and 6 agree within the target, the choice among them does not matter for this quantity. If they do not agree, the spread is part of the uncertainty, and Session 3 (comparison with measured E° and pKa) decides.
- In Jaguar, B3LYP, B3LYP-D3, M06-2X and ωB97X-D carry the flag `is_recommended=1`; PBE does not (`levels_of_theory.csv`). This is the vendor's flag, not evidence for our quantity.

**L3 · Basis set.** 6-31G\*\* (double-ζ) → def2-TZVP (triple-ζ, polarisation) → def2-TZVPD (the same plus diffuse functions). In Jaguar's `basis_sets.csv`, def2-TZVPD and LACVP++\*\* are the diffuse ones, 6-31G\*\* and def2-TZVP are not. The outer electrons of an anion are weakly bound and spread far from the nuclei, and a basis without diffuse functions confines them artificially. This matters for QH⁻ and Q²⁻ and for every AQDS state, all of them anions. The price is near-linear dependence of the basis. Read the smallest eigenvalue of the overlap matrix S in every output with a diffuse basis (`summarise_job.py` prints it; C, D4, E): a very small or negative value means the basis must be checked before production.

**L4 · Solvation model.** Jaguar offers, among others (`isolv`, `jaguar_keywords.xml`): 2 PBF (Poisson–Boltzmann, Jaguar's own model, in which all production geometries of this course were optimised), 7 PCM (C-PCM by default, `pcm_model`), and 8 SMD (Jaguar can also optimise in SMD: keyword `pbf_after_smd`; UNVERIFIED, from the SMD paper's title and not read here: parametrised on experimental solvation free energies, with non-electrostatic terms). The inputs in `inputs/solvation/` are single points of Q and Q²⁻ at their PBF geometries with no solvent, PBF, SMD and C-PCM:

| model | `isolv` | E(Q) (Eh) | E(Q²⁻) (Eh) | ΔG_solv(Q) | ΔG_solv(Q²⁻) | ΔE(Q → Q²⁻) (kcal/mol) |
|---|---|---|---|---|---|---|
| none (gas) | – | | | 0 | 0 | |
| PBF | 2 | | | | | |
| SMD | 8 | | | | | |
| C-PCM | 7 | | | | | |

The PBF single points must reproduce the final energies of `bq_Q.out` and `bq_Q2m.out`, which checks the inputs. ΔG_solv = E(model) − E(gas) at the same geometry. The spread of the last column across the three models, divided by 46.1 kcal/mol (2 × 23.06), is a first estimate of how uncertain a 2e⁻ potential is from the solvation model alone. Predict which state carries most of the spread, neutral Q or Q²⁻, and check it in the table.

**L5 · What the literature says** (abstracts read; details in the papers):

- Elhajj et al., *J. Chem. Theory Comput.* (2024), doi:10.1021/acs.jctc.4c00602. 345 quinones in DMF, one-electron potentials, four continuum models (IEF-PCM, C-PCM, COSMO, SM12). The correlation is high (r ≈ 0.95–0.96), but with systematic offsets of 200–400 mV, and larger errors for multiply charged anions. Optimising in the reaction field reduced the random error. The lessons: calibrate against experiment, and optimise in solvent.
- Zhang et al., *Sci. Rep.* (2020), doi:10.1038/s41598-020-79153-w, and *Batteries* 7, 71 (2021), doi:10.3390/batteries7040071. Geometries from a cheap level plus DFT single points with implicit solvent are about as accurate for quinone redox potentials as full DFT. The lesson: the expensive level is needed for the energy, not necessarily for the geometry.
- Huynh … Hammes-Schiffer, *J. Am. Chem. Soc.* (2016), doi:10.1021/jacs.6b05797: 1e⁻ and 2e⁻/2H⁺ potentials of 134 quinones and the scaling relations between them.
- Er et al., *Chem. Sci.* (2015), doi:10.1039/c4sc03030c: high-throughput computational screening of quinones for flow batteries.
- Methods: Grimme et al. (D3), doi:10.1063/1.3382344; Weigend and Ahlrichs (def2), doi:10.1039/b508541a; Rappoport and Furche (diffuse def2-D), doi:10.1063/1.3484283; Tannor et al., doi:10.1021/ja00105a030, and Marten et al., doi:10.1021/jp953087x (PBF); Marenich, Cramer and Truhlar (SMD), doi:10.1021/jp810292n.

**L6 · The procedure, for any new molecule.**

1. Name the quantity (ΔG of which step) and the accuracy needed (L0).
2. Screen at a cheap level: GGA or hybrid with a double-ζ basis, to find conformers, tautomers and the states that matter.
3. Converge the level on one molecule for which experiment exists, here benzoquinone (IR, D). Go up the ladder one factor at a time, and stop when the next rung changes the quantity by less than the target.
4. Compute the solvation term with at least two models. For ions, the spread is usually the largest uncertainty.
5. Validate the whole protocol against measured E° and pKa (Session 3). A systematic offset can be calibrated; a random error cannot.
6. Count the cost. Read the wall time of the benzoquinone production jobs (`summarise_job.py`), and multiply by the number of states and conformers, and by the cost of the larger molecules, before choosing a higher rung.

For this course that procedure gives B3LYP-D3/def2-TZVPD in PBF water. It is a hybrid functional (no GGA self-interaction error at this level of concern), with dispersion that costs nothing (its size for benzoquinone is to be measured in L1), a diffuse basis because most states are anions, and the solvation model in which Jaguar optimises routinely. Its weak point, solvation of the multiply charged ions, is to be measured in L4 rather than assumed away.

## A · The input (15 min)

**A1 · Read `inputs/bq/bq_Q.in` together.** Open it in VS Code or Notepad. A Jaguar input has a `&gen` section (keywords) and a `&zmat` section (geometry, Å).

| keyword | value | what it does | in VASP terms |
|---|---|---|---|
| `dftname` | `B3LYP-D3` | exchange–correlation functional with Grimme's D3 dispersion correction | `LHFCALC = .TRUE.`, `GGA = B3` with `AEXX`, `AGGAX`, `AGGAC`, `ALDAC`; `IVDW = 11/12` for D3 |
| `basis` | `def2-TZVPD` | Gaussian basis set: triple-ζ, polarisation, diffuse functions for anions | replaces `ENCUT` and the PAW potentials; completeness is controlled by the basis, not a cutoff |
| `isolv=2`, `solvent=water` | | Poisson–Boltzmann (PBF) continuum water, self-consistent with the density | VASPsol |
| `nogas=2` | | no preliminary gas-phase optimisation: the input geometry is taken as the starting point of the optimisation in solvent | |
| `igeopt=1` | | geometry optimisation to a minimum | `IBRION = 1/2`, `NSW` |
| `maxitg=200` | | maximum number of geometry steps (default 100) | `NSW` |
| `ifreq=1` | | analytic second derivatives (Hessian) at the final geometry: frequencies, ZPE, thermochemistry | `IBRION = 5–8` (finite differences or DFPT) |
| `irder=1` | | IR intensities | `LEPSILON` / Born charges |
| `molchg` | `0` | total charge | `NELECT` (but no compensating background: a molecule needs none) |
| `multip` | `1` | spin multiplicity 2S+1 | `ISPIN = 2`, `NUPDOWN` |

Not in the input, but set by default (Jaguar 13.2, `jaguar_keywords.xml`): `iuhf=2`, spin-unrestricted when `multip` > 1 and restricted otherwise; pseudospectral integrals (`nops=0`); and in solvent, convergence criteria scaled relative to the gas phase (the factor is printed in the output, C1). There are no k-points: a molecule is not periodic, and there are no periodic images to correct for when it is charged.

**A2 · Why these choices.** The argument is in section L; here, connect each keyword to it. Diffuse functions are for the anions QH⁻ and Q²⁻, whose outer electrons are weakly bound (L3). D3 costs nothing; how much it changes a step between states, and the lowest frequency of QH₂, is to be measured in L1 (`bq_QH2.out` against `bq_QH2_b3lyp.out`). The optimisation is in water rather than in the gas phase because the anions change geometry in solvent, and the course uses one geometry per state (L4, L5). PBE/LACVP++\*\* in `inputs/live/` is a cheaper level for the live job only; its numbers are not used in Session 3.

**A3 · Three broken inputs.** Predict the problem of each file in `inputs/broken/` from the `&gen` section alone, write it in the worksheet, then run

```powershell
& "$S\run" scripts\check_inputs.py inputs\broken
```

*Expected:* three `FAIL` lines. `bq_Qradm` (57 electrons as a singlet) fails the parity test. `bq_QHm` (`molchg=1` instead of −1) and `bq_Q2m` (`molchg=0` instead of −2) have an even number of electrons and pass it: only the comparison with the intended state in `states.csv` catches them. Jaguar would run all three without complaint. The lesson: the electron count catches the wrong spin, not the wrong charge.

**A4 · Your group's input.** Each group takes one file from `inputs/groups/`, writes `molchg` and `multip` in place of `??`, and checks it:

| group | file | state |
|---|---|---|
| 1 | `tp_T_pbe.in` | TEMPO, the nitroxide radical |
| 2 | `aq_Q_pbe.in` | AQDS, the oxidised quinone with two sulfonates |
| 3 | `di_I_pbe.in` | indigo |
| 4 | `di_L_pbe.in` | leucoindigo |

```powershell
& "$S\run" scripts\check_inputs.py inputs\groups
```

*Expected:* `ok` for every group. Group 2: two sulfonate groups SO₃⁻ give −2; group 1: 87 electrons, so a doublet.

## B · Submit (10 min)

See `commands.ps1`, sections B1 to B4; the Linux equivalents are in `commands.sh`.

**B1 · Host.** `& "$S\jsc" hosts list`. Use a compute host, not `localhost`. The jobs are run by the job servers on rs4, rs5 and rs6 (`rs4.differ.nl:8030` etc., `& "$S\jsc" server-info rs4.differ.nl:8030`). A job that fails at once with `srun: executable file not found` hit a bad node: submit it again.

**B2 · Live job.** Each pair submits one of the two live inputs, so that both are running:

*Input:* `inputs/live/bq_Q_pbe.in` or `bq_QH2_pbe.in` (PBE/LACVP++\*\*, PBF water; checked in A3 like the others).

*Command:* the input is copied into `results\live` first and submitted from there, so that the output files land in `results\live` and not among the inputs:

```powershell
New-Item -ItemType Directory -Force results\live | Out-Null
Copy-Item inputs\live\*.in results\live\
Push-Location results\live
& "$S\jaguar" run bq_Q_pbe.in -HOST <host> -PARALLEL 4
Pop-Location
```

*Expected:* a `JobId:` line; the command returns at once. When the job ends, `bq_Q_pbe.out`, `.log` and `.mae` come back to `results\live`. Do not submit the same file twice from the same folder: the second job overwrites the first one's output.

**B3 · Monitor.**

```powershell
& "$S\jsc" list
& "$S\jsc" tail-file --name bq_Q_pbe.log <jobid>
```

*Expected:* the job in `jsc list`, with its status (UNVERIFIED wording in 2026-2: running, then completed). The `.log` shows the SCF and geometry iterations as they happen; the `.out` is complete only at the end. A job that ends with no `.out`: read the `.log` and submit again (B1).

**B4 · The other families: not submitted in the session.** A group molecule is larger than benzoquinone, and a production job takes many times longer; the PBE versions in `inputs/groups/` are cheaper. Your group's state is submitted after the session, as the start of the project, with the same three lines as B2 (commands B4).

**B5 · One ladder or solvation job per pair** (commands B5). The instructor assigns them: the two cheap rungs `inputs/levels/bq_Q_pbe_631g.in` and `bq_Q_b3lyp_631g.in`, and the eight single points in `inputs/solvation/`. The M06-2X and ωB97X-D rungs at def2-TZVPD are run by the instructor before the session. The results go into the L tables of the worksheet at the start of Session 3.

## C · The output (30 min)

Read the production output `results\bq\bq_Q.out` (the workstation run of `inputs\bq\bq_Q.in`; B3LYP-D3/def2-TZVPD, PBF water). First the summary:

```powershell
& "$S\run" scripts\summarise_job.py results\bq\bq_Q.out
```

*Expected:* the lines below. What the input or theory fixes is given; fill in the ______ from your output (worksheet, C).

```
  job                              bq_Q
  stoichiometry                    C6H4O2
  level                            ______  (B3LYP-D3, as in the input)
  basis                            ______  (def2-TZVPD)
  solvent                          ______  (water)
  charge / multiplicity            0 / 1
  electrons                        56
  <S**2> (ideal S(S+1))            closed shell
  point group (used)               ______  (predict it from the structure)
  smallest eigenvalue of S         ______
  geometry steps                   ______
  optimisation converged           yes
  final energy E (Eh)              ______
  vibrations (expected 3N-6)       30 (30)
  imaginary frequencies            0
  lowest three (cm-1)              ______
  quasi-harmonic floor             ______
  rotational symmetry number       ______  (from the point group)
  T, P                             ______  (298.15 K, 1 atm)
  ZPE (kcal/mol)                   ______
  G_thermal from table (kcal/mol)  ______
  Gtot printed (Eh)                ______
  wall time (h)                    ______
  G = E + (ZPE + G_table)/627.5095 ______ Eh (differs from printed by ______ kcal/mol)
```

Then find each line of the summary in the `.out` yourself (search in VS Code with Ctrl+F): C1 to C5 go through them in order. The script is a shortcut for reading, not a replacement: you must be able to find every number in the output.

**C1 · Did the optimisation converge?** Search `Geometry optimization complete`. Just above it, the last step lists five criteria: energy change, gradient maximum, gradient rms, displacement maximum and displacement rms.

Each value is compared with the threshold in brackets (hartree, hartree/bohr, bohr). A criterion that is met is marked. In solvent Jaguar scales the gas-phase thresholds: search `Scaling standard convergence criteria` and write the factor in the worksheet. Convert the gradient-maximum threshold to eV/Å (1 Eh/bohr = 51.42 eV/Å) and compare it with a typical VASP `EDIFFG = −0.02`.

*Expected:* all five criteria met. Geometry steps (count the `SCFE:` lines): ______.

**C2 · Is it a minimum?** Search `Number of imaginary frequencies`.

*Expected:* 30 frequencies for 12 atoms (3N − 6), 0 imaginary. The lowest: ______ cm⁻¹, symmetry ______. Which motion is it? A saddle point found by an optimisation means the symmetry or the starting structure was wrong; displace along the imaginary mode and reoptimise.

**C3 · Radicals.** In a radical output (`bq_QHrad.out`), search `<S**2>`. A pure doublet has S(S+1) = 0.75.

*Expected:* close to 0.75: ______. As a rule of thumb, a value well above 0.75 (more than about 10 %) means spin contamination: the energy is no longer that of a doublet. The thermal table has an `elec.` row with S = R ln 2 = 1.377 cal/(mol K) for a doublet.

**C4 · Rebuild G by hand.** From the end of `bq_Q.out`:

| line | value |
|---|---|
| final `SCFE: Solution phase energy` | Eh |
| `The zero point energy (ZPE)` | kcal/mol |
| `total` row, G column (without ZPE) | kcal/mol |
| `Total Gibbs free energy, Gtot` | Eh |

Compute $E + (\mathrm{ZPE} + G_\mathrm{table})/627.5095$ and compare with Gtot (the last line of `summarise_job.py` does the same).

*Expected:* the same value, to within the rounding of the printed numbers. Gtot already contains the ZPE; it is at 1 atm, so +1.89 kcal/mol is still to be added for 1 mol/L.

Then search `Quasi-Harmonic`, above the vibrational temperatures. If it is there, every mode below a minimum frequency (printed on the next lines: ______ cm⁻¹) is treated as if it were at that frequency when the vibrational entropy is computed. Low modes give the largest entropy and are the least harmonic; a floor avoids an entropy that grows without bound as a frequency goes to zero. Compare the floor with the lowest frequency of C2: does it change anything for benzoquinone? It will matter for a molecule with soft modes, for example freely rotating groups such as the AQDS sulfonates (E1). Finally `rotational symmetry number` (______; D2h has σ = 4): σ enters the rotational entropy as −R ln σ. Do not also count symmetry-equivalent structures by hand.

**C5 · Two conformers of QH₂.** `bq_QH2.out` (trans O–H, C2h) and `bq_QH2cis.out` (cis, C2v):

*Expected:* Gtot ______ and ______ Eh, ΔG = ______ kcal/mol. With $p_i \propto e^{-G_i/RT}$ (RT = 0.593 kcal/mol at 298.15 K): ______ % trans, ______ % cis. Is this difference larger than the error of the method? Which G goes into Session 3?

**C6 · The live job.** When `bq_Q_pbe.out` is back, run `summarise_job.py` on it and compare with `bq_Q.out`: geometry steps, lowest frequency, wall time, smallest eigenvalue of the overlap matrix S.

*Expected:* fill in the C6 table of the worksheet from the two summaries.

## D · IR spectrum (15 min)

Harmonic frequencies are the curvature of the potential at the minimum; measured bands are anharmonic fundamentals and lie a few per cent lower. A scale factor fitted per method and basis absorbs most of this, on average.

**D1 · Experimental spectrum.** Download the NIST gas-phase IR spectrum of 1,4-benzoquinone (commands D1). It is NIST Standard Reference Data: use it in class, do not redistribute it.

**D2 · Compare.**

```powershell
& "$S\run" scripts\ir_compare.py results\bq\bq_Q.out --scale 0.9626 --exp results\bq_Q_nist.jdx --plot results\bq_Q_ir.pdf
```

0.9626 is the NIST CCCBDB factor for B3LYP/def2-TZVPP, the closest available to def2-TZVPD; for PBE use 0.9879 (PBEPBE/def2-TZVPP).

*Expected:* one row per strong experimental band; fill in the computed columns from the script's output (worksheet, D):

| experiment (cm⁻¹) | rel. | calc., scaled | mode | difference |
|---|---|---|---|---|
| 1678 | | | C=O stretch | |
| 1302 | | | | |
| 1070 | | | | |
| 882 | | | C–H out of plane | |

**D3 · Judge the agreement.** Two effects are mixed here: `bq_Q.out` is in water, the spectrum in the gas phase. Predict in which direction solvent shifts the C=O stretch, then check it with the gas-phase job `inputs/gas/bq_Q_gas.in` (commands D3; output `results\checks\bq_Q_gas.out`, from D4). Compare the relative differences of the in-plane bands and of the out-of-plane band at 882 cm⁻¹: ______ % and ______ %. The tabulated fundamentals (NIST CCCBDB, assignment of Anno, *J. Chem. Phys.* 42, 932 (1965)) give the lowest out-of-plane modes, 109 cm⁻¹ (B3u) and 241 cm⁻¹ (B2g); computed: ______ and ______ cm⁻¹. If the error differs between modes, a scale factor cannot fix it. Note also what the comparison assumes: that the 1965 assignment of these weak low bands is right.

**D4 · Find the cause, one factor at a time** (exercise; instructor-run if time is short). The candidates are the method (B3LYP-D3) and the numerics. Each input in `inputs/checks/` changes one thing relative to `inputs/gas/bq_Q_gas.in`:

| input | change | tests |
|---|---|---|
| `bq_Q_gas_nops.in` | `nops=1` | pseudospectral integrals with a diffuse basis |
| `bq_Q_gas_grid.in` | `iacc=1`, `rmscp=1.0e-6` | DFT grids and CPHF convergence |
| `bq_Q_gas_tzvp.in` | `basis=def2-TZVP` | diffuse functions (compare the smallest eigenvalue of S: near-linear dependence) |

Predict which one moves the B3u mode, then compare the results. If none of them does, the error is in the functional and is part of the uncertainty of every G that contains a soft mode.

## E · What changes for the other molecules (5 min)

The steps are those of benzoquinone. What changes is listed per family: the states, what is different in the input, and what to check in the output once it has run.

**E1 · AQDS** (anthraquinone-2,7-disulfonate; `inputs/aqds/`, recipe `aqds.csv`)

- *States:* the benzoquinone grid with charge −2 added to every state (the two SO₃⁻), from −2 (Q, QH₂, QH•) to −4 (Q²⁻); QH• and QH⁻ twice, at O9 and at O10 (S7).
- *Input:* the same `&gen` as benzoquinone. Diffuse functions and solvent are essential: UNVERIFIED for this molecule, a gas-phase −3 or −4 ion may not bind its extra electrons at all. Each SO₃⁻ group can rotate: all inputs start from the same orientation (one O of each group perpendicular to the ring, on opposite faces); another orientation is another conformer, with another G.
- *Check in the output:* as for benzoquinone, plus the smallest eigenvalue of S (30 atoms, a diffuse basis, and anions) and the lowest modes (the sulfonate rotations: above or below the quasi-harmonic floor (C4)?).
- *Expected:* the checks of C1–C5 on your own output: 3N − 6 frequencies, 0 imaginary, ⟨S²⟩ close to 0.75 for the radicals, the smallest eigenvalue of S. Cost: well above benzoquinone (30 atoms against 12, with S atoms).

**E2 · TEMPO** (`inputs/tempo/`, recipe `tempo.csv`)

- *States:* the oxoammonium T⁺ (`tp_Tp`), the nitroxide radical T• (`tp_T`, the stable form), the aminoxide anion T⁻ (`tp_Tm`), the hydroxylamine TH (`tp_TH`) and its protonated form TH₂⁺ (`tp_TH2p`). One-electron steps T⁺/T• and T•/T⁻; T⁻ + H⁺ → TH.
- *Input:* the same `&gen`; T• is a doublet (87 electrons) and is computed unrestricted by default.
- *Check in the output:* ⟨S²⟩ of T•; the ring is puckered, so a planar start or a symmetry imposed by hand would be wrong; read the point group from the output.
- *Expected:* the checks of C1–C5 on your own output; for TH (30 atoms, 88 electrons) 84 frequencies, 0 imaginary. Do the methyl rotations fall below the quasi-harmonic floor (C4)? Read it from the lowest modes.

**E3 · Indigo family** (`inputs/indigo/`, recipe `indigo.csv`)

- *States:* dehydroindigo D → indigo I → leucoindigo L, each step adding 2 H and 2 e⁻, with the anions and radicals between them (12 states, S7). Which H is removed is a choice of tautomer: the recipes take N–H for indigo and O–H for leucoindigo (S6).
- *Input:* the same `&gen`. Intramolecular N–H···O=C hydrogen bonds fix the trans (anti) form of indigo; leucoindigo can rotate about the central C–C bond: `di_Lm` and `di_LH3rad` start syn, the others anti, so both should be compared.
- *Check in the output:* the HOMO–LUMO gap of dehydroindigo (HOMO and LUMO energies: ______ eV); a small gap means the stability of the closed-shell solution should be checked. The smallest eigenvalue of S at the first and at the last geometry (______, ______): if it is very small or negative, def2-TZVPD is numerically linearly dependent for this molecule, and the basis must be checked before production.
- *Expected:* the checks of C1–C5 on your own output; for D (28 atoms, 134 electrons) 78 frequencies, 0 imaginary, σ from the point group.

## Homework

1. When your group's output is back (B4), run `summarise_job.py` on it and check every line as in C1–C5 and E; rebuild G by hand as in C4 and add 1.89 kcal/mol. This is the first step of the project.
2. The live PBE job against the production job: which numbers change by more than 1 kcal/mol, and which would matter for a pKa?
3. The worksheet questions of D3, E and L.
4. Make the states of your group's family with `make_inputs.py` and its recipe, and check them with `check_inputs.py`. For leucoindigo, write the recipe line for L⁻ with the N–H removed instead of the O–H.
5. Write five lines on what surprised you and what is unclear, in the worksheet.
