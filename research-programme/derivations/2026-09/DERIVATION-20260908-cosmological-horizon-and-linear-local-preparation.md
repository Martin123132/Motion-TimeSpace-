# Cosmological horizon: conditional linear local preparation without deleting bound modes

Private derivation, 2026-09-08. This is a different, explicitly stated global
background from the Lambda=0 theorem of 2026-09-07; that theorem is preserved.
It concerns the selected quadratic motion operator, not nonlinear preparation
of the entire parent state or completion of the independent D4 calculation.

## 1. Parent input and precise hypotheses

Checkpoint 5211 retains Lambda_cal and has the selected equation

```text
nabla_mu[(1-2 P_X+2 u C^2) nabla^mu chi] - m^2 chi = 0.
```

Here P starts at quadratic order in X, so its linearization at chi=0 is
`nabla_mu(K nabla^mu chi)-m^2 chi=0`, with K=1+2u C^2.
There is no added friction term, direct matter source, or imposed zero
occupation of eigenmodes. Use the same fixed-background approximation as
the existing stellar spectral calculation, but now assume:

- A regular, static, spherical stellar interior, smoothly matched to a
  Schwarzschild--de Sitter exterior, on 0<=r<r_h.
- `ds^2=-N(r)^2 dt^2+a(r)^2 dr^2+r^2 dOmega^2`, with N,a positive inside
  the static patch. At the center a=1+O(r^2), N=N_c+O(r^2).
- In the exterior, `N^2=f=1-2 mu/r-H^2 r^2`, `a^2=1/f`, H^2=Lambda/3>0.
  The stellar surface is outside the smaller vacuum root; r_h is a simple
  cosmological root, `f'(r_h)<0`. The exterior normalization fixes t.
- `m^2>0` and K bounded above and strictly away from zero; K is smooth at
  the center and has a finite positive smooth limit at the horizon.
  The exterior C^2=48 mu^2/r^6 gives K=1+96u mu^2/r^6.
- Smooth coefficients, or ordinary flux-matched finite interfaces with no
  negative surface action. No artificial reflecting outer wall, no imposed
  nonzero horizon reservoir, and no time-dependent external forcing.

These hypotheses describe a conditional background class admitted by the
leading GR+Lambda branch. They do NOT establish that a real star embedded in
time-dependent FLRW is globally such a static solution. Higher operators,
backreaction and the parent's separate rho_local state are not eliminated.

## 2. Derive the correct radial spectral problem

For a spherical harmonic with angular index ell, the radial Hilbert measure,
quadratic form and Sturm--Liouville coefficients are

```text
w = r^2 a K/N,
p = r^2 N K/a,
q = N a [K ell(ell+1)+m^2 r^2],
L_ell phi = w^(-1)[-(p phi')'+q phi],
form[phi] = integral_0^rh [p |phi'|^2+q |phi|^2] dr.
```

The regular-center Friedrichs realization is nonnegative. A zero eigenvector
would have zero form, hence phi=0 because m^2>0 and N,a>0 in the interior.
Thus negative and zero eigenvalues are excluded by the original energy form,
not by the sign of a coordinate-dependent effective potential.

Define the tortoise coordinate s and the unitary Liouville field y by

```text
ds/dr=a/N, s(0)=0,
B=r sqrt(K), y=B phi,
integral w |phi|^2 dr = integral |y|^2 ds.
```

Direct substitution gives

```text
B L_ell(phi) = [-partial_s^2+V_ell(s)]y,
V_ell = B_ss/B + N^2 [ell(ell+1)/r^2+m^2/K].
```

This retains the derivatives of K. Replacing B by r when u is nonzero would
lose physical terms. At the center y=O(s^(ell+1)); for ell=0 this is the
regular Dirichlet condition, not a reflecting boundary inserted at the star.

