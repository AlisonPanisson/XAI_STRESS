# SHAP summary (shap; task=multiclass; features=15)

Importance = share of mean|SHAP| for the stress class (row-normalized per subject), mean ± SD over subjects.

## Signal-level share
| protocol | group | mean | std |
|---|---|---|---|
| LOSO | eda | 0.379 | 0.077 |
| LOSO | hr | 0.39 | 0.087 |
| LOSO | temp | 0.23 | 0.068 |
| SUBJECT | eda | 0.542 | 0.191 |
| SUBJECT | hr | 0.202 | 0.122 |
| SUBJECT | temp | 0.255 | 0.148 |

## Top features (LOSO, then subject-specific)
| protocol | feature | mean | std |
|---|---|---|---|
| LOSO | hr_max | 0.153 | 0.03 |
| LOSO | hr_mean | 0.145 | 0.051 |
| LOSO | eda_std | 0.14 | 0.033 |
| LOSO | eda_max | 0.064 | 0.025 |
| LOSO | eda_mean | 0.063 | 0.021 |
| LOSO | eda_slope | 0.063 | 0.018 |
| LOSO | temp_slope | 0.063 | 0.018 |
| LOSO | hr_std | 0.056 | 0.015 |

| protocol | feature | mean | std |
|---|---|---|---|
| SUBJECT | eda_mean | 0.157 | 0.059 |
| SUBJECT | eda_max | 0.145 | 0.052 |
| SUBJECT | eda_min | 0.128 | 0.064 |
| SUBJECT | eda_std | 0.098 | 0.059 |
| SUBJECT | temp_min | 0.069 | 0.044 |
| SUBJECT | hr_max | 0.066 | 0.05 |
| SUBJECT | hr_mean | 0.065 | 0.042 |
| SUBJECT | temp_mean | 0.064 | 0.036 |

## Direction consistency (share of subjects where higher feature value -> higher stress SHAP)
| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| LOSO | eda_max | 0.8 | 0.421 |
| LOSO | eda_mean | 0.8 | 0.443 |
| LOSO | eda_min | 0.8 | 0.438 |
| LOSO | eda_slope | 1.0 | 0.758 |
| LOSO | eda_std | 1.0 | 0.643 |
| LOSO | hr_max | 1.0 | 0.907 |
| LOSO | hr_mean | 1.0 | 0.745 |
| LOSO | hr_min | 1.0 | 0.817 |
| LOSO | hr_slope | 0.6 | 0.103 |
| LOSO | hr_std | 1.0 | 0.904 |
| LOSO | temp_max | 0.133 | -0.459 |
| LOSO | temp_mean | 0.133 | -0.442 |
| LOSO | temp_min | 0.133 | -0.477 |
| LOSO | temp_slope | 0.0 | -0.933 |
| LOSO | temp_std | 0.933 | 0.548 |

| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| SUBJECT | eda_max | 1.0 | 0.695 |
| SUBJECT | eda_mean | 1.0 | 0.676 |
| SUBJECT | eda_min | 1.0 | 0.685 |
| SUBJECT | eda_slope | 0.733 | 0.284 |
| SUBJECT | eda_std | 1.0 | 0.743 |
| SUBJECT | hr_max | 1.0 | 0.732 |
| SUBJECT | hr_mean | 1.0 | 0.726 |
| SUBJECT | hr_min | 0.8 | 0.353 |
| SUBJECT | hr_slope | 0.733 | 0.131 |
| SUBJECT | hr_std | 0.933 | 0.645 |
| SUBJECT | temp_max | 0.333 | -0.24 |
| SUBJECT | temp_mean | 0.467 | -0.167 |
| SUBJECT | temp_min | 0.4 | -0.2 |
| SUBJECT | temp_slope | 0.067 | -0.526 |
| SUBJECT | temp_std | 0.8 | 0.294 |

## Consistency statistics
| metric | value | sd |
|---|---|---|
| LOSO: mean pairwise Spearman between subjects | 0.746 | 0.12329904292720512 |
| LOSO: mean Spearman of subject vs group-mean importance | 0.833 | 0.08778129388175793 |
| LOSO: most frequent top-1 feature | hr_max | 8/15 subjects |
| SUBJECT: mean pairwise Spearman between subjects | 0.546 | 0.28925519641304726 |
| SUBJECT: mean Spearman of subject vs group-mean importance | 0.728 | 0.2430293507091735 |
| SUBJECT: most frequent top-1 feature | eda_mean | 5/15 subjects |
| same subject: Spearman LOSO vs subject-specific importance | 0.295 | 0.17943979340096863 |
| same subject: overlap of top-3 features (of 3) | 0.4 | 0.6110100926607788 |
