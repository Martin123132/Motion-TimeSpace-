# Local dispersive preparation: a conditional route without a damping axiom

Date: 2026-09-06. Private companion derivation; not a replacement for checkpoint 5513.

## Result and scope

The prepared two-derivative GR/Newton/Maxwell branch in checkpoint 5211 is
retained. Checkpoint 5344 correctly rejects both global purification by a
closed stationary Hamiltonian and a universal positive local escape gap.
Neither rejection rules out **local observable relaxation by dispersion**.

Here a concrete part of that alternative is derived:

1. Every finite-energy solution of the free, massive motion-field equation
   on all of flat three-dimensional space loses its energy from each fixed
   bounded spatial region as time tends to infinity.
2. For its coherent states, the canonical stress difference from the vacuum
   and each fixed local Weyl-observable difference tend to zero. Global
   energy, unitarity and the global distance from the vacuum are preserved.
3. An explicit integrable-forcing bound transfers the classical local-energy
   conclusion to a more general equation, if that bound can be established
   from the parent. Its forcing is identified below, not replaced by damping.

This is a conditional propagation/preparation lemma, **not** an unconditional
MTS preparation history, a finite-time vacuum projector, a PPN bound, or an
all-operator local-GR promotion. The flat quadratic problem is a restriction
of the selected parent operator; a flat metric is not assumed to be the actual
calibrated, matter-containing background. In particular, an inertial-patch
approximation cannot simply be extended to infinite time.

## 1. Parent-owned starting equation

Checkpoints 5211 and 5344 give

```text
E_chi = nabla_mu(K_eff nabla^mu chi) - m_gap^2 chi = 0,
K_eff = 1 - 2 P_X + 2 u_O4 C^2,
P_X(0)=0,  Z_chi=1,  m_gap^2>0.
```

On the globally flat, fixed-metric quadratic reference problem, `C=0` and
`K_eff=1`. With signature `(-,+,+,+)` and `c=hbar=1`, write `m=m_gap>0`:

```text
u_tt - Delta u + m^2 u = 0,
(u(0),u_t(0)) in H^1(R^3) x L^2(R^3),
2 E_total = ||u_t||_2^2 + ||grad u||_2^2 + m^2 ||u||_2^2.
```

Here `u` is a classical displacement in the motion field, not the boundary
density matrix or its occupation. The energy norm is equivalent to the
stated Sobolev norm for each fixed positive `m`. No numerical value of `m`,
`G_N`, a charge, or an MTS state occupation is fitted or supplied by this lemma.

## 2. Finite-energy local decay without a momentum floor

For every fixed bounded `Omega`, define

```text
E_Omega(t) = (1/2) integral_Omega [u_t^2 + |grad u|^2 + m^2 u^2] d^3x.
```

**Claim in the reference problem:** `E_Omega(t) -> 0` as `|t| -> infinity`.

### Proof

Use the unitary spatial Fourier transform and `omega(k)=sqrt(|k|^2+m^2)`:

```text
u_hat(t,k) = cos(t omega) f_hat(k) + sin(t omega) g_hat(k)/omega.
```

First take smooth Fourier data supported in an annulus
`delta <= |k| <= K`, with `delta>0`. This is a dense approximation class,
not a physical lower momentum cutoff. For `|x|<=R`, the two Fourier phases
are `k.x +/- t omega(k)`. Their gradients obey

```text
|grad_k phase| >= |t| v_min - R,
v_min = delta/sqrt(K^2+m^2) > 0.
```

For `|t|>=2R/v_min`, integration by parts in the direction of this gradient
gives arbitrary inverse powers of `|t|`, uniformly on `Omega`. Smooth compact
Fourier support removes boundary terms. The same argument applies to `u_t`
and `grad u`, whose amplitudes gain only smooth factors `omega` or `k` on
the annulus. Thus local energy tends to zero for this dense class.

Now approximate arbitrary finite-energy data by those annular data in the
energy norm, with error less than `eta`. Cutting out `k=0` has vanishing
energy error as `delta -> 0`; a nonzero value of a regular Fourier transform
at zero is allowed. Energy conservation keeps the global error below `eta`
at every time. Restriction to `Omega` cannot increase the positive energy norm:

```text
sqrt(2 E_Omega[u](t))
 <= sqrt(2 E_Omega[u_approx](t)) + eta.
```

Take `limsup` at large time and then `eta -> 0`. This proves the claim.
The proof neither assumes `k>=1/R` for the actual state nor assumes a
positive instantaneous outward flux.

