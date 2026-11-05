#!/usr/bin/env python3
"""check_hr.py -- is the HR channel aligned with the labels?

Compares, per subject, heart rate from HR.csv (legacy) with heart rate derived from the .pkl BVP:
  * correlation at the assumed alignment and the best lag within +/-300 s;
  * mean HR in stress minus mean HR in the other conditions, for both sources.
Run next to rerun_wesad.py:   python check_hr.py /path/to/WESAD
Writes hr_check.csv.
"""
import sys, pathlib
sys.path.insert(0, ".")
import numpy as np, pandas as pd
import rerun_wesad as R

root = pathlib.Path(sys.argv[1])
MAXLAG = 300


def to1hz(x):
    m = (len(x) // R.FS) * R.FS
    return x[:m].reshape(-1, R.FS).mean(1)


def lag_corr(a, b, max_lag):
    """corr(a[t], b[t+k]); k>0 means a is time-stamped k seconds EARLIER than b."""
    c0, best = None, (-2.0, 0)
    for k in range(-max_lag, max_lag + 1):
        x, y = (a[:len(a) - k], b[k:]) if k >= 0 else (a[-k:], b[:len(b) + k])
        if len(x) < 100:
            continue
        c = np.corrcoef(x, y)[0, 1]
        if k == 0:
            c0 = c
        if c > best[0]:
            best = (c, k)
    return c0, best[1], best[0]


def stress_minus_others(sd, col=7):  # col 7 = hr_mean of the 9-feature window vector
    Xs, _, y, *_ = R.build_windows(sd, 60, 30)
    st = Xs[y == 2, col].mean()
    ot = np.mean([Xs[y == k, col].mean() for k in (1, 3, 4) if (y == k).any()])
    return st - ot


rows = []
for sid in R.SUBJECTS:
    try:
        sb = R.load_subject(root, sid, "bvp")
        sc = R.load_subject(root, sid, "csv")
    except Exception as e:
        print("skip", sid, e); continue
    a, b = to1hz(sc["sig"][2])[15:-15], to1hz(sb["sig"][2])[15:-15]
    n = min(len(a), len(b)); a, b = a[:n], b[:n]
    a, b = (a - a.mean()) / (a.std() + 1e-9), (b - b.mean()) / (b.std() + 1e-9)
    c0, k, cb = lag_corr(a, b, MAXLAG)
    rows.append(dict(subject=sid, corr_at_assumed=round(c0, 3), best_lag_s=k, corr_at_best=round(cb, 3),
                     hr_stress_minus_others_csv=round(stress_minus_others(sc), 2),
                     hr_stress_minus_others_bvp=round(stress_minus_others(sb), 2)))
df = pd.DataFrame(rows)
print(df.to_string(index=False))
df.to_csv("hr_check.csv", index=False)
print("\nSubjects with stress HR > other conditions:  csv %d/%d   bvp %d/%d" % (
    (df.hr_stress_minus_others_csv > 0).sum(), len(df), (df.hr_stress_minus_others_bvp > 0).sum(), len(df)))
print("Mean difference (bpm):  csv %.2f   bvp %.2f" % (df.hr_stress_minus_others_csv.mean(),
                                                       df.hr_stress_minus_others_bvp.mean()))
print("Best-lag summary (s): median %.0f, min %d, max %d; corr at assumed alignment median %.2f"
      % (df.best_lag_s.median(), df.best_lag_s.min(), df.best_lag_s.max(), df.corr_at_assumed.median()))
