"""
Paper-ready PID figures.

Creates (in ./figures):
  pid_response_side.pdf    - 2 panels side by side, fits ONE column of a two-column paper
  pid_response_column.pdf  - 2 panels stacked, also one column
  pid_kp_sweep.pdf         - Kp sweep (elbow) metrics, one column

Figures are drawn at their real printed size (one column = 3.5 in), so the font
sizes here are the font sizes in the paper. Do not scale them in LaTeX: use
  \\includegraphics{figures/pid_response_side.pdf}   (no width=...)

Run from the test_system folder:
  python pid_paper_figures.py
"""
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch

LOG_DIR = "pid_log"
OUT_DIR = "figures"
WINDOW = 10          # seconds shown
BAND = 10            # +-px "on target" zone

BASELINE_FILE = "pid_log_20260531_174435_val.csv"
YAW_FILE = "pid_log_20260531_191225_p3yaw_BANG.csv"      # P-only Kp=3 on yaw (horizontal)
VERT_FILE = "pid_log_20260531_191619_p3pitch_BANG.csv"   # P-only Kp=3 on vertical

# Colour-blind safe (Okabe-Ito)
C_BASE = "#D55E00"
C_P3 = "#0072B2"
C_BAND = "#009E73"
M_BASE = "s"         # square markers for the baseline
M_P3 = "o"           # circle markers for Kp=3
LW_BASE = 0.8        # line widths
LW_P3 = 1.0
MS = 3.5             # marker size

# IEEE / most two-column journals: one column is ~3.5 in wide
COL_W = 3.5

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,     # editable text in the PDF, accepted by IEEE PDF eXpress
    "savefig.dpi": 600,
})


def load(name):
    df = pd.read_csv(os.path.join(LOG_DIR, name))
    t = (df["timestamp"] - df["timestamp"].iloc[0]).values
    m = t <= WINDOW
    return df, t[m], df["pixel_error_x"].values[m], df["pixel_error_y"].values[m]


def gains(df, axis):
    """Return a short gain string, e.g. 'K_p=1.5, K_i=1.0' (zero terms are left out)."""
    r = df.iloc[0]
    kp, ki, kd = r[f"{axis}_kp"], r[f"{axis}_ki"], r[f"{axis}_kd"]
    parts = [f"Kp={kp:g}"]
    if ki:
        parts.append(f"Ki={ki:g}")
    if kd:
        parts.append(f"Kd={kd:g}")
    return ", ".join(parts)


def save(fig, name):
    """Save PDF + PNG. Retries because OneDrive sometimes locks the file while syncing."""
    for ext in ("pdf", "png"):
        path = os.path.join(OUT_DIR, f"{name}.{ext}")
        for attempt in range(5):
            try:
                fig.savefig(path)
                break
            except OSError:
                if attempt == 4:
                    raise
                time.sleep(1)
    plt.close(fig)
    print("Saved", name)


def first_settle(t, e):
    """Same definition as pid_evaluate.py: first time |e| < BAND."""
    idx = np.where(np.abs(e) < BAND)[0]
    return t[idx[0]] if len(idx) else None


def panel(ax, title, ylabel, series, title_size=7):
    ax.axhspan(-BAND, BAND, color=C_BAND, alpha=0.12, lw=0, zorder=0)
    ax.axhline(0, color="black", lw=0.4, alpha=0.4, zorder=1)

    for i, (t, e, color, marker, ls, label) in enumerate(series):
        # one marker per second, shifted per series so they don't overlap
        marks = np.unique(np.searchsorted(t, np.arange(i / len(series), WINDOW, 1.0)))
        marks = marks[marks < len(t)]
        ax.plot(t, e, color=color, lw=LW_BASE if i == 0 else LW_P3, ls=ls, label=label, zorder=3,
                marker=marker, ms=MS, markevery=list(marks),
                markerfacecolor="white", markeredgewidth=0.8)

    # mark when the Kp=3 controller first reaches the zone
    t, e, color = series[-1][0], series[-1][1], series[-1][2]
    ts = first_settle(t, e)
    if ts is not None:
        ax.axvline(ts, color=color, lw=0.7, ls=":", zorder=2)
        ax.annotate(rf"$t_s$={ts:.1f} s", xy=(ts, 0.5), xycoords=("data", "axes fraction"),
                    xytext=(2, 0), textcoords="offset points", va="center",
                    color=color, fontsize=8)

    ax.set_title(title, fontweight="bold", fontsize=title_size)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel, labelpad=1)
    ax.set_xlim(0, WINDOW)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax.grid(axis="y", color="black", alpha=0.08, lw=0.4)


def response_series():
    base_df, tb, exb, eyb = load(BASELINE_FILE)
    yaw_df, ty, exy, _ = load(YAW_FILE)
    vert_df, tv, _, eyv = load(VERT_FILE)

    horiz = [
        (tb, exb, C_BASE, M_BASE, "--", "Baseline PID"),
        (ty, exy, C_P3, M_P3, "-", r"P-only, $K_p$=3"),
    ]
    vert = [
        (tb, eyb, C_BASE, M_BASE, "--", "Baseline PID"),
        (tv, eyv, C_P3, M_P3, "-", r"P-only, $K_p$=3"),
    ]
    print("Gains for the caption:")
    print("  Baseline yaw:", gains(base_df, "yaw"), "| vertical:", gains(base_df, "pitch"))
    print("  P-only   yaw:", gains(yaw_df, "yaw"), "| vertical:", gains(vert_df, "pitch"))
    return horiz, vert


