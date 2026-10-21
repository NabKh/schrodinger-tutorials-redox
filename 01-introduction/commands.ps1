# Session 1 · commands for sections B and C (Windows PowerShell)
# Run one block at a time from the folder 01-introduction.
# Lines starting with # are comments. Adjust $S to your installation path.
# The Linux equivalent of every block is in commands.sh.

# ---------------------------------------------------------------------------
# B1 · open the suite by its full installation path
$S = "C:\Program Files\Schrodinger2026-2"
cd C:\schrodinger-tutorials-redox\01-introduction
New-Item -ItemType Directory -Force results | Out-Null   # outputs of this session go here
& "$S\run" python3 -c "print('suite OK')"
# expected: suite OK

# keep Maestro open while running these commands, or start the local job server:
#   & "$S\jsc" local-server-start

# for comparison: the release the environment variable points at
$env:SCHRODINGER

# ---------------------------------------------------------------------------
# B2 · hosts and jobs
# once per user, before remote submission works: register with the job server
# (server and port from your administrator)
#   & "$S\jsc" cert get <server>:<port>     (add --user <name> if your cluster user name differs)
& "$S\jsc" hosts list
& "$S\jsc" list

# ---------------------------------------------------------------------------
# B3 · LigPrep without changing the ionisation state
#   -i 0   keep the ionisation state written in the SMILES (otherwise LigPrep neutralises, and may re-ionise, QH- and Q2-; check ligprep -h)
#   -nt    no tautomers: one output per input
#   -s 1   one stereoisomer per input
#   -WAIT  return when the job has finished
& "$S\ligprep" -ismi inputs\bq_closed_shell.smi -omae results\bq_prepped.maegz `
      -i 0 -nt -s 1 -NJOBS 1 -WAIT

# check formula, charge, electron count and multiplicity of every output structure
& "$S\run" scripts\check_structures.py results\bq_prepped.maegz results\bq_radicals.mae
# expected: six rows; 56 electrons for bq_Q; 57 (multiplicity 2) for bq_QHrad and bq_Qradm;
#           58 for bq_QH2, bq_QHm and bq_Q2m
# (results\bq_radicals.mae: the two radicals exported from Maestro in step A3)

# optional: a plain .mae copy
& "$S\utilities\structconvert" results\bq_prepped.maegz results\bq_prepped.mae

# ---------------------------------------------------------------------------
# C2 · Epik from the command line
# take bq_QH2 out of the LigPrep output (or use File > Export Structures in Maestro)
& "$S\run" scripts\extract_entry.py results\bq_prepped.maegz bq_QH2 results\bq_QH2.mae

# check the options of your release; the flags below are the expected ones
# -WAIT makes each command return only when its job has finished
& "$S\epikx" -h

# Run 1, default settings
& "$S\epikx" results\bq_QH2.mae results\bq_QH2_epik_default.maegz -WAIT

# Run 2, wide window: target pH 7.0, tolerance 7.0 (pH 0 to 14), up to 16 structures
#   -pht and a population cut-off are alternatives; set one, not both
& "$S\epikx" results\bq_QH2.mae results\bq_QH2_epik_wide.maegz -ph 7.0 -pht 7.0 -ms 16 -WAIT

# Run 3, window centred where QH- and Q2- dominate (compare runs 2 and 3: threshold or window reading)
& "$S\epikx" results\bq_QH2.mae results\bq_QH2_epik_ph12.maegz -ph 12.0 -pht 2.0 -ms 16 -WAIT

# list what each run returned: charges, electron count, Epik properties
& "$S\run" scripts\list_epik_states.py results\bq_QH2_epik_default.maegz `
      results\bq_QH2_epik_wide.maegz results\bq_QH2_epik_ph12.maegz
# expected: the electron count is the same (58) in every structure of every run

# ---------------------------------------------------------------------------
# Homework · dihydrophenazine
& "$S\ligprep" -ismi inputs\homework_phenazine.smi -omae results\phz_prepped.maegz `
      -i 0 -nt -s 1 -NJOBS 1 -WAIT
& "$S\run" scripts\extract_entry.py results\phz_prepped.maegz phz_PH2 results\phz_PH2.mae
& "$S\epikx" results\phz_PH2.mae results\phz_PH2_epik_default.maegz -WAIT
& "$S\epikx" results\phz_PH2.mae results\phz_PH2_epik_wide.maegz -ph 7.0 -pht 7.0 -ms 16 -WAIT
& "$S\run" scripts\list_epik_states.py results\phz_PH2_epik_default.maegz results\phz_PH2_epik_wide.maegz

# ---------------------------------------------------------------------------
# Optional · LigPrep with Epik, for enumeration (step 3 of C3)
# confirm the flag names first:
#   & "$S\ligprep" -h
# then, for example (names as listed by -h):
#   & "$S\ligprep" -ismi inputs\bq_closed_shell.smi -omae results\bq_enum.maegz -epikx -ph 7.0 -pht 7.0 -s 1 -NJOBS 1 -WAIT
