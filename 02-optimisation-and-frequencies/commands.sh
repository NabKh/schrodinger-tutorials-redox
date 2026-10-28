# Session 2 · every command of the session (Linux, bash)
# Run one block at a time from the folder 02-optimisation-and-frequencies.
# Each block carries the name of its step in README.md. Windows equivalents: commands.ps1.

# ---------------------------------------------------------------------------
# 0 · suite, host and folder
export SCHRODINGER=/opt/schrodinger2026-2      # adjust to your installation
$SCHRODINGER/jsc hosts list
H="<one of the compute hosts listed above>"    # replace the text in quotes
mkdir -p results
# (no check of the given inputs here: you make your own in S3 and check them in S4)

# ---------------------------------------------------------------------------
# P · instructor test run, before the session
# P1 · regenerate the starting inputs, check them, then copy them into inputs/<family>/
for f in bq aqds tempo indigo; do
  $SCHRODINGER/run scripts/make_inputs.py inputs/recipes/$f.csv --out results/p1_$f
  $SCHRODINGER/run scripts/check_inputs.py results/p1_$f
done
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/bq.csv --out results/p1_b3lyp --set dftname=B3LYP --suffix _b3lyp
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/bq.csv --out results/p1_gas --level gas --suffix _gas
#   only after every line above is ok:
for f in bq aqds tempo indigo; do cp results/p1_$f/*.in inputs/$f/; done
cp results/p1_b3lyp/bq_Q_b3lyp.in results/p1_b3lyp/bq_QH2_b3lyp.in inputs/bq/
cp results/p1_gas/bq_Q_gas.in results/p1_gas/bq_QH2_gas.in inputs/gas/
#   bq_QH2cis.in and bq_QH2cis_b3lyp.in: built in Maestro (README, P1)
$SCHRODINGER/run scripts/check_inputs.py inputs

# P2 · production benzoquinone
mkdir -p results/bq && cp inputs/bq/*.in results/bq/
(cd results/bq && for i in *.in; do [[ $i =~ \.[0-9][0-9]\.in$ ]] || $SCHRODINGER/jaguar run "$i" -HOST "$H" -PARALLEL 4; done)

# P3 · gas phase and the one-factor checks
mkdir -p results/checks && cp inputs/gas/bq_Q_gas.in inputs/checks/*.in results/checks/
(cd results/checks && for i in *.in; do [[ $i =~ \.[0-9][0-9]\.in$ ]] || $SCHRODINGER/jaguar run "$i" -HOST "$H" -PARALLEL 4; done)

# P4 · the expensive ladder rungs
mkdir -p results/level && cp inputs/levels/bq_Q_m062x.in inputs/levels/bq_Q_wb97xd.in results/level/
(cd results/level && for i in bq_Q_m062x.in bq_Q_wb97xd.in; do $SCHRODINGER/jaguar run "$i" -HOST "$H" -PARALLEL 4; done)

# ---------------------------------------------------------------------------
# S2 · parents from Session 1 (if not done there)
# $SCHRODINGER/ligprep -ismi ../01-introduction/inputs/bq_closed_shell.smi -omae ../01-introduction/results/bq_prepped.maegz -i 0 -nt -s 1 -NJOBS 1 -WAIT

# S3, S4 · all states, one input each, and check them
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/bq.csv --out results/made
$SCHRODINGER/run scripts/check_inputs.py results/made
diff results/made/bq_Q2m.in inputs/bq/bq_Q2m.in

# S7 · the light steps for your group's family, no job
f=aqds               # your group's family: aqds, tempo or indigo
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/$f.csv --out results/made_$f
$SCHRODINGER/run scripts/check_inputs.py results/made_$f

# ---------------------------------------------------------------------------
# L1 · which effect matters for a difference
$SCHRODINGER/run scripts/summarise_job.py results/bq/bq_Q.out results/bq/bq_Q_b3lyp.out
$SCHRODINGER/run scripts/summarise_job.py results/bq/bq_QH2.out results/bq/bq_QH2_b3lyp.out
$SCHRODINGER/run scripts/summarise_job.py results/bq/bq_QH2cis.out results/bq/bq_QH2cis_b3lyp.out

# L2, L3 · the vendor's flags for the functionals and basis sets of the course (seconds, no job)
J=$(ls -d $SCHRODINGER/mmshare-v*/data/jaguar)
head -1 $J/levels_of_theory.csv | cut -d, -f1-10; grep -E '^(PBE|B3LYP|B3LYP-D3|M06-2X-D3|wB97X-D),' $J/levels_of_theory.csv | cut -d, -f1-10
head -1 $J/basis_sets.csv; grep -E '^(6-31G\*\*|DEF2-TZVP|DEF2-TZVPD|LACVP\+\+\*\*),' $J/basis_sets.csv

