# Original-action bulk/source-trace refinement at the long horizon

Private continuation of `DERIVATION-20260916-causal-coupled-defect-correction.md`. Start2026-09-16T16:49:55Z; safe check-in by20:49:55Z. No GitHub, subagents or protected-workbench edits.

## 1. Return to the physical comparison

The previous correction predicted the original finite dynamics from a reduced trajectory atT=.005. It did not fix the originalT=.4 comparison with the independent GR reference. This checkpoint returns to that original action and horizon, with the unchanged compact initial profile, source position6.03, speed.06, source mass.03 and prescribed flat background. This flat-background moving-source control is not the full GR limit or a live-geometry parent theory.

The old grids257/8 and513/4 changed both bulk resolution and local subdivision at once. Complete a paired rectangle with257/4,257/8,513/4,513/8, and test1025/8 as a predetermined finer continuation if runtime permits. Keep BOTH reference and MTS branches. Store81 evenly spaced times, not just the old9, and compare with the original384/512/768 characteristic references replayed at all81 times with tighter integration.

The action formula and all Gram rows remain unchanged. At fixed base grid, local subdivisions embed the old polynomial space exactly. Across base grids, however, the original Gram rows/weights themselves follow their existing grid definition: these are NOT exactly nested Gram matrices, and evidence of convergence would still require a joint-limit argument. The physical left/right source-cell widths are recorded; a source can occupy a different fraction of the base cell after refinement, so base-count ratios alone do not define the local scale ratio.

Unchanged gates: field relative error.005; source5e-7; source rate2e-5; clock2e-7; endpoint force must meet absolute2e-7 AND relative.02. The stronger sampled force requirement is absolute2e-7 at every stored time. Eighty-one samples are still not a uniform-time theorem. Classifications against each reference resolution are retained: disagreement between references is a reference-resolution warning, not automatically a theory failure.

## 2. Exact preassembly, not physical reduction

The same original finite action is

```text
L = v^T M(b) v/2 + V v^T A(b)u + V^2 u^T B(b)u/2
    - u^T K(b)u/2 - S sqrt(1-V^2).
```

Let delta=b-b0. On each reference half-domain the original moving map has R=r+s delta and J=1+j delta, with s and j fixed. In the flat background the quadrature weights are therefore

```text
M: w J R^2,
A: -w s R^2,
B: w s^2 R^2/J,
K_bulk: w R^2/J,
K_Gram: L_lift^T diag[sampling(R_node^2/J_node)/h] L_lift.
```

Consequently M is cubic in delta, A is quadratic, and B,K are sums of quadratic numerators divided by the two linear Jacobians. Preassemble their coefficient bands and Gram row weights once, then evaluate these exact polynomials/rational functions and their analytic b derivatives. No interpolation in b, fitted force, modal deletion, static trace relaxation or change of initial data occurs. The source Schur solve and all canonical momentum terms are retained.

Writing D=M_b+A-A^T and E=A_b-B, the same coupled acceleration equations are

```text
H = [[M,A u],[(A u)^T, S/(1-V^2)^(3/2)+u^T B u]],
r_u = -V D v - K u - V^2 E u,
r_b = v^T(M_b/2-A)v - 2V v^T B u
      - V^2 u^T B_b u/2 - u^T K_b u/2,
H [uddot,bddot] = [r_u,r_b].
```

The full original force is S bddot/(1-V^2)^(3/2); the clock rate is sqrt(1-V^2). Energy and source inertia are diagnosed rather than projected. The five-diagonal mass solve and sparse Gram products replace repeated quadrature assembly, not the mathematics.

`scripts/annular_flat_preassembled_flow_20260916.py` implements this flat-only evaluation. `scripts/verify_annular_flat_preassembly_20260916.py` checks action, energy, acceleration, force and complex-step variational directions against the independent original quadrature implementation on both branches, grids33 through1025, initial and moved/perturbed states. All96 checks pass; largest tested acceleration relative discrepancy1.40e-11 and force discrepancy5.61e-15. These are implementation comparisons, not physical accuracy against GR.

## 3. Run and validation design

