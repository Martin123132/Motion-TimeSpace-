# Moving Gram regularity and the mass-adjoint transport law

Private derivation checkpoint, 19 September 2026. This continues the fixed-field result rather than changing the action, source condition, or acceptance test.

## Scope and result status

The previous checkpoint proved a fixed-compensated-P2 consistency bound. Its missing hypothesis was control of the *evolving*, resolution-dependent trial and test fields. Here we derive the relevant transport identities and test them against saved evolution in both branches. The calculations use the same normalized annular interval, **0 <= t <= 4e-5**, not the longer .004 interval or a physical/SI observational test.

The reference branch is the corresponding numerical setup with the extra Gram term absent; it is not an independent full-GR validation. The known **12.5718%** impulse and approximately **13.58%** instantaneous hierarchy-force discrepancies are not removed by this calculation. This does not establish the full GR limit.

All four bounded calculation groups completed: 15 independent-algebra checks, 415 matched-profile checks, 141 endpoint-transport checks, and 100 weighted-row checks: **671 implementation checks**, not671 independent physical validations. No new trajectories, fitted couplings, discarded modes, subagents, or GitHub actions are involved. The separate integrity seal records source hashes and validation of the exported tables.

**Substantive outcome:** the changing-test law is derived and checked; the observed growth is predominantly an acceleration/test-field effect, not mass/weight drift. A cancellation-preserving weighted-row budget is much tighter than the global derivative-jump budget. We have not yet closed an action-based, continuous-time, refinement-uniform energy estimate.

## 1. The exact changing-test equation

Use the existing fixed, nonnested nodal interpolation I from the coarse reference P2 mesh to the fine reference mesh. Do not assume it is an exact function inclusion, symplectic map, or mass-orthogonal projection. Let

```text
d = v_h - I v_H,
M_H eta = I^T M_h d.
```

Both positive mass matrices change through the reconstructed geometry and source motion. Differentiating, with I fixed, gives

```text
M_H eta_dot = I^T M_h d_dot
            + I^T M_h_dot d
            - M_H_dot eta.                         (1)
```

Thus eta_dot has three distinct contributions: test acceleration, fine-mass transport, and coarse-mass transport. Omitting either transport term is an algebraic error, even if a particular run makes it small. The implementation checks all three against an independent dense, nonzero fixture and deliberately detects omissions.

The endpoint d_dot estimate reuses the previous *compensated canonical acceleration*, including source acceleration, cross transport, and the inverse-momentum residual derivative. It is not an acceleration obtained by silently setting that residual to zero. Full all-label geometry is rebuilt on both sides of every saved canonical tangent probe.

### Exact finite-secant counterpart

For any two sampled states define bar(x)=(x_plus+x_minus)/2 and D(x)=(x_plus-x_minus)/Delta_t. The defining mass-adjoint equations at the two endpoints imply

```text
bar(M_H) D(eta) = I^T [bar(M_h) D(d) + D(M_h) bar(d)]
               - D(M_H) bar(eta).                  (2)
```

This is an exact two-endpoint identity, not an asymptotic derivative claim. Since the average of positive definite mass matrices is positive definite, its solve is well-defined. Substituting the central state's masses into (2) instead would generally destroy exactness. Both the saved-time secants and the small tangent probes are checked with the actual averages.

## 2. Source-compensated derivative-jump transport

For a continuous reference P2 field u let j(u) be its source derivative jump and

```text
w(u) = u - j(u) (x - x_source)_+.
A_1(u) = sum_k |a_k(u)|,
A_2(u) = sum_k |b_k(u)|.
```

Here a_k is the first-derivative jump of w and b_k its curvature jump. All ordinary knots are retained; only the analytically prescribed source hinge is compensated. On the fixed reference mesh these maps are linear:

```text
a_dot(u) = a(u_dot),   b_dot(u) = b(u_dot),
j_dot(u) = j(u_dot).                                (3)
```

Source movement is carried by the physical mapping, mass matrices and Gram weights. It does not move the reference anchor or justify deleting j_dot. For the four fields entering weak work, the exact velocities to use are

```text
u_H       -> v_H,
eta_H     -> eta_dot from (1),
I u_H     -> I v_H,
d_h       -> d_dot.
```

For differentiable atom coordinates, the right derivative of their total variation is

