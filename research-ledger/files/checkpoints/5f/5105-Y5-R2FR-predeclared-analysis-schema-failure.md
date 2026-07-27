# 5105 — predeclared analysis schema failure

The first one-shot execution of the unchanged 5080 analyzer stopped before writing any aggregate output. The pilot config has never contained the `target_precision_budgets` field read at analysis line 304; this is true of both the historical v6 config and completed v12 config.

The failure produced no statistical result. It does not authorize changing an estimator or threshold.

Checkpoint 5106 may repair only this schema binding by reproducing the five target-margin rows already derived in checkpoint 5040 from the 5018 source. A retry is authorized only if those rows match the historical 5040 config exactly and a new execution wrapper is hash-locked before aggregate output exists.
