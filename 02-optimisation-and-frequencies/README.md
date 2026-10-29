# Session 2 · Geometry optimisation and harmonic frequencies in continuum solvent

*Jaguar input, submission and output, on 1,4-benzoquinone; what changes for AQDS, TEMPO and the indigo family*

Session 1 ended with the states of benzoquinone, each with a charge and a multiplicity (and, as homework, those of phenazine). Session 3 needs one Gibbs energy G per state, at a geometry that is a true minimum. This session produces and checks those numbers. You write Jaguar inputs, check them before they cost compute time, submit them from PowerShell or the VS Code terminal, and read the output line by line until you can rebuild G by hand. A gas-phase frequency calculation is then compared with the experimental IR spectrum, which is the only point in this course where a computed number meets a measured one directly.

The session is hands-on throughout: every step is worked through together, in pairs, on the files of this folder.

## Learning goals

1. Generate every redox state of a molecule from its closed-shell parents, with the right charge and multiplicity, and turn each into a Jaguar input, by script and in Maestro.
2. Justify a level of theory (functional, basis, solvation model) from cheaper levels and from the quantity that is needed, not from habit.
3. Explain every keyword of a Jaguar optimisation + frequency input and name what it controls physically.
4. Find a wrong charge or multiplicity in an input before submitting it, and explain why an electron count alone does not catch every error.
5. Submit, monitor, cancel, restart and retrieve a Jaguar job from the command line, one job or a whole family.
6. Decide from the output whether a structure is a minimum: convergence criteria, 3N−6 frequencies, no imaginary mode, ⟨S²⟩ for radicals.
7. Rebuild G from E, ZPE and the thermal table; state the approximations behind it (quasi-harmonic, ideal gas at 1 atm, symmetry number) and correct to 1 mol/L.
8. Compare scaled harmonic frequencies with a gas-phase IR spectrum and judge what agreement means.

## Files

| file | used in |
|---|---|
| `worksheet.md` | predictions and results, filled in during the session |
| `inputs/states.csv` | S, A, B: charge and multiplicity of every job of the course; a new job needs a new row |
| `inputs/recipes/` | S: for each family, which parent each state is made from, which H is removed, charge and multiplicity |
| `inputs/levels/` | L: benzoquinone in the gas phase at four more levels of theory (the level ladder) |
| `inputs/solvation/` | L4a: Q and Q²⁻ single points with no solvent, PBF, SMD and C-PCM; their geometry is replaced by the optimised one in L4a |
| `inputs/bq/` | reference copy only: benzoquinone states at the production level, B3LYP-D3/def2-TZVPD in PBF water (`_b3lyp` without D3). You make these files yourself in S3; this copy is for the comparison in S4 and as a fallback if your own run fails |
| `inputs/live/bq_Q_pbe.in`, `bq_QH2_pbe.in` | B: the jobs submitted during the session (PBE/LACVP++\*\*, PBF water) |
| `inputs/groups/` | A4: one input per group with `molchg=??` and `multip=??` |
| `inputs/broken/` | A3: three inputs with an error each |
| `inputs/gas/bq_Q_gas.in` | D: gas-phase Q for the IR comparison (`bq_QH2_gas.in` is not used in class) |
| `inputs/checks/` | D4: one-factor checks of the soft modes |
| `inputs/aqds/`, `inputs/tempo/`, `inputs/indigo/` | E and homework: the other redox families at the production level |
| `scripts/make_inputs.py` | S: parents → all states → one Jaguar input per state, plus `states.maegz` to open in Maestro |
| `scripts/check_inputs.py` | A3, A4: electron count, multiplicity parity, comparison with `states.csv` |
| `scripts/summarise_job.py` | C: the lines of a Jaguar output that decide whether a result is usable, and G rebuilt by hand |
| `scripts/ir_compare.py` | D: computed against experimental IR, with a scale factor; optional plot |
| `commands.ps1` (Windows), `commands.sh` (Linux) | every command of the session, under the name of its step |

`make_inputs.py` uses the Schrödinger Python API and must be run with the suite's Python, `& "$S\run" scripts\make_inputs.py ...`. The other scripts need only Python 3 with `numpy` (and `matplotlib` for the plot); they run with the suite's Python, `& "$S\run" scripts\<name>.py ...`, or any Python with those packages. Paths are written with `\` for Windows; on Linux use `/` (`commands.sh`).

**No output is in the repository, and nothing in this folder has been run yet.** Every output named below is produced by running the corresponding input on the workstation: in the instructor's test run before the session (P) for `results\bq\`, `results\checks\` and the two expensive ladder rungs, and in the session itself for the live, ladder and solvation jobs (B). The starting coordinates in `inputs/` are starting guesses; in the test run they are regenerated with `make_inputs.py` (P1), so do not read anything into them. They were written by `make_inputs.py` from the recipes in `inputs/recipes/`, not by Maestro or Epik. In class you do not start from them: you make the same files yourself (S3), check your own (S4), and only then compare with this copy.

## How each step is written

Every hands-on step has the same four parts:

- **Input**: the file(s) it reads, with their path in this folder;
- **Command**: what you type, in PowerShell or the VS Code terminal (the same lines are in `commands.ps1`, under the name of the step);
- **Expected**: what to check. Where theory fixes the answer (3N − 6 frequencies, 0 imaginary, ⟨S²⟩ = 0.75 for a doublet) it is given; numbers that only a run can give are left as ______, to be filled in from your own output;
- **Why**: what the step tests, and what you do if the result is not the expected one.

Every command uses two variables, set once (Before the session): `$H`, the compute host, and `$J`, the job ID of the job you are looking at.

**Heavy for one molecule, light for all.** Optimisation + frequency jobs at the production level take hours, and longer for the larger molecules. They are run for benzoquinone only. Everything that costs seconds is part of the session for all four families, so that each student has seen the states, inputs and outputs of the molecule of their project before starting it.

| step | benzoquinone | AQDS, TEMPO, indigo family |
|---|---|---|
| S · states → inputs (`make_inputs.py`) | in class, S3 | in class, S7 (each group its own family) |
| S, A · check (`check_inputs.py`) | in class, S4 | in class, S7 |
| A · read the input | in class, A1 | in class, A4 (fill in one group input) |
| B · submit | live PBE job, ladder and solvation jobs; production jobs in the test run (P) | after the session, as the project (homework) |
| C · read an output (`summarise_job.py`) | `bq_Q.out`, `bq_QHrad.out`, `bq_QH2*.out` from the test run | after the session, on the group's own output (E, homework) |
| D · IR | gas-phase job from the test run | not part of the session: no gas-phase spectrum is used for them |

## Before the session

0. Get the files, into your user folder (on the workstation, writing to `C:\` itself was refused):
   `git clone https://github.com/NabKh/schrodinger-tutorials-redox.git $HOME\schrodinger-tutorials-redox`, then `git -C $HOME\schrodinger-tutorials-redox log -1 --oneline` shows the version you have. If the folder already exists, either use it or clone under another name; never work in an old copy that is not a git checkout (`log` then says "not a git repository").
