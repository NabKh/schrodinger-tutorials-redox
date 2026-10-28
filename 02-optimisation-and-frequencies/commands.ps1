# Session 2 · commands for sections A to D (Windows PowerShell)
# Run one block at a time on the workstation, from the folder 02-optimisation-and-frequencies.
# Lines starting with # are comments. Replace <host> by a compute host from B1.
# The Linux equivalent of every block is in commands.sh.

# ---------------------------------------------------------------------------
# 0 · suite and folder
$S = "C:\Program Files\Schrodinger2026-2"
$env:SCHRODINGER = $S      # without this, jsc hosts list stops with "$SCHRODINGER must be defined"
cd C:\schrodinger-tutorials-redox\02-optimisation-and-frequencies
New-Item -ItemType Directory -Force results | Out-Null   # outputs of this session go here

# ---------------------------------------------------------------------------
# A3 · check the inputs before they cost compute time
& "$S\run" scripts\check_inputs.py inputs\bq
# expected: one ok line per input
& "$S\run" scripts\check_inputs.py inputs\broken
# expected: FAIL for bq_Qradm (parity); bq_QHm and bq_Q2m are caught only by states.csv

# A4 · after writing molchg and multip in your group's file
& "$S\run" scripts\check_inputs.py inputs\groups

# ---------------------------------------------------------------------------
# B1 · hosts (job servers on rs4, rs5, rs6, port 8030)
& "$S\jsc" hosts list
& "$S\jsc" server-info rs4.differ.nl:8030

# ---------------------------------------------------------------------------
# B2 · live job: one pair bq_Q_pbe, the next pair bq_QH2_pbe
New-Item -ItemType Directory -Force results\live | Out-Null
Copy-Item inputs\live\*.in results\live\
Push-Location results\live
& "$S\jaguar" run bq_Q_pbe.in -HOST <host> -PARALLEL 4
#   & "$S\jaguar" run bq_QH2_pbe.in -HOST <host> -PARALLEL 4
Pop-Location
# expected: a JobId line; the command returns at once
# a job that fails at once with "srun: executable file not found" hit a bad node: submit it again

# ---------------------------------------------------------------------------
# B3 · monitor
& "$S\jsc" list
& "$S\jsc" info <jobid>
& "$S\jsc" tail-file --name bq_Q_pbe.log <jobid>

# B4 · group job, the same way
New-Item -ItemType Directory -Force results\group | Out-Null
Copy-Item inputs\groups\<file>.in results\group\
Push-Location results\group
& "$S\jaguar" run <file>.in -HOST <host> -PARALLEL 4
Pop-Location

# ---------------------------------------------------------------------------
# C · read the output (reference outputs from the instructor, in reference\)
& "$S\run" scripts\summarise_job.py reference\bq_Q.out
& "$S\run" scripts\summarise_job.py reference\bq_QHrad.out
& "$S\run" scripts\summarise_job.py reference\bq_QH2.out reference\bq_QH2cis.out
# expected for bq_Q: converged, imaginary 0, lowest 232.7 cm-1, sigma 4, Gtot -381.566711 Eh

# C6 · your live job, when it has finished
& "$S\run" scripts\summarise_job.py results\live\bq_Q_pbe.out

# ---------------------------------------------------------------------------
# D1 · NIST gas-phase IR spectrum of 1,4-benzoquinone (NIST data: do not redistribute)
Invoke-WebRequest "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C106514&Index=0&Type=IR" -OutFile results\bq_Q_nist.jdx

# D2 · computed against experiment
& "$S\run" scripts\ir_compare.py reference\bq_Q.out --scale 0.9626 --exp results\bq_Q_nist.jdx --plot results\bq_Q_ir.pdf
# 0.9626: B3LYP/def2-TZVPP (NIST CCCBDB); use 0.9879 for the PBE live job

# D3 · the same in the gas phase (output from the instructor)
& "$S\run" scripts\ir_compare.py reference\bq_Q_gas.out --scale 0.9626 --exp results\bq_Q_nist.jdx

# D4 · one-factor checks (instructor-run if time is short)
New-Item -ItemType Directory -Force results\checks | Out-Null
Copy-Item inputs\gas\bq_Q_gas.in, inputs\checks\*.in results\checks\
Push-Location results\checks
foreach ($f in Get-ChildItem *.in) { & "$S\jaguar" run $f.Name -HOST <host> -PARALLEL 4 }
Pop-Location
