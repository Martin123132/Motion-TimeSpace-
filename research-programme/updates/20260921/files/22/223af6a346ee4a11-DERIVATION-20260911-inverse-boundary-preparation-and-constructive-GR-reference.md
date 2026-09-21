# Inverse boundary preparation and a constructive GR reference

Private working derivation, 11 September 2026. No publication or evolution claim.

## 1. What actually changed

The previous fixed boundary test prescribed an inner mass velocity, scalar velocity and scalar gradient that did not obey the necessary classical flux law. This checkpoint **implements** an inverse boundary preparation: retain the mass drive, derive the inner scalar velocity, and retain the full MTS Gram correction. It also derives and imposes the natural outer clock normalization.

The resulting MTS N16 finite system converges. The GR finite system still does not. Rather than interpret that failure as physical, a separate integrating-factor construction now produces compatible GR-plus-canonical-scalar initial data directly. An exact rational bound proves that this formula-defined reference remains in the positive metric chart throughout the annulus.

These are genuine constructions, but not a classical MTS solution, a completed GR limit, or time evolution. The new MTS finite root still has boundary-reaction and spatial-profile defects.

Predecessor: `DERIVATION-20260911-nonlinear-mass-elimination-and-boundary-flux-compatibility.md`.

## 2. Boundary action and independent controls

Use the existing canonical branch: kappa=1/10, Lambda=m_chi=b2=b3=0, initial P=0, F=1-2mu/R. This is GR **with a canonical scalar**, not vacuum GR. No universal value of Newton's constant is derived here.

The bulk spatial mass derivative has coefficient N/(kappa sqrt(F)). After integration by parts, its boundary variation is

```text
[N delta_mu/(kappa sqrt(F))]_inner^outer.
```

The retained outer action is -C_out mu_out/kappa. If outer mass is free, regular first variations require

```text
N_out/sqrt(F_out) = C_out.
```

Inner mass history is Dirichlet; its first time derivative is an external preparation, not a theory-predicted parameter. Inner scalar configuration at the initial instant remains fixed, but its first time derivative is now an unknown compatible drive. Outer scalar velocity remains prescribed. There is no new P-linear boundary source and the P-squared boundary action still has zero first variation at P=0.

For unrestricted boundary tests with regular one-sided momentum rates, the corresponding spatial reaction cancellations are

```text
lambda_mu,in = N_in/(kappa sqrt(F_in)),
lambda_chi,in = -R_in^2 N_in sqrt(F_in) w_in - Gchi_in,
lambda_chi,out = +R_out^2 N_out sqrt(F_out) w_out - Gchi_out.
```

Here w=chi_R; Gchi is the already retained Gram scalar covector, zero for the GR control. These reaction cancellations are **additional diagnostics**, not asserted consequences of a small finite residual. Boundary distributions, full time-link endpoint variations and higher time compatibility would need separate treatment if regular traces are abandoned.

## 3. Derived inverse flux condition

The predecessor derived the inner one-sided Gram force, including orientation and all time-link Jacobians:

```text
GP_in = -kappa sqrt(F_in) q_in Gchi_in/N_in.
mu_t,in = kappa R_in^2 F_in q_in w_in - GP_in.
```

Thus, setting

```text
D_in = kappa R_in^2 F_in w_in + kappa sqrt(F_in) Gchi_in/N_in,
v_in = D_in q_in,
```

derives q_in=v_in/D_in whenever D_in is nonzero. For MTS, D_in depends on the unknown geometry and momentum-rate/time-link jet; this is an **implicit compatibility equation**, not an independent explicit solution or uniqueness theorem. Positive Gram energy does not imply a universal sign for D_in.

Implementation uses the product equation, divided only by the fixed nonzero GR trace coefficient for row units. The old prescribed q_in no longer enters any equation. This is checked by changing it and obtaining bit-identical residuals. Changing the mass drive affects exactly the mass-velocity and inverse-compatibility rows; changing the outer scalar drive affects exactly its retained row.

Unknowns remain n free mass faces, n scalar momentum nodal coefficients and three reactions: 2n+3. Equations remain n mass constraints, n constraint-rate equations and three boundary equations. Original scalar configuration, initial inner mass and free momentum correction coefficients are unchanged. The previous q_in Dirichlet first-jet row is replaced, not retained alongside an extra incompatible condition. The initial inner scalar history is only prepared to first order; no full inverse boundary initial-boundary-value theorem is claimed.

Primary lapse prescription:

```text
N(R) = N_seed(R) C_out sqrt(F_out)/N_seed,out.
```

This preserves the chosen spatial lapse shape and derives its overall clock normalization. It is an explicitly chosen gauge/profile preparation, not a derivation of that entire profile. Its mass-dependent derivative is included in every Newton column. The frozen canonical pairing maps remain frozen; the mass constraint itself is unchanged by this lapse normalization.

## 4. Paired finite solve: actual results

Same external mass drive for both branches: 0.00033578281226508903. N16 means 16 intervals and 17 scalar nodes. Original converged N16 archives are starting guesses, not failed N64 iterates. Full nonlinear mass elimination is retained at every trial.

| Case | Outcome | Updates | Maximum full residual |
|---|---|---:|---:|
| GR, fixed-lapse diagnostic control | Not converged | 35 | 6.89805e-6 |
| MTS Gram, fixed-lapse diagnostic control | Converged | 16 | 2.37170e-15 |
| GR, natural outer-clock normalization | Not converged | 35 | 5.61015e-6 |
| MTS Gram, natural outer-clock normalization | Converged | 16 | 1.69749e-15 |

The fixed-lapse controls intentionally do not satisfy the natural outer clock; they isolate the normalization change and are not acceptable classical boundary preparations. Both GR failures are iteration-limit outcomes, not nonexistence proofs. N32 was not run because both primary N16 branches were required to converge before refinement.

For the primary MTS root:

- Derived q_in=-0.009858752205907272; old fixed value was -0.009795654033278759.
- Full GP_in=2.8754758024260325e-6; omitting it is detectably wrong.
- Combined flux trace gap: 5.96e-19. Actual local canonical EP trace gap: -1.37701e-11.
- Endpoint scalar Legendre trace gaps: approximately +4.009e-10 and -3.980e-10. These are not identical to the finite projection equations.
- Outer clock gap: zero to reported floating precision; lapse normalization 0.9999782491955296.
- Spatial boundary-reaction gaps: approximately (-0.10779194, -0.00366835, -0.01026569). **They do not vanish.**
- Sampled pi total variation is 8.4003; sampled bulk constraint L2 is 0.0020811, excluding Gram point/nonlocal contributions. No spatial convergence is demonstrated.

Both converged roots survive independent small perturbation/re-solves, returning within 7.12e-12 in coefficients. Final-state projected directional derivative errors are below 3.52e-12. Omitting the clock response changes Jacobian entries by approximately 1.0e-5, and is detected. Both GR failures receive the same derivative checks.

## 5. Constructive GR reference: no finite Newton solve

The reference fixes the original N16 scalar configuration and positive continuous lapse shape N0(R). It uses the original Hermite scalar velocity with a single **whole-annulus** smooth lift:

```text
x=(R-R_in)/(R_out-R_in),
q(R)=q_original(R)+(q_in,required-q_original,in)*(1-3x^2+2x^3),
q_in,required=v_in/(kappa R_in^2 F_in w_in).
```

The lift has zero endpoint derivatives, preserves the original outer scalar velocity and has fixed physical width. It is a declared free initial scalar-velocity profile, not a new coupling or a grid-sized layer. It changes the free interior momentum profile; consequently this construction is **not** a root of the old frozen-momentum-correction finite system.

Let N=sigma N0, y=sigma^2. The scalar Legendre equation gives pi=R^2 q/(N sqrt(F)). Substituting this into the mass constraint yields a linear radial equation:

```text
mu_R + p(R) mu = a0(R) + b0(R)/y,
p=kappa R w^2,
a0=kappa R^2 w^2/2,
b0=kappa R^2 q^2/(2 N0^2).
```

Define A_R+p A=a0, A_in=mu_in; B_R+p B=b0, B_in=0. Integrating factors construct these functions directly, and mu=A+B/y. At the outer boundary, set K=C_out^2/N0,out^2 and Fa=1-2A_out/R_out. The natural clock is precisely the quadratic

```text
y^2 - K Fa y + 2 K B_out/R_out = 0.
```

We select the larger positive root, continuously connected to the finite positive-lapse branch when scalar velocity is scaled to zero. This choice is made analytically, not by which fit converges. The other root is reported and has F_out approximately 3.17818e-5, outside the predeclared F>.1 chart.

Numerical construction gives:

```text
q_in = -0.00977504362882812,
sigma = 0.9999998831754183,
max|C| = 6.94e-18,
max|C_t| = 8.33e-17,
inner flux gap = 0, outer clock gap = 0 (reported floating precision).
```

