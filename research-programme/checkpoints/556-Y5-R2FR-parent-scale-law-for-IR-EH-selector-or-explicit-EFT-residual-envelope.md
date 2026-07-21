# 4540 - parent scale law for IR EH selector or explicit EFT residual envelope

Generated: `2026-07-06T10:13:15.613495+00:00`  
Marker: `PPC4161_PARENT_SCALE_LAW_FOR_IR_EH_SELECTOR_OR_EXPLICIT_EFT_RESIDUAL_ENVELOPE_4540`  
Decision: `IR_EH_SELECTOR_THEOREM_CONDITIONAL_PARENT_SCALE_LAW_MISSING_EXPLICIT_EFT_RESIDUAL_ENVELOPE_ACTIVATED`  
Claim: `L-382` remains private, conditional and nonclaim.

## What Moved

4539 froze `PPC4161-GP-HQNP` as an effective local-GR branch because the parent action has not yet signed the EH/IR selector. 4540 attacks that root.

The clean theorem is:

```text
local covariant parent action
+ parent scale/gap hierarchy
+ no extra light local modes
+ same coframe and q-natural descent
=> EC/Palatini is the unique unsuppressed parity-even linear-curvature local bulk term
=> EH local metric block after torsion/nonmetricity silence.
```

That theorem is useful but conditional. Current MTS evidence does not yet derive the needed scale/gap law. Therefore the honest branch is not “EH is fully derived”; it is:

```text
E_IR_local(A)
 <= |J_A^D c_D|
  + |J_A^k delta_kappa|
  + |J_A^G c_Gamma|
  + |J_A^T c_T|
  + |J_A^R c_R2/M_R^2|
  + |J_A^B c_bdy|.
```

This is a move forward: every non-EH local invariant now has a named coefficient, arena projection requirement and zero-or-bound route. The priority next attack is the root triple `c_D`, `delta_kappa`, `c_Gamma`; R10 finite-range scoring waits until projection coefficients exist.

## IR Normal Form Theorem

| theorem_id | claim | condition | consequence | current_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NFT4540_0_derivative_expansion | A parent-owned local covariant derivative expansion with a mass gap selects the lowest-derivative bulk invariants first. | There exists Lambda_* such that L_test Lambda_* >> 1 and all operators with more than one curvature/two derivatives are suppressed by powers of (L_test Lambda_*)^-1. | curvature-square and higher-derivative terms become EFT residuals rather than principal local gravity | conditional_parent_scale_law_missing | False | False |
| NFT4540_1_EC_Palatini_selection | Under locality, Lorentz/diffeomorphism covariance, parity-even classical sector, one observed coframe, and one-curvature IR order, the unsuppressed bulk gravity term is EC/Palatini plus vacuum term. | A_MF variables e,omega are admitted; parity-odd terms are topological/bounded; no second metric/disformal owner; no extra light torsion/scalar/vector mode. | epsilon_ABCD e^A wedge e^B wedge R^CD[omega] gives EH after torsion/nonmetricity silence | conditional_true_selector_assumptions_not_parent_derived | False | False |
| NFT4540_2_current_failure | The current corpus does not derive the parent scale/gap law needed to promote the IR selector. | Need parent-owned Lambda_*, no-extra-light-mode theorem, same-coframe functor and local memory screening. | EH remains effective/local branch principal block, not a first-principles parent theorem | proved_from_current_audit | False | False |


## Parent Scale-Law Audit

| scale_law_id | law_needed | would_zero_or_suppress | current_evidence | verdict | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SLA4540_0_IR_gap | parent mass/length hierarchy Lambda_* with L_local Lambda_* >> 1 | c_R2, higher derivative curvature tails | 4184/4185 require parent scale or R10/orbital bound | missing_parent_scale | derive Lambda_* from MTS primitives or retain c_R2/M_R envelope | False | False |
| SLA4540_1_no_light_modes | no unscreened local torsion/scalar/vector/disformal modes | c_T, c_D, preferred-frame and clock/WEP tails | 4184 selector assumption; 4185 maps c_T/c_D to local arenas | missing_parent_mode_gap | prove same-coframe and torsion algebraic/heavy laws or bound them | False | False |
| SLA4540_2_same_coframe | q-owned single observed coframe functor | c_D | private selector exists; global parent adoption open | private_not_global | 4541 triple-zero route begins with c_D | False | False |
| SLA4540_3_kappa_source | topological kappa lock plus Hilbert source-measure descent | delta_kappa | private branch closed; numeric G calibrated; global adoption open | private_not_global | 4541 triple-zero route carries delta_kappa | False | False |
| SLA4540_4_memory_silence | local support projector/screens Gamma_mem from compact local collar | c_Gamma | 4185 central MTS-specific open debt | open_core_MTS_risk | 4541 triple-zero route carries c_Gamma | False | False |
| SLA4540_5_boundary_route | boundary/topological pieces exact, fixed or Hamiltonian-routed | c_bdy | private no-flux exists; global adoption open | open_global_boundary | retain boundary envelope until sector interface theorem | False | False |