# L2 · the ladder
$SCHRODINGER/run scripts/summarise_job.py results/level/*.out results/checks/bq_Q_gas_tzvp.out results/checks/bq_Q_gas.out
for o in results/level/*.out results/checks/bq_Q_gas_tzvp.out results/checks/bq_Q_gas.out; do $SCHRODINGER/run scripts/ir_compare.py "$o"; done

# L4a · solvation single points at the optimised PBF geometries (after P2)
mkdir -p results/solv
for s in Q Q2m; do
  for m in gas pbf smd pcm; do
    job=bq_${s}_sp_$m
    { sed -n '1,/^[[:space:]]*&[[:space:]]*$/p' inputs/solvation/$job.in
      sed -n '/^&zmat/,/^[[:space:]]*&[[:space:]]*$/p' results/bq/bq_$s.01.in
    } > results/solv/$job.in
  done
done
$SCHRODINGER/run scripts/check_inputs.py results/solv
(cd results/solv && for i in *.in; do [[ $i =~ \.[0-9][0-9]\.in$ ]] || $SCHRODINGER/jaguar run "$i" -HOST "$H" -PARALLEL 4; done)
grep -E "SCFE:|Solvation energy|HOMO" results/solv/*.out

# L6 · a cheap screen, and one rung up
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/$f.csv --out results/screen --level gas --set dftname=PBE --set "basis=6-31G**" --suffix _screen
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/bq.csv --out results/rung --level gas --set dftname=M06-2X-D3 --suffix _m062x

# ---------------------------------------------------------------------------
# A3, A4 · check the inputs
$SCHRODINGER/run scripts/check_inputs.py inputs/broken inputs/live
$SCHRODINGER/run scripts/check_inputs.py inputs/groups

# ---------------------------------------------------------------------------
# B1 · hosts
$SCHRODINGER/jsc hosts list
$SCHRODINGER/jsc server-info rs4.differ.nl:8030

# B2 · live job
mkdir -p results/live && cp inputs/live/*.in results/live/
(cd results/live && $SCHRODINGER/jaguar run bq_Q_pbe.in -HOST "$H" -PARALLEL 4)
J="<the JobId printed above>"                  # replace the text in quotes

# B3 · monitor, and cancel a wrong job
$SCHRODINGER/jsc list
$SCHRODINGER/jsc info "$J"
$SCHRODINGER/jsc tail-file --name bq_Q_pbe.log "$J"   # option name UNVERIFIED: $SCHRODINGER/jsc tail-file -h
# $SCHRODINGER/jsc cancel "$J"

# B5 · one ladder or solvation job per pair
mkdir -p results/level && cp inputs/levels/bq_Q_pbe_631g.in inputs/levels/bq_Q_b3lyp_631g.in results/level/
(cd results/level && $SCHRODINGER/jaguar run bq_Q_pbe_631g.in -HOST "$H" -PARALLEL 4)

# B6 · restart from the last geometry
job=bq_Q_pbe; dir=results/live
mkdir -p $dir/restart && cp $dir/$job.01.in $dir/restart/$job.in
grep -E "igeopt|ifreq" $dir/restart/$job.in
(cd $dir/restart && $SCHRODINGER/jaguar run $job.in -HOST "$H" -PARALLEL 4)

# B6 · a whole family (also homework 1)
$SCHRODINGER/run scripts/check_inputs.py inputs/$f
mkdir -p results/$f
for i in inputs/$f/*.in; do [[ $i =~ \.[0-9][0-9]\.in$ ]] || cp "$i" results/$f/; done
(cd results/$f && for i in *.in; do [[ $i =~ \.[0-9][0-9]\.in$ ]] || $SCHRODINGER/jaguar run "$i" -HOST "$H" -PARALLEL 4; done)

# ---------------------------------------------------------------------------
# C · read the output
$SCHRODINGER/run scripts/summarise_job.py results/bq/bq_Q.out
$SCHRODINGER/run scripts/summarise_job.py results/bq/bq_QHrad.out
$SCHRODINGER/run scripts/summarise_job.py results/bq/bq_QH2.out results/bq/bq_QH2cis.out
grep -nE "Geometry optimization complete|Scaling standard convergence criteria|Number of imaginary frequencies|Quasi-Harmonic|rotational symmetry number|Gtot" results/bq/bq_Q.out

# C6 · the live job
$SCHRODINGER/run scripts/summarise_job.py results/live/bq_Q_pbe.out

# ---------------------------------------------------------------------------
# D1 · NIST spectrum (do not redistribute, do not commit)
curl -L -o results/bq_Q_nist.jdx "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C106514&Index=0&Type=IR"
head -20 results/bq_Q_nist.jdx

# D2, D3 · computed against experiment
$SCHRODINGER/run scripts/ir_compare.py results/bq/bq_Q.out --scale 0.963 --exp results/bq_Q_nist.jdx --plot results/bq_Q_ir.pdf
$SCHRODINGER/run scripts/ir_compare.py results/checks/bq_Q_gas.out --scale 0.963 --exp results/bq_Q_nist.jdx
# PBE live job: --scale 0.989

# D4 · one-factor checks
for o in results/checks/*.out; do
  $SCHRODINGER/run scripts/summarise_job.py "$o"
  $SCHRODINGER/run scripts/ir_compare.py "$o" --scale 0.963 --exp results/bq_Q_nist.jdx
done

# ---------------------------------------------------------------------------
# Homework
# HW1 · after the family block of B6
$SCHRODINGER/run scripts/summarise_job.py results/$f/*.out

# HW3 · one convergence factor (add the new rows to inputs/states.csv first)
$SCHRODINGER/run scripts/make_inputs.py inputs/recipes/$f.csv --out results/conv --set basis=def2-TZVP --suffix _tzvp
$SCHRODINGER/run scripts/check_inputs.py results/conv

# HW4 · solvation spread of one redox pair (add the new rows to inputs/states.csv)
mkdir -p results/solv_$f
for job in aq_Q aq_Qradm; do
  for m in gas pbf smd pcm; do
    { echo "entry_name: ${job}_sp_$m"
      echo "&gen"
      sed -n '/^&gen/,/^[[:space:]]*&[[:space:]]*$/p' inputs/solvation/bq_Q_sp_$m.in | sed '1d;$d' |
        grep -Ev '^[[:space:]]*(molchg|multip|iuhf)[[:space:]]*='
      grep -E '^[[:space:]]*(molchg|multip|iuhf)[[:space:]]*=' inputs/$f/$job.in
      echo "&"
      sed -n '/^&zmat/,/^[[:space:]]*&[[:space:]]*$/p' results/$f/$job.01.in
    } > results/solv_$f/${job}_sp_$m.in
  done
done
$SCHRODINGER/run scripts/check_inputs.py results/solv_$f
