# Rerun summary

Task: binary; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.805 ± 0.170 | 0.797 ± 0.149 | 0.751 ± 0.178 | 15 |
| LOSO | NN | 0.856 ± 0.113 | 0.785 ± 0.168 | 0.773 ± 0.158 | 15 |
| LOSO | RF | 0.792 ± 0.149 | 0.747 ± 0.161 | 0.713 ± 0.175 | 15 |
| LOSO | ROCKET | 0.827 ± 0.145 | 0.768 ± 0.153 | 0.753 ± 0.168 | 15 |
| LOSO | SVM | 0.875 ± 0.125 | 0.852 ± 0.138 | 0.831 ± 0.143 | 15 |
| LOSO | TSF | 0.907 ± 0.093 | 0.866 ± 0.095 | 0.869 ± 0.106 | 15 |
| LOSO | kNN | 0.855 ± 0.064 | 0.795 ± 0.119 | 0.780 ± 0.103 | 15 |
| SUBJECT_BLOCKED | LR | 0.968 ± 0.074 | 0.961 ± 0.096 | 0.955 ± 0.100 | 15 |
| SUBJECT_BLOCKED | NN | 0.970 ± 0.057 | 0.958 ± 0.077 | 0.958 ± 0.080 | 15 |
| SUBJECT_BLOCKED | RF | 0.977 ± 0.037 | 0.971 ± 0.050 | 0.967 ± 0.052 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.968 ± 0.059 | 0.956 ± 0.084 | 0.953 ± 0.085 | 15 |
| SUBJECT_BLOCKED | SVM | 0.980 ± 0.045 | 0.971 ± 0.070 | 0.971 ± 0.067 | 15 |
| SUBJECT_BLOCKED | TSF | 0.974 ± 0.058 | 0.963 ± 0.087 | 0.962 ± 0.087 | 15 |
| SUBJECT_BLOCKED | kNN | 0.979 ± 0.047 | 0.967 ± 0.077 | 0.968 ± 0.073 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.833 ± 0.000 | 0.824 ± 0.000 | 0.784 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.940 ± 0.000 | 0.889 ± 0.000 | 0.909 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.981 ± 0.000 | 0.972 ± 0.000 | 0.972 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.929 ± 0.000 | 0.912 ± 0.000 | 0.899 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.962 ± 0.000 | 0.937 ± 0.000 | 0.944 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.967 ± 0.062 | 0.963 ± 0.081 | 0.954 ± 0.087 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.991 ± 0.025 | 0.982 ± 0.049 | 0.985 ± 0.040 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.998 ± 0.009 | 0.998 ± 0.006 | 0.997 ± 0.013 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.995 ± 0.018 | 0.997 ± 0.012 | 0.994 ± 0.025 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.998 ± 0.009 | 0.998 ± 0.006 | 0.997 ± 0.013 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.2044 | 0.001 | 0.0049 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.185 | 0.0012 | 0.0049 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.2536 | 0.001 | 0.0049 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.2001 | 0.0004 | 0.0026 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.1394 | 0.0015 | 0.0049 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.093 | 0.011 | 0.011 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.1883 | 0.0001 | 0.0004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.0897 | 0.0067 | 0.1276 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.1184 | 0.0353 | 0.6361 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.1559 | 0.0063 | 0.1264 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.0379 | 0.2719 | 1.0 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.0964 | 0.0555 | 0.9441 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | -0.0262 | 0.8469 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | 0.0024 | 0.9341 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | 0.0399 | 0.4887 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | -0.078 | 0.1094 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | -0.0195 | 0.925 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.0056 | 0.4959 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | 0.0069 | 0.7349 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0048 | 0.6741 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | -0.0085 | 0.4461 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | 0.0044 | 0.7353 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0144 | 0.0925 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | -0.0019 | 0.8587 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0136 | 0.2604 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | -0.0173 | 0.1258 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | -0.0044 | 0.6744 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.676 | 0.719 | 0.811 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.734 | 0.749 | 0.858 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.737 | 0.752 | 0.862 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.761 | 0.779 | 0.878 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.77 | 0.793 | 0.889 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.786 | 0.81 | 0.897 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.845 | 0.862 | 0.925 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.788 | 0.802 | 0.886 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.814 | 0.821 | 0.897 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.815 | 0.824 | 0.901 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.838 | 0.849 | 0.913 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.882 | 0.89 | 0.929 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.896 | 0.899 | 0.933 |
