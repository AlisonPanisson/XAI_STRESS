# SHAP summary (shap; task=binary; features=15)

Importance = share of mean|SHAP| for the stress class (row-normalized per subject), mean ± SD over subjects.

## Signal-level share
| protocol | group | mean | std |
|---|---|---|---|
| LOSO | eda | 0.428 | 0.122 |
| LOSO | hr | 0.358 | 0.072 |
| LOSO | temp | 0.214 | 0.124 |
| SUBJECT | eda | 0.572 | 0.244 |
| SUBJECT | hr | 0.208 | 0.172 |
| SUBJECT | temp | 0.219 | 0.148 |

## Top features (LOSO, then subject-specific)
| protocol | feature | mean | std |
|---|---|---|---|
| LOSO | eda_std | 0.159 | 0.046 |
| LOSO | hr_max | 0.141 | 0.027 |
| LOSO | hr_mean | 0.134 | 0.038 |
| LOSO | eda_max | 0.086 | 0.034 |
| LOSO | eda_mean | 0.077 | 0.028 |
| LOSO | temp_slope | 0.068 | 0.022 |
| LOSO | eda_min | 0.056 | 0.028 |
| LOSO | eda_slope | 0.051 | 0.014 |

| protocol | feature | mean | std |
|---|---|---|---|
| SUBJECT | eda_mean | 0.162 | 0.074 |
| SUBJECT | eda_max | 0.15 | 0.065 |
| SUBJECT | eda_min | 0.137 | 0.072 |
| SUBJECT | eda_std | 0.107 | 0.071 |
| SUBJECT | hr_max | 0.068 | 0.058 |
| SUBJECT | hr_mean | 0.061 | 0.053 |
| SUBJECT | hr_min | 0.061 | 0.082 |
| SUBJECT | temp_min | 0.051 | 0.038 |

## Direction consistency (share of subjects where higher feature value -> higher stress SHAP)
| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| LOSO | eda_max | 0.8 | 0.364 |
| LOSO | eda_mean | 0.8 | 0.378 |
| LOSO | eda_min | 0.8 | 0.35 |
| LOSO | eda_slope | 1.0 | 0.79 |
| LOSO | eda_std | 1.0 | 0.666 |
| LOSO | hr_max | 1.0 | 0.879 |
| LOSO | hr_mean | 1.0 | 0.791 |
| LOSO | hr_min | 0.933 | 0.794 |
| LOSO | hr_slope | 0.733 | 0.088 |
| LOSO | hr_std | 1.0 | 0.897 |
| LOSO | temp_max | 0.133 | -0.548 |
| LOSO | temp_mean | 0.2 | -0.546 |
| LOSO | temp_min | 0.067 | -0.578 |
| LOSO | temp_slope | 0.0 | -0.927 |
| LOSO | temp_std | 0.6 | 0.226 |

| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| SUBJECT | eda_max | 1.0 | 0.529 |
| SUBJECT | eda_mean | 1.0 | 0.511 |
| SUBJECT | eda_min | 1.0 | 0.519 |
| SUBJECT | eda_slope | 0.867 | 0.271 |
| SUBJECT | eda_std | 1.0 | 0.651 |
| SUBJECT | hr_max | 1.0 | 0.639 |
| SUBJECT | hr_mean | 1.0 | 0.664 |
| SUBJECT | hr_min | 0.8 | 0.336 |
| SUBJECT | hr_slope | 0.714 | 0.118 |
| SUBJECT | hr_std | 0.933 | 0.604 |
| SUBJECT | temp_max | 0.2 | -0.361 |
| SUBJECT | temp_mean | 0.333 | -0.264 |
| SUBJECT | temp_min | 0.267 | -0.268 |
| SUBJECT | temp_slope | 0.067 | -0.52 |
| SUBJECT | temp_std | 0.533 | 0.154 |

## Consistency statistics
| metric | value | sd |
|---|---|---|
| LOSO: mean pairwise Spearman between subjects | 0.72 | 0.21677863700811034 |
| LOSO: mean Spearman of subject vs group-mean importance | 0.827 | 0.13601387150813102 |
| LOSO: most frequent top-1 feature | eda_std | 7/15 subjects |
| SUBJECT: mean pairwise Spearman between subjects | 0.475 | 0.3034969877669289 |
| SUBJECT: mean Spearman of subject vs group-mean importance | 0.666 | 0.2540983793623206 |
| SUBJECT: most frequent top-1 feature | eda_mean | 6/15 subjects |
| same subject: Spearman LOSO vs subject-specific importance | 0.384 | 0.20543963146596309 |
| same subject: overlap of top-3 features (of 3) | 0.6 | 0.6110100926607787 |
