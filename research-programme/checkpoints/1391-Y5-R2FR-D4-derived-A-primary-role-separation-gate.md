# 5375 - D4 derived-A primary-role separation gate

## Decision

`D4_DERIVED_A_FIXED_PRIMARY_ENVELOPE_PASSES__CONDITIONAL_NUMERICAL_STABILITY_ONLY`

Checkpoint 5373 remains a valid failed strict all-model gate. Its 1.487155% envelope is dominated by the 0.125430 free-A base disk. Checkpoints 5359 and 5360 independently derive A from all eight endpoint events and sign it source-complete and not fitted.

For the conditional parent-derived-A branch, the fixed-A intercept is a linear estimator. Its exact adversarial input disk is sum |p_j| r_j plus the one correlated A-disk contribution |p^T l| r_A. The free-A branch remains a sensitivity/falsifier branch; its uncertainty is not silently converted into uncertainty of the fixed-A estimator.

## Result

- fixed-A base estimator disk: `0.04662920116836757`;
- fixed-A conservative diagnostic envelope: `0.049371839788407736`;
- relative fixed-A envelope: `0.005708156931496409`;
- unchanged one-percent gate: `0.01`;
- conditional fixed-A stability passes: `True`.

## Disclosure

This role-separation audit was defined after the frozen 5373 strict gate failed. It is not labeled preregistered and does not overwrite that failure. It establishes a narrower conditional result whose premise is the parent derivation of A.

A numeric uniform M_D4 remainder constant is still absent. Therefore the unconditional D4 regulator-zero limit, decay-angle integral, full phase space, UV result, local GR and full MTS theory remain unclaimed.
