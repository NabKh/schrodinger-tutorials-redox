# Session 2 · commands for sections A to D (Linux, bash)
# Run one block at a time from the folder 02-optimisation-and-frequencies.
# Replace <host> by a compute host from B1. Windows equivalents: commands.ps1.

# 0 · suite and folder
export SCHRODINGER=/opt/schrodinger2026-2      # adjust to your installation
mkdir -p results

# S2 · parents from Session 1 (if not done there)
# $SCHRODINGER/ligprep -ismi ../01-introduction/inputs/bq_closed_shell.smi -omae ../01-introduction/results/bq_prepped.maegz -i 0 -nt -s 1 -NJOBS 1 -WAIT

# S3, S4 · all states, one input each, and check them
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/bq.csv --out results/made
$SCHRODINGER/run scripts/check_inputs.py results/made
diff results/made/bq_Q2m.in inputs/bq/bq_Q2m.in

# L · ladder and solvation inputs
$SCHRODINGER/run scripts/check_inputs.py inputs/levels
$SCHRODINGER/run scripts/check_inputs.py inputs/solvation

# A3, A4 · check the inputs
$SCHRODINGER/run scripts/check_inputs.py inputs/bq
$SCHRODINGER/run scripts/check_inputs.py inputs/broken
$SCHRODINGER/run scripts/check_inputs.py inputs/groups

# B1 · hosts
$SCHRODINGER/jsc hosts list

# B2 · live job
mkdir -p results/live && cp inputs/live/*.in results/live/
(cd results/live && $SCHRODINGER/jaguar run bq_Q_pbe.in -HOST <host> -PARALLEL 4)

# B3 · monitor
$SCHRODINGER/jsc list
$SCHRODINGER/jsc tail-file --name bq_Q_pbe.log <jobid>

# B5 · one ladder or solvation job per pair
mkdir -p results/level && cp inputs/levels/bq_Q_pbe_631g.in results/level/
(cd results/level && $SCHRODINGER/jaguar run bq_Q_pbe_631g.in -HOST <host> -PARALLEL 4)

# C · read the output
$SCHRODINGER/run scripts/summarise_job.py reference/bq_Q.out
$SCHRODINGER/run scripts/summarise_job.py reference/bq_QHrad.out
$SCHRODINGER/run scripts/summarise_job.py reference/bq_QH2.out reference/bq_QH2cis.out

# D1 · NIST spectrum (do not redistribute)
curl -L -o results/bq_Q_nist.jdx "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C106514&Index=0&Type=IR"

# D2, D3 · computed against experiment
$SCHRODINGER/run scripts/ir_compare.py reference/bq_Q.out --scale 0.9626 --exp results/bq_Q_nist.jdx --plot results/bq_Q_ir.pdf
$SCHRODINGER/run scripts/ir_compare.py reference/bq_Q_gas.out --scale 0.9626 --exp results/bq_Q_nist.jdx

# D4 · one-factor checks
mkdir -p results/checks && cp inputs/gas/bq_Q_gas.in inputs/checks/*.in results/checks/
(cd results/checks && for f in *.in; do $SCHRODINGER/jaguar run "$f" -HOST <host> -PARALLEL 4; done)
