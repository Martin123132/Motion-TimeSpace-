# 4924 - Parent Weyl-cubic finite matching, scalar threshold and counterterm theorem

**Status:** The motion-scalar determinant contribution is now derived in the
same canonical coefficient used by the GW analyses. Its sign is positive, its
parity-odd partner is zero, and its required physical mass scale is
extraordinarily small. The total MTS coefficient is nevertheless not derived:
the quantum metric sector's nonzero two-loop I1 pole makes an independent
finite renormalization boundary unavoidable unless a UV parent condition is
supplied. This is an exact separation of a calculable threshold from the
remaining Wilson boundary, not another missing-variable inventory.

Marker: MTS_PARENT_WEYL_C3_FINITE_MATCHING_4924.

## 1. Parent action audit

The relevant chain is now concrete.

1. The integrated-H parent owns one public metric and one metric 1PI action.
2. A healthy real scalar pole contributes one half Tr log D.
3. The full off-shell a6 quotient and Ricci-flat I1 projector are validated.
4. The free determinant coefficient was independently recovered without
   feeding the heat-kernel answer into the determinant response.
5. The attempted non-Gaussian correction failed both promotion and covariant
   image gates, so no numerical residual may be added.
6. The public quantum metric has the nonzero pure-gravity two-loop I1 pole.
7. The single measured-G calibration fixes the Einstein residue, not an
   independent six-derivative finite coefficient.

The last two clauses are decisive. A scalar threshold can be calculated while
the total renormalized coefficient remains a separate UV matching problem.

## 2. Exact scalar threshold

For one healthy real scalar pole of mass m_gap, the Ricci-flat parity-even
threshold is

    zeta_plus_scalar
      = F/[30240(4 pi)^2 m_gap^2],

    F=exp[-m_gap^2/Lambda_UV^2],  0<F<=1.

For N_real independent real poles, multiply by N_real. In the canonical
corpus normalization,

    a_plus_scalar
      =16 pi G zeta_plus_scalar
      =N_real G F/[30240 pi m_gap^2],

    ell_plus_scalar^4
      =N_real l_P^2 lambda_C^2 F/[30240 pi],

    ell_plus_scalar
      =[N_real/(30240 pi)]^(1/4)
       sqrt(l_P lambda_C) F^(1/4).

Here lambda_C=hbar/(m_gap c) is the reduced Compton wavelength. The numerical
prefactor for one real pole is

    [1/(30240 pi)]^(1/4)=0.05695962024.

The sign is strictly positive for a healthy scalar determinant. A scalar
determinant generates no parity-odd cubic threshold. On a Ricci-flat
projection the pure I1 coefficient is independent of the nonminimal xi term,
because every xi-dependent insertion carries Ricci scalar or Ricci-sector
data.

This closes the sign and normalization of the motion-scalar Gaussian
threshold. It does not fix the number of physical real poles or their
physical mass.

## 3. Motion-scalar scaling and provisional coefficient

The printed nonanalytic potential gives

    mu=lambda^(3/8),
    m_gap=c_m mu,
    zeta_plus_scalar
      =N_real c6 lambda^(-3/4).

In the continuum-threshold limit F=1,

    c6=1/[30240(4 pi)^2 c_m^2]

per real pole. The 4909 constant-fit pilot gives

    c_m=1.021288694 +/- 0.024081277,

while the conservative two-sigma model union is

    0.727804921 <= c_m <= 1.189451317.

Therefore the per-real-pole coefficient is

    central c6 = 2.0077121007e-7,

    conservative c6 range
      = [1.4801479971e-7, 3.9533795366e-7].

These are exact transforms of the pilot, not a promoted continuum
measurement. The physical coefficient remains proportional to
lambda^(-3/4), and the parent has not fixed lambda in physical units.

The 4914 residual-zero decision must also be read correctly:

    active non-Gaussian residual = zero selected,
    exact all-orders residual    = not proved zero.

The approximately 1.5-sigma noncovariant lattice excursions cannot be
converted into c6 because their response failed the covariant-image gate.

## 4. Corrected universal pure-gravity running

The two-loop pure-gravity pole is already in the chained I1 contraction used
by the corpus. In the convention retained at 4921,

    Delta zeta_plus
      =[209/(2880(4 pi)^4)] kappa^2 ln(mu/mu0),

    kappa^2=32 pi G.

