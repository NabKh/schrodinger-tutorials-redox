# Molecular modelling and DFT with the Schrödinger suite

*A hands-on course with Maestro, LigPrep, Epik, Jaguar and the Python API*

Five sessions on preparing structures in Maestro and LigPrep, predicting protonation
states with Epik, running and reading DFT calculations with Jaguar, deriving properties from them, and automating the work with
the Python API and the command line. The worked example is 1,4-benzoquinone, a redox-active
molecule whose experimental reduction potential and pKa values are known, so results can be checked
against experiment.

The material is written for MSc and PhD students and researchers who are new to Schrödinger and to DFT.

## Sessions

| session | title | content | folder | status |
|---|---|---|---|---|
| 1 | Introduction: redox chemistry, DFT and the Schrödinger suite | The states of 1,4-benzoquinone, the DFT background, Maestro, LigPrep and Epik | [`01-introduction/`](01-introduction/) | available |
| 2 | Geometry optimisation and harmonic frequencies in continuum solvent | Jaguar calculations on Q and QH₂; comparison with the experimental IR spectrum | [`02-optimisation-and-frequencies/`](02-optimisation-and-frequencies/) | in preparation |
| 3 | pKa values and reduction potentials from computed Gibbs energies | Thermodynamic cycles, reference constants and the E(pH) line of 1,4-benzoquinone | [`03-pka-and-reduction-potentials/`](03-pka-and-reduction-potentials/) | in preparation |
| 4 | Automating the calculations with the Schrödinger Python API | Structure preparation, Jaguar jobs and analysis as scripts | [`04-python-api/`](04-python-api/) | in preparation |
| 5 | Microstate enumeration and E-pH diagrams of new molecules | Epik and Jaguar at each redox level; macroscopic pKa values from microstates | [`05-microstates-and-e-ph-diagrams/`](05-microstates-and-e-ph-diagrams/) | in preparation |

Each session builds on the previous one.

## How to use this repository

Each session has its own folder. During a session you follow the slides and do the hands-on steps with the files of that folder:

```
NN-session/
  README.md           the hands-on steps, with slide numbers, commands and expected results
  sessionN-slides.pdf the slides
  worksheet.md        tables for your predictions and results
  inputs/             input structures
  scripts/            scripts run during the session
  commands.ps1        every command of the session (Windows PowerShell); commands.sh for Linux
  *.ipynb             notebook with the calculations of the session
```

Your own outputs go into a folder `results/` inside the session folder; git ignores it. The material of each session is added after the session has been taught.

## Requirements

- A licensed Schrödinger installation with Maestro, LigPrep, Epik and Jaguar.
  The instructions were written for release 2026-2; menu entries and option names can
  differ in other releases.
- Windows PowerShell or a Linux shell for the command-line steps (`commands.ps1` and `commands.sh`).
- For the notebooks: Python 3 with `numpy`, `matplotlib`, `rdkit` and `jupyter`
  (`pip install -r requirements.txt`). The notebooks do not need a Schrödinger licence.
- Access to a compute host for Jaguar jobs (from Session 2 on). Small LigPrep and Epik jobs
  can run on a workstation.

## Getting started

```powershell
git clone https://github.com/NabKh/schrodinger-tutorials-redox.git C:\schrodinger-tutorials-redox
```

Or use Code > Download ZIP, extract it to `C:\` and rename the folder `schrodinger-tutorials-redox-main` to `schrodinger-tutorials-redox`, so the paths in the instructions work.

Work in a folder on a local disk. Schrödinger job control can be unreliable on network drives.
Then open `01-introduction/README.md`.

## Conventions

| key | state | $n_\mathrm{H}$ | $n_e$ | charge | multiplicity |
|---|---|---|---|---|---|
| `Q` | quinone (oxidised) | 0 | 0 | 0 | 1 |
| `Qradm` | semiquinone radical anion, Q•⁻ | 0 | 1 | −1 | 2 |
| `QHrad` | neutral semiquinone radical, QH• | 1 | 1 | 0 | 2 |
| `QH2` | hydroquinone (reduced) | 2 | 2 | 0 | 1 |
| `QHm` | monoanion, QH⁻ | 1 | 2 | −1 | 1 |
| `Q2m` | dianion, Q²⁻ | 0 | 2 | −2 | 1 |

$n_\mathrm{H}$ and $n_e$ are counted relative to the neutral quinone Q. The protonated quinone QH⁺ has a pKa
far below 0 and is not used.
File and job names follow `bq_<state>_<step>`, for example `bq_QH2_epik_wide`.

## Main references

- T. Gaudin and J.-M. Aubry, "Prediction of Pourbaix diagrams of quinones for redox flow battery
  by COSMO-RS", *J. Energy Storage* **49**, 104152 (2022). COSMO-RS Pourbaix diagrams of quinones,
  with compiled experimental $E^\circ$ and pKa values.
- R. C. Johnston et al., *J. Chem. Theory Comput.* **19**, 2380 (2023). Epik 7.
- J. Ho and M. L. Coote, *WIREs Comput. Mol. Sci.* **1**, 649 (2011). First-principles prediction of
  acidities in the gas and solution phase.
- NIST Chemistry WebBook, SRD 69: infrared spectrum of 1,4-benzoquinone (CAS 106-51-4).
- P. Hohenberg and W. Kohn, *Phys. Rev.* **136**, B864 (1964); W. Kohn and L. J. Sham, *Phys. Rev.*
  **140**, A1133 (1965). The foundations of DFT.
- J. P. Perdew and K. Schmidt, *AIP Conf. Proc.* **577**, 1 (2001). Jacob's ladder of functionals.
- A. D. Becke, *J. Chem. Phys.* **98**, 5648 (1993); P. J. Stephens et al., *J. Phys. Chem.* **98**,
  11623 (1994). B3LYP.
- F. Weigend and R. Ahlrichs, *Phys. Chem. Chem. Phys.* **7**, 3297 (2005). def2 basis sets.
- S. Grimme et al., *J. Chem. Phys.* **132**, 154104 (2010). D3 dispersion correction.

## Disclaimer

This is independent teaching material. It is not affiliated with or endorsed by Schrödinger, Inc.
Schrödinger, Maestro, LigPrep, Epik and Jaguar are names of Schrödinger, Inc. software; a valid
licence is needed to run them. Menu paths and options can change between releases; when they
differ from what is written here, the documentation of your release is authoritative.

## Author

Nabil Khossossi, Dutch Institute for Fundamental Energy Research (DIFFER), Eindhoven.
Corrections and suggestions are welcome through GitHub issues.
