# 3115 - Local Vertical Noether Generator Certificate under AX1090

Private checkpoint. This is the promised 3115 generator hunt.

## Verdict

The strict local quotient route has a real mathematical certificate:

```text
private local direction is silent
iff
it is a proper first-class vertical gauge generator with zero local boundary charge
and ordinary readouts descend through the public quotient.
```

That gives a hard rule:

```text
Dq[v] = 0 is necessary but not sufficient.

Need:
  i_v E(S_parent) = 0 off shell,
  Omega(delta Phi, v[epsilon]) = delta G[epsilon],
  G[epsilon] = int epsilon C + Q_boundary,
  {G[epsilon],G[eta]} closes first-class,
  Q_boundary = 0 or exact for compact local tests,
  DObs_A[v] = 0 for clocks, rods, photons, source mass, EM/Hodge readout and constants.
```

If a candidate fails any one of those, it is not allowed to be hidden under "vertical"; it becomes an explicit residual channel.

The important move is this: **MTS should not try to make every interesting motion/time/memory/EM idea vertical.** Local GR only requires compact local silence. Galaxy/cosmology/time/EM extension physics can survive, but only through public quotient ownership or a derived activation rule that is silent in compact local tests.

## Source Register

| source_id | path | role |
|---|---|---|
| 00-heuristics | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\00-martin-fork-heuristics-private.md` | private time/flow/EM/Poynting fork heuristic |
| 07 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\07-nonpropagating-reciprocity-constraint.md` | nonpropagating `R_AB` route |
| 10 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\10-observer-map-symplectic-contract.md` | observer map, `J_q`, `R_AB` visibility |
| 2486 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2486-Y5-R2FR-parent-field-sort-and-quotient-map-signature-or-residual-owner-split.md` | `Dq[v]` and `DObs[v]` chain-rule warning |
| 2488 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2488-Y5-R2FR-terminal-public-coframe-no-shadow-action-domain-or-first-response-kernel.md` | terminal public coframe/no-shadow conditional theorem |
| 1038 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md` | prior Omega/DCX vertical generator audit |
| 1099 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md` | EM kinetic owner/no-extra-`F^2` theorem attempt |
| 1100 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md` | parent `T_Q`, charge lattice and Maxwell norm gate |
| 3114 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3114-Y5-R2FR-strict-local-quotient-parent-signature-checklist-under-AX1090.md` | first-class vertical gauge descent theorem |

## Noether Certificate

For a local candidate vertical generator `v_epsilon`, define:

```text
delta_v Phi^A = R^A_i epsilon^i + R^{A mu}_i nabla_mu epsilon^i + ...
```

A true local gauge generator must satisfy the Noether identity:

```text
sum_A E_A(S_parent) delta_v Phi^A = d N_epsilon
```

for arbitrary compactly supported `epsilon`. Equivalently, after integrating by parts:

```text
R^dagger_i(E(S_parent)) = 0
```

off shell.

The Hamiltonian/covariant-phase-space version is:

```text
Omega(delta Phi, v_epsilon) = delta G[epsilon],
G[epsilon] = int_Sigma epsilon^i C_i + int_boundary Q_epsilon.
```

For compact local silence:

```text
C_i = 0 first-class constraints,
{G[epsilon], G[eta]} = G[[epsilon,eta]] + K_boundary,
K_boundary = 0,
Q_epsilon = 0 or exact/proper on the local boundary class.
```

Then `v_epsilon` removes a representative direction rather than adding a physical exchange pole.

## Candidate Generator Audit

| generator_id | candidate | action on public quotient | Noether certificate result | verdict |
|---|---|---|---|---|
| V3115_0 | public diffeomorphism/local Lorentz | moves representatives but preserves gauge-equivalence class of `g_pub/e_pub` | standard gauge candidate for public geometry only | useful but does not silence private residuals by itself |
| V3115_1 | abstract private representative shift `y -> y + epsilon` | `Dq[v_y]=0` by definition | certificate closes only if `i_v E(S_parent)=0` and boundary charge vanishes | conditional route theorem, not source-signed yet |
| V3115_2 | reciprocal strain `R_AB` shift | fails if `R_AB` changes `J_q`, `e_pub`, `tau_pub` or source normalization | current observer-map files treat `R_AB` as visible unless constrained | not vertical; use nonpropagating constraint or residual |
| V3115_3 | `Gamma_eff/K_hat/q_loc` sector shift | would have to leave public metric, source and PPN projections unchanged | no parent Helmholtz action or Noether current certificate is signed | not vertical yet; keep `q_loc` residual |
| V3115_4 | private memory/time shift | safe only if public `tau_pub[g_pub]` and source support are terminal | terminal clock/readout clause is conditional but not a full generator | conditional extension candidate; clock residual if it leaks |
| V3115_5 | projector/domain/Hodge selector shift | often changes source support, Hodge star, Green operator or boundary normal | Hodge/domain projector variation is already retained in older gates | not locally silent unless topological/metric-independent |
| V3115_6 | boundary/reference shift | can be proper gauge only when `Q_boundary` and cocycle vanish | fixed reference and exact boundary primitive remain unsigned | boundary residual unless exact/proper |
| V3115_7 | visible EM `U(1)` gauge `A -> A + d lambda` | leaves `F=dA`, Maxwell stress and Poynting flux invariant | standard EM gauge, but it does not fix `g_EM`, `alpha_EM` or Hodge owner | gauge redundancy yes; alpha/Hodge silence no |
| V3115_8 | private Hodge/constitutive/background-flow shift | changes `*_obs`, `alpha_EM`, constitutive tensor or Poynting readout unless quotient-owned | 1099/1100 show unique Maxwell owner is not fully signed | not vertical; make public-Hodge theorem or residual |

## Derived Negative Tests

### 1. Reciprocal strain cannot be declared vertical if it moves the observer cell

Earlier local work uses:

```text
J_q = T sqrt(S),
R_AB = ln(T^2 S) = 2 ln(J_q).
```

If a proposed vertical shift changes `R_AB`, then:

```text
delta_v R_AB != 0
=> delta_v J_q != 0
=> delta_v e_pub or tau/source readout != 0
```

unless the quotient map is explicitly redefined so that the observer cell does not see `J_q`. But `2486/2488/10` already warn that `Dq_shape[v]=0` is not enough; `DObs_e[v]=0` is the required statement.

So:

```text
R_AB is not locally vertical by declaration.
```

It must be either:

```text
R_AB = 0 as a nonpropagating constraint,
```

or an explicit PPN/clock/source residual.

### 2. Gamma/Khat/q_loc cannot be gauge unless its current is a constraint

The local residual source profile was:

```text
q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}).
```

For this to be gauge-silent, `Gamma_eff/K_hat` variations must be generated by a first-class constraint:

```text
Omega(delta Phi, v_GK[epsilon]) = delta int epsilon_nu C_GK^nu + delta Q_GK[epsilon],
C_GK^nu = 0,
Q_GK = 0 or exact.
```

If instead the sector has a physical action:

```text
S_GK ~ int sqrt(-g) [ Z_G (nabla Gamma)^2 + Z_K (nabla K)^2 + Gamma T + K_munu T^munu + ... ],
```

then:

```text
delta_GK S != boundary
```

and `q_loc^nu` is a real source/current residual. That is not a failure of MTS; it is the rule that stops local-GR from being smuggled.

### 3. Poynting flux is not hidden; it belongs either to public Maxwell stress or to a constitutive residual

The EM stress route should be:

```text
S_EM = -1/4 int sqrt(-g_pub) Z_EM F_munu F^munu,
T_EM^munu = Z_EM (F^mu_alpha F^{nu alpha} - 1/4 g_pub^munu F^2),
S^i = T_EM^{0i} in the chosen public frame.
```

Therefore the Poynting vector is not a mystical extra source outside gravity. In the local-GR branch it is part of the Hilbert stress:

```text
T_total = T_matter + T_EM + ...
```

The MTS intuition can still be valuable if the "background field" is really the parent origin of:

```text
g_pub/e_pub/Hodge star,
Z_EM or alpha_EM,
current normalization,
EM wave phase/flow readout.
```

But each option has a different local consequence:

```text
Hodge star = *[g_pub] and Z_EM quotient-owned
=> EM stress descends cleanly into GR source.

