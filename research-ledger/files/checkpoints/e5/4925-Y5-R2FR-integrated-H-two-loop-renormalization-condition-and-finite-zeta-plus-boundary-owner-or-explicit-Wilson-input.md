# 4925 - Integrated-H two-loop boundary and one-Wilson matching

**Status:** The current parent does not derive a numerical finite Weyl-cubic
boundary, but the obstruction has now been reduced rather than merely listed.
The local change of variables from the densitized inverse metric
`H^{mu nu}` to `g_{mu nu}` has an exactly field-independent unit-magnitude
Jacobian in four dimensions, so it cannot hide a finite `C^3` term. The bare
coefficient and the scheme-dependent local metric/ghost finite part are also
not two independent unknowns: finite renormalization moves strength between
them while leaving one renormalized Wilson coefficient invariant.

The serious low-energy theory therefore needs **one signed parity-even
Weyl-cubic coefficient at one reference scale**, not the three placeholders
carried by the previous ledger. Its universal running, free massive-field
threshold basis, current nonclaim data envelope and induced-scale hierarchy
are now explicit.

Marker: MTS_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925.

No compact-GR, full MTS-to-GR or public theory claim is opened.

## 1. Parent ultraviolet audit

The selected gravity parent is

```text
Z = integral [D H D psi D X D Phi_SM / Vol(Diff x G_SM)]
    exp{i[S_H+S_psi+S_X+S_psiX+S_SM+S_gf+S_gh]}.
```

The four relevant facts are now separated.

1. `H^{mu nu}` is an independent integration variable, not merely an
   expectation value of the old fixed-background scalar.
2. The original scalar corpus does not define a microscopic `H` regulator,
   fixed point or all-operator bare action.
3. The induced condition `M_0^2(Lambda_UV)=0` concerns the Einstein operator.
   It has no logical implication for an independent six-derivative invariant.
4. The nonzero pure-gravity two-loop pole requires an `I1` counterterm and
   fixes its logarithmic running, but a first-order RG equation retains one
   integration constant.

Thus there is no parent-owned numerical boundary yet. The important change is
that the exact number of physical inputs at this order can now be proved.

## 2. Exact `H`-to-`g` measure calculation

In `d` dimensions let

```text
H^{mu nu}=sqrt(abs(g)) g^{mu nu},
N=d(d+1)/2.
```

For an independent symmetric variation,

```text
delta H^{mu nu}
 =sqrt(abs(g))[-g^{mu(alpha}g^{beta)nu}
                +(1/2)g^{mu nu}g^{alpha beta}]
  delta g_{alpha beta}.
```

After lowering the output indices, the dimensionless map on symmetric
tensors is

```text
h_{mu nu} -> -h_{mu nu}+(1/2)g_{mu nu} tr(h).
```

Its eigenvalue is `-1` on the `N-1` traceless directions and `(d-2)/2` on
the trace direction. The determinant of the index-raising map on symmetric
tensors is `(det g)^[-(d+1)]`. Hence

```text
abs det[dH/dg]
 =abs(d-2)/2 * abs(g)^[(d+1)(d-4)/4].
```

Exactly in four dimensions,

```text
abs det[dH/dg]=1.
```

For Lorentzian signature the independent-component determinant is `+1`; for
Euclidean signature it is `-1`. The sign and the infinite product of a
field-independent constant only normalize `Z`. They do not produce a local
curvature functional.

The executable calculation evaluates the complete `10 x 10` Jacobian for
eight random Euclidean and eight random Lorentzian metrics, plus `d=3,5`
scaling controls. Every row agrees with the analytic determinant below
`2e-8`.

This theorem applies to the displayed flat component measure `D H`. A
different non-flat DeWitt weight would be additional parent data and could
not be silently attributed to this coordinate transformation.

## 3. One-Wilson theorem

Checkpoint 4924 wrote the bare boundary and the local metric/ghost finite
piece separately. Their separation is scheme dependent. Under an arbitrary
finite renormalization,

```text
a_b'            =a_b+delta a,
a_H+gh,finite'  =a_H+gh,finite-delta a,
```

so

```text
a_UV^R(mu_U)=a_b+a_H+gh,finite
```

is invariant. A ringdown or scattering amplitude can constrain only the
renormalized sum.

Above identified massive thresholds, the ultraviolet matching equation is

