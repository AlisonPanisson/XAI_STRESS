# Rerun summary

Task: binary; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.849 ± 0.122 | 0.841 ± 0.117 | 0.806 ± 0.133 | 15 |
| LOSO | NN | 0.890 ± 0.097 | 0.839 ± 0.126 | 0.837 ± 0.121 | 15 |
| LOSO | RF | 0.867 ± 0.109 | 0.822 ± 0.136 | 0.806 ± 0.155 | 15 |
| LOSO | ROCKET | 0.827 ± 0.145 | 0.768 ± 0.153 | 0.753 ± 0.168 | 15 |
| LOSO | SVM | 0.892 ± 0.104 | 0.877 ± 0.114 | 0.855 ± 0.120 | 15 |
| LOSO | TSF | 0.907 ± 0.093 | 0.866 ± 0.095 | 0.869 ± 0.106 | 15 |
| LOSO | kNN | 0.866 ± 0.068 | 0.794 ± 0.129 | 0.788 ± 0.106 | 15 |
| SUBJECT_BLOCKED | LR | 0.978 ± 0.046 | 0.979 ± 0.051 | 0.970 ± 0.060 | 15 |
| SUBJECT_BLOCKED | NN | 0.971 ± 0.046 | 0.963 ± 0.057 | 0.959 ± 0.062 | 15 |
| SUBJECT_BLOCKED | RF | 0.985 ± 0.030 | 0.980 ± 0.051 | 0.978 ± 0.047 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.968 ± 0.059 | 0.956 ± 0.084 | 0.953 ± 0.085 | 15 |
| SUBJECT_BLOCKED | SVM | 0.961 ± 0.074 | 0.946 ± 0.100 | 0.945 ± 0.102 | 15 |
| SUBJECT_BLOCKED | TSF | 0.974 ± 0.058 | 0.963 ± 0.087 | 0.962 ± 0.087 | 15 |
| SUBJECT_BLOCKED | kNN | 0.981 ± 0.056 | 0.972 ± 0.082 | 0.972 ± 0.082 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.857 ± 0.000 | 0.847 ± 0.000 | 0.812 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.945 ± 0.000 | 0.903 ± 0.000 | 0.918 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.993 ± 0.000 | 0.995 ± 0.000 | 0.990 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.952 ± 0.000 | 0.942 ± 0.000 | 0.932 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.952 ± 0.000 | 0.923 ± 0.000 | 0.930 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.979 ± 0.040 | 0.974 ± 0.057 | 0.969 ± 0.058 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.983 ± 0.048 | 0.973 ± 0.072 | 0.975 ± 0.070 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.998 ± 0.009 | 0.998 ± 0.006 | 0.997 ± 0.013 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.995 ± 0.018 | 0.997 ± 0.012 | 0.994 ± 0.025 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.998 ± 0.009 | 0.998 ± 0.006 | 0.997 ± 0.013 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.164 | 0.0022 | 0.0089 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.1222 | 0.0023 | 0.0089 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.1721 | 0.001 | 0.0049 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.2001 | 0.0004 | 0.003 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.0898 | 0.015 | 0.022 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.093 | 0.011 | 0.022 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.1844 | 0.0004 | 0.003 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.0816 | 0.0084 | 0.1672 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.0635 | 0.3003 | 1.0 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.0633 | 0.0736 | 1.0 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.014 | 0.5936 | 1.0 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.032 | 0.3463 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | -0.0343 | 0.5614 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | -0.0524 | 0.3591 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | -0.0527 | 0.4543 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | -0.1019 | 0.0256 | 0.4859 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | -0.0839 | 0.1354 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.0099 | 0.0273 | 0.4911 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | -0.0075 | 0.4409 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0159 | 0.0656 | 0.984 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | 0.0172 | 0.0413 | 0.7023 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | 0.0028 | 0.4446 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0187 | 0.2596 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | -0.0163 | 0.0772 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0247 | 0.0504 | 0.8066 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | 0.0084 | 0.2787 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | -0.006 | 0.8784 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.755 | 0.772 | 0.859 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.79 | 0.796 | 0.882 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.812 | 0.818 | 0.898 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.806 | 0.809 | 0.906 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.807 | 0.811 | 0.91 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.83 | 0.833 | 0.922 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.835 | 0.839 | 0.922 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.824 | 0.833 | 0.925 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.83 | 0.825 | 0.921 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.867 | 0.867 | 0.94 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.89 | 0.892 | 0.952 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.937 | 0.933 | 0.969 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.949 | 0.95 | 0.976 |

## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)
| channel | rmse_var_mean | rmse_var_std | rmse_persistence_mean | rmse_persistence_std | ratio_var_over_persistence_mean | ratio_var_over_persistence_std |
|---|---|---|---|---|---|---|
| eda | 0.0518 | 0.0494 | 0.0507 | 0.0467 | 1.0383 | 0.09 |
| hr | 0.0685 | 0.0149 | 0.1587 | 0.0363 | 0.4357 | 0.0389 |
| temp | 0.0233 | 0.0134 | 0.0261 | 0.0136 | 0.8783 | 0.0612 |

RMSE (forecasting) and macro-F1 (classification) are NOT comparable.