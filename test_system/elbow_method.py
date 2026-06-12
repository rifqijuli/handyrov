import matplotlib.pyplot as plt
import numpy as np

kp          = [0.5, 1.0, 1.5, 2.0, 3.0]
iae         = [22187.2, 14785.6, 11799.3, 5368.3, 1115.4]
ise         = [8231218.5, 2607330.8, 1399494.4, 656263.4, 208624.8]
itae        = [653727.4, 595677.8, 596421.6, 114731.3, 9592.8]
settle      = [None, None, None, 8.69, 3.23]
overshoot   = [None, None, 180.8, 235.4, 45.1]
initial_err = [-307.1, -167.2, -159.3, -185.5, -367.8]

overshoot_pct = [
    abs(o / e) * 100 if o is not None else None
    for o, e in zip(overshoot, initial_err)
]

# --- Print table ---
print(f"{'Kp':<6} {'Settle(s)':<12} {'Overshoot%':<13} {'IAE':<12} {'ISE':<14} {'ITAE':<12}")
print("-" * 69)
for i, k in enumerate(kp):
    st  = f"{settle[i]:.2f}"       if settle[i]      is not None else "Never"
    ov  = f"{overshoot_pct[i]:.1f}" if overshoot_pct[i] is not None else "N/A"
    print(f"{k:<6} {st:<12} {ov:<13} {iae[i]:<12.1f} {ise[i]:<14.1f} {itae[i]:<12.1f}")

# --- Normalize helper (handles None) ---
def norm(x):
    arr = np.array([v if v is not None else np.nan for v in x], dtype=float)
    return arr / np.nanmax(arr)

# --- Plot ---
fig, ax1 = plt.subplots(figsize=(7, 8))

ax1.plot(kp, norm(iae),          marker='o', label='IAE (norm)')
#ax1.plot(kp, norm(ise),          marker='s', label='ISE (norm)')
ax1.plot(kp, norm(itae),         marker='^', label='ITAE (norm)')
ax1.plot(kp, norm(overshoot_pct),marker='D', linestyle='--', label='Overshoot % (norm)')
ax1.plot(kp, norm(settle),       marker='x', linestyle='--', label='Settling Time (norm)')
ax1.tick_params(colors="black", labelsize=20)
for spine in ax1.spines.values():
    spine.set_edgecolor("#999")

ax1.set_xlabel('$K_p$', fontsize=20)
ax1.set_ylabel('Normalized Metric', fontsize=20)
ax1.set_title('PID Performance Comparison', fontsize=20, fontweight='bold')
ax1.legend(fontsize=20, facecolor="white", edgecolor="#ccc", loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2, frameon=True)
ax1.grid(axis="y", color="black", alpha=0.08, linewidth=0.6)
ax1.grid(axis="x", color="black", alpha=0.05, linewidth=0.6)

plt.tight_layout()
plt.savefig('elbow_yaw.pdf', dpi=150)
plt.show()
plt.close()
print("\nSaved: elbow_yaw.pdf")
