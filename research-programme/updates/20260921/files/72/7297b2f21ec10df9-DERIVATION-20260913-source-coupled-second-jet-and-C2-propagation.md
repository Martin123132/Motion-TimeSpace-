# Source-coupled second jet and C2 propagation

Private continuation, 2026-09-13. Formal local time expansion, not an evolved spacetime.

## 1. Result

The finite-width action with the explicit proper-clock apparatus now has a constructed second-order initial jet. The calculation differentiates the actual transported scalar force and current, includes the gravitational and apparatus momentum-squared terms, and determines the next source reaction and energy-transfer rates. It does not iterate the old frozen oscillator surrogate.

All eight GR/MTS source-coupled preparations pass the full tested weak C2 rows at both quadratures, with maximum absolute residual 1.037e-14 against the unchanged 1e-10 gate. Derived lapse-rate slopes also give P_tt=0 at both physical cuts, to below 1.21e-20. The constant-lapse-rate controls pass C2 but fail that boundary condition by about 0.349: constraint propagation and boundary compatibility are genuinely separate checks.

This establishes a **conditional formal second jet for the candidate action and apparatus**. It does not establish a causal initial-value problem, a solution on a finite time interval, a complete GR reduction, a physical apparatus with derived support stresses, or the original prescribed boundary problem at every time order.

Predecessor: `DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md`.

## 2. Notation and the non-frozen equations being differentiated

All time derivatives below are physical coordinate-time derivatives at the initial slice. A subscript 1 or 2 denotes one or two such derivatives; R denotes a radial derivative. P is gravitational momentum, p scalar auxiliary momentum, and L=N_1/N. Initial P=0, but P_1 is generally nonzero inside the annulus.

The coframe, scalar coefficient, and source clock are

```text
U=sqrt(1-2 mu/R),  d_metric=1-kappa^2 U^4 P^2,
c=kappa U P/(N d_metric),  C=R^2 N U d_metric,
ell=N sqrt(d_metric).
```

The full transported scalar block has metric covectors

```text
G_y = K c_y - W C_y,       W=epsilon/R^2 on the initial slice,
mu_t=(H_gravity)_P-G_P+(H_app)_P,
P_t=-(H_gravity)_mu+G_mu-(H_app)_mu.
```

Here W is the finite-width density obtained from the live kinetic and transported potential coefficients, not a frozen external energy profile. The apparatus contributes H_app=ell sigma on its scalar constraint. The gravity momentum terms are retained from the existing full action rather than adding the old local scalar/shift cross term a second time.

Owners of the full covectors and gravity terms:
- `DERIVATION-20260912-nonlinear-history-Euler-equations.md`.
- `DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md`.

At P=0, the preceding preparation gives

```text
mu_R=kappa(U^2 epsilon+U sigma),
P_1=-N_R/(kappa U)+N mu/(kappa R^2 U^3)+N epsilon/(R U),
a=c_t=g_R=kappa U P_1/N,
mu_1=-kappa U K/N.
```

The density epsilon_1 includes the new scalar source force; sigma_1 includes the apparatus energy loss. They must be differentiated as a coupled pair.

## 3. Derive P_2 and c_tt, then fix the boundary slopes

Define f(mu,N,N_R,epsilon) as the displayed expression for P_1. Differentiating the full metric covector, not treating f as an all-time equation restricted to P=0, gives

```text
P_2 = L P_1 - N L_R/(kappa U) + f_mu mu_1
      + N epsilon_1/(R U) + mu_1 P_1/(R U^2),

f_mu = -N_R/(kappa R U^3) + N/(kappa R^2 U^3)
       + 3N mu/(kappa R^3 U^5) + N epsilon/(R^2 U^3).
```

The final term comes from K(c_mu)_1. Simply differentiating the restricted P=0 lapse formula would miss it. The apparatus has no direct contribution to P_2 from ell_mu here because ell_mu is quadratic in P; its changes to the initial geometry and epsilon_1 remain included.

The connection's second time derivative simplifies to

```text
h=c_tt=kappa U/N [P_2-2(L+mu_1/(R U^2))P_1]
       =mu_1/(R^2 U^4)+kappa epsilon_1/R-L_R-L g_R.
```

At a physical cut where P_1=0, the required P_2=0 condition is therefore

```text
L_R|cut = mu_1/(R^2 U^4)+kappa epsilon_1/R.
```

The outer value L_out remains fixed by the already sourced clock derivative:

```text
L_out=(C_clock)_1/C_clock-mu_1/(R U^2),  C_clock=N/U.
```

With x=(R-L_cut)/span, retain a simple declared extension

```text
L(R)=L_out+A_L span x(1-x)^2+A_R span x^2(x-1).
```

Its slopes at the two cuts are A_L and A_R, so these coefficients are set by the derived boundary formulas, not by a C2 fit. Both added shapes vanish at the endpoints. This corrects the previous constant spatial L extension without altering the initial fields, first mass rate, outer scalar acceleration, or source proper-clock trajectory. It is not a theorem selecting a unique interior lapse profile.

## 4. Differentiate the inverse-time transport, including its second map

