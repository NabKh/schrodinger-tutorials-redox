# Session 2 · every command of the session (Windows PowerShell or the VS Code terminal)
# Run one block at a time on the workstation, from the folder 02-optimisation-and-frequencies.
# Each block carries the name of its step in README.md. Lines starting with # are comments.
# The Linux equivalent of every block is in commands.sh.

# ---------------------------------------------------------------------------
# 0 · files, suite, host and folder (Before the session)
# 0.1 · get the files into your user folder (writing to C:\ itself is refused on the workstation)
git clone https://github.com/NabKh/schrodinger-tutorials-redox.git $HOME\schrodinger-tutorials-redox
git -C $HOME\schrodinger-tutorials-redox log -1 --oneline
# 0.2 · the suite (set again in every new window)
$S = "C:\Program Files\Schrodinger2026-2"
$env:SCHRODINGER = $S      # same installation as $S; without it jsc stops with "$SCHRODINGER must be defined"
& "$S\jsc" hosts list      # localhost, and rs4/rs5/rs6.differ.nl:8030 with cpursN and gpursN
# 0.3 · host and folder
$H = "cpurs4"              # a CPU node from the list above (Jaguar runs on CPUs)
Set-Location $HOME\schrodinger-tutorials-redox\02-optimisation-and-frequencies
New-Item -ItemType Directory -Force results | Out-Null   # outputs of this session go here

# ---------------------------------------------------------------------------
# P · instructor test run, before the session (README, P)
# P1 · regenerate the starting inputs, check them, then copy them into inputs\<family>\
foreach ($f in "bq", "aqds", "tempo", "indigo") {
    & "$S\run" scripts\make_inputs.py inputs\recipes\$f.csv --out results\p1_$f
    & "$S\run" scripts\check_inputs.py results\p1_$f
}
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\p1_b3lyp --set dftname=B3LYP --suffix _b3lyp
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\p1_gas --level gas --suffix _gas
#   only after every line above is ok:
foreach ($f in "bq", "aqds", "tempo", "indigo") { Copy-Item results\p1_$f\*.in inputs\$f\ }
Copy-Item results\p1_b3lyp\bq_Q_b3lyp.in, results\p1_b3lyp\bq_QH2_b3lyp.in inputs\bq\
Copy-Item results\p1_gas\bq_Q_gas.in, results\p1_gas\bq_QH2_gas.in inputs\gas\
#   drop the MAEFILE line: the geometry is in &zmat, and a .in that names a .mae fails without it
Select-String -Path inputs\*\*.in -Pattern '^MAEFILE:' -List | ForEach-Object { (Get-Content $_.Path) -notmatch '^MAEFILE:' | Set-Content $_.Path }
#   bq_QH2cis.in: built in Maestro from bq_QH2 (one O-H rotated by 180 degrees), exported as Jaguar input;
#   bq_QH2cis_b3lyp.in: a copy of it with entry_name bq_QH2cis_b3lyp and dftname=B3LYP
& "$S\run" scripts\check_inputs.py inputs

# P2 · production benzoquinone, every state
New-Item -ItemType Directory -Force results\bq | Out-Null
Copy-Item inputs\bq\*.in results\bq\
Push-Location results\bq
foreach ($i in Get-ChildItem *.in | Where-Object { $_.Name -notmatch '\.\d\d\.in$' }) { & "$S\jaguar" run $i.Name -HOST $H -PARALLEL 4 }
Pop-Location

# P3 · gas phase and the one-factor checks (D3, D4)
New-Item -ItemType Directory -Force results\checks | Out-Null
Copy-Item inputs\gas\bq_Q_gas.in, inputs\checks\*.in results\checks\
Push-Location results\checks
foreach ($i in Get-ChildItem *.in | Where-Object { $_.Name -notmatch '\.\d\d\.in$' }) { & "$S\jaguar" run $i.Name -HOST $H -PARALLEL 4 }
Pop-Location

