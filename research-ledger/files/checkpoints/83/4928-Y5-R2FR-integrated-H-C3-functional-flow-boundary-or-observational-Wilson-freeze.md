# 4928 - Integrated-H C3 functional flow and observational Wilson freeze

Marker: `MTS_INTEGRATED_H_C3_FUNCTIONAL_FLOW_4928`.

**Decision:** a real fixed-point route now exists and has been calculated, not
merely listed as a future possibility. The natural-regulator pure-gravity beta
functions attached to the 2026 primary source have one non-Gaussian fixed
point, one relevant direction and a unique infrared separatrix. Independent
integration gives

```text
g_*       =0.5890486225480862,
g_C3,*    =-3.2424842753194084e-7,
theta     =(+2.78260869565,-7.75000535537),
G_C3/G_N  =3.024098389340624e-6
```

after the source prescription subtracts the massless logarithm at
`k0=M_Pl`. In MTS conventions the conditional branch is

```text
a_+/l_P^4 =16 pi G_C3/G_N =1.520077645389635e-4,
ell_+      =1.794635816842645e-36 m.
```

That branch is overwhelmingly safe in every current local or compact arena.
It is **not yet an MTS prediction**. The four-dimensional `H` coordinate and
operator basis inherit the pure-metric flow kinematically, but the current MTS
parent has not supplied the natural gravitational regulator, a derived
zero-cosmological trajectory, the complete matter/EM/motion-field beta
functions, or the corresponding ultraviolet critical surface.

The selected nonclaim therefore remains one observational coefficient,
`A_+(Q_GW)`, rather than either a claimed fixed-point prediction or several
scheme-split placeholders.

## 1. Exact action and coefficient map

The external Euclidean truncation is

```text
Gamma_k
 =integral sqrt(g)[-R/(16 pi G_N(k))+G_C3(k) C^3].
```

The active MTS Ricci-flat parity-even coordinate is

```text
S
 =(16 pi G_N)^-1 integral sqrt(-g)[R+a_+ I1],

I1=C^3,
a_+=16 pi G_N zeta_+.
```

Consequently

```text
zeta_+=G_C3,
r_C3:=G_C3/G_N,
a_+/l_P^4=16 pi r_C3.
```

This is the same normalization already used in the 4922--4925 QNM and
Goroff-Sagnotti calculations. No factor of two or reduced-Planck conversion is
inserted.

## 2. Executed natural-regulator beta system

Write

```text
g=k^2 G_N(k),
h=g_C3=k^2 G_C3(k),
t=ln k.
```

The attached source notebook gives

```text
beta_g
 =2g(-32g+6pi)/(-9g+6pi),

beta_h
 =-N(g,h)/[120960(9g-6pi)pi^2],
```

where

```text
N(g,h)
 =69g
 +[-3709440g^2 pi+14515200g pi^2+1451520pi^3]h
 +[47585664g^3 pi^2-21337344g^2 pi^3]h^2
 +[-84188160g^4 pi^3+78382080g^3 pi^4]h^3.
```

Checkpoint 4928 transcribes these equations directly and performs the fixed
point and trajectory calculation with no fit to the article's reported final
number.

## 3. Fixed point and critical surface

The nonzero Newton fixed point follows exactly from `beta_g=0`:

```text
g_*=3pi/16=0.5890486225480862.
```

At this value the cubic equation `N(g_*,h)=0` has one real root,

```text
h_*=-3.2424842753194084e-7,
```

and one complex-conjugate pair. The triangular stability matrix has

```text
partial_g beta_g|_*=-64/23,
partial_h beta_h|_*=+7.75000535537.
```

With `theta=-eig(D beta)` this gives

```text
theta_relevant   =+64/23=+2.78260869565,
theta_irrelevant =-7.75000535537.
```

There is therefore one relevant direction. Once the dimensionful unit is
fixed by `G_N`, this two-coupling truncation has no remaining freely chosen
dimensionless `C^3` datum. The tangent of the relevant separatrix is