## EFT Residual Envelope

| envelope_id | quantity | envelope | meaning | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EFT4540_0_master | E_IR_local(A) | |R_A| <= |J_A^D c_D| + |J_A^k delta_kappa| + |J_A^G c_Gamma| + |J_A^T c_T| + |J_A^R c_R2/M_R^2| + |J_A^B c_bdy| | until the scale law is derived, each local arena A receives explicit coefficient projections instead of a hidden closure assumption | ACTIVE_NONCLAIM_ENVELOPE | False | False |
| EFT4540_1_cD | c_D | same-coframe failure; projects first to WEP, clocks, EM propagation and Poynting/Hilbert stress | zero if q-owned single coframe is parent-signed; otherwise needs source-backed bound | PRIORITY_1_ZERO_OR_BOUND | False | False |
| EFT4540_2_deltaKappa | delta_kappa | coupling/source-measure drift; projects to Gdot/G, orbital GM consistency, clock/local-G and WEP | zero if topological kappa plus Hilbert source lock is parent-signed; otherwise measured-G/LLR/orbital envelope | PRIORITY_1_ZERO_OR_BOUND | False | False |
| EFT4540_3_cGamma | c_Gamma | MTS-specific local memory hair; projects to PPN, clocks, R10 and local-G variation | zero/suppressed only with a parent local memory support law | PRIORITY_1_ZERO_OR_BOUND | False | False |
| EFT4540_4_cT | c_T | torsion-square/torsion mode residual; projects to preferred-frame, spin/contact, R10 | zero/heavy if EC torsion algebraic silence or torsion mass gap is parent-signed | SECONDARY_ZERO_OR_BOUND | False | False |
| EFT4540_5_cR2 | c_R2/M_R^2 | curvature-square finite-range tail; projects to R10 Yukawa, orbital precession and cosmology consistency | suppressed by parent IR scale or bounded by R10/orbital data | SECONDARY_ZERO_OR_BOUND | False | False |
| EFT4540_6_cBdy | c_bdy | unrouted boundary/edge charge; projects to source mass leakage, radiation reaction and clock/source drift | zero in bulk only if boundary is exact/fixed/topological/Hamiltonian-routed | SECONDARY_ZERO_OR_BOUND | False | False |


## Arena Projection Requirements

| projection_id | arena | required_projection | current_status | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| APR4540_0_PPN | PPN_vector | J_PPN = d(gamma,beta,alpha_i,xi,zeta_i,Gdot/G)/d(c_D,delta_kappa,c_Gamma,c_T,c_R2,c_bdy) | projection_coefficients_missing | derive zero law first for c_D, delta_kappa, c_Gamma | False | False |
| APR4540_1_WEP_clock_EM | WEP_clock_EM | J_WCE for c_D, delta_kappa and c_Gamma into eta, clock redshift, EM propagation and Poynting ownership | projection_coefficients_missing | same-coframe/source-memory triple-zero or bounds | False | False |
| APR4540_2_R10 | short_range_R10 | J_R10 for c_R2,c_T,c_Gamma into alpha(lambda), with real bound curve | defer_until_projection_and_curve | do not score R10 from placeholders | False | False |
| APR4540_3_orbital | orbital_ephemeris | J_orb for delta_kappa,c_R2,c_bdy,c_Gamma into perihelion, inverse-square and Gdot envelopes | projection_coefficients_missing | analytic envelope before raw ephemeris | False | False |


## Claim Gates

| claim_gate_id | gate | status | meaning | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4540_0_conditional_IR_theorem | IR normal-form theorem | PASS_CONDITIONAL | EH/Palatini follows if parent scale/gap/no-light-mode conditions hold | False | False |
| CG4540_1_parent_scale_law | current parent scale law | FAIL_MISSING_PARENT_DERIVATION | no parent-owned Lambda_* or no-extra-light-mode theorem exists yet | False | False |
| CG4540_2_EFT_envelope | explicit EFT residual envelope | ACTIVE | extra invariants are now kept as named coefficient projections rather than hidden closures | False | False |
| CG4540_3_public_GR_derivation | public GR derivation | BLOCKED_NONCLAIM | effective local branch remains useful but parent EH origin is not proved | False | False |


## Decision