# P4 · the expensive ladder rungs (L2)
New-Item -ItemType Directory -Force results\level | Out-Null
Copy-Item inputs\levels\bq_Q_m062x.in, inputs\levels\bq_Q_wb97xd.in, inputs\levels\bq_Q_wb97xd_631g.in results\level\
Push-Location results\level
& "$S\jaguar" run bq_Q_m062x.in -HOST $H -PARALLEL 4
& "$S\jaguar" run bq_Q_wb97xd.in -HOST $H -PARALLEL 4
& "$S\jaguar" run bq_Q_wb97xd_631g.in -HOST $H -PARALLEL 4   # tests the wB97X-D result (README L2)
Pop-Location

# ---------------------------------------------------------------------------
# S2 · closed-shell parents from Session 1 (skip if ..\01-introduction\results\bq_prepped.maegz exists)
#   & "$S\ligprep" -ismi ..\01-introduction\inputs\bq_closed_shell.smi -omae ..\01-introduction\results\bq_prepped.maegz -i 0 -nt -s 1 -NJOBS 1 -WAIT

# S · the rule, step 5: Epik on the three n_e forms Q, Q*- and Q2- (test run: the radical comes back as QH2, QH-, Q2-)
New-Item -ItemType Directory -Force results\epik | Out-Null
Set-Content results\epik\bq_ne.smi "O=C1C=CC(=O)C=C1 bq_Q", "[O-]c1ccc([O])cc1 bq_Qradm", "[O-]c1ccc([O-])cc1 bq_Q2m"
& "$S\utilities\structconvert" results\epik\bq_ne.smi results\epik\bq_ne.mae
& "$S\epikx" results\epik\bq_ne.mae results\epik\bq_ne_epik.maegz -ph 7.0 -pht 7.0 -ms 16 -WAIT
& "$S\run" ..\01-introduction\scripts\list_epik_states.py results\epik\bq_ne.mae results\epik\bq_ne_epik.maegz
# expected: input 52, 53, 54 electrons (no H yet); output bq_Q 56, and 58 for every state of bq_Qradm and bq_Q2m

# S3 · every state and one Jaguar input per state, from the recipe
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made
#   or from the LigPrep parents:
#   & "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\made --parents ..\01-introduction\results\bq_prepped.maegz
# expected: one line per state, e.g. H removed: H9-O1 H12-O6 (each removed H and the atom it was bonded to),
#   then "wrote 6 inputs and states.maegz to results\made"

# S4 · check them, compare with the given inputs, look at them in Maestro
& "$S\run" scripts\check_inputs.py results\made
code --diff results\made\bq_Q2m.in inputs\bq\bq_Q2m.in
# (instructor demo only) Maestro: File > Import Structures > results\made\states.maegz

# S5 · the input written from the Maestro panel (gear > Write) against the script's
#   code --diff <written file> results\made\bq_QHm.in
#   & "$S\run" scripts\check_inputs.py <written file>

# S7 · the light steps for your group's family: states, inputs and checks, no job
$f = "aqds"          # your group's family: aqds, tempo or indigo
& "$S\run" scripts\make_inputs.py inputs\recipes\$f.csv --out results\made_$f
& "$S\run" scripts\check_inputs.py results\made_$f
# Maestro: File > Import Structures > results\made_$f\states.maegz

# ---------------------------------------------------------------------------
# L1 · which effect matters for a difference (outputs of P2 and L4a)
& "$S\run" scripts\summarise_job.py results\bq\bq_Q.out results\bq\bq_Q_b3lyp.out
& "$S\run" scripts\summarise_job.py results\bq\bq_QH2.out results\bq\bq_QH2_b3lyp.out
& "$S\run" scripts\summarise_job.py results\bq\bq_QH2cis.out results\bq\bq_QH2cis_b3lyp.out

