r"""Plot what a step of this session reads from the Jaguar outputs, one figure per step.

Usage:  python plot_results.py <figure> job.out [job2.out ...] --out results\plots\<name>
writes <name>.pdf and <name>.png, and prints the numbers that are plotted.

  convergence  C1   the five convergence criteria / threshold per geometry step, and E per step
  modes        C2   every vibration as a stick: frequency and IR intensity; imaginary ones below 0
  states       C2   computed IR spectrum of every state, scaled and broadened (--scale)
  s2           C3   <S**2> at every printed SCF, against 0.75 (doublet)
  thermo       C4   G of one state split into ZPE, trans., rot., vib., elec. and the 1 mol/L term
  conformers   C5   G of two conformers and their Boltzmann populations
  dispersion   L1   G with D3 minus G without, pairs given as with.out without.out ...
  ladder       L2   r(C=O), C=O stretch, lowest B3u mode and wall time, one point per rung
  solvation    L4a  single points: give gas, then the models, for Q and then for Q2- (--pairs)
  spectra      D3   computed spectra overlaid (scaled), with the experimental band positions
  checks       D4   change of G, lowest B3u, B2g and wall time against the first file
Only computed numbers are plotted; experimental values are the band positions and fundamentals
quoted in the README (D1-D3), drawn as lines, not the NIST spectrum.
"""

import argparse
import re
from pathlib import Path

import numpy as np
from summarise_job import HARTREE_KCAL, frequencies, last

RT = 0.0019872 * 298.15  # kcal/mol
HWHM = 10.0  # cm-1, as in ir_compare.py
EXP_BANDS = (1678, 1302, 1070, 1054, 882)  # NIST gas-phase band maxima (D1, D2)
EXP_LOW = (109, 241)  # tabulated fundamentals, NIST CCCBDB (D3)
CRITERIA = ("energy change", "gradient maximum", "gradient rms", "displacement maximum", "displacement rms")


def read(path):
    return Path(path).read_text(errors="replace")


def name(path):
    return Path(path).stem


def steps(t):
    """One dict per geometry step: total energy and value / threshold of each criterion printed."""
    out = []
    for block in re.split(r"Geometry optimization step", t)[1:]:
        head = block.split("predicted energy change")[0]
        row = {"E": float(re.search(r"Total energy:\s+(-?\d+\.\d+)", head).group(1))}
        for c in CRITERIA:
            m = re.search(rf"^\s+{c}:\s+(\S+)\s+\S\s+\(\s*(\S+)\s*\)", head, re.MULTILINE)
            if m:
                row[c] = abs(float(m.group(1))) / float(m.group(2))
        out.append(row)
    return out


def final_energy(t):
    return float(re.findall(r"^\s*SCFE:.*?(-?\d+\.\d+) hartrees", t, re.MULTILINE)[-1])


def gtot(t):
    return last(r"Total Gibbs free energy, Gtot \(Htot - T\*S\):\s+(-?\d+\.\d+)", t, float)


def hours(t):
    s = last(r"Total elapsed time:\s+(\d+)", t, int)
    return s / 3600 if s is not None else np.nan


def thermo_rows(t):
    """The last thermal table: {row: (U, Cv, S, H, G)} in kcal/mol and cal/(mol K)."""
    rows = {}
    for key in ("trans.", "rot.", "vib.", "elec.", "total"):
        hits = re.findall(rf"^  {re.escape(key)}\s+" + r"(-?\d+\.\d+)\s+" * 5, t, re.MULTILINE)
        if hits:
            rows[key] = tuple(float(x) for x in hits[-1])
    return rows


def first_of(freqs, syms, sym):
    return next((f for f, s in zip(freqs, syms) if s == sym and f > 0), np.nan)


def co_stretch(freqs, syms, ints):
    """The strongest B1u mode between 1550 and 1950 cm-1 (harmonic), or nan if there is none."""
    c = [(i, f) for f, s, i in zip(freqs, syms, ints) if s == "B1u" and 1550 < f < 1950]
    return max(c)[1] if c else np.nan


def broadened(freqs, ints, scale, grid):
    return sum(i * HWHM**2 / ((grid - f * scale) ** 2 + HWHM**2) for f, i in zip(freqs, ints) if f > 0)


def save(fig, stem):
    stem = Path(stem).with_suffix("")
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    for ext in (".pdf", ".png"):
        fig.savefig(stem.with_suffix(ext), dpi=200)
    print(f"wrote {stem}.pdf and {stem}.png")


