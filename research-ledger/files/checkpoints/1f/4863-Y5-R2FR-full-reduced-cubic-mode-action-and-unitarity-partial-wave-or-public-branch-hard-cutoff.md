# 4863 — Reduced flow interaction action and public-branch hard cutoff

Marker: `REDUCED_INTERACTION_HARD_CUTOFF_4863`

**Private status:** derived correspondence-EFT checkpoint; not a UV-completion, exact partial-wave, strong-field or primitive-MTS claim.

## 1. Why 4862 needed refinement

Checkpoint 4862 derived a canonical scale by bounding each dimensionless nonlinear coefficient separately. That is a useful first diagnostic, but it is not yet a guaranteed multi-operator floor: independent cubic tensor structures may contribute in the same process and cannot receive cancellation credit.

This checkpoint therefore does the calculation that 4862 only bounded:

```text
solve the unit constraint explicitly;
expand all four Einstein-aether invariants through quartic field order;
derive the complete local K2, K3 and K4 flow action;
project it into scalar and transverse-vector modes;
form sum norms over every independent cubic and quartic tensor structure;
bound metric-flow mixing and mixed graviton vertices;
select a hard Wilsonian cutoff without 4pi or angular-cancellation credit.
```

The correction lowers the benchmark cutoff, but does not come close to rejecting the public branch.

## 2. Action and unit constraint

Use signature `(-,+,+,+)` and

\[
S_{\ae}=\frac{\bar M_{\rm Pl}^2}{2}
\int d^4x\sqrt{-\widehat g}\,[\widehat R-K+\lambda(u^2+1)],
\]

with

\[
K=c_1 I_1+c_2 I_2+c_3 I_3-c_4 I_4,
\]

\[
I_1=\nabla_\mu u_\nu\nabla^\mu u^\nu,
\qquad
I_2=(\nabla_\mu u^\mu)^2,
\]

\[
I_3=\nabla_\mu u_\nu\nabla^\nu u^\mu,
\qquad
I_4=(u^\mu\nabla_\mu u_\nu)(u^\rho\nabla_\rho u^\nu).
\]

In a local public inertial chart, solve the unit constraint exactly by

\[
u^\mu=(\sqrt{1+v^2},v_i).
\]

Define

\[
T_i:=\dot v_i,
\qquad
B_{ji}:=\partial_jv_i,
\qquad
\theta:=\partial_iv_i,
\]

\[
v\cdot T:=v_iT_i,
\qquad
(v\cdot B_j):=v_iB_{ji},
\qquad
A_i:=(v\cdot\nabla)v_i=v_jB_{ji}.
\]

## 3. Exact invariant expansion

Introducing a field-counting parameter and expanding through fourth field order gives

\[
I_1^{(2)}=-T^2+B_{ji}B_{ji},
\qquad
I_1^{(3)}=0,
\]

\[
I_1^{(4)}=(v\cdot T)^2-\sum_j(v\cdot B_j)^2,
\]

\[
I_2^{(2)}=\theta^2,
\qquad
I_2^{(3)}=2\theta(v\cdot T),
\qquad
I_2^{(4)}=(v\cdot T)^2,
\]

\[
I_3^{(2)}=B_{ij}B_{ji},
\qquad
I_3^{(3)}=2T_i v_kB_{ik},
\qquad
I_3^{(4)}=(v\cdot T)^2,
\]

\[
I_4^{(2)}=T^2,
\qquad
I_4^{(3)}=2T_iA_i,
\]

\[
I_4^{(4)}=v^2T^2-(v\cdot T)^2+A^2.
\]

All twelve invariant/order identities are generated directly from `u^0=sqrt(1+v^2)` and pass symbolic comparison. No interaction term is inserted by analogy.

## 4. Complete local interaction action

The quadratic flow invariant is

\[
\boxed{
K_2=-c_{14}T^2
+c_1B_{ji}B_{ji}
+c_2\theta^2
+c_3B_{ij}B_{ji}.
}
\]

The complete cubic invariant is

\[
\boxed{
K_3=
2c_2\theta(v\cdot T)
+2c_3T_i v_kB_{ik}
-2c_4T_i v_jB_{ji}.
}
\]

After one spatial integration by parts,

\[
\boxed{
K_3\doteq
2c_2\theta(v\cdot T)
-c_3\dot\theta\,v^2
-2c_4\dot v_i v_j\partial_jv_i,
}
\]

where `doteq` means equality in the action for the declared vanishing/periodic local boundary term.

The complete quartic invariant is

\[
\boxed{
K_4=(c_{123}+c_4)(v\cdot T)^2
-c_4v^2T^2
-c_1\sum_j(v\cdot B_j)^2
-c_4A^2.
}
\]

These are all local two-derivative pure-flow interactions through four fields. Higher powers continue because the unit hyperboloid is nonlinear, but cubic and quartic vertices set the first perturbative scales.

## 5. Scalar/vector reduction

Use the Helmholtz split

\[
v_i=V_i+\partial_i\sigma,
\qquad
\partial_iV_i=0.
\]

