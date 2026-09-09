# Whole-star localization, smeared Hilbert stress and the static-limit gate

Private analytical companion, 2026-09-07. The live D4/5515 worker remains
the sole numerical worker. This does not change its parent or proof packs.

## Result and what is new

The previous trapped-energy estimate required global coefficient envelopes;
only a standalone Schwarzschild exterior example was supplied there.
Here those envelopes are derived for a **regular stellar interior joined
to its exterior**, using the same quadratic motion operator and TOV
background as the coupled calculation. No reflecting stellar surface,
zero bound-mode occupation, or phenomenological damping law is introduced.

For a fixed admissible background and fixed compact support of the initial
data, the result bounds the fraction of energy projected into the entire
below-mass spectral subspace by a constant times **m^4** as m tends to zero.
It does not infer a physical damping rate by extrapolating the numerical
alpha_G=0.02 example.

There is also a separate domain-of-validity gate: on a positive-Lambda
background the ground-state hydrogenic cloud is approximately static and
source-dominated only if H_Lambda/(m alpha_G^2) is small. Local weak gravity
alone does not ensure that a global bound-mode calculation is physical.

## 1. Explicit hypotheses and inherited operator

Use c=hbar=1, signature (-,+,+,+), mu=G_N M and areal radius r. Assume:

- A regular, static, spherical perfect-fluid star of radius R, with
  nonnegative pressure and energy density, decreasing outward to its surface.
- A barotropic equation of state with finite central enthalpy H_c, and a
  Schwarzschild exterior. The cosmological constant is zero in THIS
  spectral theorem; section 6 is a separate validity test for extending it.
- The selected quadratic motion equation, with m>0 and
  K_0=1+2u C^2>0. The fixed background is the chi=0 matter solution.
- The complete regular spatial slice, without an artificial inner boundary,
  and compactly supported finite-energy initial displacement and velocity.

As derived in `DERIVATION-20260906-parent-trapped-energy-bound.md`,

```text
L = -w^(-1) partial_i(A^{ij} partial_j) + N^2 m^2/K_0,
q[f] = integral [A^{ij} partial_i f* partial_j f
                 + N sqrt(h) m^2 |f|^2] d^3x.
```

In Cartesian coordinates associated with areal r,

```text
ds^2 = -N^2 dt^2 + a^2 dr^2 + r^2 dOmega^2,
a=(1-2 mu(r)/r)^(-1/2),  sqrt(h)=a,
w=K_0 a/N,
eigenvalues(A) = N K_0/a (radial), N K_0 a (twice tangential).
```

This coordinate distinction matters: the isotropic-coordinate factors in
the earlier exterior example must not be reused unchanged.

## 2. Source-owned global geometric envelopes

Write rho_c for the central TOTAL energy density, not rest density.
Let c_R=mu/R<1/2 and

```text
zeta = 2 [(4 pi G_N rho_c/3) mu^2]^(1/3) < 1,
a_max = (1-zeta)^(-1/2),
N_c = sqrt(1-2 c_R) exp(-H_c),
W_max = 48 (4 pi G_N rho_c/3)^2,
delta = 2 |u| W_max < 1.
```

The central-density upper bound is deliberately conservative. A failure of
zeta<1 or delta<1 makes these particular envelopes unavailable; it does not
prove that the exact star contains a horizon or a kinetic instability.

**Compactness.** Nonnegative density bounded by rho_c implies

```text
mu(r) <= min[(4 pi G_N rho_c/3) r^3, mu],
2 mu(r)/r <= zeta.
```

The maximum of the two intersecting power-law envelopes occurs at
r_0=[3 mu/(4 pi G_N rho_c)]^(1/3). Monotone density gives r_0<=R.
This supplies a global a_max, including any interior maximum of mu(r)/r;
the surface compactness alone would not supply that bound.

**Lapse.** The TOV hydrostatic equation is
dp/dr=-(rho+p) d(log N)/dr. Defining H(p)=integral_0^p dp/(rho+p) gives
N(r)=N(R) exp[-H(p(r))]. Thus N_c<=N<=1 on the entire slice.
For p=K rho_0^Gamma and rho=rho_0+p/(Gamma-1),

```text
H_c = log[1 + Gamma K rho_0c^(Gamma-1)/(Gamma-1)].
```

This is the same central-lapse relation already used by
`scripts/parent_O4_star_profile_20260907.py`. It is not an additional
time/gravity coupling.

**Weyl curvature.** For this isotropic perfect-fluid solution,

```text
C^2 = 48 [mu(r)/r^3 - 4 pi G_N rho(r)/3]^2.
```

