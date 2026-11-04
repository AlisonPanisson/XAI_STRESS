#!/usr/bin/env python3
"""
rerun_wesad.py  --  corrected evaluation protocol for the WESAD experiments.

Addresses IEEE Access Reviewer 2, comments 2, 3 and 5:
  * physiological windows (default 60 s, 30 s step) built INSIDE contiguous label segments
    (no window crosses a label change);
  * pooled -> individual evaluation by leave-one-subject-out (LOSO);
  * subject-specific evaluation by BLOCKED cross-validation inside each label segment,
    with a purge gap so overlapping windows never fall on both sides of a split;
  * scaler (and optional SMOTE) fitted on TRAINING data only, inside every fold;
  * hyper-parameter search with inner subject-grouped (LOSO) or inner blocked CV;
  * identical windows/folds for static classifiers and time-series classifiers
    (matched comparison), per-subject metrics, mean +/- SD, paired Wilcoxon + Holm;
  * diagnostic "leaky" reference (random window splits) to quantify the inflation;
  * data-size learning/calibration curve (cold-start question);
  * VAR as a separate forecasting analysis against a persistence baseline.

Dependencies: numpy, pandas, scipy, scikit-learn, joblib.
If WESAD is missing, the script downloads it anonymously from Kaggle when possible;
the Kaggle CLI and configured credentials are an optional fallback.
Optional: aeon or sktime (library ROCKET). Without them a compact in-script ROCKET is used.

Usage
-----
  python rerun_wesad.py --root /path/to/WESAD --out results
  python rerun_wesad.py --selftest            # smoke test on synthetic data

WESAD layout expected:  <root>/S2/S2.pkl, <root>/S2/S2_E4_Data(.zip) with HR.csv, EDA.csv ...
Subjects S1 and S12 are excluded (as in the original study) -> 15 subjects.

NOTE: the original notebooks could not be read when this script was written, so the
preprocessing follows the README/dissertation description (EDA, TEMP, HR; min/mean/max),
not the notebook code line by line.
"""
import argparse, json, math, os, shutil, subprocess, sys, tempfile, time, warnings, zipfile
os.environ.setdefault("PYTHONWARNINGS", "ignore")  # inherited by joblib workers
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import wilcoxon
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifierCV
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import GroupKFold, ParameterGrid, train_test_split
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

SUBJECTS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]
KAGGLE_DATASET = "orvile/wesad-wearable-stress-affect-detection-dataset"
FS = 4  # common grid (Hz): EDA and TEMP native rate of the Empatica E4
CHANNELS = ["temp", "eda", "hr"]
STAT_NAMES = [f"{c}_{s}" for c in CHANNELS for s in ("min", "mean", "max")]
LABEL_NAMES = {1: "baseline", 2: "stress", 3: "amusement", 4: "meditation"}
STATIC = ["kNN", "LR", "RF", "SVM", "NN"]
TS = ["TSF", "ROCKET"]


# ----------------------------------------------------------------------------- loading
def _subject_data_exists(root: Path, sid: int):
    sdir = root / f"S{sid}"
    return ((sdir / f"S{sid}.pkl").is_file()
            and ((sdir / f"S{sid}_E4_Data" / "HR.csv").is_file()
                 or (sdir / f"S{sid}_E4_Data.zip").is_file()))