def convergence(files, a, plt):
    fig, axes = plt.subplots(2, len(files), figsize=(3.2 * len(files), 5), squeeze=False, sharey="row")
    for k, p in enumerate(files):
        st = steps(read(p))
        n = np.arange(1, len(st) + 1)
        print(f"{name(p)}: {len(st)} steps")
        for c in CRITERIA:
            y = [s.get(c, np.nan) for s in st]
            axes[0, k].semilogy(n, y, "o-", label=c)
            print(f"  {c:22s} " + " ".join(f"{v:7.3f}" for v in y))
        axes[0, k].axhline(1, color="k", lw=0.8)
        axes[0, k].set(title=name(p), xticks=n)
        e = np.array([s["E"] for s in st])
        de = (e - e[-1]) * HARTREE_KCAL
        print("  E - E(last step) (kcal/mol) " + " ".join(f"{v:.3f}" for v in de))
        axes[1, k].plot(n, de, "o-k")
        axes[1, k].set(xlabel="geometry step", xticks=n)
    axes[0, 0].set_ylabel("value / threshold\n(met below 1)")
    axes[1, 0].set_ylabel("E $-$ E(last step) (kcal/mol)")
    axes[0, -1].legend(fontsize=7, frameon=False)
    return fig


def modes(files, a, plt):
    fig, axes = plt.subplots(len(files), 1, figsize=(6.5, 2.2 * len(files)), squeeze=False)
    for ax, p in zip(axes[:, 0], files):
        freqs, syms, ints = frequencies(read(p))
        f, i = np.array(freqs), np.array(ints)
        imag = f < 0
        print(f"{name(p)}: {len(f)} vibrations, {imag.sum()} imaginary {f[imag]}")
        ax.vlines(f[~imag], 0, i[~imag], color="C0")
        ax.plot(f[~imag], np.zeros((~imag).sum()), "|", color="C0", ms=8)
        if imag.any():
            ax.vlines(f[imag], 0, np.maximum(i[imag], 0.05 * i.max()), color="C3", lw=2)
            for x in f[imag]:
                ax.annotate(f"{x:.0f}i", (x, 0.05 * i.max()), color="C3", ha="left", va="bottom")
        ax.axvline(0, color="k", lw=0.6)
        ax.set(
            xlim=(min(f.min() - 150, -300), 3400), ylabel="I (km/mol)", title=f"{name(p)}: {len(f)} modes, {imag.sum()} imaginary"
        )
    axes[-1, 0].set_xlabel("harmonic frequency (cm$^{-1}$); imaginary drawn at its negative value")
    return fig


def states(files, a, plt):
    fig, ax = plt.subplots(figsize=(6.5, 1.0 + 0.75 * len(files)))
    grid = np.linspace(400, 1900, 1501)
    for k, p in enumerate(files):
        freqs, syms, ints = frequencies(read(p))
        y = broadened(freqs, ints, a.scale, grid)
        off = len(files) - 1 - k
        ax.plot(grid, y / y.max() + 1.1 * off, color=f"C{k}")
        ax.text(1890, 1.1 * off + 0.5, name(p), ha="left", va="center", fontsize=8)
        top = sorted(((i, f * a.scale) for f, i in zip(freqs, ints) if 400 < f * a.scale < 1900), reverse=True)[:2]
        print(f"{name(p):12s} strongest (scaled): " + ", ".join(f"{f:.0f} ({i:.0f} km/mol)" for i, f in top))
    ax.set(xlim=(1900, 400), yticks=[], xlabel=f"wavenumber (cm$^{{-1}}$), harmonic x {a.scale}")
    ax.set_ylabel("each spectrum normalised to its strongest band")
    return fig


def s2(files, a, plt):
    fig, ax = plt.subplots(figsize=(5, 3))
    for p in files:
        v = [float(x) for x in re.findall(r"<S\*\*2> \.\.\.\s+(\S+)", read(p))]
        print(f"{name(p)}: {len(v)} values, from {min(v):.3f} to {max(v):.3f}")
        ax.plot(range(1, len(v) + 1), v, "o-", label=name(p))
    ax.axhline(0.75, color="k", lw=0.8)
    ax.axhline(0.825, color="k", lw=0.8, ls="--")
    ax.text(1, 0.7485, "0.75, pure doublet", fontsize=8, va="top")
    ax.text(1, 0.827, "0.825, 10 % above (rule of thumb)", fontsize=8, va="bottom")
    ax.set(xlabel="printed <S$^2$> line (SCF of each step)", ylabel="<S$^2$>", ylim=(0.74, 0.85))
    ax.legend(frameon=False)
    return fig