The bracket equals (4 pi G_N/3)(mean_density_within_r-rho(r)).
Monotonicity bounds it between zero and 4 pi G_N rho_c/3; outside the star
rho=0 and the same upper bound applies. Therefore |K_0-1|<=delta globally.
This formula is not assigned to arbitrary anisotropic or time-dependent
matter. No matter perturbation or Hilbert-stress improvement is discarded
from the separate radiation calculation.

One direct check of the curvature formula uses an orthonormal frame.
Spherical geometry gives R_theta_phi_theta_phi=2mu(r)/r^3.
The perfect-fluid Einstein equations give
R_theta_theta=R_phi_phi=4pi G_N(rho-p) and R=8pi G_N(rho-3p).
The Weyl trace subtraction therefore gives
C_theta_phi_theta_phi=2[mu(r)/r^3-4pi G_N rho/3]: the pressure cancels.
The electric Weyl eigenvalues are (-2D,D,D) up to convention-wide sign,
with D equal to this bracket; spherical static symmetry eliminates the
magnetic part. Hence C^2=8(4+1+1)D^2=48D^2.

## 3. Fill the global coefficient contract

The following constants satisfy the contract in the earlier proof:

```text
kappa = N_c (1-delta)/a_max,
w_min = 1-delta,
w_upper = (1+delta) a_max/N_c,
theta_lower = N_c^2/(1+delta),

b_inside/m^2 = R a_max/N_c (1+delta-N_c^2),
b_outside/m^2 = [2 mu + 96 |u| mu^2/R^5]/(1-2 c_R),
b = max(b_inside, b_outside).
```

Indeed A>=kappa I and w_min<=w<=w_upper. Also
N^2/K_0>=theta_lower. Inside, multiplying
a(K_0-N^2)/N by r and taking its positive part gives at most
R a_max(1+delta-N_c^2)/N_c.

Outside, a=1/N, N^2=1-2mu/r and C^2=48mu^2/r^6, so

```text
r [w-Na]_+
 <= [2mu + 96 |u| mu^2/r^5]/(1-2mu/r)
 <= [2mu + 96 |u| mu^2/R^5]/(1-2mu/R).
```

Consequently m^2(w-Na)<=b/r everywhere. All constants are functions of
geometry, matter data and the retained coefficient u, rather than arena
fit parameters. kappa, w_min, w_upper and theta_lower are dimensionless;
b has dimension inverse length. G_N is the existing calibrated constant.

## 4. Derived suppression without orthogonality preparation

Let P_b=1_[0,m^2)(L), and let both initial data have support in a ball of
radius ell. The Hardy/Sobolev proof in the preceding document applies to
this regular whole-space operator with C_S=4. Define

```text
epsilon_ell = (8 b/kappa) sqrt(w_upper/w_min) (4 pi/3)^(1/3) ell,
E_b/E_total <= min[1, epsilon_ell^2 max(1, theta_lower^(-1))].
```

This controls ALL below-threshold modes and all localized initial data in
the stated energy class, not one chosen eigenfunction. The numerical
companion checks these conservative coefficient envelopes against the
same source-owned stellar profile; the analytic inequalities, not samples
alone, give the conditional uniform result.

At fixed background, u and ell, b is exactly proportional to m^2.
The unsaturated energy bound is therefore proportional to m^4. Writing
b=B mu m^2, alpha_G=mu m and a_B=1/(mu m^2),

```text
epsilon_ell = [8 B/kappa sqrt(w_upper/w_min) (4 pi/3)^(1/3)] ell/a_B.
ell=R:  R/a_B = alpha_G^2/c_R.
```

Thus fixed compactness and fixed dimensionless geometry give an
alpha_G^4/c_R^2 energy-fraction bound, with the explicitly displayed
coefficient. It is not a universal numerical coefficient or an exact
zero of occupation. The cutoff min(1,...) prevents a large bound being
mistaken for a useful suppression.

Energy in P_b is conserved only for the fixed quadratic evolution.
The already derived nonlinear feeding integral remains necessary when
interactions are restored. Pointwise stress/PPN estimates require further
regularity and the full metric response; an L2/energy estimate is not itself
a pointwise bound on the O4 Hilbert stress.

## 5. Bound the actual O4 source as a smeared observable

The energy bound can control more than the scalar norm without pretending
to be a pointwise derivative bound. Let h^{ab} be a smooth, real,
compactly supported inverse-metric test variation in spacetime. It is a
test field, not the spatial metric h_ij used above. Define
Q_4[h]=integral sqrt(-g) T4_ab h^{ab}.