At any allowed finite interface use continuity of phi and p phi_r. In the
new variables these are continuity of y/B and B^2 partial_s(y/B). The
displayed smooth potential applies on each side; jumps in B must not be
silently treated as a globally smooth Schrodinger potential. These real,
flux-preserving transmission conditions retain the positive form and the
tail argument. The executable controls below use smooth coefficients.

For a compactly supported y, writing b=B_s/B gives the useful exact check

```text
integral [|y_s-b y|^2+U |y|^2] ds
 = integral [|y_s|^2+(b_s+b^2+U)|y|^2] ds,
U=N^2[ell(ell+1)/r^2+m^2/K].
```

On a finite interval the right-hand expression must additionally subtract
`[b |y|^2]` to equal the left-hand expression. Boundary terms cannot be dropped
for a noncompact or finite-wall control.

## 3. Horizon asymptotics remove the positive mass threshold

Let kappa_h=-f'(r_h)/2>0. Near the cosmological horizon,

```text
f=2 kappa_h (r_h-r)+O((r_h-r)^2),
r_h-r=O(exp(-2 kappa_h s)),
N^2=O(exp(-2 kappa_h s)), B -> r_h sqrt(K_h)>0,
B_ss/B=O(exp(-2 kappa_h s)).
```

Consequently, for every fixed ell, V_ell has an exponentially integrable tail
and tends to ZERO, not m^2. The unbounded s interval is the natural static
patch domain. No finite-radius absorbing boundary has been substituted.

For energy k^2>0, the integrable-tail ODE has independent solutions with
asymptotics exp(+iks) and exp(-iks), including their derivatives. Any nonzero
linear combination has nonzero mean square on the tail and is not L2(ds).
Thus no positive-energy eigenfunction can satisfy the horizon condition.
Together with the positive-form argument:

```text
point spectrum(L_ell) = empty.
```

The conclusion concerns true normalizable stationary modes, not long-lived
resonances. A potential well in the interior may still produce very slow
escape. A finite-box discretization will produce discrete eigenvalues even
for this continuous-spectrum problem and cannot establish trapping.

For completeness, the outgoing tail solution has nonzero conserved flux
at real k>0. A regular-center real solution has zero flux. They cannot be
proportional, so their Wronskian is nonzero there. The resulting half-line
spectral density is absolutely continuous on (0,infinity). The finite core
and the regular angular endpoint do not change the integrable-tail argument.
Zero has no eigenmass; a singular continuous measure cannot be supported only
at zero. Hence the selected radial realizations are purely absolutely
continuous, and so is their countable spherical-harmonic direct sum.

The standard short-range spectral and local-compactness results used here
are described by Teschl, section 9.7 (especially Lemma 9.37/Theorem 9.38 and
the half-line remark) and Theorem 5.6. The center condition, positive form,
K-dependent transform and horizon asymptotics above supply the application
to this operator, rather than citing the reference as an MTS theorem.
[Teschl, author-hosted 2009 online edition](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf).

## 4. What linear preparation actually follows

Take finite-energy data in the completion of compact regular data under
`2E=||chi_t||_w^2+form[chi]`. The unforced linear evolution conserves this
global energy. On every fixed compact spatial region Omega strictly inside
the horizon, define E_Omega using the same nonnegative energy density.

To justify local decay, first restrict to finitely many angular modes and a
spectral band `[delta,M]` with delta>0. Local elliptic regularity and compact
Sobolev embedding make the localized velocity, gradient and mass-energy
observations compact on that band. Apply continuous-spectrum time-average
decay, or absolute-continuity decay, to the groups exp(+-it sqrt(L)). The
spectral-band and angular truncation errors are uniformly bounded by their
conserved total energy. Removing those cutoffs in the energy norm gives

```text
E_Omega(t) -> 0  as t -> infinity.
```

