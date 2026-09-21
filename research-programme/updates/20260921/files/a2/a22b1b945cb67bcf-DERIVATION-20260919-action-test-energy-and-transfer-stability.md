# Action-based test energy and the nonnested transfer

Private checkpoint, 19 September 2026. This follows `DERIVATION-20260919-moving-Gram-regularity-and-adjoint-transport.md`. No action, source condition, trajectory, coupling, or earlier result is replaced.

## 1. What energy actually needs to control

For the fixed reference-mesh interpolation I already used in the hierarchy, let

```text
e = u_h - I u_H,     d = e_dot,     a = d_dot,
M a + K e = R,
K = K_gradient + B^T W B.
```

Here M and K are the fine scalar mass and stiffness from the unchanged action, with live geometry/source dependence. R retains the seven previously derived channels: gradient stiffness transfer, Gram stiffness transfer, source kinetic force, cross transport, source acceleration, mass transport and inverse-momentum-residual derivative. This is the scalar hierarchy equation, not an asserted closed Hamiltonian for all gravity/matter degrees of freedom.

The source-pinned P2 fields have positive scalar mass and coercive gradient stiffness under the existing positive geometry/Jacobian assumptions. We check the assembled matrix action and its positive Cholesky factors numerically; this does not certify arbitrary future geometry.

Define

```text
E_0 = (d^T M d + e^T K e)/2,
E_1 = (a^T M a + d^T K d)/2.
```

**E_1 controls ||B d||_W directly**, since ||B d||_W^2 <= d^T K d <= 2E_1. It does **not** control ||B a||_W: the acceleration term in E_1 has the mass norm, not the stiffness norm. Requiring a Gram norm of a would introduce another derivative unnecessarily for the present weak-work estimate. This corrects the overly strong target suggested at the previous checkpoint.

## 2. Exact differentiated energy law

Differentiating the hierarchy equation along the full evolving state gives

```text
M a_dot + K d = R_dot - M_dot a - K_dot e.
```

The conservative cross terms cancel by symmetry, leaving

```text
E_1_dot = a^T R_dot
        - (1/2) a^T M_dot a
        - a^T K_dot e
        + (1/2) d^T K_dot d.                         (1)
```

The negative sign on the mass term and the stiffness-displacement term are essential. Four independent, nonzero dense fixtures compare (1) against direct differentiation and detect omission of every channel. This is algebra validation, not independent physical confirmation.

Let

```text
m >= ||M^(-1/2) M_dot M^(-1/2)||,
k >= ||K^(-1/2) K_dot K^(-1/2)||,
c >= ||M^(-1/2) K_dot K^(-1/2)||,
F = ||R_dot||_(M^-1),   beta=max(m,k).
```

Energy Cauchy-Schwarz gives

```text
|E_1_dot| <= beta E_1 + sqrt(2E_1) [F + c sqrt(2E_0)].
```

For Y=sqrt(2E_1), in the upper-Dini/regularized sense also at Y=0,

```text
Y_dot <= (beta/2) Y + F + c sqrt(2E_0),
Y(t) <= exp(Q(t)) [Y(0) + integral_0^t exp(-Q(s))
                                  (F(s)+c(s)sqrt(2E_0(s))) ds],
Q(t) = integral_0^t beta(s)/2 ds.                     (2)
```

This is a **conditional energy estimate**, not a closed nonlinear stability theorem. In particular R_dot can depend on the same evolving fields and higher derivatives. Evaluating its norm at a few states does not bound that integral uniformly in time or resolution. No commutation of mass, stiffness, projection or geometry operators is assumed.

The implementation uses Cholesky coordinates (equivalent energy norms), absolute row-sum bounds for the symmetric mass/stiffness rate operators, and a Frobenius bound for the cross operator. These finite floating-point matrix bounds are not interval-arithmetic error certificates.

## 3. The mass-adjoint stability constant must be earned

The actual coarse test is eta=A d, with A=M_H^-1 I^T M_h. Define the squared finite-grid norms

```text
C_A = sup_(d != 0) (A d)^T K_H (A d) / (d^T K_h d),
C_G = sup_(d != 0) ||B_H A d||_(W_H)^2 / (d^T K_h d).
```

Since K_H dominates its Gram part, C_G <= C_A. With K_H=L_H L_H^T and K_h=L_h L_h^T,

