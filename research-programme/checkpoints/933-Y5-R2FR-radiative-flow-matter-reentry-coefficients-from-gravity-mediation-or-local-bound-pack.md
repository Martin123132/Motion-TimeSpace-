# 4917 - Gravity-mediated flow-matter re-entry and local product bound

Marker: `MTS_GRAVITY_MEDIATED_FLOW_MATTER_REENTRY_4917`

## Decision

This checkpoint calculates a first nonzero state-dependent matter-flow
coefficient instead of adding another empty coefficient ledger.

The selected parent has two sharply different hidden-visible channels.

1. Integrating the massless Einstein mode produces the universal nonlocal
   kernel

   \[
   \Gamma^{X\text{-}{\rm SM}}_{\rm EH}(q)
   =\frac{i}{M_R^2(q^2+i0)}
   \left(T_X^{\mu\nu}T^{\rm SM}_{\mu\nu}
   -\frac12T_XT_{\rm SM}\right).
   \]

   Its `1/q^2` pole is ordinary GR. It is not a local direct-flow charge.
2. The finite `R^2/C^2` strict-EFT sector has the local cross image

   \[
   \boxed{
   \mathcal L_{X{\rm SM}}^{\rm contact}
   =\frac1{M_R^4}\left[
   4a_C T_X^{\mu\nu}T^{\rm SM}_{\mu\nu}
   +2\left(a_R-\frac23a_C\right)T_XT_{\rm SM}
   \right].
   }
   \]

For a hidden perfect-fluid state this gives the first explicit local
flow-matter re-entry law:

\[
\boxed{
p_{\rm mix}
=-\frac{8a_C(\rho_X+p_X)}{M_R^4}.
}
\]

The factor `8` is fixed: the total-stress square gives a factor `4` in the
cross contact, and Hilbert variation contributes the second factor `-2` when
the contact is represented as an inverse-metric shift.

The corresponding trace shift is

\[
\boxed{
\sigma_{\rm mix}
=-\frac{
4a_Cp_X+2(a_R-2a_C/3)(-\rho_X+3p_X)
}{M_R^4}.
}
\]

This is real progress, but it is not a numerical prediction. The physical
renormalized `a_C`, `a_R` and the local closed-bath state profile are not yet
fixed. Independent mixed 1PI operators also remain outside this
curvature-squared image.

```text
universal massless cross channel      = derived; ordinary nonlocal GR
local stress-stress cross basis       = derived exactly at first EFT order
perfect-fluid p_mix                   = -8 a_C (rho_X+p_X)/M_R^4
perfect-fluid sigma_mix               = derived
vacuum enthalpy flow zero             = exact
positive-gap support flow zero        = exact for the whole contact
conditional no-cancellation cone bound= derived on the product
numeric a_C, a_R and bath profile      = open
all-orders mixed-operator zero         = not proved
```

## 1. Keep the massless pole separate

Checkpoint 4915 derives the cross exchange from the same Einstein-Hilbert
functional and matter source. For hidden stress `T_X` and visible stress
`T_SM`, the cross kernel is

\[
\Gamma^{X\text{-}{\rm SM}}_{\rm EH}
=\frac{i}{M_R^2(q^2+i0)}
\left(T_X^{\mu\nu}T^{\rm SM}_{\mu\nu}
-\frac12T_XT_{\rm SM}\right).
\]

Because

\[
\lim_{q^2\to0}\frac1{q^2}=\infty,
\qquad
\lim_{q^2\to0}q^2\frac1{q^2}=1,
\]

the channel is nonanalytic at the origin. It cannot be Taylor-matched to a
local Wilson coefficient such as `u^mu u^nu T_mu_nu`. Calling it a direct
flow charge would double-count ordinary gravity and erase the distinction
proved at checkpoint 4916.

## 2. Exact local cross basis

Checkpoint 4879 derived the first strict-EFT field-redefinition image

\[
\Delta S_{\rm contact}
=\frac1{M_R^4}\int d^4x\sqrt{-g}\left[
2a_CT_{\mu\nu}T^{\mu\nu}
+\left(a_R-\frac23a_C\right)T^2
\right].
\]

Set

\[
T_{\mu\nu}=T^X_{\mu\nu}+T^{\rm SM}_{\mu\nu}.
\]

Expanding the two squares and removing the two self pieces gives

