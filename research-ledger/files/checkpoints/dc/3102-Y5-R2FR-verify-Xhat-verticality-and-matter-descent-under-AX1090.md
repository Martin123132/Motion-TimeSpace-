# 3102 - Y5 R2FR verify Xhat verticality and matter descent under AX1090

**Purpose:** stop circling the `c_g` coupling. This note makes the actual theory move: either adopt quotient-descended ordinary matter as the parent-action rule, which forces `c_g=0`, or reject it and accept that MTS contains a finite fifth-force coupling that must be sourced and tested.

## Verdict

The current corpus already contains the exact conditional theorem shape:

- `e_obs=Obs_e(q_loc(Phi))` and `v_X in ker(Dq_loc)` imply `Lie_v e_obs=0`.
- If every ordinary matter-frame, constant, and marker function factors through `q_loc`, its vertical derivative vanishes.
- A shadow frame `A_g(Xhat)e_obs` is forbidden unless `A_g` is constant along the quotient fibre.

What was missing was not another audit. The needed extension is a parent-action domain rule:

```text
Q_obs := P_parent / ~,     Phi ~ Phi' iff q(Phi)=q(Phi')
v_X in ker(Dq)
e_pub = e_pub(q(Phi))
S_matter = Sbar[psi, e_pub(q(Phi)), omega[e_pub], theta(q(Phi))]
Allowed[S_matter] excludes A_g(Xhat)e_pub, B_g(Xhat), alpha_EM(Xhat), m_A(Xhat), clock_i(Xhat), and source-only weights unless they are explicitly retained residual fields.
```

This is the smallest clean extension because it does not add a fitted coefficient. It removes the ordinary-matter shadow slot.

## Derivation

Let `P_parent` be the parent configuration space and let `q:P_parent -> Q_obs` be the observable quotient. Let `v_X` be the local variation associated with `Xhat`.

Assume:

```text
Dq[v_X] = 0
S_matter[Phi,psi] = Sbar[psi, e_pub(q(Phi)), omega[e_pub], theta(q(Phi))]
```

Then:

```text
delta_X S_matter
= D Sbar · delta_X(q(Phi))
= D Sbar · Dq[v_X]
= 0
```

So ordinary Hilbert matter has no `Xhat` source current:

```text
J_X^matter := delta S_matter / delta Xhat = 0
```

For a possible conformal shadow frame:

```text
e_m = A_g(Xhat) e_pub(q(Phi))
```

this descends to `Q_obs` only if it is constant on each quotient fibre:

```text
v_X[ln A_g] = 0
```

Therefore:

```text
c_g := partial_X ln A_g |_{0} = 0
```

and the common scalar PPN charge from this channel vanishes:

```text
alpha_eff_PPN,cg = tau_PPN c_g S_PPN / sqrt(Z_X) = 0
```

## What This Does And Does Not Prove

This proves a clean conditional route to killing the `c_g` coupling by construction. It does **not** yet prove the full local GR/Newton limit because the left-hand field equation, boundary/support residuals, constants, disformal slots, and non-Hilbert tails still have to be either quotient-descended or explicitly retained.

But it does move the framework forward:

- If MTS adopts this parent-action domain rule, the `c_g` problem is not a tuning problem; it is a quotient-descent theorem.
- If MTS rejects this rule, `c_g` is physical and must be treated as a finite fifth-force coupling with `Z_X`, `M_X^2`, `tau_PPN`, `S_PPN`, and bound rows.
- There is no consistent middle route where `c_g` is not owned, not zero, and not tested.

## Current-Corpus Check

Existing files support the shape but do not already sign it as the active parent action:

- `1045` gives the parent matter functor theorem shape: `e_obs=Obs_e(q_loc(Phi))` and `v_X in ker(Dq_loc)` force `Lie_v e_obs=0`.
- `1046` gives the no-shadow/constant-marker chain-rule theorem shape.
- `1038` records that matter/no-marker descent was still not parent-signed.
- `3101` turns this into the zero-or-finite coupling fork.

So `3102` upgrades the route from “missing target” to an explicit proposed parent-action extension:

```text
Ordinary matter is a functor of the observable quotient Q_obs only.
Representative vertical directions are gauge/description, not physical matter arguments.
All non-quotient matter-frame/constant/source dependencies are retained residual fields, not hidden assumptions.
```

## Decision

Adopt the quotient-descended matter rule as the preferred local-GR branch unless a core MTS document explicitly requires ordinary matter to couple to representative `Xhat`.

The next useful work is not another checkpoint. It is a direct conflict search:

```text
Find every place in the corpus where ordinary matter, EM constants, particle masses, clocks, or source weights depend directly on Xhat.
For each one: either rewrite it as quotient-owned theta(q), retain it as an explicit residual coefficient, or reject the c_g=0 branch.
```

## First Conflict Search Result

I ran the first direct search against the current `post-checkpoint-work` corpus for:

```text
A_g(Xhat), B_g(Xhat), alpha_EM(Xhat), m_A(Xhat), clock_i(Xhat),
theta(q(Phi),Xhat), theta_A(Xhat), source-only weights,
S_matter = Sbar[psi, A_g(...], S_A[Psi_A,A_A(Xhat)...],
f(Xhat)F^2, w_A S_A
```

The hits do **not** look like an existing core commitment that ordinary matter must depend directly on `Xhat`. They mostly appear as:

- countermodels showing why covariance/WEP alone cannot kill `c_g`;
- finite-route examples that must be retained if the zero theorem fails;
- no-shadow/no-extra-operator requirements already identified in older work;
- source-weight counterexamples showing that `S_matter=sum_A w_A S_A` must be forbidden by parent syntax/action measure, not ignored.

So the quotient-descended matter extension survives first contact, but it needs one extra clause to be honest:

```text
NoSourceOnlySpeciesSlot:
Species labels may choose representation data and quotient-owned constants theta_A(q),
but may not choose active gravitational source multipliers w_A,
hidden source coefficients kappa_A,
or pre-variation action weights not fixed by the unique parent action measure.
```

With this included, the preferred parent matter domain becomes:

```text
S_matter =
  sum_A S_A[
    Psi_A,
    e_pub(q(Phi)),
    omega[e_pub],
    theta_A(q(Phi), representation_A)
  ]

Forbidden unless explicitly retained as residuals:
  A_A(Xhat), B_A(Xhat), f_X(Xhat)F^2,
  m_A(Xhat), y_A(Xhat), clock_i(Xhat),
  material_marker_A(Xhat), w_A S_A, kappa_A J_A.
```

This is now a real proposed extension of MTS, not just a missing-input note. It says ordinary matter lives on the public quotient geometry, while every non-quotient `Xhat` dependence is either impossible by parent syntax or becomes an explicit residual coefficient.

## Claim Status

`c_g=0` is now a proposed parent-action extension with a clean proof, not yet a public claim about current MTS.

No R10, PPN, local-GR, Newton-limit, WEP, clock, orbital, or GitHub claim follows until the conflict search is done.
