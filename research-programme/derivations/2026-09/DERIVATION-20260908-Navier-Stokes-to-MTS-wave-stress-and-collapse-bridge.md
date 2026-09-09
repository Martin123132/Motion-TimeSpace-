# From the new Navier–Stokes construction to an MTS wave–geometry calculation

2026-09-08. Private research. No GitHub publication. Heavy numerical work remains paused.

## Bottom line

There is a usable method here, not a transferable black-hole theorem. This note
constructs a leading motion-wave source and its spherical metric response from
the existing MTS correspondence action, and derives the first scalar harmonic
corrections, including the retained quartic interaction. It does not replace
the parent by a fluid, prescribe an unexplained external force, or claim that
an averaged source is already an exact microscopic solution.

The useful change of attack is **construct a realizable wave stress, solve for
its geometry, then cancel the actual field-equation residual**. A regular
black-hole centre and a complete MTS solution are not obtained below.

## 1. What the new paper actually supplies

OpenAI's [paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf),
Theorem 1.1, constructs finite-time velocity blowup with bounded kinetic energy
and smooth compact external forcing. Forced breakdown is an allowed Clay
alternative; it is not a proof of unforced Navier–Stokes breakdown.

The construction uses a concentrating axisymmetric background, an annular
stress deficit, and wave families with positive squared amplitudes that supply
the required mean momentum flux. Shear amplifies pulses; viscosity damps their
tails. Curl constructions preserve incompressibility. Repeated corrections
control the remaining interactions and cutoff errors so the residual force
extends smoothly through the singular time. See sections 3, 7.5–7.7 and 9.6–9.9.

There is no final mechanism that stops concentration: blowup is the outcome.
The source of finite energy is compatible with shrinking support and increasing
pointwise amplitude. The transferable ingredients are stress realizability,
constraint preservation and residual correction—not its chosen forcing or
its nonrelativistic singularity. This is a targeted reading, not an independent
verification of all 166 pages.

