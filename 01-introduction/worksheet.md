# Session 1 · worksheet

Fill in the predictions before running anything, then the observations.

## 0 · States of 1,4-benzoquinone on the proton-electron grid

Counted from the neutral quinone Q: $n_\mathrm{H}$ protons and $n_e$ electrons added.

| state | $n_\mathrm{H}$ | $n_e$ | charge | electrons | multiplicity |
|---|---|---|---|---|---|
| Q | 0 | 0 | | | |
| QH⁺ | 1 | 0 | | | |
| QH• | 1 | 1 | | | |
| Q•⁻ | 0 | 1 | | | |
| QH₂ | 2 | 2 | | | |
| QH⁻ | 1 | 2 | | | |
| Q²⁻ | 0 | 2 | | | |

Which of these states can Epik reach when it starts from QH₂? Which can it not, and why?

## A · Project Table after import and after LigPrep

| entry | formula after import | charge after import | formula after LigPrep | charge after LigPrep |
|---|---|---|---|---|
| bq_Q | | | | |
| bq_QH2 | | | | |
| bq_QHm | | | | |
| bq_Q2m | | | | |
| bq_QHrad | | | not passed through LigPrep | |
| bq_Qradm | | | not passed through LigPrep | |

Did any entry change? If so, which LigPrep option caused it?

## B · Command line

Output of `scripts/check_structures.py results/bq_prepped.maegz results/bq_radicals.mae` (electron count and multiplicity per entry):

```



```

## C · Epik on QH₂

| run | settings | states predicted | states observed | charges observed | electron count |
|---|---|---|---|---|---|
| 1 | defaults (pH 7.4 ± 2.0) | | | | |
| 2 | pH 7.0 ± 7.0 | | | | |
| 3 | pH 12.0 ± 2.0 | | | | |

Compare your three runs with the two columns of section 2 of `session1-notebook.ipynb`. Which reading of the pH window does your release follow: a population threshold at the target pH, or states populated anywhere in the window?

## Five lines for the start of Session 2

What surprised you, and what is still unclear?

1.
2.
3.
4.
5.

## Homework · phenazine

Which cells of the proton-electron grid are populated between pH 0 and 14?

| state | SMILES | $n_\mathrm{H}$ | $n_e$ | charge | multiplicity |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

Epik on dihydrophenazine (`phz_PH2`), default and wide settings: states and charges returned.