def _download_kaggle_archive(download_dir: Path):
    kaggle = shutil.which("kaggle")
    if kaggle is not None:
        try:
            subprocess.run(
                [kaggle, "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(download_dir)],
                check=True,
            )
            archives = list(download_dir.glob("*.zip"))
            if len(archives) == 1:
                return archives[0]
            raise RuntimeError(
                f"Expected one Kaggle dataset archive in {download_dir}, found {len(archives)}."
            )
        except subprocess.CalledProcessError as exc:
            print(
                f"[warn] Kaggle CLI download failed (exit {exc.returncode}); "
                "trying the public download endpoint.",
                file=sys.stderr,
            )

    archive_path = download_dir / "wesad-dataset.zip"
    request = Request(
        f"https://www.kaggle.com/api/v1/datasets/download/{KAGGLE_DATASET}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        with urlopen(request, timeout=60) as response, archive_path.open("wb") as archive:
            shutil.copyfileobj(response, archive)
    except (OSError, URLError) as exc:
        raise RuntimeError(
            "Could not download the WESAD dataset from Kaggle. Check network access; "
            "if anonymous download is unavailable, install the Kaggle CLI and configure "
            "Kaggle credentials."
        ) from exc
    return archive_path


def ensure_wesad_dataset(root: Path, subjects):
    """Download WESAD from Kaggle if fewer than three usable subjects are present."""
    root = root.expanduser().resolve()
    if sum(_subject_data_exists(root, sid) for sid in subjects) >= 3:
        return

    root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wesad-kaggle-", dir=root.parent) as tmp:
        tmp_path = Path(tmp)
        download_dir = tmp_path / "download"
        download_dir.mkdir()
        archive_path = _download_kaggle_archive(download_dir)

        extracted = tmp_path / "extracted"
        extracted.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            extraction_root = extracted.resolve()
            for member in archive.infolist():
                destination = (extracted / member.filename).resolve()
                if os.path.commonpath((str(extraction_root), str(destination))) != str(extraction_root):
                    raise RuntimeError(f"Unsafe path in Kaggle archive: {member.filename}")
                archive.extract(member, extracted)

        candidates = {
            path.parent.parent
            for sid in subjects
            for path in extracted.rglob(f"S{sid}.pkl")
            if path.parent.name == f"S{sid}"
        }
        source = max(
            candidates,
            key=lambda candidate: sum(_subject_data_exists(candidate, sid) for sid in subjects),
            default=None,
        )
        available = (
            sum(_subject_data_exists(source, sid) for sid in subjects)
            if source is not None else 0
        )
        if source is None or available < 3:
            raise RuntimeError(
                f"The Kaggle archive did not contain at least three usable WESAD subjects "
                f"for the expected layout (found {available})."
            )

        existing = [root / item.name for item in source.iterdir() if (root / item.name).exists()]
        if existing:
            raise FileExistsError(
                f"Cannot install downloaded WESAD data because these paths already exist: "
                f"{', '.join(map(str, existing))}"
            )
        root.mkdir(parents=True, exist_ok=True)
        for item in source.iterdir():
            shutil.move(str(item), str(root / item.name))

    print(f"[info] downloaded WESAD from Kaggle to {root}")


def _read_e4_csv(sdir: Path, sid: int, name: str):
    """Return (start_unix, fs, data) for a single-column Empatica E4 csv, or None."""
    folder = sdir / f"S{sid}_E4_Data"
    zpath = sdir / f"S{sid}_E4_Data.zip"
    txt = None
    if (folder / name).exists():
        txt = (folder / name).read_text()
    elif zpath.exists():
        with zipfile.ZipFile(zpath) as zf:
            hit = [n for n in zf.namelist() if n.endswith(name)]
            if hit:
                txt = zf.read(hit[0]).decode()
    if txt is None:
        return None
    vals = [float(r.split(",")[0]) for r in txt.strip().splitlines() if r.strip()]
    return vals[0], vals[1], np.asarray(vals[2:], dtype=float)


def load_subject(root: Path, sid: int):
    import pickle
    sdir = root / f"S{sid}"
    with open(sdir / f"S{sid}.pkl", "rb") as f:
        d = pickle.load(f, encoding="latin1")
    wrist = d["signal"]["wrist"]
    eda = np.asarray(wrist["EDA"]).ravel().astype(float)
    temp = np.asarray(wrist["TEMP"]).ravel().astype(float)
    n = min(len(eda), len(temp))
    eda, temp = eda[:n], temp[:n]
    lab = np.asarray(d["label"]).ravel().astype(int)

    hr_csv = _read_e4_csv(sdir, sid, "HR.csv")
    if hr_csv is None:
        raise FileNotFoundError(f"HR.csv not found for S{sid}")
    hr_start, hr_fs, hr = hr_csv
    eda_csv = _read_e4_csv(sdir, sid, "EDA.csv")
    if eda_csv is not None:
        offset = hr_start - eda_csv[0]
    else:
        offset = 10.0  # E4 heart rate starts ~10 s after the other channels
        print(f"[warn] S{sid}: EDA.csv missing, assuming HR offset of 10 s", file=sys.stderr)

    t = np.arange(n) / FS
    hr_t = offset + np.arange(len(hr)) / hr_fs
    hr_i = np.interp(t, hr_t, hr)
    first_valid = int(np.ceil(max(offset, 0.0) * FS))
    last_valid = int(np.floor(min(hr_t[-1], t[-1]) * FS))
    # labels are stored at the RespiBAN rate (700 Hz); align proportionally in time
    li = np.minimum((np.arange(n) * (len(lab) / n)).astype(int), len(lab) - 1)
    return dict(sig=np.vstack([temp, eda, hr_i]), label=lab[li],
                first_valid=first_valid, last_valid=last_valid)


def build_windows(sd, win_s, step_s):
    """Windows are generated inside contiguous runs of a valid label (1-4)."""
    w, s = int(win_s * FS), int(step_s * FS)
    sig, lab = sd["sig"], sd["label"]
    n = lab.shape[0]
    change = np.flatnonzero(np.diff(lab) != 0) + 1
    starts, ends = np.r_[0, change], np.r_[change, n]
    Xs, Xt, y, seg, pos, seg_minutes = [], [], [], [], [], 0.0
    seg_id = 0
    for a, b in zip(starts, ends):
        L = lab[a]
        if L not in LABEL_NAMES:
            continue
        a2, b2 = max(a, sd["first_valid"]), min(b, sd["last_valid"] + 1)
        if b2 - a2 < w:
            continue
        k = 0
        for st in range(a2, b2 - w + 1, s):
            ch = sig[:, st:st + w]
            Xs.append(np.concatenate([[c.min(), c.mean(), c.max()] for c in ch]))
            Xt.append(ch.astype(np.float32))
            y.append(L); seg.append(seg_id); pos.append(k)
            k += 1
        seg_minutes += (b2 - a2) / FS / 60.0
        seg_id += 1
    return (np.asarray(Xs), np.asarray(Xt), np.asarray(y), np.asarray(seg),
            np.asarray(pos), seg_minutes)


def build_dataset(root, subjects, win_s, step_s):
    parts, summ = [], []
    for sid in subjects:
        try:
            sd = load_subject(root, sid)
        except Exception as e:  # missing subject -> skip
            print(f"[warn] skipping S{sid}: {e}", file=sys.stderr)
            continue
        Xs, Xt, y, seg, pos, mins = build_windows(sd, win_s, step_s)
        parts.append((sid, Xs, Xt, y, seg, pos))
        row = dict(subject=sid, n_windows=len(y), labeled_minutes=round(mins, 2))
        row.update({f"n_{LABEL_NAMES[k]}": int((y == k).sum()) for k in LABEL_NAMES})
        summ.append(row)
    if len(parts) < 3:
        raise RuntimeError("fewer than 3 subjects could be loaded")
    D = dict(
        Xs=np.vstack([p[1] for p in parts]),
        Xt=np.concatenate([p[2] for p in parts]),
        y_raw=np.concatenate([p[3] for p in parts]),
        subj=np.concatenate([np.full(len(p[3]), p[0]) for p in parts]),
        seg=np.concatenate([p[4] for p in parts]),
        pos=np.concatenate([p[5] for p in parts]),
    )
    return D, pd.DataFrame(summ)


def encode_task(D, task):
    if task == "binary":
        D["y"] = (D["y_raw"] == 2).astype(int)           # stress vs non-stress
    else:
        D["y"] = D["y_raw"] - 1                           # baseline/stress/amusement/meditation
    return D


# ----------------------------------------------------------------------------- splitting
def blocked_splits(seg, pos, K, gap):
    """Blocked CV inside every label segment with a purge gap (in windows).

    Each segment is cut into K contiguous blocks; fold k tests on block k of every segment.
    Training windows within `gap` positions of any test window of the same segment are removed,
    so overlapping (and immediately adjacent) windows never straddle the split.
    Works on subsets: blocks use the rank of `pos`, the purge uses `pos` itself.
    """
    n = len(seg)
    block = np.zeros(n, dtype=int)
    for s in np.unique(seg):
        m = np.flatnonzero(seg == s)
        order = m[np.argsort(pos[m])]
        block[order] = np.floor(np.arange(len(order)) * K / len(order)).astype(int)
    splits = []
    for k in range(K):
        te = np.flatnonzero(block == k)
        if len(te) == 0:
            continue
        excl = np.zeros(n, dtype=bool)
        for s in np.unique(seg[te]):
            tp = pos[te][seg[te] == s]
            m = np.flatnonzero(seg == s)
            dist = np.abs(pos[m][:, None] - tp[None, :]).min(axis=1)
            excl[m[dist <= gap]] = True
        tr = np.flatnonzero(~excl)
        for s_ in np.unique(seg[te]):  # sanity check: no train window within `gap` of a test window
            a_, b_ = pos[tr][seg[tr] == s_], pos[te][seg[te] == s_]
            assert len(a_) == 0 or np.abs(a_[:, None] - b_[None, :]).min() > gap, "leakage in split"
        if len(tr):
            splits.append((tr, te))
    return splits


# ----------------------------------------------------------------------------- SMOTE (in-fold only)
def smote(X, y, rng, k=5):
    classes, counts = np.unique(y, return_counts=True)
    nmax = counts.max()
    Xs, ys = [X], [y]
    for c, n in zip(classes, counts):
        if n == nmax or n < 2:
            continue
        Xc = X[y == c]
        kk = min(k, n - 1)
        idx = NearestNeighbors(n_neighbors=kk + 1).fit(Xc).kneighbors(Xc)[1]
        m = nmax - n
        base = rng.integers(0, n, m)
        nb = idx[base, rng.integers(1, kk + 1, m)]
        lam = rng.random((m, 1))
        Xs.append(Xc[base] + lam * (Xc[nb] - Xc[base]))
        ys.append(np.full(m, c))
    return np.vstack(Xs), np.concatenate(ys)


# ----------------------------------------------------------------------------- static models
def model_zoo(seed, smote_on):
    cw = None if smote_on else "balanced"
    return {
        "kNN": (lambda: KNeighborsClassifier(), {"n_neighbors": [3, 5, 11]}),
        "LR": (lambda: LogisticRegression(max_iter=2000, class_weight=cw), {"C": [0.1, 1, 10]}),
        "RF": (lambda: RandomForestClassifier(n_estimators=200, class_weight=cw,
                                              random_state=seed, n_jobs=1),
               {"max_depth": [None, 8], "min_samples_leaf": [1, 3]}),
        "SVM": (lambda: SVC(class_weight=cw), {"C": [1, 10], "gamma": ["scale", 0.1]}),
        "NN": (lambda: MLPClassifier(max_iter=500, random_state=seed),
               {"hidden_layer_sizes": [(32,), (64, 32)], "alpha": [1e-4, 1e-2]}),
    }


def fit_predict_static(name, params, Xtr, ytr, Xte, cfg, seed=0, return_model=False):
    sc = MinMaxScaler().fit(Xtr)                      # fitted on training data only
    A, B = sc.transform(Xtr), sc.transform(Xte)
    if cfg.smote:
        A, ytr = smote(A, ytr, np.random.default_rng(seed))
    clf = cfg.zoo[name][0]().set_params(**params).fit(A, ytr)
    return clf.predict(B)


def default_params(name, cfg):
    return {k: v[0] for k, v in cfg.zoo[name][1].items()}


def tune(name, Xtr, ytr, inner, cfg):
    if cfg.no_tune:
        return default_params(name, cfg)
    best = (-1.0, default_params(name, cfg))
    for params in ParameterGrid(cfg.zoo[name][1]):
        sc = []
        for a, b in inner:
            if len(np.unique(ytr[a])) < 2:
                continue
            p = fit_predict_static(name, params, Xtr[a], ytr[a], Xtr[b], cfg)
            sc.append(f1_score(ytr[b], p, average="macro", zero_division=0))
        if sc and np.mean(sc) > best[0]:
            best = (float(np.mean(sc)), params)
    return best[1]


# ----------------------------------------------------------------------------- time-series models
class TSF:
    """Time Series Forest (Deng et al., 2013): trees on mean/std/slope of random intervals.
    Multivariate: each interval is drawn on a random channel."""

    def __init__(self, n_estimators=200, seed=0):
        self.n_estimators, self.seed = n_estimators, seed

    def _feat(self, X, ints):
        out = []
        for c, a, b in ints:
            seg = X[:, c, a:b]
            t = np.arange(b - a) - (b - a - 1) / 2.0
            out += [seg.mean(1), seg.std(1), (seg * t).sum(1) / (t ** 2).sum()]
        return np.column_stack(out)

    def fit(self, X, y):
        rng = np.random.default_rng(self.seed)
        n, C, m = X.shape
        r = max(1, int(np.sqrt(m)))
        self.classes_ = np.unique(y)
        self.trees = []
        for i in range(self.n_estimators):
            ints = []
            for _ in range(r):
                a = int(rng.integers(0, m - 3))
                b = int(rng.integers(a + 3, m + 1))
                ints.append((int(rng.integers(0, C)), a, b))
            tree = DecisionTreeClassifier(random_state=int(rng.integers(1 << 30)))
            tree.fit(self._feat(X, ints), y)
            self.trees.append((ints, tree))
        return self

    def predict(self, X):
        P = np.zeros((len(X), len(self.classes_)))
        for ints, tree in self.trees:
            P[:, np.searchsorted(self.classes_, tree.classes_)] += tree.predict_proba(self._feat(X, ints))
        return self.classes_[P.argmax(1)]


class MiniRocket_:
    """Compact ROCKET (Dempster et al., 2020): random convolutional kernels, PPV + max features,
    ridge classifier. Used only if aeon/sktime are not installed."""

    def __init__(self, n_kernels=1000, seed=0):
        self.n_kernels, self.seed = n_kernels, seed

    def _init(self, C, m):
        rng = np.random.default_rng(self.seed)
        self.kernels = []
        for _ in range(self.n_kernels):
            L = int(rng.choice([7, 9, 11]))
            W = rng.normal(size=(C, L)); W -= W.mean()
            dmax = max(np.log2((m - 1) / (L - 1)), 0.0)
            d = int(2 ** rng.uniform(0, dmax))
            pad = ((L - 1) * d) // 2 if rng.random() < 0.5 else 0
            self.kernels.append((W, rng.uniform(-1, 1), d, pad, L))

    def _transform(self, X):
        F = np.empty((len(X), 2 * len(self.kernels)))
        for i, (W, b, d, pad, L) in enumerate(self.kernels):
            Xp = np.pad(X, ((0, 0), (0, 0), (pad, pad))) if pad else X
            Lout = Xp.shape[2] - (L - 1) * d
            out = b + sum(np.einsum("ncl,c->nl", Xp[:, :, j * d:j * d + Lout], W[:, j]) for j in range(L))
            F[:, 2 * i] = (out > 0).mean(1)
            F[:, 2 * i + 1] = out.max(1)
        return F

    def fit(self, X, y):
        self._init(X.shape[1], X.shape[2])
        F = self._transform(X)
        self.sc = StandardScaler().fit(F)
        self.clf = RidgeClassifierCV(alphas=np.logspace(-3, 3, 10)).fit(self.sc.transform(F), y)
        return self

    def predict(self, X):
        return self.clf.predict(self.sc.transform(self._transform(X)))


def make_rocket(seed, cfg):
    if not cfg.own_rocket:
        try:
            from aeon.classification.convolution_based import RocketClassifier
            return RocketClassifier(n_kernels=2000, random_state=seed)
        except Exception:
            pass
        try:
            from sktime.classification.kernel_based import RocketClassifier
            return RocketClassifier(num_kernels=2000, random_state=seed)
        except Exception:
            pass
    return MiniRocket_(n_kernels=cfg.rocket_kernels, seed=seed)


def fit_predict_ts(name, Xtr, ytr, Xte, cfg, seed=0):
    mu = Xtr.mean(axis=(0, 2), keepdims=True)         # per-channel z-score, training data only
    sd = Xtr.std(axis=(0, 2), keepdims=True) + 1e-8
    A, B = (Xtr - mu) / sd, (Xte - mu) / sd
    if cfg.smote:
        n, C, m = A.shape
        F, ytr = smote(A.reshape(n, -1), ytr, np.random.default_rng(seed))
        A = F.reshape(-1, C, m)
    clf = TSF(cfg.tsf_trees, seed) if name == "TSF" else make_rocket(seed, cfg)
    return np.asarray(clf.fit(A, ytr).predict(B))


# ----------------------------------------------------------------------------- metrics
def metrics(y, p):
    return dict(acc=accuracy_score(y, p), bal_acc=balanced_accuracy_score(y, p),
                macro_f1=f1_score(y, p, average="macro", zero_division=0))


# ----------------------------------------------------------------------------- experiments
def loso_one(sid, D, cfg):
    te = D["subj"] == sid
    tr = ~te
    ytr, yte = D["y"][tr], D["y"][te]
    groups = D["subj"][tr]
    inner = list(GroupKFold(n_splits=min(cfg.inner_loso, len(np.unique(groups))))
                 .split(np.zeros(len(groups)), ytr, groups))
    rows = []
    for name in cfg.models:
        params = tune(name, D["Xs"][tr], ytr, inner, cfg)
        p = fit_predict_static(name, params, D["Xs"][tr], ytr, D["Xs"][te], cfg, cfg.seed)
        rows.append(dict(protocol="LOSO", subject=sid, model=name, params=json.dumps(params),
                         n_train=int(tr.sum()), n_test=int(te.sum()), **metrics(yte, p)))
    if cfg.ts:
        for name in TS:
            p = fit_predict_ts(name, D["Xt"][tr], ytr, D["Xt"][te], cfg, cfg.seed)
            rows.append(dict(protocol="LOSO", subject=sid, model=name, params="{}",
                             n_train=int(tr.sum()), n_test=int(te.sum()), **metrics(yte, p)))
    return rows


def subject_one(sid, D, cfg):
    m = D["subj"] == sid
    Xs, Xt, y, seg, pos = D["Xs"][m], D["Xt"][m], D["y"][m], D["seg"][m], D["pos"][m]
    outer = blocked_splits(seg, pos, cfg.folds, cfg.gap)
    names = cfg.models + (TS if cfg.ts else [])
    pred = {k: np.full(len(y), -1) for k in names}
    used = {k: [] for k in cfg.models}
    tested = np.zeros(len(y), bool)
    for tr, te in outer:
        inner = blocked_splits(seg[tr], pos[tr], cfg.inner_folds, cfg.gap)
        for name in cfg.models:
            params = tune(name, Xs[tr], y[tr], inner, cfg)
            used[name].append(params)
            pred[name][te] = fit_predict_static(name, params, Xs[tr], y[tr], Xs[te], cfg, cfg.seed)
        if cfg.ts:
            for name in TS:
                pred[name][te] = fit_predict_ts(name, Xt[tr], y[tr], Xt[te], cfg, cfg.seed)
        tested[te] = True
    rows = []
    for name in names:
        rows.append(dict(protocol="SUBJECT_BLOCKED", subject=sid, model=name,
                         params=json.dumps(used.get(name, []), default=str),
                         n_train=int(np.mean([len(a) for a, _ in outer])), n_test=int(tested.sum()),
                         **metrics(y[tested], pred[name][tested])))
    return rows


def leaky_one(sid, D, cfg):
    """Diagnostic only: random window splits (what the original protocol effectively did)."""
    rows = []
    if sid == "pooled":
        idx = np.arange(len(D["y"]))
        label = "POOLED_RANDOM_SPLIT"
    else:
        idx = np.flatnonzero(D["subj"] == sid)
        label = "SUBJECT_RANDOM_SPLIT"
    y = D["y"][idx]
    tr, te = train_test_split(np.arange(len(idx)), test_size=0.3, stratify=y, random_state=cfg.seed)
    for name in cfg.models:
        p = fit_predict_static(name, default_params(name, cfg), D["Xs"][idx][tr], y[tr],
                               D["Xs"][idx][te], cfg, cfg.seed)
        rows.append(dict(protocol=label, subject=sid, model=name, params="default",
                         n_train=len(tr), n_test=len(te), **metrics(y[te], p)))
    return rows


def calib_one(sid, D, cfg):
    """Cold-start curve. Test = last 20% of every label segment of the target subject.
    subject_only : train on the first q of each segment (purged from test)
    pooled       : train on the other subjects only (= LOSO restricted to this test set)
    pooled+calib : other subjects + first q of the target (weighted)"""
    m = D["subj"] == sid
    seg, pos, y = D["seg"][m], D["pos"][m], D["y"][m]
    Xs = D["Xs"][m]
    n = len(y)
    frac = np.zeros(n)
    first_test = np.full(n, np.inf)
    for s in np.unique(seg):
        idx = np.flatnonzero(seg == s)
        order = idx[np.argsort(pos[idx])]
        frac[order] = np.arange(len(order)) / len(order)
    test = frac >= 0.8
    for s in np.unique(seg):
        ft = pos[(seg == s) & test]
        if len(ft):
            first_test[seg == s] = ft.min()
    others = D["subj"] != sid
    name = cfg.calib_model
    params = default_params(name, cfg)

    def run(A, ya, w=None):
        sc = MinMaxScaler().fit(A)
        clf = cfg.zoo[name][0]().set_params(**params)
        clf.fit(sc.transform(A), ya, **({} if w is None else {"sample_weight": w}))
        return clf.predict(sc.transform(Xs[test]))

    rows = []
    p0 = run(D["Xs"][others], D["y"][others])
    rows.append(dict(subject=sid, mode="pooled", q=0.0, n_calib=0, calib_minutes=0.0,
                     **metrics(y[test], p0)))
    for q in cfg.calib_fracs:
        cal = (frac < q) & (pos <= first_test - cfg.gap - 1)
        if cal.sum() == 0:
            continue
        secs = 0.0
        for s in np.unique(seg[cal]):
            c = int(((seg == s) & cal).sum())
            secs += (c - 1) * cfg.step + cfg.win
        base = dict(subject=sid, q=q, n_calib=int(cal.sum()), calib_minutes=round(secs / 60, 2))
        if len(np.unique(y[cal])) >= 2:
            rows.append(dict(mode="subject_only", **base, **metrics(y[test], run(Xs[cal], y[cal]))))
        A = np.vstack([D["Xs"][others], Xs[cal]])
        ya = np.concatenate([D["y"][others], y[cal]])
        w = np.concatenate([np.ones(others.sum()), np.full(cal.sum(), cfg.calib_weight)])
        rows.append(dict(mode="pooled+calib", **base, **metrics(y[test], run(A, ya, w))))
    return rows


# ----------------------------------------------------------------------------- VAR (separate)
def var_one(sid, root, cfg, maxlag=10):
    """VAR on first differences of z-scored 1 Hz signals; 1-step-ahead RMSE vs persistence."""
    sd = load_subject(root, sid)
    S = sd["sig"][:, sd["first_valid"]:sd["last_valid"] + 1]
    T = (S.shape[1] // FS) * FS
    Y = S[:, :T].reshape(3, -1, FS).mean(2).T            # (time, 3) at 1 Hz
    cut = int(0.7 * len(Y))
    mu, sg = Y[:cut].mean(0), Y[:cut].std(0) + 1e-8
    Y = (Y - mu) / sg
    d = np.diff(Y, axis=0)

    def lagmat(dd, p):
        return np.hstack([dd[p - i - 1:len(dd) - i - 1] for i in range(p)]), dd[p:]

    dtr = d[:cut - 1]
    best = None
    for p in range(1, maxlag + 1):
        Xl, Yl = lagmat(dtr, p)
        Z = np.hstack([np.ones((len(Xl), 1)), Xl])
        B, *_ = np.linalg.lstsq(Z, Yl, rcond=None)
        R = Yl - Z @ B
        k = Y.shape[1]
        aic = np.log(np.linalg.det(R.T @ R / len(R)) + 1e-300) + 2 * p * k * k / len(R)
        if best is None or aic < best[0]:
            best = (aic, p, B)
    _, p, B = best
    Xl, Yl = lagmat(d, p)
    Z = np.hstack([np.ones((len(Xl), 1)), Xl])
    dhat = Z @ B                                          # predicted difference at index p.. of d
    # d[j] = Y[j+1]-Y[j]; row r of Yl is d[p+r] -> target time p+r+1, previous level Y[p+r]
    tgt_time = np.arange(len(Yl)) + p + 1
    test = tgt_time > cut
    y_true = Y[tgt_time[test]]
    y_var = Y[tgt_time[test] - 1] + dhat[test]
    y_per = Y[tgt_time[test] - 1]
    rows = []
    for j, c in enumerate(CHANNELS):
        rv = float(np.sqrt(np.mean((y_true[:, j] - y_var[:, j]) ** 2)))
        rp = float(np.sqrt(np.mean((y_true[:, j] - y_per[:, j]) ** 2)))
        rows.append(dict(subject=sid, channel=c, lag=p, rmse_var=rv, rmse_persistence=rp,
                         ratio_var_over_persistence=rv / rp if rp > 0 else np.nan,
                         n_test=int(test.sum())))
    return rows


# ----------------------------------------------------------------------------- statistics / reporting
def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj, run, m = np.empty(len(p)), 0.0, len(p)
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj


def wilcoxon_safe(x, y):
    d = np.asarray(x) - np.asarray(y)
    if np.allclose(d, 0):
        return np.nan
    try:
        return float(wilcoxon(x, y).pvalue)
    except Exception:
        return np.nan


def build_stats(loso, subj, metric="macro_f1"):
    rows = []
    # (1) personalization: subject-specific (blocked) vs LOSO, same model, paired over subjects
    fam = []
    for m in sorted(set(loso.model) & set(subj.model)):
        a = subj[subj.model == m].set_index("subject")[metric]
        b = loso[loso.model == m].set_index("subject")[metric]
        j = a.index.intersection(b.index)
        if len(j) < 5:
            continue
        fam.append(dict(family="personalization", comparison=f"{m}: subject-specific vs LOSO",
                        n=len(j), mean_diff=float((a[j] - b[j]).mean()),
                        p=wilcoxon_safe(a[j].values, b[j].values)))
    # (2) time-series vs static, matched windows/folds, within protocol
    fam2 = []
    for proto, df in (("LOSO", loso), ("SUBJECT_BLOCKED", subj)):
        for t in TS:
            for s in STATIC:
                if t not in set(df.model) or s not in set(df.model):
                    continue
                a = df[df.model == t].set_index("subject")[metric]
                b = df[df.model == s].set_index("subject")[metric]
                j = a.index.intersection(b.index)
                if len(j) < 5:
                    continue
                fam2.append(dict(family=f"ts_vs_static[{proto}]", comparison=f"{t} vs {s}",
                                 n=len(j), mean_diff=float((a[j] - b[j]).mean()),
                                 p=wilcoxon_safe(a[j].values, b[j].values)))
    for f in (fam, fam2):
        if f:
            adj = holm([r["p"] if not np.isnan(r["p"]) else 1.0 for r in f])
            for r, ap in zip(f, adj):
                r["p_holm"] = float(ap)
    return pd.DataFrame(fam + fam2)


def mean_sd_table(df):
    g = df.groupby(["protocol", "model"])
    out = g[["acc", "bal_acc", "macro_f1"]].agg(["mean", "std"])
    t = pd.DataFrame(index=out.index)
    for c in ("acc", "bal_acc", "macro_f1"):
        t[c] = [f"{m:.3f} ± {s:.3f}" for m, s in zip(out[(c, "mean")], out[(c, "std")].fillna(0))]
    t["n_subjects"] = g["subject"].nunique()
    return t.reset_index()


def to_md(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- main
def make_cfg(a):
    cfg = argparse.Namespace(**vars(a))
    cfg.zoo = model_zoo(a.seed, a.smote)
    cfg.models = STATIC
    cfg.gap = int(math.ceil(a.win / a.step))
    cfg.calib_fracs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    cfg.inner_loso = 5
    cfg.inner_folds = 3
    cfg.tsf_trees = 50 if a.quick else 200
    cfg.rocket_kernels = 300 if a.quick else 1000
    cfg.own_rocket = a.own_rocket
    return cfg


def run(args):
    t0 = time.time()
    root, out = Path(args.root), Path(args.out)
    cfg = make_cfg(args)
    subjects = args.subjects or SUBJECTS
    ensure_wesad_dataset(root, subjects)
    out.mkdir(parents=True, exist_ok=True)
    D, summ = build_dataset(root, subjects, args.win, args.step)
    D = encode_task(D, args.task)
    if args.extra_feats:  # control: give static models the std and slope that TSF can exploit
        Xt = D["Xt"].astype(float)
        tt = (np.arange(Xt.shape[2]) - (Xt.shape[2] - 1) / 2.0) / FS      # seconds, centered
        std = Xt.std(axis=2)                                               # (n, 3)
        slope = (Xt * tt).sum(axis=2) / (tt ** 2).sum()                    # units per second
        D["Xs"] = np.hstack([D["Xs"], std, slope])                         # 9 -> 15 features
        print(f"[info] extra features enabled: {D['Xs'].shape[1]} static features per window")
    summ.to_csv(out / "windows_per_subject.csv", index=False)
    ids = sorted(np.unique(D["subj"]).tolist())
    print(f"[info] {len(ids)} subjects, {len(D['y'])} windows "
          f"({args.win:.0f} s window, {args.step:.0f} s step, purge gap {cfg.gap} windows)")
    print(summ.to_string(index=False))
    J = dict(n_jobs=args.n_jobs)

    loso = pd.DataFrame(sum(Parallel(**J)(delayed(loso_one)(s, D, cfg) for s in ids), []))
    loso.to_csv(out / "loso_per_subject.csv", index=False)
    print(f"[done] LOSO ({time.time() - t0:.0f}s)")

    subj = pd.DataFrame(sum(Parallel(**J)(delayed(subject_one)(s, D, cfg) for s in ids), []))
    subj.to_csv(out / "subject_blocked_per_subject.csv", index=False)
    print(f"[done] subject-specific blocked CV ({time.time() - t0:.0f}s)")

    leaky = pd.DataFrame(sum(Parallel(**J)(delayed(leaky_one)(s, D, cfg) for s in ["pooled"] + ids), []))
    leaky.to_csv(out / "diagnostic_random_split.csv", index=False)

    calib = pd.DataFrame(sum(Parallel(**J)(delayed(calib_one)(s, D, cfg) for s in ids), []))
    calib.to_csv(out / "calibration_curve_per_subject.csv", index=False)

    var = None
    if not args.skip_var:
        try:
            var = pd.DataFrame(sum(Parallel(**J)(delayed(var_one)(s, root, cfg) for s in ids), []))
            var.to_csv(out / "var_forecasting.csv", index=False)
        except Exception as e:
            print(f"[warn] VAR skipped: {e}", file=sys.stderr)

    stats = build_stats(loso, subj)
    stats.to_csv(out / "statistical_tests.csv", index=False)

    # ---- summary
    md = ["# Rerun summary", "",
          f"Task: {args.task}; window {args.win:.0f} s, step {args.step:.0f} s; blocked folds K={args.folds}; "
          f"SMOTE in-fold: {bool(args.smote)}; tuning: {not args.no_tune}", "",
          "## Data per subject (for the personalization-feasibility sentence)",
          f"- windows per subject: {summ.n_windows.mean():.0f} ± {summ.n_windows.std():.0f} "
          f"(range {summ.n_windows.min()}–{summ.n_windows.max()})",
          f"- labeled minutes per subject: {summ.labeled_minutes.mean():.1f} ± {summ.labeled_minutes.std():.1f} "
          f"(range {summ.labeled_minutes.min():.1f}–{summ.labeled_minutes.max():.1f})", "",
          "## Main results (mean ± SD over subjects; per-subject values in CSV)",
          to_md(mean_sd_table(pd.concat([loso, subj]))), "",
          "## Diagnostic: random window splits (what the original protocol effectively did)",
          to_md(mean_sd_table(leaky)), ""]
    if len(stats):
        md += ["## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)", to_md(stats.round(4)), ""]
    cc = calib.groupby(["mode", "q"])[["n_calib", "calib_minutes", "macro_f1", "bal_acc", "acc"]].mean().round(3)
    md += [f"## Calibration / cold-start curve ({args.calib_model}; mean over subjects)", to_md(cc.reset_index()), ""]
    if var is not None and len(var):
        vv = var.groupby("channel")[["rmse_var", "rmse_persistence", "ratio_var_over_persistence"]].agg(["mean", "std"]).round(4)
        vv.columns = ["_".join(c) for c in vv.columns]
        md += ["## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)",
               to_md(vv.reset_index()), "",
               "RMSE (forecasting) and macro-F1 (classification) are NOT comparable."]
    (out / "summary.md").write_text("\n".join(md))
    json.dump(dict(args={k: v for k, v in vars(args).items()}, subjects=ids,
                   seconds=round(time.time() - t0)), open(out / "run_info.json", "w"), indent=2, default=str)
    print(f"[done] all outputs in {out}/  (summary.md first)  total {time.time() - t0:.0f}s")


# ----------------------------------------------------------------------------- synthetic self-test
def make_synthetic(root: Path, n_subjects=6, seed=0):
    import pickle
    rng = np.random.default_rng(seed)
    plan = [(0, 20), (1, 300), (0, 10), (2, 180), (4, 90), (3, 150), (4, 90), (0, 10)]
    ids = SUBJECTS[:n_subjects]
    for k, sid in enumerate(ids):
        sec = sum(d for _, d in plan)
        n = sec * FS
        lab_s = np.concatenate([np.full(d, L) for L, d in plan])
        lab700 = np.repeat(lab_s, 700)
        lab_4 = np.repeat(lab_s, FS)
        off = rng.normal(0, 1, 3)
        eda = 2 + off[0] + 0.8 * (lab_4 == 2) + 0.3 * (lab_4 == 3) + 0.2 * np.cumsum(rng.normal(0, .01, n))
        temp = 33 + off[1] - 0.4 * (lab_4 == 2) + 0.1 * np.cumsum(rng.normal(0, .005, n))
        hr = 70 + 4 * off[2] + 8 * (lab_4[::FS] == 2) + 3 * (lab_4[::FS] == 3)
        eda += rng.normal(0, .15, n); temp += rng.normal(0, .05, n); hr = hr + rng.normal(0, 2, len(hr))
        sdir = root / f"S{sid}"
        sdir.mkdir(parents=True)
        pickle.dump({"signal": {"wrist": {"EDA": eda[:, None], "TEMP": temp[:, None],
                                          "BVP": rng.normal(size=(n * 16, 1)), "ACC": np.zeros((n * 8, 3))}},
                     "label": lab700, "subject": f"S{sid}"}, open(sdir / f"S{sid}.pkl", "wb"))
        hr_txt = "1000010.0\n1.000000\n" + "\n".join(f"{v:.2f}" for v in hr[10:])
        eda_txt = "1000000.0\n4.000000\n" + "\n".join(f"{v:.5f}" for v in eda)
        if k % 2 == 0:
            (sdir / f"S{sid}_E4_Data").mkdir()
            (sdir / f"S{sid}_E4_Data" / "HR.csv").write_text(hr_txt)
            (sdir / f"S{sid}_E4_Data" / "EDA.csv").write_text(eda_txt)
        else:
            with zipfile.ZipFile(sdir / f"S{sid}_E4_Data.zip", "w") as z:
                z.writestr("HR.csv", hr_txt); z.writestr("EDA.csv", eda_txt)
    return ids


def parse():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", help="WESAD root directory")
    p.add_argument("--out", default="results")
    p.add_argument("--win", type=float, default=60.0, help="window length (s)")
    p.add_argument("--step", type=float, default=30.0, help="window step (s)")
    p.add_argument("--task", choices=["multiclass", "binary"], default="multiclass",
                   help="multiclass: baseline/stress/amusement/meditation; binary: stress vs rest")
    p.add_argument("--folds", type=int, default=5, help="blocked CV folds for subject-specific models")
    p.add_argument("--smote", type=int, default=0, help="1 = SMOTE inside training folds only")
    p.add_argument("--no-tune", action="store_true", help="skip hyper-parameter search")
    p.add_argument("--extra-feats", action="store_true",
                   help="control: add per-window std and slope (15 static features instead of 9)")
    p.add_argument("--no-ts", dest="ts", action="store_false", help="skip TSF/ROCKET")
    p.add_argument("--own-rocket", action="store_true", help="force the in-script ROCKET")
    p.add_argument("--skip-var", action="store_true")
    p.add_argument("--calib-model", choices=["RF", "LR", "SVM"], default="RF")
    p.add_argument("--calib-weight", type=float, default=5.0)
    p.add_argument("--subjects", type=int, nargs="*")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--n-jobs", type=int, default=-1)
    p.add_argument("--quick", action="store_true", help="smaller TS models (smoke test)")
    p.add_argument("--selftest", action="store_true", help="run on synthetic data")
    return p.parse_args()


if __name__ == "__main__":
    a = parse()
    if a.selftest:
        tmp = Path(tempfile.mkdtemp())
        ids = make_synthetic(tmp / "WESAD")
        a.root, a.subjects, a.quick, a.no_tune = str(tmp / "WESAD"), ids, True, True
        a.win, a.step, a.out = 20.0, 10.0, a.out if a.out != "results" else "selftest_results"
    if not a.root:
        sys.exit("--root is required (or use --selftest)")
    run(a)