def thermo(files, a, plt):
    t = read(files[0])
    rows = thermo_rows(t)
    zpe = last(r"The zero point energy \(ZPE\):\s+(-?\d+\.\d+)", t, float)
    floor = last(r"minimum value of\s+(\S+) cm\^-1", t, float)
    parts = {"ZPE": zpe} | {k.rstrip("."): rows[k][4] for k in ("trans.", "rot.", "vib.", "elec.")}
    parts["1 atm -> 1 mol/L"] = RT * np.log(24.46)
    for k, v in parts.items():
        print(f"  {k:18s} {v:+8.3f} kcal/mol")
    print(f"  sum {sum(parts.values()):+.3f}; G - E printed {(gtot(t) - final_energy(t)) * HARTREE_KCAL:+.3f} (without 1 mol/L)")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3), gridspec_kw={"width_ratios": [1.3, 1]})
    ax1.bar(range(len(parts)), list(parts.values()), color=["C1"] + ["C0"] * 4 + ["C2"])
    ax1.set_xticks(range(len(parts)), list(parts), rotation=30, ha="right", fontsize=8)
    ax1.axhline(0, color="k", lw=0.6)
    ax1.set(ylabel="contribution to G $-$ E (kcal/mol)", title=f"{name(files[0])}, 298.15 K")
    for k, v in enumerate(parts.values()):
        ax1.text(k, v, f"{v:+.2f}", ha="center", va="bottom" if v > 0 else "top", fontsize=7)
    for k, p in enumerate(files):
        f = np.array(frequencies(read(p))[0])
        ax2.plot(f[:6], [k] * min(6, len(f)), "|", ms=12, color="C0")
        if (f < 0).any():  # imaginary modes, drawn at their negative value
            ax2.plot(f[f < 0], [k] * (f < 0).sum(), "|", ms=12, mew=2, color="C3")
        print(f"  {name(p):12s} lowest: " + ", ".join(f"{x:.1f}" for x in f[:4]))
    if floor:
        ax2.axvline(floor, color="C3", lw=1)
        ax2.text(floor, len(files) - 0.4, f" floor {floor:.0f}", color="C3", fontsize=8)
    ax2.set_yticks(range(len(files)), [name(p) for p in files], fontsize=8)
    ax2.set(xlabel="six lowest modes (cm$^{-1}$), imaginary in red", xlim=(-400, 600), ylim=(-0.6, len(files) - 0.2))
    ax2.axvline(0, color="k", lw=0.6)
    return fig


def conformers(files, a, plt):
    g = np.array([gtot(read(p)) for p in files])
    dg = (g - g.min()) * HARTREE_KCAL
    w = np.exp(-dg / RT)
    pop = w / w.sum()
    mix = g.min() - RT * np.log(w.sum()) / HARTREE_KCAL
    for p, d, q in zip(files, dg, pop):
        print(f"  {name(p):12s} dG {d:+.2f} kcal/mol  {100 * q:.1f} %")
    print(f"  mixture G {mix:.6f} Eh, {(mix - g.min()) * HARTREE_KCAL:+.2f} kcal/mol from the lowest")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 2.8))
    labels = [name(p) for p in files]
    ax1.bar(labels, dg, color="C0")
    ax1.axhline(RT, color="k", ls="--", lw=0.8)
    ax1.text(-0.4, RT, " RT = 0.59", fontsize=8, va="bottom")
    ax1.set(ylabel="G $-$ G(lowest) (kcal/mol)")
    ax2.bar(labels, 100 * pop, color="C2")
    for k, q in enumerate(pop):
        ax2.text(k, 100 * q, f"{100 * q:.1f} %", ha="center", va="bottom", fontsize=8)
    ax2.set(ylabel="Boltzmann population (%)", ylim=(0, 100))
    return fig