Up to spatial boundary terms,

\[
\boxed{
K_2=-q\left[\dot V^2+(\partial_i\dot\sigma)^2\right]
+c_1(\partial_iV_j)^2
+c_{123}(\Delta\sigma)^2,
}
\]

with

\[
q:=c_{14}=\frac{2rp}{1+r}.
\]

The complete compact cubic mode action is

\[
\boxed{
\begin{aligned}
K_3\doteq{}&
2c_2\Delta\sigma\,
(V+\nabla\sigma)\cdot(\dot V+\nabla\dot\sigma)\\
&-c_3\Delta\dot\sigma\,|V+\nabla\sigma|^2\\
&-2c_4(\dot V_i+\partial_i\dot\sigma)
(V_j+\partial_j\sigma)
\partial_j(V_i+\partial_i\sigma).
\end{aligned}
}
\]

This expression retains every `SSS`, `SSV`, `SVV` and `VVV` vertex. No pairwise cancellation is used in the hard norm.

The pure-scalar cubic collapses to one coefficient:

\[
\boxed{
K_{3,S}\doteq(q-c_2)\Delta\dot\sigma\,|\nabla\sigma|^2.
}
\]

The identity behind this is

\[
c_3-c_4=-q.
\]

The pure-vector cubic is

\[
\boxed{
K_{3,V}=-2c_4\dot V_iV_j\partial_jV_i.
}
\]

At the particularly useful `r=1/3` slice,

\[
q=\frac p2,
\qquad
c_2=\frac{p}{2(1-p)},
\qquad
c_4=-\frac{p(1-p)}6.
\]

Therefore

\[
q-c_2=-\frac{p^2}{2(1-p)}.
\]

The scalar self-cubic has an exact extra power of `p`; it is not the dangerous channel. The vector self-cubic is also weaker than the combined mixed-mode norm. The lowest hard scale comes from retaining the mixed scalar-vector structures together.

## 6. Exact operator norms

Within `0<p<=0.06`, `0<r<=1/3`, the signs are fixed:

\[
c_4\le0,
\qquad
c_2+c_4\ge0.
\]

The first follows from `c1>=c14`. For the second,

\[
c_2\ge\frac p2,
\qquad
c_1-c_{14}\le\frac p2.
\]

Consequently the no-cancellation sum norm of the independent cubic structures is

\[
\boxed{
C_3:=|c_2|+|c_3|+|c_4|
=c_2+D-c_{14}.
}
\]

The quartic tensor norm is

\[
\boxed{
C_4:=|c_{123}+c_4|+2|c_4|+c_1
=c_2+D-c_{14}=C_3.
}
\]

A simple whole-corridor ceiling follows from

\[
c_2\le\frac{2p}{3(1-p)},
\qquad
D-c_{14}\le p:
\]

\[
\boxed{
C_3=C_4\le
\overline C_{\rm op}(p)
:=\frac{p(5-3p)}{3(1-p)}.
}
\]

This is the key correction to 4862. The 4862 scale used a ceiling for one coefficient; the hard floor must use the sum norm over all independent structures.

## 7. Canonical hard cutoff

Use the common local canonical flow variable

\[
v_c=\bar M_{\rm Pl}\sqrt q\,v.
\]

The exact pure-flow norm scales are

\[
\boxed{
\Lambda_3^{\rm exact}
=\bar M_{\rm Pl}\frac{q^{3/2}}{C_3},
\qquad
\Lambda_4^{\rm exact}
=\bar M_{\rm Pl}\frac{q}{\sqrt{C_4}}.
}
\]

Because `q<C3=C4`,

\[
\frac{\Lambda_3^{\rm exact}}{\Lambda_4^{\rm exact}}
=\sqrt{\frac q{C_3}}<1,
\]

and

\[
\frac{\Lambda_3^{\rm exact}}{\bar M_{\rm Pl}\sqrt q}
=\frac q{C_3}<1.
\]

The cubic norm scale controls.

Using the global operator ceiling gives the guaranteed whole-corridor floor

\[
\boxed{
\Lambda_{\rm hard}^{\rm floor}
=\frac{6\sqrt2\,\bar M_{\rm Pl}(1-p)\sqrt p}{5-3p}
\left(\frac r{1+r}\right)^{3/2}.
}
\]

For a required resolved energy, define

\[
y=\left[
\frac{E_{\rm req}(5-3p)}
{6\sqrt2\bar M_{\rm Pl}(1-p)\sqrt p}
\right]^{2/3}.
\]

Then the conservative hard-floor condition is

\[
\boxed{r\ge\frac y{1-y}.}
\]

## 8. Metric mixing and graviton vertices

Canonical metric perturbations have `h_c=Mbar_Pl h`. A representative one-graviton/two-flow vertex scales as

\[
\bar M_{\rm Pl}^2 C,h(\partial v)^2
\longrightarrow
\frac{C}{\bar M_{\rm Pl}q}
h_c(\partial v_c)^2.
\]

Hence

