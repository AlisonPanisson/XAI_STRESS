# Rerun summary

Task: multiclass; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.519 ± 0.105 | 0.492 ± 0.089 | 0.437 ± 0.112 | 15 |
| LOSO | NN | 0.586 ± 0.103 | 0.508 ± 0.089 | 0.467 ± 0.098 | 15 |
| LOSO | RF | 0.559 ± 0.117 | 0.485 ± 0.122 | 0.442 ± 0.126 | 15 |
| LOSO | ROCKET | 0.552 ± 0.119 | 0.474 ± 0.093 | 0.439 ± 0.104 | 15 |
| LOSO | SVM | 0.527 ± 0.102 | 0.493 ± 0.080 | 0.434 ± 0.099 | 15 |
| LOSO | TSF | 0.602 ± 0.181 | 0.521 ± 0.153 | 0.479 ± 0.168 | 15 |
| LOSO | kNN | 0.542 ± 0.101 | 0.463 ± 0.091 | 0.434 ± 0.092 | 15 |
| SUBJECT_BLOCKED | LR | 0.831 ± 0.097 | 0.810 ± 0.103 | 0.799 ± 0.105 | 15 |
| SUBJECT_BLOCKED | NN | 0.859 ± 0.071 | 0.811 ± 0.095 | 0.812 ± 0.093 | 15 |
| SUBJECT_BLOCKED | RF | 0.870 ± 0.067 | 0.845 ± 0.071 | 0.837 ± 0.074 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.842 ± 0.081 | 0.807 ± 0.099 | 0.802 ± 0.096 | 15 |
| SUBJECT_BLOCKED | SVM | 0.846 ± 0.089 | 0.838 ± 0.101 | 0.821 ± 0.101 | 15 |
| SUBJECT_BLOCKED | TSF | 0.847 ± 0.075 | 0.804 ± 0.087 | 0.800 ± 0.092 | 15 |
| SUBJECT_BLOCKED | kNN | 0.872 ± 0.086 | 0.836 ± 0.099 | 0.831 ± 0.099 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.590 ± 0.000 | 0.542 ± 0.000 | 0.527 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.717 ± 0.000 | 0.608 ± 0.000 | 0.576 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.910 ± 0.000 | 0.872 ± 0.000 | 0.882 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.657 ± 0.000 | 0.624 ± 0.000 | 0.621 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.793 ± 0.000 | 0.720 ± 0.000 | 0.728 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.890 ± 0.086 | 0.872 ± 0.114 | 0.853 ± 0.125 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.934 ± 0.077 | 0.892 ± 0.122 | 0.884 ± 0.135 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.986 ± 0.030 | 0.981 ± 0.048 | 0.978 ± 0.052 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.913 ± 0.089 | 0.907 ± 0.091 | 0.895 ± 0.099 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.944 ± 0.056 | 0.926 ± 0.074 | 0.922 ± 0.071 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.3625 | 0.0001 | 0.0004 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.3447 | 0.0001 | 0.0004 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.3947 | 0.0001 | 0.0004 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.3628 | 0.0001 | 0.0004 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.3874 | 0.0001 | 0.0004 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.3206 | 0.0001 | 0.0004 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.3968 | 0.0001 | 0.0004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.0449 | 0.4887 | 1.0 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.0426 | 0.5245 | 1.0 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.0369 | 0.1205 | 1.0 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.0453 | 0.4543 | 1.0 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.0118 | 0.804 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | 0.0046 | 0.9341 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | 0.0023 | 0.6788 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | -0.0034 | 0.8469 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | 0.005 | 0.5995 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | -0.0284 | 0.1688 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.0313 | 0.3591 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | 0.0007 | 0.978 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0372 | 0.0256 | 0.5115 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | -0.0214 | 0.4887 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | -0.0122 | 0.5245 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0294 | 0.1578 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | 0.0026 | 0.925 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0353 | 0.1205 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | -0.0195 | 0.3627 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | -0.0103 | 0.7197 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.42 | 0.466 | 0.544 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.484 | 0.526 | 0.599 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.511 | 0.548 | 0.634 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.582 | 0.621 | 0.712 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.658 | 0.689 | 0.764 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.662 | 0.691 | 0.768 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.729 | 0.748 | 0.807 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.472 | 0.549 | 0.51 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.529 | 0.593 | 0.585 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.615 | 0.669 | 0.675 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.632 | 0.693 | 0.72 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.692 | 0.757 | 0.776 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.767 | 0.808 | 0.831 |

## VAR 1-step forecasting vs persistence (z-scored; ratio < 1 means VAR beats persistence)
| channel | rmse_var_mean | rmse_var_std | rmse_persistence_mean | rmse_persistence_std | ratio_var_over_persistence_mean | ratio_var_over_persistence_std |
|---|---|---|---|---|---|---|
| eda | 0.0518 | 0.0494 | 0.0507 | 0.0467 | 1.0383 | 0.09 |
| hr | 0.0685 | 0.0149 | 0.1587 | 0.0363 | 0.4357 | 0.0389 |
| temp | 0.0233 | 0.0134 | 0.0261 | 0.0136 | 0.8783 | 0.0612 |

RMSE (forecasting) and macro-F1 (classification) are NOT comparable.