```text
C_A = ||L_H^T A L_h^(-T)||_2^2,
C_G = ||sqrt(W_H) B_H A L_h^(-T)||_2^2.               (3)
```

We evaluate these operators over **all fine scalar directions**, not just the observed velocity error. The largest eigenvalue of T T^T gives the numerical sharp value; max_i sum_j |(T T^T)_ij| is an explicit algebraic upper bound. The maximizing vector is transformed back and its original-coordinate Rayleigh quotient checked independently. This is a finite-matrix calculation, not a mesh-uniform theorem.

The original weak work therefore obeys

```text
|W_G| <= [sqrt(C_G) ||B_H u_H||_(W_H)
                      + ||B_h Iu_H||_(W_h)] sqrt(d^T K_h d)
      <= [same prefactor] sqrt(2E_1).                 (4)
```

Equation (4) needs neither a bounded unweighted curvature-jump total nor a Gram norm of a. Its usefulness nevertheless depends on C_G, E_1 and the forcing in (2), which cannot be assumed small.

### Measured finite-grid warning

At the actual final states, with 257/513 bulk nodes and the existing 2e-5/1e-5 source caps:

| Squared energy norm | Reference | MTS |
|---|---:|---:|
| Sharp C_A | 2334.01687 | 2266.86004 |
| Row-sum upper bound on C_A | 3992.68166 | 3858.47110 |
| Actual observed d quotient in C_A | .257284 | 7.505334 |
| Sharp C_G | 0 | 118.16684 |
| Row-sum upper bound on C_G | 0 | 176.09822 |

The initial constants are almost the same. These are energy amplification factors; corresponding norm factors are their square roots. Neither branch supports an assumption that the old mass-adjoint is an innocuous near-contraction. The reference's zero Gram constant is structural because its additional Gram operator is absent, not proof of a physical advantage.

For the original worst stiffness direction normalized to fine energy1, approximately84.4% (reference) and84.7% (MTS) of the amplified coarse energy lies in the ordinary element **[6.02625,6.026875]**, not the immediate source element. The five largest elements hold about97.7% of the coarse energy. Immediate-source gradient contributions are only about1.6e-5 of that energy. Neighboring cell-length ratios reach40 on the coarse mesh and20 on the fine mesh. Those observations motivate a comparison-operator control; they do not by themselves prove which construction causes the amplification.

## 4. Checking a genuine canonical derivative, not a frozen path

If v=v(s) and the complete canonical state obeys s_dot=F(s), then

```text
a(s)=Dv(s) F(s),
a_dot = D^2v(s)[F,F] + Dv(s) DF(s) F(s).              (5)
```

A second difference of v(s+epsilon F(s)) with F frozen misses the second term in (5). We therefore reconstruct F at each outer perturbed state and use its own full all-label canonical direction for the inner acceleration probe. Source acceleration, changing mass/cross terms, and the inverse residual rate remain present. An elementary nonzero control v(s)=s^2, F(s)=s^3 distinguishes 8s^6 from the erroneous frozen value2s^6.

The actual endpoint calculation uses outer steps1e-7 and5e-8, with inner steps half as large, in both branches. R is reconstructed independently from the seven action channels at each probed state and compared with M a+K e. Its finite derivative is then used in (1). These are numerical directional estimates; neither two probe sizes nor internal product-rule agreement certifies derivative convergence.

For an exact finite-secant check, use midpoint-averaged M,K,e,d,a, secants D, and endpoint spacing2epsilon. The differentiated-law expression has additional terms

```text
bar(d)^T bar(K) [D(d)-bar(a)]
-bar(a)^T bar(K) [D(e)-bar(d)]
+(epsilon^2/2) [D(a)^T D(M) D(a) + D(d)^T D(K) D(d)]. (6)
```

Keeping (6) separates an exact algebraic secant identity from a claimed time derivative. The finite probes are not evolved replacement trajectories.

## 5. Common-refinement control of the transfer

The newly measured large C_A requires an independent test of nodal transfer aliasing. On the union of the coarse and fine reference element boundaries, assemble

```text
C = integral Phi_H(x)^T rho_h(x) Phi_h(x) dx,
P = M_H^-1 C,
J = M_h^-1 C^T,
A-P = M_H^-1 [I^T M_h-C].                            (7)
```

Here rho_h is the actual fine physical mass density pulled back to the reference coordinate. Quadrature is split at every coarse/fine element boundary, and the reconstructed fine mass is checked against the original matrix. J and P are exact mass adjoints of one another in this finite construction; P is not quietly substituted for A in the old calculation.