# L2, L3 · the vendor's flags for the functionals and basis sets of the course (seconds, no job)
$JD = (Get-ChildItem "$S\mmshare-v*\data\jaguar").FullName
Import-Csv $JD\levels_of_theory.csv | Where-Object Method -in "PBE","B3LYP","B3LYP-D3","M06-2X-D3","wB97X-D" | Format-Table Method, is_recommended, is_dispersion_corrected_dft, is_hybrid_dft, is_meta_gga_dft, is_long_range_corrected_dft
Import-Csv $JD\basis_sets.csv | Where-Object full_name -in "6-31G**","DEF2-TZVP","DEF2-TZVPD","LACVP++**" | Format-Table full_name, is_diffuse, is_ecp
# expected (2026-2): recommended 1 for all but PBE; diffuse 1 for DEF2-TZVPD and LACVP++** only; ECP 1 for LACVP++** only

# L2 · the ladder, when the rungs are back (B5, P3, P4)
foreach ($o in Get-ChildItem results\level\*.out) { & "$S\run" scripts\summarise_job.py $o.FullName }
& "$S\run" scripts\summarise_job.py results\checks\bq_Q_gas_tzvp.out results\checks\bq_Q_gas.out
foreach ($o in Get-ChildItem results\level\*.out) { & "$S\run" scripts\ir_compare.py $o.FullName }
& "$S\run" scripts\ir_compare.py results\checks\bq_Q_gas_tzvp.out
& "$S\run" scripts\ir_compare.py results\checks\bq_Q_gas.out
# r(C=O): open the final structure (<job>.01.mae) in Maestro and measure it

# L4a · solvation single points at the optimised PBF geometries (after P2)
#   &gen of inputs\solvation\<job>.in + &zmat of results\bq\bq_<state>.01.in -> results\solv\<job>.in
New-Item -ItemType Directory -Force results\solv | Out-Null
# the loop variable is $st, not $s: PowerShell names ignore case, and $s would overwrite $S
foreach ($st in "Q", "Q2m") {
    $zmat = [regex]::Match((Get-Content -Raw results\bq\bq_$st.01.in), '(?s)&zmat.*?\n\s*&').Value
    foreach ($m in "gas", "pbf", "smd", "pcm") {
        $job = "bq_${st}_sp_$m"
        $gen = [regex]::Match((Get-Content -Raw inputs\solvation\$job.in), '(?s)^.*?&gen.*?\n\s*&').Value
        Set-Content -Path results\solv\$job.in -Value ($gen + "`n" + $zmat + "`n")
    }
}
& "$S\run" scripts\check_inputs.py results\solv      # expected: eight ok lines; open one and look at it
Push-Location results\solv
foreach ($i in Get-ChildItem *.in | Where-Object { $_.Name -notmatch '\.\d\d\.in$' }) { & "$S\jaguar" run $i.Name -HOST $H -PARALLEL 4 }
Pop-Location
#   when they are back:
Select-String -Path results\solv\*.out -Pattern "SCFE:|Solvation energy|HOMO"   # the last SCFE line of each file is E

# L6 · a cheap screen of a new family, and one rung up
& "$S\run" scripts\make_inputs.py inputs\recipes\$f.csv --out results\screen --level gas --set dftname=PBE --set basis=6-31G** --suffix _screen
& "$S\run" scripts\make_inputs.py inputs\recipes\bq.csv --out results\rung --level gas --set dftname=M06-2X-D3 --suffix _m062x
#   new job names need new rows in inputs\states.csv before check_inputs.py passes them

# ---------------------------------------------------------------------------
# A1 · read the production input you made in S3
code results\made\bq_Q.in

# A3 · three broken inputs, and the live inputs before B2
& "$S\run" scripts\check_inputs.py inputs\broken inputs\live
# expected: three FAIL lines and two ok lines

# A4 · after writing molchg and multip (and iuhf=1 if multip > 1) in your group's file
& "$S\run" scripts\check_inputs.py inputs\groups
# expected: ok for your file, TODO for the other three

# ---------------------------------------------------------------------------
# B1 · hosts (job servers on rs4, rs5, rs6, port 8030)
& "$S\jsc" hosts list
& "$S\jsc" server-info rs4.differ.nl:8030
# set $H to a compute host, not localhost (block 0)

