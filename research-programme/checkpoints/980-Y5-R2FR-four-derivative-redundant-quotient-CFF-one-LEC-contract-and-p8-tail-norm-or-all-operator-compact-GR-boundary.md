# 4964 - Four-derivative quotient, one-CFF-LEC contract and p8 tail norm

Marker: `MTS_4964_R2C2_QUOTIENT_CFF_LEC_P8_TAIL`.

Formal marker: `PPC4161_R2C2_QUOTIENT_CFF_LEC_P8_TAIL_4964`.

Date: `2026-07-13`.

Status: private analytic and source-locked checkpoint. This checkpoint removes
an incorrectly posed matching target rather than choosing convenient finite
coefficients. At first strict-EFT order, the two local gravitational
four-derivative coordinates `a_R` and `a_C` are redundant in neutral vacuum.
Their invariant content on matter support is a stress-contact packet, which
must be matched together with the independent matter/EOS/worldline basis.
The curvature-photon operator is different: it retains one physical
coefficient `c_IR`, whose action, field equation, stress and flat limit are
derived but whose finite QCD contribution is not numerically calibrated. The
first uncalculated `p>=8` compact tail is converted into an exact conditional
response-norm bound and eleven numerical coefficient budgets. Exact
all-operator compact GR and full MTS remain false.

## 1. Why the old target was over-counted

Checkpoints 4876, 4884 and 4918 correctly separated universal running from
finite matching in

```text
Gamma_4=int sqrt(-g)[a_R R^2+a_C C_mnrs C^mnrs].
```

They then retained the total finite `a_R,a_C` values as two open matching
coordinates. That is valid as off-shell bookkeeping but over-counts the
neutral-vacuum observable problem at first EFT order. Local field
redefinitions move those two coefficients between the gravitational and
matter bases without changing on-shell observables.

A separate bookkeeping error is explicitly prevented here. The 4932
coordinates are

```text
g_plus =(g_F2sq+g_F4)/2,
g_minus=(g_F2sq-g_F4)/2.
```

Consequently the `W_plus,W_minus` limits used in 4935 are photon-quartic
`F^4` coordinates. They are not numerical values of gravitational `a_R,a_C`
and are not used as such.

## 2. Exact four-dimensional curvature quotient

In four dimensions,

```text
C_mnrs C^mnrs=E4+2 R_mn R^mn-(2/3)R^2,
```

where `E4` is the Euler density. Introduce the local inverse-metric change of
variables

```text
delta g^mn=(2/M_R^2)
  [-2a_C R^mn+(a_R+a_C/3)R g^mn].
```

The Einstein-Hilbert variation is

```text
delta S_EH=(M_R^2/2) int sqrt(-g) G_mn delta g^mn.
```

Using `G_mn R^mn=R_mn R^mn-R^2/2` and `G^m_m=-R`, its local bulk density is

```text
delta L_EH
 =-2a_C R_mnR^mn+(2a_C/3-a_R)R^2.
```

This cancels

```text
L_4-a_C E4
 =2a_C R_mnR^mn+(a_R-2a_C/3)R^2
```

exactly. The generator checks this with rational SymPy algebra and obtains a
zero remainder.

The result is deliberately scoped:

```text
independent neutral-vacuum p4 parameters at first EFT order = 0.
```

It applies to the selected strict EFT and positive-gap/on-shell neutral
vacuum sector. It does not declare the separately resummed fourth-order pole
theory equivalent, discard the Euler boundary/topology, remove nonlocal loop
form factors, or erase terms generated at second and higher orders in the
field redefinition.

## 3. Where the four-derivative information goes

With the Hilbert convention

```text
delta S_m=-1/2 int sqrt(-g) T_mn delta g^mn
```

and the leading Einstein equation

```text
R_mn=(T_mn-T g_mn/2)/M_R^2,
R=-T/M_R^2,
```

the same change of variables gives

```text
Delta L_contact
 =[2a_C T_mnT^mn+(a_R-2a_C/3)T^2]/M_R^4.
```

The symbolic difference between the direct substitution and this expression
is zero. This reproduces and consolidates the earlier stress-contact formulas
without interpreting `a_R,a_C` as two exterior-vacuum observables.

The contact packet is physical only after it is combined with every
independent matter, EOS, finite-size and worldline counterterm in the same
basis. Therefore:

```text
finite a_R/a_C exterior-vacuum matching obstruction = removed at p4;
full compact-matter contact matching                 = still open.
```

This is not a zero assumption. It is the equivalence-theorem quotient and an
explicit relocation of the open physics.

## 4. Curvature-photon coefficient is not redundant

The retained Ricci-flat CP-even electromagnetic action is

```text
S_EM=int sqrt(-g)[-F^2/4+c_IR C_mnrs F^mn F^rs]
     +int sqrt(-g) A_m J^m.
```

Checkpoint 4946 established

```text
nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n,

T_EM_mn=F_ma F_n^a-g_mn F^2/4+c_IR H_CFF_mn.
```

The same `c_IR` controls propagation and Hilbert stress. In flat spacetime,
`C_mnrs=0`, so standard Maxwell propagation and stress are exact for every
value of `c_IR`.

The coefficient count is one, not zero and not one per arena:

```text
c_IR=c_nonQCD+c_QCD^r(mu).
```

The source-backed non-QCD interval is

```text
-9.621794773634823e-31 m^2
 <=c_nonQCD<=
-9.621794073504142e-31 m^2.
```

