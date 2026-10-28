"""Compare computed IR frequencies from a Jaguar .out with an experimental JCAMP-DX spectrum.

Usage:  python ir_compare.py job.out [--scale 0.9626] [--exp spectrum.jdx] [--plot fig.pdf]
"""

import argparse
import re

import numpy as np
from summarise_job import frequencies


def read_jcamp(path):
    """Read an (X++(Y..Y)) JCAMP-DX spectrum, as served by the NIST Chemistry WebBook."""
    head, x, y = {}, [], []
    data = False
    with open(path, errors="replace") as fh:
        lines = fh.readlines()
    for line in lines:
        if line.startswith("##"):
            key, _, val = line[2:].partition("=")
            head[key.strip().upper()] = val.strip()
            data = key.strip().upper() == "XYDATA"
            continue
        if data and line.strip():
            vals = [float(v) for v in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", line)]
            x0 = vals[0] * float(head.get("XFACTOR", 1))
            x += [x0 + i * float(head["DELTAX"]) for i in range(len(vals) - 1)]
            y += vals[1:]
    order = np.argsort(x)
    x, y = np.array(x)[order], np.array(y)[order] * float(head.get("YFACTOR", 1))
    if head.get("YUNITS", "").upper().startswith("TRANSMITTANCE"):
        y = -np.log10(np.clip(y, 1e-4, None))
    return x, y / y.max(), head


def peaks(x, y, min_height=0.1):
    """Local maxima over five points above min_height, strongest first."""
    i = [k for k in range(2, len(y) - 2) if y[k] == y[k - 2 : k + 3].max() and y[k] > min_height]
    return sorted(zip(x[i], y[i]), key=lambda p: -p[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--exp")
    ap.add_argument("--plot")
    a = ap.parse_args()
    with open(a.out, errors="replace") as fh:
        freqs, syms, ints = frequencies(fh.read())
    imax = max(ints)
    print(f"{'mode':>4s} {'sym':>4s} {'harmonic':>9s} {'scaled':>8s} {'I (km/mol)':>10s} {'rel':>5s}")
    for k, (f, s, i) in enumerate(zip(freqs, syms, ints), 1):
        mark = "  <- IR active" if i / imax > 0.05 else ""
        print(f"{k:4d} {s:>4s} {f:9.1f} {f * a.scale:8.1f} {i:10.2f} {i / imax:5.2f}{mark}")
    if a.exp:
        x, y, head = read_jcamp(a.exp)
        print(f"\nexperiment: {head.get('TITLE')} | {head.get('STATE', '')} | {head.get('ORIGIN', '')}")
        print(f"{'exp peak':>9s} {'rel':>5s} {'nearest scaled':>15s} {'sym':>4s} {'error':>7s}")
        active = [(f * a.scale, s) for f, s, i in zip(freqs, syms, ints) if i / imax > 0.02]
        for xp, yp in peaks(x, y):
            f, s = min(active, key=lambda c: abs(c[0] - xp))
            print(f"{xp:9.0f} {yp:5.2f} {f:15.1f} {s:>4s} {f - xp:+7.1f}")
    if a.plot:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6.5, 3))
        grid = np.linspace(400, 4000, 3601)
        calc = sum(i * 10**2 / ((grid - f * a.scale) ** 2 + 10**2) for f, i in zip(freqs, ints))
        ax.plot(grid, calc / calc.max(), label=f"calc. x {a.scale}")
        if a.exp:
            ax.plot(x, y, color="k", lw=0.8, label="experiment (NIST)")
        ax.set(xlim=(4000, 400), xlabel="wavenumber (cm$^{-1}$)", ylabel="normalised absorbance")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(a.plot)
        print(f"\nwrote {a.plot}")


if __name__ == "__main__":
    main()