\[
\boxed{
\Lambda_{hvv}\ge
\bar M_{\rm Pl}\frac q{\overline C_{\rm op}}.
}
\]

Relative to the pure-flow hard floor this carries one fewer inverse `sqrt(q)` and is parametrically higher. Pure Einstein-Hilbert vertices remain Planck suppressed.

The quadratic canonical flow-metric mixing obeys

\[
\epsilon_{\rm mix}
\le\frac{\overline C_{\rm op}}{\sqrt q}.
\]

Define

\[
A(p)=\frac{p(5-3p)^2}{18(1-p)^2}.
\]

Then

\[
\boxed{
\epsilon_{\rm mix}\le1
\quad\Leftarrow\quad
r\ge\frac{A}{1-A}.
}
\]

This gives a separate, explicit guard against using the fixed-public-metric flow reduction where gravitational mixing is nonperturbative.

## 9. Numerical branch gate

At

\[
p=10^{-15},
\qquad
r=\frac13,
\]

the exact operator norms are

\[
C_3=C_4=1.3333333333\times10^{-15}.
\]

The exact hard scales are

\[
\boxed{
\Lambda_3^{\rm exact}
=2.0420805864\times10^{10}\ {\rm GeV},
}
\]

\[
\Lambda_4^{\rm exact}
=3.3347036336\times10^{10}\ {\rm GeV}.
\]

The whole-corridor lower estimate evaluated at the same point is

\[
\Lambda_{\rm hard}^{\rm floor}
=1.6336644691\times10^{10}\ {\rm GeV}.
\]

The pure projected self-channel scales are

\[
\Lambda_{3,S}=5.4455482304\times10^{25}\ {\rm GeV},
\]

before capping the description at the Planck scale, and

\[
\Lambda_{3,V}=1.6336644691\times10^{11}\ {\rm GeV}.
\]

Thus the retained mixed scalar-vector norm, not a scalar blow-up, controls the conservative floor.

The mixed graviton-flow scale is

\[
\Lambda_{hvv}=9.1324620135\times10^{17}\ {\rm GeV},
\]

and

\[
\epsilon_{\rm mix}=5.96\times10^{-8}.
\]

The corrected hard-floor ratio requirements are

\[
r_{\min}^{\rm R10}=1.15\times10^{-15},
\]

\[
r_{\min}^{1\,\rm TeV}=3.88\times10^{-6},
\]

while the metric-mixing condition requires

\[
r_{\min}^{\rm mix}=1.39\times10^{-15}.
\]

All are far below the selected `r=1/3`. Even after the multi-operator correction, the optional `1 TeV` stress scale remains more than seven orders of magnitude below the exact hard cutoff.

## 10. Why this is a hard cutoff rather than an exact partial-wave claim

Massless scalar, vector and tensor exchange creates forward-channel subtleties in a literal partial-wave diagonalization. Using angular cancellations or a `4pi` factor could raise the inferred scale, but is unnecessary here.

The branch is therefore tested with the stricter Wilsonian rule

\[
\boxed{
E<\min(
\Lambda_3^{\rm exact},
\Lambda_4^{\rm exact},
\Lambda_{hvv},
\bar M_{\rm Pl}).
}
\]

This requires every canonical vertex expansion parameter to remain below unity before any cancellation or phase-space advantage. It is sufficient for the local EFT use made here, but is not advertised as the exact first partial-wave eigenvalue.

## 11. Decision

Closed here:

```text
all I1-I4 interactions through fourth field order;
complete local K2, K3 and K4 unit-flow action;
complete compact scalar/vector cubic action;
pure scalar and pure vector cubic reductions;
multi-operator cubic and quartic sum norms;
corrected exact and global hard cutoffs;
metric-flow mixing floor and mixed-graviton scale;
large nonempty intersection with the source-backed public-frame corridor.
```

Still open:

```text
an exact angular partial-wave eigenvalue, which is not needed to raise this conservative floor;
compact-body sensitivities and strong-equivalence-principle violation;
dipole/quadrupole radiation on the p,r surface;
exact-GR gauge restoration at p,r=0;
primitive MTS derivation of the correspondence action.
```

Branch decision:

```text
PUBLIC gHat: RETAIN AS LEAD PRIVATE BRANCH;
SAME-g beta_u=0: RETAIN AS FALLBACK, NOT TRIGGERED;
4862 4.08e10 GeV: SUPERSEDED AS SINGLE-COEFFICIENT DIAGNOSTIC;
4863 exact hard norm cutoff: 2.04e10 GeV at the working point;
NEXT DECISIVE TEST: compact-body sensitivity and dipole-radiation scaling.
```

Primary cross-checks: [Jacobson and Mattingly](https://arxiv.org/abs/gr-qc/0007031), [Withers](https://arxiv.org/abs/0905.2446), [Oost, Mukohyama and Wang](https://arxiv.org/abs/1802.04303), and [Gupta et al.](https://arxiv.org/abs/2104.04596).

Next: `4864-Y5-R2FR-one-parameter-compact-body-sensitivity-and-dipole-radiation-scaling-or-strong-field-fallback.md`.
