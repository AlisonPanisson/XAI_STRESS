#!/usr/bin/env python3
"""
shap_wesad.py -- SHAP analysis under the corrected protocol (companion of rerun_wesad.py).

Put this file in the same folder as rerun_wesad.py (it imports its loading/splitting code,
so windows and folds are identical to the reported results).

Two explanation settings, both with Random Forest:
  LOSO     : RF trained on 14 subjects, SHAP computed on the held-out subject's windows
             (what a population-level model does on a NEW professional).
  SUBJECT  : RF trained inside blocked-CV folds of one subject, SHAP computed on that fold's
             held-out windows, pooled over folds (what a subject-specific model relies on).

Outputs (in --out):
  shap_importance_per_subject.csv  mean|SHAP| per subject x feature x protocol (stress class + all classes)
  shap_group_importance.csv        same, summed by signal (temp/eda/hr) and by descriptor type
  shap_direction.csv               per subject: Spearman(feature value, SHAP value) for the stress class
  shap_consistency.csv             inter-subject agreement and LOSO-vs-subject agreement
  shap_summary.md                  tables ready to quote
  shap_importance.png              figure (feature-level bars, per-subject signal shares)

Usage
-----
  pip install shap matplotlib                      # shap is required unless --method perm
  python shap_wesad.py --root /path/WESAD --out shap_binary --task binary --extra-feats \
         --results-dir results_binary_extra        # optional: reuse tuned RF hyper-parameters
  python shap_wesad.py --selftest --method perm    # smoke test on synthetic data

--method perm uses permutation importance instead of SHAP (smoke test / sanity check only;
the paper's analysis should use --method shap).
"""
import argparse, json, sys, tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

import rerun_wesad as R

STRESS_CLASS = 1  # encoded label of "stress" in both tasks (binary: stress=1; multiclass: baseline=0, stress=1)


def feature_names(extra):
    names = list(R.STAT_NAMES)
    if extra:
        names += [f"{c}_std" for c in R.CHANNELS] + [f"{c}_slope" for c in R.CHANNELS]
    return names


def signal_of(name):
    return name.split("_")[0]


def descriptor_of(name):
    return name.split("_")[1]


# ---------------------------------------------------------------------------- explanation
def to_class_first(sv, n_features):
    """Normalize SHAP output to (n_classes, n_samples, n_features). Handles the list-of-arrays
    format (older shap) and the (n, f, c) array format (newer shap)."""
    if isinstance(sv, list):
        return np.stack([np.asarray(a) for a in sv], axis=0)
    sv = np.asarray(sv)
    if sv.ndim == 2:                       # single output
        return sv[None]
    if sv.shape[1] == n_features:          # (n, f, c)
        return np.transpose(sv, (2, 0, 1))
    if sv.shape[2] == n_features:          # (c, n, f)
        return sv
    raise ValueError(f"unexpected SHAP output shape {sv.shape}")


def explain(clf, Xtr, ytr, Xte, yte, method, seed):
    """Return per-class attribution array (n_classes, n_test, n_features) for 'shap',
    or a (1, n_test, n_features)-shaped pseudo-attribution for 'perm' (stress-class importances
    broadcast over samples; no per-sample direction available)."""
    nf = Xte.shape[1]
    if method == "shap":
        import shap
        sv = shap.TreeExplainer(clf).shap_values(Xte)
        return to_class_first(sv, nf)
    r = permutation_importance(clf, Xte, yte, scoring="balanced_accuracy", n_repeats=10,
                               random_state=seed)
    imp = np.clip(r.importances_mean, 0, None)
    return np.tile(imp[None, None, :], (1, len(Xte), 1))


def make_rf(seed, params=None):
    kw = dict(n_estimators=200, class_weight="balanced", random_state=seed, n_jobs=1)
    kw.update(params or {})
    return RandomForestClassifier(**kw)


def summarize(att, X, nf):
    """att: (c, n, f). Returns mean|SHAP| for the stress class and over all classes, plus
    Spearman(value, SHAP) for the stress class."""
    c = min(STRESS_CLASS, att.shape[0] - 1)
    stress = att[c]
    imp_stress = np.abs(stress).mean(0)
    imp_all = np.abs(att).mean(axis=(0, 1))
    dirs = np.full(nf, np.nan)
    if att.shape[0] > 1:  # direction needs per-sample SHAP (not available for perm)
        for j in range(nf):
            if X[:, j].std() > 0 and stress[:, j].std() > 0:
                dirs[j] = spearmanr(X[:, j], stress[:, j]).correlation
    return imp_stress, imp_all, dirs


