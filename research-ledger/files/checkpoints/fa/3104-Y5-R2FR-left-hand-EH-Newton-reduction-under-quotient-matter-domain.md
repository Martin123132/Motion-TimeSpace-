# 3104 - Y5 R2FR left-hand EH/Newton reduction under quotient matter domain

**Purpose:** continue `3103` without circling. `3102` and `3103` closed the dangerous right-hand coupling route by putting ordinary matter on the public quotient only. This checkpoint asks whether the left-hand geometry can now be made to reduce to Einstein-Hilbert plus controlled residuals, and therefore to the Newton/Poisson limit.

**Status:** this is a constructive local-GR branch, not a public claim. The branch becomes real if the parent action adopts the public geometry action rule below. If the rule is rejected, the leftover terms are no longer vague missing pieces: they are the geometric residual vector that must be zero-proved or bounded.

## Inputs Used

| input_id | source | role |
|---|---|---|
| IN3104_0 | `3102-Y5-R2FR-verify-Xhat-verticality-and-matter-descent-under-AX1090.md` | quotient-descended ordinary matter forces `c_g=0` if adopted |
| IN3104_1 | `3103-Y5-R2FR-Xhat-matter-domain-conflict-resolution-under-AX1090.md` | forbids hidden matter/source multipliers and gives one Hilbert source |
| IN3104_2 | `1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md` | old EH/Newton gate: metric-only, second-order, LC, no-extra-sector, GM transfer |
| IN3104_3 | `1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md` | old R11 residual interface for `R2/fR` and torsion/nonmetricity |
| IN3104_4 | `1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md` | EH block exists only as an anchor unless adopted into parent action |
| IN3104_5 | `1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md` and `1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md` | Hamiltonian/charge normalization remains guarded |

## Public Geometry Action Rule

The branch extension is:

```text
Q_obs := P_parent / ~
q : P_parent -> Q_obs
g_pub = g[q(Phi)]
connection_pub = LC(g_pub)
ordinary matter = S_matter[Psi_A, g_pub, theta_A(q(Phi), representation_A)]
```

and the local exterior/public geometry action is required to have the principal form

```text
S_pub =
  (1 / (2 kappa_*)) int_M sqrt(-g_pub) (R[g_pub] - 2 Lambda_*)
  + S_top[g_pub, q(Phi)]
  + S_silent[q(Phi)]
  + S_res[g_pub, q(Phi), residual fields].
```

This is not “import GR and hope”. It is a parent-action choice: the observable quotient geometry is the only local spin-2 carrier in the compact local branch, and the lowest-derivative diffeomorphism-invariant 4D metric action is the Einstein-Hilbert action up to a cosmological term and topological/boundary pieces. In other words, Lovelock is used as a selection theorem only after the public geometry rule is adopted.

The rule forbids treating `R2/fR`, torsion, nonmetricity, projector stress, memory stress, boundary flux, or hidden scalar exchange as invisible. If any of them survive, they live in `S_res` and must appear in the residual tensor below.

## First Variation

Define the Hilbert matter stress from the single quotient matter action:

```text
T_total_munu := -(2 / sqrt(-g_pub)) delta S_matter / delta g_pub^munu.
```

`3103` gives the source-side simplification:

```text
delta_X S_matter = 0
c_g = b_conf = b_dis = b_alpha = b_mA = b_clock_i = b_marker = Delta_w_A = delta_kappa_A = 0
```

inside the quotient-matter branch. Therefore `T_total_munu` is not allowed to carry hidden `Xhat`-dependent species weights, source-only multipliers, or clock/material markers.

Varying `S_pub + S_matter` with respect to `g_pub` gives

```text
G_munu[g_pub] + Lambda_* g_munu + E_res_munu = kappa_* T_total_munu
```

where

```text
E_res_munu := -(2 kappa_* / sqrt(-g_pub)) delta(S_top + S_silent + S_res) / delta g_pub^munu
```

with the convention that truly topological or silent terms have zero local variation. This is the central reduction statement. The right-hand side is now ordinary Hilbert matter; all remaining deviations from GR sit on the left as `E_res_munu`.

## Bianchi/Ward Condition

The Einstein tensor obeys

```text
nabla^mu G_munu = 0.
```

If `S_pub + S_matter` is diffeomorphism invariant and all retained sectors are varied, the field equation implies

```text
nabla^mu T_total_munu = (1 / kappa_*) nabla^mu E_res_munu.
```

So local GR conservation is recovered if

```text
E_res_munu = 0,
```