For each layer translation and factor anchor, let J_i=T_i,s and B_i=T_i,ss at s=0. To avoid conflating this B_i with the spatial factor matrix, write the latter as B_factor. If b_R=h exp(g), then

```text
J_i=exp(g_i-g_anchor),
B_i=exp(g_i-2g_anchor)[b_i-b_anchor].
```

This solves J_R=aJ and B_R=aB+hJ^2. The arbitrary additive constant of b cancels. It is a transport primitive, not a new clock or coupling parameter.

Let A=sum B_factor,i chi_i, D=sum S_i J_i C_i. Then

```text
A_1=sum B_factor,i J_i q_i,
A_2=sum B_factor,i [B_i q_i+J_i^2 q_1,i],
D_1=sum S_i [B_i C_i+J_i^2 C_1,i],
C_1/C=L-mu_1/(R U^2),
q_1=(L-mu_1/(R U^2))q+(NU/R^2)p_1.
```

At fixed physical node time the differentiated scalar force and potential coefficient are

```text
(Gchi_i)_1 = -sum_f B_factor,fi/(h_spacing J_fi^2)
             [A_1 D+A D_1-A D B_fi/J_fi],

(d_i)_2 = sum_f S_fi/h_spacing
          [(A_1^2+A A_2)/J_fi^2-A A_1 B_fi/J_fi^3].
```

Here B_fi denotes T_fi,ss, not the factor weight. The inverse-map factors are essential: differentiating at the anchor and calling it a physical-time derivative is incorrect.

For the old pair current I=A(S C_i A_1-B_factor,i q_i D)/h_spacing, obtain I_s by the product rule with these live coefficient and acceleration derivatives. At a radial evaluation point R, differentiating the full inverse-time current yields

```text
K_1(R)=exp(-3g(R)) integral dz w(z) sum_pairs orientation_indicator
       {exp(g_i+2g_anchor) I_s
        +exp(g_i+g_anchor) I [b_i+b_anchor-2b(R)]}.
```

The third inverse Jacobian and the derivative of the evaluation-point map are retained. Split-layer direct integration independently checks this against the stored primitive representation; a separate transport ODE checks J and B.

## 5. A compact mass-acceleration law

Before simplification, differentiating the metric equation gives

```text
mu_2 = -kappa U/N [K_1-(L+mu_1/(R U^2))K]
       + [V_gravity-2kappa^2 N U^5 epsilon-kappa^2 N U^4 sigma] P_1,

V_gravity=kappa R U^3[U^2 N_R+N mu_R/R-N mu/R^2].
```

The last source term is precisely the apparatus metric Hessian found in the preceding stage. Substituting the initial mass constraint and P_1 equation reduces the square bracket to -kappa^2 R U^6 P_1. Therefore

```text
mu_2 = -kappa U/N [K_1-(L+mu_1/(R U^2))K]
       -kappa^2 R U^6 P_1^2.
```

This simplification does **not** mean apparatus gravity can be omitted: the cancellation uses its contribution to both mu_R and the explicit metric Hessian. The main runner checks the unsimplified and reduced algebra.

## 6. Source reaction rate and the N_2 cancellation

