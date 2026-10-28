# Session 2 · Geometry optimisation and harmonic frequencies in continuum solvent

*Jaguar input, submission and output, on 1,4-benzoquinone; what changes for AQDS, TEMPO and the indigo family*

Session 1 ended with a list of states, each with a charge and a multiplicity. Session 3 needs one Gibbs energy G per state, at a geometry that is a true minimum. This session produces and checks those numbers. You write Jaguar inputs, check them before they cost compute time, submit them from PowerShell or the VS Code terminal, and read the output line by line until you can rebuild G by hand. A gas-phase frequency calculation is then compared with the experimental IR spectrum, which is the only point in this course where a computed number meets a measured one directly.

The session is hands-on throughout: every step is done together, in pairs, on the files of this folder.

## Learning goals

1. Explain every keyword of a Jaguar optimisation + frequency input and name what it controls physically.
2. Find a wrong charge or multiplicity in an input before submitting it, and explain why an electron count alone does not catch every error.
3. Submit, monitor and retrieve a Jaguar job from the command line.
4. Decide from the output whether a structure is a minimum: convergence criteria, 3N−6 frequencies, no imaginary mode, ⟨S²⟩ for radicals.
5. Rebuild G from E, ZPE and the thermal table; state the approximations behind it (quasi-harmonic, ideal gas at 1 atm, symmetry number) and correct to 1 mol/L.
6. Compare scaled harmonic frequencies with a gas-phase IR spectrum and judge what agreement means.

## Files

| file | used in |
|---|---|
| `worksheet.md` | predictions and results, filled in during the session |
| `inputs/states.csv` | A, B: charge and multiplicity of every job of the course |
| `inputs/bq/` | A, C: benzoquinone states at the production level, B3LYP-D3/def2-TZVPD in PBF water; `_b3lyp` without D3 |
| `inputs/live/bq_Q_pbe.in`, `bq_QH2_pbe.in` | B: the jobs submitted during the session (PBE/LACVP++\*\*, PBF water) |
| `inputs/groups/` | A4, B4: one input per group with `molchg=??` and `multip=??` |
| `inputs/broken/` | A3: three inputs with an error each |
| `inputs/gas/` | D: gas-phase Q and QH₂ for the IR comparison |
| `inputs/checks/` | D4: one-factor checks of the soft modes |
| `inputs/aqds/`, `inputs/tempo/`, `inputs/indigo/` | E and homework: the other redox families at the production level |
| `scripts/check_inputs.py` | A3, A4: electron count, multiplicity parity, comparison with `states.csv` |
| `scripts/summarise_job.py` | C: the lines of a Jaguar output that decide whether a result is usable, and G rebuilt by hand |
| `scripts/ir_compare.py` | D: computed against experimental IR, with a scale factor; optional plot |
| `commands.ps1` (Windows), `commands.sh` (Linux) | B, C, D: every command of the session |

The scripts need only Python 3 with `numpy` (and `matplotlib` for the plot); they run with the suite's Python, `& "$S\run" scripts\<name>.py ...`, or any Python with those packages. Reference outputs of the production jobs are handed out by the instructor at the start of section C; they are not in the repository.

## Before the session

1. On the Windows workstation, in PowerShell: `$S = "C:\Program Files\Schrodinger2026-2"` and `$env:SCHRODINGER = $S` (without the second line `jsc hosts list` stops with "$SCHRODINGER must be defined"). Then `& "$S\jsc" hosts list` shows the compute hosts besides `localhost` (Session 1, B2). Write one down: it replaces `<host>` in every command below.
2. `& "$S\jsc" cert get <server>:<port>` has been run once (Session 1, Before the session, item 4).
3. Either PowerShell or the VS Code terminal opens in `C:\schrodinger-tutorials-redox\02-optimisation-and-frequencies`. In VS Code: File > Open Folder > the repository, then Terminal > New Terminal (PowerShell is the default shell on Windows).
4. `& "$S\run" scripts\check_inputs.py inputs\bq` prints one `ok` line per input.

## Time plan

| time | part | what you do |
|---|---|---|
| 0:00 | 0 · Goal | from states to G; what makes a G usable |
| 0:10 | A · The input | read `bq_Q.in` keyword by keyword; fix three broken inputs; fill in your group's input |
| 0:35 | B · Submit | submit the live job and your group's job; monitor them |
| 0:50 | C · The output | read a finished output while the live jobs run; rebuild G |
| 1:25 | D · IR spectrum | scale, compare with the NIST gas-phase spectrum, judge the agreement |
| 1:45 | E · Other molecules | what changes for AQDS, TEMPO and indigo |
| 1:55 | Homework | |

