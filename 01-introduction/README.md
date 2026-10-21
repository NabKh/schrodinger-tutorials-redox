# Session 1 · Introduction: redox chemistry, DFT and the Schrödinger suite

Follow `session1-slides.pdf`; this page gives, for each hands-on step of the slides, what to do, the files and commands to use, and the expected result. Parts 0 and 1 of the slides (chemistry and DFT background) have no hands-on steps. No DFT jobs are run in this session; Jaguar starts in Session 2.

## Files

| file | used in |
|---|---|
| `session1-slides.pdf` | the whole session |
| `worksheet.md` | predictions and results, filled in during the session |
| `inputs/bq_closed_shell.smi`, `inputs/bq_radicals.smi` | A, B: the six benzoquinone states |
| `commands.ps1` (Windows), `commands.sh` (Linux) | B, C and homework: every command of the session |
| `scripts/check_structures.py` | B: formula, charge, electron count and multiplicity of each structure |
| `scripts/extract_entry.py` | C: copies one entry out of a structure file |
| `scripts/list_epik_states.py` | C, homework: the states Epik returned, with charge and electron count |
| `session1-notebook.ipynb` | C and homework: charges, populations against pH, E(pH) line, macro-pKa, error propagation |
| `inputs/homework_phenazine.smi` | homework |

The three scripts run with the suite's Python: `& "$S\run" scripts\<name>.py ...` on Windows, where `$S` is the installation folder (B1), and `$SCHRODINGER/run scripts/<name>.py ...` on Linux. The notebook needs only `numpy`, `matplotlib`, `rdkit` and `jupyter` (`requirements.txt` in the main folder), no Schrödinger licence.

## Before the session

1. Maestro opens and Help > About Maestro reports release 2026-2; Maestro, LigPrep, Epik and Jaguar start without a licence error.
2. The repository is on a local disk, for example `C:\schrodinger-tutorials-redox`, not on a network share.
3. The job settings of any panel (gear icon next to Run) list a compute host besides `localhost` (needed from Session 2 on).
4. For remote jobs, each user registers once with the job server: `& "C:\Program Files\Schrodinger2026-2\jsc" cert get <server>:<port>` (server and port from your administrator; add `--user <name>` if your cluster user name differs).
5. In PowerShell, `& "C:\Program Files\Schrodinger2026-2\run" python3 -c "print('suite OK')"` prints `suite OK`.

## The states used in this session (slides 9 and 13)

| key | label | $n_\mathrm{H}$ | $n_e$ | charge | multiplicity | SMILES |
|---|---|---|---|---|---|---|
| Q | Q | 0 | 0 | 0 | 1 | `O=C1C=CC(=O)C=C1` |
| Qradm | Q•⁻ | 0 | 1 | −1 | 2 | `[O-]c1ccc([O])cc1` |
| QHrad | QH• | 1 | 1 | 0 | 2 | `[O]c1ccc(O)cc1` |
| QH2 | QH₂ | 2 | 2 | 0 | 1 | `Oc1ccc(O)cc1` |
| QHm | QH⁻ | 1 | 2 | −1 | 1 | `[O-]c1ccc(O)cc1` |
| Q2m | Q²⁻ | 0 | 2 | −2 | 1 | `[O-]c1ccc([O-])cc1` |

- charge = $n_\mathrm{H} - n_e$ (Jaguar keyword `molchg`)
- multiplicity = 2 if $n_e$ is odd (one unpaired electron), otherwise 1 (Jaguar keyword `multip`). This assumes a closed-shell parent and the low-spin state. For a charged parent, such as the methyl viologen dication MV²⁺, add its charge to the first rule.

Radicals are calculated spin-unrestricted in Jaguar (`iuhf=1`); its default for open shells is restricted.

## A · Maestro (slides 31 to 40)

**A1 · Project** (slide 34).
1. Get the repository as described under Getting started in the [main README](../README.md).
2. In the folder `01-introduction`, create a subfolder `results` for your outputs.
3. Maestro: File > Change Directory > `01-introduction`.
4. File > Save Project As > `bq_part1`.
5. Help > About Maestro: note the release.

*Expected:* the project name in the title bar, release 2026-2.

**A2 · Task search and job settings** (slide 35). Type `ligprep` in the task search box and open the panel. Open the job settings (gear icon next to Run) and look at the host list. LigPrep and Epik run on `localhost`; Jaguar jobs go to a compute host.

**A3 · Import the states** (slides 36 and 37). File > Import Structures > `inputs/bq_closed_shell.smi` and `inputs/bq_radicals.smi`.

*Expected:* six entries, `bq_Q`, `bq_QH2`, `bq_QHm`, `bq_Q2m`, `bq_QHrad`, `bq_Qradm`. The radicals contain `[O]`, an oxygen with no hydrogen and no charge. Select the two radicals and File > Export Structures > `results/bq_radicals.mae`; section B checks this file.