Use the already derived full Hilbert stress in
`DERIVATION-20260907-O4-Hilbert-source-and-responsive-matter.md`:

```text
T4_ab = 2u W v_a v_b
        +8u nabla^c nabla^d(X C_acbd)+4u X R^{cd} C_acbd.
```

Compact support permits two integrations by parts, WITHOUT commuting the
derivative order:

```text
B_h = 4 C_acbd nabla^d nabla^c h^{ab}
      +2 R^{cd} C_acbd h^{ab},
Q_4[h] = 2u integral sqrt(-g) [W h^{ab} v_a v_b + B_h X].
```

This is the adjoint form of the curvature variation. No term containing
derivatives of X has been thrown away; its derivatives now act on the
specified test variation. For h^{ab}=sigma(x) g^{ab}, Weyl tracelessness
gives B_h=0, hence the same trace identity T4^a_a=2uWX as the earlier
independent calculation. Freezing W in the stress would give the wrong
sign and does not reproduce this check.

In a static orthonormal frame use ordinary Euclidean matrix/tensor norms
only for estimates. Set S=v_0^2+sum_i v_i^2 and K_min=1-delta. Then
|X|<=S and |h^{ab}v_a v_b|<=||h||_op S. Define the computable test norm

```text
C4[h] = sup_support (|W| ||h||_op + |B_h|).
```

An explicit, less sharp substitute replaces |B_h| by
4||C||_F||nabla^2 h||_F+2||Ric||_F||C||_F||h||_F.
For the static spherical background the Weyl tensor is purely electric,
so its orthonormal Euclidean squared norm is W and ||C||_F<=sqrt(W_max).
The perfect-fluid Ricci components additionally give

```text
||Ric||_F^2 = (8 pi G_N)^2 (rho^2+3p^2),
Ric_max = 8 pi G_N sqrt(rho_c^2+3p_c^2).
C4[h] <= W_max H_op +4 sqrt(W_max) H_2
                     +2 Ric_max sqrt(W_max) H_F,
```

where H_2=sup||nabla^2 h||_F, H_F=sup||h||_F and p_c is central pressure.
The exterior Ricci tensor vanishes. These are explicit background and
measurement-resolution norms; a small u alone is not the whole estimate.
Since the quadratic local energy is

```text
E_Omega(t) = (1/2) integral_Omega N sqrt(h)
              [K_0 S + m^2 chi^2] d^3x,
```

the full O4 source satisfies

```text
|Q_4[h]| <= (4 |u| C4[h]/K_min) integral_I E_Omega(t) dt.
```

I is the time support of h, and Omega contains its spatial support.
The test norm involves the prescribed geometry and up to two derivatives
of h, not uncontrolled pointwise fourth derivatives of the scalar.
The identity remains meaningful distributionally when X C is only
integrable; interface distributions are not silently deleted. A boundary
or a test variation not compactly supported needs its explicit boundary terms.

For the canonical part set
H_op=sup||h||_op and H_tr=sup|g_ab h^{ab}|. Its contribution obeys

```text
|Q_can[h]| <= 2 max[(H_op+H_tr/2)/K_min, H_tr/2]
                   integral_I E_Omega(t) dt.
```

The sum bounds the retained quadratic scalar Hilbert source, including O4.
For the bound component alone E_Omega(t)<=E_b, giving an explicit
coefficient times |I| E_b and therefore the m^4 localized-excitation bound.
For the complete field one must also bound its complementary energy and
nonlinear feeding; cross terms are not removed by a claim of linear decay.

More precisely, in the quadratic evolution assume separately that the
complementary spectral component has local energy tending to zero. The
local energy norm gives sqrt(E_Omega)<=sqrt(E_b)+sqrt(E_complement,Omega).
For time translates of one fixed compact test field on the static
background, the preceding full-source bound consequently has late-time
limsup at most its displayed coefficient times |I| E_b. This carries the
localized initial-data suppression into a weak local stress residual
without assuming initial orthogonality to the bound modes. The local
decay hypothesis itself is not established by this inequality.

This is a weak, finite-resolution SOURCE bound. To claim a metric, clock or
PPN observable, its actual constrained Einstein/matter response must supply
the corresponding adjoint test field and a finite test norm. A singular
point-source Green function or an unspecified measurement kernel cannot be
substituted automatically. Nevertheless the full O4 stress no longer
requires an arbitrary pointwise derivative closure for this class of
specified smeared source observables.

## 6. Do not apply a global static cloud outside its regime

The selected Einstein limit with positive Lambda has weak-field potential
Phi=-mu/r-Lambda r^2/6. Put H_Lambda=sqrt(Lambda/3). At a radius r the
ratio of the cosmological radial acceleration to the source acceleration is
H_Lambda^2 r^3/mu. At the hydrogenic ground-state scale a_B,

