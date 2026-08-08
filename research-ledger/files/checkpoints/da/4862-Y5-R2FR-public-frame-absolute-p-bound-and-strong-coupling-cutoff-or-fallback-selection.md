# 4862 — Public-frame absolute-`p` bound and canonical cutoff window

Marker: `PUBLIC_P_BOUND_CUTOFF_SELECTION_4862`

**Private status:** derived correspondence-theory checkpoint; not a public MTS/GR claim.

## 1. Question decided here

Checkpoint 4861 selected

\[
\widehat g^{\mu\nu}=g^{\mu\nu}+p u^\mu u^\nu
\]

as the lead public matter, photon, clock, free-fall and source metric. Relative gravitational-wave/photon timing then fixes the common cone but does not bound the absolute value of `p`.

This checkpoint asks two quantitative questions rather than reopening the frame choice:

1. Is there a source-backed nonempty `(p,d)` region satisfying weak PPN and cosmological-`G` constraints?
2. Does the shrinking flow kinetic term force that region below the two-derivative strong-coupling scale?

The answer is **yes, a large nonempty region survives the present gates**. The public `gHat` branch remains the lead private branch. The same-`g`, `beta_u=0` branch remains a fallback, but is not triggered here.

## 2. Public coefficient surface

Write

\[
d=rp,
\qquad
0<r\le\frac13,
\qquad
0<p<1.
\]

The 4861 public coefficients become

\[
D=p(1+r-rp),
\]

\[
\widehat c_1=\frac{D}{2},
\qquad
\widehat c_3=-\frac{D}{2},
\]

\[
\widehat c_2=\widehat c_{123}
=\frac{2p}{3(1+r)(1-p)},
\]

\[
\widehat c_{14}=\frac{2rp}{1+r},
\qquad
\widehat c_4=\widehat c_{14}-\frac{D}{2}.
\]

The physical weak preferred-frame coefficients are

\[
\boxed{
\widehat\alpha_1=-\frac{8rp}{1+r},
\qquad
\widehat\alpha_2=-\frac{rp(1-3r)}{1+r}.
}
\]

The cosmological/Newton calibration ratio is

\[
\boxed{
\frac{\widehat G_{\rm cos}}{\widehat G_N}=1-p.
}
\]

## 3. Absolute-`p` envelope

### 3.1 Weak `alpha1`

Using the source-backed weak-field bound

\[
|\alpha_1|\le10^{-4},
\]

gives

\[
p\le10^{-4}\frac{1+r}{8r}.
\]

Because `8r/(1+r)` is maximized at `r=1/3`, the `r`-independent sufficient condition is

\[
\boxed{p\le5\times10^{-5}.}
\]

### 3.2 Weak `alpha2`

The strong-field `2e-9` row in the local register is not used as the baseline. Compact-body preferred-frame parameters depend on sensitivities and their derivatives; the 2021 Einstein-aether pulsar analysis explicitly warns that existing strong-field `hat alpha1/hat alpha2` bounds cannot simply be inserted as priors.

The baseline therefore uses the weak-field value

\[
|\alpha_2|\le10^{-7}.
\]

For `0<r<1/3`,

\[
p\le10^{-7}\frac{1+r}{r(1-3r)}.
\]

The shape

\[
f(r)=\frac{r(1-3r)}{1+r}
\]

has its maximum at

\[
r_*=-1+\frac{2\sqrt3}{3},
\qquad
f(r_*)=7-4\sqrt3.
\]

Hence a sufficient condition valid for every `0<r<=1/3` is

\[
\boxed{
p\le p_{\rm PPN}
:=\frac{10^{-7}}{7-4\sqrt3}
=1.3928203230\times10^{-6}.
}
\]

The `2e-9` strong-field proxy would reduce this to `2.7856406461e-8`, but that number remains diagnostic until the MTS/Einstein-aether compact-body sensitivity map is evaluated.

### 3.3 Cosmological `G`

On this coefficient surface,

\[
\frac{\widehat c_{14}+3\widehat c_2}{2+3\widehat c_2}=p
\]

exactly. The Einstein-aether BBN gate