The weaker time-average statement follows already from absence of point
spectrum plus the same compactness/cutoff argument. Neither statement
requires declaring the initial data orthogonal to bound states: under these
hypotheses there are no such states. The global energy need not vanish;
local energy is carried toward the horizon, consistently with unitary
evolution on the complete tortoise domain. This does not evade or contradict
the previous prohibition on unitary purification of a whole state.

The earlier full Hilbert-source estimate for a smooth compactly supported
metric variation h, translated in static time, has the form

```text
|Q_can[h_T]+Q_O4[h_T]|
 <= C_h integral_T^(T+Delta) E_Omega(t) dt -> 0.
```

K, curvature, and h through two derivatives remain in C_h, as derived on
2026-09-07. Compact-support integration by parts is local and does not
require Lambda=0; the bounds must use the PRESENT geometry's Ricci tensor,
including Lambda. One must not import the old zero-Lambda numerical C_h.
This is a linear motion-sector weak-source relaxation theorem, not a
pointwise PPN bound or relaxation of all parent fields and operators.

## 5. Exact controls and important counterexamples

In pure de Sitter, mu=0 and C^2=0, so K=1 for either sign of u. Then

```text
r=tanh(Hs)/H,
V_ell=(1-H^2 r^2)[m^2+ell(ell+1)/r^2-2H^2].
```

- For ell=0 and m^2=2H^2, V=0 exactly. The regular half-line wave equation
  is solved by odd extension; compact pulses leave any compact region after
  a finite time. This is a GR+scalar baseline, not distinctive MTS evidence.
- For m^2=H^2, V=-H^2 sech^2(Hs) is negative but the original energy form is
  positive. Negative effective potential alone is NOT a tachyon proof.
- At m=0, ell=0, y=tanh(Hs) is a bounded zero resonance, not an L2 bound
  state. The constant chi is not forced to zero. This is outside m^2>0.
- For the excluded m^2=-4H^2, y=tanh(Hs) sech(Hs) is an L2 half-line mode
  with eigenvalue -H^2. This supplies a genuine growing-mode negative control.
- H->0 is a nonuniform global limit: the horizon moves to infinity and the
  asymptotic potential changes from zero to m^2. The old Lambda=0 stellar
  bound modes do not contradict the positive-Lambda theorem.

Bony and Hafner's Schwarzschild--de Sitter wave analysis independently
emphasizes the zero-resonance distinction. Its black-hole boundary conditions
and decay rates are not imported as a theorem for our stellar interior.
[Bony and Hafner, arXiv:0706.0350](https://arxiv.org/abs/0706.0350).

There is no finite astronomical timescale guarantee here. Already the
homogeneous pure-de-Sitter equation in FLRW time is
`chi_tt+3H chi_t+m^2 chi=0`, with exponents
`-3H/2 +- sqrt(9H^2/4-m^2)`. For m<<H the slow exponent is approximately
`-m^2/(3H)`. This illustrates why an asymptotic preparation theorem is not
evidence of rapid local relaxation. Homogeneous data are not finite-total-
energy localized data of the static-patch theorem; the example is a separate
timescale warning, not an imported rate for a star.

## 6. Sources, next execution and scope

Local inputs:

- `5211-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md`
- `DERIVATION-20260906-parent-trapped-energy-bound.md`
- `DERIVATION-20260907-whole-star-localization-and-static-validity.md`

The companion `scripts/parent_horizon_preparation_20260908.py` checks the
Liouville transform, boundary identity, de-Sitter controls, finite-pulse
propagation and timescale roots. These algebra/implementation checks do not
numerically certify the continuum spectrum or construct a real Lambda-TOV
star. Run it only after the current E06 worker has exited safely.

Next physical task: obtain a sourced positive-Lambda stellar/cosmological
background and bound finite-time leakage or persistent forcing in that
background. Nonlinear mode feeding, rho_local preparation, metric/fluid
backreaction and higher operators remain separate requirements. No full MTS,
all-operator local GR, measured PPN or empirical preparation pass is claimed.