With suitably weighted/smooth data there are stronger quantitative decay
estimates; the free weighted-energy theorem of Komech and Kopylova,
Proposition 2.1, gives an inverse-three-halves norm decay. Their interacting
potential theorem explicitly separates continuous spectral states and imposes
threshold conditions. Neither result is imported as a theorem about the
full MTS background. [Primary source](https://arxiv.org/abs/1003.3799)

There is **no universal preparation time derived here**. In particular, a
bound `E_Omega(t)<=h(t) E_total` with `h(t)->0` cannot hold uniformly over
all finite-energy initial data: choose initial data by evolving a packet
localized in `Omega` backwards from any arbitrarily late observation time.
Localization/weighted norms and the preparation history matter to any rate.

## 3. Hilbert energy leaves the region; it is not destroyed

For the canonical free scalar, put

```text
e = (u_t^2 + |grad u|^2 + m^2 u^2)/2,
S = -u_t grad u,
partial_t e + div S = 0,
dE_Omega/dt = -integral_boundary S.n dA.
```

The last identity is classical for sufficiently regular data/domain and
extends in the usual integrated weak sense; the local-decay proof does not
require a pointwise boundary trace for every energy-space solution.
No Lindblad rate, friction term, stress sink, or rule `Phi>=kappa E_Omega`
has been inserted. In a fixed Cartesian orthonormal frame, the quadratic
Hilbert stress obeys, component by component,

```text
|T_u^{mu nu}| <= e,
integral_Omega |T_u^{mu nu}| d^3x <= E_Omega(t) -> 0.
```

For example, `|T^{0i}|=|u_t partial_i u|<=e`; spatial diagonal components
are differences of positive squares whose absolute values are bounded by
their sum `2e/2`. The total stress-energy still has its conserved global
energy. This bound is for the canonical quadratic contribution, not the
full curvature/P(X)/loop stress.

## 4. What local vacuum convergence does and does not mean

Consider a coherent displacement of the same free-field vacuum. Define
the displacement convention so its field and momentum means are `u,u_t`,
and its covariance is the vacuum covariance. For fixed smooth real smears
`F,G` supported in `Omega`, use the bounded Weyl observable

```text
W(F,G)=exp(i integral [F chi + G pi] d^3x).
omega_u,t(W)=omega_0(W) exp(i integral_Omega [F u+G u_t] d^3x).
```

Since `|omega_0(W)|<=1` and `|exp(i a)-1|<=|a|`, weighted Cauchy-Schwarz gives

```text
|omega_u,t(W)-omega_0(W)|
 <= sqrt(2 E_Omega(t)) sqrt(||F||_2^2/m^2 + ||G||_2^2) -> 0.
```

The `m^-1` dependence is explicit: this estimate is not a mass-uniform or
massless limit. Finite products of Weyl operators reduce to another Weyl
operator times a phase. Linear combinations and norm approximation therefore
give pointwise convergence on the generated local Weyl C*-algebra. No
convergence uniformly over all measurements or in global trace norm follows.
No identification with the parent's binary projector/occupation is made.

For coherent displacements the vacuum-subtracted canonical quadratic stress
expectation equals the classical stress above, so its local integral also
decays. This use of coherent states and canonical stress is compatible with
the algebraic free-field treatment of Casini, Grillo and Pontello; we do not
use a relative-entropy formula or add an improvement/boundary term.
[Primary source](https://arxiv.org/abs/1903.00109)

A probability mixture of such coherent states with finite mean total energy
inherits these local limits by dominated convergence. This is still a
specified class of states, not a characterization of every parent state.
Globally the coherent occupation norm and vacuum overlap stay constant;
the state has not been unitarily purified. Local observables can relax while
the distinguishing excitation travels outside the fixed observation region.

## 5. A derived transfer bound for the actual remainder

For the classical forced equation

```text
u_tt - Delta u + m^2 u = J,
integral_0^infinity ||J(s)||_L2 ds < infinity,
```

let `U(t)` be the free group, `Psi=(u,u_t)`, and
`||Psi||_E^2=2E_total`. Duhamel's formula and unitarity define a finite-energy
scattering datum and an explicit tail bound:

```text
Psi_plus = Psi(0) + integral_0^infinity U(-s)(0,J(s)) ds,
||Psi(t)-U(t)Psi_plus||_E <= B_J(t),
B_J(t) = integral_t^infinity ||J(s)||_L2 ds,
sqrt(2E_Omega[Psi](t))
 <= sqrt(2E_Omega[U(t)Psi_plus]) + B_J(t) -> 0.
```

For the displayed parent equation, its exact rearrangement relative to this
flat reference operator is

```text
J_parent = (Box_g-Box_eta) chi
         + nabla_mu[(K_eff-1) nabla^mu chi].
```

The signs follow by multiplying `(Box_eta-m^2)chi` by minus one in the
chosen signature. This expression is evaluated on a solution; its second
derivatives can be quasilinear. Writing it down does not establish existence,
scattering, or the L1-time/L2-space condition. Additional operators beyond
the displayed parent equation must contribute their own exact remainder.

This is a sufficient, testable mathematical condition, not a necessary
condition and not a sourced damping coefficient. Static long-range gravity,
bound modes, nonlinear terms or continuing incoming radiation may violate it.
Weak curvature alone does not prove time-integrability. Modified-scattering
or curved-background estimates may be needed instead. The transfer bound
is classical; interacting quantum state convergence needs further work.

### An explicit coefficient bound, rather than an unnamed remainder

In the same fixed coordinates let `s=sqrt(-det g)` and define

```text
A^{mu nu} = K_eff g^{mu nu} - eta^{mu nu},
B^nu = s^(-1) partial_mu(s K_eff g^{mu nu}),
J_parent = A^{mu nu} partial_mu partial_nu chi + B^nu partial_nu chi.
```

These are exact coefficient identities for the displayed parent equation,
not fitted couplings. Use Euclidean component norms in this coordinate chart
and spatial Lebesgue norms on each reference time slice. Cauchy-Schwarz in
the component indices followed by Holder's inequality gives either bound

```text
||J_parent||_2 <= ||A||_infinity ||D^2 chi||_2
                 + ||B||_infinity ||D chi||_2,
||J_parent||_2 <= ||A||_2 ||D^2 chi||_infinity
                 + ||B||_2 ||D chi||_infinity.
```

Here `D` includes time derivatives; the second derivative norm is the full
component norm, not just a spatial Laplacian. Each inequality can be used
only when its stated norms are finite. Integrating either right-hand side
from `t` to infinity supplies the tail `B_J(t)` directly. This is a concrete
way to connect a future solution estimate to the transfer theorem, without
inserting a decay rate. It is still a sufficient test, not a proof that the
actual solution passes it. For example a static metric with a `1/r` tail
generally has a non-square-integrable `A` on R^3; small metric amplitude
does not automatically make either estimate integrable in time.

## 6. Boundaries that prevent a hidden closure

- A homogeneous oscillator is not finite total energy on R^3; it remains a
  valid obstruction when the parent allows homogeneous occupied backgrounds.
- A finite reflecting box, trapped modes and a continuously supplied state
  are outside the free whole-space decay theorem. None is silently removed
  from the actual parent spectrum.
- Small local quadratic stress does not itself bound the metric, exterior
  tidal fields, gravitational memory or the PPN vector; retarded/source and
  boundary matching are still required.
- The full P(X), curvature and quantum stresses need their own bounds; H^1
  control alone does not bound every higher-derivative operator.
- The parent's CTP state/projector must be related to the stated observable
  class before this can replace any preparation datum `rho_local=rho_0`.
- No actual cosmological/local preparation history, numerical relaxation
  time, `G_N`, charge normalization or source coefficient is supplied here.

Thus the new route is local dispersive relaxation, not global purification.
It preserves the 5344 no-go and sharpens what can still be attempted. The
active D4 enclosure remains unchanged and continues independently.

## Sources and reproducibility

Local sources are listed with exact paths in
`source-intake/local-preparation/20260906/provenance.json`.
The companion is `scripts/local_dispersive_preparation_20260906.py`.
Its dry-run writes nothing. Its finite quadrature examples, bulk/boundary
energy-flux balance, coherent-phase bound, forced-mode transfer witness and
homogeneous-mode negative control are **checks of examples/algebra, not proofs of the
infinite-dimensional theorem**. The proof is in Sections 2-5.

The numerical example uses dimensionless `m=1`, not a claimed MTS mass.
No periodic spatial simulation is used to infer continuum decay. The script
must run only when the checkpoint-5513 numerical worker is absent; it refuses
to run its calculations alongside that worker. Validation results will be
written to `source-intake/local-preparation/20260906/checks.json` after execution.
No physical claim flag is promoted by a passing test.

### Executed validation, 2026-09-06

AST parsing and in-memory compilation passed without bytecode. The dry-run
correctly detected the live checkpoint-5513 worker and prohibited numerical
execution alongside it. After record 37 finished and its completion marker,
state hash and all 23 validation rows were verified, the companion ran alone
on one core at BelowNormal priority: **16/16 checks passed**, approximately
1.02 numerical seconds. The main numerical state hash was unchanged by this
run. No `scripts/__pycache__` was created.

For the dimensionless Gaussian example (`m=1`, radius `3`), the fine-grid
local energy changed from `6.946880463682323` at `t=0` to
`0.00011281025014050248` at `t=80`. Global spectral energy remained
`6.960409996039633`, and global coherent-state trace distance from the vacuum
remained `0.993122931024592`. Bulk energy change matched boundary energy
flux; doubling both quadrature resolutions passed the comparison tolerance.
The homogeneous zero-flux control did not relax. These are reference-problem
examples, not MTS units, fitted parent parameters, a universal rate, or a
nonlinear-parent simulation.

Result file: `source-intake/local-preparation/20260906/checks.json`.
SHA-256: `d9afff304c6ae72fedeed5aa8ca9d431fe08b89d0ad7ecc172aa8902dfd29e21`.
It records the script/source hashes, individual checks and all physical
claim flags as false. The next derivation is a parent-owned estimate of the
identified remainder or an appropriate curved-background scattering estimate,
not an assumed relaxation constant. This companion does not displace the
active D4 enclosure as numerical owner.