```text
dh/dg|_*=-1.58491812387e-7.
```

## 4. Infrared separatrix and exact logarithm

The generator integrates the stable ratio equation

```text
r=h/g,
x=ln g,
dr/dx=beta_h/beta_g-r
```

from the non-Gaussian point to `x=-50`. Changing the starting displacement
from `1e-3` to `1e-8` changes the extracted infrared constant below displayed
precision.

The small-coupling expansion is exact:

```text
beta_g=2g+O(g^2),

beta_h
 =2h+c_log g+O(gh,g^2,h^2),

c_log
 =69/(725760pi^3)
 =23/(241920pi^3)
 =3.066242112944727e-6.
```

Hence

```text
d(h/g)/dt=c_log+o(1),
ln g=2ln(k/k0)+o(1),

h/g
 =A_C3+(c_log/2)ln g+o(1)
 =A_C3+c_log ln(k/k0)+o(1).
```

The independently calculated limit is

```text
A_C3
 =lim_[g->0]{h/g-(c_log/2)ln g}
 =3.024098389340624e-6.
```

This reproduces the source's displayed `3.02e-6` coefficient.

## 5. Source-internal logarithmic-sign audit

The 2026 article text prints the natural-scheme logarithmic slope as
`-3.07e-6`. Its attached beta notebook instead gives the positive exact
coefficient above. This is not a numerical ambiguity:

```text
lim_[g,h->0](beta_h-2h)/g
 =+69/(725760pi^3).
```

The article's own reference-scale crossing also selects the positive sign.
Under `k0'=xi k0`, invariance of the logarithmic sum gives

```text
A_C3(xi)=A_C3(1)+c_log ln xi.
```

Therefore

```text
xi_zero
 =exp[-A_C3(1)/c_log]
 =0.372970638857598,
```

matching the article's stated natural-scheme threshold near `0.37`. A negative
slope in that equation would not produce the stated lower crossing. The
checkpoint quarantines this as a source sign-convention or typographical
discrepancy while retaining the executable notebook equations and their
reproduced limit.

## 6. Conditional pure-gravity prediction in MTS units

At `k0=M_Pl=G_N^-1/2`, the natural separatrix maps to

```text
r_C3                    =3.024098389340624e-6,
a_+/l_P^4               =1.520077645389635e-4,
ell_+/l_P               =0.1110366736513342,
ell_+                    =1.794635816842645e-36 m,
a_+                      =1.037302260032333e-143 m^4,
alpha_ev(GW250114 mass)  =9.52082825626367e-164.
```

The older shifted-regulator source branch gives `r_C3=9.6e-3`, or
`ell_+=0.83346 l_P`; it is also negligible but requires an ad hoc subtraction
of an unphysical shifted-Gaussian divergence. It is retained only as a scheme
comparator.

For the natural branch,

```text
a_+/a_NS,1percent =7.12659171350531e-158,
a_+/a_GW,bound    =1.7651266e-162.
```

Thus if this trajectory were the MTS ultraviolet trajectory, the finite
Weyl-cubic obstruction would be solved decisively and with positive sign.

## 7. Integrated-H inheritance theorem

The functional-flow result is not alien to the selected integrated-`H`
geometry. Checkpoint 4925 proved

```text
H^{mn}=sqrt(abs(g))g^{mn},
abs det(dH/dg)=1 in d=4.
```

Therefore the following conditional theorem holds.

If

1. the gauge-fixed gravitational functional integral is transformed between
   `H` and `g` through this invertible algebraic map;
2. the ghost, gauge-fixing and cutoff operators are all transformed through
   the same public metric;
3. the projection retains the same essential `R` and `I1=C^3` operators;

then the `H` and `g` descriptions have the same essential beta-flow fixed
points and critical exponents. The constant point Jacobian cannot create an
additional `C^3` boundary.