```text
a_eff(Q)
 =a_UV^R(mu_U)
  +sum_i Delta a_i^threshold
  +beta_GS l_P^4 ln(Q/mu_U),

beta_GS=209/(1440 pi^2).
```

Below all thresholds one may instead define

```text
a_IR(Q_ref)
 =a_UV^R(mu_U)
  +all matched thresholds
  +beta_GS l_P^4 ln(Q_ref/mu_U).
```

This is one signed parameter. Writing

```text
a_IR=s_+ ell_IR^4
```

does not add a second parameter; `s_+` and `ell_IR` are the sign-magnitude
representation of the same coefficient.

This distinction matters:

- a competitive low-energy test requires one fitted or bounded `a_IR`;
- a fundamental MTS prediction requires deriving its microscopic
  decomposition;
- failure to derive that decomposition does not create several independent
  test parameters.

## 4. RG-invariant observable

At scale `Q`, the gravitational-QNM coordinate is

```text
alpha_ev(Q)=a_eff(Q)/M^4=s_+[ell_+(Q)/M]^4.
```

Changing the subtraction scale shifts `a_UV^R` oppositely to the explicit
logarithm, leaving `alpha_ev` invariant. Taking the reduced Planck energy as
the reference gives the following universal transfers:

| arena | `ln(Q/Mbar_Pl)` | `Delta a/l_P^4` | running length |
|---|---:|---:|---:|
| GW250114 remnant | `-90.033` | `-1.32399` | `1.734e-35 m` |
| 12 km neutron star | `-87.891` | `-1.29249` | `1.723e-35 m` |
| 10-solar-mass horizon | `-88.792` | `-1.30574` | `1.728e-35 m` |
| Earth radius | `-94.166` | `-1.38477` | `1.753e-35 m` |

The transfer is of order one Planck length even across roughly ninety
e-folds. Its length is about `3.5e-40` of the current robust QNM envelope, so
its coefficient contribution is about `1.5e-158` of that envelope. This is
an exact running calculation, not a claim that the finite boundary vanishes.

## 5. Boundary mechanisms actually tested

### 5.1 Induced Einstein zero

Rejected. `M_0^2=0` does not constrain `I1`; the two operators have different
dimensions and independent beta functions.

### 5.2 `H` coordinate measure

Closed with a zero contribution. Its four-dimensional point Jacobian is
field independent and cannot generate `I1`.

### 5.3 Minimal subtraction zero

Rejected as a physical prediction. A finite counterterm moves the zero, so
`a_R(mu_0)=0` is a convention or matching condition, not an observable
theorem.

### 5.4 Asymptotic safety

Retained as a genuine future mechanism, not adopted. The external
Einstein-Hilbert-plus-Goroff-Sagnotti functional-RG truncation finds the
dimensionless `C^3` direction irrelevant at its non-Gaussian fixed point.
That could remove an independent parameter if the actual MTS `H`, matter and
regulator flow lands on the same UV critical surface. The corpus has not
calculated that flow, and the truncation value cannot simply be imported.

### 5.5 Causality

Retained as a scale gate, not a zero proof. A sizeable correction to the
graviton three-point vertex in a weakly coupled UV completion requires a
higher-spin tower at a related scale. This constrains what a large coefficient
would mean; it does not derive its exact value or sign.

### 5.6 Selected route

Until a microscopic regulator or fixed point is constructed, use one explicit
signed `a_IR(Q_ref)` and constrain it with data. This is ordinary disciplined
gravity EFT, not an arena-specific closure function.

## 6. Massive threshold basis

For a massive minimally coupled species with `Q << m`, the Ricci-flat `I1`
threshold is

```text
zeta_+^i
 =r_i/[30240(4pi)^2 m_i^2],

r_scalar=+1,
r_Dirac=-4,
r_Proca=+3.
```

The scalar result reproduces checkpoint 4924. The Dirac and massive-vector
rows now give the exact spin-dependent continuation. Their parity-odd
partners vanish for these parity-even determinants.

For one species and no cancellation, the internal neutron-star one-percent
mass floors are approximately

```text
real scalar:     8.5767e-52 eV,
Dirac fermion:   1.7153e-51 eV,
massive vector:  1.4856e-51 eV.
```