The exact 4946 counterterm theorem proves that flat HVP, one-current hadron
form factors, one-stress gravitational form factors and trace-anomaly data do
not determine the finite transverse-traceless QCD contact. A numeric
`c_QCD^r` would therefore be fabricated if inferred from those data alone.
The legitimate completion is one lattice TJJ match or one robust
curved-photon calibration, followed by universal transfer without retuning.

For scale reference only, the existing transfer functions give a `10^-6`
polarization split at

```text
|c_IR|=69.65480735584059 m^2  for the declared neutron-star benchmark,
|c_IR|=145.37022509445288 m^2 for the 10-solar-mass horizon proxy.
```

The historical geometry envelope `1.3544193104492175e15 m^2` is valid only
as a conditional weak Earth/Sun control and is not a physical QCD match.

## 5. Exact conditional p8-plus tail theorem

After quotienting Ricci/EOM-redundant terms, define the dimensionless compact
curvature control

```text
chi=l_P^2 M_geo/r^3.
```

Let `C_n` be the aggregate response norm of all on-shell operators containing
`n` curvature powers at derivative order `p=2n`. This definition includes
the tensor-contraction and operator-count norm; it is not one arbitrarily
chosen Wilson coefficient. Suppose the omitted coefficients obey

```text
C_n<=C_8 R^(n-4),  n>=4,
R chi<1.
```

Then the entire omitted local tail satisfies the exact geometric-series
bound

```text
epsilon_p8plus
 <=sum_(n>=4) C_n chi^(n-1)
 <=C_8 chi^3/(1-R chi).
```

The one-percent compact gate is therefore equivalent to

```text
C_8<=0.01(1-R chi)/chi^3.
```

This is a theorem conditional on the aggregate coefficient norm and its
growth radius. It is not a naturalness assumption and does not set either
quantity to one.

## 6. Eleven compact coefficient budgets

The nine 4962 EOS masses/radii were cross-checked against the independent
4883 response table. A declared `1.4 M_sun,12 km` benchmark and a `10 M_sun`
Schwarzschild horizon complete the eleven rows.

The most restrictive object is the near-turning SLY4 star:

```text
chi_max=6.912516257600412e-79,

C_8<3.027551244686395e232
  for the explicitly labelled unit-growth benchmark R=1,

C_8<1.513775622343198e232
  if R chi=1/2.
```

For comparison, the selected 4963 acceleration-response normalization is

```text
C_6=140(16pi)|A_C3^S|<=0.15518290951781644.
```

Thus a p8 term would need an aggregate response enhancement of at least
`1.950956618930259e233` relative to that selected p6 response to reach one
percent under the unit-growth benchmark. The corresponding
response-equivalent length is about `9.023 km`. This length is a translation
of the norm budget, not a measured cutoff or a claim of Planck-scale
naturalness.

## 7. Why the remaining tail cannot be proved from p6 data

Consider two actions

```text
Gamma_A=Gamma_p6,
Gamma_B=Gamma_p6+delta c_8 O_8.
```

Every projector and beta function restricted to `p<=6` is identical in the
two theories, while a `p8` observable changes with `delta c_8`. Therefore no
finite p6 trajectory, however accurately solved, can prove a p8 coefficient
or convergence radius without an additional UV-flow projection, amplitude
or analyticity input. This is an exact non-identifiability result, not a
request for another missing-input ledger.

The practical next calculation is consequently a minimal Ricci-flat p8
on-shell basis and its functional-flow projection. That can supply the first
`C_8` row and begin a convergence test. Until then the scientifically proper
claim is order-by-order EFT control, not exact equality after every possible
higher operator is included.

## 8. Decision

```text
R2/C2 independent neutral-vacuum p4 matching     = quotient removes it;
R2/C2 invariant matter contact packet            = derived;
full EOS/worldline contact matching              = open;
CFF retained physical coefficient count          = one;
CFF action/equation/stress/flat limit             = derived;
physical numeric c_IR calibration                 = open;
p8-plus conditional response-norm theorem         = derived;
parent C8 and convergence-radius bound            = open;
selected static compact GR through declared p6    = retained;
exact all-operator compact GR                     = false;
full MTS                                           = false.
```

The decisive improvement is that finite `a_R,a_C` no longer sit in the
vacuum calibration ledger as two unexplained universal numbers. Their vacuum
role is quotient-redundant at first EFT order, their matter role is an
explicit contact packet, and the genuinely nonredundant open coordinates are
now separated cleanly: one curved-photon LEC and the unprojected p8-plus
on-shell tower.

## 9. Generated evidence

- `post-checkpoint-work/scripts/Y5_R2FR_4964_four_derivative_quotient_CFF_LEC_and_p8_tail.py`
- `post-checkpoint-work/source-intake/functional_rg/4964/four_derivative_quotient_CFF_p8_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4964/four_derivative_field_redefinition_quotient.csv`
- `post-checkpoint-work/source-intake/functional_rg/4964/finite_matching_parameter_count.csv`
- `post-checkpoint-work/source-intake/functional_rg/4964/CFF_one_LEC_calibration_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4964/p8plus_tail_norm_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4964/compact_all_operator_decision.csv`
- `post-checkpoint-work/source-intake/functional_rg/4964/PROVENANCE.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4964_four_derivative_quotient_CFF_LEC_and_p8_tail_validation.py`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4964_VALIDATION.csv` (`26/26` checks pass)

Next: `4965-Y5-R2FR-minimal-Ricci-flat-p8-on-shell-basis-and-functional-flow-projection-or-order-by-order-EFT-boundary.md`.

No GitHub action is authorized.