# B2 · live job: one pair bq_Q_pbe, the next pair bq_QH2_pbe
New-Item -ItemType Directory -Force results\live | Out-Null
Copy-Item inputs\live\*.in results\live\
Push-Location results\live
& "$S\jaguar" run bq_Q_pbe.in -HOST $H -PARALLEL 4
#   & "$S\jaguar" run bq_QH2_pbe.in -HOST $H -PARALLEL 4
Pop-Location
$J = "<the JobId printed above>"   # replace the text in quotes
# a job that leaves only its .in failed before Jaguar started (jsc info: "srun": executable file not found): submit the same .in again

# B3 · monitor, and cancel a wrong job
& "$S\jsc" list
& "$S\jsc" info $J
& "$S\jsc" tail-file --name bq_Q_pbe.log $J     # prints the whole log so far; -f keeps following until the job ends; Ctrl+C stops following, not the job
#   & "$S\jsc" cancel $J                        # only if the job was submitted with a wrong input

# B5 · one ladder or solvation job per pair (as assigned)
New-Item -ItemType Directory -Force results\level | Out-Null
Copy-Item inputs\levels\bq_Q_pbe_631g.in, inputs\levels\bq_Q_b3lyp_631g.in results\level\
Push-Location results\level
& "$S\jaguar" run bq_Q_pbe_631g.in -HOST $H -PARALLEL 4
#   & "$S\jaguar" run bq_Q_b3lyp_631g.in -HOST $H -PARALLEL 4
Pop-Location
#   or one solvation single point, once results\solv\ is written (L4a):
#   Push-Location results\solv; & "$S\jaguar" run bq_Q2m_sp_smd.in -HOST $H -PARALLEL 4; Pop-Location

# B6 · restart an optimisation that stopped at maxitg, from its last geometry
$job = "bq_Q_pbe"; $dir = "results\live"
New-Item -ItemType Directory -Force $dir\restart | Out-Null
Copy-Item $dir\$job.01.in $dir\restart\$job.in
Copy-Item $dir\$job.01.mae $dir\restart\                # the .01.in names it on its MAEFILE line
code $dir\restart\$job.in                      # check: igeopt=1 and ifreq=1 still in &gen, MAEFILE: $job.01.mae
Push-Location $dir\restart
& "$S\jaguar" run "$job.in" -HOST $H -PARALLEL 4
Pop-Location

# B6 · a whole family, one job per input (also homework 1); restart files *.NN.in are skipped
$f = "aqds"          # your group's family: aqds, tempo or indigo
& "$S\run" scripts\check_inputs.py inputs\$f
New-Item -ItemType Directory -Force results\$f | Out-Null
Get-ChildItem inputs\$f\*.in | Where-Object { $_.Name -notmatch '\.\d\d\.in$' } | Copy-Item -Destination results\$f\
Push-Location results\$f
foreach ($i in Get-ChildItem *.in | Where-Object { $_.Name -notmatch '\.\d\d\.in$' }) { & "$S\jaguar" run $i.Name -HOST $H -PARALLEL 4 }
Pop-Location

# ---------------------------------------------------------------------------
# C · read the production outputs of the test run (P2, in results\bq\)
& "$S\run" scripts\summarise_job.py results\bq\bq_Q.out
& "$S\run" scripts\summarise_job.py results\bq\bq_QHrad.out
& "$S\run" scripts\summarise_job.py results\bq\bq_QH2.out results\bq\bq_QH2cis.out
# C1-C4 by hand in the .out (VS Code, Ctrl+F):
Select-String -Path results\bq\bq_Q.out -Pattern "Geometry optimization complete|Scaling standard convergence criteria|Number of imaginary frequencies|Quasi-Harmonic|rotational symmetry number|Gtot"

# C6 · your live job, when it has finished
& "$S\run" scripts\summarise_job.py results\live\bq_Q_pbe.out

# P3, D4 · basis functions removed by Jaguar (near-linear dependence), every state: basis - canonical
foreach ($o in Get-ChildItem results\bq\*.out, results\checks\*.out | Where-Object { $_.Name -notmatch '\.\d\d\.out$' }) {
  $nb = [regex]::Match((Select-String -Path $o.FullName -Pattern "number of basis functions" | Select-Object -First 1).Line, '\d+\s*$').Value.Trim()
  $nc = [regex]::Match((Select-String -Path $o.FullName -Pattern "number of canonical orbitals" | Select-Object -Last 1).Line, '\d+\s*$').Value.Trim()
  "{0,-22} basis {1,4}  canonical {2,4}  removed {3,3}" -f $o.Name, $nb, $nc, ($nb - $nc) }
