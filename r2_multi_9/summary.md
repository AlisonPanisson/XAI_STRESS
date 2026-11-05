# Rerun summary

Task: multiclass; window 60 s, step 30 s; blocked folds K=5; SMOTE in-fold: False; tuning: True

## Data per subject (for the personalization-feasibility sentence)
- windows per subject: 93 ± 1 (range 90–96)
- labeled minutes per subject: 50.0 ± 0.7 (range 48.1–51.2)

## Main results (mean ± SD over subjects; per-subject values in CSV)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| LOSO | LR | 0.554 ± 0.152 | 0.498 ± 0.125 | 0.441 ± 0.153 | 15 |
| LOSO | NN | 0.614 ± 0.098 | 0.514 ± 0.094 | 0.467 ± 0.103 | 15 |
| LOSO | RF | 0.522 ± 0.140 | 0.446 ± 0.153 | 0.391 ± 0.159 | 15 |
| LOSO | ROCKET | 0.552 ± 0.119 | 0.474 ± 0.093 | 0.439 ± 0.104 | 15 |
| LOSO | SVM | 0.531 ± 0.106 | 0.481 ± 0.094 | 0.428 ± 0.106 | 15 |
| LOSO | TSF | 0.602 ± 0.181 | 0.521 ± 0.153 | 0.479 ± 0.168 | 15 |
| LOSO | kNN | 0.518 ± 0.115 | 0.441 ± 0.101 | 0.404 ± 0.100 | 15 |
| SUBJECT_BLOCKED | LR | 0.830 ± 0.086 | 0.821 ± 0.093 | 0.804 ± 0.095 | 15 |
| SUBJECT_BLOCKED | NN | 0.849 ± 0.089 | 0.806 ± 0.117 | 0.802 ± 0.121 | 15 |
| SUBJECT_BLOCKED | RF | 0.871 ± 0.066 | 0.849 ± 0.076 | 0.839 ± 0.079 | 15 |
| SUBJECT_BLOCKED | ROCKET | 0.842 ± 0.081 | 0.807 ± 0.099 | 0.802 ± 0.096 | 15 |
| SUBJECT_BLOCKED | SVM | 0.858 ± 0.073 | 0.861 ± 0.080 | 0.836 ± 0.083 | 15 |
| SUBJECT_BLOCKED | TSF | 0.847 ± 0.075 | 0.804 ± 0.087 | 0.800 ± 0.092 | 15 |
| SUBJECT_BLOCKED | kNN | 0.861 ± 0.090 | 0.841 ± 0.105 | 0.834 ± 0.102 | 15 |

## Diagnostic: random window splits (what the original protocol effectively did)
| protocol | model | acc | bal_acc | macro_f1 | n_subjects |
|---|---|---|---|---|---|
| POOLED_RANDOM_SPLIT | LR | 0.590 ± 0.000 | 0.530 ± 0.000 | 0.508 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | NN | 0.690 ± 0.000 | 0.580 ± 0.000 | 0.555 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | RF | 0.938 ± 0.000 | 0.934 ± 0.000 | 0.929 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | SVM | 0.645 ± 0.000 | 0.588 ± 0.000 | 0.590 ± 0.000 | 1 |
| POOLED_RANDOM_SPLIT | kNN | 0.845 ± 0.000 | 0.791 ± 0.000 | 0.806 ± 0.000 | 1 |
| SUBJECT_RANDOM_SPLIT | LR | 0.862 ± 0.084 | 0.847 ± 0.105 | 0.823 ± 0.109 | 15 |
| SUBJECT_RANDOM_SPLIT | NN | 0.906 ± 0.072 | 0.838 ± 0.122 | 0.826 ± 0.139 | 15 |
| SUBJECT_RANDOM_SPLIT | RF | 0.986 ± 0.026 | 0.985 ± 0.034 | 0.983 ± 0.033 | 15 |
| SUBJECT_RANDOM_SPLIT | SVM | 0.892 ± 0.079 | 0.899 ± 0.072 | 0.869 ± 0.088 | 15 |
| SUBJECT_RANDOM_SPLIT | kNN | 0.957 ± 0.065 | 0.944 ± 0.089 | 0.946 ± 0.087 | 15 |