\[
\left|\frac{c_{14}+3c_2}{2+3c_2}\right|\le\frac18
\]

therefore gives the direct absolute anchor

\[
\boxed{p\le\frac18.}
\]

An updated generic BBN analysis reports `G_BBN/G_0=0.99^{+0.06}_{-0.05}` at two sigma. If the only relevant MTS effect during BBN is the constant replacement `G_BBN/G_0=1-p`, its lower side gives the conditional update

\[
\boxed{p\le0.06.}
\]

This update is not used as a full MTS cosmology claim because additional MTS background or abundance effects would require a dedicated likelihood.

### 3.4 Combined result

The direct absolute bound over the full family is supplied by BBN. More importantly for a branch that should not depend on choosing a special `r`, there is a nonempty weak-PPN-safe sufficient corridor:

\[
\boxed{
0<p\le1.3928203230\times10^{-6},
\qquad
0<r\le\frac13.
}
\]

This is not the full allowed region; near zeros of `alpha2`, larger `p` can survive. It is the region that passes the sourced weak gates for every retained `r`.

The old working value `p=1e-15` is therefore reclassified correctly:

```text
not an absolute bound from GW170817;
not required by the public-frame PPN equations;
a conservative high-margin benchmark inside a sourced viable corridor.
```

## 4. Canonical nonlinear scale

Use the public two-derivative action normalization

\[
S_{\ae}=\frac{\bar M_{\rm Pl}^2}{2}
\int d^4x\sqrt{-\widehat g}\,[\widehat R-K(\widehat c_i,\widehat\nabla u)+\lambda(u^2+1)].
\]

The unit constraint gives

\[
u^0=\sqrt{1+v_i v_i}
=1+\frac{v^2}{2}-\frac{v^4}{8}+\cdots.
\]

For one local transverse polarization

\[
u^\mu=(\sqrt{1+v^2},0,v,0),
\qquad
v=v(t,x),
\]

the exact local kinetic invariant expanded through quartic order is