| decision_id | decision | meaning | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC4540_0 | IR_EH_SELECTOR_THEOREM_CONDITIONAL_PARENT_SCALE_LAW_MISSING_EXPLICIT_EFT_RESIDUAL_ENVELOPE_ACTIVATED | 4540 derives the correct IR normal-form fork: with a parent scale/gap law, EH/Palatini is selected; without it, every extra invariant must be carried as an explicit EFT residual envelope. Current evidence chooses the envelope branch. | 4541-Y5-R2FR-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md | False | False |


## Next Target

| next_id | target | objective | derive_first | fallback | avoid | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4540_0 | 4541-Y5-R2FR-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md | try to zero the priority triple c_D, delta_kappa and c_Gamma before scoring finite-range tails | same-coframe functor, kappa/source lock and local memory support projector | if any coefficient remains finite, write projection-bound rows into WEP/clock/PPN/orbital arenas before R10 | jumping to R10 alpha(lambda) before projection coefficients exist | False |


## Status

| timestamp_utc | branch_id | checkpoint_id | result | conditional_IR_EH_selector_theorem_written | parent_scale_law_derived | EFT_residual_envelope_active | public_local_GR_claim_allowed | numeric_G_predicted | priority_coefficients | next_target | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-06T10:13:15.471417+00:00 | MTS_R2FR_Y5_PARENT_SCALE_LAW_IR_EH_SELECTOR_OR_EFT_ENVELOPE_4540 | 4540 | IR_EH_SELECTOR_THEOREM_CONDITIONAL_PARENT_SCALE_LAW_MISSING_EXPLICIT_EFT_RESIDUAL_ENVELOPE_ACTIVATED | True | False | True | False | False | c_D;delta_kappa;c_Gamma | 4541-Y5-R2FR-same-coframe-kappa-memory-triple-zero-under-effective-local-branch-or-projection-bound.md | False | False |


## Source Register

| checkpoint | source_id | label | path | exists | needle | needle_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4540 | SRC4540_00_4539_status | 4539 status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4539_STATUS.csv | True | primary_live_residual | True | 4539 freezes effective local GR and selects E_EH_IR as primary residual | False |
| 4540 | SRC4540_01_4539_handoff | 4539 residual handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4539_RESIDUAL_HANDOFF_MATRIX.csv | True | RH4539_0_EH_IR | True | EH/IR selector is next target | False |
| 4540 | SRC4540_02_4184_status | 4184 IR selector status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_STATUS.csv | True | selector_assumptions_parent_derived | True | IR selector theorem is conditional and not parent-derived | False |
| 4540 | SRC4540_03_4184_axioms | 4184 selector axiom set | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv | True | SEL4184_2_IR_order | True | IR order and no-extra-light-mode assumptions | False |
| 4540 | SRC4540_04_4184_normal | 4184 normal form classification | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION.csv | True | NFC4184_0_EC_Palatini | True | EC/Palatini is selected only if selector clauses hold | False |
| 4540 | SRC4540_05_4184_EFT | 4184 EFT bound ledger | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv | True | RB4184_1_cR2 | True | EFT residual coefficient families after failed selector | False |
| 4540 | SRC4540_06_4185_coefficients | 4185 coefficient arena map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP.csv | True | RC4185_2_cGamma | True | coefficient-to-arena projection map | False |
| 4540 | SRC4540_07_4185_scale_candidates | 4185 parent zero/scale candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4185_PARENT_ZERO_SCALE_LAW_CANDIDATES.csv | True | PSL4185_4_higher_derivative_scale | True | candidate parent zero/scale laws | False |
| 4540 | SRC4540_08_4185_bounds | 4185 bound interface matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4185_BOUND_INTERFACE_MATRIX.csv | True | BI4185_0_PPN | True | arena interfaces for residual coefficient bounds | False |
| 4540 | SRC4540_09_packet | packet 4539 freeze | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\180-PPC4161-private-local-packet-integration.md | True | PPC4161_PACKET_PARENT_ADOPT_GR_PARITY_HQNP_SELECTOR_OR_FREEZE_EFFECTIVE_LOCAL_GR_BRANCH_4539 | True | effective local GR branch freeze is installed | False |


## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4540_00_sources | PASS | all source paths exist and needles found |
| VAL4540_01_normal_form | PASS | conditional EC/Palatini selector and current failure are explicit |
| VAL4540_02_scale_law_audit | PASS | parent scale law remains missing rather than silently assumed |
| VAL4540_03_envelope | PASS | all named EFT residual coefficients are in the active envelope |
| VAL4540_04_projection_requirements | PASS | arena projection requirements recorded as nonclaim |
| VAL4540_05_claim_firewall | PASS | parent scale law fails and all gates remain nonclaim |
| VAL4540_06_csv_parse | PASS | all generated CSV files parse and have rows |
| VAL4540_07_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4540_OVERALL | PASS | 4540 parent scale-law fork and EFT residual envelope |

