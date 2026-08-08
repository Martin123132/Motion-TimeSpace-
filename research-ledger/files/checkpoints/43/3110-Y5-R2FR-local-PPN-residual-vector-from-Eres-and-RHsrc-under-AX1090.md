# 3110 - Y5 R2FR local PPN residual vector from Eres and RHsrc under AX1090

**Purpose:** continue from `3109` into the real local-GR gate. Newtonian `GM` closure is necessary but not sufficient. This checkpoint derives the PPN residual-vector map sourced by `E_res_munu`, `R_Hsrc`, time/frame mismatch, and extra charge channels.

**Verdict:** the PPN problem is now a projection problem, not a vague "local GR missing" problem. If the public EH branch is exact and `R_Hsrc=0`, all PPN components reduce to the GR values. If full MTS carries any residual charge/tensor/frame channel, that channel must appear in a named PPN component. Gamma-only or Newton-only success is explicitly insufficient.

## Source Register

| source_id | path | role |
|---|---|---|
| SRC3110_0 | `3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md` | field equation `G_munu + E_res_munu = kappa_* T_total_munu` |
| SRC3110_1 | `3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md` | non-circular Newton/Gauss/orbital bridge |
| SRC3110_2 | `3109-Y5-R2FR-Hilbert-worldtube-source-mass-lock-or-DeltaGM-residual-row-under-AX1090.md` | dressed source mass and `R_Hsrc` decomposition |
| SRC3110_3 | `3015-Y5-R2FR-PPN-kernel-from-local-closure-residual-envelope-under-AX1090.md` | previous PPN kernel contract and comparator-only rows |
| SRC3110_4 | `2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md` | full-vector/no-gamma-only guard |
| SRC3110_5 | `1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md` | earlier full PPN residual-vector discipline |
| SRC3110_6 | `541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md` | PPN followthrough after source-measure closure |
| SRC3110_7 | `510-worldtube-source-measure-glue-or-Meff-residual-runner.md` | warning that source closure alone does not imply PPN closure |
| SRC3110_8 | `source-intake/mts_residuals/P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv` | `R_Hsrc`/`Delta_GM_total` residual rows feeding this gate |

## Starting Equation

Use the public local equation from `3104`:

```text
G_munu[g_pub] + E_res_munu = kappa_* T_total_munu
```

with the cosmological term dropped on local solar-system scales, and with the `3109` source-mass relation:

```text
GM_orbit = G_* M_pub[W;tau_pub] + Delta_GM_total.
```

Define the dimensionless source-normalization residual

```text
epsilon_H := R_Hsrc / M_pub,
epsilon_GM := Delta_GM_total / (G_* M_pub).
```

Only a universal, constant, source-blind common factor in `epsilon_GM` may be absorbed into calibrated `G_*`. Anything source-dependent, radial, time-dependent, frame-dependent, composition-dependent, or tensorial must remain in the PPN residual vector.

## PPN Metric Readout

In a fixed public PPN gauge, write the local metric schematically as:

```text
g_00 = -1 + 2 U/c^2 - 2 beta U^2/c^4 + h_00^extra,
g_ij = delta_ij (1 + 2 gamma U/c^2) + h_ij^extra,
g_0i = g_0i^GR[V_i,W_i] + h_0i^extra.
```

Here `U` is the post-calibration Newtonian potential sourced by the dressed public mass:

```text
nabla^2 U = -4 pi G_* rho_pub
```

up to the already named Newton/source residuals. The PPN residual vector is:

```text
Delta_PPN :=
{
gamma - 1,
beta - 1,
alpha1,
alpha2,
alpha3,
zeta1,
zeta2,
zeta3,
zeta4,
xi
}.
```

GR corresponds to `Delta_PPN=0` in this convention.

## Projection Derivation

Expand the residual field equation by post-Newtonian order:

```text
E_res_00 = E00^(2) c^2 + E00^(4) + O(c^-2),
E_res_ij = Eij^(2) + Eij^(4)c^-2 + ...,
E_res_0i = E0i^(3)c + O(c^-1).
```

The Newtonian residual is:

```text
Xi_N := P_N[E00^(2)] + 4 pi G_* rho_pub epsilon_H + Xi_extra_source.
```

This feeds:

```text
nabla^2 U_obs = -4 pi G_* rho_pub - Xi_N.
```

For PPN scoring, the calibrated monopole part of `Xi_N` can be absorbed only if it is common and constant. The non-common remainder is:

```text
Xi_N^shape := Xi_N - <Xi_N>_common_monopole.
```

and it must be retained.

The first-order spatial curvature residual is:

```text
delta_gamma :=
gamma - 1
= P_gamma[ Eij^(2) - delta_ij Ekk^(2)/3, E00^(2), Xi_N^shape, R_time_frame ].
```

Interpretation: `gamma` is not controlled by Newtonian `GM` alone. It measures whether the spatial curvature potential and clock/Newtonian potential are sourced in the same way.

The second-order time-time residual is:

```text
delta_beta :=
beta - 1
= P_beta[ E00^(4), nonlinear(E00^(2),Eij^(2)), R_Hsrc, Xi_N^shape, R_boundary, R_extra_source ].
```

Interpretation: `beta` is where a theory can look Newtonian and still fail local GR. It tests nonlinear superposition, source dressing, and second-order conservation.

The preferred-frame/location vector block is:

```text
{alpha1, alpha2, alpha3, xi}
= P_vector[ E0i^(3), anisotropic(Eij^(2)), R_time_frame, R_projector, R_domain, R_boundary ].
```

