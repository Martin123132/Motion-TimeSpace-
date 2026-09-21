# Full source-force spatial budget (corrected provenance totals)

This version preserves the derivation and numerical results of the earlier report and corrects the final check/failure accounting; no scientific result or tolerance changes.

Private continuation of `DERIVATION-20260919-coarse-time64-isolation.md`.

## Result in plain language

We now have a derived and numerically checked response functional for the **full reduced source force**, not just its explicit Gram contribution. It includes the scalar velocity, projection inertia, dust drive and the moving-geometry/source terms. The unchanged action reproduces the recorded forces on both reference and MTS, at coarse32, coarse64 and the fixed fine resolution.

The MTS spatial discrepancy is dominated by the free wave-drive difference. A signed, force-weighted reconstruction points chiefly to the mismatch between the two frozen spatial evolution operators, rather than to the already-small coarse time-step change. However, the independent spatial dual-pairing precision check remains failed. The transport calculation is therefore a **diagnostic decomposition, not a qualified error certificate**. The failed check is not relabeled as passing.

No new evolution, changed coupling, clipped mode, changed source boundary, public upload or full-GR claim is made.

## 1. Full Schur difference, with its actual denominator

Use the original action's source Schur reduction. Let J be the free wave drive, G the dust drive, I_d>0 the dust inertia, Q>=0 the residual field-projection inertia, and q=Q/I_d. For either discrete level,

```text
F = (J-q G)/(1+q).
Delta F = [Delta J-q_f Delta G-Delta q (G_c+F_c)]/(1+q_f).     (1)
```

Here Delta means fine-minus-coarse, or later-time-resolution-minus-earlier-time-resolution on the same spatial grid. Multiplying by1+q_f and substituting(1+q_c)F_c=J_c-q_cG_c proves(1). The independently recorded force need not equal its floating Schur evaluation exactly; its signed closure residual is retained separately.

For the **coarse64 versus fixed fine** endpoint comparison:

| Signed force contribution | Reference | MTS |
|---|---:|---:|
| Wave-drive difference / denominator | +1.72705352e-10 | -1.97088634e-8 |
| Dust-drive-change term | -2.49412e-22 | -3.24883e-20 |
| Projection-inertia-change term | -1.81109190e-10 | -1.81105719e-10 |
| Recorded closure residual | +1.53035e-16 | +1.12815e-15 |
| Actual recorded difference | -8.40368584e-12 | -1.98899680e-8 |

Approximately99.09% of the signed MTS difference is in the wave-drive term. This is a decomposition of this finite diagnostic, not a universal causal attribution to a physical coupling. The reference exhibits substantial cancellation between its wave-drive and inertia terms; dropping inertia would destroy that comparison. The dust-drive *change* is negligible here, not the dust drive or gravity in general.

## 2. Derive the full field response from the existing action

At a fixed terminal geometry/time-derivative and source position/velocity, write u for scalar nodal values, v for scalar nodal velocities, V for source velocity, S for finite-element sampling, D for the source-motion derivative map, W for the positive kinetic quadrature weights and K for the complete gradient-plus-Gram stiffness. These are the original action objects, not a fitted replacement. Define

```text
t = S v + V D u,             d = dot(D) u + D v,
M = S^T W S,                 b = S^T W D u,
ell = V D^T W t - K u - S^T[dot(W)t + V W d].                (2)
```

The partial derivative subscript R holds the prescribed geometry function fixed while varying source position through the original map. The dotted coefficients include the actual geometry time derivative and source-map transport. Holding rates fixed during the momentum transport gives

```text
F_raw = (1/2)t^T W_R t + V t^T W D_R u - (1/2)u^T K_R u,
T_R = d^T W t + (D u)^T dot(W)t + V(D u)^T W d,
J(u,v) = F_raw - T_R - b^T M^-1 ell,
Q(u) = [D u-S M^-1 b]^T W [D u-S M^-1 b].                    (3)
```

The positive residual form for Q avoids subtracting two nearly equal kinetic inertias. The gradient implementation differentiates the entire projection, including its residual term. At this fixed background/source jet, J and q are homogeneous quadratic functions of the scalar phase variables z=(u,v). The rational force itself is not quadratic.

For two phase vectors z_c,z_f in this *same* discrete functional, with midpoint z_bar, quadratic polarization gives an exact finite secant:

```text
c = [grad J(z_bar)-(G+F(z_c)) grad q(z_bar)]/[1+q(z_f)],
F(z_f)-F(z_c) = c^T(z_f-z_c).                                (4)
```

This is not a first-order Taylor approximation. It retains scalar position AND velocity dependence and the field-dependent source-inertia denominator. The helper implements matrix-free derivatives of(2)-(3); synthetic dense-matrix calculations independently reconstruct J, test directional derivatives and test(4), with nonzero inertia and dust channels.

