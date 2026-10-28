# Session 2 · worksheet

Fill in the predictions before running anything, then the observations. Every number that is not a prediction comes from an output on the workstation: in the session (B) or from the instructor's test run (P).

## 0 · Goal

Your five lines from Session 1, read out at the start: which one matters for today?

## S · From one molecule to all its states

**S1.** Fill in before running `make_inputs.py`, then compare with its output.

| state | job | parent | H removed | formula | electrons | `molchg` | `multip` |
|---|---|---|---|---|---|---|---|
| Q | `bq_Q` | | | | | | |
| Q•⁻ | `bq_Qradm` | | | | | | |
| QH• | `bq_QHrad` | | | | | | |
| QH⁻ | `bq_QHm` | | | | | | |
| QH₂ | `bq_QH2` | | | | | | |
| Q²⁻ | `bq_Q2m` | | | | | | |

Why is Q²⁻ made from QH₂ and not from Q, although it has the same atoms as Q?

**S7 · The other families.** Before running: atoms, N, `molchg`, `multip` of each state of your family, from the recipe.

| job | atoms | N | `molchg` | `multip` | open or closed shell |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

After running: For your group's family, from the `check_inputs.py` output: which states are open shell, and which two states have the same atoms but different N?

**S5.** The input you wrote from the Maestro panel (gear > Write) against `results\made\bq_QHm.in`: which lines differ, and does `check_inputs.py` pass it?

## L · Level of theory

**L1 · Which effect matters for a difference?** Prediction first: does D3 or solvation change ΔG(Q → QH₂) more?

| effect | what is compared | shift (kcal/mol) | for the 2e⁻ step (V) |
|---|---|---|---|
| D3 dispersion | `bq_Q` − `bq_Q_b3lyp`, Gtot | | |
| D3 dispersion | `bq_QH2` − `bq_QH2_b3lyp`, Gtot | | |
| D3 dispersion | `bq_QH2cis` − `bq_QH2cis_b3lyp`, Gtot | | |
| D3, on the step | change of ΔG(Q → QH₂) | | |
| solvation | 5 % of ΔG_solv(Q²⁻) from L4a | | |

**L2 · Ladder** (Q, gas phase). Prediction first: which rung changes r(C=O) most?

| rung | level | r(C=O) (Å) | ν(C=O), harmonic (cm⁻¹) | lowest out-of-plane mode (cm⁻¹, label in output) | wall time |
|---|---|---|---|---|---|
| 1 | PBE/6-31G\*\* | | | | |
| 2 | B3LYP/6-31G\*\* | | | | |
| 3 | B3LYP-D3/def2-TZVP | | | | |
| 4 | B3LYP-D3/def2-TZVPD | | | | |
| 5 | M06-2X-D3/def2-TZVPD | | | | |
| 6 | ωB97X-D/def2-TZVPD | | | | |
| exp. | | | 1668 (fundamental; band maximum 1678) | 109 | |

**L4a · Solvation** (single points at the optimised PBF geometries of `bq_Q` and `bq_Q2m`; kcal/mol unless stated).

| model | E(Q) (Eh) | E(Q²⁻) (Eh) | ΔG_solv(Q) | ΔG_solv(Q²⁻) | ΔE(Q → Q²⁻) |
|---|---|---|---|---|---|
| gas | | | 0 | 0 | |
| PBF | | | | | |
| SMD | | | | | |
| C-PCM | | | | | |

PBF single points against the final `SCFE` of `bq_Q.out` / `bq_Q2m.out`: ______ / ______ Eh. ΔG_solv against the printed `Solvation energy` line: ______ / ______. Gas-phase HOMO of Q²⁻: ______ eV.

Spread of ΔE(Q → Q²⁻) across the three models: ______ kcal/mol = ______ V for the 2e⁻ step. Is this larger or smaller than the D3 effect of L1?

**L6.** In one sentence each: which rung would you stop at for benzoquinone, and what would make you go higher for indigo?

## A · The input

**A1.** For each keyword, one line in your own words: what does it change physically?

| keyword | what it does | what happens if it is missing |
|---|---|---|
| `dftname` | | |
| `basis` | | |
| `isolv`, `solvent` | | |
| `nogas` | | |
| `igeopt` | | |
| `maxitg` | | |
| `ifreq` | | |
| `irder` | | |
| `molchg` | | |
| `multip` | | |

