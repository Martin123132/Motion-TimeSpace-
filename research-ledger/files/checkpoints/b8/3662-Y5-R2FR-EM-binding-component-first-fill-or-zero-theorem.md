# 3662 - EM-binding component first fill or zero theorem

**Status:** 3662 refuses the unsigned EM-binding zero theorem, computes source-backed nonclaim Ti/Pt SEMF Coulomb binding fractions, and writes the source-body schemas needed before WEP/R10/gamma can score the shared EM component.

**Claim ceiling:** no EM-binding zero, WEP, R10, gamma, local-GR, PPN, Newtonian, source-calibration, clock/orbital, or EH-dominance pass is claimed.

## Main result

The EM-binding component cannot be zero-claimed yet. It would vanish only if `f_EM=0`, if the parent action forbids EM binding from coupling to `X`, or if the relevant source has no Coulomb binding. Ordinary Ti/Pt nuclei do have Coulomb binding, so the nonzero branch is live.

The first numeric nonclaim fill is now in place:

`B_A^EM ~= E_C/(M_A c^2)`, with `E_C=a_C Z(Z-1)A^(-1/3)` and `a_C=0.711 MeV`.

Ti/Pt are filled as natural-element SEMF proxies, but WEP/R10/gamma still cannot score until the attractor/source composition and `f_EM`, `Z_X`, `lambda_X`, `k_H`, `k_G` inputs are owned.

## EM zero theorem attempt
- `EMZ3662_0_component_definition`: COMPONENT_DEFINITION_DERIVED - `Q_X^EM = B_source_EM*f_EM; B_source_EM=sum_i w_i B_i^EM`
- `EMZ3662_1_Coulomb_binding_formula`: SEMF_FORMULA_READY - `B_A^EM ~= E_C/(M_A c^2); E_C=a_C Z(Z-1)A^(-1/3)`
- `EMZ3662_2_zero_route`: CONDITIONAL_ZERO_THEOREM_PREMISES_UNSIGNED - `f_EM=0 or B_source_EM=0 or parent_no_EM_binding_X_coupling => Q_X^EM=0`
- `EMZ3662_3_countermodel`: NONZERO_EM_BINDING_BRANCH_LIVE - `Z>1 and f_EM!=0 => B_A^EM*f_EM can contribute to Q_X`

## Elemental EM rows
- `EME3662_Ti`: `Ti` B_A_EM=`0.002029005328` - SOURCE_BACKED_NUMERIC_NONCLAIM_NATURAL_ELEMENT_APPROX
- `EME3662_Pt`: `Pt` B_A_EM=`0.004051780873` - SOURCE_BACKED_NUMERIC_NONCLAIM_NATURAL_ELEMENT_APPROX
- `EME3662_TiPt_delta`: `Ti_minus_Pt_proxy` B_A_EM=`-0.002022775545` - DELTA_B_EM_NUMERIC_NONCLAIM_SOURCE_COMPOSITION_STILL_REQUIRED

## Source-body schemas
- `EMS3662_0_source_body_generic`: `source_body_S` - SOURCE_BODY_COMPOSITION_REQUIRED
- `EMS3662_1_Cassini_Sun`: `solar_source_for_gamma` - SOLAR_COMPOSITION_REQUIRED_FOR_GAMMA
- `EMS3662_2_Earth_WEP`: `Earth_source_for_WEP` - EARTH_COMPOSITION_REQUIRED_FOR_WEP
- `EMS3662_3_lab_R10`: `lab_source_for_R10` - LAB_SOURCE_COMPOSITION_REQUIRED_FOR_R10

## Shared component rows
- `ESC3662_0_WEP_TiPt_EM_piece`: `WEP/MICROSCOPE` - TEST_PAIR_NUMERIC_SOURCE_SIDE_MISSING_NONCLAIM
- `ESC3662_1_R10_EM_piece`: `R10/fifth-force` - SYMBOLIC_CURVE_AND_SOURCE_TEST_PRODUCT_MISSING_NONCLAIM
- `ESC3662_2_gamma_EM_piece`: `Cassini/PPN gamma` - GAMMA_SOURCE_SIDE_MISSING_NONCLAIM

## Claim gates
- `CG3662_0_zero_attempt`: PASSED_AUDIT - EM-binding zero theorem attempted
- `CG3662_1_numeric_TiPt`: PASSED_NUMERIC_FILL_NONCLAIM - Ti/Pt EM binding fractions computed
- `CG3662_2_source_schema`: PASSED_SCHEMA_GATE - source-body schemas written
- `CG3662_3_shared_use`: PASSED_MAPPING_GATE - shared WEP/R10/gamma mapping written
- `CG3662_4_no_claim`: ACTIVE_GUARD - no WEP/R10/gamma/local-GR pass claimed
- `CG3662_5_next`: SOURCE_COMPOSITION_OR_fEM_ZERO_NEXT - next step sources source-body composition or derives f_EM=0

## Next checkpoint

`3663-Y5-R2FR-EM-source-composition-fill-or-fEM-zero-theorem.md` via `scripts/Y5_R2FR_3663_EM_source_composition_fill_or_fEM_zero_theorem.py`.

## Sources
- `next_3661`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3661_NEXT_TARGET.csv` exists=True needle_found=True
- `basis_3661`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3661_QX_COMPONENT_BASIS_ROWS.csv` exists=True needle_found=True
- `envelope_3661`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3661_QX_NO_CANCELLATION_ENVELOPE_ROWS.csv` exists=True needle_found=True
- `arenas_3661`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3661_SHARED_BOUND_ARENA_ROWS.csv` exists=True needle_found=True
- `material_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv` exists=True needle_found=True
- `matter_theorem_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `local_bounds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `external_atomic_weights`: `CIAAW/IUPAC standard atomic weights; https://www.ciaaw.org/atomic-weights.htm` exists=True needle_found=True
- `external_SEMF_aC`: `semi_empirical_mass_formula_convention; a_C≈0.711 MeV; see https://en.wikipedia.org/wiki/Semi-empirical_mass_formula` exists=True needle_found=True