```text
D_+ sum |a_k| = sum_(a_k != 0) sign(a_k) a_dot_k
             + sum_(a_k == 0) |a_dot_k|
            <= sum |a_dot_k|.                       (4)
```

The zero case is essential; the total variation need not be differentiable there. In exact mathematics (3)-(4) give, for absolutely continuous fields,

```text
A_i(u(t)) <= A_i(u(0)) + integral_0^t A_i(u_dot(s)) ds.   (5)
```

For eta, (1) supplies u_dot rather than an unexplained closure. Writing J_i for the respective compensated atom map yields the useful sufficient estimate

```text
A_i(eta(t)) <= A_i(eta(0)) + integral_0^t [
 ||J_i M_H^-1 I^T M_h d_dot||_1
+||J_i M_H^-1 I^T M_h_dot d||_1
+||J_i M_H^-1 M_H_dot eta||_1 ] ds.                  (6)
```

Equation (6) is conditional on these integrals and the mass inverse being controlled. It does not provide a resolution-independent bound merely by being written down. The actual endpoint calculation records each channel after applying J_i, not only its coefficient-vector size, because differentiation can amplify a small coefficient perturbation.

### What saved snapshots can certify

Between recorded times, the triangle inequality gives

```text
A_i(u_n) <= A_i(u_0) + sum_(m=1..n) ||J_i(u_m-u_(m-1))||_1.  (7)
```

This controls the samples and the *piecewise-linear interpolation of their coefficient vectors*. It does not control the unobserved evolution between samples; that interpolant is not asserted to solve the original equations. Sampled maxima, secants, and trapezoidal integrals are not continuous-time suprema or rigorous integration certificates.

## 3. The evolving condition needed for the fixed-field theorem

The previous rational Gram-template bound is C_* = 59097/573104 + 1/56. For q_max=max(h W), the ideal-arithmetic compensated factor obeys

```text
||B u||_W <= sqrt(C_* q_max) [sqrt(2h) A_1(u) + sqrt(3h^3) A_2(u)].   (8)
```

Measured lifting and factorization residuals are retained in numerical implementations; they are not interval-arithmetic error certificates. Define the bracket on the right as L_h(u). For the actual nonnested weak work,

```text
W_G = (B_H eta)^T W_H B_H u_H - (B_h d)^T W_h B_h Iu_H,
|W_G| <= C_* [q_H L_H(eta)L_H(u_H) + q_h L_h(d)L_h(Iu_H)].          (9)
```

An evolving-family consistency proof needs the two products in (9) to tend to zero uniformly on the intended time interval, together with controlled coefficients and arithmetic. Bounds (5)-(6) identify quantities that could establish this. Neither nine snapshots nor a single endpoint derivative establishes those uniform refinement hypotheses.

It is not necessary that every derivative-jump total remain constant, nor that every factor independently vanish: the *products* determine the sufficient condition. Conversely, powers of h in (8) cannot be cited without controlling the h-dependence of the fields/tests multiplying them. Continuous P2 fields with gradient jumps are not automatically in H^3.

## 4. Signed work transport, without discarding cancellations

For one level put f=B u and g=B z, where B is fixed on the reference mesh. Then

```text
d/dt sum W f g = sum W_dot f g
              + sum W (B u_dot) g
              + sum W f (B z_dot).                 (10)
```

Subtract the fine-level expression from the coarse one. This separates weight, trial and test transport while keeping their signs. Fine factors use the actual fine jump operator on Iu_H and d, so nonnested source-jump differences are retained rather than assumed zero.

As an exact finite-probe check, when endpoints are separated by 2 epsilon,

```text
D(W f g) = D(W) bar(f) bar(g)
         + bar(W) D(f) bar(g) + bar(W) bar(f) D(g)
         + epsilon^2 D(W) D(f) D(g).               (11)
```

The last mixed secant term must not be mistaken for part of the differential product rule. The checks distinguish (10)'s finite-difference estimate from (11)'s algebraic identity.

At every saved time we also reconstruct f and g from local gradient atoms, curvature atoms, polynomial moments and measured floating residual. All sixteen bilinear products are retained, including gradient-curvature cross terms. Absolute budgets are reported separately; they do not replace the signed result.

## 5. A stronger route than global unweighted jump totals

The jump representation is valid but its absolute totals can be extremely pessimistic on the graded mesh. It is not necessary to force that particular majorant to be small. Let