- `scripts/run_annular_joint_refinement_20260916.py`: unreduced full evolution, original frozen-spectrum step rule refreshed every.05,81 saved times, safe accepted chunks, original Euler-Lagrange/force checks at9 times. Baseline tolerances2e-10/2e-12; optional full-duration controls halve the step cap and tighten tolerances to2e-12/2e-14.
- `scripts/run_annular_dense_GR_references_20260916.py`: original384/512/768 references,81 times, tighter2e-12/2e-14 and.05/degree step caps; explicitly compare with their old9-time forces.
- `scripts/validate_annular_joint_refinement_20260916.py`: same gates and reference resolutions for both branches, field quadrature control, original-case replay comparisons, source/bulk rectangle effects and reference-dependent flags. It never requires a physical pass to record a successful implementation.
- `scripts/validate_annular_joint_refinement_20260916_v2.py`: preserves the first validator's historical replay failure rather than aborting before inspecting the remaining new cases. The old reference257/8 run differs in state by2.41193e-8 versus the unchanged2e-8 replay threshold, while its force difference4.18574e-9 passes the separate force control. Its state-replay flag remains FALSE. The new validator records that exception, and adds full-duration tighter257/8 runs for BOTH branches alongside the planned513/8 controls; it does not convert the failed legacy check to a pass. The old reference used53632 RHS calls without the later spectrum cap, compared with373508 in the new baseline, so different temporal resolution is a candidate explanation to test, not an assumed excuse.

The four-grid rectangle separates the effect of local subdivision at fixed original Gram stencil from changing the bulk/stencil resolution. Its interaction is

```text
I(t) = [F_513,8(t)-F_513,4(t)] - [F_257,8(t)-F_257,4(t)].
```

Nonzero I means the two refinement effects do not add independently at these finite scales. It is not a new physical coupling. Source-boundary inertia and its initial memory evolve in the full equations and are never suppressed to improve the fit.

### Why the two refinement directions are not interchangeable

The previously derived unit-trace layer of thickness epsilon has mass O(epsilon^3), bulk stiffness O(epsilon), and fixed-stencil Gram trace stiffness D. Refining only the trace layer at fixed bulk stencil therefore permits a trial frequency of order sqrt(D)/epsilon^(3/2). In a joint regime epsilon proportional to h and D proportional to h, the same trial ratio instead gives frequency of order1/h. Thus the severe fixed-stencil trace limit is not automatically representative of the joint limit.

This is a conditional scaling deduction from the existing layer formulas, not a theorem that the actual full moving spectrum or force error has that asymptotic behaviour. The validator records the actual source-width/h ratios and D/h, where D=(G hinge)^T W(G hinge), to expose whether the tested sequence is even compatible with that regime. It does not set the trace to equilibrium, erase homogeneous oscillations, or infer force convergence from energy convergence. The source-width fraction changes across dyadic base grids, and that finite-scale effect is explicitly retained.

## 4. Results and decision

### Exact full-Gram source-force response

At the same original field/source state, MTS and the reference branch share M,A,B and the material action; only K_Gram differs. Put c=A u, s=H_bb-c^T M^-1 c and mu=S/(1-V^2)^(3/2). Subtracting the two coupled Euler-Lagrange systems therefore gives

```text
Delta F_same = (mu/s) [-u^T K_Gram,b u/2 + c^T M^-1 K_Gram u].
```

The second term is the source response to the changed field acceleration. Keeping only the explicit derivative of Gram energy would omit it. With two independently evolved states y_M and y_R, the complete difference is exactly

```text
F_M(y_M)-F_R(y_R)
  = [F_M(y_M)-F_R(y_M)] + [F_R(y_M)-F_R(y_R)].
```

The validator evaluates the derived same-state formula and the separately measured trajectory feedback at all81 times on every paired grid. This split depends on the chosen common state and is not a unique causal intervention; no term is subtracted from the actual predictions or from a failed GR comparison. A small Gram energy alone is not a bound on its force or accumulated feedback.