\[
K[v]
=-\widehat c_{14}\dot v^2
+\widehat c_1(v')^2
+\widehat c_{123}v^2\dot v^2
-\widehat c_1v^2(v')^2
+O(v^4\partial v\partial v).
\]

Thus the transverse canonical variable is

\[
\boxed{v_c=\bar M_{\rm Pl}\sqrt{\widehat c_{14}}\,v.}
\]

Also

\[
\frac{\widehat c_{123}}{\widehat c_{14}}
=\frac{1}{3r(1-p)}\ge1,
\]

so `c14` is the smallest flow kinetic owner throughout the retained corridor.

For `p<=0.06` and `0<r<=1/3`, every two-derivative coefficient obeys the conservative envelope

\[
|\widehat c_i|\le
\overline C(p):=\frac{2p}{3(1-p)}.
\]

The proof is elementary:

```text
c1=|c3|=p(1+r-rp)/2 <= 2p/3 <= Cbar;
c2=c123=Cbar/(1+r) <= Cbar;
c4<0 and |c4|<=p/2<Cbar.
```

A cubic vertex and quartic vertex then canonicalize as

\[
\bar M_{\rm Pl}^2 C_3v(\partial v)^2
\longrightarrow
\frac{C_3}{\bar M_{\rm Pl}\widehat c_{14}^{3/2}}
v_c(\partial v_c)^2,
\]

\[
\bar M_{\rm Pl}^2 C_4v^2(\partial v)^2
\longrightarrow
\frac{C_4}{\bar M_{\rm Pl}^2\widehat c_{14}^{2}}
v_c^2(\partial v_c)^2.
\]

The corresponding tree-level suppression scales are

\[
\Lambda_3=\bar M_{\rm Pl}\frac{\widehat c_{14}^{3/2}}{C_3},
\qquad
\Lambda_4=\bar M_{\rm Pl}\frac{\widehat c_{14}}{\sqrt{C_4}},
\qquad
\Lambda_\sigma=\bar M_{\rm Pl}\sqrt{\widehat c_{14}}.
\]

Using `C3,C4<=Cbar` gives the conservative two-derivative canonical diagnostic

\[
\boxed{
\Lambda_{\rm safe}(p,r)
=3\sqrt2\,\bar M_{\rm Pl}(1-p)\sqrt p
\left(\frac{r}{1+r}\right)^{3/2}.
}
\]

It is the controlling one because

\[
\frac{\Lambda_{\rm safe}}{\Lambda_\sigma}
=\frac{3r(1-p)}{1+r}\le\frac34,
\]

and

\[
\left(\frac{\Lambda_{\rm safe}}{\Lambda_{4,\rm safe}}\right)^2
=\frac{3r(1-p)}{1+r}\le\frac34.
\]

No `4pi` enhancement has been inserted, making this an intentionally conservative canonical scale.

## 5. Exact EFT-window inversion

For a required resolved energy `E_req`, define

\[
x=left[
\frac{E_{\rm req}}
{3\sqrt2\,\bar M_{\rm Pl}(1-p)\sqrt p}
\right]^{2/3}.
\]

Then

\[
\boxed{
\Lambda_{\rm safe}\ge E_{\rm req}
\quad\Longleftrightarrow\quad
r\ge\frac{x}{1-x}
}
\]

when `0<x<1`.

Using the 2022 CODATA Planck mass gives

\[
\bar M_{\rm Pl}=2.4353232036\times10^{18}\ {\rm GeV}.
\]

The `38.6 micrometre` R10 anchor corresponds to

\[
E_{\rm R10}=\frac{\hbar c}{38.6\ \mu{\rm m}}
=5.112\times10^{-12}\ {\rm GeV}.
\]

At the retained point `p=1e-15`, `r=1/3`,

\[
\boxed{
\Lambda_{\rm safe}=4.08416\times10^{10}\ {\rm GeV}.
}
\]

The minimum ratios are

\[
r_{\min}(E_{\rm R10})=6.26\times10^{-16},
\]

and, for an optional aggressive `1 TeV` stress diagnostic,

\[
r_{\min}(1\ {\rm TeV})=2.11\times10^{-6}.
\]

Both leave a large interval below `r=1/3`. The public working branch is therefore not close to its leading canonical cutoff.

## 6. What this does and does not prove

Closed here:

```text
absolute p is bounded without reusing relative GW timing;
weak and strong-field alpha2 inputs are no longer conflated;
an r-independent source-backed PPN-safe corridor is explicit;
the smallest kinetic owner is identified exactly;
the unit-flow canonical field and leading nonlinear suppression laws are derived;
the EFT condition is inverted to an exact r floor;
the retained p=1e-15,r=1/3 point has a very large local/R10 cutoff margin;
the public gHat branch survives and remains the lead private branch.
```

Not closed here:

```text
the complete reduced scalar-vector-graviton cubic action;
partial-wave scattering eigenvalues and exact order-one unitarity factors;
possible constraint-elimination enhancement in a mixed scalar channel;
compact-body sensitivities and dipole radiation;
the p,r->0 gauge-restored exact-GR endpoint;
primitive derivation of gHat and the coefficient surface from the original MTS scalar grammar.
```

The `Lambda_safe` result is a derived two-derivative canonical floor under ordinary local EFT power counting, not a claimed UV completion. A lower eigenchannel found by the full reduced cubic calculation would supersede it.

## 7. Decision

```text
LEAD: public gHat branch retained;
FALLBACK: same-g beta_u=0 remains available but is not selected;
WORKING POINT: p=1e-15,r=1/3 retained as a benchmark, not an observational limit;
NEXT HARD CALCULATION: full reduced cubic mode action plus partial-wave unitarity.
```

Primary cross-checks: [Oost, Mukohyama and Wang](https://arxiv.org/abs/1802.04303), [Gupta et al.](https://arxiv.org/abs/2104.04596), [Withers](https://arxiv.org/abs/0905.2446), [Alvey et al.](https://arxiv.org/abs/1910.10730), and [2022 CODATA](https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf).

Next: `4863-Y5-R2FR-full-reduced-cubic-mode-action-and-unitarity-partial-wave-or-public-branch-hard-cutoff.md`.