```text
g = sqrt(W) B u,     Y = ||g||_2,
rho = (1/2) max_rows |W_dot/W|.
```

For positive differentiable weights on the fixed active rows, differentiation and Cauchy-Schwarz give

```text
D_+ Y <= ||B u_dot||_W + rho Y,
Y(t) <= exp(R(t)) [Y(0) + integral_0^t exp(-R(s)) ||B u_dot(s)||_W ds],
R(t) = integral_0^t rho(s) ds.                       (12)
```

The empty reference Gram space is handled directly as zero, without dividing by nonexistent weights. A change of active row support would require a separate argument. This keeps cancellation *inside* B u_dot before taking its norm, rather than bounding every gradient and curvature atom separately.

For two saved endpoints write s=sqrt(W), f=B u. There is the exact finite identity

```text
g_plus-g_minus = bar(s) (f_plus-f_minus)
              + (s_plus-s_minus) bar(f).            (13)
```

Summing norms of these two increments bounds all saved Y values. Summing the norm of their *combined* increment is a tighter bound. These are certificates for the saved arrays subject to the stated floating tolerances; their linear interpolation in g is not the physical trajectory. Equation (12), not a sampled sum, is the route to a continuous-time statement.

## 6. What the saved evolution actually shows

Nine matched times were evaluated in each branch, using the coarse32-step trajectory, fine128-step MTS trajectory, and fine64-step reference trajectory. Stored timestamps and hashes were checked. All-label live geometry was reconstructed each time. The initial and final weak work reproduce the previous sealed results.

### A. Unweighted test roughness is not unique to MTS

For the coarse mass-adjoint test eta:

| Quantity | Reference | MTS |
|---|---:|---:|
| Initial A_1 | 1.45033e-4 | 1.45033e-4 |
| Final A_1 | 4.02115e-3 | 4.89441e-3 |
| Initial A_2 | .0259197 | .0259197 |
| Final A_2 | 236.9103 | 202.1209 |
| Largest sampled A_2 | 236.9103 | 860.8097 |
| Sample-path A_2 bound, (7) | 784.07 | 2359.78 |

The MTS curvature-jump total peaks at t=2e-5, not at the endpoint. Its final value is below the reference endpoint, while its interior maximum is higher. Both facts matter. Neither branch gets a stability verdict from an endpoint-only comparison. These large unweighted derivative totals do not alone establish a physical instability; neither do they prove a harmless discretization effect. The meshes contain very short source cells, making derivatives sensitive to small coefficient changes.

### B. Actual signed work and transport

The MTS signed weak Gram work increases from **2.47634280e-11** initially to **4.05935591e-10** finally. The source-straddling portion at the endpoint remains **2.87110e-14**, approximately .00707% of the total. All sixteen local atom products reconstruct the work; their endpoint absolute sum is **1.80163e-9**, so cancellation is significant but not hidden by the reporting.

Using the smallest existing full canonical tangent probe, epsilon=2.5e-8:

| Contribution to endpoint work rate | Value |
|---|---:|
| Test-field transport | 9.52197580e-6 |
| Trial-field transport | 5.70985004e-9 |
| Weight transport | 5.53265851e-12 |
| Signed total | 9.52769119e-6 |
| Direct full-state probe | 9.52769117e-6 |
| Absolute row-rate budget | 4.60254421e-5 |

Test transport accounts for approximately **99.94%** of the total endpoint rate. This is a signed decomposition of a numerical hierarchy diagnostic, not a new physical force or a full causal classification of the theory. The reference Gram work is identically zero because that term is absent; its nonzero test/atom evolution is still tested.

For MTS, the coefficient-vector maximum of eta_dot is **.0059542039**. The fine- and coarse-mass channels each have maximum about **9.3388e-9** and largely cancel. More importantly, after applying the curvature-atom map, the acceleration channel's absolute rate is **9.76114e7**, while each mass channel contributes approximately **10.87**. Thus the same endpoint dominance holds in the derivative diagnostic, not only in coefficient size. No mass term has been discarded from the equations.

The base differential-law comparison error is at most about **1.18e-11** for the MTS coefficient derivative over four probes; exact centered-adjoint errors are at most about **2.96e-15**. Work-rate comparisons agree to about **1.49e-14** or better. Errors are **not monotonically improving with probe refinement**; these are finite numerical controls, not certified derivatives. Signed atom-variation rates can be negative, and near-zero atoms can be roundoff-sensitive. Absolute rate budgets are reported separately.

