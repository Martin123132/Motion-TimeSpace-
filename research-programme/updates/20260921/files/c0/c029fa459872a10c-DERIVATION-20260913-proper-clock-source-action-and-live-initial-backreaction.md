# Proper-clock source action and live initial backreaction

Private, 2026-09-13. No publication, new fundamental-field claim, or full spacetime evolution.

## 1. What this construction achieves

The previous free exterior did not supply the acceleration imposed in the old driven problem. This stage constructs an explicit finite-width **external apparatus model** with a proper-clock variable and an energy variable. Its scalar force, energy transfer, and gravitational coupling follow from one action. The geometry is re-prepared with positive initial apparatus energy, rather than keeping the old source-free geometry and adding a force afterward.

Eight matched preparations recover the prescribed outer acceleration while satisfying the modified initial C0 and C1 constraints at both tested quadratures. Omitting the source energy from C0 or its energy loss from C1 gives large failures. Thus the local driven compatibility mechanism is constructive, not just a missing-input ledger.

**This is not a prediction of the prescribed acceleration.** The apparatus enforces a specified trajectory; the equations determine its reaction and energy cost. Neither its microscopic realization nor the unique finite-width profile is derived from MTS. This resolves a limited forced-boundary accounting problem, not the full GR limit, full second-order constraints, or a physical black-hole source.

Predecessors:
- `DERIVATION-20260913-geometric-collar-memory-and-driven-acceleration-law.md`.
- `DERIVATION-20260913-off-shell-finite-width-action-and-clock-coframe.md`.

## 2. Keep the apparatus explicit in the action

Retain the existing scalar fields, metric, horizontal transport, and whole-factor action. At each translated radius in the rightmost scalar collar introduce a source proper-clock reading theta, its conjugate energy E, and a multiplier lambda. The apparatus follows a fixed-radius timelike worldline in the existing positive chart:

```text
U = sqrt(1-2 mu/R),
d_metric = 1-kappa^2 U^4 P^2 > 0,
ell = N sqrt(d_metric),

S_app = integral dz w(z) integral dt
        [ E theta_t - ell E + ell lambda (chi - D_z(theta)) ].
```

Here P is gravitational momentum, not the scalar momentum p. D_z is an externally specified scalar trajectory at that source's proper-clock reading. The weight w and width are the declared existing regulator choices. The source occupies the **whole rightmost collar**, including the portions inside and outside the original physical cut. It is not a delta force inserted at that cut. There is no second copy of the scalar kinetic action.

Proper time ell dt is distinct from both the boundary gravitational clock N/U and the horizontal interaction map. No auxiliary frozen synchronization parameter is substituted for proper time.

Variations give

```text
theta_t = ell,                      chi = D_z(theta),
rho = ell lambda,                  omega_node p_t = Gchi + rho,
E_t = -ell lambda D_z'(theta) = -lambda chi_t,
temporal boundary term = [E delta theta].
```

The equations follow before eliminating the multiplier or imposing the scalar trajectory in the action. Substituting chi=D before varying would incorrectly erase its reaction. The temporal endpoint term is also retained; an unrestricted clock variation verifies that it is not zero.

Define V=E-lambda(chi-D_z). Off shell,

```text
delta_metric S_app = - integral w V delta ell dt dz,
partial_N ell = sqrt(d_metric),
partial_mu ell = 2 N kappa^2 U^2 P^2/(R sqrt(d_metric)),
partial_P ell = -N kappa^2 U^4 P/sqrt(d_metric).
```

On the multiplier constraint V=E, these are the apparatus gravitational variations. At P=0 its lapse contribution is E while its direct mu and P first variations vanish. They must not be discarded at higher order:

```text
partial_P^2 ell |P=0 = -N kappa^2 U^4,
(mu_tt)_app,direct |P=0 = -N kappa^2 U^4 sigma P_t.
```

The last line is only the direct source contribution, with sigma the radial source density. Other metric/scalar/transport derivatives still contribute to mu_tt and the full second-order constraint. It is **not** a completed C2 calculation.

### What is assumed about the apparatus

This is an ideal externally controlled clock/actuator, not a uniquely derived material sector. Its energy is conjugate to clock reading and enters linearly: the enlarged Hamiltonian is not thereby proved bounded below. Restricting the initial data to positive E does not establish global positivity or stability. Fixed-radius support, the stresses needed to hold it there, and radial embedding variations are not resolved by a time-reparametrization check. Those limitations prohibit claiming a complete covariant physical apparatus or a new healthy fundamental MTS field.

## 3. The source changes the initial geometry

Let epsilon remain the scalar bare-energy density from the whole transported stencil, and let

```text
sigma(R) = w((R-r_out)/width) E((R-r_out)/width)/width
```

inside the rightmost band, zero elsewhere. At P=0 the proper-clock source Hamiltonian is N sigma, **not N U sigma**. Consequently

