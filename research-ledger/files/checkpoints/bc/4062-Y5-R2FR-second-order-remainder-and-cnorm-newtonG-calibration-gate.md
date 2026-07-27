# 4062 - Second-Order Remainder and c_norm/Newton-G Calibration Gate

- Timestamp: `2026-07-02T01:28:05+00:00`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## Result

4062 separates two things that must not be mixed:

1. a constant universal calibration of Newton's constant;
2. forbidden derivative hair hidden inside measured `GM`.

The selected branch law is:

```text
G_N := c^4 kappa_eff/(8*pi),    kappa_eff = kappa_* Z_0
Delta_cnorm = |D ln G_obs| + |D ln M_eff| + |D ln(1+epsilon_mu)|.
```

A constant `G_N` is allowed as calibration. GR itself does not derive the numerical value of `G`; it uses one empirically calibrated universal coupling. The MTS requirement is therefore not "predict G's number today"; it is:

```text
D_t G_N = D_r G_N = D_lambda G_N = D_species G_N = D_frame G_N = 0
```

inside the compact local branch, unless a bound row is supplied.

## Second-Order Guard

After 4060 normal-ordering:

```text
Gamma_ren(Y_* + deltaY) = 1/2 H_AB deltaY^A deltaY^B + O(deltaY^3).
```

If the local fixed-point/reset branch gives exact `deltaY=0`, then `Q_quad=0`. If not, the branch keeps:

```text
Q_quad <= C_Ploc C_2 |deltaY| |nabla deltaY| / L_*^2.
```

## What Moved

The Newton/GR route is now cleaner:

- one universal constant coupling may be calibrated;
- nonconstant `Gdot`, radial/range dependence, WEP/species dependence, frame drift, and extra monopoles are not calibration and must be zero or bounded;
- the next job is an explicit EH weak-field readout showing Poisson/Newton and PPN use the same Hilbert source and calibrated `G_N`.