For the original maximizing direction, write A d=P d+(A-P)d. Its stiffness energy contains the P energy, defect energy **and their signed cross term**. For the actual work the exact split is

```text
(B_H u_H)^T W_H B_H A d
 = (B_H u_H)^T W_H B_H P d
 + (B_H u_H)^T W_H B_H (A-P)d.                       (8)
```

Dropping the second term would change the original result and is not allowed. P,J also depend on the geometry when built this way; replacing I in a future moving error definition would introduce J_dot u_H and further derivative terms. The present control is a *frozen-state diagnostic*, not a revised field equation, prediction or dynamical proof.

## Numerical completion

All calculations completed:36 algebra checks,60 actual transfer-stability checks,6 localization checks,62 nested-derivative/energy checks and18 common-mesh checks: **182 implementation checks**, not independent physical validations. All43 earlier failed executions remain preserved; this stage added none. No worker started a new evolution.

### A. The action-energy identity survives actual canonical probing

At outer step5e-8 and inner step2.5e-8:

| Quantity | Reference | MTS |
|---|---:|---:|
| E_1 | 2.88531185e-7 | 4.80557380e-6 |
| Derived E_1 rate | -3.02731691e-6 | -8.11523833e-4 |
| Direct nested-probe rate | -3.02726572e-6 | -8.11523912e-4 |
| Differential identity comparison error | 5.12e-11 | 7.90e-11 |
| Exact corrected secant comparison error | 9.53e-16 | 3.03e-14 |
| Conditional absolute rate bound | .00118458 | .148459 |
| Residual-derivative mass-dual norm F | .924203 | 46.05060 |
| beta/2 | .0547717 | .0667538 |

Both endpoint E_1 rates are negative, even though the preceding MTS weak Gram work rate was positive. Those are different quantities; their signs are not contradictory. A negative endpoint energy rate is **not** a stability theorem, just as positive weak-work growth was not by itself an instability theorem.

The conservative norm bound is much looser than the signed rate. The cross-operator Frobenius bounds c are about3.90e4 (reference) and1.13e5 (MTS). These are finite matrix estimates on a highly graded discretization, not physical coupling constants. They illustrate why merely displaying a Gronwall inequality does not close the problem.

At the two probe sizes, the reference signed rate changes by about.74%; the MTS rate changes by about.00064%. The internal differential identity agreeing well does not certify the absolute derivative: the same nested estimates enter both sides. Every numerical result remains explicitly non-claim, with no interval or monotone-convergence certification.

The retained action-channel contributions to a^T R_dot at the smaller probe are:

| Channel | Reference | MTS |
|---|---:|---:|
| Gradient-stiffness transfer derivative | -5.68109e-6 | +2.30789e-5 |
| Gram-stiffness transfer derivative | 0 | -8.37652e-4 |
| Source kinetic derivative | +1.31527e-6 | +1.43418e-6 |
| Cross-transport derivative | +1.23777e-6 | +1.46986e-6 |
| Source-acceleration derivative | -1.59040e-11 | -6.70324e-9 |
| Mass-transport derivative | +4.76456e-9 | +7.05839e-8 |
| Inverse-residual derivative | -4.31720e-10 | -4.75990e-9 |

Thus the Gram-transfer derivative is the leading signed MTS forcing contribution in this diagnostic. Source and numerical inverse-residual terms remain retained, not assumed absent. The full matrix/energy work bound in (4) is4.38153e-6 for MTS, versus actual weak work4.05936e-10. It is substantially looser than the previous saved-path bound1.06290e-7. The advance here is a derived action-based control route, **not a newly sharp numerical error bound**.

### B. Common-mesh quadrature isolates a real transfer problem—but not the actual mismatch

The union mesh has547 cells. Reconstructing the original fine mass on it agrees to about1.55e-13 relative maximum-entry error in both branches. The common-mesh cross mass differs from I^T M_h by as much as.05934 in an entry; this is not explained by floating roundoff.

| Finite-grid squared norm | Reference | MTS |
|---|---:|---:|
| Original sharp C_A | 2334.01687 | 2266.86004 |
| Common-mesh sharp C_A | 11.99397 | 115.33175 |
| Common-mesh upper C_A | 18.68489 | 319.90766 |
| Original sharp C_G | 0 | 118.16684 |
| Common-mesh sharp C_G | 0 | 114.73946 |

