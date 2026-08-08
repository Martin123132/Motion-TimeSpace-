# 4943 - Matter-source interior continuation, junction and fifth-force gate

Marker: `MTS_MATTER_SOURCE_INTERIOR_JUNCTION_NO_FIFTH_FORCE_4943`.

Date: `2026-07-13`.

Status: private analytic and source-executed checkpoint. On the selected
integrated-`H`, reflection-even parent, ordinary matter does not source one
motion scalar. The fixed-public-metric matter action contains no `psi`, the
effective action is even in `psi`, and inherited gravity-mediated contacts
begin at quadratic scalar order. The 4942 `psi=0` branch therefore extends
through ordinary material interiors and their nonsingular interfaces. Its
scalar charge and classical one-scalar fifth force vanish. Conservative
strict-EFT coefficient caps keep the quadratic interior operator positive on
Earth, Sun, white-dwarf and neutron-star density benchmarks. This closes the
declared matter-source continuation; it does not derive the public matter
functor from `psi`, test a reflection-breaking state, complete physical CFF
threshold matching, or promote full MTS/local GR.

## 1. Parent-owned matter source

Checkpoint 4916 owns the public metric as an independent integrated field
`H` modulo diffeomorphisms and declares

```text
Args(S_SM)={H,Phi_SM,theta_SM}.
```

Consequently, at fixed public metric,

```text
delta S_SM/delta psi=0.
```

The fixed-metric 1PI factorization from checkpoint 4919 is

```text
Gamma[H,psi,Phi_SM]
 =Gamma_X[H,psi]+Gamma_SM[H,Phi_SM].
```

All direct hidden-visible mixed functional derivatives therefore vanish.
This is stronger than assuming a small coupling: the single-scalar source is
absent in the selected parent action.

There is an exact diagonal motion reflection,

```text
(psi,X_Omega)->(-psi,-X_Omega),
```

with `H` and visible matter fixed. A reflection-even measure, state and
boundary functional imply

```text
Gamma_eff[H,psi,Phi_SM]
 =Gamma_eff[H,-psi,Phi_SM],

delta Gamma_eff/delta psi|psi=0=0.
```

Metric exchange does not evade this selection rule. The scalar stress starts
at `psi^2`, so internal metric lines generate scalar-pair vertices but no
one-scalar tadpole.

## 2. Six-derivative selection audit

The scalar degrees of the checkpoint-4930 basis are

```text
O1: degree 6;
O2: degree 4;
O3: degree 0;
O4: degree 2;
O5: degree 3.
```

`O1`, `O2` and `O4` have zero first variation at `psi=0`; `O3` is purely
metric. `O5` is odd under the selected reflection and is forbidden:

```text
u_O5=0
```

is invariant under reflection-preserving flow. Thus none of the five basis
operators supplies an ordinary-matter tadpole on this branch. This does not
calculate all of their beta functions.

## 3. Gravity-mediated interior quadratic operator

The inherited strict-EFT stress contact is

```text
Delta L_contact
 =M_R^-4[
   4a_C T_psi^mn T_mn^SM
  +2(a_R-2a_C/3)T_psi T_SM].
```

For a perfect fluid with density `rho`, pressure `p` and
`T=-rho+3p`, the local quadratic scalar density may be written

```text
L_psi^(2)
 =A_time (partial_t psi)^2/2
 -B_space |grad psi|^2/2
 -m_eff^2 psi^2/2,
```

where the symbolic expansion gives exactly

```text
A_time
 =Z[1+{8a_C rho+4(a_R+a_C/3)T}/M_R^4],

B_space
 =Z[1+{-8a_C p+4(a_R+a_C/3)T}/M_R^4],

m_eff^2
 =m^2[1+4(2a_R-a_C/3)T/M_R^4].
```

All three independent SymPy residuals are exactly zero. Every contact term is
even in `psi`; hence

```text
delta DeltaGamma_contact/delta psi|psi=partial psi=0=0.
```

## 4. Conservative interior stability bound

Under the dominant energy condition `|p|<=rho`, the coefficient shifts obey

```text
|Delta A|/Z, |Delta B|/Z
 <=[16|a_R|+(40/3)|a_C|]rho/M_R^4,

|Delta m^2|/m^2
 <=[32|a_R|+(16/3)|a_C|]rho/M_R^4.
```

