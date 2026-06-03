# 177 - Parent Action, Perturbation, Local-GR Contract

Private derivation contract. This is not a public claim.

## 1. Trigger

Checkpoint 176 decided that the next useful move is not another broad scoring
refresh. The empirical late-time/non-CMB card is clean enough for private
priority-setting. The bottleneck is now derivation.

This checkpoint writes the exact contract a future parent action must satisfy
before the locked no-clock branch can be treated as a serious field-theory
candidate rather than a disciplined empirical closure.

## 2. Machine Artifact

Script:

```text
scripts/parent_action_perturbation_local_GR_contract.py
```

Run:

```text
runs/20260531-235959-parent-action-perturbation-local-GR-contract
```

Command:

```text
python scripts/parent_action_perturbation_local_GR_contract.py --timestamp 20260531-235959
```

Status:

```text
parent_action_perturbation_local_GR_contract_written_not_derived
```

Claim ceiling:

```text
parent_action_contract_only_no_derivation_or_promotion
```

## 3. What This Checkpoint Did

It wrote a machine-readable contract for:

| output | file |
|---|---|
| source audit | `source_register.csv` |
| promotion blockers | `promotion_blocker_map.csv` |
| minimal parent action | `minimal_parent_action_contract.csv` |
| field/variable ownership | `field_variable_contract.csv` |
| variation requirements | `variation_requirement_contract.csv` |
| perturbation outputs | `perturbation_output_contract.csv` |
| local GR silence | `local_GR_silence_contract.csv` |
| CMB/Boltzmann interface | `CMB_interface_contract.csv` |
| amplitude/domain ownership | `amplitude_and_domain_ownership_contract.csv` |
| forbidden closures | `forbidden_closure_ledger.csv` |
| pass/fail gates | `acceptance_gates.csv` |
| decision | `decision.csv` |

It did not derive the action.

It did not promote the theory.

It did not claim CMB success, local GR derivation, perturbation completion, or
that `B_mem = 2/27` is predicted.

## 4. Active Promotion Blockers

The contract carries forward the six active blockers from checkpoint 176:

| gate | blocker | contract target |
|---|---|---|
| P04 | parent perturbation action missing | parent action variation contract |
| P06 | `F_fric(a,k)`, `mu(a,k)`, and `S_mem(a,k)` not derived | perturbation output contract |
| P07 | CMB Boltzmann-level interface missing | CMB interface contract |
| P08 | local GR / PPN silence not derived | local GR silence contract |
| P09 | zero-knob domain selector `D` not derived | domain selector contract |
| P10 | `B_mem = 2/27` empirical, not parent-derived | amplitude owner contract |

This is now the title-belt problem.

The empirical card can keep MTS in the fight, but these six rows decide whether
it is a field theory rather than a clever closure.

## 5. Minimal Parent Action Contract

The future parent action must own, at minimum:

```text
S_parent =
int d^4x sqrt(-g) [
  R/(16 pi G)
  + L_m(g, psi_m)
  + L_mem(g, Q, D, M, lambda_M)
  + L_D(g, D, chi_D, lambda_D)
  + L_Q(g, D, Q, lambda_Q)
]
+ S_boundary[g, D, Q, R, lambda_R].
```

Required sectors:

| sector | required ownership |
|---|---|
| metric | one metric/coframe used by matter, cosmology, lensing, and local PPN |
| matter | universal coupling with no hidden matter-sector spread |
| domain selector | zero-knob `D` or `chi_D` mechanism |
| load tensor | parent-owned `Q^A_B` before FLRW reduction |
| memory stress | `E_mem^{mu nu}` from variation, not fitted as a fluid by hand |
| boundary charge | endpoint law that fixes `DeltaR = 2/9` and then `B_mem = 2/27` |
| two-point ruler | sidecar only unless a parent source law is derived |

## 6. Variation Contract

The future action has to pass these reductions:

| variation | pass condition |
|---|---|
| `delta_g S_parent = 0` | Bianchi-compatible metric equation with total stress owned by the action |
| `nabla_mu E_total^{mu nu} = 0` | no inserted local force; `q_loc^nu -> 0` follows or is tightly bounded |
| `delta_Q S_parent = 0` | load tensor source law gives FLRW `Q^i_j = X_D delta^i_j` |
| `delta_D S_parent = 0` | coherent domains selected without threshold knobs |
| `delta_M S_parent = 0` | exact auxiliary memory or high-sound-speed suppression is derived |
| `delta_R S_parent = 0` | endpoint/boundary-charge law fixes the locked amplitude before data scoring |

No plateau axiom is allowed.

No post-fit amplitude story is allowed.

No pair-ruler half-kernel is allowed inside the no-clock lead branch.

## 7. Perturbation, CMB, And Local-GR Contract

Perturbation outputs required:

| output | required limit |
|---|---|
| `F_fric(a,k)` | tends to zero in the GR limit |
| `mu(a,k)` | tends to one, or is bounded by a derived smooth-memory law |
| `eta_slip(a,k)` / `Sigma(a,k)` | no hidden lensing slip |
| `S_mem(a,k)` | derived source term, not an inserted growth correction |
| `c_s_eff^2` or constraint owner | avoids Boltzmann denominator pathologies |

Local-GR outputs required:

| output | required local behavior |
|---|---|
| `q_loc^nu` | vanishes or is bounded below tested limits |
| `G_eff/G` | tends to one |
| `gamma`, `beta` | tend to one |
| `alpha_clock`, `epsilon_matter` | vanish or satisfy known bounds |
| `Phi - Psi` | no local slip in the tested weak-field limit |

CMB interface outputs required:

```text
rho_mem(a), w_mem(a), c_a^2(a), c_s_eff^2(a,k),
delta_mem, theta_mem, sigma_mem or exact auxiliary constraints.
```

Background safety is not a CMB pass. A future CMB claim needs a real
Boltzmann-level run with TT/TE/EE/lensing and no hand-tuned bridge.

## 8. Gate Results

All contract-writing gates passed:

| gate | result |
|---|---|
| all cited sources exist | pass |
| active blockers mapped | pass |
| parent action terms specified | pass |
| perturbation outputs specified | pass |
| local GR silence specified | pass |
| CMB interface requirements specified | pass |
| amplitude/domain owner specified | pass |
| theory promotion blocked | pass |
| claim ceiling preserved | pass |

The important point is the seventh and eighth row together:

```text
we now know what has to be owned, and we are explicitly not pretending it is
owned yet.
```

## 9. Decision

Decision:

```text
parent_action_perturbation_local_GR_contract_written_not_derived
```

Meaning:

```text
MTS has a clean derivation contract. The no-clock locked branch remains the lead
empirical target, but promotion is blocked until the parent action derives the
memory stress, perturbation functions, local GR silence, domain selector, and
2/27 amplitude.
```

Boxing-card readout:

```text
This does not win the belt. It writes the judges' score sheet before the title
fight starts. From here, every clever move has to land on the same card as GR,
LCDM, growth, CMB, and local PPN.
```

## 10. Next Target

Create:

```text
178-memory-perturbation-owner-attempt.md
```

Next task:

```text
Attempt the first real owner derivation: either construct an auxiliary/high-
sound-speed memory sector that derives F_fric(a,k), mu(a,k), slip/Sigma(a,k),
and S_mem(a,k), or demote the perturbation/growth support to explicit
closure-only status.
```
