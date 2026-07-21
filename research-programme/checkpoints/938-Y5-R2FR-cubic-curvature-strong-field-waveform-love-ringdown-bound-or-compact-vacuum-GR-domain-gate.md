# 4922 - Weyl-cubic coefficient map, GW170608 bound and vacuum-domain gate

**Status:** A coefficient-coordinate error in checkpoint 4921 is corrected.
The corpus parity-even Weyl-cubic packet is mapped to the coefficient directly
constrained in a two-parameter GW170608 analysis. The corrected pure-`I1`
static metric makes weak Solar-system and clock feedback negligible throughout
that observational envelope. The same posterior does not enforce one-percent
EFT control at a black-hole horizon, so compact-vacuum GR is not promoted.
MTS still does not predict the finite value of the cubic coefficient.

Marker: `MTS_WEYL_C3_GW170608_DOMAIN_GATE_4922`.

## 1. Canonical invariant packet

The corpus parity-even operator is

```text
O_+ = C_mn^rs C_rs^ab C_ab^mn = I1 = C7
```

on a Ricci-flat background. Write its effective action in either of the
equivalent forms

```text
S = integral sqrt(-g)[R/(16 pi G_N) + zeta_+ I1 + ...]

  = (16 pi G_N)^-1 integral sqrt(-g)
      [R + a_+ I1 + ...],

a_+ = 16 pi G_N zeta_+ = s_+ ell_+^4,
s_+ = sign(zeta_+),
ell_+ = abs(16 pi G_N zeta_+)^(1/4).
```

This is the coefficient coordinate shared by the corpus, the pure
parity-even black-hole solution, and the first GW coupling below. It does not
set `zeta_+` to zero and it does not derive it from the MTS parent.

## 2. Why checkpoint 4921 had to be superseded

Burger, Emond and Moynihan use

```text
P = beta1 I2 + beta2 I1 + Ricci terms.
```

On the smooth four-dimensional Ricci-flat quotient used by the corpus,

```text
I2 = I1/2,
zeta_+ = lambda(beta2+beta1/2).
```

Their displayed nonrotating probe potential has an `r^-6` coefficient
proportional to `lambda beta1`, not to the complete expression above. The
counterexample

```text
beta1=0, beta2!=0
```

has zero Burger `beta1` probe length while `zeta_+=lambda beta2` is nonzero.
Therefore no inversion from the old `L3` to `zeta_+` exists without an
additional owned `beta2/beta1` relation. The following 4921 statements are
demoted to a declared Burger-`beta1` benchmark:

- `L3^4=144 pi G_N abs(d3)` as a total-cubic normalization;
- the `r^-6` transfer as the generic corpus `I1` exterior;
- the Galileo, Cassini and Mercury `L3` envelopes as bounds on `zeta_+`;
- `epsilon_K=L3^4 K/9` as the active invariant control parameter.

The nonlocal source/state separation and the absence of a direct fixed-metric
Maxwell variation remain valid.

## 3. Correct pure-`I1` static transfer

For `a_+=s_+ ell_+^4`, the sourced nonrotating solution is written as

```text
ds^2 = -N(r)^2 f(r) dt^2 + dr^2/f(r) + r^2 dOmega^2,

f = 1-2M/r
    +24 s_+ ell_+^4 M^2[9/r^6-49M/(3r^7)],

N = 1-108 s_+ ell_+^4 M^2/r^6.
```

At first order in `ell_+^4`, the two `r^-6` terms in `N^2 f` cancel exactly:

```text
N^2 f = 1-2M/r+40 s_+ ell_+^4 M^3/r^7.
```

With `g_tt=-(1-2 Phi)`, this gives

```text
delta Phi = -20 s_+ ell_+^4 M^3/r^7,

abs(delta a/a_N) = 140 ell_+^4 M^2/r^6,

abs(alpha_clock)
 = 20 ell_+^4 M^2
   abs(r1^-7-r2^-7)/abs(r1^-1-r2^-1).
```

The cancellation is why the 4921 `r^-6` potential cannot be carried into the
pure corpus `I1` route.

## 4. Direct GW170608 coefficient bound

Liu and Yunes analyse the parity-preserving cubic action

```text
L_D6 = alpha1_EFT I1
     + (alpha2_EFT/2)(I1-2I2),

alpha_bar_i = alpha_i_EFT/(Lambda^4 M_geo^4).
```

Thus the exact sample-level map for the corpus direction is

```text
alpha_bar1 = a_+/M_geo^4
           = s_+(ell_+/M_geo)^4.
```

The second coefficient is retained and marginalized. It is not identified
with `zeta_+`; its operator has no isolated-body contribution in the cited
EFT treatment but contributes to two-body binding and radiation.

The published 90-percent marginalized results are

```text
alpha_bar1 =  0.87 +1.95 -1.03  -> [-0.16, 2.82],
alpha_bar2 = -0.35 +4.12 -2.92  -> [-3.27, 3.77],
log B_EFT/GR = -2.81.
```

The data therefore prefer GR over this EFT model. The sign-dependent
dimensionless limits on the corpus length are