These extraordinarily weak floors show why any ordinary massive visible
species is harmless in this channel. The remaining job is not discovering
the coefficient formula; it is assembling the actual MTS/visible spectrum,
threshold ordering and physical motion scale without double counting.

## 7. Current Wilson envelope

The checkpoint does not combine the polar and axial posteriors as though
their excitation weights were known. It carries the full robustness scan as
a conservative nonclaim envelope.

Using the maximum absolute 90-percent endpoint and the 95th-percentile
remnant mass gives

```text
abs(alpha_ev) <= 0.05390798,
ell_IR <= 49.228989 km,
abs(a_eff) <= (49.228989 km)^4.
```

For a complete coefficient known independently to be nonnegative, the
largest positive endpoint gives

```text
alpha_ev <= 0.03549245,
ell_IR <= 44.344691 km.
```

If `a_calc` denotes the explicit threshold and running sum, the exact affine
constraint on the ultraviolet Wilson input is

```text
-A_obs-a_calc <= a_UV^R(mu_U) <= A_obs-a_calc.
```

The internal neutron-star one-percent target is `ell_+<=3.473408 km`. The
conservative observational room is therefore larger by factor `14.1731` in
length and `4.03515e4` in the signed coefficient magnitude. Compact GR is not
promoted.

## 8. Induced-scale hierarchy

Newton matching gives the exact conditional relation

```text
W1 Lambda_UV^2=96 pi^2 Mbar_Pl^2.
```

Writing

```text
a_UV^R=c_W(hbar c/Lambda_UV)^4
```

shows what a dimensionless UV coefficient means. For the displayed positive
`W1=1` and `W1=4` anchors,

```text
Lambda_UV/Mbar_Pl =30.7812 or 15.3906,
ell(c_W=1)        =2.632e-36 m or 5.265e-36 m.
```

An order-one `c_W` would therefore lie roughly forty orders of magnitude in
length below the current QNM envelope and thirty-nine below the internal
neutron-star target. Conversely, present data permit dimensionless
coefficients of order `1e160` in this normalization. The hierarchy proves
that observations do not yet test Planck-natural `c_W`; it does **not** prove
that `c_W` is order one.

## 9. Verdict

Derived:

- the exact four-dimensional unit-magnitude `H`-to-`g` Jacobian;
- the absence of a hidden coordinate-measure `C^3` term;
- the collapse of bare and local metric/ghost finite pieces into one
  renormalized coefficient;
- the RG-invariant matching equation and Planck-to-arena transfer;
- the spin-0, spin-1/2 and spin-1 Ricci-flat threshold basis;
- the current signed and positive nonclaim Wilson envelopes;
- the exact induced-cutoff hierarchy conditional on `W1`.

Not derived:

- a microscopic numerical value or sign for `a_UV^R`;
- the actual MTS fixed-point trajectory or complete finite regulator;
- the physical motion scale and complete threshold spectrum;
- polarization excitation weights;
- compact-matter closure.

Current theory status:

```text
independent parity-even I1 test inputs = one;
H-coordinate Jacobian contribution    = derived zero;
universal two-loop running            = derived and negligible;
finite UV boundary value              = explicit Wilson input;
weak invariant-vacuum GR              = retained;
compact vacuum GR                     = not promoted;
compact matter and full MTS-to-GR     = not promoted.
```

## 10. Next target

`4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md`

That checkpoint should assemble the visible spin-0, spin-1/2 and spin-1
thresholds without using free quarks below confinement, derive or reject a
physical normalization of the motion scale, and then express the remainder
as the same single low-energy coefficient rather than reopening multiple
scheme placeholders.

No GitHub action is authorized.

## Sources

- Goroff and Sagnotti, two-loop pure-gravity divergence: https://doi.org/10.1016/0370-2693(85)91470-4
- Donoghue, gravity as an effective field theory: https://arxiv.org/abs/gr-qc/9405057
- Gies, Knorr, Lippoldt and Saueressig, `C^3` asymptotic-safety truncation: https://arxiv.org/abs/1601.01800
- Camanho, Edelstein, Maldacena and Zhiboedov, graviton causality constraints: https://arxiv.org/abs/1407.5597
- Goon, finite heavy-field gravity thresholds: https://arxiv.org/abs/1611.02705
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`
- `post-checkpoint-work/4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4925_integrated_H_two_loop_Wilson_boundary.py`
