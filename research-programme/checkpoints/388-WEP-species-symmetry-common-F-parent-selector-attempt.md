# 388 - WEP Species Symmetry Common-F Parent Selector Attempt

Private WEP/local-GR selector checkpoint. This is not a public WEP, clock, PPN, preferred-frame, fifth-force, Einstein-Hilbert, source-normalization, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 387 forced the local fork:

```text
identity coframe
```

or:

```text
class-metric pullback retained as closure/counterstress.
```

The hardest always-relevant local row is still:

```text
eta_WEP.
```

So this checkpoint tries the exact missing theorem:

```text
can the parent theory force F_A(C_D)=F(C_D)?
```

The result is:

```text
yes, conditionally,
if the parent matter sector is a species-blind geometry functor.
```

But:

```text
that functor is not yet derived from the MTS parent action.
```

So:

```text
common-F theorem contract written,
eta_WEP still active,
no WEP/local-GR promotion.
```

This is useful because it finds the right symmetry:

```text
not full species permutation,
but species-blind geometry.
```

## 2. Machine Artifact

Script:

```text
scripts/WEP_species_symmetry_common_F_parent_selector_attempt.py
```

Run:

```text
runs/20260602-020500-WEP-species-symmetry-common-F-parent-selector-attempt
```

Outputs:

```text
results/source_register.csv
results/theorem_attempts.csv
results/species_blind_functor_contract.csv
results/no_go_results.csv
results/eta_transition.csv
results/branch_decision.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
common_F_species_blind_geometry_theorem_conditional_parent_selector_not_derived_eta_WEP_still_active
```

Claim ceiling:

```text
common_F_selector_attempt_only_no_WEP_clock_PPN_fifth_force_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. The Right Symmetry

The wrong symmetry is:

```text
all species are identical.
```

That is too strong.

Electrons, nuclei, photons, clocks, and matter fields are not the same species.

They can differ by:

```text
spin,
mass,
charge,
internal representation,
and ordinary constant parameters.
```

The needed symmetry is narrower:

```text
all species use the same geometry map.
```

Species labels may live in:

```text
theta_A = {mass_A, charge_A, spin_A, representation_A, ...}
```

but not in:

```text
ehat_A(C_D),
F_A(C_D),
m_A(C_D),
alpha_A(C_D),
or q_A(C_D).
```

That is the species-blind geometry functor.

## 4. Conditional Common-F Theorem

Assume the parent matter action has the form:

```text
S_matter = sum_A S_A[Psi_A, ehat, omega[ehat], theta_A].
```

where:

```text
theta_A
```

contains internal species data only, and:

```text
theta_A
```

does not contain MTS class functions.

Then there is only one geometry argument:

```text
ehat.
```

If this shared geometry is written in class-metric form:

```text
ehat = exp(F(C_D)) e,
```

then every species has:

```text
F_A(C_D)=F(C_D).
```

So:

```text
Delta F_AB = 0.
```

This conditionally kills the direct species class-metric split.

But it does not yet derive:

```text
why the parent action must be species-blind in this exact way.
```

Therefore this is:

```text
conditional theorem,
not WEP pass.
```

## 5. Theorem Attempts

| Attempt | Verdict | Reason |
|---|---|---|
| diffeomorphism/local Lorentz only | fail | covariance permits `F_A(C_D)` |
| representative invariance only | fail for common-F | `C_D` is representative-invariant |
| full species permutation | too strong | would also overconstrain masses/charges |
| species-blind geometry functor | conditional theorem | one geometry argument forces common `F` |
| identity coframe selection | strongest conditional route | gives `F_A=0` and removes pullback |
| naturalness/smallness | fail | small is not theorem-zero |

The key no-go remains:

```text
S_A[psi_A, exp(F_A(C_D))g]
```

is perfectly covariant and representative-invariant.

So spacetime symmetry and lifted-`C` representative symmetry are not enough.

We need a parent matter-sector rule:

```text
species labels are internal-only,
not class-sector spurions.
```

## 6. Species-Blind Functor Contract

The exact contract is:

| Contract item | Mathematical statement | Status |
|---|---|---|
| single geometry argument | `S_matter=sum_A S_A[Psi_A, ehat, omega[ehat], theta_A]` | conditional premise |
| species labels internal-only | `theta_A` has constants/representations but no `theta_A(C_D)` | not parent-derived |
| no species class spurion | no `sigma_A C_D O_A` or `lambda_A f(C_D)O_A` | required selection rule |
| common geometry map | `ehat=ehat(e,C_D,...)` independent of `A` | conditional result |
| identity preference | local branch sets `ehat=e` or proves class pullback silent/owned | next theorem target |

This contract is now crisp.

If a future parent action satisfies it, then:

```text
F_A=F
```

is not an extra patch.

It follows because species never had separate geometry maps.

## 7. What Still Fails

The common-F theorem does not solve everything.

Even if:

```text
F_A=F
```

the common pullback remains:

```text
Pi_C^matter ~ T_hat partial_C F.
```

So common-F can remove:

```text
composition/WEP species split.
```

But it does not remove:

```text
clock,
gamma,
fifth-force,
or Gdot/G
```

common-mode pressure.

Those still need:

```text
identity coframe,
F'(C_D)=0 locally,
pure gauge,
source-normalized constant mode,
or Ward-owned no-hair counterstress.
```

So the common-F result is important, but not sufficient for local GR.

## 8. No-Go Results

| No-go | Consequence |
|---|---|
| covariance does not imply WEP | `F_A(C_D)` can be covariant for each `A` |
| representative invariance does not remove species spurions | lifted-`C` quotient does not close `eta_WEP` |
| full species symmetry is not the right symmetry | species can differ internally without different geometry |
| common-F does not solve common mode | `T partial_C F` still sources local rows |
| small species functions are not zero | `eta_WEP` needs theorem-zero or source-locked coefficient |

This is the cleanest statement of the situation:

```text
the symmetry we need is geometric universality,
not identical matter species.
```

## 9. Eta Transition

If the species-blind geometry functor is parent-derived, the eta row changes:

| Term | If parent-derived | Current status |
|---|---|---|
| `Delta F_AB` | derived-zero | conditional-zero only |
| `Delta m_A(C_D)` | derived-zero if masses are constants independent of `C_D` | conditional-zero only |
| `Delta alpha_A(C_D)` | derived-zero if EM/clock constants are class-independent | conditional-zero only |
| `q_A` class/bulk/source charge | derived-zero if no species class spurion exists | conditional-zero only |
| representative leakage | conditional gauge-zero from lifted-`C` theorem | conditional gauge-zero |

Current source-locked pressure:

```text
eta_WEP <= 2.8e-15.
```

So without the parent theorem:

```text
eta_WEP remains active.
```

No row moves to:

```text
derived_zero.
```

## 10. Branch Decision

| Branch | Common-F status | WEP status |
|---|---|---|
| identity metric coframe | `F_A=0` if parent-selected | best local-GR route, still not derived |
| universal class metric | common-F conditional theorem possible | species split killed, common-mode pullback remains |
| species class metric | not allowed for local-GR unless common-F theorem supplied | `eta_WEP` active |
| counterstress class pullback | owns rather than kills pullback | modified-gravity fallback with budgets |

This sharpens checkpoint 387:

```text
common-F is not impossible.
```

But it needs a precise parent selector.

Without that selector, the clean local-GR route remains:

```text
identity coframe.
```

## 11. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| theorem attempts written | pass | six common-F routes audited |
| species-blind geometry functor theorem | conditional pass | common `F` follows if species labels are internal-only |
| species-blind functor parent-derived | fail | no parent action principle yet forbids species class spurions |
| full species symmetry rejected | pass | required symmetry is geometry universality, not identical species |
| `eta_WEP` resolved | fail | common-F theorem is conditional |
| common-mode pullback resolved | fail | common `F` leaves `T partial_C F` unless identity/source-normalization/no-hair is derived |
| WEP/PPN/local GR promoted | fail | no row moves to derived-zero |
| claim ceiling enforced | pass | no WEP/clock/PPN/fifth-force/EH/local-GR pass |

## 12. Decision

Decision:

```text
common_F_species_blind_geometry_theorem_conditional_parent_selector_not_derived_eta_WEP_still_active
```

Meaning:

```text
a narrow common-F theorem exists,
but only if species-blind geometry is a parent action principle.
```

That theorem is:

```text
one shared geometry argument + internal-only species labels
  -> ehat_A=ehat
  -> F_A(C_D)=F(C_D).
```

But the current MTS branch has not yet derived the parent principle.

So:

```text
eta_WEP remains active,
common-mode pullback remains active,
and local GR is not promoted.
```

This is progress because the missing theorem is no longer vague.

It is exactly:

```text
derive species-blind geometry,
or choose identity coframe as the local parent principle.
```

## 13. Next Target

Next:

```text
389 - Identity Coframe Parent Selection Principle
```

Aim:

```text
attempt to derive ehat=e locally from the parent action/equivalence-principle contract.
```

Pass condition:

```text
ehat=e becomes a parent theorem,
or remains explicitly labelled local WEP closure.
```

Why this next:

```text
common-F helps WEP species split but does not remove common-mode pullback.
```

The strongest local-GR route is still:

```text
identity coframe locally.
```