## Paired Wilcoxon tests on macro-F1 (Holm-adjusted within family)
| family | comparison | n | mean_diff | p | p_holm |
|---|---|---|---|---|---|
| personalization | LR: subject-specific vs LOSO | 15 | 0.3628 | 0.0001 | 0.0004 |
| personalization | NN: subject-specific vs LOSO | 15 | 0.3343 | 0.0001 | 0.0004 |
| personalization | RF: subject-specific vs LOSO | 15 | 0.4475 | 0.0001 | 0.0004 |
| personalization | ROCKET: subject-specific vs LOSO | 15 | 0.3628 | 0.0001 | 0.0004 |
| personalization | SVM: subject-specific vs LOSO | 15 | 0.4078 | 0.0001 | 0.0004 |
| personalization | TSF: subject-specific vs LOSO | 15 | 0.3206 | 0.0001 | 0.0004 |
| personalization | kNN: subject-specific vs LOSO | 15 | 0.4294 | 0.0001 | 0.0004 |
| ts_vs_static[LOSO] | TSF vs kNN | 15 | 0.075 | 0.1876 | 1.0 |
| ts_vs_static[LOSO] | TSF vs LR | 15 | 0.0379 | 0.5245 | 1.0 |
| ts_vs_static[LOSO] | TSF vs RF | 15 | 0.0878 | 0.0043 | 0.0854 |
| ts_vs_static[LOSO] | TSF vs SVM | 15 | 0.0508 | 0.4212 | 1.0 |
| ts_vs_static[LOSO] | TSF vs NN | 15 | 0.0119 | 0.8469 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs kNN | 15 | 0.0347 | 0.3028 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs LR | 15 | -0.0024 | 0.6788 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs RF | 15 | 0.0476 | 0.0554 | 0.9965 |
| ts_vs_static[LOSO] | ROCKET vs SVM | 15 | 0.0105 | 0.7197 | 1.0 |
| ts_vs_static[LOSO] | ROCKET vs NN | 15 | -0.0284 | 0.4212 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs kNN | 15 | -0.0338 | 0.1876 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs LR | 15 | -0.0043 | 0.7197 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs RF | 15 | -0.0391 | 0.073 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs SVM | 15 | -0.0363 | 0.1205 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | TSF vs NN | 15 | -0.0018 | 0.7615 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs kNN | 15 | -0.0318 | 0.0736 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs LR | 15 | -0.0024 | 0.975 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs RF | 15 | -0.0371 | 0.0946 | 1.0 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs SVM | 15 | -0.0344 | 0.048 | 0.9118 |
| ts_vs_static[SUBJECT_BLOCKED] | ROCKET vs NN | 15 | 0.0001 | 0.7776 | 1.0 |

## Calibration / cold-start curve (RF; mean over subjects)
| mode | q | n_calib | calib_minutes | macro_f1 | bal_acc | acc |
|---|---|---|---|---|---|---|
| pooled | 0.0 | 0.0 | 0.0 | 0.367 | 0.423 | 0.512 |
| pooled+calib | 0.1 | 12.467 | 8.733 | 0.439 | 0.469 | 0.543 |
| pooled+calib | 0.2 | 21.467 | 13.233 | 0.457 | 0.501 | 0.574 |
| pooled+calib | 0.3 | 30.467 | 17.733 | 0.53 | 0.575 | 0.637 |
| pooled+calib | 0.4 | 39.333 | 22.167 | 0.593 | 0.636 | 0.696 |
| pooled+calib | 0.5 | 47.6 | 26.3 | 0.63 | 0.669 | 0.728 |
| pooled+calib | 0.6 | 58.4 | 31.7 | 0.698 | 0.729 | 0.79 |
| subject_only | 0.1 | 12.467 | 8.733 | 0.473 | 0.558 | 0.502 |
| subject_only | 0.2 | 21.467 | 13.233 | 0.564 | 0.63 | 0.614 |
| subject_only | 0.3 | 30.467 | 17.733 | 0.581 | 0.652 | 0.653 |
| subject_only | 0.4 | 39.333 | 22.167 | 0.606 | 0.661 | 0.689 |
| subject_only | 0.5 | 47.6 | 26.3 | 0.685 | 0.732 | 0.756 |
| subject_only | 0.6 | 58.4 | 31.7 | 0.756 | 0.792 | 0.823 |
