# 3968 - Quadratic Source Closure B Equals A2 Or Finite Beta Vector

Timestamp: `2026-07-01T15:41:00+00:00`

## Result

3968 takes the direct derivation route.

The square law is conditionally proven from a single exterior mass parameter:

```text
g_00 = -1 + 2 mu/(r c^2) - 2 mu^2/(r^2 c^4) + O(c^-6)
mu = A_source mu_0
W = mu_0/r

therefore

g_00 = -1 + 2 A_source W/c^2 - 2 A_source^2 W^2/c^4 + O(c^-6)
B_source = A_source^2
beta_eff = B_source/A_source^2 = 1
```

That is the clean route. It does **not** yet prove MTS local GR, because MTS still has to derive the premises:

- EH-dominant observed exterior metric;
- one parent-owned exterior monopole;
- source/worldtube/Gauss charge equality;
- same metric/coframe readout through second order;
- no hidden `q_loc`, boundary/domain/projector, R11, or coupling `U^2` stress.

## Finite Fallback

If those premises do not close:

```text
Delta_B_square := B_source - A_source^2
delta_beta_source = Delta_B_square/A_source^2
|delta_beta_source| <= (sum_i |Delta_B_i|)/|A_source|^2
```

So the beta problem is no longer vague. It is either the single-mass exterior theorem, or a finite obstruction vector.

## Source Intake

Source needles found: `17/17`.

## Decision

Next target: prove single-exterior-mass uniqueness for the compact local branch, or fill finite obstruction rows.
