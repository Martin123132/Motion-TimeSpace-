# 4932 - Photon-graviton functional flow and MTS portal projection

Marker: `MTS_PHOTON_GRAVITON_FLOW_MTS_PROJECTION_4932`.

Date: `2026-07-12`.

Status: private source-backed derivation checkpoint; external fixed-point
comparator and exact MTS normalization map; no full-MTS, local-GR, Maxwell
emergence or public evidence claim.

## 1. Question and decisive result

Checkpoint 4931 left the nonperturbative gauge-curvature portal as an unknown
functional-trace problem. A direct source hunt has now found a calculation in
the same essential photon-gravity operator language:

```text
Benjamin Knorr and Alessia Platania,
arXiv:2405.08860,
photon-graviton essential FRG through four derivatives.
```

The primary TeX, PDF, source archive and official general-regulator
Mathematica notebook are locally hash locked. The paper supplies a real
interacting, GR-connected fixed point with

```text
FP1:
  g*       = 0.131,
  g_plus*  = 0.351,
  g_minus* = 3.327,
  g_CFF*   = 0.00375,
  theta    = {1.845,-0.239+/-0.0155 i,-0.291}.
```

This rejects a generic theorem that the photon `CFF` portal must vanish at an
interacting gravitational fixed point. It does not prove that the enlarged
MTS fixed point equals FP1.

The exact operator normalization is

```text
c_gamma=G_CFF,
u_gamma=k^2 c_gamma=g_CFF.
```

The most predictive FP1 trajectory has the published infrared Wilson ratio

```text
W_C=lim G_CFF/(16pi G_N)=0.000550.
```

If, and only if, the MTS parent inherits that external trajectory, then

```text
c_gamma^parent,FP1,IR
  =16pi ell_P^2 W_C
  =7.221914138634598e-72 m^2.
```

This is a source-backed conditional projection, not an MTS fitted parameter
and not the total low-energy electromagnetic coefficient.

## 2. Source and reproducibility boundary

The source packet is recorded in
`source-intake/functional_rg/4932/PROVENANCE.md`. It contains:

```text
2405.08860.pdf,
2405.08860-source.tar,
src-2405.08860/WGCqg.tex,
RHS_general_regulator.nb,
DataCite and Mendeley metadata snapshots.
```

The downloaded notebook hash exactly equals the official Mendeley API hash.
It has 18 stored `BoxData` input cells and no stored `Output` cells. It gives
the general-regulator functional-trace inputs, including `RHSCFFint`, but a
compatible Wolfram/xAct execution environment is not installed. Therefore:

```text
source action and scheme                 = independently audited;
fixed-point table and IR Wilson endpoint = independently transcribed/checked;
SI conversion and MTS map                = independently calculated;
complete rational beta RHS               = source locked, not re-executed.
```

No line in this checkpoint represents the source endpoints as a fresh
independent evaluation of its Mathematica trace.

## 3. Essential operator closure

The Lorentzian source action is

```text
Gamma=int sqrt(g)[
  R/(16pi G_N)+G_E Euler-F2
  +G_F2sq(F2)^2+G_F4 F4+G_CFF CFF].
```

Here

```text
F2=F_mn F^mn/4,
F4=F^m_n F^n_r F^r_s F^s_m/4.
```

The dimensionless essential coordinates are

```text
g=k^2 G_N,
g_F2sq=k^4 G_F2sq,
g_F4=k^4 G_F4,
g_CFF=k^2 G_CFF,

g_plus =(g_F2sq+g_F4)/2,
g_minus=(g_F2sq-g_F4)/2.
```

The central operator-count result is

```text
the CFF flow is not closed in {g,g_CFF};
the minimal source-complete four-derivative flow is
{g,g_plus,g_minus,g_CFF}.
```

Both independent `F^4` directions must be included in the next MTS trace.
Setting them to zero would repeat the very closure assumption this programme
is trying to eliminate.

The Euler term is topological and does not feed the other beta functions.
The redundant completion

```text
R^2, S_mn S^mn, F Delta F, R F^2, S_mn F^m_a F^{an}
```