def load_tuned(results_dir):
    """RF hyper-parameters selected in the main experiments (optional)."""
    tuned = {"LOSO": {}, "SUBJECT": {}}
    if not results_dir:
        return tuned
    d = Path(results_dir)
    try:
        l = pd.read_csv(d / "loso_per_subject.csv")
        for _, r in l[l.model == "RF"].iterrows():
            tuned["LOSO"][int(r.subject)] = json.loads(r.params)
        s = pd.read_csv(d / "subject_blocked_per_subject.csv")
        for _, r in s[s.model == "RF"].iterrows():
            tuned["SUBJECT"][int(r.subject)] = json.loads(r.params)
    except Exception as e:
        print(f"[warn] could not load tuned params from {d}: {e}", file=sys.stderr)
    return tuned


def loso_subject(sid, D, cfg, tuned, nf):
    te = D["subj"] == sid
    tr = ~te
    clf = make_rf(cfg.seed, tuned["LOSO"].get(sid)).fit(D["Xs"][tr], D["y"][tr])
    att = explain(clf, D["Xs"][tr], D["y"][tr], D["Xs"][te], D["y"][te], cfg.method, cfg.seed)
    return sid, summarize(att, D["Xs"][te], nf)


def subject_subject(sid, D, cfg, tuned, nf):
    m = D["subj"] == sid
    X, y, seg, pos = D["Xs"][m], D["y"][m], D["seg"][m], D["pos"][m]
    folds = R.blocked_splits(seg, pos, cfg.folds, cfg.gap)
    plist = tuned["SUBJECT"].get(sid)
    atts, Xte_all = [], []
    for k, (tr, te) in enumerate(folds):
        p = plist[k] if isinstance(plist, list) and len(plist) == len(folds) else None
        clf = make_rf(cfg.seed, p).fit(X[tr], y[tr])
        a = explain(clf, X[tr], y[tr], X[te], y[te], cfg.method, cfg.seed)
        # classes may be missing in a fold; align to the full class set
        atts.append(a); Xte_all.append(X[te])
    ncls = max(a.shape[0] for a in atts)
    atts = [np.concatenate([a, np.zeros((ncls - a.shape[0],) + a.shape[1:])], 0) if a.shape[0] < ncls else a
            for a in atts]
    att = np.concatenate(atts, axis=1)
    return sid, summarize(att, np.vstack(Xte_all), nf)


# ---------------------------------------------------------------------------- reporting
def norm_rows(M):
    return M / np.clip(M.sum(1, keepdims=True), 1e-12, None)


def spearman_safe(a, b):
    if np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(spearmanr(a, b).correlation)


def mean_pairwise_spearman(M):
    vals = [spearman_safe(M[i], M[j]) for i in range(len(M)) for j in range(i + 1, len(M))]
    return float(np.nanmean(vals)), float(np.nanstd(vals))


def to_md(df):
    return R.to_md(df)