This closes **kinematic compatibility**. It does not select a regulator or
field content and therefore does not close dynamic inheritance.

## 8. Why the number is not yet an MTS prediction

The inheritance gate has three closed and six open clauses:

```text
H-to-g algebraic coordinate                 closed;
constant four-dimensional point measure    closed;
essential Ricci-flat I1 basis               closed;

natural gravity/ghost regulator             not parent-selected;
Lambda_k=0 ultraviolet trajectory           not derived;
pure-gravity ultraviolet field content      false for full MTS;
complete MTS non-Gaussian fixed point        not calculated;
matter-completed critical-surface dimension not calculated;
k0=M_Pl transition-scale owner              prescribed, not derived.
```

In particular, the active action contains visible matter, electromagnetism and
the motion sector. Their ultraviolet fluctuations can change both beta
functions, the fixed point and the stability matrix. Decoupling in the local
infrared does not erase their ultraviolet contribution near the Planck
transition. Importing the pure-gravity number as the MTS value would therefore
be the same type of unjustified closure this programme is designed to avoid.

## 9. Selected observational Wilson freeze

The physical low-energy quantity is one RG-invariant amplitude coefficient at
a stated kinematic reference,

```text
A_+(Q_GW)
 =a_R(mu)+a_nonlocal(Q_GW,mu)+matched thresholds.
```

Scale or scheme changes redistribute the local and logarithmic pieces but do
not create extra observable parameters. The existing GW250114 robustness
envelope gives

```text
abs A_+(Q_GW) <=5.873319830123418e18 m^4,
ell_GW          <=49.2289885265 km.
```

If the complete coefficient is independently shown nonnegative,

```text
0<=A_+(Q_GW)<=3.866931828175418e18 m^4.
```

The polarization branches remain separate:

```text
polar: -0.0168705 < alpha_ev < +0.0319509,
axial: -0.0430573 < alpha_ev < +0.0210358
```

at the internal 90-percent recast. Both contain GR. They are not multiplied or
combined without a parent excitation-weight prediction.

The observational envelope remains a factor `40351.55` above the selected
one-percent neutron-star coefficient target. Thus observation alone does not
promote compact GR, while the conditional fixed-point branch would pass it by
over 150 coefficient orders.

## 10. Result and next derivation

Checkpoint 4928 has achieved four nontrivial advances:

1. the full attached functional flow is independently integrated;
2. the unique pure-gravity infrared `C^3` coefficient is reproduced;
3. the integrated-`H` coordinate is proved kinematically compatible with that
   essential flow;
4. the exact boundary between a conditional prediction and the one physical
   observational Wilson input is now explicit.

Current decision:

```text
pure-gravity natural C3 flow              -> calculated;
unique separatrix after fixing G_N        -> derived in the truncation;
published IR coefficient                  -> independently reproduced;
article logarithmic sign                  -> discrepancy found and quarantined;
integrated-H kinematic inheritance        -> derived;
full MTS dynamic inheritance              -> not derived;
observational low-energy parameter count  -> exactly one;
weak GR/Newton/Maxwell                     -> retained;
compact and full MTS-to-GR                 -> not promoted.
```

Direct next target:

`4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md`

Calculate the leading matter/EM/motion-sector deformation of the natural
essential flow and test fixed-point survival and critical-surface dimension.
If no controlled matter-completed projection can be derived, retain the one
observational Wilson coefficient without reopening already closed
normalization or measure questions.

No GitHub action or public claim is authorized.

## Primary sources

- Gies, Knorr, Lippoldt and Saueressig, `arXiv:1601.01800`.
- Del Porro, Ferrarin and Platania, `arXiv:2509.07058`, including its attached
  natural-regulator beta-function notebook.

The locked files and SHA-256 values are recorded in
`post-checkpoint-work/source-intake/functional_rg/4928/PROVENANCE.md`.
