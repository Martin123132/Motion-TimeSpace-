# 3105 - Y5 R2FR EM wave/Poynting public-geometry route under AX1090

**Purpose:** answer the objection properly: before locking the local-GR branch to an Einstein-Hilbert left-hand choice, check whether EM waves, Maxwell stress, the Poynting vector, radiation pressure, and constitutive background-field structure can help derive the public geometry rule or expose a missing residual.

**Verdict:** the Poynting route is real and useful, but it does not by itself derive the Einstein-Hilbert operator. It can help derive or test the **public metric/Hodge/cone/source** side: EM waves identify the light cone, Poynting flux supplies an energy-momentum current, and Maxwell stress enters the same Hilbert source. The actual EH left-hand operator still needs a separate parent-action selection or residual tensor.

## Source Register

| source_id | source | relevant point |
|---|---|---|
| SRC3105_0 | `3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md` | left-hand branch is `EH + E_res_munu`; matter/source side is quotient-owned |
| SRC3105_1 | `1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md` | unique Maxwell subblock theorem exists as a target but does not close; independent `F_Q^2` remains legal |
| SRC3105_2 | `1109-Y5-R10-no-independent-lambda-F2-theorem-or-finite-alpha-coefficient-acquisition.md` | universal Maxwell normalization can be calibration-only; hidden/running/readout dependence becomes finite alpha residual |
| SRC3105_3 | `1234-Y5-R10-EM-owner-uniqueness-or-quark-gluon-edge-owner-proof.md` | EM owner uniqueness fails mainly at unique `F_Q^2`, current normalization, and readout descent |
| SRC3105_4 | `1135-Y5-R10-FD-gradient-flow-constitutive-law-or-epsilon-closure-demotion.md` | constitutive-law analogy exists elsewhere but was not derived from parent variables |
| SRC3105_5 | `09-hamiltonian-radial-cell-derivation.md` | null propagation alone was already known to be insufficient for a stronger reciprocity theorem |

## Core EM/Poynting Facts

In a quotient/public Maxwell branch, write the EM action as

```text
S_EM = -1/4 int sqrt(-g_pub) Z_Q F_munu F^munu
```

where `Z_Q = g_EM^{-2}` is the Maxwell kinetic normalization. The Hilbert stress tensor is

```text
T_EM_munu =
  Z_Q (F_muα F_nu^α - 1/4 g_pub_munu F_αβ F^αβ).
```

For an observer with four-velocity `u^mu`, the measured energy density and Poynting flux are the spatial decomposition of this same tensor:

```text
u_EM = T_EM_munu u^mu u^nu
S_EM^a = -h^a_mu T_EM^munu u_nu
```

In ordinary local units this is the familiar

```text
S = E x B / mu0.
```

So the Poynting vector is not an extra optional decoration. It is the EM energy-flux piece of the stress-energy that the gravitational field must see.

## Branch A: Poynting As Ordinary Quotient Stress

If EM belongs to the same quotient matter/public-geometry functor as `3103`, then

```text
S_EM = S_EM[A_Q, g_pub, Z_Q(q(Phi), ell_EM)]
Lie_vX Z_Q = 0
```

and the total source in the local field equation becomes

```text
T_total_munu = T_matter_munu + T_EM_munu + T_binding_munu + ...
```

with no separate hidden `Xhat` source in the Poynting flux.

This branch supports `3104` because the electromagnetic wave momentum is now on the same right-hand side as matter:

```text
G_munu + Lambda_* g_munu + E_res_munu = kappa_* T_total_munu.
```

But it inherits the old EM-owner blocker:

```text
Z_Q must be quotient-owned or fixed representation/topological data.
```

If `Z_Q = Z_Q(Xhat)` or if an independent `f(Xhat)F^2` term is allowed, then EM waves carry a vertical coupling and the local branch must retain `b_alpha`, clock/WEP, and radiation-pressure residuals.

## Branch B: Premetric/Constitutive Background-Field Route

This is the route closest to the user's intuition that the Poynting vector works on a background field.

Instead of starting with metric Maxwell, start with

```text
dF = 0
dH = J
H^munu = 1/2 chi^munuαβ F_αβ.
```

Here `chi` is the constitutive tensor supplied by the MTS background/flow/public quotient. The Poynting vector and wave momentum are then built from `F` and `H`, not inserted after the fact.

The local-vacuum Maxwell/GR limit is recovered if the constitutive tensor collapses to a metric Hodge star:

```text
chi^munuαβ =
  Z_Q sqrt(-g_pub) (g_pub^μα g_pub^νβ - g_pub^μβ g_pub^να).
```

This gives:

```text
H = Z_Q *_{g_pub} F
S_EM = -1/4 int F wedge H
```

and EM waves propagate on the null cone of `g_pub`.

This is the serious background-field route:

1. The MTS background does not directly replace Maxwell.
2. It supplies the constitutive/Hodge structure.
3. Non-birefringent EM waves determine the conformal class of `g_pub`.
4. Positive energy and impedance/normalization fix the remaining scale data.
5. Poynting flux becomes the stress-energy flux of the public geometry, not a second hidden source.

## What Branch B Can Derive

If the parent action gives a local, linear, reciprocal, nondispersive, positive constitutive law with a single degenerate Fresnel cone, then the EM wave sector can derive the **public light-cone/Hodge** structure:

```text
MTS background constitutive law
  -> unique non-birefringent Fresnel cone
  -> conformal metric class [g_pub]
  -> H = Z_Q *_{g_pub} F
  -> Poynting flux = T_EM^{0i} in that public geometry.
```

This would be a meaningful derivation of part of the public geometry rule. It is exactly the kind of place we should look.

## What Branch B Cannot Derive Alone

Even if EM waves derive the public null cone, they do not uniquely choose the gravitational left-hand operator.

The following all can share the same local Maxwell cone/source structure unless separately excluded:

```text
Einstein-Hilbert
f(R)
R^2 / Ricci^2 / Weyl^2 corrections
torsion/nonmetricity theories with metric Maxwell readout
scalar-tensor theories with quotient-fixed EM
boundary/topological residuals
```

So the Poynting route can strengthen the route to `g_pub`, same-source stress, and Bianchi accounting, but it does not replace the `EH + E_res_munu` fork from `3104`.

## Double-Counting Guard

This is crucial.

Poynting energy can enter only one way in the local branch:

```text
ordinary EM stress in T_total_munu
```

or

```text
independent background/hidden flux in E_res_munu.
```

It cannot be counted in both. If the EM wave is a public Maxwell excitation, its energy flux belongs to `T_EM_munu`. If the MTS background has an additional non-EM flow carrying energy, that is a separate residual stress and must be named in `E_res_munu`.

This prevents an attractive but fatal mistake: using the Poynting vector to explain the gravitational source and then also adding a hidden background flux that duplicates the same energy.

## Poynting Route Decision Table

| route_id | route | closes if | consequence if closed | if not closed |
|---|---|---|---|---|
| PR3105_0_metric_Maxwell | `S_EM=-Z_Q/4 int sqrt(-g)F^2` | `Z_Q` is quotient-owned and `Lie_vX Z_Q=0` | Poynting flux is ordinary public Hilbert stress | retain `b_alpha`, clock/WEP/EM residuals |
| PR3105_1_constitutive_metric | `H=chi(F)` derives `H=Z_Q *F` | parent `chi` is local, reciprocal, nonbirefringent, positive, nondispersive | EM waves derive public cone/Hodge structure | retain birefringence/anisotropy/medium residual |
| PR3105_2_Bianchi_source | `T_EM` comes from same action as matter and metric | `dF=0`, `dH=J`, Lorentz exchange with matter, no hidden source weights | total stress conservation becomes clean | retain EM current/source-normalization residual |
| PR3105_3_EH_operator | Poynting derives EH left-hand operator | would need additional variational theorem selecting metric second-order spin-2 dynamics | not achieved by EM waves alone | return to `EH + E_res_munu` fork |
| PR3105_4_background_flux | MTS has non-EM background energy flow | distinct variable/stress and no double-counting with `T_EM` | explicit `E_res_munu` component with wave/flux projection | cannot be used as ordinary Poynting evidence |

## Resulting Local Equation

With EM included honestly, `3104` should be sharpened to:

```text
G_munu[g_pub] + Lambda_* g_munu + E_res_munu
  = kappa_* (T_matter_munu + T_EM_munu + T_binding_munu + T_other_public_munu).
```

The Poynting vector is then the spatial flux part of `T_EM_munu`. In weak-field/radiation regimes it contributes radiation pressure and momentum flux to the source side. In local vacuum without EM radiation, it vanishes and cannot be used to close the pure gravitational residual.

## Claim Status

No local-GR, Newton, Maxwell-owner, `b_alpha=0`, alpha-drift, WEP, clock, R10, or PPN pass is claimed here.

But this checkpoint does change the route:

```text
Do not lock the public geometry branch until the EM constitutive/Hodge route is checked.
Poynting can help derive the public metric cone and source stress.
Poynting cannot by itself derive the EH operator.
Any extra background energy flow must live in E_res_munu, not also in T_EM_munu.
```

## Next Best Step

Write:

```text
3106-Y5-R2FR-constitutive-Hodge-star-derivation-or-EM-medium-residual-under-AX1090.md
```

Task: search the MTS object language for an existing constitutive/Hodge structure:

```text
H = Z_Q *_{g_pub} F
```

or for a parent `chi^munuαβ` whose Fresnel cone reduces to the public metric cone. If found, this strengthens the public geometry derivation. If not, keep an explicit EM-medium residual vector:

```text
Delta_chi, birefringence, anisotropy, dispersion, impedance drift, b_alpha, current-normalization residual.
```