def fig_response(layout):
    horiz, vert = response_series()
    if layout == "side":
        fig, axes = plt.subplots(1, 2, figsize=(COL_W, 2.1), constrained_layout=True)
    else:
        fig, axes = plt.subplots(2, 1, figsize=(COL_W, 4.0), constrained_layout=True)
    fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, wspace=0.03)

    panel(axes[0], r"Horizontal Error ($d_x$) over time", r"Error on $d_x$ (px)", horiz)
    panel(axes[1], r"Vertical Error ($d_y$) over time", r"Error on $d_y$ (px)", vert)

    h, l = axes[0].get_legend_handles_labels()
    h.append(Patch(facecolor=C_BAND, alpha=0.25, lw=0))
    l.append(rf"$\pm${BAND} px")
    fig.legend(h, l, loc="outside upper center", ncol=3, frameon=False,
               handlelength=2.4, columnspacing=1.0, handletextpad=0.4)

    name = f"pid_response_{layout}"
    save(fig, name)


# Yaw Kp sweep runs (all P-only): (file, Kp, colour, marker)
SWEEP_FILES = [
    ("pid_log_20260531_183721_p0,5.csv", 0.5, "#E69F00", "v"),
    ("pid_log_20260531_184007_p1.csv", 1.0, "#56B4E9", "^"),
    ("pid_log_20260531_184545_p1,5.csv", 1.5, "#009E73", "D"),
    ("pid_log_20260531_184328_p2.csv", 2.0, "#CC79A7", "p"),
    (YAW_FILE, 3.0, C_P3, M_P3),
]


def fig_kp_response():
    """Horizontal error over time for the baseline and every yaw Kp in the sweep."""
    _, tb, exb, _ = load(BASELINE_FILE)
    series = [(tb, exb, C_BASE, M_BASE, "--", "Baseline PID")]
    for name, kp, color, marker in SWEEP_FILES:
        df, t, ex, _ = load(name)
        assert df["yaw_kp"].iloc[0] == kp and df["yaw_ki"].iloc[0] == 0, name
        series.append((t, ex, color, marker, "-", rf"$K_p$={kp:g}"))

    # a bit wider than tall
    fig, ax = plt.subplots(figsize=(2.85, 2.3), constrained_layout=True)
    fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02)
    panel(ax, r"Horizontal Error ($d_x$) over time", r"Error on $d_x$ (px)", series, title_size=8)

    h, l = ax.get_legend_handles_labels()
    h.append(Patch(facecolor=C_BAND, alpha=0.25, lw=0))
    l.append(rf"$\pm${BAND} px")
    fig.legend(h, l, loc="outside upper center", ncol=4, frameon=False, fontsize=7,
               handlelength=1.8, columnspacing=0.6, handletextpad=0.3, labelspacing=0.2)
    save(fig, "pid_response_kp_sweep")


def fig_kp_sweep():
    # Values from elbow_method.py (yaw Kp sweep)
    kp = [0.5, 1.0, 1.5, 2.0, 3.0]
    iae = [22187.2, 14785.6, 11799.3, 5368.3, 1115.4]
    itae = [653727.4, 595677.8, 596421.6, 114731.3, 9592.8]
    settle = [None, None, None, 8.69, 3.23]
    overshoot = [None, None, 180.8, 235.4, 45.1]
    initial_err = [-307.1, -167.2, -159.3, -185.5, -367.8]
    overshoot_pct = [abs(o / e) * 100 if o is not None else None
                     for o, e in zip(overshoot, initial_err)]

    def norm(x):
        a = np.array([v if v is not None else np.nan for v in x], dtype=float)
        return a / np.nanmax(a)

    fig, ax = plt.subplots(figsize=(COL_W, 2.6), constrained_layout=True)
    styles = [
        (norm(iae), "IAE", "#0072B2", "o", "-"),
        (norm(itae), "ITAE", "#E69F00", "^", "-"),
        (norm(overshoot_pct), "Overshoot", "#009E73", "D", "--"),
        (norm(settle), "Settling time", "#CC79A7", "s", "--"),
    ]
    for y, label, c, m, ls in styles:
        ax.plot(kp, y, color=c, marker=m, ls=ls, lw=0.9, ms=4.5, label=label)

    ax.axvline(3.0, color="black", lw=0.6, ls=":", alpha=0.6)
    ax.annotate(r"chosen $K_p$ = 3", xy=(3.0, 1.0), xytext=(-4, 0), textcoords="offset points",
                ha="right", va="center", fontsize=8)
    ax.set_xlabel(r"Yaw $K_p$")
    ax.set_ylabel("Normalised metric")
    ax.set_xticks(kp)
    ax.set_ylim(-0.03, 1.08)
    ax.grid(axis="y", color="black", alpha=0.08, lw=0.4)
    ax.legend(loc="lower left", frameon=True, framealpha=0.9, edgecolor="none",
              borderpad=0.3, labelspacing=0.25)
    save(fig, "pid_kp_sweep")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    fig_response("side")
    fig_response("column")
    fig_kp_response()
    fig_kp_sweep()
