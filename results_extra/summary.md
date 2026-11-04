# Rerun summary

Task: multiclass; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.508 ± 0.183 | 0.480 ± 0.144 | 0.431 ± 0.159 | 15 |
| LOSO | NN | 0.613 ± 0.157 | 0.534 ± 0.139 | 0.502 ± 0.151 | 15 |
| LOSO | RF | 0.570 ± 0.129 | 0.491 ± 0.101 | 0.440 ± 0.130 | 15 |
| LOSO | ROCKET | 0.472 ± 0.135 | 0.410 ± 0.098 | 0.373 ± 0.107 | 15 |
| LOSO | SVM | 0.545 ± 0.149 | 0.487 ± 0.120 | 0.440 ± 0.142 | 15 |
| LOSO | TSF | 0.619 ± 0.186 | 0.533 ± 0.152 | 0.483 ± 0.183 | 15 |
| LOSO | kNN | 0.500 ± 0.164 | 0.429 ± 0.116 | 0.385 ± 0.143 | 15 |
| SUBJECT_BLOCKED | LR | 0.789 ± 0.097 | 0.789 ± 0.093 | 0.766 ± 0.088 | 15 |
| SUBJECT_BLOCKED | NN | 0.805 ± 0.079 | 0.756 ± 0.103 | 0.753 ± 0.102 | 15 |
| SUBJECT_BLOCKED | RF | 0.864 ± 0.055 | 0.840 ± 0.058 | 0.835 ± 0.057 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.791 ± 0.094 | 0.776 ± 0.104 | 0.767 ± 0.101 | 15 |
| SUBJECT_BLOCKED | SVM | 0.798 ± 0.082 | 0.788 ± 0.086 | 0.768 ± 0.081 | 15 |
| SUBJECT_BLOCKED | TSF | 0.825 ± 0.067 | 0.778 ± 0.077 | 0.777 ± 0.075 | 15 |
| SUBJECT_BLOCKED | kNN | 0.815 ± 0.074 | 0.775 ± 0.093 | 0.763 ± 0.088 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.495 ± 0.000 | 0.447 ± 0.000 | 0.445 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.693 ± 0.000 | 0.605 ± 0.000 | 0.609 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.917 ± 0.000 | 0.914 ± 0.000 | 0.913 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.617 ± 0.000 | 0.607 ± 0.000 | 0.585 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.805 ± 0.000 | 0.782 ± 0.000 | 0.789 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.846 ± 0.073 | 0.827 ± 0.098 | 0.802 ± 0.094 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.904 ± 0.070 | 0.843 ± 0.115 | 0.842 ± 0.123 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.979 ± 0.040 | 0.962 ± 0.071 | 0.965 ± 0.067 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.893 ± 0.070 | 0.886 ± 0.075 | 0.859 ± 0.088 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.932 ± 0.059 | 0.910 ± 0.089 | 0.904 ± 0.089 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.3353 | 0.0001 | 0.0004 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.2512 | 0.0001 | 0.0004 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.3951 | 0.0001 | 0.0004 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.3939 | 0.0001 | 0.0004 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.328 | 0.0001 | 0.0004 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.2943 | 0.0001 | 0.0004 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.3786 | 0.0001 | 0.0004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.0982 | 0.0355 | 0.532 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.0523 | 0.4543 | 1.0 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.0432 | 0.0554 | 0.775 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.0429 | 0.2769 | 1.0 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | -0.0194 | 0.8904 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | -0.0117 | 0.6788 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | -0.0575 | 0.0302 | 0.4824 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | -0.0666 | 0.0256 | 0.4603 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | -0.067 | 0.107 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | -0.1292 | 0.0006 | 0.0122 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | 0.0138 | 0.7615 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | 0.0112 | 0.8904 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0576 | 0.0012 | 0.022 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | 0.0091 | 0.804 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | 0.0237 | 0.6788 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | 0.0036 | 0.8469 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | 0.001 | 0.978 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0678 | 0.0256 | 0.4603 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | -0.0011 | 0.7615 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | 0.0135 | 0.3303 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.429 | 0.492 | 0.563 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.477 | 0.534 | 0.591 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.514 | 0.58 | 0.63 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.577 | 0.635 | 0.681 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.628 | 0.676 | 0.728 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.68 | 0.718 | 0.759 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.73 | 0.765 | 0.791 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.481 | 0.567 | 0.503 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.554 | 0.638 | 0.605 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.603 | 0.683 | 0.668 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.638 | 0.703 | 0.712 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.669 | 0.727 | 0.728 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.714 | 0.764 | 0.78 |

## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)
| channel | rmse_var_mean | rmse_var_std | rmse_persistence_mean | rmse_persistence_std | ratio_var_over_persistence_mean | ratio_var_over_persistence_std |
|---|---|---|---|---|---|---|
| eda | 0.0565 | 0.065 | 0.0556 | 0.0619 | 1.033 | 0.0845 |
| hr | 0.0055 | 0.0018 | 0.0331 | 0.012 | 0.17 | 0.0296 |
| temp | 0.0233 | 0.0134 | 0.026 | 0.0136 | 0.8794 | 0.0612 |

RMSE (forecasting) and macro-F1 (classification) are NOT comparable.