All ten new baseline trajectories reachT=.4, with81 stored times. Four full-duration tighter controls finish on257/8 and513/8, both branches. The denser384/512/768 GR replays and the final validator are complete. No evolved trajectory was reduced or force-adjusted.

### Actual force comparison

Errors below use the finest768 GR reference, in the original control's force units. The unchanged absolute threshold is2e-7; endpoint acceptance also retains the2% relative threshold.

| Base / splits | Reference endpoint error | Reference maximum over81 times | MTS endpoint error | MTS maximum over81 times |
| --- | ---: | ---: | ---: | ---: |
| 257 / 4 | 4.55104e-7 | 2.16444e-6 | 8.26919e-6 | 1.37251e-5 |
| 257 / 8 | 2.92625e-7 | 2.16847e-6 | 7.74682e-6 | 1.35382e-5 |
| 513 / 4 | 1.17966e-9 | 7.84943e-7 | 2.61803e-6 | 3.04088e-6 |
| 513 / 8 | 2.25912e-7 | 5.48205e-7 | 2.30808e-6 | 3.67184e-6 |
| 1025 / 8 | 1.77193e-7 | 2.16929e-7 | 7.70343e-8 | 9.20686e-7 |

The finer MTS endpoint passes against ALL three references. Its entire sampled trajectory does not: its maximum remains4.60 times the absolute threshold, peaking atT=.21. Even the old9 observations would not pass: their maximum is3.42445e-7. The81-time check exposes an appreciably larger interior peak rather than rewarding a favourable endpoint.

The reference branch is subjected to the same tests. None of its tested cases passes the81-time force requirement either. Its finest peak is only1.085 times the threshold; the reference1025 endpoint verdict depends on oracle resolution (384 fails,512/768 pass). Thus baseline discretization/reference effects are real, not counted exclusively against MTS. But the MTS maximum is still substantially larger and cannot be excused by that baseline issue.

The maximum384-versus768 and512-versus768 oracle force differences are8.78433e-8 and4.44074e-8, respectively. Old-versus-new time-integration changes of these references are below9.52e-13. Spatial oracle uncertainty therefore matters near the reference branch's threshold; it is too small to explain the MTS9.21e-7 peak. These differences are resolution diagnostics, not rigorous uncertainty bounds.

### Bulk refinement helps; extra local subdivision is not a universal cure

At eight source subdivisions, MTS peak error decreases1.35382e-5 ->3.67184e-6 ->9.20686e-7 as base resolution increases257 ->513 ->1025. Improvement factors3.687 and3.988 correspond to observed orders1.882 and1.996. This is consistent with roughly second-order reduction on these three grids, not an asymptotic convergence theorem or permission to extrapolate a pass. The reference observed orders are1.984 then1.337, so even the baseline is not uniformly following a clean fitted power law.

At fixed513, doubling the source subdivision improves the MTS endpoint but worsens its81-time maximum from3.04088e-6 to3.67184e-6. At fixed257 it changes the maximum only slightly. The MTS refinement-rectangle interaction reaches2.76412e-6, while the reference interaction reaches6.43886e-7. The two numerical refinement directions do not simply add. Blindly shrinking the source cell alone is therefore not supported as the next cure.

Measured MTS D/h values are2.80958,1.43466,2.80744 on257,513,1025, with no change under local subdivision at fixed base. Source-width/h ratios for the eight-split sequence are(0.10,0.025), (0.075,0.05), (0.025,0.10). These data are compatible with the conditional joint scaling discussed above, but the changing source-cell fraction is significant and no constant asymptotic coefficient is inferred.

### Field, source motion and clock

Every tested branch/grid passes the existing field and source/velocity/clock gates. Against768, maximum MTS field error at eight splits decreases0.194237% ->0.049396% ->0.012751%; the corresponding reference values are0.036532% ->0.009547% ->0.002585%. The finest MTS source-position, speed and clock errors are2.053e-10,5.752e-8 and1.196e-11. Good state/waveform behaviour does not override the stricter source-force failure.

### The derived coupling response explains why energy is insufficient

The exact same-state Gram-force identity agrees with direct paired force evaluation within1.98e-18 across all405 sampled states. Representative complete, signed endpoint splits are:

| Base / splits | Direct Gram force | Changed-trajectory feedback | Total MTS minus finite reference |
| --- | ---: | ---: | ---: |
| 257 / 8 | +2.45636e-5 | -1.71094e-5 | +7.45419e-6 |
| 513 / 8 | +6.36748e-6 | -8.90147e-6 | -2.53399e-6 |
| 1025 / 8 | -2.69937e-7 | +1.57099e-8 | -2.54228e-7 |

The maximum direct and feedback contributions on1025/8 are1.47444e-6 and2.18340e-6, while the maximum total branch difference is1.08102e-6. Their maxima need not occur at the same time. The maximum Gram energies decrease7.10840e-9 ->4.52964e-10 ->2.86178e-11, roughly sixteenfold per bulk refinement. Hence a rapidly shrinking energy term still produces larger force/trajectory contributions with cancellations and sign changes. Dropping the feedback term, subtracting the direct term, or equating energy convergence with force convergence would be wrong.

### Time controls and preserved legacy failure

The first validator stopped on reference257/8's historical state replay difference2.41193e-8; this resides in field rates, not source position. Its old/new force difference is4.18574e-9. The original2e-8 state-replay criterion and FALSE verdict are preserved. The historical run used53632 RHS calls without the later spectrum cap. The new baseline and tighter capped versions use373508 and746624 calls and differ in state by1.324e-13 and force by3.568e-14 over the full horizon. Together with the independent original-action checks, this strongly supports insufficient historical temporal resolution as the explanation; it is not a reason to erase the historical failure or relax its tolerance.

Full-duration baseline/tighter maximum force changes are:

| Grid | Reference | MTS |
| --- | ---: | ---: |
| 257 / 8 | 3.568e-14 | 7.327e-12 |
| 513 / 8 | 6.342e-14 | 3.641e-12 |

These are many orders below the remaining GR force discrepancies on those grids. The1025/8 run does NOT yet have its own full-duration tighter control. Its endpoint success and observed refinement trend are therefore provisional numerical evidence, not a fully controlled final win. Per-case flags explicitly enforce that distinction.

### Decision and next bounded target

This is a real advance in the original long-horizon comparison: the unmodified MTS action now reaches the endpoint gate on the finest tested grid, and the whole-trajectory discrepancy decreases substantially under bulk refinement. It is NOT the full sampled force pass, a continuum proof, or a general GR reduction.

Next, prioritize a full-duration tighter1025/8 check on BOTH branches, and derive the leading spatial/source-force defect around the largest discrepancy nearT=.21. Use the explicit Gram/source-Schur identity AND the induced trajectory response. A useful constructive route is to project the independent GR reference into the original source-fitted variables, derive its discrete field/source/clock residual, and test whether that residual predicts the signed force-error curve without fitting or subtraction. Qualify the projection and its time derivative first; these have not been constructed here. Do not simply replay the priorT=.005 reduced/full correction or jump straight to a much larger mesh based on a fitted power law.

Successful current suites: exact preassembly96, dense GR references12, paired rectangle33, finer1025 run9, tighter513 run9, additional tighter257 run9, final validation54; total222 implementation/control checks. One failed validation is preserved in addition to21 earlier failed attempts. These counts are not physical confirmations.

Evidence:

- `source-intake/navier-stokes/20260914/annular-flat-preassembly-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-dense-GR-references-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-joint-rectangle-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-joint-finer1025-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-joint-tight513-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-joint-tight257-attempt01/status.json`
- Preserved failure: `source-intake/navier-stokes/20260914/annular-joint-validation-attempt01/status.json`
- Final validation: `source-intake/navier-stokes/20260914/annular-joint-validation-attempt02/status.json`
- Prior seal: `source-intake/navier-stokes/20260914/annular-causal-correction-final-integrity.json`
- Current seal (complete only when its state says so): `source-intake/navier-stokes/20260914/annular-joint-refinement-final-integrity.json`

All own numerical jobs have finished; final integrity sealing follows. Work remained local with at most two low-priority workers sharing one CPU core. No public repository action or change to the protected workbench.