The previously declared proper trajectory is quadratic, so D'''=0. Set

```text
v=mu_1/(R U^2),
w_mu=mu_2/(R U^2)+mu_1^2/(R^2 U^4),
t_P=kappa^2 U^4 P_1^2.
```

Differentiating chi=D(theta), theta_t=ell, and the kinetic equation gives the required driven p_2 at the source:

```text
(NU/R^2)p_2 = 3D'' N^2 L+q(2Lv+w_mu+t_P)
              -2(L-v)(NU/R^2)p_1,
rho_1=omega_node p_2-(Gchi)_1,
lambda_1=(rho_1-L rho)/N,
E_2=-lambda_1 q-lambda q_1.
```

Terms containing N_2 cancel between the kinetic relation and the proper-clock trajectory. N_2 is therefore not needed to determine this reaction rate or C2. It remains relevant to a complete lapse/clock history and to the numerical value of the scalar third coordinate-time derivative. The verifier tests the cancellation with two independent N_2/N choices rather than declaring N_2=0 physically.

For all other scalar nodes p_2=(Gchi)_1/omega_node. The live energy second derivative is

```text
e_2=omega_node(p_1^2+p p_2)/R^2+R^2 d_2,
```

followed by the unchanged finite-width radial-density map. This preserves the distinct layer fields and the source energy balance.

## 7. Full C2 and its conditional interior identity

The complete local lapse equation, before radial boundary terms, is

```text
C_gravity = mu_R/(kappa U)
 + kappa U^3[(U^2/2-3mu_R+3mu/R)P^2+R U^2 P P_R],
C_total = C_gravity-U d_metric epsilon-sqrt(d_metric) sigma+K c_N.
```

Its second derivative includes the mass/energy product derivatives and all of

```text
gravity P^2 and P P_R terms,
+2kappa^2 U^5 epsilon P_1^2,
-sigma_2+kappa^2 U^4 sigma P_1^2,
K(c_N)_2+2K_1(c_N)_1
  =-K h/N+2L K g_R/N-2K_1 g_R/N.
```

The unrestricted weak implementation retains the radial terms from integrating mu_R and the inherited P-squared boundary action. The latter has zero second derivative on these prepared P_1=0 endpoints; it is not omitted from the formula. Six test functions nonzero at the boundaries are evaluated at radial quadrature orders 24 and 40.

The differentiated transport/source Ward identity is

```text
(K_1)_R+3g_R K_1+2hK
 +NU(L-mu_1/(R U^2))epsilon_1+NU epsilon_2
 +NL sigma_1+N sigma_2=0.
```

The verifier substitutes the initial mass constraint, the derived metric equations, and both Ward identities into the complete local C2 expression and checks exact symbolic reduction to zero. This is a **conditional smooth-interior algebraic identity**, not a causal-existence theorem. The numerical radial and boundary tests supplement it; they are not replaced by an appeal to covariance.

These formulas assume a sufficiently regular two-sided time germ around the slice for the inverse maps. They do not silently remove temporal action-boundary terms at the edge of a one-sided evolution.

## 8. Measured checks and surviving limitations

The eight cases and apparatus budgets are unchanged from the previous stage. Main run: 39 checks; all eight weak C2 and endpoint P_2 gates pass. Exact independent-verification completion is recorded in the final integrity file, not inferred from this note.

| Result | Maximum absolute value |
|---|---:|
| Weak C2 residual, both quadratures | 1.037e-14 |
| Differentiated local Ward residual | 2.963e-12 |
| P_2 at the physical cuts | 1.21e-20 |
| Difference between the two weak C2 quadratures | 1.111e-14 |
| Error fitting the transport primitive derivative | 6.842e-14 |

These are floating-point checks on the fixture, not interval certificates or continuum-limit error bounds. Independent force/time-map/current checks and the symbolic identity are recorded separately by the verifier.

Negative controls retain errors rather than redefining a pass:
- Constant spatial L: endpoint P_2 errors 0.34937 (GR), 0.34923 (MTS), although C2 itself remains near 1e-15.
- Omit source second-order energy/chart terms: C2 errors 0.0880–0.1504.
- Omit transport-connection terms: 5.35e-6–3.91e-5.
- Omit the tested gravity/scalar momentum-squared terms: 8.87e-6–2.46e-5.
- Omit radial boundary contributions: 0.1098–0.1938.

### The remaining source-history issue is concrete

For beta22,h/2,E_0=0.001 the compatible derivatives are

| Output in fixture units | GR | MTS |
|---|---:|---:|
| Required inner mass acceleration | 0.0166881251 | 0.0153455862 |
| Outer mass acceleration | 0.0078530781 | 0.0058727706 |
| Source force derivative at outer cut | 9.52539661 | 7.20473640 |
| Source energy second derivative at outer cut | -0.21705060 | -0.17346844 |

The inner mass acceleration is **derived output**, not a sourced common prescribed value. If an affine inner mass history with zero acceleration were imposed, these preparations would not satisfy it. One cannot compare subsequent GR/MTS evolution as a matched experiment while silently giving them these different boundary histories.

The original prescribed outer scalar acceleration and first boundary data remain matched. Layer-profile dependence persists, and the source now has an explicitly calculated changing energy-loss rate. No positive-energy time interval, apparatus lifetime, or evolved solution is claimed from the Taylor coefficients.

## 9. Next step

First reconcile the required inner mass acceleration with a declared **common source-history contract**, retaining the remaining exterior/source freedom rather than changing a boundary number separately for each theory. Determine the gravitational clock history to the order needed for that contract. Then attempt a small, saved time-slab or history-consistent evolution test with all temporal endpoint work and source energy retained; do not pretend the history action is already a causal ordinary ODE.

Do not restart blind mode enlargement or fit C2 after this result. The second-order constraint machinery now has a derived identity and passing finite-width checks. The remaining work is boundary-history matching, interval existence/evolution, and the still explicit regulator/apparatus assumptions. Global GR recovery and the physical MTS parent theory remain unproved.

## 10. Evidence and preservation

- Starting seal: `source-intake/navier-stokes/20260913/annular-clock-reservoir-coupling-final-integrity.json`.
- Starting preparations: `source-intake/navier-stokes/20260913/annular-clock-reservoir-coupling-attempt01/status.json`.
- Full second-jet construction: `scripts/annular_source_second_jet_20260913.py`.
- Executed matrix runner: `scripts/derive_annular_source_second_jet_20260913.py`.
- Completed arrays, controls and hashes: `source-intake/navier-stokes/20260913/annular-source-second-jet-attempt01/status.json`.
- Independent algebra/transport verifier: `scripts/verify_annular_source_second_jet_20260913.py`.
- Verification authority: `source-intake/navier-stokes/20260913/annular-source-second-jet-final-integrity.json`.

All earlier executed evidence remains immutable. No GitHub action, subagent, or full geometric evolution is performed. Computation uses one below-normal-priority, single-core Python worker at a time. The protected original workbench check is an mtime scan since 2026-09-13T11:03:10Z, not a pre-turn content-hash baseline. The final resume snapshot precedes any final completion line added to the mutable resume.
