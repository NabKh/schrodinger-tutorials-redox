# Session 2 · worksheet

Fill in the predictions before running anything, then the observations.

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

**S5.** The input you wrote from the Maestro panel (gear > Write) against `results\made\bq_QHm.in`: which lines differ, and does `check_inputs.py` pass it?

## L · Level of theory

**L2 · Ladder** (Q, gas phase). Prediction first: which rung changes r(C=O) most?

| rung | level | r(C=O) (Å) | ν(C=O), harmonic (cm⁻¹) | lowest B3u (cm⁻¹) | wall time |
|---|---|---|---|---|---|
| 1 | PBE/6-31G\*\* | | | | |
| 2 | B3LYP/6-31G\*\* | | | | |
| 3 | B3LYP-D3/def2-TZVP | | | | |
| 4 | B3LYP-D3/def2-TZVPD | | | | |
| 5 | M06-2X-D3/def2-TZVPD | | | | |
| 6 | ωB97X-D/def2-TZVPD | | | | |
| exp. | | | 1678 | 109 | |

**L4 · Solvation** (single points at the PBF geometries; kcal/mol unless stated).

| model | E(Q) (Eh) | E(Q²⁻) (Eh) | ΔG_solv(Q) | ΔG_solv(Q²⁻) | ΔE(Q → Q²⁻) |
|---|---|---|---|---|---|
| gas | | | 0 | 0 | |
| PBF | | | | | |
| SMD | | | | | |
| C-PCM | | | | | |

Spread of ΔE(Q → Q²⁻) across the three models: ______ kcal/mol = ______ V for the 2e⁻ step. Is this larger or smaller than the D3 effect of L1?

**L6.** In one sentence each: which rung would you stop at for benzoquinone, and what would make you go higher for indigo?

## A · The input

**A1.** For each keyword, one line in your own words: what does it change physically?

| keyword | what it does | what happens if it is missing |
|---|---|---|
| `dftname` | | |
| `basis` | | |
| `isolv`, `solvent` | | |
| `igeopt` | | |
| `ifreq` | | |
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

## B · Submit

| job | job ID | host | submitted at | finished at |
|---|---|---|---|---|
| `bq_Q_pbe` or `bq_QH2_pbe` | | | | |
| group job | | | | |

## C · The output (`bq_Q.out`)

| quantity | prediction | from the output | line number |
|---|---|---|---|
| geometry steps | | | |
| all five convergence criteria met? | | | |
| number of frequencies (3N − 6) | | | |
| imaginary frequencies | | | |
| lowest frequency (cm⁻¹) and symmetry | | | |
| ⟨S²⟩ of `bq_QHrad` | | | |
| rotational symmetry number σ | | | |
| final E (Eh) | | | |
| ZPE (kcal/mol) | | | |
| G_thermal from the `total` row (kcal/mol) | | | |
| G rebuilt by hand (Eh) | | | |
| Gtot printed (Eh) | | | |
| G at 1 mol/L (Eh) | | | |

**C4.** Benzoquinone has no mode below 100 cm⁻¹. Name a molecule of this course where the quasi-harmonic floor will change G, and say why.

**C5 · QH₂ conformers.**

| | Gtot (Eh) | ΔG (kcal/mol) | population at 298 K |
|---|---|---|---|
| trans (`bq_QH2`) | | 0 | |
| cis (`bq_QH2cis`) | | | |

Is ΔG larger than the error of the method? Which G goes into Session 3, and why?

**C6 · Live job against production.**

| quantity | PBE/LACVP++\*\* (live) | B3LYP-D3/def2-TZVPD |
|---|---|---|
| geometry steps | | 9 |
| lowest frequency (cm⁻¹) | | 232.7 |
| wall time (h) | | 1.12 |

## D · IR spectrum

| experiment (cm⁻¹) | assignment | calc., harmonic | calc., scaled | difference (cm⁻¹) | difference (%) |
|---|---|---|---|---|---|
| 1678 | C=O stretch | | | | |
| 1302 | | | | | |
| 1070 | | | | | |
| 882 | C–H out of plane | | | | |

**D3.** Prediction: does solvent raise or lower the C=O stretch, and why? Result from the gas-phase job:

**D4.** Which of the three checks do you expect to move the lowest B3u mode? Why?

| check | prediction | lowest B3u (cm⁻¹) | 882 band, scaled (cm⁻¹) |
|---|---|---|---|
| baseline (`bq_Q_gas`) | | | |
| `nops=1` | | | |
| `iacc=1`, `rmscp=1.0e-6` | | | |
| def2-TZVP | | | |

## E · Other molecules

For your group's molecule: one thing that can make its G unusable, and how you would detect it in the output.

## Five lines

What surprised you, and what is unclear?
