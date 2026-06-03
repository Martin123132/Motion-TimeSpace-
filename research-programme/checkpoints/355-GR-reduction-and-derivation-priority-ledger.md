# 355 - GR Reduction And Derivation Priority Ledger

Private orientation/proof-queue checkpoint. This is not a public local-GR, PPN, CMB, cosmology, or unified-field claim.

## 1. Purpose

This checkpoint resets the working priority exactly:

```text
connect MTS to GR,
and replace as many fitted/closure pieces as possible with derivations.
```

The cosmology fits, local-bound runners, and robustness tests are still useful.

But they are not the centre of the programme.

The centre is:

```text
parent motion/time/space structure
    -> variational field equations
    -> local GR limit
    -> Newtonian/PPN recovery
    -> FLRW memory as a compatible projection
    -> closure constants progressively converted into theorems.
```

So the source-locked local-bound runner from checkpoint 354 is now treated as a guardrail, not the main proof.

The next decisive target is not:

```text
can a runner pass a bound?
```

It is:

```text
can the parent action produce the conservation identity and projector variation needed for local GR?
```

## 2. Machine Artifact

Script:

```text
scripts/gr_reduction_derivation_priority_ledger.py
```

Run:

```text
runs/20260601-175655-GR-reduction-derivation-priority-ledger
```

Key outputs:

```text
results/source_register.csv
results/GR_reduction_chain.csv
results/derivation_debt_ledger.csv
results/no_cheat_rules.csv
results/next_derivation_queue.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
GR_connection_and_derivation_priority_reset_no_local_GR_promotion
```

Claim ceiling:

```text
programme_orientation_and_proof_queue_only_no_GR_or_PPN_pass_claim
```

Source paths missing:

```text
0
```

## 3. Current Honest Position

The project is not dead and it is not done.

The current state is:

```text
MTS has a coherent conditional local-GR route.
MTS has a live late-time empirical closure branch.
MTS has a source-locked local-bound guardrail.
MTS does not yet derive local GR.
MTS does not yet derive the major closure constants.
```

That is not a failure state.

It means the work has narrowed to a proper field-theory fight:

```text
own the parent variation,
own the conservation identity,
own the local no-hair/silence theorem,
then compute residuals.
```

If that chain works, then MTS is no longer merely a phenomenological dark-sector fit.

It becomes a serious GR-reduction candidate.

## 4. Exact GR Connection Ladder

The safe ladder is:

```text
S_parent[g/e, X, P, boundary data, matter]
    -> delta S_parent = 0
    -> local effective equation
       G_eff_munu[g, e] = kappa T_matter_munu + E_MTS_munu
    -> Ward/Bianchi identity
       nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu) = 0
    -> local exterior no-hair/silence
       E_MTS_munu -> 0 or boundary-only with no bulk PPN support
    -> Einstein-Hilbert exterior
       G_munu + Lambda g_munu = kappa T_matter_munu
    -> Newtonian and PPN limits.
```

The important detail is order.

We cannot start by assuming:

```text
G_munu + Lambda g_munu = kappa T_munu
```

and then decorate it with MTS.

The GR operator, conservation ledger, and vanishing/screened MTS residual must be earned from the parent construction.

## 5. GR Reduction Chain

| Order | Layer | Current status | Derived status | Main blocker |
|---:|---|---|---|---|
| 1 | parent variational action | contract fragments exist | not derived | full field content and allowed variations not fixed |
| 2 | single physical geometry | specified as `N0` contract | not derived | universal matter coupling is an assumption |
| 3 | Ward/Bianchi identity | conditional ledger written | conditional | projector/boundary variation is not fully owned |
| 4 | local no-hair/silence | no-hair contract and partial boundary route | open conditional | double-zero/local suppression mechanism not parent-derived |
| 5 | Einstein-Hilbert exterior | conditional theorem | not promoted | metric-only exterior and vanishing `E_MTS` are not derived |
| 6 | Newtonian limit | follows from EH plus universal coupling | conditional | `G` normalization and local silence remain upstream |
| 7 | PPN residual vector | symbolic owner map plus source-locked targets | not calculated | closed residual coefficients not derived |
| 8 | cosmology/FLRW compatibility | compatibility route exists | partial | `B_mem`, `q_trace`, `epsilon_H`, `H_star/H0` remain closure/conditional |

This is the real scoreboard.

Local data runners sit at layer 7.

They matter, but layers 1-6 decide whether MTS actually connects to GR.

## 6. Derivation Debt Ledger