Actual-action checks compare against the existing independent Schur implementation. At both spatial levels and both branches, the new functional and directional gradients pass their predeclared numerical checks. The geometry tangent still comes from the existing finite-difference live canonical construction: this is not an exact or interval-certified geometry derivative.

## 3. Keep geometry and the nonnested transfer explicit

Let theta include the prescribed metric and its time derivative, source position and velocity. Let I be the original, nonnested nodal interpolation applied to both u and v. The exact ordered telescope is

```text
F_f(z_f;theta_f)-F_c(z_c;theta_c)
 = [F_f(z_f;theta_f)-F_f(Iz_c;theta_f)]        field/state
 + [F_f(Iz_c;theta_f)-F_f(Iz_c;theta_c)]      geometry/source jet
 + [F_f(Iz_c;theta_c)-F_c(z_c;theta_c)]       operator/transfer. (5)
```

The last term includes the declared nonnested interpolation; it is not mislabeled as a pure continuum truncation error. Counterfactual fixed-background evaluations are comparison functionals, not newly evolved physical solutions. The actual geometries still come from the full saved state of all material layers.

At coarse64 versus fixed fine:

| Signed force term | Reference | MTS |
|---|---:|---:|
| Scalar-position part of field secant | +5.93509611e-10 | -2.96587070e-8 |
| Scalar-velocity part | -3.29143796e-11 | -4.12312852e-11 |
| Geometry/source-jet change | -1.09520e-17 | -1.26048e-17 |
| Operator plus nonnested transfer | -5.68999050e-10 | +9.80996924e-9 |
| Recorded closure residual | +1.53035e-16 | +1.12815e-15 |

All terms and signs remain. Reconstruction errors are below7.29e-17 across all six spatial/temporal comparisons, versus tolerances approximately3.68e-16. In particular, the reference's velocity term is not negligible relative to its small final gap. The full-force functional is a genuinely broader observable than the prior explicit-Gram gradient.

## 4. Force-weighted two-level Duhamel identity

For the unchanged frozen action on level L, use

```text
A_L = M_L,star^-1 K_L,star,
Y_L = (u_L,v_L),       L_L = [[0,1],[-A_L,0]],
r_L = a_L+A_L u_L,
Y_L(T) = E_L(T)Y_L(0) + R_L + d_L,
R_L = integral_0^T E_L(T-s)(0,r_L(s)) ds.                    (6)
```

E_L is the homogeneous propagator. For exact trajectories and exact integration, d_L=0. In this computation r is sampled from the saved canonical acceleration, interpolated piecewise-linearly, and propagated by the original banded-mass/factored-stiffness exponential. Therefore d_L is the **measured path/forcing-sampling defect**, not assumed zero and not an independently bounded unknown error.

Contracting the fine-minus-transferred-coarse state with the full-force secant c yields

```text
c^T[Y_f(T)-IY_c(T)]
 = c^T E_f(T)[Y_f(0)-IY_c(0)]                       initial representation
 + c^T[E_f(T)I-I E_c(T)]Y_c(0)                     frozen operator commutator
 + c^T[R_f-I R_c]                                 moving/source forcing
 + c^T[d_f-I d_c].                                measured path defect (7)
```

Equation(7) follows directly from(6), with no assumed operator commutation and no exact-nesting assumption. The forcing retains all moving/source terms through the canonical acceleration; it has not yet been split into individually certified time-dependent channels. Add the endpoint geometry/operator/closure terms from(5) to obtain the full recorded force gap.

The affine-forcing exponential is independently tested against small dense matrix exponentials, including zero frequency, adjoint matrix action and actual halfsteps. All scalar modes are retained. This is a constant linear computational split with live remainders, not a frozen-background replacement theory or full nonlinear Jacobian adjoint.

### Measured33-node budget

The following transport numbers remain **precision-limited diagnostics only**, subject to section5:

| Signed coarse64/fine force contribution | Reference | MTS |
|---|---:|---:|
| Initial representation | -6.40004673e-10 | -1.99105066e-9 |
| Frozen evolution-operator commutator | +1.26154784e-9 | -2.99978176e-8 |
| Moving/source forcing response | -6.05098412e-11 | +2.33983619e-9 |
| Measured path/sampling defect | -4.38096817e-13 | -5.09062580e-11 |
| Endpoint operator/transfer correction | -5.68999050e-10 | +9.80996924e-9 |

The much smaller endpoint geometry/closure terms remain in the machine-readable table. For MTS, the frozen evolution-operator commutator dominates this particular signed path, partially canceled by the endpoint operator/transfer term. This is stronger evidence about where the numerical discrepancy enters than a global energy norm, but it does not prove divergence, identify a unique physical cause, or show how the terms behave on a third spatial level.