# expected (test run, results\bq): removed 30 for Q, 29 for Q*- and Q2-, 30 for QH* and QH-, 31 for QH2

# ---------------------------------------------------------------------------
# D1 · NIST gas-phase IR spectrum of 1,4-benzoquinone (NIST data: do not redistribute, do not commit)
Invoke-WebRequest "https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C106514&Index=0&Type=IR" -OutFile results\bq_Q_nist.jdx
Get-Content results\bq_Q_nist.jdx -TotalCount 20                 # header: ##STATE, ##XUNITS, ##YUNITS

# D2 · computed against experiment
& "$S\run" scripts\ir_compare.py results\bq\bq_Q.out --scale 0.963 --exp results\bq_Q_nist.jdx --plot results\bq_Q_ir.pdf
# 0.963 +- 0.044: B3LYP/def2-TZVPP (NIST CCCBDB); for the PBE live job use 0.989 +- 0.027 (PBEPBE/6-31+G**)
#   & "$S\run" scripts\ir_compare.py results\live\bq_Q_pbe.out --scale 0.989 --exp results\bq_Q_nist.jdx

# D3 · the same in the gas phase (P3)
& "$S\run" scripts\ir_compare.py results\checks\bq_Q_gas.out --scale 0.963 --exp results\bq_Q_nist.jdx

# D4 · one-factor checks (P3)
foreach ($o in Get-ChildItem results\checks\*.out) {
    & "$S\run" scripts\summarise_job.py $o.FullName
    & "$S\run" scripts\ir_compare.py $o.FullName --scale 0.963 --exp results\bq_Q_nist.jdx
}

# ---------------------------------------------------------------------------
# Homework
# HW1 · your family at the production level: block "B6 · a whole family" above, then
foreach ($o in Get-ChildItem results\$f\*.out) { & "$S\run" scripts\summarise_job.py $o.FullName }

# HW3 · one convergence factor on your molecule (add the new rows to inputs\states.csv first)
& "$S\run" scripts\make_inputs.py inputs\recipes\$f.csv --out results\conv --set basis=def2-TZVP --suffix _tzvp
& "$S\run" scripts\check_inputs.py results\conv
#   submit one of them as in B2, from results\conv

# HW4 · solvation spread of one redox pair of your family (after HW1; add the new rows to inputs\states.csv)
#   &gen of inputs\solvation\bq_Q_sp_<model>.in with molchg, multip, iuhf of your own input; &zmat of your .01.in
$pair = "aq_Q", "aq_Qradm"     # the two states of one redox step
New-Item -ItemType Directory -Force results\solv_$f | Out-Null
foreach ($job in $pair) {
    $zmat = [regex]::Match((Get-Content -Raw results\$f\$job.01.in), '(?s)&zmat.*?\n\s*&').Value
    $own = Select-String -Path inputs\$f\$job.in -Pattern '^\s*(molchg|multip|iuhf)\s*=' | ForEach-Object { $_.Line.Trim() }
    foreach ($m in "gas", "pbf", "smd", "pcm") {
        $tpl = Get-Content -Raw inputs\solvation\bq_Q_sp_$m.in
        $keep = [regex]::Match($tpl, '(?s)&gen\s*\n(.*?)\n\s*&').Groups[1].Value -split "`r?`n" |
            Where-Object { $_ -notmatch '^\s*(molchg|multip|iuhf)\s*=' }
        $text = "entry_name: ${job}_sp_$m`n&gen`n" + ((@($keep) + @($own)) -join "`n") + "`n&`n" + $zmat + "`n"
        Set-Content -Path results\solv_$f\${job}_sp_$m.in -Value $text
    }
}
& "$S\run" scripts\check_inputs.py results\solv_$f
#   submit as in L4a, from results\solv_$f