is needed to perform the projection but is removed by the essential
field-redefinition kernel rather than counted as independent observables.

## 4. Scheme comparison

The external calculation uses

```text
linear metric split,
background-field approximation,
harmonic gravity and photon gauges,
essential k-dependent field redefinitions,
natural endomorphisms,
Litim regulator,
a selected trajectory with vanishing dimensionful Lambda in the IR.
```

This is structurally close to the natural-essential MTS route selected in
checkpoint 4928. It is not identical ownership. The external truncation has
no MTS motion scalar, no full Standard Model completion and no six-derivative
Weyl-cubic `C3` direction. Scheme similarity therefore licenses an embedding
test, not a splice.

## 5. Published fixed points and signed stability

The published source table is

| point | `g*` | `g_plus*` | `g_minus*` | `g_CFF*` | critical exponents `theta` | relevant directions |
|---|---:|---:|---:|---:|---|---:|
| GFP | 0 | 0 | 0 | 0 | `{-4,-4,-2,-2}` | 0 |
| MFP | 0 | -12.577 | -10.383 | -0.0901 | `{4.227,-0.477,-0.723,-1.041}` | 1 |
| FP1 | 0.131 | 0.351 | 3.327 | 0.00375 | `{1.845,-0.239+/-0.0155i,-0.291}` | 1 |
| FP2 | 0.126 | -0.308 | 4.001 | -0.00410 | `{1.936,0.184,-0.141,-0.236}` | 2 |

With beta-matrix eigenvalues `lambda=-theta`, FP1 has

```text
lambda_FP1={-1.845,0.239-/+0.0155 i,0.291}.
```

Its distance to the imaginary axis is therefore

```text
delta_FP1=0.239.
```

For a block-diagonal source comparator enlarged by unknown MTS mixing, a
sufficient Bauer-Fike-style modal condition for preserving the signed index
is

```text
||E_modal||_2<0.239.
```

This is about `7.866` times tighter than the `1.88` comparator used before the
photon block was known. FP2 gives the still tighter value `0.141`. The MFP is
not selected for the local-GR route because `g*=0` makes it a gravity-free
ultraviolet completion.

The norm inequality is sufficient, not necessary, and its modal basis must be
declared. The exact enlarged stability matrix remains the preferred test.

## 6. Infrared trajectory and Wilson projection

Near the Gaussian infrared endpoint, the source finds

```text
g(k)      ~g_IR (k/k0)^2,
g_plus(k) ~g_IR^2 (k/k0)^4 f_plus,
g_minus(k)~g_IR^2 (k/k0)^4[
             f_minus-(548/15)log(c_l g_IR(k/k0)^2)],
g_CFF(k)  ~g_IR (k/k0)^2 f_c,
G_N       =g_IR/k0^2.
```

For the unique GR-connected FP1 separatrix,

```text
W_plus =0.00792,
W_C    =0.000550,
W_minus=0.0955 at c_l=16pi.
```

`W_minus` is logarithmic-subtraction dependent. `W_C` has no corresponding
log ambiguity in this truncation.

The ultraviolet ratio is

```text
g_CFF*/(16pi g*)=0.0005694953,
```

which differs from the infrared `W_C` by `3.5446%`. This is a useful guard:
one must integrate the separatrix rather than identify a UV coordinate ratio
with an IR Wilson coefficient.

Using

```text
ell_P=sqrt(hbar G_SI/c^3)=1.616255024423705e-35 m,
```

the conditional FP1 parent contribution is

```text
c_gamma^parent,FP1,IR=7.221914138634598e-72 m^2,
sqrt(c_gamma^parent)=2.687361929222523e-36 m.
```

## 7. Electromagnetic hierarchy

Checkpoint 4931 derived the electron threshold

```text
Delta c_gamma,e=-9.621568578321357e-31 m^2.
```

Consequently

```text
|Delta c_gamma,e|/|c_gamma^parent,FP1,IR|
  =1.332274019549677e41.
```

The known electron QED threshold is therefore forty-one orders of magnitude
larger than the conditional quantum-gravity parent portal. The proper
low-energy ledger remains