\[
\boxed{
\Delta\mathcal L_{X{\rm SM}}
=\frac{4a_C}{M_R^4}T_X^{\mu\nu}T^{\rm SM}_{\mu\nu}
+\frac{2(a_R-2a_C/3)}{M_R^4}T_XT_{\rm SM}.
}
\]

This basis is local. If the supports have a positive gap, every cross product
vanishes pointwise. That preserves checkpoint 4879's separated-source local-GR
certificate. A pervasive or overlapping hidden state is different and must be
projected rather than silently set to zero.

## 3. Perfect-fluid projection

Use signature `(-,+,+,+)` and write the hidden state as

\[
T_X^{\mu\nu}
=(\rho_X+p_X)u^\mu u^\nu+p_Xg^{\mu\nu},
\qquad
T_X=-\rho_X+3p_X.
\]

Then

\[
T_X^{\mu\nu}T^{\rm SM}_{\mu\nu}
=(\rho_X+p_X)u^\mu u^\nu T^{\rm SM}_{\mu\nu}
+p_XT_{\rm SM}.
\]

Therefore

\[
\Delta\mathcal L_{X{\rm SM}}
=C_u u^\mu u^\nu T^{\rm SM}_{\mu\nu}
+C_TT_{\rm SM},
\]

with

\[
C_u=\frac{4a_C(\rho_X+p_X)}{M_R^4},
\]

\[
C_T=\frac{
4a_Cp_X+2(a_R-2a_C/3)(-\rho_X+3p_X)
}{M_R^4}.
\]

Represent this contact by the first-order visible inverse-metric change

\[
\delta g_{\rm SM}^{\mu\nu}
=p_{\rm mix}u^\mu u^\nu+2\sigma_{\rm mix}g^{\mu\nu}.
\]

With the convention

\[
\delta S_{\rm SM}
=-\frac12\int d^4x\sqrt{-g}\,
T^{\rm SM}_{\mu\nu}\delta g_{\rm SM}^{\mu\nu},
\]

exact coefficient matching gives

\[
-\frac12p_{\rm mix}=C_u,
\qquad
-\sigma_{\rm mix}=C_T.
\]

Hence

\[
\boxed{p_{\rm mix}=-8a_C(\rho_X+p_X)/M_R^4}
\]

and the trace result quoted in the decision. The executable calculation
expands both representations symbolically and obtains zero residual.

The metric-shift representation is a field basis for the first strict-EFT
contact, not a second fundamental metric and not an all-orders resummation.
Physical comparisons must keep every operator at the same EFT order.

## 4. Exact zero conditions

The anisotropic coefficient obeys

\[
p_{\rm mix}=0
\quad\Longleftrightarrow\quad
a_C(\rho_X+p_X)=0
\]

for finite nonzero `M_R`. This gives two intrinsic zeros:

- `a_C=0` eliminates the Weyl-contact route;
- `rho_X+p_X=0` eliminates the flow direction. A vacuum-like state has no
  physical preferred four-velocity even though a trace contact may remain.

There is a third geometric zero:

\[
\operatorname{supp}(T_X)\cap
\operatorname{supp}(T_{\rm SM})=\varnothing
\quad\Longrightarrow\quad
\Delta S^{X{\rm SM}}_{\rm contact}=0.
\]

For a generic overlapping visible source the complete contact vanishes only
when both

\[
a_C(\rho_X+p_X)=0
\]

and

\[
4a_Cp_X
+2\left(a_R-\frac23a_C\right)(-\rho_X+3p_X)=0
\]

hold. For classical four-dimensional Maxwell, `T_SM=0`, so the trace shift
does not alter its principal cone at this order. The anisotropic enthalpy
piece remains unless one of its exact zeros applies.

Useful state specializations are

\[
p_X=-\rho_X:
\quad p_{\rm mix}=0,
\]

\[
p_X=0:
\quad p_{\rm mix}=-8a_C\rho_X/M_R^4,
\]

\[
p_X=\rho_X/3:
\quad p_{\rm mix}=-\frac{32a_C\rho_X}{3M_R^4}.
\]

## 5. Conditional cone bound

In the contact field basis the leading graviton kinetic term is Einstein and
the universal visible inverse metric is

\[
g_{\rm m}^{\mu\nu}
=g^{\mu\nu}+p_{\rm mix}u^\mu u^\nu.
\]

In the local state rest frame,