private Hodge or Z_EM varies along v
=> clocks, spectra, WEP, Poynting and source coupling acquire residuals.
```

So Poynting is a good clue for the next derivation, but not a free vertical generator.

## Certificate Matrix

| test | pass condition | current 3115 result |
|---|---|---|
| quotient kernel | `Dq[v]=0` before variation | available only as conditional shape |
| action Noether identity | `i_v E(S_parent)=0` off shell | not source-signed for private MTS sectors |
| momentum map | `Omega(delta,v)=delta G` with first-class `G` | template exists from 582/1038, not filled by parent action |
| boundary silence | `Q_boundary=0` or exact/proper | not signed for reference/projector/edge sectors |
| readout silence | clocks, rods, photons, source mass, EM constants, Hodge star descend through `q` | conditionally framed by 2488/1099/1100 but not promoted |
| degree count | private pair removed from reduced phase space | not evaluated for MTS private sectors |

## Consequence for the Local-GR Route

3115 does **not** prove local GR yet.

It proves the sharper fork:

```text
Either:
  construct the vertical Noether generator and remove the private local pole,
or:
  keep the direction as a physical residual with a PPN/R10/clock/WEP/orbital/EM projection.
```

This is progress because it forbids the loop:

```text
call it vertical -> notice missing proof -> write missing ledger -> repeat.
```

Now every candidate has a binary certificate target.

## Claim Status

No local-GR, PPN, WEP, clock, orbital, R10, Maxwell, fine-structure, Poynting, derived-`G`, or public unification claim follows from 3115.

The internal advance is:

```text
local silence requires a Noether generator certificate;
Poynting/EM is routed into public Hilbert stress or explicit constitutive residual;
R_AB and Gamma/Khat/q_loc are not allowed to be hidden as vertical without the certificate.
```

## Next Target

Write:

```text
3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md
```

Direct target:

1. derive the clean public route `S_EM[g_pub,A] -> T_EM -> Poynting -> Hilbert source`;
2. prove what must be quotient-owned: Hodge star, `Z_EM`, current normalization, charge lattice, and clock/spectral readout;
3. if the proof fails, stage the explicit EM residual vector: `delta_*`, `b_alpha`, current normalization, constitutive tensor, clock/spectral response, and Poynting/source projection.

This is the best next strike because it connects your Poynting/background intuition to the local source-coupling/GR route instead of leaving it floating as metaphor.
