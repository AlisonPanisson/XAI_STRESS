# SHAP summary (shap; task=multiclass; features=15)

Importance = share of mean|SHAP| for the stress class (row-normalized per subject), mean ± SD over subjects.

## Signal-level share
| protocol | group | mean | std |
|---|---|---|---|
| LOSO | eda | 0.506 | 0.064 |
| LOSO | hr | 0.191 | 0.051 |
| LOSO | temp | 0.303 | 0.055 |
| SUBJECT | eda | 0.586 | 0.199 |
| SUBJECT | hr | 0.14 | 0.112 |
| SUBJECT | temp | 0.274 | 0.146 |

## Top features (LOSO, then subject-specific)
| protocol | feature | mean | std |
|---|---|---|---|
| LOSO | eda_std | 0.201 | 0.042 |
| LOSO | eda_slope | 0.103 | 0.025 |
| LOSO | temp_slope | 0.09 | 0.026 |
| LOSO | eda_max | 0.08 | 0.024 |
| LOSO | hr_max | 0.079 | 0.022 |
| LOSO | eda_mean | 0.073 | 0.022 |
| LOSO | temp_mean | 0.07 | 0.021 |
| LOSO | temp_max | 0.066 | 0.022 |

| protocol | feature | mean | std |
|---|---|---|---|
| SUBJECT | eda_mean | 0.167 | 0.062 |
| SUBJECT | eda_max | 0.155 | 0.051 |
| SUBJECT | eda_min | 0.14 | 0.064 |
| SUBJECT | eda_std | 0.11 | 0.06 |
| SUBJECT | temp_min | 0.074 | 0.054 |
| SUBJECT | temp_mean | 0.073 | 0.046 |
| SUBJECT | temp_max | 0.067 | 0.044 |
| SUBJECT | hr_max | 0.05 | 0.046 |

## Direction consistency (share of subjects where higher feature value -> higher stress SHAP)
| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| LOSO | eda_max | 0.8 | 0.4 |
| LOSO | eda_mean | 0.867 | 0.483 |
| LOSO | eda_min | 0.733 | 0.414 |
| LOSO | eda_slope | 1.0 | 0.848 |
| LOSO | eda_std | 1.0 | 0.699 |
| LOSO | hr_max | 0.0 | -0.76 |
| LOSO | hr_mean | 0.067 | -0.581 |
| LOSO | hr_min | 0.2 | -0.379 |
| LOSO | hr_slope | 0.067 | -0.237 |
| LOSO | hr_std | 0.0 | -0.905 |
| LOSO | temp_max | 0.267 | -0.318 |
| LOSO | temp_mean | 0.2 | -0.311 |
| LOSO | temp_min | 0.2 | -0.336 |
| LOSO | temp_slope | 0.0 | -0.836 |
| LOSO | temp_std | 0.867 | 0.514 |

| protocol | feature | pos_share | mean_rho |
|---|---|---|---|
| SUBJECT | eda_max | 1.0 | 0.712 |
| SUBJECT | eda_mean | 1.0 | 0.674 |
| SUBJECT | eda_min | 1.0 | 0.664 |
| SUBJECT | eda_slope | 0.867 | 0.356 |
| SUBJECT | eda_std | 1.0 | 0.757 |
| SUBJECT | hr_max | 0.067 | -0.62 |
| SUBJECT | hr_mean | 0.067 | -0.606 |
| SUBJECT | hr_min | 0.133 | -0.554 |
| SUBJECT | hr_slope | 0.533 | -0.057 |
| SUBJECT | hr_std | 0.133 | -0.456 |
| SUBJECT | temp_max | 0.4 | -0.211 |
| SUBJECT | temp_mean | 0.467 | -0.148 |
| SUBJECT | temp_min | 0.467 | -0.18 |
| SUBJECT | temp_slope | 0.067 | -0.515 |
| SUBJECT | temp_std | 0.733 | 0.274 |

## Consistency statistics
| metric | value | sd |
|---|---|---|
| LOSO: mean pairwise Spearman between subjects | 0.793 | 0.11725250069585601 |
| LOSO: mean Spearman of subject vs group-mean importance | 0.885 | 0.07016339853749293 |
| LOSO: most frequent top-1 feature | eda_std | 15/15 subjects |
| SUBJECT: mean pairwise Spearman between subjects | 0.595 | 0.2519313752496129 |
| SUBJECT: mean Spearman of subject vs group-mean importance | 0.778 | 0.20146768729735123 |
| SUBJECT: most frequent top-1 feature | eda_mean | 4/15 subjects |
| same subject: Spearman LOSO vs subject-specific importance | 0.393 | 0.18076494051342162 |
| same subject: overlap of top-3 features (of 3) | 0.533 | 0.8055363982396383 |
