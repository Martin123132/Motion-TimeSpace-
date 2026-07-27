# 4206 - Y5 R2FR Calibrated GN Bridge Or Source-Charge Caveat

Decision: `CALIBRATED_GN_BRIDGE_IMPORTED_INTO_4205_STRUCTURAL_NEWTON_COUPLING_CLOSED_NUMERIC_G_NOT_PREDICTED_HTAU_PARENT_CHARGE_CAVEAT_ACTIVE_NONCLAIM`

4206 imports the existing calibrated source-coupling law into the 4205 gate.

The local coupling bridge is:

```text
G_cal := c^4 kappa_eff/(8*pi),
kappa_eff = kappa_* Z_0,
D_A ln kappa_eff = 0.
```

This means MTS can reduce to the GR/Newton coupling structure with one calibrated `G_N`, just like GR, without pretending to predict the numerical value of `G`.

The caveat is still sharp:

```text
M_H^dress = H_tau[S_link] - H_ref
```

must be parent-owned, not imported from orbital `GM` or left as notation.
