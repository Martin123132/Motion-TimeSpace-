# 3119 - Same-Current Owner or `delta_J` Source/Test Residual Priority under AX1090

Private checkpoint. This follows 3118: after `b_alpha`, the next EM/source-coupling leak is hidden current normalization.

## Verdict

The same-current owner theorem has a clean conditional form:

```text
A_Q, T_Q, charge labels n_A, matter current J_A, and source/test coupling
all descend from the same parent visible U(1) owner or fixed representation data
```

implies:

```text
delta_J = 0.
```

But the current corpus does **not** parent-sign that theorem yet. Existing files keep the same-current owner as an explicit unsigned clause. Therefore `delta_J` remains the second-priority finite EM residual after `b_alpha`.

Important distinction:

```text
Ward conservation:
  proves the selected current is conserved.

Same-current ownership:
  proves the selected current normalization cannot carry hidden source/test weights.
```

The local-GR/Maxwell route needs the second statement, not just the first.

## Source Register

| source_id | path | role |
|---|---|---|
| 1062 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md` | WEP alpha/source-normalization theorem and source-label counterexamples |
| 1088 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md` | minimal ordinary matter signature and source-weight countermodels |
| 1098 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md` | ordinary constant/source-weight owner signature |
| 1100 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md` | `T_Q`, charge lattice and same-current owner gate |
| 3116 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md` | `delta_J` as EM source/test residual |
| 3118 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3118-Y5-R2FR-no-hidden-visible-coefficient-hom-for-local-EM-or-balpha-product-bound-runner-under-AX1090.md` | `b_alpha` runner and next `delta_J` target |

## Definitions

Let the visible EM interaction be:

```text
S_int = integral sqrt(-g_pub) A_Q_mu J_Q^mu.
```

The clean parent-owned current has:

```text
J_Q^mu = sum_A n_A J_A^mu,
```

where:

```text
n_A := fixed representation/charge-lattice weight,
J_A^mu := Noether/Ward matter current of species A in the public quotient frame.
```

The hidden current-normalization residual is:

```text
J_Q^mu(y) = sum_A n_A [1 + delta j_A(y)] J_A^mu,
delta_J_A := Lie_v delta j_A,
```

or, more invariantly:

```text
delta_J_A := Lie_v ln c_A(y)
```

for hidden source/test current weight `c_A(y)`.

## Same-Current Owner Theorem

**Claim.** In the compact local branch, if:

```text
1. A_Q is the public projection of a parent charge generator T_Q;
2. charge labels n_A are fixed representation/lattice data;
3. matter action is q-basic:
   S_matter = sum_A S_A[Psi_A, e_pub(q), A_Q(q), n_A, theta_A];
4. no q_A(y), c_A(y), w_A(y), kappa_A(y), source-only material weights, or post-variation current selectors exist;
5. radiative/readout reduction preserves this current owner;
```

then:

```text
delta_J_A = 0
```

for every compact local vertical generator.

**Proof.**

For `v in ker(Dq_parent)`:

```text
Dq_parent[v] = 0.
```

If:

```text
A_Q = Abar_Q(q_parent(Phi)),
J_A = Jbar_A(q_parent(Phi), Psi_A, theta_A),
n_A = fixed representation data,
Lie_v theta_A = 0,
```

then:

```text
Lie_v A_Q = 0,
Lie_v n_A = 0,
Lie_v J_A = 0
```

up to gauge/diffeomorphism/local-Lorentz matter lifts already accounted for in the public quotient.

Therefore:

```text
Lie_v J_Q^mu
= Lie_v sum_A n_A J_A^mu
= 0.
```

No hidden source/test current derivative remains:

```text
delta_J_A = 0.
```

This theorem is exact conditional. It is not a current MTS claim because `T_Q`, fixed charge base unit, no source-only weights, and radiative/readout closure remain unsigned.

## Why Ward Conservation Is Not Enough

Gauge invariance can give:

```text
nabla_mu J_Q^mu = 0.
```

But conservation does not prove unique normalization.

A countermodel can use:

```text
J_Q^mu = sum_A n_A c_A(y) J_A^mu
```

where `c_A(y)` is a hidden material/source/test marker that is constant along the selected matter flow or inserted before readout. Such a construction can preserve a conserved selected current while changing source/test response.

So:

```text
conserved current != same parent current owner.
```

The parent action must forbid `c_A(y)` slots or derive them as q-basic/fixed representation data.

## Countermodels

| countermodel_id | term | why it survives without same-current owner | residual |
|---|---|---|---|
| DJ3119_0 | `sum_A n_A c_A(y) A_Q J_A` | hidden source/test charge weights can preserve visible gauge form while changing material response | `delta_J_A` |
| DJ3119_1 | `sum_A w_A(y) S_A` | source-only matter weights can alter active source/readout without changing public metric descent | `qbar_source_weight` |
| DJ3119_2 | post-variation current selector | current is extracted after material/readout projection rather than from one parent action | `delta_J_readout` |
| DJ3119_3 | hidden charge-base normalization `Q_*(y)` | relative integer labels stay fixed but observed base unit floats | `delta_Qstar` |
| DJ3119_4 | radiative/source threshold `delta J_rad(y)` | tree-level current owner can be reopened after effective reduction | `delta_J_rad` |

These are legal enough as countermodels that they cannot be erased by saying "U(1) current exists."

## Observable Projections

`delta_J` feeds three immediate arenas:

### WEP / composition

For two test bodies `A,B`:

```text
Delta a_AB^J
~ K_WEP(lambda) [Q_A^J - Q_B^J] beta_source_J delta_J tau_WEP.
```

The same anti-cheat rules as `b_alpha` apply:

```text
no beta_source_J = 1 by assertion,
no tau_WEP = 1 by assertion,
no clock-to-WEP transfer without parent map,
no source/test cancellation.
```

### R10 / short range

For a finite-range branch:

```text
alpha_J(lambda)
= K_X^R10(lambda) beta_s^J(lambda) beta_t^J(lambda)
  + epsilon_tail(lambda).
```

This is structurally like the 3118 `b_alpha` product runner, but the source/test legs are current-normalization legs rather than alpha-kinetic legs.

### Source calibration / local GR

If EM current normalization changes source EM binding or field stress:

```text
T_EM[J_Q(y)] -> T_EM + Delta T_EM^J.
```

Then:

```text
GM_orbit = G_eff M_pub + Delta_GM_J + ...
```

so `delta_J` also belongs in the source-coupling/local-GR residual vector, not only WEP/R10.

## Priority Decision

`delta_J` is second priority after `b_alpha` because:

1. `b_alpha` already has clock/WEP/R10 scaffolding and runner support from 3118;
2. `delta_J` can mimic source/test alpha effects even if `b_alpha=0`;
3. `delta_J` touches source calibration and local GR more directly than a pure spectral alpha drift;
4. `delta_star` and broad constitutive tensors are important, but their projection kernels are less mature.

## Claim Status

No public EM current, WEP, R10, source-calibration, local-GR, Maxwell, derived-`alpha`, derived-`G`, or unification claim follows from 3119.

The internal advance is:

```text
same-current owner theorem is written;
Ward conservation is separated from normalization ownership;
delta_J is promoted to the second finite EM residual priority;
WEP/R10/source-calibration projection forms are staged without claim.
```

## Next Target

Write:

```text
3120-Y5-R2FR-deltaJ-product-bound-runner-or-current-owner-source-intake-under-AX1090.md
```

Direct target:

1. create a nonclaim `delta_J` input template paralleling 3118's `b_alpha` runner;
2. require real MTS-side `beta_source_J`, `beta_test_J`, `tau_WEP/R10`, `K_X`, material charge convention, and source paths;
3. keep all output rows nonclaim until a current-owner theorem or finite sourced coefficients exist.
