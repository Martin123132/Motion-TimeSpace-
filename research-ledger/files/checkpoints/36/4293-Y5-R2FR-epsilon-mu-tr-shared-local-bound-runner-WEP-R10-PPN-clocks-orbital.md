# 4293 Y5 R2FR epsilon_mu_tr shared local bound runner

## Purpose

This checkpoint converts the 4292 shared transition residual into a real local empirical pressure test across WEP, R10, PPN, clocks and orbital rows.

## Outcome

The private AJ seed is:

```text
epsilon_AJ_seed = 0.08394692185032419.
```

Unit projection into WEP, PPN gamma/beta, clock, orbital and one-year Gdot rows fails. R10 has a diagnostic anchor-only pass if one incorrectly treats `alpha_tr(38.6um)=epsilon_mu_tr`, but this is not claim-valid because R10 needs finite-range hair and a reviewed full curve.

## Next

Try to derive `epsilon_mu_tr=0` from parent transition membership. If that fails, derive the projection suppression map:

```text
epsilon_mu_tr -> Y_WEP, Y_gamma, Y_beta, Y_clock, Y_orbit, d/dt, alpha_tr(lambda).
```
