# 4936 - Motion 1PI closure, O4 projection and predictivity gate

Marker: `MTS_MOTION_FUNCTIONAL_COMPLETION_AND_PREDICTIVITY_GATE_4936`.

Date: `2026-07-12`.

Status: private analytic and source-executed checkpoint. The literal
one-coupling `|psi|^(4/3)` realization is rejected as an RG-closed quantum
truncation. The motion sector itself is not rejected: the full functional
potential route is selected. No full-MTS or local-GR/Newton/Maxwell claim is
made.

## 1. Exact fractional-potential flow

In four Euclidean dimensions, define

```text
u(varphi)=(3/4)gtilde |varphi|^(4/3),

q=|varphi|^(2/3),

C_eta=(1-eta_psi/6)/(32pi^2).
```

The optimized-regulator LPA-prime flow is

```text
partial_t u
 =-4u+(1+eta_psi/2)varphi u'
  +C_eta/(1+u''),

u''=gtilde/(3q).
```

Substitution gives the exact rational flow

```text
partial_t u
 =[gtilde(eta_psi-4)/2]q^2
  +3C_eta q/(gtilde+3q).
```

At `eta_psi=0`, its small-field expansion is

```text
partial_t u
 =3q/(32pi^2 gtilde)
  +[-2gtilde-9/(32pi^2 gtilde^2)]q^2
  +27q^3/(32pi^2 gtilde^3)
  -81q^4/(32pi^2 gtilde^4)+... .
```

The first quantum term is `|varphi|^(2/3)`, not
`|varphi|^(4/3)`. It is outside the retained family and dominates it as
`varphi -> 0`. Therefore a beta function obtained by projecting only the
`q^2` coefficient is inconsistent.

This is not merely a canonical-counting warning. Classical marginality of
the fractional term requires

```text
eta_psi=4,
```

whereas silence of the optimized scalar trace requires

```text
eta_psi=6.
```

At `eta_psi=4` the forbidden leading term remains
`q/(32pi^2 gtilde)`. At `eta_psi=6` the scalar trace vanishes but the
nonzero `q^2` canonical flow remains. Hence this LPA-prime system has no
nonzero scalar-only fixed point inside the one-coupling fractional family.

## 2. What this does and does not reject

The rejected statement is

```text
Gamma_k contains only (3/4)gtilde_k |varphi|^(4/3)
in its scalar-potential sector at every scale.
```

The parent motion idea is not rejected. Three mathematical escape routes
exist:

1. solve a full fixed function `u_*(varphi)` and its eigenoperators;
2. derive an exact gravity-motion trace that cancels every generated channel;
3. derive a different parent field-space metric and measure in which the
   elementary coordinate is not the current canonical `psi`.

The exact cancellation contract is now explicit. At `eta_psi=4`, the rest
of the trace must begin with

```text
[q]   T_rest=-1/(32pi^2 gtilde),

[q^2] T_rest=+3/(32pi^2 gtilde^2) at a fixed point,

[q^3] T_rest=-9/(32pi^2 gtilde^3),
```

and continue through the full rational series. No current parent calculation
satisfies this infinite contract, so it is an open derivation route rather
than a closure axiom.

## 3. Mass-scale consequence

At canonical field dimension one,

```text
[g_psi]=8/3,

m_gap=c_m g_psi^(3/8)
```

is the dimensional form. The flow calculation proves that `c_m` is a
nonperturbative trajectory observable, not a number derivable from the
one-coupling ansatz alone. At the anomalous dimension `eta_psi=4` that would
make the fractional interaction marginal, `g_psi` is dimensionless and
cannot generate a mass scale by itself.

The field map

```text
psi=chi^3
```

does turn the potential into `(3/4)g_psi chi^4`, but it also gives

```text
(1/2)(nabla psi)^2=(9/2)chi^4(nabla chi)^2.
```

A canonical `chi` field would require the different parent metric

```text
Z(psi)=1/[9|psi|^(4/3)].
```

Moreover `dpsi/dchi=3chi^2` vanishes at the vacuum. The quartic reading is
therefore a potentially useful microscopic reconstruction, not an allowed
silent field redefinition of the current parent.

## 4. Primary-source scalar-gravity execution

The official supplementary notebook for Benjamin Knorr,
`Safe essential scalar-tensor theories` (`arXiv:2204.08564`, supplement DOI
`10.17632/9v7ftgswc5.1`) was acquired and hash locked. All 25 input BoxData
cells were mechanically extracted. One very large stored output cell is
retained as raw BoxData because the local Mathics parser rejected it; this
does not affect the exact beta/gamma input expressions.

The extracted linear-regulator formulas were independently parsed, rooted
and differentiated. They reproduce

```text
A:
  g=0.2519733249374084,
  g_Dphi4=-17.9179138877062,
  theta={0.403504921226913,1.99177283732834},
  gamma_phi=0.830223954951144;

B:
  g=0.254186084253391,
  g_Dphi4=-6.03272982289601,
  theta={-0.408876408059480,1.96731286281011},
  gamma_phi=0.781908233497444.
```

The exact source beta function further gives