```text
C0_local = mu_R/(kappa U) - U epsilon - sigma,
mu_R = kappa (U^2 epsilon + U sigma),
g_R = -(ln N)_R + mu/(R^2 U^2) + kappa epsilon/R.
```

The direct P_t source term vanishes here, but mu and therefore g change when the initial constraint is re-solved. The old geometric-weight law is correspondingly modified:

```text
H = N U exp(g),
(ln H)_R = 2 mu/(R^2 U^2) - kappa sigma/(R U).
```

Keeping the old matter-free H identity after adding source energy would be wrong. The integrated new identity passes; its nonzero source integral is about 1.99e-5 for the smaller budget and 3.98e-5 for the larger one.

The preparation retains the same two inherited scalar-momentum directions, fixed h=1/64, factor matrices, original physical cuts, inner mass value/rate, outer scalar velocity, and outer gravitational clock. It re-solves the mass equation and initial coefficients, and derives endpoint lapse slopes so P_t vanishes at the original cuts. The source is only at the outer band; the existing left seed adjustment therefore retains its linear integrating factor on the left half-band. No coefficient is chosen to minimize C1.

An independent verification integrates the equation for U instead of mu:

```text
U_R = (1-U^2)/(2 R U) - kappa U epsilon/R - kappa sigma/R.
```

This checks the different gravitational weighting of scalar and source energy through a separately parameterized radial ODE.

## 4. Why the added force need not break first-order conservation

At P=0 the source has no direct mu_t contribution. The existing action current still gives

```text
mu_t = -kappa U Kbar/N.
```

For one driven layer node, with q=chi_t=N U p/R^2,

```text
delta e_t = p rho/R^2,
E_t = -lambda q,
U delta e_t + E_t = 0,             rho=N lambda.
```

Multiplying by the fixed layer density gives U delta epsilon_t + sigma_t=0. This is the missing work accounting. The current's free scalar identity extends to

```text
Kbar_R + 2 g_R Kbar + N U epsilon_t + N sigma_t = 0.
```

In detail, differentiating the local lapse constraint and retaining the transport-connection contribution gives

```text
C1_local = partial_t[mu_R/(kappa U)-U epsilon-sigma] - Kbar g_R/N
         = -(Kbar_R + 2 g_R Kbar + N U epsilon_t + N sigma_t)/N.
```

The source term in mu_R cancels from the intermediate geometric coefficient; it does not license dropping sigma_t. Numerical tests use the unrestricted weak form over the original annulus, with its actual radial boundary terms, six nonvanishing test polynomials, and two quadratures. They do not replace the physical cuts by closed outer support ends.

There is also lapse work. For a source with H_app=N E at P=0,

```text
(H_app)_t = N_t E - rho q.
```

Thus rho q is exchanged scalar/source power; N_t E is metric work. These cannot be conflated with a conserved source-free mechanical energy. No infinite reservoir or free energy is being silently assumed.

## 5. Match the specified acceleration through source-clock data

Only the inherited outer scalar acceleration and gravitational clock history are used. As previously, the old inner scalar acceleration is not reused after re-preparation changes its velocity. No unsourced second derivative of the inner mass drive is imposed.

At the physical outer cut,

```text
C_clock = N/U,
N_t/N = (C_clock)_t/C_clock - mu_t/(R U^2),
D_z'(0) = q(z,0)/N(z,0),
D_0''(0) = [a_prescribed-(N_t/N) q]/N^2.
```

The full declared source profile for this pilot is

```text
D_z(theta) = chi(z,0) + [q(z,0)/N(z,0)] theta + (1/2) D_0''(0) theta^2.
```

Its constant proper-acceleration extension across the collar is a **modeling choice**, not a derived uniqueness result. For the first metric time derivative the pilot extends N_t/N as a spatial constant normalized to the sourced outer clock derivative; this is likewise declared rather than inferred from the missing full time history.

Comparing the scalar kinetic equation with chi=D_z(theta) yields the reaction at the prepared slice:

```text
Delta_a(z) = N^2 D_0'' + mu_t q/(R U^2) - (N U/R^2) p_t,free,
rho(z) = omega_node R^2 Delta_a(z)/(N U),
lambda(z) = rho(z)/N.
```

The common N_t q/N term cancels in this reaction equation. At z=0 the sourced clock converts the proper trajectory back to the specified physical coordinate acceleration. The external target, not C1, fixes this trajectory; C1 then checks its energy and metric accounting. A recovery test is therefore meaningful for consistency but **not an independent prediction of acceleration or a measurement of an MTS coupling**.

The two prescribed initial source energies, E_0=0.001 and 0.002, are internal-fixture apparatus budgets, not fitted fundamental constants. All quantities retain the archived fixture normalization; no SI observation is claimed. Positive energy is checked initially only. The clock model must be stopped or supplemented if that energy is exhausted.

