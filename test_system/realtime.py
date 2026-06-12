import pandas as pd

df = pd.read_csv("detection_log.csv")

idle     = df[df['frame_id'] == 0]
tracking = df[df['frame_id'] > 0]

RT_THRESHOLD = 25  # FPS
RT_MS_THRESHOLD = 1000 / RT_THRESHOLD  # ms per frame

for label, subset in [("Idle", idle), ("Tracking", tracking)]:
    mean_fps = subset['fps'].mean()
    mean_ms  = subset['loop_ms'].mean()
    percentage_rt   = (subset['fps'] >= RT_THRESHOLD).mean() * 100
    percentage_ms_rt = (subset['loop_ms'] <= RT_MS_THRESHOLD).mean() * 100

    print(f"--- {label} ({len(subset)} frames) ---")
    print(f"  Mean FPS:        {mean_fps:.1f}")
    print(f"  Mean latency:    {mean_ms:.1f} ms")
    print(f"  Frames ≥ 25fps:  {percentage_rt:.1f}%")
    print(f"  Frames ≤ 40ms:   {percentage_ms_rt:.1f}%")
    verdict = "✅ Real-time" if mean_fps >= RT_THRESHOLD else "❌ Not real-time"
    print(f"  Verdict:         {verdict}\n")