```text
r_turn=(mu/H_Lambda^2)^(1/3),
(a_B/r_turn)^3 = [H_Lambda/(m alpha_G^2)]^2.
```

Accordingly H_Lambda << m alpha_G^2 is necessary for a source-dominated
cloud at that scale. This is a scale-separation diagnostic, not a proof of
a de Sitter bound spectrum. For a nominal nth hydrogenic radius n^2 a_B,
the acceleration ratio grows as n^6. One cannot transport the infinite
static bound tower to the cosmological problem unchanged.

A time-dependent FLRW problem also needs its actual expansion and tidal
terms, rather than identifying every H(t) with H_Lambda. A finite static
local patch does not justify a mode whose tail lies far outside it.
If the gate fails, use the appropriate evolving-background initial-value
problem; neither the static radiation coefficient nor this global projector
bound is then automatically a statement about the actual universe.

## Reproduction and scope

Companion: `scripts/parent_whole_star_localization_20260907.py`.
It must run between D4 workers, not alongside the active 5515 calculation.
Results are written under `source-intake/local-preparation/20260907/`.
It uses the frozen matched2 reference and both signs of its illustrative
curvature probe; it does not supply measured stellar or cosmological inputs.

The u=0 control is the same GR-plus-massive-scalar baseline, not a weaker
test assigned only to MTS. The localization mechanism and its m^4 power are
shared physics; the retained parent coefficient and mass enter through the
explicit envelopes. This is not new empirical preference for MTS over GR.

This fills the regular-interior coefficient requirement of a conditional
localization bound and derives its retained smeared-Hilbert-source consequence.
It does not prove cosmological preparation, nonlinear
relaxation, a physical damping timescale, a numerical PPN residual, or the
full all-operator MTS-to-GR limit. Those conclusions remain open.

## Executed checks

After 5515/bounded1 exited with its state saved and all 20 batch checks
passing, the companion ran alone on one core at BelowNormal priority.
In-memory compilation passed; the dry run passed 36/36 and the stellar
reference passed **53/53** in 5.289 numerical seconds.

The three profiles are the frozen matched2 reference at eta=0,+/-0.005.
Each checks 1,281 interior/exterior radii against the analytically derived
envelopes. Controls include the flat baseline, mass and unit rescaling,
both signs of u, horizon/kinetic/central-density contract failures, exact
Weyl pressure cancellation, the full conformal stress trace, a variable-
curvature adjoint integration identity and a noncompact boundary counterexample.
Samples support implementation checks, not a proof of uniform inequalities.

For eta=0 the conservative coefficients are
N_c=0.8796948675820793, zeta=0.18945690322020126,
kappa=0.7919907582646546, theta_lower=0.773863060050252,
and b/m^2=0.1417490791459215 in the declared reference units.
The interior term controls b; using only the exterior value
0.043505371258418996 would understate this conservative global envelope.
Both nonzero signs have delta=0.13166770998394248 and remain within the
same positive-kinetic bound. No sign is discarded to obtain the result.

For initial data localized within the stellar radius, evaluated bounds are:

| alpha_G | eta=0 energy-fraction bound | eta=+/-0.005 bound |
| ---: | ---: | ---: |
| 0.02 | 1 (uninformative) | 1 (uninformative) |
| 0.01 | 0.133887325 | 0.655644462 |
| 0.005 | 0.008367958 | 0.040977779 |
| 0.0025 | 0.000522997 | 0.002561111 |

These vary m at fixed reference geometry and u, not the physical state of a
measured star. They evaluate the proven conditional expression with numerical
reference inputs; they are not interval-certified stellar parameters or
measured MTS residuals. The original alpha_G=0.02 reference supplies no useful
suppression from this deliberately coarse bound. Halving m reduces the
unsaturated bound by sixteen, as derived, without refitting a coefficient.

Passing result:
`source-intake/local-preparation/20260907/whole-star-localization-reference1/result.json`,
SHA256 `ce3785850bb36f03667ca2e08956a512fce64231775340b70639feda61a694ea`.
Dry-run SHA256:
`1b9ccd429f4a0b794775ccebfab9c4fe9584b2f15ab022a8be51c0f3758115d4`.
Executed companion SHA256:
`ebf2e600dab30541c26e0a18ef479cf36c3dd208514d5fa80ecb9ab2b597ccee`.
All retained source and main-state hashes match; all physical claim flags
remain false. This is a bounded-source result, not a new relaxation-rate claim.
