import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

mode = "isolate"

FILES = [
    ("pid_log/pid_log_20260531_191619_p3pitch_BANG.csv", "Kp=3.0", "#31d100", "p"),  # Kp=3.0 pitch (vertical)
    #("pid_log/pid_log_20260531_183721_p0,5.csv", "Kp=0.5",             "#eb0b56", "x"),
    #("pid_log/pid_log_20260531_184007_p1.csv",          "Kp=1.0",             "#ff9f43", "s"),
    #("pid_log/pid_log_20260531_184545_p1,5.csv", "Kp=1.5",             "#ffbf69", "^"),
    #("pid_log/pid_log_20260531_184328_p2.csv",   "Kp=2.0",             "#500092", "D"),
    ("pid_log/pid_log_20260531_191225_p3yaw_BANG.csv",   "Kp=3.0",             "#6890ff", "o"),
    ("pid_log/pid_log_20260531_174435_val.csv",          "Baseline", "#ff6f9f", "v"),
]

WINDOW = 10
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")  # Subscript digits for legend labels
SUBdxdy = str.maketrans("xy", "ₓᵧ")  # Subscript 'x' and 'y' for axis labels
yaw_label_title = "Horizontal Error (dx) over time"
vert_label_title = "Vertical Error (dy) over time"
y_axis_label_on_yaw = "Error on X (dx)"
y_axis_label_on_vert = "Error on Y (dy)"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7.5))
#fig, ax = plt.subplots(figsize=(7, 7.5))
fig.patch.set_facecolor("white")


for ax in (ax1, ax2):
    ax.set_facecolor("white")
    ax.tick_params(colors="black", labelsize=20)
    ax.xaxis.label.set_color("black")
    ax.yaxis.label.set_color("black")
    ax.title.set_color("black")
    for spine in ax.spines.values():
        spine.set_edgecolor("#999")

'''

ax.set_facecolor("white")
ax.tick_params(colors="black", labelsize=20)
ax.xaxis.label.set_color("black")
ax.yaxis.label.set_color("black")
ax.title.set_color("black")
for spine in ax.spines.values():
    spine.set_edgecolor("#999")
'''

for filepath, label, color, marker in FILES:
    df   = pd.read_csv(filepath)
    t    = df['timestamp'] - df['timestamp'].iloc[0]
    mask = t <= WINDOW
    t_w  = t[mask].values
    ex   = df['pixel_error_x'][mask].values
    ey   = df['pixel_error_y'][mask].values
    if mode == "isolate":
        if color == "#31d100":  # Kp=3.0 pitch (vertical)
            ax2.plot(t_w, ey, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=10)
        elif color == "#6890ff":  # Kp=3.0 yaw (horizontal)
            ax1.plot(t_w, ex, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=10)
        else:
            ax1.plot(t_w, ex, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=5)
            ax2.plot(t_w, ey, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=5)
    elif mode == "sweep":
        ax.plot(t_w, ex, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=10)
    else:
        ax1.plot(t_w, ex, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=5)
        ax2.plot(t_w, ey, label=label, color=color, linewidth=1.5, marker=marker, markersize=8, markevery=5)

for ax, title, ylabel in [
    (ax1, yaw_label_title.translate(SUBdxdy), y_axis_label_on_yaw.translate(SUBdxdy)),
    (ax2, vert_label_title.translate(SUBdxdy), y_axis_label_on_vert.translate(SUBdxdy)),
]:
    ax.axhline( 10, color="#15803d", linestyle="--", linewidth=1.0, alpha=0.7, label="±10 px zone")
    ax.axhline(-10, color="#15803d", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.axhline(  0, color="black",   linestyle=":",  linewidth=0.6, alpha=0.2)
    ax.set_title(title, fontsize=20, fontweight="bold", pad=8)
    ax.set_xlabel("Time [k] (s)", fontsize=20)
    ax.set_ylabel(ylabel,     fontsize=20)
    ax.set_xlim(0, WINDOW)
    ax.legend(fontsize=20, facecolor="white", edgecolor="#ccc", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=True)
    ax.grid(axis="y", color="black", alpha=0.08, linewidth=0.6)
    ax.grid(axis="x", color="black", alpha=0.05, linewidth=0.6)
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

#fig.suptitle("PID Tuning Comparison — First 10 Seconds", fontsize=13, fontweight="bold", color="black", y=1.01)
plt.tight_layout()
plt.savefig("pid_comparison_print.pdf", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()