\[
c_{\rm m}^2=\frac1{1-p_{\rm mix}},
\qquad
\delta_c:=\frac{c_T}{c_{\rm m}}-1
=\sqrt{1-p_{\rm mix}}-1.
\]

The exact kinematic inversion is

\[
\boxed{p_{\rm mix}=1-(1+\delta_c)^2.}
\]

At the retained first strict-EFT order,

\[
\boxed{
\delta_c
=-\frac12p_{\rm mix}+O(p_{\rm mix}^2)
=\frac{4a_C(\rho_X+p_X)}{M_R^4}+O(a_C^2).
}
\]

Thus the signed product interval below follows directly at the order at which
the contact was derived; using the exact kinematic inversion changes it only
at second order.

Using the interval retained at checkpoint 4860,

\[
-3\times10^{-15}\le\delta_c\le7\times10^{-16},
\]

gives

\[
-1.40000000000000049\times10^{-15}
\le p_{\rm mix}\le
5.999999999999991\times10^{-15}.
\]

Since `p_mix=-8a_C(rho_X+p_X)/M_R^4`, the signed product interval is

\[
\boxed{
-7.49999999999998875\times10^{-16}
\le
\frac{a_C(\rho_X+p_X)}{M_R^4}
\le
1.75000000000000061\times10^{-16}.
}
\]

A conservative symmetric statement is

\[
\boxed{
\left|\frac{a_C(\rho_X+p_X)}{M_R^4}\right|
\le7.5\times10^{-16}.
}
\]

This is a conditional no-cancellation product bound. It applies when the
hidden state is homogeneous, or when its path average is the relevant
coefficient, and when no independent mixed operator cancels the same cone
projection. It is not a pointwise laboratory bound on an arbitrary
inhomogeneous bath profile.

The observation interval is sourced through checkpoint 4860 to the
[GW170817/GRB170817A relative-speed analysis](https://arxiv.org/abs/1710.05834).

## 6. Loop anchor and why it is not the answer

Checkpoint 4876 derived for one real scalar

\[
a_{C,{\rm scalar}}=\frac{L}{1920\pi^2},
\]

and checkpoint 4877 generalized the healthy matter contribution to

\[
a_{C,{\rm matter}}=\frac{LW_C}{1920\pi^2}.
\]

The one-real-scalar component would give

\[
p_{{\rm mix},{\rm scalar}}
=-\frac{L(\rho_X+p_X)}{240\pi^2M_R^4}.
\]

The conservative cone envelope then maps to

\[
\left|\frac{L(\rho_X+p_X)}{M_R^4}\right|
\lesssim1.4212\times10^{-11}
\]

on that component-only benchmark. This is not a prediction because

\[
a_C^R
=a_C^{\rm bare}+a_C^{\rm threshold}+a_C^{\rm matter}
+a_C^{H/{\rm ghost}}+\cdots
\]

and the finite total is matching data until the complete parent spectrum and
renormalization condition fix it. The same ownership issue applies to `a_R`.

## 7. What has and has not closed

Closed here:

```text
massless EH cross channel separated from local Wilson matching;
exact X-SM stress-contact basis;
factor and sign of p_mix;
trace coefficient sigma_mix;
vacuum, coefficient and support zeros;
conditional signed and symmetric cone-product bounds;
one-real-scalar loop projection as a non-total anchor.
```

Still open:

```text
the renormalized total a_C and a_R of the actual parent;
the local and cosmological h_X=rho_X+p_X state profile;
clock, WEP and massive-matter projection of sigma_mix;
independent u u F F, Higgs, fermion and hidden-scalar 1PI operators;
possible cancellations among a complete same-order operator basis;
strong-field and global-sector interfaces.
```

The all-orders zero from checkpoint 4916 is therefore not restored. Instead,
one calculable gravity-mediated piece of the re-entry basis has been filled,
its exact zeros have been proved and its observable product has been bounded.

## 8. Next target

`4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-aC-aR-matching-or-multiarena-bound.md`

Use the actual closed scalar-bath state to derive or bound `rho_X+p_X` and
`-rho_X+3p_X`, assemble the renormalized `a_C/a_R` matching decomposition, and
project `sigma_mix` into clocks and WEP alongside the cone product. This must
either yield sourced numbers or leave a sharply scoped product bound; it must
not return to a generic missing-coefficient inventory.

No GitHub action or public claim is authorized.
