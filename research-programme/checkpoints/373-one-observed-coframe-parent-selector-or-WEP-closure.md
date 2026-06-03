# 373 - One Observed Coframe Parent Selector Or WEP Closure

Private WEP/local-GR selector checkpoint. This is not a public WEP, clock, PPN, Einstein-Hilbert, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 372 improved the common-mode local branch:

```text
if local trivial class / boundary-state silence holds,
then grad(phi_C)=0.
```

But checkpoint 371 kept the sharper WEP problem alive:

```text
does the parent theory force all species to see the same class function F(C_D),
or can species see F_A(C_D)?
```

This checkpoint tests the next selector target:

```text
can one observed coframe be parent-derived,
or must it be written honestly as a WEP closure axiom?
```

Answer:

```text
one observed coframe / common F(C_D) is not parent-derived by the current branch.
```

So:

```text
direct WEP/clock vertices are conditionally zero if one coframe is assumed,
but eta_WEP remains active because the coframe/common-F selector is still closure.
```

No glory pass.

But also no hidden cheat.

## 2. Machine Artifact

Script:

```text
scripts/one_observed_coframe_parent_selector_or_WEP_closure.py
```

Run:

```text
runs/20260601-233000-one-observed-coframe-parent-selector-or-WEP-closure
```

Outputs:

```text
results/source_register.csv
results/selector_candidates.csv
results/no_go_steps.csv
results/parent_action_contract.csv
results/WEP_closure_axioms.csv
results/eta_residual_vector.csv
results/promotion_rules.csv
results/failure_modes.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
one_observed_coframe_common_F_not_parent_derived_WEP_closure_axiom_required_eta_active
```

Claim ceiling:

