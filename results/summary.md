# Rerun summary

Task: multiclass; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.493 ± 0.205 | 0.428 ± 0.163 | 0.368 ± 0.188 | 15 |
| LOSO | NN | 0.517 ± 0.164 | 0.416 ± 0.142 | 0.367 ± 0.160 | 15 |
| LOSO | RF | 0.470 ± 0.124 | 0.414 ± 0.113 | 0.343 ± 0.132 | 15 |
| LOSO | ROCKET | 0.472 ± 0.135 | 0.410 ± 0.098 | 0.373 ± 0.107 | 15 |
| LOSO | SVM | 0.461 ± 0.192 | 0.400 ± 0.141 | 0.336 ± 0.169 | 15 |
| LOSO | TSF | 0.619 ± 0.186 | 0.533 ± 0.152 | 0.483 ± 0.183 | 15 |
| LOSO | kNN | 0.450 ± 0.190 | 0.382 ± 0.141 | 0.336 ± 0.156 | 15 |
| SUBJECT_BLOCKED | LR | 0.780 ± 0.103 | 0.788 ± 0.099 | 0.756 ± 0.101 | 15 |
| SUBJECT_BLOCKED | NN | 0.817 ± 0.099 | 0.777 ± 0.120 | 0.775 ± 0.119 | 15 |
| SUBJECT_BLOCKED | RF | 0.843 ± 0.078 | 0.823 ± 0.072 | 0.814 ± 0.074 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.791 ± 0.094 | 0.776 ± 0.104 | 0.767 ± 0.101 | 15 |
| SUBJECT_BLOCKED | SVM | 0.811 ± 0.077 | 0.817 ± 0.072 | 0.790 ± 0.074 | 15 |
| SUBJECT_BLOCKED | TSF | 0.825 ± 0.067 | 0.778 ± 0.077 | 0.777 ± 0.075 | 15 |
| SUBJECT_BLOCKED | kNN | 0.836 ± 0.058 | 0.819 ± 0.066 | 0.807 ± 0.060 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.488 ± 0.000 | 0.423 ± 0.000 | 0.418 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.619 ± 0.000 | 0.500 ± 0.000 | 0.471 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.902 ± 0.000 | 0.914 ± 0.000 | 0.906 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.600 ± 0.000 | 0.562 ± 0.000 | 0.555 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.824 ± 0.000 | 0.818 ± 0.000 | 0.814 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.820 ± 0.094 | 0.802 ± 0.100 | 0.776 ± 0.100 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.873 ± 0.071 | 0.789 ± 0.122 | 0.784 ± 0.133 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.976 ± 0.035 | 0.958 ± 0.067 | 0.962 ± 0.060 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.872 ± 0.090 | 0.870 ± 0.085 | 0.840 ± 0.097 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.941 ± 0.055 | 0.919 ± 0.076 | 0.918 ± 0.084 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.3872 | 0.0001 | 0.0004 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.4082 | 0.0001 | 0.0004 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.4706 | 0.0001 | 0.0004 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.3939 | 0.0001 | 0.0004 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.4546 | 0.0001 | 0.0004 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.2943 | 0.0001 | 0.0004 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.4716 | 0.0001 | 0.0004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.1471 | 0.0215 | 0.3878 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.1145 | 0.073 | 1.0 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.1397 | 0.0043 | 0.0812 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.147 | 0.002 | 0.0403 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.1161 | 0.0554 | 0.9411 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | 0.0372 | 0.3591 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | 0.0047 | 0.7197 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | 0.0298 | 0.2078 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | 0.0372 | 0.5614 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | 0.0063 | 0.6788 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.0303 | 0.2078 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | 0.0216 | 0.5995 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0366 | 0.0833 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | -0.0134 | 0.8904 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | 0.0021 | 0.8904 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0404 | 0.0833 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | 0.0114 | 0.6387 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0468 | 0.1205 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | -0.0235 | 0.7197 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | -0.008 | 0.9341 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.299 | 0.384 | 0.43 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.47 | 0.549 | 0.551 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.51 | 0.592 | 0.571 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.546 | 0.617 | 0.606 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.564 | 0.633 | 0.626 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.587 | 0.655 | 0.646 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.656 | 0.709 | 0.705 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.494 | 0.579 | 0.514 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.595 | 0.665 | 0.641 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.583 | 0.657 | 0.637 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.628 | 0.69 | 0.693 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.659 | 0.712 | 0.724 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.708 | 0.754 | 0.764 |

## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)
| channel | rmse_var_mean | rmse_var_std | rmse_persistence_mean | rmse_persistence_std | ratio_var_over_persistence_mean | ratio_var_over_persistence_std |
|---|---|---|---|---|---|---|
| eda | 0.0565 | 0.065 | 0.0556 | 0.0619 | 1.033 | 0.0845 |
| hr | 0.0055 | 0.0018 | 0.0331 | 0.012 | 0.17 | 0.0296 |
| temp | 0.0233 | 0.0134 | 0.026 | 0.0136 | 0.8794 | 0.0612 |

RMSE (forecasting) and macro-F1 (classification) are NOT comparable.