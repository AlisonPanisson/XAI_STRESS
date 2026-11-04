# Rerun summary

Task: binary; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.715 ± 0.164 | 0.704 ± 0.132 | 0.632 ± 0.175 | 15 |
| LOSO | NN | 0.790 ± 0.132 | 0.667 ± 0.178 | 0.639 ± 0.199 | 15 |
| LOSO | RF | 0.785 ± 0.179 | 0.736 ± 0.160 | 0.686 ± 0.215 | 15 |
| LOSO | ROCKET | 0.769 ± 0.138 | 0.677 ± 0.141 | 0.647 ± 0.152 | 15 |
| LOSO | SVM | 0.708 ± 0.206 | 0.689 ± 0.152 | 0.612 ± 0.209 | 15 |
| LOSO | TSF | 0.898 ± 0.065 | 0.839 ± 0.123 | 0.835 ± 0.133 | 15 |
| LOSO | kNN | 0.740 ± 0.191 | 0.654 ± 0.197 | 0.625 ± 0.212 | 15 |
| SUBJECT_BLOCKED | LR | 0.960 ± 0.073 | 0.961 ± 0.073 | 0.949 ± 0.091 | 15 |
| SUBJECT_BLOCKED | NN | 0.958 ± 0.070 | 0.940 ± 0.097 | 0.940 ± 0.100 | 15 |
| SUBJECT_BLOCKED | RF | 0.968 ± 0.046 | 0.962 ± 0.060 | 0.956 ± 0.064 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.968 ± 0.072 | 0.967 ± 0.072 | 0.960 ± 0.088 | 15 |
| SUBJECT_BLOCKED | SVM | 0.968 ± 0.057 | 0.963 ± 0.057 | 0.957 ± 0.072 | 15 |
| SUBJECT_BLOCKED | TSF | 0.964 ± 0.061 | 0.947 ± 0.093 | 0.947 ± 0.091 | 15 |
| SUBJECT_BLOCKED | kNN | 0.978 ± 0.039 | 0.975 ± 0.052 | 0.970 ± 0.055 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.738 ± 0.000 | 0.739 ± 0.000 | 0.685 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.871 ± 0.000 | 0.787 ± 0.000 | 0.803 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.950 ± 0.000 | 0.964 ± 0.000 | 0.932 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.812 ± 0.000 | 0.848 ± 0.000 | 0.775 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.967 ± 0.000 | 0.952 ± 0.000 | 0.952 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.958 ± 0.079 | 0.973 ± 0.052 | 0.950 ± 0.088 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.986 ± 0.039 | 0.983 ± 0.055 | 0.980 ± 0.058 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.991 ± 0.025 | 0.990 ± 0.029 | 0.987 ± 0.035 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.998 ± 0.009 | 0.998 ± 0.006 | 0.997 ± 0.013 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.998 ± 0.009 | 0.999 ± 0.006 | 0.997 ± 0.013 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.3173 | 0.0001 | 0.0006 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.3003 | 0.002 | 0.004 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.2699 | 0.001 | 0.0029 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.3129 | 0.0001 | 0.0006 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.3456 | 0.0001 | 0.0004 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.1116 | 0.0103 | 0.0103 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.3448 | 0.0001 | 0.0004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.2102 | 0.0043 | 0.0769 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.2034 | 0.001 | 0.0196 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.1493 | 0.0303 | 0.4549 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.2232 | 0.002 | 0.0383 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.1957 | 0.0043 | 0.0769 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | 0.0221 | 0.7299 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | 0.0153 | 0.7776 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | -0.0388 | 0.3967 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | 0.0351 | 0.7197 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | 0.0076 | 0.975 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.023 | 0.1027 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | -0.0022 | 0.5533 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0089 | 0.499 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | -0.0108 | 0.5406 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | 0.0071 | 0.8384 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0099 | 0.4838 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | 0.011 | 0.2626 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | 0.0042 | 0.7555 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | 0.0024 | 0.398 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | 0.0203 | 0.0128 | 0.2047 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.654 | 0.688 | 0.792 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.729 | 0.764 | 0.855 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.748 | 0.781 | 0.862 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.75 | 0.787 | 0.859 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.743 | 0.781 | 0.851 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.746 | 0.784 | 0.855 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.768 | 0.801 | 0.863 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.856 | 0.864 | 0.898 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.862 | 0.863 | 0.906 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.857 | 0.858 | 0.898 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.908 | 0.913 | 0.937 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.908 | 0.913 | 0.937 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.919 | 0.924 | 0.945 |

## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)
| channel | rmse_var_mean | rmse_var_std | rmse_persistence_mean | rmse_persistence_std | ratio_var_over_persistence_mean | ratio_var_over_persistence_std |
|---|---|---|---|---|---|---|
| eda | 0.0565 | 0.065 | 0.0556 | 0.0619 | 1.033 | 0.0845 |
| hr | 0.0055 | 0.0018 | 0.0331 | 0.012 | 0.17 | 0.0296 |
| temp | 0.0233 | 0.0134 | 0.026 | 0.0136 | 0.8794 | 0.0612 |

RMSE (forecasting) and macro-F1 (classification) are NOT comparable.