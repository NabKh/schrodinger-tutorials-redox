#!/usr/bin/env bash
# Session 1 · commands for sections B and C (Linux, bash)
# Run one block at a time from the folder 01-introduction.
# Adjust SCHRODINGER to your installation path. Same steps as commands.ps1.

# ---------------------------------------------------------------------------
# B1 · the suite by its full installation path
export SCHRODINGER=/opt/schrodinger2026-2
cd ~/schrodinger-tutorials-redox/01-introduction
mkdir -p results   # outputs of this session go here
"$SCHRODINGER/run" python3 -c "print('suite OK')"
# if command-line jobs cannot connect: "$SCHRODINGER/jsc" local-server-start

# ---------------------------------------------------------------------------
# B2 · hosts and jobs
# once per user: "$SCHRODINGER/jsc" cert get <server>:<port>
"$SCHRODINGER/jsc" hosts list
"$SCHRODINGER/jsc" list

# ---------------------------------------------------------------------------
# B3 · LigPrep without changing the ionisation state
"$SCHRODINGER/ligprep" -ismi inputs/bq_closed_shell.smi -omae results/bq_prepped.maegz \
    -i 0 -nt -s 1 -NJOBS 1 -WAIT
# results/bq_radicals.mae: the two radicals exported from Maestro in step A3
"$SCHRODINGER/run" scripts/check_structures.py results/bq_prepped.maegz results/bq_radicals.mae
# expected: six rows; 56 electrons for bq_Q; 57 (multiplicity 2) for bq_QHrad and bq_Qradm;
#           58 for bq_QH2, bq_QHm and bq_Q2m
"$SCHRODINGER/utilities/structconvert" results/bq_prepped.maegz results/bq_prepped.mae

# ---------------------------------------------------------------------------
# C2 · Epik from the command line
"$SCHRODINGER/run" scripts/extract_entry.py results/bq_prepped.maegz bq_QH2 results/bq_QH2.mae
"$SCHRODINGER/epikx" -h
"$SCHRODINGER/epikx" results/bq_QH2.mae results/bq_QH2_epik_default.maegz -WAIT
"$SCHRODINGER/epikx" results/bq_QH2.mae results/bq_QH2_epik_wide.maegz -ph 7.0 -pht 7.0 -ms 16 -WAIT
"$SCHRODINGER/epikx" results/bq_QH2.mae results/bq_QH2_epik_ph12.maegz -ph 12.0 -pht 2.0 -ms 16 -WAIT
"$SCHRODINGER/run" scripts/list_epik_states.py results/bq_QH2_epik_default.maegz \
    results/bq_QH2_epik_wide.maegz results/bq_QH2_epik_ph12.maegz

# ---------------------------------------------------------------------------
# Homework · dihydrophenazine
"$SCHRODINGER/ligprep" -ismi inputs/homework_phenazine.smi -omae results/phz_prepped.maegz \
    -i 0 -nt -s 1 -NJOBS 1 -WAIT
"$SCHRODINGER/run" scripts/extract_entry.py results/phz_prepped.maegz phz_PH2 results/phz_PH2.mae
"$SCHRODINGER/epikx" results/phz_PH2.mae results/phz_PH2_epik_default.maegz -WAIT
"$SCHRODINGER/epikx" results/phz_PH2.mae results/phz_PH2_epik_wide.maegz -ph 7.0 -pht 7.0 -ms 16 -WAIT
"$SCHRODINGER/run" scripts/list_epik_states.py results/phz_PH2_epik_default.maegz results/phz_PH2_epik_wide.maegz