```text
c_gamma^IR
  =c_gamma^parent
   +c_gamma^free-leptons
   +c_gamma^QCD/hadronic
   +c_gamma^EW-spin1
   +... .
```

Thus the external FP1 result, if inherited, would make the ultraviolet parent
portal negligible for current low-energy propagation tests. It would not
replace the QED/QCD/EW threshold calculation.

## 8. Positivity firewall

At the published FP1 endpoint and `c_l=16pi`, algebra gives

```text
W_F2sq=W_plus+W_minus=0.10342,
W_F4  =W_plus-W_minus=-0.08758,

W_F2sq+2W_F4-2|W_C|=-0.07284.
```

The nominal inequalities

```text
W_F2sq+2W_F4-2|W_C|>0,
W_F4>0
```

are therefore violated at that endpoint. This is recorded, not hidden. It is
not turned into an MTS rejection because the source explicitly discusses the
unsettled applicability of strict gravity-free positivity inequalities in the
presence of a massless graviton and logarithmic subtraction. The result is a
future common-scheme consistency test, not a current binary gate.

## 9. Exact inheritance contract

The external FP1 result becomes an MTS prediction only if all of the following
close:

```text
I1  retain the exact canonical photon/CFF normalization;
I2  include both essential F4 directions;
I3  include C3 and calculate C3-CFF-F4 mixing;
I4  include the MTS motion and selected visible-matter Hessians;
I5  use one declared essential field-redefinition/gauge/regulator scheme;
I6  solve the enlarged common-zero problem;
I7  preserve the desired signed index exactly or prove ||E_modal||_2<0.239;
I8  integrate a GR-connected infrared trajectory and calculate its W_C.
```

Only `I1` is closed now. `I2` is a concrete correction to the next truncation;
`I3-I8` are calculations, not excuses to insert zero coefficients.

## 10. Decision

Checkpoint 4932 advances the portal problem materially:

```text
real nonzero interacting photon-gravity portal fixed point = sourced;
GR-connected one-relevant-direction FP1                    = sourced;
exact MTS CFF normalization map                            = closed;
minimal four-derivative photon closure                     = corrected;
unique external FP1 infrared W_C                           = sourced;
conditional SI parent coefficient                         = calculated;
QED-versus-QG hierarchy                                    = calculated;
signed mixing tolerance                                    = tightened to 0.239;
full rational source notebook                              = acquired, not re-executed;
full MTS enlarged fixed point                              = open;
MTS local-GR/Maxwell promotion                             = false.
```

The next target is not another missing-input ledger. It is the smallest real
enlargement that can decide inheritance:

```text
4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md
```

That checkpoint must construct or bound the combined `C3-CFF-F4` stability
block. If it cannot satisfy the `0.239` gate, FP1 remains an external
comparison rather than the MTS parent.

## 11. Generated evidence

The executable generator is
`scripts/Y5_R2FR_4932_photon_graviton_flow_MTS_projection.py`. It writes:

```text
P8_Y5_R2FR_4932_SOURCE_SCHEME.csv
P8_Y5_R2FR_4932_ESSENTIAL_OPERATOR_CLOSURE.csv
P8_Y5_R2FR_4932_PUBLISHED_FIXED_POINTS.csv
P8_Y5_R2FR_4932_SIGNED_STABILITY.csv
P8_Y5_R2FR_4932_MTS_NORMALIZATION_MAP.csv
P8_Y5_R2FR_4932_FP1_IR_WILSON.csv
P8_Y5_R2FR_4932_FP1_SI_PROJECTION.csv
P8_Y5_R2FR_4932_QED_VS_QG_HIERARCHY.csv
P8_Y5_R2FR_4932_POSITIVITY_COMBINATIONS.csv
P8_Y5_R2FR_4932_MTS_INHERITANCE_GATE.csv
P8_Y5_R2FR_4932_SOURCE_REGISTER.csv
P8_Y5_R2FR_4932_GATE_DECISION.csv
```

Every row remains `valid_for_claim=false` because this is a private MTS
inheritance test, not a completed full-theory prediction.
