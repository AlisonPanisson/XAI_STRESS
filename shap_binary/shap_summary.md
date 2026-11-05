# SHAP summary (shap; task=binary; features=15)

Importance = share of mean|SHAP| for the stress class (row-normalized per subject), mean ± SD over subjects.

## Signal-level share
| protocol | group | mean | std |
|---|---|---|---|
| LOSO | eda | 0.517 | 0.138 |
| LOSO | hr | 0.226 | 0.082 |
| LOSO | temp | 0.257 | 0.117 |
| SUBJECT | eda | 0.6 | 0.234 |
| SUBJECT | hr | 0.148 | 0.134 |
| SUBJECT | temp | 0.252 | 0.155 |

## Top features (LOSO, then subject-specific)
| protocol | feature | mean | std |
|---|---|---|---|
| LOSO | eda_std | 0.208 | 0.058 |
| LOSO | eda_max | 0.092 | 0.04 |
| LOSO | hr_max | 0.09 | 0.033 |
| LOSO | eda_mean | 0.085 | 0.035 |
| LOSO | temp_slope | 0.076 | 0.027 |
| LOSO | eda_slope | 0.071 | 0.022 |
| LOSO | hr_mean | 0.065 | 0.032 |
| LOSO | eda_min | 0.06 | 0.027 |

| protocol | feature | mean | std |
|---|---|---|---|
| SUBJECT | eda_mean | 0.169 | 0.073 |
| SUBJECT | eda_max | 0.156 | 0.06 |
| SUBJECT | eda_min | 0.145 | 0.071 |
| SUBJECT | eda_std | 0.113 | 0.067 |
| SUBJECT | temp_min | 0.062 | 0.052 |
| SUBJECT | temp_mean | 0.062 | 0.049 |
| SUBJECT | temp_max | 0.056 | 0.049 |
| SUBJECT | hr_max | 0.054 | 0.049 |

## Direction consistency (share of subjects where higher feature value -> higher stress SHAP)
| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| LOSO | eda_max | 0.733 | 0.406 |
| LOSO | eda_mean | 0.8 | 0.405 |
| LOSO | eda_min | 0.867 | 0.402 |
| LOSO | eda_slope | 1.0 | 0.87 |
| LOSO | eda_std | 1.0 | 0.706 |
| LOSO | hr_max | 0.0 | -0.779 |
| LOSO | hr_mean | 0.0 | -0.701 |
| LOSO | hr_min | 0.2 | -0.377 |
| LOSO | hr_slope | 0.0 | -0.344 |
| LOSO | hr_std | 0.0 | -0.919 |
| LOSO | temp_max | 0.133 | -0.36 |
| LOSO | temp_mean | 0.133 | -0.385 |
| LOSO | temp_min | 0.2 | -0.369 |
| LOSO | temp_slope | 0.0 | -0.884 |
| LOSO | temp_std | 0.733 | 0.363 |

| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| SUBJECT | eda_max | 1.0 | 0.522 |
| SUBJECT | eda_mean | 1.0 | 0.47 |
| SUBJECT | eda_min | 1.0 | 0.482 |
| SUBJECT | eda_slope | 0.867 | 0.23 |
| SUBJECT | eda_std | 1.0 | 0.68 |
| SUBJECT | hr_max | 0.0 | -0.727 |
| SUBJECT | hr_mean | 0.0 | -0.701 |
| SUBJECT | hr_min | 0.067 | -0.63 |
| SUBJECT | hr_slope | 0.467 | -0.055 |
| SUBJECT | hr_std | 0.2 | -0.41 |
| SUBJECT | temp_max | 0.333 | -0.292 |
| SUBJECT | temp_mean | 0.333 | -0.233 |
| SUBJECT | temp_min | 0.333 | -0.209 |
| SUBJECT | temp_slope | 0.067 | -0.544 |
| SUBJECT | temp_std | 0.733 | 0.208 |

## Consistency statistics
| metric | value | sd |
|---|---|---|
| LOSO: mean pairwise Spearman between subjects | 0.615 | 0.23214233136418488 |
| LOSO: mean Spearman of subject vs group-mean importance | 0.787 | 0.17113996870657908 |
| LOSO: most frequent top-1 feature | eda_std | 12/15 subjects |
| SUBJECT: mean pairwise Spearman between subjects | 0.536 | 0.2947250275620352 |
| SUBJECT: mean Spearman of subject vs group-mean importance | 0.735 | 0.2532424649061567 |
| SUBJECT: most frequent top-1 feature | eda_mean | 7/15 subjects |
| same subject: Spearman LOSO vs subject-specific importance | 0.465 | 0.30131194614367496 |
| same subject: overlap of top-3 features (of 3) | 1.067 | 1.1234866364235145 |
