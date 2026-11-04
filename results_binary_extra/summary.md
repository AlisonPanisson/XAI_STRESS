# Rerun summary

Task: binary; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.761 ± 0.129 | 0.752 ± 0.133 | 0.691 ± 0.149 | 15 |
| LOSO | NN | 0.861 ± 0.093 | 0.796 ± 0.151 | 0.777 ± 0.169 | 15 |
| LOSO | RF | 0.840 ± 0.128 | 0.792 ± 0.143 | 0.766 ± 0.176 | 15 |
| LOSO | ROCKET | 0.769 ± 0.138 | 0.677 ± 0.141 | 0.647 ± 0.152 | 15 |
| LOSO | SVM | 0.759 ± 0.191 | 0.714 ± 0.162 | 0.666 ± 0.216 | 15 |
| LOSO | TSF | 0.898 ± 0.065 | 0.839 ± 0.123 | 0.835 ± 0.133 | 15 |
| LOSO | kNN | 0.781 ± 0.164 | 0.695 ± 0.196 | 0.674 ± 0.213 | 15 |
| SUBJECT_BLOCKED | LR | 0.970 ± 0.056 | 0.971 ± 0.063 | 0.960 ± 0.073 | 15 |
| SUBJECT_BLOCKED | NN | 0.966 ± 0.054 | 0.959 ± 0.062 | 0.954 ± 0.072 | 15 |
| SUBJECT_BLOCKED | RF | 0.983 ± 0.028 | 0.978 ± 0.042 | 0.976 ± 0.041 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.968 ± 0.072 | 0.967 ± 0.072 | 0.960 ± 0.088 | 15 |
| SUBJECT_BLOCKED | SVM | 0.965 ± 0.056 | 0.948 ± 0.077 | 0.951 ± 0.078 | 15 |
| SUBJECT_BLOCKED | TSF | 0.964 ± 0.061 | 0.947 ± 0.093 | 0.947 ± 0.091 | 15 |
| SUBJECT_BLOCKED | kNN | 0.978 ± 0.047 | 0.969 ± 0.070 | 0.968 ± 0.067 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.762 ± 0.000 | 0.778 ± 0.000 | 0.715 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.888 ± 0.000 | 0.793 ± 0.000 | 0.821 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.960 ± 0.000 | 0.970 ± 0.000 | 0.944 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.881 ± 0.000 | 0.862 ± 0.000 | 0.838 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.952 ± 0.000 | 0.927 ± 0.000 | 0.930 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.974 ± 0.045 | 0.983 ± 0.029 | 0.967 ± 0.055 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.993 ± 0.020 | 0.987 ± 0.034 | 0.989 ± 0.030 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.2686 | 0.0001 | 0.0009 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.1774 | 0.001 | 0.004 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.2098 | 0.001 | 0.004 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.3129 | 0.0001 | 0.0009 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.2853 | 0.0008 | 0.004 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.1116 | 0.0103 | 0.0103 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.2941 | 0.0012 | 0.004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.1614 | 0.0215 | 0.3663 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.1436 | 0.0015 | 0.0305 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.0689 | 0.124 | 1.0 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.1694 | 0.0303 | 0.4549 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.0583 | 0.1005 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | -0.0268 | 0.4887 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | -0.0445 | 0.2455 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | -0.1192 | 0.0071 | 0.1355 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | -0.0188 | 0.7119 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | -0.1298 | 0.0157 | 0.2818 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.0211 | 0.0663 | 0.9284 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | -0.0134 | 0.4008 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0292 | 0.0273 | 0.4365 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | -0.0043 | 0.9292 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | -0.0074 | 0.7555 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0079 | 0.4768 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | -0.0002 | 0.859 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0161 | 0.7989 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | 0.0089 | 0.5076 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | 0.0057 | 0.5751 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.796 | 0.811 | 0.878 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.841 | 0.849 | 0.91 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.862 | 0.868 | 0.922 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.858 | 0.865 | 0.918 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.863 | 0.871 | 0.918 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.862 | 0.865 | 0.918 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.868 | 0.876 | 0.925 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.881 | 0.891 | 0.922 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.901 | 0.912 | 0.953 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.947 | 0.953 | 0.973 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.951 | 0.956 | 0.976 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.957 | 0.964 | 0.98 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.962 | 0.967 | 0.984 |

## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)
| channel | rmse_var_mean | rmse_var_std | rmse_persistence_mean | rmse_persistence_std | ratio_var_over_persistence_mean | ratio_var_over_persistence_std |
|---|---|---|---|---|---|---|
| eda | 0.0565 | 0.065 | 0.0556 | 0.0619 | 1.033 | 0.0845 |
| hr | 0.0055 | 0.0018 | 0.0331 | 0.012 | 0.17 | 0.0296 |
| temp | 0.0233 | 0.0134 | 0.026 | 0.0136 | 0.8794 | 0.0612 |

RMSE (forecasting) and macro-F1 (classification) are NOT comparable.