**A4 · Check the Project Table** (slide 38). Compare formula and total charge:

| entry | formula | charge |
|---|---|---|
| bq_Q | C6H4O2 | 0 |
| bq_QH2 | C6H6O2 | 0 |
| bq_QHm | C6H5O2 | −1 |
| bq_Q2m | C6H4O2 | −2 |
| bq_QHrad | C6H5O2 | 0 |
| bq_Qradm | C6H4O2 | −1 |

The charge is stored in the structure; the spin multiplicity is set in the Jaguar panel (table above). If the formula and charge columns are not shown, `scripts/check_structures.py` gives the same check (section B).

**A5 · LigPrep without changing the ionisation state** (slide 39). Select the four closed-shell entries, not the radicals, and open LigPrep:

- Use structures from: Project Table (selected entries)
- Ionization: **Do not change**
- **Untick Generate tautomers**
- Stereoisomers: 1
- Job settings: `localhost`, job name `bq_prep`

*Expected:* four new entries with the same formulas and charges as in A4.

> **Pitfalls.** With "Generate possible states at target pH", LigPrep converts QH⁻ back into neutral hydroquinone without a warning. With tautomer generation on, extra entries can appear. LigPrep adds hydrogens to radicals, so QH• and Q•⁻ are not passed through it; Jaguar optimises the imported structures. Always check formula and charge after a preparation step.

**A6 · Jaguar panel, look only** (slide 40). Open Jaguar > Optimization through task search and go through the tabs: Input (charge and spin per entry), Theory, Properties (frequencies), Solvation, and the job settings. Close the panel without running.

## B · Command line (slides 41 to 45)

See `commands.ps1` (Windows) or `commands.sh` (Linux), sections B1 to B3.

**B1** (slide 42) opens the suite by its full installation path. If several releases are installed, the environment variable `SCHRODINGER` may point at a different one. Keep Maestro open while running the commands, or start the local job server first: `& "$S\jsc" local-server-start`.
*Expected:* `suite OK`.

**B2** (slide 43) lists the hosts and your jobs. Before a Windows workstation can submit to remote hosts, each user registers once with the job server: `& "$S\jsc" cert get <server>:<port>`, with the server and port from your administrator.
*Expected:* the configured hosts, and the `bq_prep` job from A5.

**B3** (slide 44) runs LigPrep with `-i 0 -nt`, the command-line equivalent of "Do not change" with tautomers off, then `scripts/check_structures.py` on the output and on `results/bq_radicals.mae`. Without `-i 0`, LigPrep neutralises, and may re-ionise, QH⁻ and Q²⁻; check the default with `ligprep -h`.
*Expected:* 56 electrons for `bq_Q`; 57 for `bq_QHrad` and `bq_Qradm`, multiplicity 2; 58 for `bq_QH2`, `bq_QHm` and `bq_Q2m`.

| GUI | command |
|---|---|
| File > Change Directory | `cd <folder>` |
| File > Export Structures (format conversion) | `& "$S\utilities\structconvert" in.maegz out.mae` |
| LigPrep panel | `& "$S\ligprep" -ismi ... -omae ... -i 0 -nt -s 1` |
| Epik panel | `& "$S\epikx" in.mae out.maegz -ph 7.0 -pht 7.0` |
| Jaguar panel > Run | `& "$S\jaguar" run -HOST <host> -PARALLEL 16 job.in` |
| Job Monitor | `& "$S\jsc" list` |

PowerShell finds `run.exe` from `"$S\run"`; on Linux the programs are `$SCHRODINGER/run`, `$SCHRODINGER/ligprep` and so on.

## C · Epik (slides 46 to 54)

**What Epik does.** Epik 7 predicts pKa values with an ensemble of graph convolutional neural networks (Johnston et al. 2023), trained on over 42,000 pKa values, experimental and computed with Jaguar pKa, mostly for drug-like, closed-shell molecules. It lists the protonation states and tautomers populated within a pH window, a target pH plus or minus a tolerance. It changes the number of **protons only**, never the number of electrons: on the grid it moves along a row and never to another row.

| setting | default (EpikX, 2026-2) | wide run |
|---|---|---|
| target pH | 7.4 | 7.0 |
| pH tolerance | 2.0 | 7.0 |
| population cut-off | alternative to the tolerance | not set |
| charge window | −2 to +2 | covers QH₂ (0) to Q²⁻ (−2) |
| maximum structures | 16 | 16 |

There are two readings of a pH window. The Epik 7 paper defines the tolerance as a population threshold at the target pH ($10^{-\Delta\mathrm{pH}}$: 10 % for 1.0, 1 % for 2.0). The LigPrep documentation describes states populated within the range. The three runs below show which reading your release applies.