For the **old maximizing direction**, its coarse energy falls from2334.02 to.99982 under the common-mesh projection in the reference, and from2266.86 to1.09171 in MTS. The retained nodal-minus-common defect carries energies2333.54 and2266.52 respectively, with signed cross energies-.52286 and-.75483. This demonstrates that nodal transfer aliasing accounts for the enormous amplification in that old worst direction. It does not make the new operator a contraction over *all* directions; its different worst directions give the constants in the table.

Crucially, **this does not explain away the actual MTS weak-work mismatch**. For the observed test field, the coarse work splits as

```text
original coarse work       = 4.403423232748186e-10,
common-mesh coarse work    = 4.403434500791122e-10,
retained nodal defect work = -1.126804293702491e-15.
```

The defect is only about.00028% of the total original weak work. Correcting that comparison operator alone would leave the observed Gram mismatch almost unchanged, and would not alter the raw force/impulse discrepancy. The remaining Gram stability constant also changes only modestly. This is a useful rejected explanation, not permission to relabel the mismatch a harmless coding artifact.

## Decision and next derivation

We now have an exact differentiated scalar-energy law, a conditional growth estimate, and measured finite-grid constants connecting that energy to the weak Gram diagnostic. What remains is **closure of the forcing**, not discovery of another missing symbol. Neither the large unweighted jump totals nor the old worst nodal-transfer direction should be used as an MTS-only rejection test; equally, neither can be used to excuse the actual discrepancy.

The next focused calculation should derive and evaluate the leading Gram residual derivative directly from its operators, avoiding a numerical jerk wherever possible. With T=M_h I M_H^-1 and fixed I,

```text
S_G = T K_G,H u_H - K_G,h Iu_H,
T_dot = M_h_dot I M_H^-1 - T M_H_dot M_H^-1,
S_G_dot = T_dot K_G,H u_H + T K_G,H_dot u_H + T K_G,H v_H
        - K_G,h_dot Iu_H - K_G,h I v_H.              (9)
```

Equation (9) is derived here; its dedicated action-channel comparison and a useful uniform forcing bound are **not yet completed**. It contains no hidden assumption that the operators commute and needs only velocities and geometry/mass derivatives, rather than the full third field-time derivative. The next test should compare it with the already saved nested result, retain signed source/gradient cancellations, and then seek a closure in E_0/E_1 plus explicit consistency terms. Replacing R_dot by its measured endpoint value would be circular as a time-uniform proof.

Do not silently replace I by the geometry-dependent common-mesh J. If a future fixed or moving projection is adopted, derive its altered residual and all time-derivative terms first; keep the present results as the original baseline.

## Claim limits and reproducibility

The original **12.5718%** impulse and approximately **13.58%** instantaneous hierarchy-force discrepancies remain unchanged. This does not establish the full GR limit. The tested physical setup remains the normalized annular one through t=4e-5; the .004 interval, SI bounds and other sectors are not retested. Checks are implementation controls, not independent physical validations. No GitHub, subagents, sibling-workbench changes or new trajectories.

- Previous integrity: `source-intake/navier-stokes/20260914/annular-moving-Gram-regularity-final-integrity.json`.
- Energy/transfer algebra: `scripts/annular_action_test_energy_20260919.py`, `scripts/validate_annular_action_test_energy_20260919.py`.
- Actual stability: `scripts/derive_annular_action_adjoint_stability_20260919.py`.
- Worst-direction localization: `scripts/diagnose_annular_action_adjoint_amplification_20260919.py`.
- Nested canonical derivatives: `scripts/derive_annular_differentiated_action_energy_20260919.py`.
- Common-mesh counterfactual: `scripts/derive_annular_common_mesh_adjoint_control_20260919.py`.
- Numerical evidence: `source-intake/navier-stokes/20260914/annular-action-adjoint-stability-attempt01/status.json`, `source-intake/navier-stokes/20260914/annular-differentiated-action-energy-attempt01/status.json`, `source-intake/navier-stokes/20260914/annular-common-mesh-adjoint-control-attempt01/status.json`.
- Final export/integrity generator: `scripts/seal_annular_action_test_energy_20260919.py`.

The protected-workbench check is mtime since 2026-09-19 16:30:14 UTC, not a pre-turn whole-tree hash baseline. Completed evidence and executed sources are immutable; failed attempts, if any, remain visible.