def dispersion(files, a, plt):
    pairs = list(zip(files[::2], files[1::2]))
    d = [(gtot(read(w)) - gtot(read(wo))) * HARTREE_KCAL for w, wo in pairs]
    for (w, wo), v in zip(pairs, d):
        print(f"  {name(w):12s} - {name(wo):18s} {v:+.2f} kcal/mol")
    step = d[1] - d[0]
    print(f"  change of the {name(pairs[0][0])} -> {name(pairs[1][0])} step: {step:+.2f} kcal/mol = {-step / 46.12:+.3f} V (2e-)")
    fig, ax = plt.subplots(figsize=(5, 3))
    labels = [name(w) for w, _ in pairs] + [f"step {name(pairs[0][0])}\n-> {name(pairs[1][0])}"]
    vals = d + [step]
    ax.bar(labels, vals, color=["C0"] * len(d) + ["C3"])
    for k, v in enumerate(vals):
        ax.text(k, v, f"{v:+.2f}", ha="center", va="top", fontsize=8)
    ax.axhline(0, color="k", lw=0.6)
    ax.axhline(-4.6, color="k", ls="--", lw=0.8)
    ax.text(len(vals) - 0.5, -4.6, "0.1 V (2e$^-$) ", ha="right", va="bottom", fontsize=8)
    ax.set(ylabel="G(with D3) $-$ G(without) (kcal/mol)")
    return fig


def ladder(files, a, plt):
    rows = []
    for p in files:
        t = read(p)
        freqs, syms, ints = frequencies(t)
        nimag = sum(f < 0 for f in freqs)
        rows.append(
            (name(p), last(r"O1\s+-C1\s+:\s+(\S+)", t, float), co_stretch(freqs, syms, ints), first_of(freqs, syms, "B3u"), hours(t), nimag)
        )
    for r in rows:
        print(f"  {r[0]:18s} r(C=O) {r[1]:.3f}  C=O {r[2]:7.1f}  B3u {r[3]:6.1f}  {r[4]:.2f} h  imaginary {r[5]}")
    fig, axes = plt.subplots(1, 4, figsize=(10, 3), sharex=True)
    x = np.arange(len(rows))
    for ax, col, lab in zip(axes, (1, 2, 3, 4), ("r(C=O) (Å)", "C=O stretch, harmonic (cm$^{-1}$)", "lowest B3u (cm$^{-1}$)", "wall time (h)")):
        y = np.array([r[col] for r in rows])
        bad = np.array([r[5] > 0 for r in rows])
        ax.plot(x, y, "-", color="0.7")
        ax.plot(x[~bad], y[~bad], "o", color="C0")
        ax.plot(x[bad], y[bad], "x", color="C3", ms=8, mew=2, label="not a minimum")
        ax.set_ylabel(lab)
    axes[1].axhline(1668, color="k", ls="--", lw=0.8)
    axes[1].text(0, 1668, "exp. 1668", fontsize=8, va="bottom")
    axes[2].axhline(109, color="k", ls="--", lw=0.8)
    axes[2].text(0, 109, "exp. 109", fontsize=8, va="bottom")
    axes[0].legend(fontsize=7, frameon=False)
    for ax in axes:
        ax.set_xticks(x, [r[0].replace("bq_Q_", "") for r in rows], rotation=45, ha="right", fontsize=7)
    return fig


def solvation(files, a, plt):
    n = len(files) // 2
    q, q2 = files[:n], files[n:]
    eq = np.array([final_energy(read(p)) for p in q])
    e2 = np.array([final_energy(read(p)) for p in q2])
    labels = [name(p).rsplit("_", 1)[-1] for p in q]
    dq, d2 = (eq - eq[0]) * HARTREE_KCAL, (e2 - e2[0]) * HARTREE_KCAL
    de = (e2 - eq) * HARTREE_KCAL
    for row in zip(labels, dq, d2, de):
        print("  {:6s} dGsolv(Q) {:+8.2f}  dGsolv(Q2-) {:+8.2f}  dE(Q->Q2-) {:+8.2f} kcal/mol".format(*row))
    spread = de[1:].max() - de[1:].min()
    print(f"  spread of dE over the solvent models {spread:.1f} kcal/mol = {spread / 46.12:.2f} V (2e-)")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3))
    x = np.arange(1, n)
    ax1.bar(x - 0.2, dq[1:], 0.4, label="Q")
    ax1.bar(x + 0.2, d2[1:], 0.4, label="Q$^{2-}$")
    ax1.set_xticks(x, labels[1:])
    ax1.set(ylabel="$\\Delta G_\\mathrm{solv}$ = E(model) $-$ E(gas) (kcal/mol)")
    ax1.set_ylim(min(d2.min(), dq.min()) * 1.25, 0)
    ax1.legend(frameon=False, loc="lower center", ncol=2)
    ax2.bar(range(n), de, color=["0.6"] + ["C0"] * (n - 1))
    for k, v in enumerate(de):
        ax2.text(k, v, f"{v:+.1f}", ha="center", va="bottom" if v > 0 else "top", fontsize=8)
    ax2.axhline(0, color="k", lw=0.6)
    ax2.set_xticks(range(n), labels)
    ax2.set(ylabel="E(Q$^{2-}$) $-$ E(Q) (kcal/mol)", title=f"spread {spread:.1f} kcal/mol = {spread / 46.12:.2f} V (2e$^-$)")
    return fig