The intentionally broad checkpoint-4878 strict-EFT control caps are

```text
|a_R|<=3.43214640967e56,
|a_C|<=1.02964392290e57.
```

They were applied to the source-backed Earth, Sun, one-solar-mass
white-dwarf and 1.4-solar-mass, 12-km neutron-star benchmarks at both their
mean density and ten times their mean density. The worst row is the latter
neutron-star proxy:

```text
|Delta A|/Z,|Delta B|/Z <=9.058001273285e-18,
|Delta c_psi^2|         <=1.811600254657e-17,
|Delta m^2|/m^2         <=7.764001091390e-18.
```

Every tested lower bound on `A_time`, `B_space` and `m_eff^2/m^2` is
positive. The same conservative denominator gives the proxy thresholds

```text
R_critical   =7.9247675353e9 m^-2,
rho_critical =4.2460231142e35 kg m^-3.
```

The sampled densities lie at least 17 orders below the kinetic threshold.
This is a strict-EFT corridor result, not a global theorem for arbitrary
matter states, singular surfaces or trans-Planckian curvature.

## 5. Interior equation and junctions

Combining the 4942 O4 term and the matter-dependent quadratic packet gives
the homogeneous equation

```text
nabla_mu(K_eff^munu nabla_nu psi)
 -m_eff^2 psi+O(psi^3)=0.
```

For a nonsingular material interface `Sigma`, variation and a pillbox limit
give

```text
[psi]_Sigma=0,

[n_mu K_eff^munu nabla_nu psi]_Sigma=0.
```

No reflection-odd surface action exists on the declared branch. Therefore
`psi=0` satisfies the interior equation, exterior equation, field continuity
and flux continuity simultaneously.

## 6. Scalar charge and fifth force

The asymptotic scalar charge is the flux

```text
Q_psi
 =surface integral n_mu K_eff^munu nabla_nu psi
 =0.
```

Equivalently, every visible-matter vertex with one external zero-background
motion scalar vanishes:

```text
Gamma_(psi-SM)^(1,n)|psi=0=0.
```

There is no classical single-scalar pole between ordinary bodies, so

```text
a_psi/a_N=0
```

at that order. Scalar-pair effects, metric-mediated quantum contacts, the
pure-C3 exterior residual and the CFF photon residual remain nonzero classes;
this checkpoint does not erase them.

## 7. What is now established

```text
direct ordinary-matter motion source at fixed H = exact zero;
reflection-even effective tadpole             = exact zero;
O5 on the selected branch                     = forbidden;
interior psi=0 continuation                    = derived;
field and flux junctions                      = derived;
ordinary-matter scalar charge                 = zero;
classical one-scalar fifth force              = zero;
strict-EFT interior quadratic stability       = bounded and passed;
arena-specific J_gap retuning                 = absent.
```

This is a material improvement over checkpoint 4942: the vacuum zero branch
is now a source-and-junction theorem inside the selected parent rather than
an exterior assumption.

## 8. Claim boundary

```text
selected integrated-H local matter branch     = closed at one-scalar order;
public H matter functor derived from psi      = false;
reflection-breaking state/source tested       = false;
singular or explicit odd surface action       = excluded, not tested;
complete QCD/hadronic and EW CFF matching     = open;
all remaining scalar beta functions           = open;
full visible-matter fixed point               = false;
full MTS fixed point                          = false;
local GR/Newton/Maxwell promotion              = false.
```

The zero fifth force follows from an exact parent selection rule and stable
homogeneous branch; it is not a fitted suppression coefficient. The parent
still takes the public metric and its visible matter functor as explicit
field-theoretic data, so this result must not be advertised as deriving all
visible matter from motion alone.

## 9. Next target

`4944-Y5-R2FR-complete-electroweak-spin1-and-hadronic-CFF-matching-or-total-photon-residual-bound.md`

Complete the physical curved-photon coefficient in one convention by adding
charged scalar, fermion, electroweak spin-1 and hadronic threshold pieces to
the fixed parent CFF coefficient, including signs and matching scales. Then
project the total coefficient onto the same local systems. If a threshold
cannot be calculated from the retained field content, bound it explicitly
rather than calling the parent-only value physical. Keep the 4943 source and
junction theorem fixed and do not retune `J_gap`.

No GitHub action is authorized.
