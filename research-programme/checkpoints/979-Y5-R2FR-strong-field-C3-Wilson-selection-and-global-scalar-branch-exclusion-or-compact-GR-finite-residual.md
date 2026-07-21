# 4963 - Strong-field C3 selection and nonlinear scalar-branch theorem

Marker: `MTS_4963_C3_SELECTION_GLOBAL_SCALAR_BRANCH`.

Date: `2026-07-13`.

Status: private analytic, source-locked and numerically executed checkpoint.
The complete declared CP-even six-derivative zero-motion-state trajectory now
selects a finite parity-even Weyl-cubic coordinate in its locked natural
source scheme. Its compact residual is negligible even after a deliberately
conservative finite-gap and raw-running enlargement. Independently, an exact
static multiplier identity excludes every regular disconnected scalarized
branch that remains inside the certified healthy `x<=0.1` functional chart.
This promotes the selected healthy static `p6` compact sector, not exact
all-operator compact GR or full MTS.

## 1. What is being decided

Checkpoint 4962 left two verdict-changing compact residuals:

1. the physical ownership and size of the parity-even `C3` Wilson term;
2. a possible disconnected nonlinear scalarized branch, despite the absence
   of a perturbative zero mode.

The calculation here attacks both. It does not reopen the already-derived
universal weak source residue, add another value of `G`, fit a compact-body
coefficient, or use the observational GW250114 envelope as a prediction.

## 2. Declared `p6` C3 source closure

On the selected `psi=0`, reflection-even branch, the source-locked
six-derivative basis is

```text
O1=X^3,
O2=X(nabla nabla psi)^2,
O3=C^3,
O4=C^2 X,
O5=reflection odd.
```

Its zero-state C3 source audit is exact within this basis:

```text
O1: silent by scalar degree six;
O2: silent by scalar degree four;
O3: retained target coordinate h_C3;
O4: retained in the Hessian and combined trajectory;
O5: forbidden by psi -> -psi;
P(X): complete local functional tower retained through eta_psi;
J_gap: finite threshold displacement bounded from the 4942 family.
```

Thus the `p6` zero-state C3 projection is source-complete in the declared
truncation. This statement deliberately stops at `p6`: the untruncated
`p>=8` curvature-motion tower is not calculated.

## 3. Finite C3 coordinate selected by the trajectory

The Gaussian-endpoint form is

```text
h_C3/g=A_C3+B_C3 ln(g)+O(g ln g),

B_C3=1/2[c_gravity+photon
          +lim(eta_psi/g)/(483840 pi^2)].
```

The locked inputs give

```text
c_gravity+photon=-3.669491731602941e-5,
lim eta_psi/g=-0.424413183872... or -0.424413183612...,
B_C3=-1.839189694975e-5 to -1.839189694972e-5.
```

For all four combinations of regulator scheme and polynomial order `N=6,8`,
the final 10 and 20 trajectory rows were independently fit to

```text
h_C3/g=A+B ln(g)+C g+D g ln(g).
```

The largest pointwise fit residual is `1.03439842412e-10`; the largest
difference between fitted and independently derived `B` is
`2.57929246666e-10`. Taking the union of those blind fits and direct
source-slope subtraction gives

```text
A_C3 massless:
  -2.197101166424444e-5 <= A_C3 <= -2.195270844100629e-5.
```

The 45-row 4942 finite-mass family is then re-read. Within each mapping and
gravity-seed family, the maximum displacement from its smallest-`J_gap` row
is

```text
Delta A_C3(J_gap)=8.08875617759326e-8,
J_gap,max=0.23990506758224886.
```

Enlarging the current massless bracket symmetrically by that older-family
displacement gives the deliberately conservative selected envelope

```text
-2.2051899226020373e-5
  <= A_C3^S <=
-2.1871820879230358e-5.
```

The superscript `S` matters: this is a finite renormalized coordinate in the
locked natural source scheme. Its finite sign and range are selected in that
scheme, but `A_C3^S` alone is not a scheme-independent observable.

## 4. Local coefficient and running guardrail

The inherited normalization is

```text
G_C3=A_C3^S l_P^2,
a_+=16 pi A_C3^S l_P^4.
```

The selected finite envelope gives

```text
|G_C3| <=5.76057419780756e-75 m^2,
|a_+|  <=7.564067676419907e-143 m^4.
```

For a characteristic length `L`, the raw local running coordinate is

```text
A_run(L,q)=A_C3^S+B_C3 ln[(q l_P/L)^2],
q in [1/2,2].
```

This raw-running quantity is reported only as a conservative log-sensitivity
envelope. A physical amplitude must combine the local coefficient with the
corresponding nonlocal loop form factor, whose scale dependence cancels the
local running. Treating `A_run` by itself as a measured Wilson coefficient
would be an overclaim.

## 5. Compact C3 residual

For the locked parity-even exterior solution,

```text
|Delta Phi/Phi_N|=20|a_+|M^2/r^6,
|Delta a/a_N|    =140|a_+|M^2/r^6,
epsilon_h        =(3/4)|a_+|/M^4.
```