```text
beta_Dphi4(g,0)
 =(406/5)g^2
  -1284571 g^3/(5400pi)+O(g^4).
```

Thus gravity additively generates an essential scalar interaction even when
its coupling is zero. This proves that the gravity-motion source channel is
real. The values are not inserted into MTS: the source theory is
shift-symmetric and four-derivative, and its essential-scheme `gamma_phi`
must not be identified numerically with MTS `eta_psi` without a convention
map.

## 5. Exact O4 projector and source channels

For

```text
S_O4=u_O4 integral sqrt(g) C^2(nabla psi)^2,
```

the local constant-Weyl momentum kernel is

```text
Gamma_psi_psi^(2) contains 2u_O4 C^2 p^2.
```

Therefore the normalized projector is

```text
P_O4
 =(1/2) partial_(C^2) partial_(p^2) Gamma_psi_psi^(2)
 |_(C^2=p^2=0),

P_O4[2u_O4 C^2p^2]=u_O4.
```

This gives three exact channel results.

1. For an isolated free shift-symmetric scalar with
   `P_psi=-Box_g` and a background-scalar-independent regulator, the complete
   scalar trace is independent of `psi`; two scalar variations annihilate it.
   Its additive O4 source is exactly zero.
2. For the fractional parent, `E=V''` obeys

   ```text
   E'=-2g_psi/(9psi^(5/3)),
   E''=10g_psi/(27psi^(8/3)).
   ```

   The scalar trace is no longer silent, but its bare-vacuum O4 projection is
   singular. A renormalized finite-`k` potential and generally a
   field-dependent `u_O4(psi)` are required.
3. The gravity-motion block is a proved additive channel by the executed
   `406g^2/5` lower-derivative comparator. Its six-derivative `C^2p^2`
   coefficient still requires the corresponding curved-background trace.

## 6. Predictivity decision

The route gate gives

```text
one-coupling fractional family       = rejected;
exact mixed-trace cancellation       = open but unsatisfied;
psi=chi^3 current-parent equivalence = rejected;
full functional motion potential     = selected;
phenomenological mass/O4 closure     = demoted.
```

The selected next system is

```text
partial_t u_k(varphi)
 =-4u+(1+eta_psi/2)varphi u'
  +T_scalar[u]+T_gravity-motion[u;g,g_plus,g_minus,g_CFF,h_C3,u_O4,...].
```

It must possess a regular fixed function, a finite stability spectrum and a
trajectory to the 4935 Gaussian/GR branch. The strongest unification target
is one total relevant direction after Newton's scale is fixed. More relevant
directions are not automatically inconsistent, but every extra datum would
have to be derived or measured rather than hidden.

The independently executed source fixed point B shows that a gravity-scalar
system with one relevant and one irrelevant direction is mathematically
possible. It is precedent, not an MTS solution.

## 7. Interface to the galaxy phase flow

The sibling equations supplied for comparison,

```text
dn/d ln R=q n(1-n),

db/d ln R=-s b(1-b),
```

have an exact parent-eigenmode interpretation. If `r_n,r_b>0` are amplitude
or spectral-weight ratios and

```text
n=r_n/(1+r_n),       d ln r_n/d ln R=q,

b=r_b/(1+r_b),       d ln r_b/d ln R=-s,
```

then the two logistic equations follow identically, with

```text
n(R)=1/[1+(R_n/R)^q],

b(R)=1/[1+(R/R_b)^s].
```

If `k` is derived to scale as `1/R`, a Hessian eigenmode
`delta a proportional to k^lambda` gives `q=-lambda=theta` for the growing
occupation, while a decaying occupation gives `s=lambda=-theta`.

Conditionally applying this coordinate map to the external source point B
would give `q=1.9673128628` and `s=0.4088764081`. Those are not MTS or galaxy
predictions. The parent must still identify the positive amplitude ratios,
derive `k(R)`, calculate the MTS eigenvalues and vary the resulting action to
obtain the activation stress tensor. The value of this result is structural:
the galaxy logistic law can arise from a fixed-point Hessian without being
inserted as a fundamental logistic axiom.

## 8. Claim boundary

```text
official scalar-gravity source flow executed       = true;
gravity additive scalar channel                    = proved;
fractional one-coupling LPA closure                = false;
nonzero scalar-only fractional fixed point         = false;
motion sector as a whole                           = not rejected;
full functional motion route                       = selected;
O4 projector                                       = derived;
free-scalar additive O4 source                     = exact zero;
fractional bare-vacuum O4 projection               = singular;
numeric mixed O4 coefficient                       = open;
galaxy logistic kinematic map                      = derived;
galaxy parent amplitudes and exponents             = open;
full MTS fixed function and trajectory             = open;
local GR/Newton/Maxwell promotion                  = false.
```

## 9. Next target

`4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md`

Derive the constant-background metric-motion block Hessian of the unchanged
parent, calculate the functional potential trace including its mixed gravity
source, formulate the regular fixed-functional boundary conditions and solve
or reject a finite-spectrum one-scale branch. The `O4` curved-momentum
projector should be carried with it rather than frozen.