```text
s_+=-1: ell_+/M_geo < 0.16^(1/4) = 0.6324555,
s_+=+1: ell_+/M_geo < 2.82^(1/4) = 1.2958725.
```

Using only the paper's approximate component masses `12+7 solar masses`
gives `M_geo approximately 28.0567 km` and illustrative translations

```text
s_+=-1: ell_+ < 17.7446 km,
s_+=+1: ell_+ < 36.3579 km.
```

The dimensionless posterior interval is authoritative. The kilometre values
are approximate because checkpoint 4922 does not possess posterior samples
that correlate source mass and coupling.

Model boundary: the waveform includes the leading 5PN and partial 6PN
inspiral corrections, an interpolated merger, and a QNM ringdown fit used in
its stated spin range. It is not a direct cubic-EFT numerical-relativity
merger simulation. The authors impose explicit EFT-validity priors.

## 5. Corrected weak local projection

The corrected Galileo clock envelope alone is

```text
ell_+ < 7.5841082408e9 m,
```

so it is vastly weaker than the GW scale. At the approximate positive GW
endpoint `ell_+=36.3579 km`, the corrected projections are

```text
Galileo alpha_clock                 = 1.3098771e-26,
Earth-surface abs(delta a/a_N)      = 7.1957602e-26,
Earth-surface ell_+^4 K             = 2.4671178e-26,
Sun-surface ell_+^4 K               = 1.6131431e-27.
```

These are not fitted MTS signals. They show that an `I1` coefficient anywhere
inside the current GW envelope cannot disturb the already selected weak
invariant-vacuum GR branch at measurable local precision.

## 6. Compact-domain gate

The canonical strict-EFT control parameter is

```text
epsilon_K = ell_+^4 K.
```

At a Schwarzschild horizon,

```text
K_h = 3/(4M_geo^4),
epsilon_h = (3/4) abs(alpha_bar1).
```

The GW170608 posterior endpoints therefore allow

```text
epsilon_h = 0.12   on the negative branch,
epsilon_h = 2.115  on the positive branch.
```

For a one-percent domain requirement, the endpoints are too weak by factors
`12` and `211.5`. Equivalently, a same-mass 19-solar-mass horizon would need
`ell_+<9.5339 km`; the existing ten-solar-mass benchmark needs
`ell_+<5.01785 km`, and the selected neutron-star curvature benchmark needs
`ell_+<3.47341 km` before interior/EOS issues are even considered.

Therefore:

```text
weak invariant-vacuum GR    -> retained after corrected transfer;
compact-vacuum GR           -> not promoted;
compact-matter GR           -> not promoted;
full MTS-to-GR              -> not promoted.
```

The failed compact gate is not evidence for a nonzero correction. It means
the published upper limit is not yet small enough to certify the chosen
one-percent expansion domain.

## 7. Maxwell and source coupling

`I1` is metric-only, hence at fixed metric

```text
delta S_I1/dA_mu = 0.
```

It does not create charge, alter the Maxwell kinetic term, or directly modify
the Poynting vector. Electromagnetic effects arise only through the corrected
metric unless separate mixed operators such as `R F^2` are activated. This
checkpoint therefore bounds one gravitational residual; it does not close the
MTS-to-Maxwell or calibrated-source-coupling derivation.

## 8. Decision and next derivation

Closed here:

- the invariant map from corpus `zeta_+` to `ell_+` and `alpha_bar1`;
- the noninvertibility of the old Burger-`beta1` length;
- the corrected pure-`I1` static potential, acceleration and clock transfer;
- a direct two-parameter-marginalized GW bound on the corpus direction;
- the weak-versus-compact domain decision.

Still open:

- a parent-derived finite `zeta_+`, including its sign;
- posterior samples for an exact physical-length recast;
- a direct finite-spin gravitational pure-even QNM likelihood with current
  high-SNR data;
- compact-matter interior and EOS matching;
- the separate parity-odd boundary coefficient;
- MTS-to-Maxwell and source-coupling closure.

Direct next target:

`4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md`

Use the GW250114 ringdown products with the finite-spin **gravitational** QNM
template of arXiv:2307.07431 only if the remnant spin and posterior products
support an exact coefficient-level recast. The 2026 rapid-spin calculation
arXiv:2604.11755 treats scalar perturbations and is explicitly rejected as a
gravitational-wave QNM template. Do not infer a stronger number by copying a
generic-QNM deviation bound, and do not promote compact GR unless both the
observational posterior and EFT-control condition are satisfied.

No GitHub action or public claim is authorized.

## Sources

- `https://arxiv.org/abs/2407.08929`
- `https://arxiv.org/abs/2110.11378`
- `https://arxiv.org/abs/1910.11618`
- `https://arxiv.org/abs/2205.05132`
- `https://arxiv.org/abs/2407.07043`
- `https://arxiv.org/abs/2509.08099`
- `https://arxiv.org/abs/2307.07431`
- `https://arxiv.org/abs/2604.11755` (scalar-sector exclusion only)
- `post-checkpoint-work/4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md`
- `post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md`
- `post-checkpoint-work/4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4922_Weyl_C3_GW170608_domain.py`