The finite and raw-running envelopes were evaluated for all nine BSK24,
SLY4 and DD2 stars from 4962, a declared `1.4 M_sun, 12 km` benchmark, and a
`10 M_sun` Schwarzschild proxy. The worst results are

```text
maximum finite compact residual
  =7.415086500522157e-158,

maximum raw-running-envelope residual
  =1.106517857252991e-155.
```

They are respectively `155.1299` and `152.9560` orders below the declared
one-percent control gate. This is not an observational detection and does
not replace a complete local-plus-nonlocal waveform calculation. It does
show that the selected `p6` C3 trajectory cannot threaten the compact GR
corridor by any numerically plausible interpretation of its retained local
coefficient.

## 6. Exact nonlinear static scalar identity

Consider a static solution split into smooth material domains with lapse
`N`, spatial metric `gamma_ij`, and nonlinear scalar current

```text
J^i=J^i[P(X),O4,matter contacts].
```

The exact static equation is

```text
D_i(N J^i)-N V_eff'(psi)=0.
```

Multiply by `psi`, integrate each domain, and integrate by parts:

```text
integral N sqrt(gamma)
  [D_i psi J^i+psi V_eff'(psi)]
=sum_boundaries integral N sqrt(h) psi n_i J^i.
```

The internal terms cancel pairwise because checkpoint 4943 derived

```text
[psi]=0,
[n_i J^i]=0.
```

The outer term vanishes for `psi->0`; a regular stellar center has no inner
surface; and the lapse suppresses the corresponding term at a regular
static horizon. Hence the right-hand side is zero.

Inside the certified functional chart,

```text
0<=x<=0.1,
P_X>0,
P_X+2X P_XX>0,
D_i psi J^i >=b_min |D psi|^2,
b_min>0.
```

The complete trajectory scan gives a minimum Hessian singular value
`0.336372084499022`. The O4 and matter-contact shifts remain positive; all
nine EOS rows pass, with maximum density/instability ratio
`5.3697748471940454e-18`. The retained regular mass-gap term gives

```text
psi V_eff'(psi)=m_eff^2 psi^2>=0.
```

If the original positive fractional potential is retained instead, its
product `psi V'(psi)=g_psi |psi|^(4/3)` has the same nonnegative sign.
Reflection symmetry excludes odd bulk and surface sources.

Every term in the integrated identity is therefore nonnegative. Equality
forces `D_i psi=0`; positive mass fixes `psi=0`, while in the massless case
the asymptotic condition fixes the remaining constant to zero. Consequently

```text
there is no regular healthy disconnected static scalar branch
that remains entirely inside x<=0.1.
```

This is nonlinear in amplitude within the certified chart; it is not merely
the perturbative zero-mode statement from 4962.

## 7. Exact escape surfaces

The contrapositive identifies what a surviving disconnected branch must do:

```text
x>0.1,
or P_X<=0,
or P_X+2X P_XX<=0,
or psi V_eff'(psi)<0,
or activate a reflection-odd bulk/surface source,
or violate regular junction/asymptotic data.
```

The current `N=12` charts lose convexity before `x=0.25`, so an all-`X`
global theorem is not claimed. Time-dependent binaries and rotating horizons
also require a hyperbolic energy estimate or nonlinear evolution rather than
the static elliptic identity.

## 8. Physics decision

```text
declared p6 zero-state C3 source closure       = passed;
finite C3 coordinate in locked source scheme  = selected;
p6 compact C3 residual                        = negligible;
healthy disconnected static scalar branch
  wholly inside x<=0.1                        = excluded;
all-X scalar branch exclusion                 = false;
dynamical/rotating branch exclusion           = false;
p>=8 source completeness                      = open;
finite R2/C2 and physical CFF matching        = open;
exact all-operator compact GR                 = false;
full MTS                                      = false.
```

The controlled compact branch has moved forward: `C3` and a healthy static
nonlinear scalar branch are no longer generic unresolved dangers inside the
declared `p6`, `x<=0.1` domain. The next verdict-changing target is finite
`R2/C2/CFF` matching together with a bounded `p>=8` tail, not another search
for the already-selected `C3` finite coordinate.

## 9. Generated artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4963_strong_field_C3_selection_and_global_scalar_branch.py`
- `post-checkpoint-work/source-intake/functional_rg/4963/strong_field_C3_and_scalar_branch_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4963/C3_source_ownership_audit.csv`
- `post-checkpoint-work/source-intake/functional_rg/4963/C3_Wilson_selection_and_running.csv`
- `post-checkpoint-work/source-intake/functional_rg/4963/compact_C3_residual_domain.csv`
- `post-checkpoint-work/source-intake/functional_rg/4963/nonlinear_scalar_branch_theorem.csv`
- `post-checkpoint-work/source-intake/functional_rg/4963/strong_field_compact_GR_decision.csv`
- `post-checkpoint-work/source-intake/functional_rg/4963/PROVENANCE.md`

No GitHub action was taken.