def main(a):
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    root = Path(a.root)
    D, summ = R.build_dataset(root, a.subjects or R.SUBJECTS, a.win, a.step, a.hr_source)
    D = R.encode_task(D, a.task)
    if a.extra_feats:
        Xt = D["Xt"].astype(float)
        tt = (np.arange(Xt.shape[2]) - (Xt.shape[2] - 1) / 2.0) / R.FS
        D["Xs"] = np.hstack([D["Xs"], Xt.std(axis=2), (Xt * tt).sum(axis=2) / (tt ** 2).sum()])
    names = feature_names(a.extra_feats)
    assert D["Xs"].shape[1] == len(names), "feature count mismatch (use --extra-feats consistently)"
    nf = len(names)
    cfg = argparse.Namespace(**vars(a)); cfg.gap = int(np.ceil(a.win / a.step))
    tuned = load_tuned(a.results_dir)
    ids = sorted(np.unique(D["subj"]).tolist())
    print(f"[info] {len(ids)} subjects, {nf} features, method={a.method}")

    J = dict(n_jobs=a.n_jobs)
    res = {"LOSO": dict(Parallel(**J)(delayed(loso_subject)(s, D, cfg, tuned, nf) for s in ids)),
           "SUBJECT": dict(Parallel(**J)(delayed(subject_subject)(s, D, cfg, tuned, nf) for s in ids))}

    rows, dir_rows = [], []
    mats = {}
    for proto in ("LOSO", "SUBJECT"):
        M = np.array([res[proto][s][0] for s in ids])
        mats[proto] = M
        for i, s in enumerate(ids):
            imp_s, imp_a, dirs = res[proto][s]
            for j, f in enumerate(names):
                rows.append(dict(protocol=proto, subject=s, feature=f, signal=signal_of(f),
                                 descriptor=descriptor_of(f), mean_abs_shap_stress=imp_s[j],
                                 mean_abs_shap_all=imp_a[j], share_stress=imp_s[j] / max(imp_s.sum(), 1e-12)))
                dir_rows.append(dict(protocol=proto, subject=s, feature=f, spearman_value_vs_shap=dirs[j]))
    imp = pd.DataFrame(rows); imp.to_csv(out / "shap_importance_per_subject.csv", index=False)
    pd.DataFrame(dir_rows).to_csv(out / "shap_direction.csv", index=False)

    grp = []
    for key in ("signal", "descriptor"):
        g = imp.groupby(["protocol", "subject", key]).share_stress.sum().reset_index()
        g.columns = ["protocol", "subject", "group", "share"]; g["by"] = key
        grp.append(g)
    grp = pd.concat(grp); grp.to_csv(out / "shap_group_importance.csv", index=False)

    # ---- consistency statistics
    cons = []
    for proto in ("LOSO", "SUBJECT"):
        m, sd = mean_pairwise_spearman(mats[proto])
        mean_vec = norm_rows(mats[proto]).mean(0)
        to_mean = [spearman_safe(mats[proto][i], mean_vec) for i in range(len(ids))]
        top1 = pd.Series([names[int(np.argmax(r))] for r in mats[proto]]).value_counts()
        cons.append(dict(metric=f"{proto}: mean pairwise Spearman between subjects", value=m, sd=sd))
        cons.append(dict(metric=f"{proto}: mean Spearman of subject vs group-mean importance",
                         value=float(np.nanmean(to_mean)), sd=float(np.nanstd(to_mean))))
        cons.append(dict(metric=f"{proto}: most frequent top-1 feature", value=top1.index[0],
                         sd=f"{top1.iloc[0]}/{len(ids)} subjects"))
    cross = [spearman_safe(mats["LOSO"][i], mats["SUBJECT"][i]) for i in range(len(ids))]
    top3 = [len(set(np.argsort(-mats["LOSO"][i])[:3]) & set(np.argsort(-mats["SUBJECT"][i])[:3]))
            for i in range(len(ids))]
    cons.append(dict(metric="same subject: Spearman LOSO vs subject-specific importance",
                     value=float(np.nanmean(cross)), sd=float(np.nanstd(cross))))
    cons.append(dict(metric="same subject: overlap of top-3 features (of 3)",
                     value=float(np.mean(top3)), sd=float(np.std(top3))))
    cons = pd.DataFrame(cons); cons.to_csv(out / "shap_consistency.csv", index=False)

    # ---- summary tables
    feat = imp.groupby(["protocol", "feature"]).share_stress.agg(["mean", "std"]).reset_index()
    sig = grp[grp.by == "signal"].groupby(["protocol", "group"]).share.agg(["mean", "std"]).reset_index()
    dr = pd.DataFrame(dir_rows).groupby(["protocol", "feature"]).spearman_value_vs_shap.agg(
        pos_share=lambda x: float((x.dropna() > 0).mean()) if x.notna().any() else np.nan,
        mean_rho="mean").reset_index()
    fmt = lambda d: d.assign(**{c: d[c].round(3) for c in d.columns if d[c].dtype.kind == "f"})
    top = []
    for proto in ("LOSO", "SUBJECT"):
        t = feat[feat.protocol == proto].sort_values("mean", ascending=False).head(8)
        top.append(fmt(t))
    md = [f"# SHAP summary ({a.method}; task={a.task}; features={nf})", "",
          "Importance = share of mean|SHAP| for the stress class (row-normalized per subject), mean ± SD over subjects.", "",
          "## Signal-level share", to_md(fmt(sig)), "",
          "## Top features (LOSO, then subject-specific)", to_md(top[0]), "", to_md(top[1]), "",
          "## Direction consistency (share of subjects where higher feature value -> higher stress SHAP)",
          to_md(fmt(dr[dr.protocol == "LOSO"])), "", to_md(fmt(dr[dr.protocol == "SUBJECT"])), "",
          "## Consistency statistics", to_md(cons.assign(value=cons.value.map(
              lambda v: round(v, 3) if isinstance(v, float) else v))), ""]
    if a.method != "shap":
        md.insert(2, "**WARNING: permutation importance was used (no direction information). Use --method shap for the paper.**\n")
    (out / "shap_summary.md").write_text("\n".join(md))

    # ---- figure
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(16, 4.8), gridspec_kw=dict(width_ratios=[1.5, 1, 1]))
        x = np.arange(nf); w = 0.4
        for k, (proto, lab) in enumerate((("LOSO", "Population-level (LOSO)"), ("SUBJECT", "Subject-specific"))):
            f = feat[feat.protocol == proto].set_index("feature").loc[names]
            ax[0].bar(x + (k - 0.5) * w, f["mean"], w, yerr=f["std"], capsize=2, label=lab)
        ax[0].set_xticks(x); ax[0].set_xticklabels(names, rotation=70, ha="right")
        ax[0].set_ylabel("share of mean |SHAP| (stress)"); ax[0].legend(); ax[0].set_title("(a) Feature importance")
        for axi, proto, t in ((ax[1], "LOSO", "(b) LOSO: signal share per subject"),
                              (ax[2], "SUBJECT", "(c) Subject-specific: signal share per subject")):
            g = grp[(grp.by == "signal") & (grp.protocol == proto)].pivot(index="subject", columns="group", values="share")
            g = g[[c for c in R.CHANNELS if c in g.columns]]
            bottom = np.zeros(len(g))
            for c in g.columns:
                axi.bar(g.index.astype(str), g[c], bottom=bottom, label=c); bottom += g[c].values
            axi.set_title(t); axi.set_xlabel("subject"); axi.set_ylim(0, 1)
            if proto == "LOSO": axi.legend(ncol=3, fontsize=8)
        plt.tight_layout(); plt.savefig(out / "shap_importance.png", dpi=200); plt.close()
    except Exception as e:
        print(f"[warn] figure skipped: {e}", file=sys.stderr)
    print(f"[done] outputs in {out}/ (read shap_summary.md first)")