## 0 · Goal (10 min)

For each state $i$ of Session 1 this session gives

$$G_i = E_\mathrm{el} + E_\mathrm{ZPE} + G_\mathrm{thermal}(298.15\ \mathrm{K}, 1\ \mathrm{atm}) + 1.89\ \mathrm{kcal/mol}$$

with $E_\mathrm{el}$ the electronic energy in PBF water at the optimised geometry, and $1.89 = RT\ln(24.46)$ kcal/mol the change of standard state from 1 atm to 1 mol/L. A G is usable only if

- the charge and multiplicity are those of the intended state (A),
- the geometry optimisation converged (C1),
- the structure is a minimum: 3N−6 real frequencies (C2),
- for a radical, the wavefunction is a doublet and not a mixture: ⟨S²⟩ close to 0.75 (C3),
- the lowest-G conformer was found, or the conformers were weighted (C5).

Two energies in Session 3 enter a pKa or a potential as differences. An error of 1.36 kcal/mol in one G moves a pKa by one unit; 23.06 kcal/mol is 1 V per electron.

## A · The input (25 min)

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

Not in the input, but set by default (Jaguar 13.2, `jaguar_keywords.xml`): `iuhf=2`, spin-unrestricted when `multip` > 1 and restricted otherwise; pseudospectral integrals (`nops=0`); and in solvent, convergence criteria three times looser than in the gas phase (output line *Scaling standard convergence criteria by a factor of 3.00*). There are no k-points: a molecule is not periodic, and there are no periodic images to correct for when it is charged.

**A2 · Why these choices.** Discuss before going on: why diffuse functions (the anions QH⁻ and Q²⁻, whose outer electrons are weakly bound); why D3, and whether it can matter for a single small molecule (compare `bq_QH2.out` and `bq_QH2_b3lyp.out` in C: the lowest frequency changes from 252.9 to 252.7 cm⁻¹); why optimise in water rather than in the gas phase (anions change geometry in solvent, and the course uses one geometry per state, as in Session 1). PBE/LACVP++\*\* in `inputs/live/` is a cheaper level for the live job only; its numbers are not used in Session 3.

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

## B · Submit (15 min)

See `commands.ps1`, sections B1 to B4; the Linux equivalents are in `commands.sh`.

**B1 · Host.** `& "$S\jsc" hosts list`. Use a compute host, not `localhost`. The jobs are run by the job servers on rs4, rs5 and rs6 (`rs4.differ.nl:8030` etc., `& "$S\jsc" server-info rs4.differ.nl:8030`), 32 cores each; the reference jobs ran with `-HOST cpurs4` and `-HOST cpurs6`. A job that fails at once with `srun: executable file not found` hit a bad node: submit it again.

**B2 · Live job.** Each pair submits one of the two live inputs, so that both are running:

```powershell
& "$S\jaguar" run inputs\live\bq_Q_pbe.in -HOST <host> -PARALLEL 4
```

The command returns at once with a job ID; the output comes back to the folder you submitted from when the job ends. Do not submit the same file twice: the second job overwrites the first one's output.

**B3 · Monitor.**

```powershell
& "$S\jsc" list
& "$S\jsc" tail-file --name bq_Q_pbe.log <jobid>
```

The `.log` shows the SCF and geometry iterations as they happen; the `.out` is complete only at the end.

**B4 · Group job.** Submit your group's input from A4 the same way. These are larger molecules; they will not finish during the session. You will read them in the homework.

## C · The output (35 min)

While the live jobs run, work on the finished production output `bq_Q.out` (B3LYP-D3/def2-TZVPD, PBF water), handed out by the instructor. First the summary:

```powershell
& "$S\run" scripts\summarise_job.py reference\bq_Q.out
```

then find each line of the summary in the `.out` yourself (search in VS Code with Ctrl+F).

**C1 · Did the optimisation converge?** Search `Geometry optimization complete`. Just above it, the last step:

```
  energy change:          -1.2264E-04 *  (  1.5000E-04 )
  gradient maximum:        7.4724E-04 *  (  1.3500E-03 )
  gradient rms:            2.4496E-04 *  (  9.0000E-04 )
  displacement maximum:    1.9324E-03 *  (  5.4000E-03 )
  displacement rms:        7.8163E-04 *  (  3.6000E-03 )
```