### C. Cancellation-preserving transport is far less pessimistic

MTS weighted factors on the saved path:

| Field | Initial Gram norm | Final Gram norm | Largest sampled norm | Separated transport bound |
|---|---:|---:|---:|---:|
| u_H | 1.045149e-4 | 1.045147e-4 | 1.045149e-4 | 1.045194e-4 |
| eta_H | 3.652771e-6 | 2.584916e-4 | 4.956500e-4 | 9.014431e-4 |
| Iu_H | 2.638310e-5 | 2.638297e-5 | 2.638310e-5 | 2.638495e-5 |
| d_h | 4.273010e-15 | 5.854292e-5 | 5.854292e-5 | 4.575406e-4 |

Combining these *sample-path* norm bounds gives **1.06290448e-7** for absolute weak work across all recorded times; retaining coupled increments gives **1.06290319e-7**. This is still about **262 times** the largest observed work, so it is not a sharp closure. Nevertheless it is over **23,000 times smaller** than the global derivative-atom work majorant **.00248509 at the endpoint**, while covering every sampled time. These are different scope majorants, not competing physical predictions. The earlier final pointwise Cauchy bound, 2.85607e-8, is tighter than the new whole-sampled-path bound, as expected.

For eta the accumulated field-transport contribution is **8.97790e-4**, versus **2.86298e-10** from changing weights. The trial norm remains nearly unchanged, but the test norm oscillates and grows relative to its small initial value. Endpoint-only regularity checks would miss its interior maximum. This is why another fixed-field refinement plot is not the decisive next step.

## 7. Decision and next calculation

Do not close the evolving-family claim, and do not reject MTS solely because the global A_2 majorant becomes large: the reference also has large jump totals, and the weighted bound is vastly less pessimistic. The outstanding hierarchy discrepancy remains real and unchanged.

The next substantive target is an **action-based energy estimate for the weighted test forcing**, rather than another source-only patch or an assumption of bounded unweighted third derivatives:

1. Use the full scalar stiffness K=K_gradient+B^T W B to control the Gram norm by the action's stiffness energy.
2. Derive the differentiated wave-error energy, keeping changing M/K, source acceleration, source traces, residual forcing and commutators. A bound on the undifferentiated energy is not automatically a bound on its time derivative.
3. Derive/test stiffness-norm stability of eta=M_H^-1 I^T M_h d on the actual graded, nonnested meshes. Positive mass matrices alone do not guarantee a mesh-uniform constant.
4. Only then try to replace the sampled budgets in (12) by controlled time/refinement bounds. A finite-grid constant must be labeled finite-grid, not promoted to a continuum theorem.

This route directly addresses the measured test/acceleration-dominated channel. No long new evolution is justified before establishing what the proposed energy can actually control.

## Reproducible sources

- Previous result: `DERIVATION-20260919-weak-Gram-consistency-and-fixed-field-bound.md`.
- Previous seal: `source-intake/navier-stokes/20260914/annular-weak-Gram-consistency-final-integrity.json`.
- Transport and algebra: `scripts/annular_moving_Gram_budget_20260919.py`, `scripts/validate_annular_moving_Gram_budget_20260919.py`.
- Matched-time evaluation: `scripts/derive_annular_moving_Gram_profile_20260919.py`.
- Full canonical endpoint checks: `scripts/derive_annular_moving_Gram_rate_20260919.py`.
- Weighted-row transport: `scripts/derive_annular_weighted_row_transport_20260919.py`.
- Calculation records: `source-intake/navier-stokes/20260914/annular-moving-Gram-profile-attempt01/status.json`, `source-intake/navier-stokes/20260914/annular-moving-Gram-rate-attempt01/status.json`, `source-intake/navier-stokes/20260914/annular-weighted-row-transport-attempt01/status.json`.
- Export and integrity generation: `scripts/seal_annular_moving_Gram_regularity_20260919.py`.
- Sourced derivative atoms: `scripts/derive_annular_frozen_Gram_refinement_20260919.py`.
- Local signed reconstruction: `scripts/derive_annular_local_atom_Gram_bounds_20260919.py`.

All results are private, non-claim numerical/derivation evidence. Implementation checks are not independent physical validations. Protected-workbench verification uses mtime since 2026-09-19 15:35:14 UTC, not a pre-turn whole-tree hash baseline.