def spectra(files, a, plt):
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    grid = np.linspace(50, 1900, 1851)
    for k, p in enumerate(files):
        freqs, syms, ints = frequencies(read(p))
        y = broadened(freqs, ints, a.scale, grid)
        ax.plot(grid, y / y.max(), color=f"C{k}", label=f"{name(p)}, x {a.scale}")
        co = co_stretch(freqs, syms, ints) * a.scale
        low = [first_of(freqs, syms, s) * a.scale for s in ("B3u", "B2g")]
        print(f"  {name(p):12s} C=O scaled {co:.1f}; lowest B3u, B2g scaled " + ", ".join(f"{x:.1f}" for x in low))
    for x in EXP_BANDS:
        ax.axvline(x, color="k", ls="--", lw=0.6)
    for x in EXP_LOW:
        ax.axvline(x, color="k", ls=":", lw=0.8)
    ax.plot([], [], "k--", lw=0.6, label="exp. band maxima (D2)")
    ax.plot([], [], "k:", lw=0.8, label="exp. fundamentals 109, 241 (D3)")
    ax.set(xlim=(1900, 50), xlabel="wavenumber (cm$^{-1}$)", ylabel="normalised absorbance (calc.)")
    ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2)
    return fig


def checks(files, a, plt):
    ref = read(files[0])
    g0, f0 = gtot(ref), frequencies(ref)
    rows = []
    for p in files[1:]:
        t = read(p)
        f = frequencies(t)
        rows.append(
            (
                name(p).rsplit("_", 1)[-1],
                (gtot(t) - g0) * HARTREE_KCAL,
                first_of(f[0], f[1], "B3u") - first_of(f0[0], f0[1], "B3u"),
                first_of(f[0], f[1], "B2g") - first_of(f0[0], f0[1], "B2g"),
                hours(t) / hours(ref),
            )
        )
    for r in rows:
        print(f"  {r[0]:6s} dG {r[1]:+.3f} kcal/mol  dB3u {r[2]:+.1f}  dB2g {r[3]:+.1f} cm-1  cost x {r[4]:.2f}")
    fig, axes = plt.subplots(1, 4, figsize=(10, 2.8), sharex=True)
    x = np.arange(len(rows))
    labs = ("$\\Delta G$ (kcal/mol)", "$\\Delta$ lowest B3u (cm$^{-1}$)", "$\\Delta$ B2g (cm$^{-1}$)", f"wall time / {name(files[0])}")
    for ax, col, lab in zip(axes, (1, 2, 3, 4), labs):
        y = [r[col] for r in rows]
        ax.bar(x, y, color=["C3" if r[0] == "tzvp" else "C0" for r in rows])
        for k, v in enumerate(y):
            ax.text(k, v, f"{v:+.2f}" if col < 4 else f"{v:.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=7)
        ax.axhline(1 if col == 4 else 0, color="k", lw=0.6)
        ax.set_ylabel(lab)
        ax.set_xticks(x, [r[0] for r in rows])
    return fig


FIGURES = dict(
    convergence=convergence,
    modes=modes,
    states=states,
    s2=s2,
    thermo=thermo,
    conformers=conformers,
    dispersion=dispersion,
    ladder=ladder,
    solvation=solvation,
    spectra=spectra,
    checks=checks,
)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("figure", choices=FIGURES)
    ap.add_argument("outputs", nargs="+")
    ap.add_argument("--out", required=True, help="file name without extension; .pdf and .png are written")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    save(FIGURES[a.figure](a.outputs, a, plt), a.out)


if __name__ == "__main__":
    main()
