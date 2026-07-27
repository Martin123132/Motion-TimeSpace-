# 3107 - Y5 R2FR Newton constant calibration vs parent scale derivation under AX1090

**Purpose:** formalize the `G` point cleanly. GR does not derive the numerical value of Newton's constant; it uses a universal coupling calibrated by experiment. MTS should not be punished for doing the same at the first local-GR/Newton reduction stage, but it also must not pretend a calibrated constant is a derived one.

**Verdict:** reducing MTS to GR/Newton requires `G0` and `G1`: the correct field-equation form plus a non-circular calibration to the measured Newtonian coupling after source-charge transfer. Deriving `G` from MTS primitives is `G2`, a stronger future target. Current MTS does not yet derive `G2`, and that is not fatal for the local-GR pass.

## Source Register

| source_id | source | relevant point |
|---|---|---|
| SRC3107_0 | `3106-Y5-R2FR-constitutive-Hodge-star-derivation-or-EM-medium-residual-under-AX1090.md` | introduced the `G0/G1/G2` split |
| SRC3107_1 | `3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md` | EH principal operator gives Poisson form if residuals close |
| SRC3107_2 | `1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md` | forbids using orbital `GM` as an early denominator |
| SRC3107_3 | `1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md` | constant universal coupling/source normalization remains not parent-derived |
| SRC3107_4 | `1148-Y5-R10-cR11-source-normalization-owner-or-zero-theorem.md` | source-normalization operator aliases the measured-GM bottleneck |
| SRC3107_5 | `1149-Y5-R10-source-normalization-owner-minimal-lemma-or-channel-bound-fallback.md` | minimal source-owner lemma separates Hilbert charge, PiM flux, and Gauss/orbital calibration |
| SRC3107_6 | `1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md` | worldtube/Hilbert glue and no-orbital-GM guard remain active |
| SRC3107_7 | `1230-Y5-R10-universal-action-scale-measure-owner-theorem-or-finite-delta-w-prior.md` | universal action-scale/measure-owner theorem is conditional, not parent-signed |

## Three Different Jobs

| level | name | question | required status |
|---|---|---|---|
| G0 | field-equation form | Does MTS reduce to an Einstein/Poisson-type equation with one public metric and one Hilbert source? | required for local GR/Newton |
| G1 | empirical calibration | Does the coupling in that equation match measured Newtonian gravity without circularly using orbital `GM` as proof? | required for local GR/Newton |
| G2 | parent-scale derivation | Does MTS derive the numerical value/scale of `G` from deeper primitives? | optional stronger win, not required for first GR reduction |

This distinction matters. If MTS reaches `G0+G1`, it is doing what GR itself does operationally. If MTS reaches `G2`, it has gone beyond standard GR.

## G0: Field-Equation Form

Start from the public geometry action branch:

```text
S_pub = (1 / (2 kappa_*)) int sqrt(-g_pub) (R[g_pub] - 2 Lambda_*) + S_res
```

with quotient-owned matter:

```text
S_matter = S_matter[Psi_A, g_pub, theta_A(q(Phi), representation_A)].
```

Variation gives

```text
G_munu[g_pub] + Lambda_* g_munu + E_res_munu = kappa_* T_total_munu.
```

So `G0` passes if:

```text
E_res_munu = 0 or bounded below relevant PPN/R10/clock/orbital limits,
T_total_munu is the single quotient Hilbert source,
and no hidden matter/source multipliers survive.
```

This is the "MTS reduces to the GR field-equation shape" target. It does not require deriving the numerical value of `kappa_*`.

## G1: Newton/Measured-G Calibration

In the weak static slow-motion branch,

```text
g_00 = -(1 + 2 Phi/c^2)
T_00 ~= rho c^2
```

the EH principal operator gives the Poisson form

```text
nabla^2 Phi = (kappa_* c^4 / 2) rho + residuals.
```

Newtonian gravity is

```text
nabla^2 Phi = 4 pi G_meas rho.
```

Therefore the calibrated coupling is

```text
kappa_* = 8 pi G_meas / c^4.
```

This is not cheating after `G0` and source-charge transfer are derived. It is the standard GR calibration. The cheating would be using observed orbital `GM` to define the source charge before proving that the field equation/source charge produces the orbital readout.

## Anti-Circularity Rule

Forbidden early move:

```text
M_source := GM_orbit / G_ref
```

before deriving

```text
M_source[W] = H_tau[S] - H_ref
or
M_source[W] = (4 pi G_ref)^-1 int_S Pi_M J_H
```

and before proving the Gauss/orbital bridge:

```text
nabla^2 Phi = 4 pi G_* rho_H
=> r^2 |a_r| = G_* M_H.
```

Allowed later move:

```text
Once the source charge and Gauss/orbital bridge are derived,
set G_* = G_meas by calibration.
```

This keeps the ladder intact: derive the roof access first, then measure the ruler.

## G2: Parent Derivation of G

Deriving `G` would require a parent normalization law, not just the GR limit. Examples of the kind of structure required:

```text
1 / (2 kappa_*) = C_parent * N_cell / L_cell^2
```

or

```text
kappa_*^{-1} = action_scale * cell_density * public_measure_factor
```

or

```text
kappa_*^{-1} = hbar_parent * c / L_parent^2
```

with every symbol parent-owned before readout:

```text
action scale,
cell/domain measure,
length/time units,
hbar/c status,
public coframe,
source-current normalization,
and no hidden calibration offset.
```

The current corpus has pieces pointing in this direction, especially the universal action-scale/measure-owner work, but it has not parent-signed the full scale theorem. So:

```text
G2 = not derived current corpus.
```

That is a useful truth, not a disaster.

## Calibration Versus Derivation Ledger

| item | calibrated route | derived route | current status |
|---|---|---|---|
| `kappa_*` | universal constant fitted to `G_meas` after `G0` and source bridge | parent action scale fixes `kappa_*` before readout | calibration allowed later; derivation not current |
| `M_source` | inferred from field/source theorem then compared to orbital dynamics | parent Hamiltonian/Hilbert/worldtube charge | theorem route not closed |
| `GM_orbit` | readout predicted after Gauss bridge | not a primitive source denominator | cannot be used early |
| universal source coupling | same `kappa_*` for all quotient matter | action-scale/measure owner theorem | conditional only |
| drift/species/range dependence | forbidden or bounded residuals | parent superselection/no-hair theorem | still open |

## What Would Count As Local GR/Newton Reduction

MTS gets a serious local GR/Newton reduction if:

1. `G0_form`: public metric EH principal operator or equivalent second-order spin-2 operator is derived/adopted and residuals are zero/bounded.
2. `single_source`: quotient matter gives one Hilbert `T_total_munu` including EM stress without hidden weights.
3. `source_charge`: compact source charge is a parent Hilbert/Hamiltonian/worldtube object before orbital readout.
4. `Gauss_bridge`: the same source charge controls the `1/r` potential and orbital acceleration.
5. `G1_calibration`: the universal coupling is calibrated to measured `G` after the above bridge.
6. `PPN_stability`: `gamma`, `beta`, preferred-frame/location, clock, and orbital residuals are zero/bounded.

None of those require `G2`. `G2` is a separate "can MTS explain the size of gravity?" project.

## Current State

| gate_id | gate | status | why |
|---|---|---|---|
| GATE3107_0_G0 | field-equation form | conditional | `3104` gives the clean branch, but EH/residual closure remains not fully parent-signed |
| GATE3107_1_single_source | quotient Hilbert source | improved | `3102/3103` strongly clean the right-hand source, but full source charge remains downstream |
| GATE3107_2_G1 | calibrated Newton coupling | not yet claimable | source charge/Gauss bridge still open; calibration is allowed only after bridge |
| GATE3107_3_G2 | parent derivation of `G` | not derived | action-scale/cell-measure theorem not parent-signed |
| GATE3107_4_no_overdemand | do not require derived `G` for GR reduction | pass as policy | GR itself calibrates `G`; MTS may do same for first reduction |
| GATE3107_5_no_smuggling | do not borrow orbital `GM` early | pass as policy | guard inherited from 1006/1150 |

## Decision

The Newton-constant question should not derail the local-GR route.

Correct policy:

```text
First: derive local field equation + source charge + Gauss/orbital bridge.
Then: calibrate kappa_* to measured G, exactly as GR does.
Later: try to derive kappa_* from MTS parent action scale/cell measure.
```

Incorrect policy:

```text
Demand G2 before allowing any GR reduction.
Use orbital GM to define the source mass before proving source charge.
Claim calibrated G is derived G.
```

## Claim Status

No local-GR pass, Newton pass, measured-GM pass, source-normalization pass, PPN pass, or derived-`G` claim is made here.

This checkpoint is still real progress because it removes a false binary:

```text
MTS does not need to derive G to reduce to GR/Newton.
MTS does need to avoid circular GM calibration before the source bridge.
MTS may later attempt a parent-scale derivation of G as a stronger result.
```

## Next Best Step

Write:

```text
3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md
```

Task: attack the `G1` bridge directly. Derive or bound the chain

```text
T_total_munu
-> parent source charge M_H[W]
-> Gauss/Poisson surface charge
-> exterior 1/r potential
-> orbital GM readout
```

without using orbital `GM` as an input. If this fails, retain an explicit `GM_calibration_residual` and source-normalization residual vector.