Each value is compared with the threshold in brackets (hartree, hartree/bohr, bohr); `*` marks a criterion that is met. In solvent Jaguar uses three times the gas-phase thresholds by default (`Scaling standard convergence criteria by a factor of 3.00`). 4.5 × 10⁻⁴ Eh/bohr, the gas-phase maximum gradient, is 0.023 eV/Å: compare with a typical VASP `EDIFFG = −0.02`.

*Expected:* 9 geometry steps (count the `SCFE:` lines), all five criteria met.

**C2 · Is it a minimum?** Search `Number of imaginary frequencies`.

*Expected:* 30 frequencies for 12 atoms (3N − 6), 0 imaginary, the lowest 232.7 cm⁻¹ (B3u, the out-of-plane ring bend). A saddle point found by an optimisation means the symmetry or the starting structure was wrong; displace along the imaginary mode and reoptimise.

**C3 · Radicals.** In a radical output (`bq_QHrad.out`), search `<S**2>`. A pure doublet has S(S+1) = 0.75.

*Expected:* 0.754. As a rule of thumb, a value well above 0.75 (more than about 10 %) means spin contamination: the energy is no longer that of a doublet. The thermal table has an `elec.` row with S = R ln 2 = 1.377 cal/(mol K) for a doublet.

**C4 · Rebuild G by hand.** From the end of `bq_Q.out`:

| line | value |
|---|---|
| final `SCFE: Solution phase energy` | −381.625370 Eh |
| `The zero point energy (ZPE)` | 54.567 kcal/mol |
| `total` row, G column (without ZPE) | −17.758 kcal/mol |
| `Total Gibbs free energy, Gtot` | −381.566711 Eh |

Compute $E + (\mathrm{ZPE} + G_\mathrm{table})/627.5095$ and compare with Gtot (the last line of `summarise_job.py` does the same).

*Expected:* the same value to 0.001 kcal/mol. Gtot already contains the ZPE; it is at 1 atm, so +1.89 kcal/mol is still to be added for 1 mol/L.

Then read the three lines above the vibrational temperatures:

```
  The Quasi-Harmonic approximation will be applied to compute
  vibrational constributions to thermodynamic properties.
  Frequencies will be adjusted to a minimum value of  100.00 cm^-1.
```

Jaguar 2026-2 treats every mode below 100 cm⁻¹ as if it were at 100 cm⁻¹ when it computes the vibrational entropy (a correction of the Session 1 slides, which say harmonic). Low modes give the largest entropy and are the least harmonic; this avoids an entropy that grows without bound as a frequency goes to zero. Benzoquinone has no mode below 100 cm⁻¹, so here it changes nothing; for TEMPO's methyl rotors and the sulfonate rotations of AQDS it does. Finally `rotational symmetry number: 4` (D2h): σ enters the rotational entropy as −R ln σ. Do not also count symmetry-equivalent structures by hand.

**C5 · Two conformers of QH₂.** `bq_QH2.out` (trans O–H, C2h) and `bq_QH2cis.out` (cis, C2v):

*Expected:* Gtot −382.794292 and −382.793832 Eh, ΔG = 0.29 kcal/mol in favour of trans. With $p_i \propto e^{-G_i/RT}$: 62 % trans, 38 % cis. Is this difference larger than the error of the method? Which G goes into Session 3?

**C6 · The live job.** When `bq_Q_pbe.out` is back, run `summarise_job.py` on it and compare with `bq_Q.out`: geometry steps, lowest frequency, wall time, smallest eigenvalue of the overlap matrix S.

*Expected:* the instructor fills in the PBE numbers after the Thursday test run.

## D · IR spectrum (20 min)

Harmonic frequencies are the curvature of the potential at the minimum; measured bands are anharmonic fundamentals and lie a few per cent lower. A scale factor fitted per method and basis absorbs most of this, on average.

**D1 · Experimental spectrum.** Download the NIST gas-phase IR spectrum of 1,4-benzoquinone (commands D1). It is NIST Standard Reference Data: use it in class, do not redistribute it.

**D2 · Compare.**

```powershell
& "$S\run" scripts\ir_compare.py reference\bq_Q.out --scale 0.9626 --exp results\bq_Q_nist.jdx --plot results\bq_Q_ir.pdf
```

0.9626 is the NIST CCCBDB factor for B3LYP/def2-TZVPP, the closest available to def2-TZVPD; for PBE use 0.9879 (PBEPBE/def2-TZVPP).