```text
WEP_closure_axiom_and_selector_audit_only_no_WEP_clock_PPN_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. What Is Already Won

The clean conditional matter action remains:

```text
S_matter = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A].
```

At fixed observed coframe:

```text
delta S_matter / delta Z_I = 0
```

for non-geometric MTS variables:

```text
Z_I in {X, J_rel, V_def, P_D, Cperp, species charges, ...}.
```

That means:

```text
if all sectors use one ehat,
direct WEP/clock/composition vertices are absent by action structure.
```

This is a real conditional theorem shape.

It is stronger than “make the WEP violation small”.

It says:

```text
the direct vertex is not in the action.
```

## 4. The No-Go Core

Start from the most general branch still allowed by representative invariance:

```text
S_m = sum_A S_A[Psi_A, exp(F_A(C_D)) g, constants_A(C_D)].
```

Lifted-`C` representative invariance removes:

```text
B_perp,
b_2,
scalar Cperp,
local j_3 representative data.
```

But:

```text
delta_B F_A(C_D) = 0
```

for every species `A`, because `C_D` is already a class observable.

Therefore representative invariance does not imply:

```text
F_A(C_D) = F_B(C_D)
```

for all species.

This is the current WEP no-go:

```text
representative invariance kills representative vertices,
not species-specific class response.
```

## 5. Selector Candidate Audit

| Candidate | Result | Why |
|---|---|---|
| diffeomorphism invariance | insufficient | covariance permits species metrics or species functions |
| representative invariance | progress but not WEP | `F_A(C_D)` is representative-invariant |
| local `phi_C` silence | orthogonal | helps common-mode clock/gamma pressure, not species universality |
| minimal metric coupling | safe if postulated | exact closure but not parent-derived |
| internal species symmetry | future theorem target | no such parent symmetry has been supplied here |
| naturalness | pressure against overclaim | allowed species couplings need symmetry-forbidding |

So the honest position is:

```text
one observed coframe is currently a closure axiom,
not a derived parent selector.
```

## 6. Exact Contract A Future Parent Action Must Satisfy

A future parent action must do all of this, not just gesture at it:

| Contract item | Required statement | Mathematical form | Current status |
|---|---|---|---|
| unique observed coframe | one coframe for all matter observables | `ehat_A^a_mu = ehat^a_mu` for every `A` | not parent-derived |
| no direct non-geometric arguments | no direct MTS matter force at fixed coframe | `delta S_matter / delta Z_I | ehat = 0` | conditional theorem if assumed |
| no species class functions | species labels cannot enter class response | `F_A(C_D)=F(C_D)` | closure axiom required |
| representative quotient only | matter sees class observables, not representative data | `S_matter=S_matter[Psi,ehat(C_D,g)]` | conditional lifted-`C` route |
| matter Ward identity | ordinary matter conserved on observed geometry | `nabla_hat_mu T_hat^mu_nu=0` | conditional if single-coframe action holds |
| selector stress ownership | selector stress is in the Ward ledger | `nabla_mu(T_matter+T_MTS+T_selector)^mu_nu=0` | open |

This is the exact deal.

If the parent theory can supply this, the WEP channel becomes genuinely structural.

If not, this is closure.

## 7. WEP Closure Axioms

For the branch to remain usable without pretending to have solved WEP, write the closure explicitly:

| Axiom | Statement | Why needed | Status |
|---|---|---|---|
| `W1_one_observed_coframe` | all matter, photons, clocks, rulers, and standards couple to one `ehat` | kills direct metric/composition split | explicit closure |
| `W2_common_class_function` | no species-dependent `F_A(C_D)` | prevents class-response WEP differences | explicit closure |
| `W3_constant_independence` | matter/EM/clock constants do not directly depend on `C_D` | prevents clock/composition leakage | explicit closure |
| `W4_representative_invariance` | representative data are unobservable to matter | prevents direct representative vertices | conditional theorem target |
| `W5_local_common_mode_silence_or_bound` | common-mode `phi_C` is theorem-zero or source-bounded | protects clock/gamma/fifth-force rows | conditional or budget-only |

This is not a retreat.

It is the difference between a clean field-theory route and a handwave wearing a lab coat.

## 8. Residual eta Vector

The active WEP residual is:

```text
eta_WEP ~ c_AB Delta F_AB + c_m Delta m_A(C_D) + c_alpha Delta alpha_A(C_D) + c_rep eps_rep.
```

with:

```text
Delta F_AB = F_A(C_D) - F_B(C_D).
```

Current controls:

| Term | Current control | Runner policy |
|---|---|---|
| species class metric split | not parent-derived zero | `eta_WEP` remains active |
| species mass/constant response | forbidden only by closure axiom | WEP and clock rows remain active |
| representative vertex leakage | conditionally forbidden by lifted-`C` invariance | conditional zero if parent-owned |
| common-mode gradient | conditional local zero theorem or fallback bounds | clock/gamma/fifth-force rows remain conditional or budgeted |

So:

```text
eta_WEP is not switched off.
```

It is moved into a cleaner ledger:

```text
the only way to switch it off is parent-selected single coframe/common F,
or an explicit measured/source-locked bound.
```

## 9. Promotion Rules

| Promotion | Current result | Allowed claim |
|---|---|---|
| direct WEP vertex absent | conditional only | yes, if one-coframe action is assumed |
| one observed coframe parent-derived | fail | not allowed |
| WEP pass | fail | not allowed |
| clock/PPN pass | fail | not allowed |
| local GR pass | fail | not allowed |

This checkpoint therefore improves the project by refusing to blur two different statements:

```text
one coframe would solve the direct WEP vertex problem
```

and:

```text
MTS has derived one coframe.
```

Only the first is currently true.

## 10. Decision

Decision:

```text
one_observed_coframe_common_F_not_parent_derived_WEP_closure_axiom_required_eta_active
```

Meaning:

```text
the branch has an exact conditional WEP kill switch,
but the selector for one observed coframe/common F(C_D) is not derived.
```

Therefore:

```text
one observed coframe remains an explicit WEP closure axiom,
eta_WEP remains active,
and no WEP/clock/PPN/EH/local-GR pass is claimed.
```

This is slightly grim but useful-grim.

It prevents us from selling ourselves a fake local-GR victory.

It also leaves a clear future theorem target:

```text
find a parent species symmetry or variational selector that forces ehat_A=ehat.
```

## 11. Next Target

Next:

```text
374 - Fifth-Force Preferred-Frame Source-Lock Manifest
```

Aim:

```text
source-lock the quarantined fifth-force, preferred-frame, xi, and residual coframe/vector leakage rows before scoring them.
```

Pass condition:

```text
all local residual rows are either theorem-zero,
ready budget rows,
or explicitly quarantined with no score.
```

Why this next:

```text
after WEP is honestly closure-labelled,
the remaining local branch needs a source-locked residual manifest
before any more PPN/local-GR promotion attempts.
```