Mapping directly to a_plus=16 pi G zeta_plus gives

    Delta a_plus
      =[209/(1440 pi^2)] l_P^4 ln(mu/mu0).

For one unit of logarithm,

    ell_plus_GS
      =[209/(1440 pi^2)]^(1/4) l_P
      =0.3482338723 l_P.

Even a logarithm of magnitude 100 gives only 1.1012 l_P. This contribution is
irrelevant to every current weak or compact arena.

The older 0.603159 l_P value used the superseded checkpoint-4921 Burger
beta1 length, whose fourth power was nine times the canonical a_plus
coordinate. It is not the active I1 running length.

## 5. Counterterm theorem

The finite-boundary question can now be decided without hand waving.

1. I1 is a local parity-even Diff invariant.
2. No retained MTS symmetry forbids it.
3. The quantum public metric has a nonzero two-loop I1 divergence.
4. Therefore a counterterm-complete quantum parent must contain
   zeta_plus,b(mu0) I1.
5. The pole fixes running, not the finite value at mu0.
6. Measured G fixes M_R^2 and the universal source residue only.
7. No current UV fixed point, spectral identity or matching observable fixes
   zeta_plus,b(mu0).

Consequently,

    a_plus(mu)
      =a_plus,b(mu0)
       +a_plus,scalar
       +a_plus,interacting_residual
       +sum_i a_plus,i,threshold
       +Delta a_plus,GS
       +a_plus,H+ghost,finite.

The scalar term and GS running are derived. The finite boundary, complete
massive spectrum, physical pole count, non-Gaussian continuum residual and
metric/ghost finite term are not.

Setting zeta_plus,b(mu0)=0 is legal and useful as a minimal matching branch.
It is an explicit renormalization condition at one scale, not a consequence
of Diff symmetry and not an all-scale zero theorem.

This proves that the current corpus cannot derive the total finite zeta_plus
or its sign from the motion-scalar determinant alone.

## 6. Physical scale gates

For a positive scalar threshold, an ell_plus envelope implies

    m_gap c^2
      >hbar c sqrt(N_real) l_P
       /[sqrt(30240 pi) ell_cap^2].

The resulting one-real-pole floors are

    GW250114 robust positive branch:
      ell_cap = 44.3447 km,
      m_gap > 5.2620e-54 eV;

    GW170608 published positive branch:
      approximate ell_cap = 36.3579 km,
      m_gap > 7.8277e-54 eV;

    ten-solar-mass one-percent horizon:
      ell_cap = 5.01785 km,
      m_gap > 4.1096e-52 eV;

    1.4-solar-mass, 12-km neutron-star one-percent benchmark:
      ell_cap = 3.47341 km,
      m_gap > 8.5767e-52 eV.

Every floor scales as sqrt(N_real). Using the conservative low endpoint of
the c_m pilot, the strongest displayed requirement becomes

    mu > 1.17843e-51 eV

for one real pole.

This is genuine progress: the motion-scalar threshold cannot endanger the
selected compact benchmarks unless its physical scale is fantastically
small. But the corpus has not independently fixed mu, so the scalar compact
gate remains an exact conditional theorem rather than a promoted prediction.

## 7. Decisions

Derived:

- the finite per-real-pole motion-scalar I1 threshold;
- its positive sign and zero parity-odd scalar partner;
- the exact c_m-to-c6 transformation and conservative pilot interval;
- the canonical Goroff-Sagnotti running in the corrected I1 coordinate;
- the mass-gap floors required by current GW and compact-domain gates;
- the theorem that a quantum-metric parent needs an independent finite I1
  renormalization boundary.

Not derived:

- the physical real-pole multiplicity;
- lambda or mu in physical units;
- a nonzero interacting residual;
- other massive thresholds;
- the finite integrated-H/ghost contribution;
- the finite boundary zeta_plus,b(mu0);
- the total zeta_plus magnitude or sign.

Current theory verdict:

    motion-scalar Gaussian threshold = derived and positive;
    universal pure-gravity running   = derived and negligible;
    scalar compact safety            = exact conditional scale theorem;
    total compact-vacuum GR          = not promoted;
    compact-matter GR                = not promoted;
    full MTS-to-GR                   = not promoted.

Next target:

4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md

That target must search the integrated-H measure for an actual UV condition
on zeta_plus,b. If none exists, the framework should declare one bounded
Wilson input explicitly rather than continue pretending the scalar threshold
fixes the total.

No GitHub action or public claim is authorized.