## 6. Actual results

Eight cases: GR and metric_Gram (the MTS control), each with beta22 at widths h/2 and h/4 and beta23 at h/2 for E_0=0.001; both branches also run beta22,h/2 with E_0=0.002. All initial root preparations converge.

| Quantity | Maximum absolute error |
|---|---:|
| Preserved initial boundary data | 4.45e-16 |
| Source-inclusive C0 | 1.027e-14 |
| Source-inclusive C1 | 3.43e-16 |
| Local source/scalar energy exchange | 1.78e-15 |
| Prescribed acceleration recovery | 4.17e-16 |
| Off-shell source-action variation | 2.72e-19 |

Errors are rounded upward from recorded maxima. These are floating-point fixture checks, not uniform or interval-certified theorems.

Representative beta22,h/2,E_0=0.001 results:

| Branch | Free acceleration | Driven acceleration | Scalar generalized force | Source E_t |
|---|---:|---:|---:|---:|
| GR | -1.2602853882 | 0.05577372039 | 0.5728365452 | -0.01071164236 |
| MTS | -1.2539464387 | 0.05577372039 | 0.5700777952 | -0.01066005924 |

The target was 0.05577372038655635. Free acceleration still fails in every case; this has not been relabeled a free-boundary success.

Useful negative controls:
- Leave out initial apparatus energy: C0 errors 0.0005–0.001; the asymmetric half-band contribution is 0.0006875 at the smaller budget.
- Add scalar force without source energy loss: C1 errors 0.00512–0.00705.
- Let the source lose energy without the scalar force: the opposite uncancelled C1 term remains.
- Set E(0)=0 while requiring this positive work: E_t(0)<0, hence any differentiable continuation has negative E for sufficiently small positive time. This is not an admissible positive-energy repair.

The reported E_0/(-E_t) values, roughly 0.084–0.169 in fixture time units, are **instantaneous budget-to-loss ratios**, not predicted lifetimes; rates and geometry have not been evolved. The source has a nonzero direct metric second-time-derivative term, with maxima about 8.27e-7–3.24e-6 across cases. Discarding it because the first source metric force vanishes at P=0 would be an error.

Layer-shape dependence persists: the unprescribed outer mass rate is still about 38% different between the two shape choices. Successful C0/C1 cancellation does not select a physical regularizer or a source profile. Nor does agreement of these forced GR/MTS checks establish equality of their source-free dynamics.

## 7. Next calculation and honest stopping point

The next concrete calculation is the **coupled second-order initial jet**, keeping the canonical apparatus fields. Differentiate the scalar force and transported current, derive P_tt and the needed clock derivatives, retain the source metric Hessian and E_tt=-lambda_t q-lambda q_t, and evaluate the full C2 and remaining boundary-history conditions in both controls. This requires the parent transport variations; a frozen-memory replay cannot replace it.

The already declared D_z supplies a proper-clock trajectory, but the full gravitational clock/lapse continuation, radial support stresses, and global port matching are not completed here. A short evolution and a positive-energy interval may follow only after the needed compatibility conditions are actually tested. Do not advertise the apparatus as a unique derived field or erase its modeling choices in order to promote the result.

All full-GR/full-first-jet/full-C2/global-evolution flags remain false. The narrower result is concrete: an action-level proper-clock source can provide the previously missing boundary force **with its initial gravitational and energy-transfer cost accounted for**.

## 8. Evidence

- Predecessor seal: `source-intake/navier-stokes/20260913/annular-collar-response-final-integrity.json`.
- Original prepared-case ledger: `source-intake/navier-stokes/20260913/annular-finite-width-boundary-cut-attempt01/status.json`.
- GR prescribed-history owner: `source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/canonical_N16_GR_sample0.npz`.
- MTS prescribed-history owner: `source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/canonical_N16_metric_Gram_sample0.npz`.
- Source-coupled preparation and initial response: `scripts/annular_clock_reservoir_coupling_20260913.py`.
- Executed runner: `scripts/derive_annular_clock_reservoir_coupling_20260913.py`.
- Completed matrix, 81 main checks, arrays and hashes: `source-intake/navier-stokes/20260913/annular-clock-reservoir-coupling-attempt01/status.json`.
- Independent verifier: `scripts/verify_annular_clock_reservoir_coupling_20260913.py`.
- Verification completion and immutable source/output hashes: `source-intake/navier-stokes/20260913/annular-clock-reservoir-coupling-final-integrity.json`.

The verifier additionally checks finite worldline time reparametrization, the independent U equation, the nonzero source metric Hessian, explicit lapse work, and the zero-budget control. Read its final state for completion; this note is sealed, not rewritten after execution. The original workbench is checked for modified file times since 2026-09-13T10:28:20Z, not by a pre-turn hash baseline. All computation is single-worker, below-normal priority, and single-core; no prior executed evidence is altered.
