# 4287 - cGamma AJ real profile or parent coefficient derivation

Marker: `PPC4161_CGAMMA_AJ_REAL_PROFILE_OR_PARENT_COEFFICIENT_DERIVATION_4287`

Decision: `PARENT_ZERO_NOT_DERIVED_AJ_REDUCED_TO_EXPLICIT_STRONG_WINDOW_PROFILE_LAW_NONCLAIM`

4287 tries the parent-zero route and keeps it unsigned. The advance is the finite calculator-ready gate:

```text
A_J,eff_private <= 0.167893843691 * Pi_B * (T_res/tau_L) / abs(c_Gamma)
```

or:

```text
T_res/tau_L >= A_J,eff_private * abs(c_Gamma) / (0.167893843691 * Pi_B).
```

The next target is a real sourced row for `R_transport_to_local`, `R_Bgrad_to_local`, `T_res/tau_L`, `c_Gamma`, `Pi_B`, or `A_J,eff_private`, or a parent theorem that sets the residual pair exactly to zero.
