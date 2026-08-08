# 3173 — Parent Exterior Operator Match Or PiJ2metric Source Row Under AX1090

Private checkpoint. This is an extraction theorem, not a local-GR claim, PPN pass, solar J2 pass, or public-facing result.

## What Moved

3172 derived the public exterior `r^-3` quadrupole Green profile, but left the actual coupling open:

```text
Upsilon_J2 = Pi_J2_metric * T_source * G_ext_l2_surface.
```

3173 attacks the real coupling problem directly. The result is:

```text
Pi_J2_metric/Upsilon_J2 has an exact parent-action extractor formula.
```

But the current corpus does not yet contain the parent Hessian/readout objects needed to evaluate it.

## Exact Operator Extractor

Let:

```text
Phi_A
```

be the parent field vector, and:

```text
sigma_K2 := K_2 C_K2_unit
```

be the first-order `l=2` source/residual lane.

Expand the parent Euler-Lagrange equations around a local exterior background `Phi0`:

```text
0 = E_A[Phi0 + delta Phi; sigma_K2]
  = L_AB delta Phi_B + S_A sigma_K2 + O(delta Phi^2, sigma_K2^2).
```

where:

```text
L_AB = delta E_A / delta Phi_B
```

is the linearized parent operator/Hessian, and:

```text
S_A = partial E_A / partial sigma_K2
```

is the K2 source vector.

On the physical quotient, after gauge fixing/constraint reduction:

```text
delta Phi_B = - (L_parent^-1)_BA S_A sigma_K2.
```

Let:

```text
E_metric
```

map parent perturbations into the public metric perturbation, and:

```text
P_surf,l2
```

extract the solar-surface public `l=2` metric amplitude.

Then:

```text
A_surface = P_surf,l2 E_metric[delta Phi].
```

So the non-fitted transfer kernel is:

```text
Upsilon_J2 = - P_surf,l2 E_metric L_parent^-1 S_K2.
```

This is the important part: `Pi_J2_metric` is not a mood, not a fit, and not a guessed constant. It is a functional-derivative object.

## Operator-Match Gate

The 3172 `r^-3` theorem applies if:

```text
P_ext,l2 E_metric L_parent^-1 S_K2
```

obeys the source-free public exterior `l=2` metric equation:

```text
r^2 f_2'' + 2 r f_2' - 6 f_2 = 0.
```

Then asymptotic flatness gives:

```text
f_2(r) proportional to r^-3.
```

But this still requires the parent operator match. It cannot be imported from GR.

## Current Corpus Audit

| Required object | Current state | Verdict |
| --- | --- | --- |
| `S_parent[Phi; sigma]` | contracts/toy lanes exist | missing full parent action |
| `L_parent` | reciprocal scalar toy operator exists only for `R_AB` | missing public metric-sector Hessian |
| `S_K2` | `K_2 := |W_2 M_Lambda|` exists as restricted lane | missing source variation |
| `E_metric` | 3159 gives public convention once `A_metric` exists | missing parent-to-public readout |
| `P_surf,l2` | 3172 gives radial/profile rule once `A_surface` exists | conditional only |
| no-GR-import proof | 04/09/10 forbid smuggling | not yet satisfied |

So the extractor formula is derived, but not instantiated.

## No Shortcut From `R_AB = 0`

The reciprocal-route result:

```text
R_AB = ln(T^2 S) = 0
```

is still important for local `gamma=1` routing.

But it does not imply:

```text
P_surf,l2 E_metric L_parent^-1 S_K2 = 1.
```

Reason:

```text
R_AB
```

is the reciprocal trace/radial-routing lane, while solar J2 is a tracefree `l=2` public metric amplitude. They can be related by a parent action, but not by assertion.

Therefore:

```text
R_AB = 0
```

cannot be used as a shortcut to set:

```text
Pi_J2_metric = 1.
```

## Source-Ready Nonclaim Rows

3173 stages source-ready rows for:

```text
Pi_J2_metric;
T_source;
operator_match_l2.
```

All remain:

```text
valid_for_claim = false.
```

The rows are useful because they say exactly what must be sourced:

```text
L_parent;
S_K2;
E_metric;
gauge quotient;
source-domain normalization;
solar-surface projector.
```

## Decision

The J2/local-GR route is not closed, but it is no longer vague.

Before any solar J2, PPN, Shapiro, clock, orbital, or local-GR claim, the next step must either extract:

```text
L_parent, S_K2, E_metric
```

from an explicit parent action, or admit that the parent action gap is the hard block.

Next target:

```text
3174-Y5-R2FR-parent-Hessian-and-metric-readout-extraction-or-action-gap-lock-under-AX1090.
```

## Generated Artifacts

```text
source-intake/mts_residuals/P8_Y5_R2FR_3173_INPUTS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3173_OPERATOR_MATCH_DERIVATION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3173_CURRENT_ARTIFACT_AUDIT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3173_PIJ2_EXTRACTOR_CONTRACT.csv
source-intake/mts_residuals/P8_Y5_R2FR_3173_SOURCE_READY_NONCLAIM_ROWS.csv
source-intake/mts_residuals/P8_Y5_R2FR_3173_DECISION.csv
source-intake/mts_residuals/P8_Y5_R2FR_3173_VALIDATION.csv
```
