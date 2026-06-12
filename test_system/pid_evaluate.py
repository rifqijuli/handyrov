import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def pid_metrics(filepath, label):
    df = pd.read_csv(filepath)
    t = df['timestamp'] - df['timestamp'].iloc[0]
    dt = np.diff(t.values)

    ex = df['pixel_error_x'].values
    ey = df['pixel_error_y'].values

    # Yaw metrics
    iae_x  = np.sum(np.abs(ex[:-1]) * dt)
    itae_x = np.sum(t.values[:-1] * np.abs(ex[:-1]) * dt)
    ise_x  = np.sum(ex[:-1]**2 * dt)

    # Pitch metrics
    iae_y  = np.sum(np.abs(ey[:-1]) * dt)
    itae_y = np.sum(t.values[:-1] * np.abs(ey[:-1]) * dt)
    ise_y  = np.sum(ey[:-1]**2 * dt)

    # Settling time yaw (|error_x| < 10px)
    settle_x = t[np.where(np.abs(ex) < 10)[0]]
    settle_t_x = settle_x.iloc[0] if len(settle_x) > 0 else None

    # Settling time pitch (|error_y| < 10px)
    settle_y = t[np.where(np.abs(ey) < 10)[0]]
    settle_t_y = settle_y.iloc[0] if len(settle_y) > 0 else None

    # Overshoot yaw
    zc_x = np.where(np.diff(np.sign(ex)))[0]
    overshoot_x = np.max(np.abs(ex[zc_x[0]:])) if len(zc_x) > 0 else 0

    # Overshoot pitch
    zc_y = np.where(np.diff(np.sign(ey)))[0]
    overshoot_y = np.max(np.abs(ey[zc_y[0]:])) if len(zc_y) > 0 else 0

    print(f"\n=== {label} ===")
    print(f"  Kp (yaw):         {df['yaw_kp'].iloc[0]}")
    print(f"  --- Yaw ---")
    print(f"  Initial error:    {ex[1]:.1f} px")
    print(f"  Settling time:    {settle_t_x:.2f} s" if settle_t_x else "  Settling time:    Never")
    print(f"  Overshoot:        {overshoot_x:.1f} px ({overshoot_x/abs(ex[1])*100:.1f}%)")
    print(f"  IAE:              {iae_x:.1f}")
    print(f"  ITAE:             {itae_x:.1f}")
    print(f"  ISE:              {ise_x:.1f}")
    print(f"  --- Vertical ---")
    print(f"  Initial error:    {ey[1]:.1f} px")
    print(f"  Settling time:    {settle_t_y:.2f} s" if settle_t_y else "  Settling time:    Never")
    print(f"  Overshoot:        {overshoot_y:.1f} px ({overshoot_y/abs(ey[1])*100:.1f}%)")
    print(f"  IAE:              {iae_y:.1f}")
    print(f"  ITAE:             {itae_y:.1f}")
    print(f"  ISE:              {ise_y:.1f}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(t, ex)
    ax1.axhline(10, color='green', linestyle='--', alpha=0.5)
    ax1.axhline(-10, color='green', linestyle='--', alpha=0.5, label='±10px zone')
    ax1.set_title(f"Yaw Error — {label}")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Pixel Error X")
    ax1.legend()

    ax2.plot(t, ey, color='orange')
    ax2.axhline(10, color='green', linestyle='--', alpha=0.5)
    ax2.axhline(-10, color='green', linestyle='--', alpha=0.5, label='±10px zone')
    ax2.set_title(f"Vertical Error — {label}")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Pixel Error Y")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f"pid_{label.replace('=','').replace(' ','_')}.png", dpi=150)
    plt.close()
    print(f"  Plot saved: pid_{label}.png")



pid_metrics("pid_log/pid_log_20260531_183721_p0,5.csv", "Kp=0.5 (Yaw)")
pid_metrics("pid_log/pid_log_20260531_184007_p1.csv", "Kp=1 (Yaw)")
pid_metrics("pid_log/pid_log_20260531_184545_p1,5.csv", "Kp=1.5 (Yaw)")
pid_metrics("pid_log/pid_log_20260531_184328_p2.csv", "Kp=2 (Yaw)")
pid_metrics("pid_log/pid_log_20260531_191225_p3yaw_BANG.csv", "Kp=3 (Yaw)")

pid_metrics("pid_log/pid_log_20260531_191619_p3pitch_BANG.csv", "Kp=3 (Vertical)")
pid_metrics("pid_log/pid_log_20260531_192031.csv", "Kp=3 (Yaw & Vertical)")
pid_metrics("pid_log/pid_log_20260531_180657_val.csv", "Combined PID (Validation)")
pid_metrics("pid_log/pid_log_20260531_171420_v_init.csv", "Combined PID (Initial)")

pid_metrics("pid_log/pid_log_20260531_174435_val.csv", "Baseline - Yaw 1.5,1.0,2e-08 | Vert 1.5,0.0,5e-08 | Fwd 1.0,0.0,0.0")