Integrating-factor quadrature at orders 8/12/16 agrees; an independent DOP853 solution agrees in A,B within 2.23e-16. These comparisons are not outward-rounded enclosures of numerical quadrature.

### Exact whole-annulus positivity, not just sampling

Quadratic Bernstein coefficients bound w; cubic Bernstein coefficients bound q_original. The global lift lies in [0,1]. With W>=|w|, Q>=|q|, Nmin<=N0 and length L:

```text
0 <= A <= R/2,
A <= Amax = mu_in + kappa R_out^2 W^2 L/2,
0 <= B <= Bmax = kappa R_out^2 Q^2 L/(2 Nmin^2).
```

The exact rational bounds give positive Fa_min and discriminant lower bound. Consequently the large root obeys y>=K Fa_min/2. Thus

```text
mu <= Amax+Bmax/y_min,
F >= 1-2*(Amax+Bmax/y_min)/R_in > 0.65933098,
N^2 >= y_min Nmin^2 > 0.32972126.
```

All inequalities are checked using fractions, with full numerators/denominators retained. They prove the positive chart for the **exact formula-defined reference**, using stored binary polynomial data and an exactly derived rational q_in. They do not enclose all rounding errors of the numerical samples, and are not a spacetime existence certificate.

## 6. Why this helps diagnose the finite failure

For the unprojected GR canonical first jet at P=0,

```text
mu_t=kappa N F^(3/2) pi w,
q=N sqrt(F) pi/R^2,
pi_t=(N sqrt(F) R^2 w)_R,
P_t=N H/(R sqrt(F))-N_R/(kappa sqrt(F))+N mu/(kappa R^2 F^(3/2)),
H=pi^2/(2R^2)+R^2 w^2/2.
```

Substituting these expressions into the full canonical C_t, including its P_t term, cancels identically. The new symbolic check is off shell at P=0: it does not require an initial C=0 substitution. The integrating-factor construction separately supplies C=0. The source profiles are piecewise smooth, chi/q are C1 and the lapse is continuous P1; this is a compatible initial first jet, not a globally smooth evolving spacetime.

This shows that the repaired boundary drive admits a constructive GR reference. It does **not** prove that the finite solver must converge on its different free-data slice, or identify every finite obstruction. Nor should its excellent strong GR residual be scored against an MTS finite residual as though these were identical tests. Its proper role is a non-fitted control for the spatial/canonical representation.

## 7. Concrete next step

Use this formula-defined GR first jet as a manufactured control for the existing canonical discretization. Reconstruct its fields consistently, derive the actual projection and boundary-reaction defects, and repair the specific discrete compatibility failure through the action/test spaces rather than searching for increasingly oscillatory initial momenta. Any proposed repair must pass this control and then the paired full-Gram test with unchanged boundary protocol. Do not silently smear the Gram point/nonlocal covectors into a GR energy density.

Then require refinement and endpoint-reaction/Legendre control before evolving. Higher boundary jets also follow a definite law: v_t=D_t q+D q_t, so q_t=(v_t-D_t q)/D when the relevant coupled jet is known and D is nonzero. The outer clock derivative requires N_t,out=C_t,out sqrt(F_out)-C_out mu_t,out/(R_out sqrt(F_out)). Neither complete time jet is solved in this checkpoint.

## 8. Reproduction and evidence

Scripts, in order:

- `scripts/annular_canonical_inverse_boundary_20260911.py`
- `scripts/derive_annular_canonical_inverse_boundary_20260911.py`
- `scripts/derive_annular_canonical_gr_boundary_reference_20260911.py`
- `scripts/verify_annular_canonical_inverse_boundary_20260911.py`
- `scripts/verify_annular_gr_reference_global_chart_20260911.py`
- `scripts/seal_annular_canonical_inverse_boundary_20260911.py`

Saved reports:

- `source-intake/navier-stokes/20260911/annular-canonical-inverse-boundary-attempt01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-gr-boundary-reference-attempt01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-inverse-boundary-control-attempt01/status.json`
- `source-intake/navier-stokes/20260911/annular-canonical-gr-reference-global-chart.json`

Use a fresh attempt directory; completed evidence is immutable. All work stays private in post-checkpoint-work. One BelowNormal single-core Python at a time; no subagents, GitHub, frozen-workbench or galaxy edits. No failed state is evolved and no worker is left running at finalization.