or more generally if `E_res_munu` is separately conserved and observationally bounded. This is the clean version of the old Bianchi problem: after `3103`, the matter/source side no longer hides the failure. Any conservation debt is a left-hand residual debt.

## Newton/Poisson Limit

Take the local weak-field, slow-motion, quasi-static branch:

```text
g_00 = -(1 + 2 Phi / c^2)
g_ij = (1 - 2 Psi / c^2) delta_ij
T_00 ~= rho c^2
|Phi|/c^2 << 1
```

For the EH principal operator with negligible local `Lambda_*` and silent residuals, the leading equation reduces to

```text
nabla^2 Phi = 4 pi G_* rho
G_* := kappa_* c^4 / (8 pi).
```

With retained non-EH sectors the honest equation is

```text
nabla^2 Phi =
  4 pi G_* rho
  + R_Eres[Phi, Psi, residual fields]
  + R_Lambda
  + R_boundary.
```

Thus Newton follows from this branch if and only if:

```text
R_Eres, R_Lambda, R_boundary are zero or below the relevant local/orbital/PPN bounds,
and the Hamiltonian/worldtube charge fixes G_* M to the measured orbital GM.
```

The important improvement is that the source `rho` is no longer contaminated by direct `Xhat` composition weights. The remaining problem is the left-hand operator and the mass/charge calibration, not arbitrary matter coupling.

## What This Actually Proves

| result_id | statement | status | reason |
|---|---|---|---|
| RES3104_0 | quotient matter gives one ordinary Hilbert source | proved inside `3102`/`3103` branch | all direct `Xhat` matter/source multipliers are forbidden or residualized |
| RES3104_1 | EH principal operator gives GR-form left-hand equation | conditional but mathematically clean | follows from adopting the public geometry action rule |
| RES3104_2 | Newton/Poisson follows from EH plus same source | conditional but clean | weak-field EH limit gives Poisson with `G_* = kappa_* c^4/(8 pi)` |
| RES3104_3 | full local GR/PPN pass | not claimed | residual tensor, boundary/charge normalization, and PPN vector still need closure |
| RES3104_4 | old R11/R2FR work is not wasted | retained as residual fallback | if public geometry action rule is incomplete, the old residual vector is exactly where deviations go |

## Remaining Left-Hand Residual Vector

| residual_id | object | closes if | otherwise |
|---|---|---|---|
| LHR3104_0_R2FR | `R2/fR` or curvature-square scalar mode | no bare higher-curvature term and no hidden `X R` vertex are parent-signed | keep finite scalar/R10/PPN residual |
| LHR3104_1_connection | torsion/nonmetricity/independent connection | `connection_pub = LC(g_pub)` is parent-signed | keep WEP/clock/lightcone/spin/PPN connection residual |
| LHR3104_2_extra_stress | motion/time/domain/projector/memory stress | terms are topological, gauge, positive source-free silent, or zero by field equation | keep `E_res_munu` and source bounds |
| LHR3104_3_boundary | boundary/reference flux and counterterm | local variation and Hamiltonian flux vanish or are fixed before readout | keep boundary charge residual |
| LHR3104_4_GM_transfer | `G_* M_H = GM_orbital` | parent Noether/worldtube/Gauss calibration is signed | Newton-looking equation cannot yet be identified with measured orbital gravity |
| LHR3104_5_PPN_vector | `gamma-1`, `beta-1`, preferred-frame/location terms | residual tensor and connection residuals vanish/bound in local solution | keep explicit PPN residual vector |

## Claim Status

No public local-GR, Newton, PPN, R10, WEP, clock, or orbital pass is claimed here.

Private status is better than the old gate language:

```text
Right-hand/source problem: mostly closed inside the quotient-matter branch.
Left-hand/EH problem: reducible to one public geometry action rule plus residual tensor.
Newton problem: algebraically reachable once E_res and GM transfer are closed.
```

That is a genuine ladder rung: the local branch is no longer “find the missing coupling”. It is now “adopt or derive the public EH principal operator, then kill or bound the explicit residual tensor.”

## Next Best Step

Write:

```text
3105-Y5-R2FR-public-EH-principal-operator-adoption-or-geometric-residual-vector-under-AX1090.md
```

Task: test the public geometry action rule against the existing MTS object language. If no core axiom demands a live non-EH left-hand term, promote the rule as the preferred local-GR branch. If one does, place that term explicitly into `E_res_munu` with its weak-field, PPN, R10, clock, and orbital projections.