The same method is applied to the actual coarse32-to64 temporal comparison. Initial representation and the frozen operator commutator then vanish because the spatial grid and initial data are identical. MTS's moving-forcing contribution is1.56765e-13; its measured path/sampling contribution is2.20572e-11, reproducing the observed2.22138e-11 force change after closure terms. Reference gives-4.35963e-15 and1.69048e-12 respectively. This warns against dropping d_L: the temporal force change is mostly in that recorded defect on both branches.

All9/17/33 forcing-node results are retained. A small final reconstruction residual is only an algebraic telescope, since the measured defect is included; it cannot by itself certify the forcing integral or the true continuum error.

## 5. Precision failure retained, not converted into a pass

The first transport attempt stops at its independent forward/backward initial-pairing control. For reference the discrepancy is1.60e-15, exceeding the predeclared3.002e-16 tolerance. The failed attempt remains immutable.

A separate diagnostic finds severe cancellation: sums of absolute products are about0.208(reference) and12.05(MTS), while the desired signed pairings are about6.2e-10 and-3.2e-8. The usual finite-dot-product roundoff majorants are1.50e-13 and8.72e-12. MTS forward/backward differences reach2.35e-12. These dot-product bounds do **not** certify the preceding matrix exponentials. Repeated propagation can differ at this scale, and NumPy longdouble has only53 mantissa bits on this Windows runtime, so casting did not provide extra precision.

The second attempt completes the requested diagnostic budget but keeps the original tolerance and stores `original_strict_dual_gate_pass=false`; all four spatial dual comparisons still fail it. The two same-grid temporal initial pairings cancel exactly. No tolerance is enlarged to turn the old failed gate into a pass. The diagnostic's successful completion means its outputs exist and its scoped algebra checks pass, **not** that the independent spatial transport qualification succeeded.

Therefore the endpoint full-force/secant result is supported by its independent tests, whereas the spatial transport budget is provisional. Its leading terms are far larger than the observed dual discrepancy, but its smallest terms and any certified transport bound remain unresolved. Fixing cancellation must precede promotion to a validated force-error bound.

## Next target

Use a cancellation-preserving force-weighted formulation: propagate initial differences and operator-forced increments directly rather than subtracting large homogeneous solutions, and contract with the action's factored force derivative rather than a large assembled coefficient vector where possible. Retest the **same** strict dual gate on both reference and MTS, or use genuinely higher precision with a clearly separate error budget. Do not simply weaken the failed tolerance.

Once that precision qualification closes, isolate the force-weighted frozen operator commutator already identified by(7), including its initial-data contribution and actual source-local rows. This is the next spatial-consistency target; another blind time refinement is not justified by the current force results.

## Evidence and limits

- Full action/Schur response: `scripts/annular_full_schur_force_20260919.py`.
- Original-action affine propagator: `scripts/annular_position_action_response_20260919.py`.
- Independent algebra controls: `scripts/validate_annular_full_force_20260919.py`.
- Actual endpoint/secant calculation: `scripts/derive_annular_full_force_endpoints_20260919.py`.
- Failed strict transport: `scripts/derive_annular_full_force_transport_20260919.py`.
- Precision diagnostic: `scripts/diagnose_annular_full_force_duality_20260919.py`.
- Transport with failed qualification explicitly retained: `scripts/derive_annular_full_force_transport_v2_20260919.py`.
- Prior seal: `source-intake/navier-stokes/20260914/annular-coarse-time64-final-integrity-v2.json`.

The four completed new runs have70+59+17+622=768 scoped implementation checks. They are not independent physical validations. The strict transport failure is retained. The first sealer also fails because its broad filename-prefix scan picks up an unrelated, completed September16 linearization run and wrongly expects it to be a new failure. That earlier run is not changed. A versioned sealer uses explicit owned-run paths and preserves the first sealing failure. The second sealer then fails a hand-entered total that omitted12 source-hash checks in the precision diagnostic. The final sealer derives totals directly from owned status files instead of requiring that erroneous constant. Three new failed executions are thus retained, increasing the historical count from45 to48. The retained false dual qualification is additional information, not counted as a passed physical check.

The corrected integrity implementation is `scripts/seal_annular_full_force_v3_20260919.py`; preceding failed manifests are `source-intake/navier-stokes/20260914/annular-full-force-final-integrity.json` and `source-intake/navier-stokes/20260914/annular-full-force-final-integrity-v2.json`. This bookkeeping correction changes no calculation or scientific acceptance threshold.

The original12.5718% impulse mismatch and13.5770% fine-continuum endpoint mismatch are unchanged. The32.5535% MTS coarse-fine force difference is a different comparison and denominator. This does not establish the full GR limit, a refinement-uniform bound, a certified continuous-time estimate, the original longer.004 window, or new observational agreement.

Private post-checkpoint-work only; one single-core BelowNormal worker at a time, no subagents/GitHub/sibling edits. Protected-workbench verification uses modification times since2026-09-19 21:32:36UTC, not a pre-turn whole-tree hash baseline.