*Expected* (production output `bq_Q.out`, PBF water, against the gas-phase spectrum):

| experiment (cm⁻¹) | rel. | calc., scaled | mode | difference |
|---|---|---|---|---|
| 1678 | 1.00 | 1659 | B1u, C=O stretch | −19 |
| 1302 | 0.23 | 1306 | B2u | +4 |
| 1070 | 0.15 | 1079 | B2u | +9 |
| 882 | 0.31 | 918 | B3u, C–H out of plane | +36 |

**D3 · Judge the agreement.** Two effects are mixed here: `bq_Q.out` is in water, the spectrum in the gas phase. Predict in which direction solvent shifts the C=O stretch, then check it with the gas-phase job `inputs/gas/bq_Q_gas.in` (commands D3; output from the instructor). The C=O band and the in-plane modes agree to about 1 %; the out-of-plane band at 882 cm⁻¹ does not (+4 %). The tabulated fundamentals (NIST CCCBDB, assignment of Anno, *J. Chem. Phys.* 42, 932 (1965)) make it sharper: the lowest out-of-plane modes are 109 cm⁻¹ (B3u) and 241 cm⁻¹ (B2g), computed 232.7 and 349.4 cm⁻¹. A scale factor cannot fix an error that differs between modes. Note also what the comparison assumes: that the 1965 assignment of these weak low bands is right.

**D4 · Find the cause, one factor at a time** (exercise; instructor-run if time is short). The candidates are the method (B3LYP-D3) and the numerics. Each input in `inputs/checks/` changes one thing relative to `inputs/gas/bq_Q_gas.in`:

| input | change | tests |
|---|---|---|
| `bq_Q_gas_nops.in` | `nops=1` | pseudospectral integrals with a diffuse basis |
| `bq_Q_gas_grid.in` | `iacc=1`, `rmscp=1.0e-6` | DFT grids and CPHF convergence |
| `bq_Q_gas_tzvp.in` | `basis=def2-TZVP` | diffuse functions (smallest eigenvalue of S: 8 × 10⁻⁷, near-linear dependence) |

Predict which one moves the B3u mode, then compare the results with the instructor's. If none of them does, the error is in the functional and is part of the uncertainty of every G that contains a soft mode.

## E · What changes for the other molecules (10 min)

| family | what to watch |
|---|---|
| **AQDS** (anthraquinone-2,7-disulfonate) | Charges −2 to −4: diffuse functions and solvent are essential; a gas-phase calculation of the −3 and −4 ions is meaningless (UNVERIFIED for this molecule: the extra electrons may not be bound without solvent). Each SO₃⁻ group can rotate: all inputs here start from the same orientation (one O of each group perpendicular to the ring, on opposite faces); a different orientation is a different conformer, with a different G. 30 atoms with three-row S atoms: expect at least the 6.7 h of TEMPO-H (30 atoms, `tp_TH.out`) per job. |
| **TEMPO** | The radical is the stable form: check ⟨S²⟩. The ring is puckered (Cs), and the four methyl groups give soft rotor modes, where the quasi-harmonic treatment matters. TEMPO⁻ (`tp_Tm.in`, the aminoxide anion) completes the grid. 6.7 h (`tp_TH.out`) to 7.7 h (`tp_TH2p.out`) per job. |
| **Indigo family** | Dehydroindigo → indigo → leucoindigo adds 2 H and 2 e⁻ at each step. Intramolecular N–H···O=C hydrogen bonds fix the trans (anti) form of indigo; leucoindigo can rotate about the central C–C bond: `di_Lm` and `di_LH3rad` start syn, the others anti, so compare both. Dehydroindigo has a small HOMO–LUMO gap (2.55 eV, `di_D.out`, HOMO and LUMO energies): check the stability of the closed-shell solution. Its smallest overlap eigenvalue is negative (−1.5 × 10⁻⁸): def2-TZVPD is numerically linearly dependent for this molecule, and the basis should be checked before production. About 23 h per job. |

## Homework

1. Read your group's output from B4 with `summarise_job.py`: converged? minimum? ⟨S²⟩? Rebuild G by hand as in C4 and add 1.89 kcal/mol.
2. The live PBE job against the production job: which numbers change by more than 1 kcal/mol, and which would matter for a pKa?
3. The worksheet questions of D3 and E.
4. Write five lines on what surprised you and what is unclear, in the worksheet.
