# 4003 - Parent Theta/Qtau Current Chain Or Integrability Source Row

- Timestamp: `2026-07-01T19:35:19+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint makes the exact parent-current fork explicit.

The route is real:

`delta L_parent = E_A delta Phi^A + d Theta_total(Phi;delta Phi)`

`J_tau = Theta_total(Phi;L_tau Phi) - i_tau L_parent - mu_tau`

`J_tau = d Q_tau^MTS + C_tau` on the constrained branch.

Then the 4002 Hamiltonian one-form is

`alpha_tau[delta Phi]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref`.

So the proof path is not vague: derive the parent current, prove the retained pieces zero/exact/proper, and only then let `H_tau` become a source charge.

## Non-Smuggled Local GR Route

The clean descent lemma is:

`L_parent = q^*L_red + L_vert_alg + dB`

with projectable `tau`, explicit `Dq`, vertical directions killed by quotient/symplectic silence, fixed boundary/reference `B`, and matter/source descent through `q`.

If those clauses hold, then

`Q_tau^parent = q^*Q_tau^red + i_tau B + proper corner terms`,

and the EH/GR exterior charge can be inherited rather than borrowed.

That is the bridge we want: GR comes out as the reduced current branch, not as a pasted-on baseline.

## What Blocks The Claim

`Q_tau^EH` exists as a reference comparator, but `Q_tau^MTS` is not promoted while these pieces remain unowned:

- `Q_tau^X`, `Theta_X`, `C_tau^X` for the extra motion/time/memory/range sector.
- projector/source-current variation, especially `(delta Pi_M)J_H`.
- boundary/reference/corner improvements and fixed `H_ref`.
- matter, EM, coupling, and Poynting placement in the same current.
- quotient/current projectability through `q` and `Dq`.
- parent presymplectic null equivalence `ker(Dq)=ker(Omega_parent)`.

## Bound If Closure Fails

`Delta_current_chain_4003=|C_tau_bulk|+|I_X|+|I_projector|+|I_boundary|+|I_matter_EM|+|I_Dq|+|Theta_leak|+|Qtau_leak|+|Omega_null_gap|+|sector_gap|+|EH_borrowing_guard|`.

This is the useful part: if a proof clause does not close, it becomes a named component to derive, bound, or source. No more fog bank.

## Evaluator Results

- `CASE4003_0_full_parent_current_zero`: `CONDITIONAL_ZERO_THEOREM_AVAILABLE`, zero=True, delta=`0.0`, claim=False, next=`then feed 4002 H_tau/H_ref and local-GR gates`
- `CASE4003_1_EH_only_reference`: `EH_BORROWING_REFUSED`, zero=False, delta=`GUARD_ACTIVE_PLUS_SYMBOLIC_COMPONENTS`, claim=False, next=`do not promote EH baseline; derive or retain non-EH components`
- `CASE4003_2_X_extra_missing`: `I_X_OPEN`, zero=False, delta=`SYMBOLIC_I_X_BOUND_REQUIRED`, claim=False, next=`derive Theta_X/Q_tau_X or prove algebraic auxiliary zero`
- `CASE4003_3_projector_boundary_missing`: `PROJECTOR_BOUNDARY_OPEN`, zero=False, delta=`SYMBOLIC_PROJECTOR_BOUNDARY_BOUND_REQUIRED`, claim=False, next=`connect 4001 projector and fixed boundary/reference selector`
- `CASE4003_4_Dq_matter_marker_missing`: `MATTER_DQ_COUPLING_OPEN`, zero=False, delta=`SYMBOLIC_MATTER_DQ_BOUND_REQUIRED`, claim=False, next=`prove q/Dq source descent or write coupling/Poynting residual row`
- `CASE4003_5_numeric_nonclaim_component_row`: `NONCLAIM_SOURCE_ROW_ACCEPTED`, zero=False, delta=`PARTIAL_NUMERIC_COMPONENTS_TOTAL_CHAIN_OPEN`, claim=False, next=`keep row nonclaim and continue component extraction`
- `CASE4003_6_missing_parent_rows`: `BLOCKED_MISSING_PARENT_ROWS`, zero=False, delta=`MISSING`, claim=False, next=`repair source/schema rows before scoring`

## Verdict

We moved from “Theta/Qtau missing” to an exact contract and a ranked attack vector. The best next leap is `I_X`: derive whether the extra MTS sector is algebraic/auxiliary so `Theta_X=Q_tau_X=0/proper`, or expose the first real extra-sector Hamiltonian current.

## Next Target

- `4004-Y5-R2FR-IX-extra-sector-current-extraction-or-source-backed-curl-row.md`
- `scripts/Y5_R2FR_4004_IX_extra_sector_current_extraction_or_source_backed_curl_row.py`

## Source Count

- source needles found: `16/16`