**C1 · Three runs in Maestro** (slide 51). Select `bq_QH2` in the group made by the `bq_prep` job and open Epik.

| run | settings | job name |
|---|---|---|
| 1 | defaults | `bq_QH2_epik_default` |
| 2 | target pH 7.0, pH tolerance 7.0, up to 16 states | `bq_QH2_epik_wide` |
| 3 | target pH 12.0, pH tolerance 2.0 | `bq_QH2_epik_ph12` |

Write down your prediction before running, then count the output states and their charges.

*Expected:*

| run | threshold reading | window reading |
|---|---|---|
| 1 | QH₂ | QH₂, QH⁻ (14 % at pH 9.4) |
| 2 | QH₂, QH⁻ | QH₂, QH⁻, Q²⁻ |
| 3 | QH⁻, Q²⁻ (QH₂ is close to the cut) | QH₂, QH⁻, Q²⁻ |

No run returns Q or QH•, and the electron count stays 58. Section 2 of `session1-notebook.ipynb` reproduces both columns; its window reading uses a 10 % population, a choice made for illustration.

**C2 · Command line** (slide 52). These are the commands of section C2 of `commands.ps1`:

```powershell
& "$S\run" scripts\extract_entry.py results\bq_prepped.maegz bq_QH2 results\bq_QH2.mae
& "$S\epikx" -h
& "$S\epikx" results\bq_QH2.mae results\bq_QH2_epik_default.maegz -WAIT
& "$S\epikx" results\bq_QH2.mae results\bq_QH2_epik_wide.maegz -ph 7.0 -pht 7.0 -ms 16 -WAIT
& "$S\epikx" results\bq_QH2.mae results\bq_QH2_epik_ph12.maegz -ph 12.0 -pht 2.0 -ms 16 -WAIT
& "$S\run" scripts\list_epik_states.py results\bq_QH2_epik_default.maegz results\bq_QH2_epik_wide.maegz results\bq_QH2_epik_ph12.maegz
```

| flag | meaning |
|---|---|
| `-ph` | target pH |
| `-pht` | pH tolerance |
| `-ms` | maximum number of returned structures (default 16) |

These are the expected flags; confirm them with `-h`, and if your release lists a different name, use that one. `-WAIT` makes each command return only when its job has finished.
*Expected:* the same states as in C1.

**Why Epik cannot replace Jaguar.** On the proton-electron grid Epik moves along a row and never between rows, so it cannot connect Q with QH₂. Epik's own pKa values do not enter the computed results; they matter only if a poor prediction removes a state from the list.

**C3 · Enumeration for a new molecule** (slide 53).

1. Build one input structure per redox level ($n_e$ = 0, 1, 2), with charge and hydrogens as intended. Build the open-shell row by hand: Epik and LigPrep are made for closed-shell molecules.
2. Run Epik on each closed-shell input with target pH 7.0 and pH tolerance 7.0, up to 16 states, and add runs at pH 12 ± 2 and pH 2 ± 2: under the threshold reading, pH 7 ± 7 misses states populated only near the ends, such as Q²⁻. Tautomers are generated unless switched off.
3. Alternatively, LigPrep with Ionization by Epik (not Epik Classic) with tautomers on; confirm the command-line flags with `ligprep -h`. This is the opposite of A5.
4. From the command line: `epikx` with `-ph`, `-pht` and `-ms`, as in C2; confirm the flags with `-h` first.
5. Group the output by charge, remove duplicates and symmetry-equivalent copies (statistical factor through symmetry numbers or by counting, not both), check formula and charge, set the multiplicity, and check OH rotamers. Each remaining microstate needs a Jaguar Gibbs energy.

For benzoquinone over pH 0 to 14 this gives Q in the oxidised row, QH• and Q•⁻ in the radical row (built by hand), and QH₂, QH⁻ and Q²⁻ in the reduced row; Q²⁻ possibly only from the pH 12 run.

## Homework (slide 56)

1. Work through `session1-notebook.ipynb`: charges and multiplicities, populations against pH, the E(pH) line, micro- and macro-pKa, and how an error in a Gibbs energy reaches pKa and potential.
2. Draw the proton-electron grid of phenazine (`c1ccc2nc3ccccc3nc2c1`). Which cells are populated between pH 0 and 14? Give SMILES, $n_\mathrm{H}$, $n_e$, charge and multiplicity of each. Phenazine is protonated on a ring nitrogen near pH 1.
3. Run Epik with default and wide settings on dihydrophenazine (`c1ccc2c(c1)Nc1ccccc1N2`), using the homework commands in `commands.ps1`, and record the states and charges in the worksheet.
4. Write five lines on what surprised you and what is unclear, in the worksheet.