Interpretation: any hidden time-flow, disformal/current direction, projector direction, boundary-selected frame, or source/readout frame mismatch lands here unless parent-zeroed.

The nonconservation block is:

```text
{zeta1,zeta2,zeta3,zeta4}
= P_zeta[ nabla_mu E_res^mu_nu, nabla_mu T_extra^mu_nu, d/dtau R_Hsrc, source-exchange currents ].
```

By Bianchi:

```text
nabla_mu G^mu_nu = 0
```

so the field equation requires:

```text
nabla_mu E_res^mu_nu = kappa_* nabla_mu T_total^mu_nu.
```

If ordinary quotient matter is conserved but `E_res` has a nonzero divergence, then some hidden exchange or source residual is still active. That cannot be hidden inside calibrated `G`; it is a PPN conservation residual.

## Derived PPN Residual Map

The local full-vector map is:

```text
gamma - 1
= K_gamma^E[Eij^(2)-E00^(2)]
+ K_gamma^N[Xi_N^shape]
+ K_gamma^H[epsilon_H]
+ K_gamma^frame[R_time_frame].

beta - 1
= K_beta^E[E00^(4)]
+ K_beta^NL[(E^(2))^2]
+ K_beta^H[epsilon_H]
+ K_beta^B[R_boundary]
+ K_beta^extra[R_extra_source].

alpha_i
= K_alpha_i^0[E0i^(3)]
+ K_alpha_i^frame[R_time_frame]
+ K_alpha_i^proj[R_projector]
+ K_alpha_i^extra[R_extra_vector].

zeta_i
= K_zeta_i^div[nabla.E_res - kappa_* nabla.T_total]
+ K_zeta_i^src[d_tau R_Hsrc]
+ K_zeta_i^exchange[J_extra].

xi
= K_xi^domain[R_domain + R_boundary + anisotropic(Eij^(2))].
```

The `K` objects are not free fit parameters. They are the PPN Green/projection operators fixed by the public metric gauge and the source/readout convention. Current MTS does not yet provide numeric source-backed values for these kernels, so all rows remain nonclaim.

## The No-Cancellation Rule

A full PPN pass requires either:

```text
Delta_PPN = 0 by parent theorem,
```

or every component is source-backed and below its corresponding empirical bound.

Forbidden:

```text
gamma passes,
therefore local GR passes.
```

Forbidden:

```text
alpha_i cancels beta/gamma by tuning.
```

Forbidden:

```text
epsilon_GM is absorbed into measured G when it is source-, time-, radius-, or frame-dependent.
```

Allowed:

```text
one universal constant monopole normalization may calibrate G_* after the source-mass bridge.
```

Everything else stays in the absolute residual vector:

```text
|Delta_PPN|_abs :=
(
|gamma-1|,
|beta-1|,
|alpha1|,
|alpha2|,
|alpha3|,
|zeta1|,
|zeta2|,
|zeta3|,
|zeta4|,
|xi|
).
```

## What This Gives Us

If the following are all parent-signed:

```text
E_res_munu = 0 through PPN order,
R_Hsrc = 0,
R_time_frame = 0,
R_boundary = 0,
R_projector = 0,
R_extra_source = 0,
```

then:

```text
Delta_PPN = 0,
```

and the branch reduces to GR at local PPN order.

If any term survives, the theory is not dead, but the surviving term is no longer vague. It lands in the `3110` residual vector and must be either theorem-zeroed or numerically bounded.

## Residual Rows

The machine-readable interface is staged at:

```text
source-intake/mts_residuals/P8_Y5_R2FR_3110_LOCAL_PPN_RESIDUAL_VECTOR.csv
```

Every row is nonclaim. The value column contains a theorem target or `MISSING_COMPONENT_INPUTS`, never a fabricated prediction.

## Gate Table

| gate_id | target | status | reason |
|---|---|---|---|
| GATE3110_0 | Newtonian source normalization | improved conditional | `3108/3109` give the bridge, but `Delta_GM_total` remains nonzero until proven/bounded |
| GATE3110_1 | gamma channel | mapped nonclaim | needs spatial-curvature projection of `Eij^(2)` and source/readout shape residuals |
| GATE3110_2 | beta channel | mapped nonclaim | needs second-order `E00^(4)` and nonlinear/source-dressing closure |
| GATE3110_3 | preferred-frame channels | mapped nonclaim | any hidden time/frame/projector direction feeds `alpha_i`/`xi` |
| GATE3110_4 | conservation channels | mapped nonclaim | divergence of `E_res` or source exchange feeds `zeta_i`/`alpha3` |
| GATE3110_5 | local-GR PPN pass | not claimable | no parent theorem or source-backed numeric vector yet |

## Claim Status

No local-GR, PPN, Cassini, perihelion, preferred-frame, clock, orbital, WEP, R10, or derived-`G` claim follows from this checkpoint.

But the project now has a clean next battlefield:

```text
local GR reduction = source-mass bridge + PPN residual vector closure.
```

That is the right standard. It is stricter than a galaxy/rotation fit, and it is also fairer than demanding a derived numerical `G` before allowing the GR limit.

## Next Best Step

Write:

```text
3111-Y5-R2FR-Eres-zero-through-PPN-order-or-component-bound-priority-under-AX1090.md
```

Direct target:

```text
Try to zero the largest class first:
E_res_munu through PPN order.

If E_res cannot be theorem-zeroed, split it into
E00^(2), Eij^(2), E0i^(3), E00^(4), div(E_res)
and choose the first component that can be bounded from existing local data.
```

That is better than testing randomly: it attacks the operator residual before hunting small empirical numbers.