1. On the Windows workstation, in PowerShell: `$S = "C:\Program Files\Schrodinger2026-2"` and `$env:SCHRODINGER = $S`. The second line sets the variable to the same installation as `$S`, so it cannot point at another release (Session 1, B1); without it `jsc hosts list` stops with "$SCHRODINGER must be defined". Then `& "$S\jsc" hosts list` shows the compute hosts besides `localhost` (Session 1, B2). Set `$H = "<one of them>"`. On the workstation the list shows `localhost` (the workstation itself) and the servers `rs4`, `rs5`, `rs6.differ.nl:8030`, each with a CPU node (`cpurs4`, …) and a GPU node (`gpurs4`, …). Jaguar runs on CPUs: `$H = "cpurs4"` (or `cpurs5`, `cpurs6`). `$S`, `$env:SCHRODINGER` and `$H` are lost when the window is closed: in a new window, set them again.
2. `& "$S\jsc" cert get <server>:<port>` is run once per server, if not already in Session 1 (Before the session, item 4).
3. Either PowerShell or the VS Code terminal opens in `$HOME\schrodinger-tutorials-redox\02-optimisation-and-frequencies` (`Set-Location $HOME\schrodinger-tutorials-redox\02-optimisation-and-frequencies`), and `New-Item -ItemType Directory -Force results` makes the folder for everything you produce; `inputs\` is never changed. In VS Code: File > Open Folder > the repository, then Terminal > New Terminal (PowerShell is the default shell on Windows).
4. Session 1's LigPrep output `..\01-introduction\results\bq_prepped.maegz` exists (Session 1, B3); if not, S3 builds the parents from SMILES.

## P · Instructor test run (before 30 Oct)

Everything students read in C, D and L1 comes from these jobs. They are run once, on the workstation, exactly as in class (commands P1–P4).

- **P1 · Inputs.** Regenerate the starting inputs of every family with `make_inputs.py` (S3, S7) and copy them into `inputs\<family>\`, then delete their `MAEFILE:` line (the geometry is in `&zmat`; an input that names a `.mae` fails at once when the `.mae` is not next to it: `Error: unable to find file: bq_Q.mae`, test run); the `_b3lyp` inputs with `--set dftname=B3LYP --suffix _b3lyp`. `bq_QH2cis.in` is not in the recipe (a SMILES carries no cis/trans O–H): build it in Maestro from `bq_QH2` by rotating one O–H by 180°. Run `check_inputs.py` on every folder: all `ok`.
- **P2 · Production benzoquinone.** All of `inputs\bq\*.in` into `results\bq\`.
- **P3 · Gas phase and checks.** `inputs\gas\bq_Q_gas.in` and `inputs\checks\*.in` into `results\checks\`.
- **P4 · Expensive ladder rungs.** `inputs\levels\bq_Q_m062x.in` and `bq_Q_wb97xd.in` into `results\level\`.

*Expected:* for every job, a `.out` that passes C1–C3. A job that does not is restarted (B6) or its input corrected before the session, and the fix is written into this README.

## Time plan

| time | part | what you do |
|---|---|---|
| 0:00 | 0 · Goal | Session 1's five lines (worksheet) read out; from states to G; what makes a G usable |
| 0:05 | S · States → inputs | one molecule, all its states, one input each: by script, then the same in Maestro (demo) |
| 0:30 | L · Level of theory | why B3LYP-D3/def2-TZVPD in PBF water: predictions now, tables from the runs (B5, D3, D4, P) |
| 0:45 | A · The input | read `bq_Q.in` keyword by keyword; fix three broken inputs; fill in your group's input |
| 1:00 | B · Submit | check, then submit the live job and one ladder or solvation job (benzoquinone only); monitor them |
| 1:10 | C · The output | read the benzoquinone production output of the test run; rebuild G |
| 1:40 | D · IR spectrum | scale, compare with the NIST gas-phase spectrum, judge the agreement |
| 1:55 | E · Other molecules | what changes for AQDS, TEMPO and indigo (read at home if time is short) |

## 0 · Goal (5 min)

For each state $i$ this session gives

$$G_i = E_\mathrm{el} + E_\mathrm{ZPE} + G_\mathrm{thermal}(298.15\ \mathrm{K}, 1\ \mathrm{atm}) + 1.89\ \mathrm{kcal/mol}$$

with $E_\mathrm{el}$ the electronic energy in PBF water at the optimised geometry, and $1.89 = RT\ln(24.46)$ kcal/mol the change of standard state from 1 atm to 1 mol/L (RT = 0.592 kcal/mol at 298.15 K). A G is usable only if

- the charge and multiplicity are those of the intended state (A),
- the geometry optimisation converged (C1),
- the structure is a minimum: 3N−6 real frequencies (C2),
- for a radical, the wavefunction is a doublet and not a mixture: ⟨S²⟩ close to 0.75 (C3),
- the lowest-G conformer was found, or the conformers were weighted (C5).

Two energies in Session 3 enter a pKa or a potential as differences. An error of 1.364 kcal/mol in one G moves a pKa by one unit at 298.15 K; 23.06 kcal/mol is 1 V per electron.

## S · From one molecule to all its states, and to one Jaguar input per state (25 min)

Session 1 gave the states of benzoquinone as a list. Here we make them, from start to finish, with a script; then the same in Maestro. The other families follow the same steps (S6, S7).

**Where all the states come from.** One molecule, written as a SMILES (Session 1, `01-introduction/inputs/bq_closed_shell.smi`), gives every state in three moves:

| move | what happens | by hand | by script |
|---|---|---|---|
| a | SMILES → 3D structure of each closed-shell **parent**: Q (C=O) and QH₂ (O–H) | Maestro: draw, or import Session 1's LigPrep output | `make_inputs.py` (same 3D builder as LigPrep) |
| b | **remove a proton**: delete an H bonded to O (QH•, QH⁻, Q²⁻); the atoms change | Maestro: select the H, delete | `strip` column of the recipe |
| c | **add an electron**: only the charge changes, not the atoms (Q•⁻, and the charge of b) | Jaguar panel, *Molecule* tab: charge, multiplicity | `charge`, `multiplicity` columns |

Not Epik: Epik adds or removes protons for a given pH, but not electrons, so it cannot make Q•⁻ or QH•, and LigPrep puts H back on radicals (Session 1, A5). Two parents and these three moves give the six states; the four other files in `inputs/bq/` are not new states but the same molecules at B3LYP without D3 (`_b3lyp`, L1) and QH₂ with one O–H turned by 180° (`bq_QH2cis`, built in Maestro, P1).

**S1 · The proton–electron grid.** Every state is a reference state plus $n_\mathrm{H}$ protons and $n_e$ electrons:

$$\text{charge} = q_\mathrm{ref} + n_\mathrm{H} - n_e,\qquad \text{multiplicity} = 2 \text{ if the electron count is odd, else } 1$$

with $q_\mathrm{ref}$ the charge of the oxidised reference state: 0 for benzoquinone Q and dehydroindigo D, −2 for AQDS (two SO₃⁻), +1 for the TEMPO oxoammonium T⁺.

*Input:* the grid below, and Session 1's rules.

*Command:* none. Fill in the worksheet table S1 (charge, electrons, multiplicity, parent, H removed) before opening the recipe.

| state | job | $n_\mathrm{H}$ | $n_e$ | formula |
|---|---|---|---|---|
| Q | `bq_Q` | 0 | 0 | C₆H₄O₂ |
| Q•⁻ | `bq_Qradm` | 0 | 1 | C₆H₄O₂ |
| QH• | `bq_QHrad` | 1 | 1 | C₆H₅O₂ |
| QH⁻ | `bq_QHm` | 1 | 2 | C₆H₅O₂ |
| QH₂ | `bq_QH2` | 2 | 2 | C₆H₆O₂ |
| Q²⁻ | `bq_Q2m` | 0 | 2 | C₆H₄O₂ |

*Expected:* your table equals `inputs/recipes/bq.csv` (open it after filling in).

*Why:* two kinds of operation make every state from only two closed-shell **parents**, Q and QH₂:

- *removing a proton*: delete an H bonded to O (the atoms change);
- *adding an electron*: change `molchg` only (the atoms stay the same; the electrons are not in the structure file, they are set by the charge).

Q, Q•⁻ and Q²⁻ have the same atoms. The recipe nevertheless makes Q²⁻ from QH₂: Q²⁻ is the hydroquinone without its two protons, so its C–O bonds are expected to be closer to phenolate single bonds than to the C=O of Q, and the hydroquinone ring is the closer start. Check it after the run: r(C–O) in `bq_Q2m.out` against `bq_Q.out` and `bq_QH2.out` (final geometries). Either start should end in the same minimum; a start closer to it costs fewer geometry steps and is less likely to stop in a different one. The radicals are never passed through LigPrep, which adds hydrogens to them (Session 1, A5).

The recipe has one row per state:

```
job,parent,smiles,strip,charge,multiplicity
```

`strip` lists the hydrogens to delete, separated by spaces: `O` is the first H bonded to an O (in atom order) not yet chosen, `O:2` the second, `O O` both; `N` likewise for N–H; an integer is an atom number as shown in Maestro.

**S2 · The parents in 3D.** Two routes, both fine for a molecule this small:

1. *From Session 1*: the LigPrep output `..\01-introduction\results\bq_prepped.maegz` (Session 1, B3: `-i 0 -nt -s 1`, ionisation not changed, no tautomers, one stereoisomer). Its entries are titled `bq_Q`, `bq_QH2`, … from the second column of `bq_closed_shell.smi`; the script picks the parents by title, and stops if two entries have the same title.
2. *From the SMILES in the recipe*: the script builds each parent in 3D itself (`SmilesStructure(...).get3dStructure()` of the Schrödinger API).

**S3 · All states and all inputs, by script.**

*Input:* `inputs/recipes/bq.csv`; optionally `..\01-introduction\results\bq_prepped.maegz`.

*Command* (commands S3):

```powershell
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made
#  or, from the Session 1 LigPrep output:
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made --parents ..\01-introduction\results\bq_prepped.maegz
```

*Expected:* one line per state, for example `bq_Q2m  from bq_QH2  H removed: H9-O1 H12-O6  12 atoms  N=  58  molchg=-2  multip=1`. Each removed H is printed with the atom it was bonded to: `H9-O1` means H9, bonded to O1, so an O–H was removed and not a C–H. The atom numbers depend on how the parent was built, and `wrote 6 inputs and states.maegz to results\made`. Copy your lines into the worksheet (S1).

*Why:* for each row the script copies the parent, deletes the listed hydrogens, checks that the electron count fits the multiplicity, writes `results\made\<job>.in` with the `&gen` keywords of the production level (A1), adds `iuhf=1` (unrestricted) to every state with multiplicity > 1, and appends the structure to `results\made\states.maegz`. `molchg` and `multip` are set from the recipe *after* the structure: the Schrödinger API otherwise takes the charge from the formal charges of the atoms, and a deleted H leaves the O without a formal charge, so QH⁻ would silently become neutral (`setStructure`, `schrodinger/application/jaguar/input.py`). The same keywords at another level: `--level live` (PBE/LACVP++\*\*) or `--level gas`; any single keyword with `--set`, for example `--set basis=6-31G**`; and `--suffix _x` appended to every job name. If the script stops with "electrons cannot have multiplicity", the recipe row is wrong, not the script.

**S4 · Check before submitting.**

*Input:* `results\made\*.in`, `results\made\states.maegz`, `inputs\bq\*.in`.

*Command* (commands S4):

```powershell
& "$S\run" scripts\check_inputs.py results\made
code --diff results\made\bq_Q2m.in inputs\bq\bq_Q2m.in
```

`results\made\states.maegz` holds the six structures for Maestro (File > Import Structures): instructor demo, not needed for the check.

*Expected:* six `ok` lines. In the diff (or, without VS Code on the PATH, `Compare-Object (Get-Content results\made\bq_Q2m.in) (Get-Content inputs\bq\bq_Q2m.in)`):

- `solvent=water` and `multip=1` only in the reference copy. The Schrödinger API writes only keywords that differ from Jaguar's default (`getNonDefault`, `schrodinger/application/jaguar/input.py`), and water and multiplicity 1 are the defaults (`jaguar_keywords.xml`). Both files ask for the same calculation. A radical's `multip=2` is not a default, so it is always written.
- `MAEFILE: bq_Q2m.mae` only in your file: the API also writes `results\made\bq_Q2m.mae`, the same structure as a Maestro file, and points to it. Keep the `.mae` next to its `.in`; when an input is copied elsewhere, copy both.
- Different coordinates and atom names (`C2`, `O6`, `H9` against `C1`, `O2`, `H1`): every 3D build is a new start, and the optimisation should take both to the same minimum.

In the coordinates, check that the H atoms left in Q²⁻ are the C–H ones: each is about 1.08 Å from a ring C (for example H9 to C3 in `results\made\bq_Q2m.in`). An O–H would be about 0.97 Å from an O. Which H was removed is already in the S3 output (`H9-O1`).

*Why:* `check_inputs.py` compares every input with `states.csv` (A3); the diff shows that the inputs given in `inputs/bq/` are made the same way, and that only the start differs. The optimisation should take both starts to the same minimum.

**S5 · The same in Maestro (instructor demo).** One state, then compared with the script:

1. File > Import Structures: `bq_prepped.maegz` from Session 1 (or draw the parent).
2. Derived state: copy the parent entry in the Project Table (UNVERIFIED menu wording in 2026-2: right-click > Duplicate), select the O–H hydrogen in the Workspace and delete it, rename the entry (`bq_QHm`). Removing a proton leaves an O with one bond and no formal charge: either set its formal charge to −1 or set the charge in step 3. Adding an electron needs no change to the structure at all.
3. Jaguar > Optimization (task search, as in Session 1, A6). Tabs:
   - *Molecule*: charge and spin multiplicity of the entry (`molchg`, `multip`).
   - *Theory*: B3LYP-D3, basis def2-TZVPD (`dftname`, `basis`).
   - *SCF*: defaults.
   - *Optimization*: maximum steps 200 (`maxitg`).
   - *Properties*: vibrational frequencies with IR intensities (`ifreq`, `irder`).
   - *Solvation*: PBF, water (`isolv=2`, `solvent`).
4. The gear menu > Write: writes the `.in` file without running it.

*Input:* the written `bq_QHm.in` and `results\made\bq_QHm.in`. *Command:* `code --diff <written file> results\made\bq_QHm.in`, then `check_inputs.py` on the written file. *Expected:* lines that differ: ______ (worksheet S5); `ok`. *Why:* the GUI is good for one state and for looking; the script is reproducible, and is what you use for 30 states. Either way, `check_inputs.py` is run before anything is submitted.

**S6 · The other families.** Same steps, other recipes in `inputs/recipes/`:

| family | parents (closed shell) | derived states | watch |
|---|---|---|---|
| AQDS, `aqds.csv` | `aq_Q` (−2), `aq_QH2` (−2) | Q•⁻ from Q; QH•, QH⁻ (two sites each) and Q²⁻ from QH₂ | the two SO₃⁻ give −2 to every state. The number in the job name is the O that *keeps* its H: `aq_QHrad9` has H on O9, the carbonyl O on the side of the two sulfonates (C9 is peri to C1 and C8, next to C2 and C7). `O:1` and `O:2` are the first and second O–H in atom order; in the atom order of the SMILES in `aqds.csv`, O:1 is atom O10, the O at C10, so stripping it leaves the H on O9. The S7 output shows it: `aq_QHrad9` and `aq_QHm9` print `H removed: H27-O10`, the `10` jobs `H31-O22`. The 2,7-substitution makes the two sites different, so both are computed. |
| TEMPO, `tempo.csv` | `tp_Tp` (oxoammonium, +1), `tp_TH` (hydroxylamine), `tp_TH2p` (+1) | T• and T⁻ from TH, by removing the O–H | T• is a doublet with 87 electrons; the oxoammonium N=O⁺ is a closed shell. |
| indigo, `indigo.csv` | `di_D`, `di_I`, `di_L` (0, 2 and 4 N–H/O–H hydrogens) | D•⁻ from D; D²⁻, DH•, I⁻ (N–H removed) and I•⁻ from I; LH₃•, L⁻, L²⁻ (O–H removed) from L | D²⁻ has the atoms of D but is made from I minus both N–H, as Q²⁻ from QH₂. Which H is removed is a choice of tautomer: L⁻ with O⁻ and with N⁻ are different states with different G. The recipes take O–H for leucoindigo and N–H for indigo; the other choice is a homework question. |

**S7 · The light steps for your group's family** (commands S7). No job is submitted; each command takes seconds.

*Input:* your family's recipe, `inputs/recipes/aqds.csv`, `tempo.csv` or `indigo.csv`; the given inputs in `inputs/<family>/`.

*Command:*

```powershell
$f = "aqds"          # your group's family: aqds, tempo or indigo
& "$S\run" scripts\make_inputs.py inputs\recipes\$f.csv --out results\made_$f
& "$S\run" scripts\check_inputs.py results\made_$f
```

*Expected:* one `ok` line per state. Predict atoms, N, `molchg`, `multip` and open/closed shell for each job from the recipe (S1 rules) before running, then check them against the output; the rows of your family:

```
aq_Q               ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_Q2m             ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_QH2             ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_QHm10           ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_QHm9            ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_QHrad10         ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_QHrad9          ok      __ atoms  N= ___  molchg=__  multip=_  ______
aq_Qradm           ok      __ atoms  N= ___  molchg=__  multip=_  ______
tp_T               ok      __ atoms  N= ___  molchg=__  multip=_  ______
tp_TH              ok      __ atoms  N= ___  molchg=__  multip=_  ______
tp_TH2p            ok      __ atoms  N= ___  molchg=__  multip=_  ______
tp_Tm              ok      __ atoms  N= ___  molchg=__  multip=_  ______
tp_Tp              ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_D               ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_D2m             ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_DHrad           ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_Dradm           ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_I               ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_Im              ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_Iradm           ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_L               ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_L2m             ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_LH3rad          ok      __ atoms  N= ___  molchg=__  multip=_  ______
di_Lm              ok      __ atoms  N= ___  molchg=__  multip=_  ______
```

*Why:* read the table as the S1 grid of the family. Every proton removed lowers the atom count by one and the charge by one at the same N; every electron added raises N by one at the same atoms; odd N is a doublet. A SMILES carries no conformation: syn or anti about the central C–C of leucoindigo, the orientation of the SO₃⁻ groups. Look at them in `results\made_$f\states.maegz`: the AQDS states at O9 and O10 (S6), the AQDS states with charge −3 and −4 (the hardest to describe, E1), and the indigo conformers (E3).

## L · Choosing the level of theory, from cheap to expensive (15 min)

The production level of this course is B3LYP-D3/def2-TZVPD in PBF water. It was chosen beforehand; L1–L4 test it once the runs are back, and it should not be accepted without that test. A level of theory is chosen for one quantity and one accuracy.

In class, section L is predictions: every table below is filled in later, from the jobs submitted in B5 and from the test run (P, D3, D4).

**L0 · The quantity and the target.** Session 3 uses differences of G between states: a pKa from a deprotonation, a potential from a reduction. The targets are 1.364 kcal/mol for one pKa unit and 23.06 kcal/mol per electron for 1 V, so 0.1 V for a 2e⁻ step is 4.6 kcal/mol. An approximation matters only if it changes such a *difference* by a comparable amount. That it changes the absolute energy is not enough.

**L1 · Which effect matters for a difference?**

*Input:* the benzoquinone production outputs of the test run (`results\bq\`, P2) and the solvation single points (L4a).

*Command:* `summarise_job.py` on each pair (commands L1).

*Expected:*

| effect | what to read | for the target |
|---|---|---|
| D3 dispersion | Gtot with and without D3: `bq_Q.out` against `bq_Q_b3lyp.out`, `bq_QH2.out` against `bq_QH2_b3lyp.out` (and `bq_QH2cis` against `bq_QH2cis_b3lyp`); shifts ______ and ______ kcal/mol | change of the Q → QH₂ step: ______ kcal/mol = ______ V (2e⁻) |
| solvation | ΔG_solv of Q and Q²⁻ from L4a: ______ and ______ kcal/mol | an error of 5 % in that of Q²⁻: ______ kcal/mol = ______ V (2e⁻) |

*Why:* prediction first: which of the two rows changes a *difference* more? The answer decides where the effort goes, into the functional or into the solvation model. The `Solvation energy` line of a production output is not used here: with `nogas=2` its gas-phase reference is computed at the *starting* geometry (A1), so it is not a ΔG_solv at one geometry.

**L2 · Functional: the ladder** (Jacob's ladder: GGA → hybrid → meta-GGA hybrid and range-separated hybrid). Q in the gas phase, optimisation and frequencies.

*Input:* the files in the table. *Command:* B5 (the cheap rungs, in class) and P3, P4 (test run); then `summarise_job.py` on each output, and `ir_compare.py` for the C=O stretch and the lowest out-of-plane mode (commands L2). *Expected:*

| rung | input | functional (type) | basis | r(C=O) (Å) | ν(C=O), harmonic (cm⁻¹) | lowest out-of-plane mode (cm⁻¹, label in output) | wall time |
|---|---|---|---|---|---|---|---|
| 1 | `levels/bq_Q_pbe_631g.in` | PBE (GGA) | 6-31G\*\* | | | | |
| 2 | `levels/bq_Q_b3lyp_631g.in` | B3LYP (hybrid GGA) | 6-31G\*\* | | | | |
| 3 | `checks/bq_Q_gas_tzvp.in` | B3LYP-D3 | def2-TZVP | | | | |
| 4 | `gas/bq_Q_gas.in` | B3LYP-D3 | def2-TZVPD | | | | |
| 5 | `levels/bq_Q_m062x.in` | M06-2X-D3 (hybrid meta-GGA) | def2-TZVPD | | | | |
| 6 | `levels/bq_Q_wb97xd.in` | ωB97X-D (range-separated hybrid with dispersion) | def2-TZVPD | | | | |
| exp. | | | | | 1668 (B1u fundamental; band maximum 1678) | 109 | |

The experimental values are the tabulated fundamentals of NIST CCCBDB (assignment of Becker, Charney and Anno, D3) and the band maximum of the NIST gas-phase spectrum (D1).

*Why:* each step changes as few things as possible.

- Steps 1 → 2 change the exchange (no exact exchange → part exact exchange). UNVERIFIED (general knowledge, not checked here): GGAs give too long bonds and too low frequencies, because of the self-interaction (delocalisation) error; hybrids reduce it.
- Steps 2 → 3 change two things at once, the basis (6-31G\*\* → def2-TZVP) and D3; 3 → 4 adds only the diffuse functions (L3).
- Steps 4 → 5 → 6 change the functional at a fixed basis. If 4, 5 and 6 agree within the target, the choice among them does not matter for this quantity. If they do not agree, the spread is part of the uncertainty, and Session 3 (comparison with measured E° and pKa) decides.
- The ladder measures the geometry and the frequencies of one neutral molecule, not the redox energy difference that Session 3 needs. Agreement here is necessary, not sufficient.
- Jaguar's `levels_of_theory.csv` (in `mmshare-v*\data\jaguar\`) flags some functionals as recommended (`is_recommended`; commands L2, L3). In 2026-2 the flag is 1 for B3LYP, B3LYP-D3, M06-2X-D3 and ωB97X-D, and 0 for PBE. This is the vendor's flag, not evidence for our quantity.

**L3 · Basis set.** 6-31G\*\* (double-ζ) → def2-TZVP (triple-ζ, polarisation) → def2-TZVPD (the same plus diffuse functions). Which of them are diffuse is listed in Jaguar's `basis_sets.csv` (commands L2, L3). In 2026-2 `is_diffuse` is 1 for DEF2-TZVPD and LACVP++\*\* and 0 for 6-31G\*\* and DEF2-TZVP; `is_ecp` is 1 only for LACVP++\*\* (an effective core potential on the heavier atoms). What LACVP++\*\* is for H–Ar is not in the file: read it in the Jaguar manual. The outer electrons of an anion are weakly bound and spread far from the nuclei, and a basis without diffuse functions confines them artificially. This matters for QH⁻ and Q²⁻ and for every AQDS state, all of them anions. The price is near-linear dependence of the basis. Read the smallest eigenvalue of the overlap matrix S in every output with a diffuse basis (`summarise_job.py` prints it; C, D4, E): a very small value means the basis must be checked before production.

**L4 · Solvation model.** Jaguar offers, among others (`isolv`, `jaguar_keywords.xml`): 2 PBF (Poisson–Boltzmann, Jaguar's own model, in which all production geometries of this course are optimised), 7 PCM (variant set by `pcm_model`: `cosmo`, `cpcm` (default) or `ssvpe`; set explicitly to `cpcm` in the inputs here), and 8 SMD. In Jaguar, SMD uses C-PCM electrostatics plus its own non-electrostatic terms, so SMD and C-PCM are not independent models for the electrostatic part. `pbf_after_smd=1` runs a PBF single point after an SMD optimisation (`jaguar_keywords.xml`, 2026-2); it is not used here. UNVERIFIED (from the SMD paper's title, not read here): SMD is parametrised on experimental solvation free energies.

**L4a · Solvation single points at the optimised geometries.**

*Input:* `results\bq\bq_Q.01.in` and `results\bq\bq_Q2m.01.in` (the restart inputs of the production jobs, with the last geometry, P2) and the `&gen` sections of `inputs\solvation\*.in` (`igeopt=0`, one `isolv` each, no `ifreq`, `irder` or `nogas`).

*Command* (commands L4a): the `&zmat` of each `.01.in` is combined with each of the four `&gen` sections into `results\solv\`, and the eight jobs are submitted from there.

*Expected:*

| model | `isolv` | E(Q) (Eh) | E(Q²⁻) (Eh) | ΔG_solv(Q) | ΔG_solv(Q²⁻) | ΔE(Q → Q²⁻) (kcal/mol) |
|---|---|---|---|---|---|---|
| none (gas) | – | | | 0 | 0 | |
| PBF | 2 | | | | | |
| SMD | 8 | | | | | |
| C-PCM | 7 | | | | | |

- The PBF single points reproduce the final `SCFE` of `bq_Q.out` and `bq_Q2m.out`: ______ and ______ Eh. This checks the inputs.
- ΔG_solv = E(model) − E(gas) at the same geometry, and it equals the `Solvation energy` line of the same single-point output: ______ against ______ kcal/mol.
- HOMO energy of Q²⁻ in the gas phase: ______ eV. If it is positive, the second electron is not bound in the gas phase: the gas energy then depends on the basis, and so does ΔG_solv(Q²⁻).

*Why:* the spread of the last column across the three models, divided by 46.1 kcal/mol (2 × 23.06), is a first estimate of how uncertain a 2e⁻ potential is from the solvation model alone. Predict which state carries most of the spread, neutral Q or Q²⁻, and check it in the table. The geometry is the PBF one for all four models: a single point does not include the geometry relaxation in each model.

**L5 · What the literature says** (abstracts read; details in the papers):

- Elhajj et al., *J. Chem. Theory Comput.* (2024), doi:10.1021/acs.jctc.4c00602. 345 quinones in DMF (dimethylformamide), one-electron potentials, four continuum models (IEF-PCM, C-PCM, COSMO, SM12). The correlation with experiment is high for the first reduction Q/Q•⁻ (r ≈ 0.95–0.96) and lower for the second, Q•⁻/Q²⁻ (r ≈ 0.74–0.90), whose intercepts lie 210–410 mV below those of the first. Optimising in the reaction field reduced the random error only slightly. The lessons: calibrate against experiment, separately for each step, and expect the doubly charged anion to be the weak point.
- Zhang, Khetan and Er, *Sci. Rep.* 10, 22149 (2020), doi:10.1038/s41598-020-79153-w, and Zhou, Khetan and Er, *Batteries* 7, 71 (2021), doi:10.3390/batteries7040071 (Li-ion cathodes). Geometries from a cheap level plus DFT single points with implicit solvent are about as accurate for quinone redox potentials as full DFT. The lesson: the expensive level is needed for the energy, not necessarily for the geometry.
- Huynh … Hammes-Schiffer, *J. Am. Chem. Soc.* (2016), doi:10.1021/jacs.6b05797: 1e⁻ and 2e⁻/2H⁺ potentials of 134 quinones and the scaling relations between them.
- Er et al., *Chem. Sci.* (2015), doi:10.1039/c4sc03030c: high-throughput computational screening of quinones for flow batteries.
- Methods: Grimme et al. (D3), doi:10.1063/1.3382344; Weigend and Ahlrichs (def2), doi:10.1039/b508541a; Rappoport and Furche (diffuse def2-D), doi:10.1063/1.3484283; Tannor et al., doi:10.1021/ja00105a030, and Marten et al., doi:10.1021/jp953087x (PBF); Marenich, Cramer and Truhlar (SMD), doi:10.1021/jp810292n.

**L6 · The procedure, for any new molecule.**

1. Name the quantity (ΔG of which step) and the accuracy needed (L0).
2. Screen at a cheap level: GGA or hybrid with a double-ζ basis, to find conformers, tautomers and the states that matter: `make_inputs.py <recipe> --out results\screen --level gas --set dftname=PBE --set basis=6-31G** --suffix _screen` (commands L6).
3. Converge the level on one molecule for which experiment exists, here benzoquinone (IR, D). Go up the ladder one factor at a time, for example `--level gas --set dftname=M06-2X-D3 --suffix _m062x`, and stop when the next rung changes the quantity by less than the target.
4. Compute the solvation term with at least two models (L4a). For ions, the spread is usually the largest uncertainty.
5. Validate the whole protocol against measured E° and pKa (Session 3). A systematic offset can be calibrated; a random error cannot.
6. Count the cost. Read the wall time of the benzoquinone production jobs (`summarise_job.py`), and multiply by the number of states and conformers, and by the cost of the larger molecules, before choosing a higher rung.

The course level was chosen with this procedure in mind: a hybrid functional, with dispersion that costs little (its size for benzoquinone is measured in L1), a diffuse basis because most states are anions, and the solvation model in which Jaguar optimises routinely. Its weak point, solvation of the multiply charged ions, is measured in L4a rather than assumed away.

## A · The input (15 min)

**A1 · Read your own `results/made/bq_Q.in` (made in S3) together.**

*Input:* `results/made/bq_Q.in`. *Command:* `code results\made\bq_Q.in` (or Notepad). *Expected:* in this order: `MAEFILE: bq_Q.mae` (the structure file next to it: keep the two together, S4); a `&gen` section (keywords) ending with `&`, with only the keywords that differ from Jaguar's defaults (8 for bq_Q); `entry_name: bq_Q` (the Maestro entry name, used as title; not a keyword); and a `&zmat` section (geometry, Å, one atom per line with a numbered label such as `C1`). *Why:* every keyword below is one physical or numerical choice; fill in the worksheet A1 in your own words.

| keyword | value | what it does | in VASP terms |
|---|---|---|---|
| `dftname` | `B3LYP-D3` | exchange–correlation functional with Grimme's D3 dispersion correction (zero damping) | B3LYP: `LHFCALC = .TRUE.`, `GGA = B3` with `AEXX`, `AGGAX`, `AGGAC`, `ALDAC`; D3 zero damping is `IVDW = 11` (`IVDW = 12` is Becke–Johnson damping, written `B3LYP-D3(BJ)` elsewhere) |
| `basis` | `def2-TZVPD` | Gaussian basis set: triple-ζ, polarisation, diffuse functions for anions | replaces `ENCUT` and the PAW potentials; completeness is controlled by the basis, not a cutoff |
| `isolv=2`, `solvent=water` (`solvent` not written: water is the default, S4) | | Poisson–Boltzmann (PBF) continuum water, self-consistent with the density | VASPsol |
| `nogas=2` | | "assume input zmat is gas phase minimum in solv geopt" (`jaguar_keywords.xml`): no preliminary gas-phase optimisation; the gas-phase reference energy is computed once, at the input geometry, and the optimisation in solvent starts from it | |
| `igeopt=1` | | geometry optimisation to a minimum | `IBRION = 1/2`, `NSW` |
| `maxitg=200` | | maximum number of geometry steps (default 100) | `NSW` |
| `ifreq=1` | | Hessian at the final geometry, then frequencies, ZPE, thermochemistry | `IBRION = 5/6` (finite differences) or `7/8` (DFPT) |
| `irder=1` | | IR intensities | `LEPSILON` / Born charges |
| `molchg` | `0` (not written for a neutral state: 0 is the default) | total charge | `NELECT` (but no compensating background: a molecule needs none) |
| `multip` | `1` (not written for a singlet: 1 is the default, S4) | spin multiplicity 2S+1 | `ISPIN = 2`, `NUPDOWN` |

The radical inputs (`bq_Qradm.in`, `bq_QHrad.in`) also carry `iuhf=1`, an unrestricted wavefunction. Not in the input, but set by default (`jaguar_keywords.xml`, 2026-2):

- `iuhf=2`: restricted if closed shell, unrestricted if open shell; `iuhf=1` makes the choice explicit.
- `nops=0`: pseudospectral integrals where possible.
- `iacc=3`: "quick/solvent" SCF cutoffs; `rmscp=5.0e-5`: CPHF convergence (D4).
- `iaccg=-99`: geometry convergence criteria "ACCURATE in general, SOLV if using PBF". The PBF production and live jobs use the SOLV criteria, the gas-phase jobs the accurate ones (`iaccg=2`). The live job `bq_Q_pbe` (PBF) printed these thresholds in brackets at every geometry step: energy change 1.5E-04, gradient max 1.35E-03 and rms 9.0E-04, displacement max 5.4E-03 and rms 3.6E-03, with a trust radius of 0.30.
- The Hessian: UNVERIFIED (manual, not re-read this session): analytic second derivatives only for basis sets without f functions. The live PBE/LACVP++\*\* job would then have an analytic Hessian, and the def2-TZVPD production jobs a numerical one, from finite differences of analytic gradients (about 6N gradients, 72 for benzoquinone), at many times the cost. Read in the output which one was used.

There are no k-points: a molecule is not periodic, and there are no periodic images to correct for when it is charged.

**A2 · Why these choices.** The argument is in section L; here, connect each keyword to it. Diffuse functions are for the anions QH⁻ and Q²⁻, whose outer electrons are weakly bound (L3). D3 costs little; how much it changes a step between states, and the lowest frequency of QH₂, is measured in L1 (`bq_QH2.out` against `bq_QH2_b3lyp.out`). The optimisation is in water rather than in the gas phase because the anions change geometry in solvent, and the course uses one geometry per state (L4, L5). PBE/LACVP++\*\* in `inputs/live/` and `inputs/groups/` is a cheaper level for practice only; its numbers are not used in Session 3.

**A3 · Three broken inputs.**

*Input:* `inputs/broken/*.in`, and `inputs/live/*.in` (checked here like the others before B2).

*Command:*

```powershell
& "$S\run" scripts\check_inputs.py inputs\broken inputs\live
```

*Expected:* predict the problem of each broken file from the `&gen` section alone and write it in the worksheet first. Then: three `FAIL` lines, and two `ok` lines for `inputs\live`. Which test catches each broken file, parity or `states.csv`? ______ (worksheet A3). Would Jaguar itself refuse any of the three? ______ (found out in the test run).

*Why:* an error by an odd number of electrons (a wrong multiplicity, or a charge off by one) breaks the parity of the electron count and is caught by it. An error by an even number, such as a charge off by ±2, keeps the parity and is caught only by the comparison with the intended state in `states.csv`. The lesson: the electron count catches the wrong spin, not every wrong charge.

**A4 · Your group's input.**

*Input:* one file from `inputs/groups/`:

| group | file | state |
|---|---|---|
| 1 | `tp_T_pbe.in` | TEMPO, the nitroxide radical |
| 2 | `aq_Q_pbe.in` | AQDS, the oxidised quinone with two sulfonates |
| 3 | `di_I_pbe.in` | indigo |
| 4 | `di_L_pbe.in` | leucoindigo |

Decide `molchg` and `multip` from the structure and the S1 rule *before* opening `states.csv`. Write them in place of `??`; if `multip` > 1, add the line `iuhf=1` as in the radical inputs of `inputs/bq/`.

*Command:*

```powershell
& "$S\run" scripts\check_inputs.py inputs\groups
```

*Expected:* `ok` for your file, `TODO` for the three files of the other groups.

*Why:* this is the same check as A3 on a molecule you have not seen computed. A `FAIL` with "expected molchg=…" means your count and the intended state differ: recount the electrons (`N` on the line) before changing anything.

**Your own molecule.** Copy `inputs/bq/bq_Q.in` to a new name, replace the `&zmat` section (Maestro: export as Jaguar input, or `make_inputs.py` with a one-row recipe), set `molchg` and `multip`, and add one row to `inputs/states.csv` (`job,family,charge,multiplicity,added_H,added_e,predicted_point_group,note`). Without that row `check_inputs.py` reports `not in states.csv`.

## B · Submit (10 min)

See `commands.ps1`, sections B1 to B6; the Linux equivalents are in `commands.sh`. Each job is copied into a `results\` folder first and submitted from there, so that the outputs land there and not among the inputs. `-PARALLEL 4` runs the job on 4 cores; Session 1 used 16 (Session 1 README, line 108). Four is used here so that one job per pair fits on the hosts at the same time.

**B1 · Host.**

*Command:* `& "$S\jsc" hosts list`; `& "$S\jsc" server-info rs4.differ.nl:8030`. *Expected:* the compute hosts, and for the job server on rs4 (rs5 and rs6 likewise) its address, `Job server version: 2026-2 …`, `Server API version` equal to `Client API version` (v1.20.5 in the test run) and the free disk space of its file store. A server version or API version different from your client's is the first thing to report if submission fails. *Why:* use a compute host, not `localhost`: set `$H` to it. A job that fails at once with `srun: executable file not found` hit a bad node: submit it again.

**B2 · Live job.** Each pair submits one of the two live inputs, so that both are running.

*Input:* `inputs/live/bq_Q_pbe.in` or `bq_QH2_pbe.in` (PBE/LACVP++\*\*, PBF water; checked in A3).

*Command:*

```powershell
New-Item -ItemType Directory -Force results\live | Out-Null
Copy-Item inputs\live\*.in results\live\
Push-Location results\live
& "$S\jaguar" run bq_Q_pbe.in -HOST $H -PARALLEL 4
Pop-Location
```

*Expected:* a `JobId:` line; the command returns at once. Set `$J` to that JobId. When the job ends, these come back to `results\live` (test run): `bq_Q_pbe.out` (the output read in C), `bq_Q_pbe.log` (progress), `bq_Q_pbe.01.mae` (final structure), `bq_Q_pbe.01.in` (input with the last geometry, B6), `bq_Q_pbe.vib` and `bq_Q_pbe_vib.spm` (vibrations, for Maestro), and `bq_Q_pbe.recover`, `.01.smap`, `.write_dir.json` (job bookkeeping, not read in this session).

*Why:* do not submit the same file twice from the same folder: the second job overwrites the first one's output.

**B3 · Monitor and cancel.**

*Command:*

```powershell
& "$S\jsc" list
& "$S\jsc" info $J
& "$S\jsc" tail-file --name bq_Q_pbe.log $J
& "$S\jsc" cancel $J          # only if the job is wrong
```

*Expected:* `jsc list` shows a table `JobId Name Status Created Runtime Host` with the job as `Running` on `rs4`, or `Waiting` when rs4 is full (in the test run rs4 ran 8 jobs of `-PARALLEL 4` at once and queued the 9th and 10th as `Waiting`: with the whole class submitting, expect to wait); `jsc info` shows the full JobId, the command line, `Status: Running` and the start time. The `.log` shows the SCF and geometry iterations as they happen; the `.out` is complete only at the end. `tail-file --name <file>` prints a job header and then the whole file so far; with `-f` it keeps following it and returns by itself when the job ends (Ctrl+C stops following, not the job). Each geometry step shows the energy, gradient and displacement with the threshold in brackets: `.` not met, `*` met. At the end the log reads `Job bq_Q_pbe completed on rs4.differ.nl` and the time (4.2 min, 4 geometry steps in the test run). A finished job disappears from `jsc list` ("No active jobs were found."); read its final status with `jsc info`: `Status: Completed` and the total running time (4m15s in the test run). `jsc cancel` prints `canceled job <full JobId>`; the job leaves `jsc list` and `jsc info` shows `Status: Canceled`, `Failure reason: The job was canceled by the user.` (a `Waiting` job, test run; the other jobs keep running).

*Why:* a job that ends with no `.out`: read the `.log` and submit again (B1). Cancel a job as soon as you see it was submitted with a wrong input: it frees the host for the others.

**B4 · The other families: not submitted in the session.** A group molecule is larger than benzoquinone, and a production job takes many times longer. The PBE inputs in `inputs/groups/` are for practice (A4); the project uses the production inputs of the family, `inputs\<family>\`, submitted after the session with the family loop of B6 (homework 1).

**B5 · One ladder or solvation job per pair.**

*Input:* as assigned by the instructor: the two cheap rungs `inputs/levels/bq_Q_pbe_631g.in` and `bq_Q_b3lyp_631g.in`, or one of the solvation single points of L4a (once `results\solv\` has been written).

*Command:* commands B5 (the same three lines as B2, from `results\level\` or `results\solv\`).

*Expected:* a `JobId:` line. The M06-2X and ωB97X-D rungs at def2-TZVPD are run in the test run (P4). The results go into the L tables of the worksheet at the start of Session 3.

*Why:* a pair that runs a rung or a model fills one row of a table that the whole class reads.

**B6 · Restart, and a whole family.**

*Restart:* an optimisation that stopped at `maxitg` is continued from its last geometry. *Input:* `<job>.01.in`. *Command:* commands B6: copy it into a `restart` folder under the job's own name, together with `<job>.01.mae`, and submit it from there (the `.01.in` starts with `MAEFILE: <job>.01.mae`, test run; without that file Jaguar stops at once with `Error: unable to find file`). *Expected:* a `JobId:` line (test run: `bq_Q_pbe` restarted this way launched, and was cancelled since it had already converged), then a new `.out` that continues from the last geometry. *Why:* open the copied file first and check that `&gen` still has `igeopt=1` and `ifreq=1` (test run: both kept); keeping the job name means `check_inputs.py` still finds it in `states.csv`. The `.01.in` also carries the last wavefunction (`&guess`) and Hessian (`&hess`), so the restart does not start from scratch (`results\bq\bq_Q.01.in`, test run: 298 kB).

*Family:* every input of a folder, one job each. *Input:* `inputs\<family>\*.in`, without the restart files `*.NN.in`. *Command:* commands B6, family loop. *Expected:* one `JobId:` line per input. *Why:* this is how the project is submitted; check the folder with `check_inputs.py` before the loop.

## C · The output (30 min)

The outputs read here come from the instructor's test run (P2): `results\bq\bq_Q.out` is the workstation run of `inputs\bq\bq_Q.in` (B3LYP-D3/def2-TZVPD, PBF water).

*Input:* `results\bq\bq_Q.out`.

*Command:*

```powershell
& "$S\run" scripts\summarise_job.py results\bq\bq_Q.out
```

*Expected:* the lines below. What the input or theory fixes is given; fill in the ______ from your output (worksheet, C). A line printed as `NOT FOUND` is missing from the output or worded differently: find it by hand.

```
  job                              bq_Q
  stoichiometry                    C6H4O2
  level                            ______  (B3LYP-D3, as in the input)
  basis                            ______  (def2-TZVPD)
  solvent                          ______  (water)
  charge / multiplicity            0 / 1
  electrons                        56
  <S**2> (ideal S(S+1))            ______  (closed shell: no line expected)
  point group (used)               ______  (predict it from the structure)
  smallest eigenvalue of S         ______
  SCFE lines (>= geometry steps)   ______
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

*Why:* then find each line of the summary in the `.out` yourself (search in VS Code with Ctrl+F): C1 to C5 go through them in order. The script is a shortcut for reading, not a replacement: you must be able to find every number in the output.

**C1 · Did the optimisation converge?**

*Input:* `bq_Q.out`. *Command:* search `Geometry optimization complete`; just above it, the last step lists five criteria: energy change, gradient maximum, gradient rms, displacement maximum and displacement rms. Then search `Scaling standard convergence criteria`.

*Expected:* all five criteria met (each value against the threshold in brackets: hartree, hartree/bohr, bohr). Scaling factor in solvent: ______. Number of the last geometry step: ______ (the number of `SCFE` lines can be larger: one `SCF energy` line for the gas phase, then one `Solution phase energy` line per solvation iteration of every geometry step; the live job had 4 steps and 12 lines). Gradient-maximum threshold: ______ Eh/bohr = ______ eV/Å (1 Eh/bohr = 51.42 eV/Å).

*Why:* in VASP terms, compare with `EDIFFG = −0.02` (eV/Å, a force criterion on every atom) — but VASP stops on forces alone, Jaguar on five criteria at once, so the numbers are comparable only as orders of magnitude. If a criterion is not met and the step limit was reached, restart (B6).

**C2 · Is it a minimum?**

*Input:* `bq_Q.out`. *Command:* search `Number of imaginary frequencies`. *Expected:* 30 frequencies for 12 atoms (3N − 6), 0 imaginary. The lowest: ______ cm⁻¹, label ______. Which motion is it? (Maestro: open `bq_Q.01.mae` or the `.out` and animate the mode.)

*Why:* an imaginary mode after an optimisation usually means that the optimiser stopped at a saddle point, often because the start had a symmetry that the minimum does not have. Displace along the imaginary mode, reoptimise, and check again.

**C3 · Radicals.**

*Input:* `results\bq\bq_QHrad.out`. *Command:* `summarise_job.py results\bq\bq_QHrad.out`, and search `<S**2>`. *Expected:* close to 0.75: ______. The thermal table has an `elec.` row with S = R ln 2 = 1.377 cal/(mol K) for a doublet.

*Why:* a pure doublet has S(S+1) = 0.75. A value well above it means spin contamination: the energy is no longer that of a doublet. As a rule of thumb only (not a fixed limit): more than about 10 % above 0.75 needs a look at the spin density and at another functional.

**C4 · Rebuild G by hand.**

*Input:* the end of `bq_Q.out`. *Command:* search each line of the table:

| line | value |
|---|---|
| last `Solution phase energy` (line `SCFE:  Solution phase energy: …`, two spaces after `SCFE:`) | Eh |
| `The zero point energy (ZPE)` | kcal/mol |
| `total` row, G column (without ZPE) | kcal/mol |
| `Total Gibbs free energy, Gtot` | Eh |

*Expected:* $E + (\mathrm{ZPE} + G_\mathrm{table})/627.5095$ = Gtot, to within the rounding of the printed numbers (the last line of `summarise_job.py` does the same). With `nogas=2` the gas-phase energy is computed once, at the input geometry (the `.out` says so after `The solvation energy is computed from`), so the printed `Solvation energy` is not a solvation free energy between two optimised geometries; E and Gtot are not affected. Gtot already contains the ZPE; it is at 1 atm, so +1.89 kcal/mol is still to be added for 1 mol/L.

Then search `Quasi-Harmonic`, above the vibrational temperatures. If it is there, every mode below a minimum frequency (printed on the next lines: ______ cm⁻¹) is treated as if it were at that frequency when the vibrational entropy is computed. Compare the floor with the lowest frequency of C2 (worksheet C4). Finally `rotational symmetry number`: ______.

*Why:* low modes give the largest entropy and are the least harmonic; a floor avoids an entropy that grows without bound as a frequency goes to zero. Which molecules of the course have modes that could fall below the floor (E)? σ enters the rotational entropy as −R ln σ, so G contains +RT ln σ: D2h has σ = 4, and a σ of 1 (for example from a structure that lost its symmetry) would make G lower by RT ln 4 = 0.82 kcal/mol. Do not also count symmetry-equivalent structures by hand.

**C5 · Two conformers of QH₂.**

*Input:* `results\bq\bq_QH2.out` (trans O–H, C2h) and `bq_QH2cis.out` (cis, C2v). *Command:* commands C (`summarise_job.py` on both). *Expected:* Gtot ______ and ______ Eh, ΔG = ______ kcal/mol. With $p_i = e^{-G_i/RT} / \sum_j e^{-G_j/RT}$ (RT = 0.592 kcal/mol): ______ % trans, ______ % cis. The G of QH₂ as a mixture: $G = -RT \ln \sum_i e^{-G_i/RT}$ = ______ Eh.

*Why:* is ΔG larger than the error of the method? The mixture G is never above the lowest one, and differs from it by at most RT ln 2 = 0.41 kcal/mol for two conformers. Which G goes into Session 3, and why (worksheet C5)?

**C6 · The live job.**

*Input:* `results\live\bq_Q_pbe.out`, when it is back. *Command:* `summarise_job.py results\live\bq_Q_pbe.out`. *Expected:* fill in the C6 table of the worksheet: geometry steps, lowest frequency, wall time, smallest eigenvalue of S, against `bq_Q.out`. Test run (PBE/LACVP++**, PBF water, 4 threads on rs4): every line found; 4 geometry steps but 12 `SCFE` lines; 30 vibrations, 0 imaginary, lowest 118.7 cm⁻¹ (B3u); point group D2h, σ = 4; smallest eigenvalue of S 3.086E-06; quasi-harmonic floor 100 cm⁻¹; 0.07 h; G rebuilt by hand equals Gtot (−380.986496 Eh) to 0.000 kcal/mol. *Why:* the same molecule at a cheaper level; the differences show what the production level costs and what it changes.

## D · IR spectrum (15 min)

Harmonic frequencies are the curvature of the potential at the minimum; measured bands are anharmonic fundamentals and lie a few per cent lower. A scale factor fitted per method and basis absorbs most of this, on average. The outputs come from the test run (P2, P3).

**D1 · Experimental spectrum.**

*Input:* none. *Command:* commands D1 (download from the NIST Chemistry WebBook into `results\bq_Q_nist.jdx`). *Expected:* a text file whose header lines include `##TITLE=`, `##STATE=` (gas), `##XUNITS=1/CM`, `##YUNITS=ABSORBANCE`; data from 550 to 3846 cm⁻¹. *Why:* it is NIST Standard Reference Data: use it in class, do not redistribute it, do not commit it. Modes below 550 cm⁻¹ are outside the spectrum.

**D2 · Compare.**

*Input:* `results\bq\bq_Q.out`, `results\bq_Q_nist.jdx`.

*Command:*

```powershell
& "$S\run" scripts\ir_compare.py results\bq\bq_Q.out --scale 0.963 --exp results\bq_Q_nist.jdx --plot results\bq_Q_ir.pdf
```

0.963 ± 0.044 is the NIST CCCBDB factor for B3LYP/def2-TZVPP, the closest available to def2-TZVPD; for the live PBE job use 0.989 ± 0.027 (PBEPBE/6-31+G\*\*) (cccbdb.nist.gov, vibrational scaling factors). The ± is the scatter of the fit: 0.044 is 74 cm⁻¹ at 1678 cm⁻¹, larger than most differences below.

*Expected:* five experimental peaks found (1678, 882, 1302, 1054, 1070 cm⁻¹, strongest first), each matched to one computed mode, with the error in cm⁻¹ and %. Fill in the computed columns (worksheet, D):

| experiment (cm⁻¹) | rel. | mode (index) | calc., scaled | assignment | difference |
|---|---|---|---|---|---|
| 1678 | | | | C=O stretch | |
| 1302 | | | | | |
| 1070 / 1054 | | | | | |
| 882 | | | | C–H out of plane | |

*Why:* the script matches each peak to the nearest IR-active mode and marks a peak that falls on a mode already matched (`same mode as the … peak`): that is one band split in two, not a second mode. In the test run the live PBE job put 1054 and 1070 on the same mode 17 (1054.8 cm⁻¹ scaled). Check every match by the displacement of the mode in Maestro. 1678 cm⁻¹ is the band maximum: the tabulated C=O fundamental is 1668 cm⁻¹ (B1u), and the band is split by a Fermi resonance. The plot broadens each computed line with a Lorentzian of 10 cm⁻¹ half width.

**D3 · Judge the agreement.**

*Input:* `results\checks\bq_Q_gas.out` (gas phase, P3). *Command:* commands D3. *Expected:* predict first in which direction solvent shifts the C=O stretch, then: C=O in water ______, in the gas phase ______ cm⁻¹. Relative differences of the in-plane bands and of the out-of-plane band at 882 cm⁻¹: ______ % and ______ %. The two lowest out-of-plane modes, computed: ______ and ______ cm⁻¹, against the tabulated fundamentals 109 and 241 cm⁻¹ (NIST CCCBDB).

*Why:* `bq_Q.out` is in water, the spectrum in the gas phase; the gas-phase job separates the solvent from the method. The low modes are below 550 cm⁻¹ and not in the spectrum: they are compared with the tabulated fundamentals only. 241 cm⁻¹ (B2g) is IR-inactive (a g mode of a centrosymmetric molecule) and comes from other data. Symmetry labels depend on the choice of axes: CCCBDB labels the 109 cm⁻¹ mode B3u, the 1965 papers B1u. Identify each mode by its displacement, not by its label. The assignment is that of Becker, Charney and Anno, *J. Chem. Phys.* 42, 942 (1965), doi:10.1063/1.1696085, with the normal-coordinate analysis of Anno, *J. Chem. Phys.* 42, 932 (1965), doi:10.1063/1.1696084. If the error differs between modes, a single scale factor cannot fix it. The comparison also assumes that the 1965 assignment of these weak low bands is right.

**D4 · Find the cause, one factor at a time** (outputs from the test run, P3).

*Input:* each file in `inputs/checks/` changes one thing relative to `inputs/gas/bq_Q_gas.in`:

| input | change | tests (`jaguar_keywords.xml`, 2026-2) |
|---|---|---|
| `bq_Q_gas_nops.in` | `nops=1` | "analytic calculation only": no pseudospectral integrals, with a diffuse basis |
| `bq_Q_gas_iacc.in` | `iacc=1` | "v. high scf accuracy (ufine only)" instead of the default quick cutoffs |
| `bq_Q_gas_cphf.in` | `rmscp=1.0e-6` | CPHF convergence, default 5.0e-5: the response of the density, which enters the Hessian and the IR intensities |
| `bq_Q_gas_tzvp.in` | `basis=def2-TZVP` | diffuse functions (compare the smallest eigenvalue of S: near-linear dependence) |

*Command:* commands D4 (`summarise_job.py` and `ir_compare.py` on each). *Expected:* lowest out-of-plane mode and 882 band for each (worksheet D4). *Why:* predict which one moves the lowest out-of-plane mode, then compare. If none of them moves it, the numerics are not the cause; what remains is the functional and the harmonic approximation itself, for a soft mode that may be strongly anharmonic, and these checks cannot separate the two. Either way it is part of the uncertainty of every G that contains a soft mode.

## E · What changes for the other molecules (5 min)

The steps are those of benzoquinone. What changes is listed per family: the states, what is different in the input, and what to check in the output once it has run (after the session, homework 1).

**E1 · AQDS** (anthraquinone-2,7-disulfonate; `inputs/aqds/`, recipe `aqds.csv`)

- *Input:* the inputs of `inputs/aqds/`, regenerated in the test run (P1): the benzoquinone grid with charge −2 added to every state (the two SO₃⁻), from −2 (Q, QH₂, QH•) to −4 (Q²⁻); QH• and QH⁻ twice, at O9 and at O10 (S6). The same `&gen` as benzoquinone. Each SO₃⁻ group can rotate, and a SMILES fixes no orientation: check in `states.maegz` that all states start from the same orientation; another orientation is another conformer, with another G.
- *Command:* homework 1 (family loop), then `summarise_job.py` on each output.
- *Expected:* the checks of C1–C5 on your own output: 3N − 6 frequencies (30 atoms: 84; 32 for QH₂: 90), 0 imaginary, ⟨S²⟩ close to 0.75 for the radicals, the smallest eigenvalue of S (30–32 atoms, a diffuse basis, and anions). The lowest modes, the sulfonate rotations: above or below the quasi-harmonic floor (C4)? ______.
- *Why:* diffuse functions and solvent are essential here: UNVERIFIED for this molecule, a gas-phase −3 or −4 ion may not bind its extra electrons at all (L4a, HOMO check). Cost: well above benzoquinone (30 atoms against 12, with S atoms).

**E2 · TEMPO** (`inputs/tempo/`, recipe `tempo.csv`)

- *Input:* the oxoammonium T⁺ (`tp_Tp`), the nitroxide radical T• (`tp_T`, the stable form), the aminoxide anion T⁻ (`tp_Tm`), the hydroxylamine TH (`tp_TH`) and its protonated form TH₂⁺ (`tp_TH2p`). One-electron steps T⁺/T• and T•/T⁻; T⁻ + H⁺ → TH. The same `&gen`; T• is a doublet (87 electrons), with `iuhf=1`.
- *Command:* as E1.
- *Expected:* ⟨S²⟩ of T•: ______; point group read from the output: ______ (the ring is puckered, so a planar start or a symmetry imposed by hand would be wrong). For TH (30 atoms, 88 electrons) 84 frequencies, 0 imaginary. Do the methyl rotations fall below the quasi-harmonic floor (C4)? ______.
- *Why:* in TH and TH₂⁺ the O–H on N can be axial or equatorial, connected by inversion at N and ring flip: two conformers, to be compared as in C5.

**E3 · Indigo family** (`inputs/indigo/`, recipe `indigo.csv`)

- *Input:* dehydroindigo D → indigo I → leucoindigo L, each step adding 2 H and 2 e⁻, with the anions and radicals between them (11 states, S7). Which H is removed is a choice of tautomer: the recipes take N–H for indigo and O–H for leucoindigo (S6). The same `&gen`. Intramolecular N–H···O=C hydrogen bonds fix the trans form of indigo; leucoindigo can rotate about the central C–C bond, so syn and anti are two conformers of every L state.
- *Command:* as E1. For the second conformer: in Maestro, set the N–C–C–N dihedral about the central bond to 0° (syn) or 180° (anti) (UNVERIFIED menu wording in 2026-2: Edit > Adjust > Distances, Angles or Dihedrals), export as a Jaguar input with a new job name (`di_Lm_anti`), and add a row to `states.csv`.
- *Expected:* HOMO and LUMO energies of D: ______ eV. Smallest eigenvalue of S at the first and the last geometry: ______, ______. For D (28 atoms, 134 electrons) 78 frequencies, 0 imaginary, σ from the point group. G of syn and anti for each L state: ______.
- *Why:* a small HOMO–LUMO gap means that the closed-shell solution may not be the lowest: rerun the single point with `wf_stability=1` (wave-function stability analysis, `jaguar_keywords.xml`, 2026-2). A very small eigenvalue of S means def2-TZVPD is numerically near-linearly dependent for this molecule, and the basis must be checked before production. The point groups in `states.csv` are predictions; the output decides.

## Homework

Each item has the same four parts as the steps of the session.

1. **Submit your family at the production level.** *Input:* `inputs\<family>\*.in`. *Command:* `check_inputs.py inputs\<family>`, then the family loop (commands B6, HW1). *Expected:* one `ok` line and one `JobId:` per state. When the outputs are back, `summarise_job.py` on each: every line checked as in C1–C5 and E; G rebuilt by hand as in C4, + 1.89 kcal/mol. *Why:* this is the first step of the project, and the G of Session 3.
2. **Live against production.** *Input:* `results\live\bq_Q_pbe.out`, `results\bq\bq_Q.out`. *Command:* `summarise_job.py` on both. *Expected:* the numbers that change by more than 1 kcal/mol: ______. *Why:* which of them would matter for a pKa (1.364 kcal/mol per unit)?
3. **One convergence factor on your own molecule.** *Input:* the production input of one state of your family. *Command:* `make_inputs.py inputs\recipes\<family>.csv --out results\conv --set basis=def2-TZVP --suffix _tzvp` (or `--set iacc=1 --suffix _iacc`), add the `states.csv` rows, check, submit one job. *Expected:* the change in the lowest frequency and in G: ______. *Why:* D4 on your molecule: is the production level converged for it?
4. **One solvation spread on your own redox pair.** *Input:* the two `.01.in` of one redox step of your family. *Command:* L4a with your two jobs (commands HW4), the new rows added to `states.csv`. *Expected:* ΔE of the step with PBF, SMD and C-PCM: ______; spread ______ V. *Why:* L4a for the molecule of your project.
5. **States and the other tautomer.** *Input:* your family's recipe. *Command:* `make_inputs.py` and `check_inputs.py` (S7). For leucoindigo, write the recipe line for L⁻ with the N–H removed instead of the O–H, add its row to `states.csv`, and rerun. *Expected:* `ok` for every line. *Why:* a tautomer is a different state with a different G (S6).
6. **The worksheet questions** of D3, E and L, and **five lines** on what surprised you and what is unclear, in the worksheet.