| Object | Current label | Desired label | Promotion blocked until |
|---|---|---|---|
| `N0` unique metric/coframe | contract | theorem | one geometry controls matter, clocks, rulers, lensing, and PPN |
| `N5` projector stress | hard blocker partly sharpened | zero/boundary/conserved theorem | `T_projector` is not silently dropped |
| `N6` metric-only EH exterior | conditional | local GR theorem | `E_MTS_munu` is zero/boundary-only through PPN order |
| local no-hair double zero | contract | mechanism | local gradients and amplitudes are bounded without plateau axiom |
| PPN residual vector | owner map | computed coefficients | gamma, beta, preferred-frame, clock, WEP, and fifth-force residuals are bounded |
| `B_mem = 2/27` | locked closure | parent-derived amplitude or permanent closure | rank/dimension are not inserted after the fact |
| `epsilon_H = 1` | closure/conditional target | Ward/Hamiltonian normalization theorem | the unit value is not selected by calibration convenience |
| `H_star = H0` | identity route but not parent selection | boundary/observer selection theorem | the scale is selected dynamically rather than fitted |
| FLRW memory projection | partial compatibility | derived projection law | global memory and local silence share one parent mechanism |
| perturbation/CMB owner | open | Boltzmann-level interface | compressed-distance success is connected to perturbation consistency |

This is why "derive as much as possible" is now operational.

Each closure has to either become:

```text
theorem,
bounded residual,
or honestly labelled closure.
```

## 7. No-Cheat Rules

| Rule | Meaning |
|---|---|
| do not assume GR limit | local Einstein equations must emerge from the parent action |
| do not drop projector stress | projector/boundary stress must be zero, boundary-only, or retained in a conserved ledger |
| do not use PPN runner as proof | source-locked local bounds are guardrails after equations exist |
| do not promote closure constants | `B_mem`, `epsilon_H`, `H_star/H0`, `u3`, dimension 27, and rank 2 remain closure/conditional until derived |
| do not let cosmology bypass GR | late-time fits can keep a branch alive but cannot substitute for local GR reduction |
| do not demand knockout only | empirical ties or slight wins matter if MTS pays the theory bill with a coherent derivation |

That last row is important.

MTS does not need to win every empirical score by a mile to be interesting.

If it stays competitive while replacing patchwork assumptions with a field-theory derivation, that is a legitimate route to victory.

But the derivation bill has to be paid.

## 8. Next Derivation Queue

| Priority | Target | Deliverable | Pass condition |
|---:|---|---|---|
| 1 | parent Ward identity with projector variation | `356-parent-action-ward-identity-and-projector-variation.md` | all metric, projector, domain, and boundary variations appear in the conservation identity |
| 2 | local no-hair/silence theorem | prove or bound `E_MTS_munu -> 0` in local exterior | auxiliary fields are pure gauge, boundary-only, or source-locked below local bounds |
| 3 | EH exterior operator derivation | metric-only local action and weak-field operator map | surviving operator is EH plus `Lambda` with no extra local propagating modes |
| 4 | source-locked local PPN runner | runner using checkpoint 354 source-locked scales | computed residual vector is below locked targets or explicitly fails |
| 5 | closure-to-theorem conversion | rank/dim/amplitude/calibration derivation attempts | at least one closure is derived without post-hoc insertion |

This order matters.

The local-bound runner is not cancelled.

It is placed after the parent Ward/no-hair machinery so that the code tests actual equations rather than a hand-selected silence ansatz.

## 9. What The Next Target Must Prove

Checkpoint 356 should write the parent variation in the form:

```text
delta S_parent
  = delta_g S
  + delta_X S
  + delta_P S
  + delta_boundary S
  + delta_matter S.
```

Under a diffeomorphism generated by `xi^mu`, it must derive the identity:

```text
nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu)
  + F_projector^nu
  + F_boundary^nu
  + F_domain^nu
  = 0.
```

Then it must show one of three things:

```text
F_projector^nu + F_boundary^nu + F_domain^nu = 0
```

or:

```text
those terms are pure boundary charges with no local bulk PPN support
```

or:

```text
they remain as physical residuals and must be carried into the PPN vector.
```

What is forbidden:

```text
erase the terms because GR needs them gone.
```

## 10. Decision

Decision:

```text
GR_connection_and_derivation_priority_reset_no_local_GR_promotion
```

Meaning:

```text
The project priority is now explicitly GR-first and derivation-first.
Checkpoint 354's source-locked local bound runner remains useful,
but the next proof step is the parent Ward identity and projector variation.
```

No promotion:

```text
no local GR pass,
no official PPN pass,
no parent amplitude derivation,
no public unified-field claim.
```

## 11. Bottom Line

The way forward is not to hammer every dataset until MTS wins by knockout.

The way forward is:

```text
stay empirically competitive,
derive the local GR limit,
turn closures into theorems where possible,
and label the remaining closures honestly.
```

That is the correct standard for a serious field-theoretic framework.

Next target:

```text
356 - Parent Action Ward Identity And Projector Variation
```
