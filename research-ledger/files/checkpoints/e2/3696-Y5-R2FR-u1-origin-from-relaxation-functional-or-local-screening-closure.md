# 3696 - u1 origin from relaxation functional or local screening closure

Private checkpoint. No GitHub action. No local-GR/Newton/R10/PPN/EM claim.

## Status
- `SCALAR_RLOCK_DOES_NOT_DERIVE_U1_UNDER_EVENNESS_DIRECT_LEAKAGE_PENALTY_REQUIRED`
- The R(m;X_B) lock still helps the trace branch by giving F1=0, but under scalar-even leakage variables it contributes only quartic z stiffness and no quadratic horizontal mass gap. A separate parent-derived leakage penalty U_Z=u_1 s_L, or a risky linear-memory route, is required for local screening.

## Main Result
- The scalar relaxation lock `R(m;X_B)` still matters: it can lock `F1=0` and give `F2=a_F lambda_R`.
- But under the same scalar-evenness route used for local safety, `m(z)-m_L=O(s_L)` with `s_L=G_AB z^A z^B`.
- Then `R(m(z))-R_L = 0.5 lambda_R O(s_L^2)`, which is quartic in `z`, so it gives `u_1^R=0`.
- Therefore scalar R-lock alone does **not** derive the quadratic horizontal mass gap.

## Route Split
- Safe/even route: protects local trace/source behavior but does not generate `u_1`.
- Linear-memory route: can generate `M_AB=a_R lambda_R b_A b_B`, but threatens parity and only gaps the directions spanned by `b_A`.
- Direct penalty route: `U_Z=u_1 s_L+O(s_L^2)` gives `M_AB=2u_1G_AB`; this is the clean target, but must be parent-derived.

## Direct Penalty Contract
- Needed term: `S_leak = -int sqrt(-g) u_1(X_B,rho,theta,J_phys) G_AB z^A z^B + O(z^4)`.
- Required gates: parity, positive `G_H`, positive local `u_1`, bounded corrections, environment dependence, and ordinary-sector silence.

## u1 Origin Rows
- `UOR3696_0_Rlock_memory`: scalar memory relaxation lock | `SOURCE_CONFIRMED_CONDITIONAL` | R(m;X_B)=R_L+0.5 lambda_R(m-m_L)^2+O((m-m_L)^3), F=F_L+a_F[R-R_L]
- `UOR3696_1_chain_Hessian`: R-lock contribution to z-Hessian | `DERIVED_CHAIN_RULE` | partial_A partial_B U_R|_0 = a_R[lambda_R m_A m_B + R_m m_AB]|_0 = a_R lambda_R m_A m_B
- `UOR3696_2_even_m_no_gap`: even scalar memory map | `NO_GO_FOR_U1_FROM_EVEN_SCALAR_RLOCK` | if m(z)=m_L+c_1 s_L+O(s_L^2), then m_A=0 and R(m(z))-R_L=0.5 lambda_R c_1^2 s_L^2+O(s_L^3)
- `UOR3696_3_linear_m_route`: linear memory map route | `POSSIBLE_BUT_DANGEROUS_RANK_AND_PARITY_ROUTE` | if m(z)=m_L+b_A z^A+O(z^2), then M_AB^R=a_R lambda_R b_A b_B
- `UOR3696_4_direct_leakage_penalty`: direct horizontal leakage penalty | `BEST_ROUTE_NOT_PARENT_DERIVED` | U_Z(z;X_B)=u_1(X_B,local_state)s_L+O(s_L^2)
- `UOR3696_5_verdict`: u1 origin verdict | `U1_NOT_DERIVED_DIRECT_LEAKAGE_PENALTY_REQUIRED` | current R(m;X_B) lock does not by itself derive u_1>0 for the horizontal mass gap under the same evenness assumptions that protect local PPN

## Direct Penalty Contract Rows
- `DPC3696_0_action_term`: parent leakage penalty | `CONTRACT_REQUIRED` | S_leak = -int sqrt(-g) u_1(X_B,rho,theta,J_phys) G_AB z^A z^B + O(z^4)
- `DPC3696_1_symmetry`: leakage-frame parity | `CONTRACT_REQUIRED` | S_leak[z]=S_leak[-z]
- `DPC3696_2_positivity`: positive local curvature | `CONTRACT_REQUIRED` | u_1(local)>0 and G_H>0
- `DPC3696_3_environment`: local/cosmic separation | `CONTRACT_REQUIRED` | u_1(local) large enough for local tests while u_1(gal/cos) does not erase intended long-range response
- `DPC3696_4_source_silence`: ordinary-sector safety | `CONTRACT_REQUIRED` | partial_z S_matter=0 and no hidden z-dependent masses/charges except quotient-owned terms

## Route Scores
- `RS3696_0_scalar_Rlock`: scalar R-lock only | `REJECT_AS_SOLE_MASS_GAP_ORIGIN` | u_1^R=0 if m-m_L=O(s_L)
- `RS3696_1_linear_memory`: linear memory map | `HIGH_SCRUTINY_ROUTE` | M_AB=a_R lambda_R b_A b_B
- `RS3696_2_direct_penalty`: direct leakage penalty | `BEST_NEXT_ROUTE` | M_AB=2u_1G_AB
- `RS3696_3_closure`: closure/Yukawa branch | `FALLBACK_NONCLAIM` | u_1 declared or fitted, lambda_H=1/sqrt(2u_1-corrections)

## Decisions
- `DEC3696_0`: `NO_GO_ADOPTED` - The same evenness that protects local PPN makes scalar R(m) quartic in z, so it cannot alone produce u_1.
- `DEC3696_1`: `NEXT_ROUTE_SELECTED` - The next derivation should seek a parent/coarse-grained entropy or Onsager penalty proportional to s_L.
- `DEC3696_2`: `CLAIM_BLOCKED` - u_1 remains unsigned; local screening remains conditional or closure-only.

## Claim Gates
- `CG3696_0_u1`: `BLOCKED` - u_1 not derived from scalar R-lock under evenness
- `CG3696_1_penalty`: `BLOCKED` - direct leakage penalty not parent-signed
- `CG3696_2_source_silence`: `BLOCKED` - ordinary matter/EM/source silence under z not proved
- `CG3696_3_environment`: `BLOCKED` - local/cosmic/galaxy u_1 separation not derived
- `CG3696_4_local_GR`: `BLOCKED` - local GR screening still awaits sourced u_1 and arena projections
- `CG3696_5_public`: `BLOCKED` - private checkpoint only; no public/GitHub claim

## Source Register
- `handoff_3695`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3695_NEXT_TARGET.csv`
- `hessian_3695`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3695_HESSIAN_EXTRACTION_ROWS.csv`
- `mu_3695`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3695_SYMBOLIC_MUH_ROWS.csv`
- `equations_register`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\05-equation-register.md`
- `variable_audit_Rlock`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\04-variable-audit.csv`
- `scalar_evenness_126`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\126-scalar-evenness-origin.md`
- `signed_map_127`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\127-signed-leakage-coordinate-map.md`
- `leakage_invariant_125`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\125-local-leakage-vector-invariant.md`

## Next Target
- `3697-Y5-R2FR-direct-leakage-penalty-from-coarse-graining-Onsager-or-closure.md`
- Objective: try to derive the direct quadratic leakage penalty U_Z=u_1 s_L from coarse-graining entropy, Onsager dissipation, or parent variational stability; if not, mark u_1 as closure-only and pass it to the nonclaim Yukawa runner