**A3 · Broken inputs.** Prediction from the `&gen` section, then the result of `check_inputs.py`.

| file | predicted error | caught by parity? | caught by `states.csv`? |
|---|---|---|---|
| `broken/bq_Qradm.in` | | | |
| `broken/bq_QHm.in` | | | |
| `broken/bq_Q2m.in` | | | |

Why does an electron count catch a wrong spin but not every wrong charge?

**A4 · Your group's input.**

| file | molchg | multip | number of electrons | open or closed shell |
|---|---|---|---|---|
| | | | | |

Decided before opening `states.csv`? Yes / no. If `multip` > 1: `iuhf=1` added?

## B · Submit

| job | job ID | host | submitted at | finished at |
|---|---|---|---|---|
| `bq_Q_pbe` or `bq_QH2_pbe` | | | | |
| ladder or solvation job (B5) | | | | |

## C · The output (`bq_Q.out`)

| quantity | prediction | from the output | line number |
|---|---|---|---|
| last geometry step (and number of `SCFE` lines) | | | |
| scaling factor of the convergence criteria in solvent | | | |
| all five convergence criteria met? | | | |
| number of frequencies (3N − 6) | | | |
| imaginary frequencies | | | |
| lowest frequency (cm⁻¹) and symmetry | | | |
| ⟨S²⟩ of `bq_QHrad` | | | |
| point group used | | | |
| smallest eigenvalue of S | | | |
| rotational symmetry number σ | | | |
| final E (Eh) | | | |
| quasi-harmonic floor (cm⁻¹) | | | |
| ZPE (kcal/mol) | | | |
| G_thermal from the `total` row (kcal/mol) | | | |
| G rebuilt by hand (Eh) | | | |
| Gtot printed (Eh) | | | |
| G at 1 mol/L (Eh), + 1.89 kcal/mol | | | |

**C4.** Is any mode of `bq_Q` below the quasi-harmonic floor? What kind of motion would produce such a mode, and what would the floor then change in G: the enthalpy, the entropy, or both?

**C5 · QH₂ conformers.**

| | Gtot (Eh) | ΔG (kcal/mol) | population at 298 K |
|---|---|---|---|
| trans (`bq_QH2`) | | 0 | |
| cis (`bq_QH2cis`) | | | |

G of QH₂ as a mixture, $-RT \ln \sum_i e^{-G_i/RT}$ (RT = 0.592 kcal/mol): ______ Eh.

Is ΔG larger than the error of the method? Which G goes into Session 3, and why?

**C6 · Live job against production.**

| quantity | PBE/LACVP++\*\* (live) | B3LYP-D3/def2-TZVPD |
|---|---|---|
| geometry steps | | |
| lowest frequency (cm⁻¹) | | |
| wall time (h) | | |
| smallest eigenvalue of S | | |

## D · IR spectrum

Scale factor used: ______ (± ______).

| experiment (cm⁻¹) | assignment | mode (index) | calc., harmonic | calc., scaled | difference (cm⁻¹) | difference (%) |
|---|---|---|---|---|---|---|
| 1678 (band maximum; fundamental 1668) | C=O stretch | | | | | |
| 1302 | | | | | | |
| 1070 / 1054 | | | | | | |
| 882 | C–H out of plane | | | | | |

Is every match confirmed by the displacement of the mode in Maestro? Which?

**D3.** Prediction: does solvent raise or lower the C=O stretch, and why? Result from the gas-phase job: C=O in water ______, in the gas phase ______ cm⁻¹.

The two lowest out-of-plane modes, computed: ______ and ______ cm⁻¹ (tabulated 109 and 241 cm⁻¹; 241 is IR-inactive). Which motion is each, from the displacement?

**D4.** Which of the four checks do you expect to move the lowest out-of-plane mode? Why?

| check | prediction | lowest out-of-plane mode (cm⁻¹, label in output) | 882 band, scaled (cm⁻¹) | smallest eigenvalue of S |
|---|---|---|---|
| baseline (`bq_Q_gas`) | | | | |
| `nops=1` | | | | |
| `iacc=1` | | | | |
| `rmscp=1.0e-6` | | | | |
| def2-TZVP | | | | |

## E · Other molecules

For your group's molecule: one thing that can make its G unusable, and how you would detect it in the output.

## Five lines

What surprised you, and what is unclear?