def parse():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root"); p.add_argument("--out", default="shap_results")
    p.add_argument("--win", type=float, default=60.0); p.add_argument("--step", type=float, default=30.0)
    p.add_argument("--task", choices=["multiclass", "binary"], default="binary")
    p.add_argument("--folds", type=int, default=5)
    p.add_argument("--extra-feats", action="store_true", help="15 features (min/mean/max/std/slope), as in the control run")
    p.add_argument("--results-dir", help="folder with loso_per_subject.csv / subject_blocked_per_subject.csv for tuned RF params")
    p.add_argument("--hr-source", choices=["bvp", "csv"], default="bvp")
    p.add_argument("--method", choices=["shap", "perm"], default="shap")
    p.add_argument("--subjects", type=int, nargs="*"); p.add_argument("--seed", type=int, default=42)
    p.add_argument("--n-jobs", type=int, default=-1)
    p.add_argument("--selftest", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    a = parse()
    if a.method == "shap":
        try:
            import shap  # noqa: F401
        except ImportError:
            sys.exit("shap is not installed: pip install shap  (or use --method perm for a smoke test)")
    if a.selftest:
        tmp = Path(tempfile.mkdtemp()); ids = R.make_synthetic(tmp / "WESAD")
        a.root, a.subjects, a.win, a.step = str(tmp / "WESAD"), ids, 20.0, 10.0
        a.out = a.out if a.out != "shap_results" else "shap_selftest"
    if not a.root:
        sys.exit("--root is required (or use --selftest)")
    main(a)