The official alternatives are in [Fefferman's Clay statement](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf).
The [announcement](https://openai.com/index/navier-stokes-solution/) describes an
unreleased discovery model; access to that model is not required to inspect
the released mathematics or Lean source.

## 2. What is formalized, and what this inspection can establish

Pinned repository commit: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, dated
2026-09-08T10:57:25Z. Source: [OpenAI/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538).

The inspected endpoint is an existential counterexample for every positive
viscosity, with smooth decaying force and initial data, excluding a global
smooth finite-energy solution. The periodic alternative has a separate endpoint.
The whole-space chain is:

```text
NavierStokes/ComparatorSolution.lean
 -> ComparatorR3Theorem.lean
 -> R3ActualCandidate.lean -> ActualCandidateAssembly.selected_witness
 -> R3FiniteEnergyComparison.lean -> R3/WholeSpaceUniqueness.lean
```

The last comparison is important: constructing one singular candidate alone
would not rule out a different smooth solution with the same data.
The candidate assembly contains actual potential, direct-field and pressure
sums, not just an assumed existence proposition at the displayed endpoint.

`ComparatorDefinitions.lean` expresses the PDE, incompressibility, smoothness,
initial condition, force decay and uniform energy requirement. Its explanation
of the totalized derivative outside differentiability does not remove the
explicit smoothness conditions on admissible solutions.

`formalization.yaml` reports only `propext`, `Classical.choice` and `Quot.sound`
as endpoint axioms, and labels its review self-assessed. The challenge module
contains intentional theorem placeholders. These are acceptable only if they
are not dependencies of the submission; the acquisition companion checks that
static import separation and compares the definition bodies.

**No Lean build, comparator execution or independent kernel check is claimed.**
A lexical scan is not a proof checker. Mathlib and compiler/tooling are outside
this local static audit. Released verification metadata must not be presented
as our independent verification.

Completed static result: 580 repository-local Lean files are reachable from
the submission. The scanner found none of its searched placeholder/axiom/
unsafe-tactic tokens in that closure after masking comments and strings.
The challenge module is not imported, and the definition bodies match after
that masking and whitespace normalization. These are positive source-level
checks, still not a kernel or comparator run.

The source archive is kept zipped, not expanded into thousands of working
files. Hashes, local paths, import closure and scan results belong in
`source-intake/navier-stokes/20260908/static-audit.json`. A small selected-source
folder retains exact upstream files and license material without modification.

## 3. The existing MTS starting point is not being discarded

Local source owners, all in this directory:

- `5203-Y5-R2FR-one-canonical-translation-gauge-parent-action-cross-coupling-and-branch-reduction-theorem.md`: one coframe action and its retained operators.
- `5211-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md`: selected exact classical two-derivative GR/Maxwell truncation and common Hilbert source.
- `4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md`: Einstein vacuum inclusion for the stated quadratic-curvature action, not all higher operators.
- `DERIVATION-20260907-O4-Hilbert-source-and-responsive-matter.md`: full curvature-varied O4 stress, not just a frozen kinetic coefficient.
- `RESULTS-20260908-parent-nonlinear-motion-comparison.md`: retained nonlinear motion bounds and completed control tests in their stated domain.

Use signature `(-,+,+,+)`, `c=hbar=1`, and retain calibrated `G_N`. The
geometric mass parameter below is `mu=G_N M`, not the scalar gap `m_chi`.

```text
S_ret = integral sqrt(-g) [ (R-2 Lambda)/(16 pi G_N)
                          -X/2-m_chi^2 chi^2/2+Q(X)-u_O4 C^2 X ],
X = g^ab partial_a chi partial_b chi,
Q(X) = b2 X^2+b3 X^3+... .
```

This is the relevant retained block, not the entire CTP/visible/C3/CFF/nonlocal
parent. Coefficients are held at one specified RG scale. The finite-order
construction first solves the `u_O4=0` correspondence block with Q retained.
Section 8 specifies the extra work required for the physical nonzero O4 and
other operators; they are not declared absent from MTS.

## 4. Derive the stress that waves can actually supply

On a smooth background, set `chi_epsilon=epsilon a(x) cos(S(x)/epsilon)`.
For the quadratic scalar block, the inverse-wavelength and transport orders
of its equation give

```text
k_a = partial_a S,
k_a k^a = 0,
2 k^a partial_a a + a nabla_a k^a = 0,
nabla_a(a^2 k^a) = 0.
```

On a compact caustic-free region with slow bounded coefficients, phase
averaging the canonical Hilbert tensor gives the leading result

```text
<T_ab> = (a^2/2) k_a k_b + lower-order terms.
```

The scalar mass is retained in the lower orders, not set to zero in the
parent. This approximation needs frequency large relative to the gap and
the background variation, but below the physical EFT cutoff.

For nonresonant independent rays with negligible interactions at the retained
order, `T_ab=sum_j I_j k_ja k_jb`, `I_j>=0`. In a local orthonormal frame,
necessary conditions are `rho>=0`, positive-semidefinite spatial pressure,
`trace(P)=rho`, and `|energy flux|<=rho` in units c=1. These are not asserted
to be a complete realizability test for every chosen set of rays.

This gives a concrete test of a proposed geometrical stress: it must lie in
the cone the actual parent waves generate. Arbitrary negative weights are
not allowed. Radiation-like stress is not cold galactic matter and does not
derive electric charge or a Maxwell gauge symmetry.

Related established work exists directly for Einstein equations:
[Huneau and Luk](https://arxiv.org/abs/2404.07659) discuss effective wave stresses,
transport constraints and geometric-optics constructions. Their review's
section 8.9.1 connects concentrated null shells with trapped-surface formation;
its other sections distinguish proved restricted results from open general
statements. This is a more direct mathematical bridge than identifying a
Navier–Stokes velocity with spacetime. None of those theorems automatically
covers the extra MTS operators or the entire strong-field evolution.

## 5. Construct the spherical leading wave–geometry pair

Use ingoing horizon-regular coordinates and an exterior annulus `r>=r_min>0`:

```text
ds^2 = -F(v,r) dv^2 + 2 dv dr + r^2 dOmega^2,
F = 1-2 mu(v)/r-Lambda r^2/3,
chi_0 = epsilon A(v) cos(v/epsilon)/r.
```

Choose a smooth incident amplitude A from characteristic data. The transport
equation fixes the `1/r` amplitude: `partial_r(r^2 a^2)=0`. Direct calculation
of the Einstein tensor yields

```text
(G_ab+Lambda g_ab) = [2 mu'(v)/r^2] (dv)_a (dv)_b,
<T_ab>_leading = [A(v)^2/(2 r^2)] (dv)_a (dv)_b,
mu'(v) = 2 pi G_N A(v)^2.
```

Thus wave intensity determines mass growth from the same gravitational
coupling. This is not choosing a metric and inventing an external force to
support it. A and an initial mass remain physical initial data; their actual
cosmological preparation has not been derived here.

For future null directions `l=partial_v+(F/2)partial_r`, `n=-partial_r`,
normalized by `g(l,n)=-1`, the spherical area expansions are

```text
theta_l = F/r,     theta_n = -2/r.
```

The leading model has marginal spheres at `F=0` and future-trapped spheres
where both displayed expansions are negative. For Lambda=0 the marginal
radius is `r=2mu`; nonzero Lambda stays in F. This is a local trapping
calculation, not a determination of a global event horizon. No denominator
`1/F` appears in these field coordinates at a simple horizon.

This leading geometry is the known Vaidya radiation geometry (with Lambda
retained), not a newly discovered MTS black hole. The contribution here is
its explicit use as a residual-correction starting point for our owned scalar.

## 6. Do not turn the leading average into a fictitious exact solution

For this actual scalar, direct differentiation gives

```text
X[chi_0] = 2 epsilon A^2 sin(theta)cos(theta)/r^3
         +epsilon^2[-2 A A'/r^3+F A^2/r^4]cos(theta)^2,
theta=v/epsilon,

(Box_g-m_chi^2)chi_0 = -U chi_0,
U = m_chi^2+2mu/r^3-2Lambda/3.
```

So the exact gradient is not null, and the seed is not an exact solution.
This avoids the real obstruction proved by
[Faraoni, Giusti and Fahim](https://doi.org/10.1140/epjc/s10052-021-09040-9):
a scalar with an exactly null gradient cannot source the spherical Vaidya
solution as an exact free massless scalar, because its field equation conflicts
with the required expansion. A high-frequency average is a different assertion.

There is also an order-one oscillating Einstein residual: `sin(theta)^2` is
not its mean `1/2` pointwise. Its leading vv component can be cancelled by
the first oscillatory mass correction, rather than silently erased:

```text
delta mu(v) = -2 pi G_N integral_(v0)^v A(s)^2 cos(2s/epsilon) ds,
delta mu' = -2 pi G_N A(v)^2 cos(2v/epsilon).
```

For `A(v0)=0`, integration by parts gives the explicit control

```text
|delta mu(v)| <= pi G_N epsilon
                [A(v)^2+integral_(v0)^v |(A(s)^2)'| ds].
```

The field remains small in amplitude while its first derivatives need not
be small. This correction cancels the leading fast vv mismatch only; the
rr, mixed, angular, scalar and constraint equations still have their own
subleading residuals. Replacing `mu` by `mu+delta mu` is not claimed to solve
them all. In particular, `T_rr=(partial_r chi)^2+...` is nonzero at finite
epsilon, whereas the simple Vaidya metric has zero rr Einstein component.

## 7. Derive the first scalar correction, including Q rather than dropping it

For the sign convention in section 3,

```text
E_chi = (Box_g-m_chi^2)chi-2 nabla_a[Q'(X)nabla^a chi].
```

For Q=b2 X^2 the additional seed residual at order epsilon is

```text
E_Q[chi_0] = epsilon b2 A^3/r^5 [-2cos(theta)+10cos(3theta)]
            +O(epsilon^2).
```

This follows by expanding `-4b2 nabla_a(X nabla^a chi_0)`, retaining both
the v and r derivatives; it is not an adjustable residual coefficient.
Higher powers X^n, n>=3, start at order epsilon^(n-1) on this one-ray seed
with fixed bounded coefficients and r_min>0.

Add

```text
chi_1 = epsilon^2 [B1(v,r) sin(theta)+B3(v,r) sin(3theta)].
```

At fixed leading metric, cancelling the two order-epsilon harmonics gives

```text
partial_r(r B1) = A U/2+b2 A^3/r^4,
partial_r(r B3) = -(5/3)b2 A^3/r^4.
```

Choosing zero correction at a declared reference radius r0 yields

```text
B1 = A/(2r) [(m_chi^2-2Lambda/3)(r-r0)
             +mu(v)(r0^-2-r^-2)]
     +b2 A^3/(3r)(r0^-3-r^-3),

B3 = 5b2 A^3/(9r)(r^-3-r0^-3).
```

These are explicit finite-order parent-field corrections, with the mass gap,
curvature and quartic coefficient retained. They cancel the displayed scalar
residual at order epsilon; this is not a convergence theorem for an infinite
series or a full coupled-metric error estimate. The calculation is on a bounded
annulus and a finite slow-time interval. Its coefficients diverge towards r=0,
so it cannot be advertised as a regular-centre construction.

The explicit smallness test is also available: compare `epsilon B1` and
`epsilon B3` with `A/r` using these formulas, or use absolute norms at amplitude
zeros. Merely having `epsilon m_chi<<1` does not control the cumulative phase
correction across an arbitrarily long propagation distance. In particular,
the mass contribution contains `epsilon m_chi^2 |r-r0|`.

## 8. Where the full MTS completion enters—and an extra interaction trap

With `K=1+2u_O4 C^2>0`, the quadratic eikonal stays null but transport becomes
`nabla_a(K a^2 k^a)=0`. On the spherical background it fixes
`a=A(v)/(r sqrt(K))`. This statement alone is not the gravitational source.
Indeed the kinetic part obeys `K a^2/2=A(v)^2/(2r^2)`: suppressing the scalar
amplitude with a large K does not suppress this transported gravitational
energy flux. This cancellation is another reason not to infer a regular core
from amplitude suppression alone; the full stress must decide the outcome.
The actual curvature-varied stress inherited from the September 7 derivation is

```text
T4_ab = 2u_O4 C^2 partial_a chi partial_b chi
       +8u_O4 nabla^c nabla^d(X C_acbd)
       +4u_O4 X R^cd C_acbd.
```

The second term can magnify fast derivatives. Small `2u_O4 C^2` or vanishing
mean X is not enough to bound it. Use the previously derived positive jet-norm
bound on the actual field, with the physical cutoff and C3/CFF/nonlocal budgets.
A sufficient scale hierarchy includes curvature and frequency control of the
form `|u_O4| |C| omega^2 << 1` as well as `|u_O4| |C|^2 << 1`, with the norm
constants, amplitude jets and gap checked on a specified region. One must not
send frequency to infinity at fixed EFT coefficients without proving validity.

Nor is every collection of individually null waves protected by X=0. For two
independent phases and null covectors k,l with k.l=kappa, let
`p=a k sin(theta)+b l sin(phi)`. Then

```text
<X>=0,          <X^2>=a^2 b^2 kappa^2,
<TQ_ab> = -2b2 a^2 b^2 kappa (k_a l_b+l_a k_b)
          +b2 a^2 b^2 kappa^2 g_ab.
```

For oppositely directed unit-frequency rays, this quartic stress is
`4b2 a^2 b^2 diag(1,1,1,-1)` in the ordered (t,x,y,z) covariant components.
It survives averaging and changes the radial pressure. Therefore a generic
many-wave stress cannot simply be imported from the independent-radiation
cone when this nonlinear contribution matters. It must be derived again
from the parent; large interactions also need the hyperbolicity test.

## 9. What this says about black holes, and the next construction

There are distinct questions: forming a trapped surface, evolving the full
theory through a regular horizon, resolving an interior curvature singularity,
and quantum information/evaporation. A positive radiation source can assist
the first; it is not by itself a mechanism for the latter two. On the canonical
branch `T_ab z^a z^b>=0` for null z, so the null Raychaudhuri equation adds
focusing, not a repulsive cutoff. This is not a no-go theorem for all MTS
higher-curvature or quantum terms.

Our next calculation is now explicit: use general spherical null-coordinate
metric functions rather than the one-function Vaidya seed, solve the rr and
mixed constraints together with the displayed scalar corrections, then include
the full O4 Hilbert contribution using the same coefficient sources. Compute
the error in both null expansions on a finite annulus. A strictly negative
expansion with an error smaller than its margin would establish a robust
trapping result in that declared domain. This does not require a regular-centre
claim and does not excuse leaving the scalar equation unsolved.

More explicitly, choose the general spherical gauge
`ds^2=-exp(2delta)F dv^2+2exp(delta)dvdr+r^2dOmega^2`, with
`F=1-2mu(v,r)/r-Lambda r^2/3`. Its normalized expansions are
`theta_l=exp(delta)F/r`, `theta_n=-2exp(-delta)/r`.
If the reference has `F0<=-sigma<0`, a sufficient trapping margin is
`2|delta mu_total|/r<sigma`, with finite real delta. Section 6 bounds the
first oscillatory part of delta mu_total; the other corrections are not
zero merely because that first part is small.

If we instead pursue a regular centre, the necessary spherical bounded-density
behaviour is `m_MS(r)=O(r^3)` after consistently including/subtracting Lambda.
The displayed incident-wave expansion does not give that. We must derive a
different controlled nonlinear regime, not declare a smooth core because the
total energy is finite. No empirical, local-GR, black-hole-completion or MTS
unification gate is promoted by this note.

## 10. Verification and preservation

The companions are `scripts/navier_stokes_source_audit_20260908.py` and
`scripts/motion_wave_bridge_20260908.py`. The latter checks finite-order symbolic
identities (Einstein tensor, scalar residual harmonics, transport, expansion
normalization and nonlinear crossed-wave averages), with G_N=1 in its symbolic
fixtures. It is not a numerical evolution or a formal PDE existence proof.
See their generated JSON outputs for actual completion and failures; no test
count is assumed merely from the scripts being written.

Completed at 2026-09-08T21:42:05Z: **29/29 symbolic checks passed**, SymPy
1.14.0, recorded in `source-intake/navier-stokes/20260908/wave-bridge-checks.json`.
The static source audit completed at 21:43:00Z. All five cited parent-source
paths were checked and exist. The downloaded archive and PDF are hashed in
the audit. The first slow text scanner was stopped and optimized before any
audit output existed; the downloads were preserved. This was not an interrupted
physics integration and did not alter the D4 or stellar evidence.

All new source acquisition and outputs are under this private directory.
The old stellar-relative validation and D4 numerical frontier are unchanged
and remain paused. This is not a restart or replacement of those frozen runs.
