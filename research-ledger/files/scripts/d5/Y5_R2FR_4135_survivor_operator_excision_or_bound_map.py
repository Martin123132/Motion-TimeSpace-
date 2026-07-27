from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4135-Y5-R2FR-survivor-operator-excision-or-bound-map.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SURVIVOR_OPERATOR_EXCISION_OR_BOUND_MAP_4135"
CHECKPOINT_ID = "4135"
DECISION = "SURVIVOR_OPERATORS_REDUCED_TO_LOCAL_NORMAL_FORM_OR_COEFFICIENT_EXTRACTOR"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4135_00_4134_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4134_NEXT_TARGET.csv",
        "4135-Y5-R2FR-survivor-operator-excision-or-bound-map.md",
        "4134 selected survivor operator excision or bound map.",
    ),
    "SRC4135_01_4134_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4134_STATUS.csv",
        "QEXTRA_REDUCED_TO_SURVIVOR_OPERATOR_BOUNDARY_FLUX_REMAINDER",
        "4134 Qextra remainder status.",
    ),
    "SRC4135_02_4134_live_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4134_LIVE_BOUND_ROWS.csv",
        "R_survivor_ops",
        "Reduced live Qextra survivor operator bound.",
    ),
    "SRC4135_03_4134_matrix": (
        SOURCE_DIR / "P8_Y5_R2FR_4134_CHANNEL_ZERO_MATRIX.csv",
        "NOT_ZERO_UNTIL_SURVIVOR_OPERATORS_EXCISED_OR_BOUNDED",
        "4134 channel matrix identifying nonEH survivors.",
    ),
    "SRC4135_04_4021_witness": (
        SOURCE_DIR / "P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv",
        "WIT4021_2_no_extra_operators",
        "Local parent-action witness and no-extra-operator clause.",
    ),
    "SRC4135_05_4021_lemmas": (
        SOURCE_DIR / "P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
        "LEM4021_1_EH_operator_zero",
        "Derived zero lemmas under the witness.",
    ),
    "SRC4135_06_4022_ops": (
        SOURCE_DIR / "P8_Y5_R2FR_4022_OPERATOR_CLASS_STRESS_TEST.csv",
        "OP4022_10_Gamma_Khat_q_loc",
        "Operator stress-test survivor list.",
    ),
    "SRC4135_07_4022_survivors": (
        SOURCE_DIR / "P8_Y5_R2FR_4022_SURVIVOR_PPN_ROUTE.csv",
        "SURV4022_10_Gamma_Khat_q_loc",
        "Survivor PPN route and coefficient requirements.",
    ),
    "SRC4135_08_double_zero_r11": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv",
        "R2_fR_scalar_mode",
        "Double-zero operator mapping for local R11 survivors.",
    ),
    "SRC4135_09_local_eh_r11": (
        SOURCE_DIR / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
        "Ricci_Weyl_squared",
        "Local EH R11 operator audit.",
    ),
    "SRC4135_10_memory": (
        SOURCE_DIR / "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        "O2_quadratic_gate_sufficient",
        "Double-zero memory origin attempt.",
    ),
    "SRC4135_11_operator_requirements": (
        SOURCE_DIR / "P8_OPERATOR_CLASSIFICATION_REQUIREMENTS.csv",
        "retained_residual",
        "Operator classification requirements.",
    ),
    "SRC4135_12_gk_decision": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_DECISION.csv",
        "q_loc_problem_reduced_to_variational_stress_problem",
        "Gamma/Khat/q_loc decision.",
    ),
    "SRC4135_13_gk_residual": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
        "QR513_0_nonvariational_stress",
        "Gamma/Khat/q_loc residual or demotion ledger.",
    ),
    "SRC4135_14_source_norm": (
        SOURCE_DIR / "P8_R11_SOURCE_NORMALIZATION_DECISION.csv",
        "D0_minimum_fill",
        "Source-normalization operator decision.",
    ),
    "SRC4135_15_qloc_bound": (
        SOURCE_DIR / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "QB516_4_R11_operator",
        "q_loc bound runner specification.",
    ),
    "SRC4135_16_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4135_survivor_operator_excision_or_bound_map.py",
        "Reproducible generator for this 4135 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def normal_form_theorem_rows() -> List[dict]:
    data = [
        (
            "NFT4135_0_operator_basis",
            "local 2PN normal form",
            "S_loc^{<=2PN}=S_vert[Phi]+(2 kappa_*)^-1 int R[g_obs]eps_obs+S_matter+S_EM+S_binding+dB+S_top+S_aux^double-zero",
            "This is the strongest clean route: name the local parent action class and forbid all other <=2PN observed-metric operators rather than tune them later.",
            "NORMAL_FORM_IMPORTED_FROM_WIT4021",
        ),
        (
            "NFT4135_1_excision_theorem",
            "survivor operator excision theorem",
            "If every retained survivor is exact/topological, vertical with Dq=0, auxiliary double-zero, higher than 2PN, or absent, then R_survivor_ops=0.",
            "Vary by class: exact/topological terms give no local Euler stress; vertical terms do not vary g_obs; double-zero terms vanish with first variation at the fixed point; absent terms have zero coefficient.",
            "DERIVED_CANDIDATE_EXCISION_THEOREM",
        ),
        (
            "NFT4135_2_no_smuggling_gate",
            "adoption or coefficient fork",
            "R_survivor_ops=0 requires actual corpus adoption of the normal form; otherwise every survivor must expose coefficient, units, weak-field projection, source path, and arena tolerance.",
            "A private witness is enough to guide derivation but not enough to claim local GR.",
            "PUBLIC_CLAIM_BLOCKED_UNTIL_ADOPTION_OR_BOUNDS",
        ),
        (
            "NFT4135_3_reduced_master",
            "reduced Qextra remainder",
            "epsilon_Qextra_4135 = R_survivor_ops[normal_form_or_coefficients] + R_boundary_harmonic + R_undescended_support + R_unstationary_flux + R_parent_adoption",
            "4135 removes ambiguity from R_survivor_ops: it is now a normal-form adoption problem or a concrete coefficient extractor problem.",
            "MASTER_REMAINDER_REDUCED",
        ),
    ]
    rows: List[dict] = []
    for theorem_id, claim_piece, formula, proof, status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "formula": formula,
                "proof_skeleton": proof,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def operator_excision_rows() -> List[dict]:
    data = [
        (
            "OEM4135_0_R2_fR",
            "R2_fR_scalar_mode",
            "c_R2_or_c_fR",
            "length^2 or normalized dimensionless curvature coefficient",
            "exclude by normal form; admit only auxiliary double-zero, vertical-only, higher-than-2PN, or explicit coefficient bound",
            "EXCISED_BY_WIT4021_IF_ADOPTED_ELSE_COEFFICIENT_REQUIRED",
            "delta_gamma_R11 + delta_beta_R11 + alpha(lambda)",
            "scalar mass/coupling map, R10 lambda, PPN gamma/beta projection",
            "P8_Y5_R2FR_4022_SURVIVOR_PPN_ROUTE.csv",
        ),
        (
            "OEM4135_1_Ricci_Weyl",
            "Ricci_Weyl_squared",
            "c_Ricci_or_c_Weyl",
            "length^2 or normalized quadratic-curvature coefficient",
            "admit only 4D topological Gauss-Bonnet/exact combination, auxiliary double-zero, or explicit weak-field projection",
            "TOPOLOGICAL_GB_OR_EXCISED_ELSE_COEFFICIENT_REQUIRED",
            "delta_gamma_R11 + xi + wave/slip sector",
            "quadratic curvature basis, GB decomposition flag, spin-2/scalar weak-field projection",
            "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
        ),
        (
            "OEM4135_2_scalar_tensor",
            "scalar_tensor_class_metric",
            "F_phi_C_or_c_scalar",
            "dimensionless coupling plus derivative/range units",
            "exclude unless scalar is locally fixed with zero derivatives, coupling is double-zero, or coefficient/range is bounded",
            "EXCISED_BY_FIXED_SCALAR_OR_DOUBLE_ZERO_ELSE_BOUND_REQUIRED",
            "Gdot/G + gamma/beta + clocks + alpha(lambda)",
            "F_phi derivatives, scalar mass/range, matter coupling, clock and R10 projection",
            "P8_Y5_R2FR_4022_OPERATOR_CLASS_STRESS_TEST.csv",
        ),
        (
            "OEM4135_3_vector",
            "vector_preferred_frame",
            "c_domain_vector_or_selector_marker",
            "dimensionless vector/aether/domain-selector coefficient",
            "exclude unless no local preferred selector/vector exists, or vector coefficient is double-zero/vertical",
            "EXCISED_BY_NO_VECTOR_THEOREM_ELSE_PREFERRED_FRAME_BOUND",
            "alpha1 + alpha2 + alpha3 + xi",
            "vector norm, coupling coefficients, domain anisotropy map, preferred-frame projection",
            "P8_Y5_R2FR_4022_WITNESS_ADMISSION_MATRIX.csv",
        ),
        (
            "OEM4135_4_torsion_nonmetricity",
            "torsion_nonmetricity",
            "c_T_or_c_Q",
            "connection-response coefficient",
            "exclude by observed Levi-Civita branch or prove torsion/nonmetricity coefficient double-zero",
            "EXCISED_BY_LEVI_CIVITA_OBSERVED_BRANCH_ELSE_CONNECTION_BOUND",
            "WEP + clock + lightcone + R11 ledger",
            "independent connection flag, torsion/nonmetricity source coupling, clock/lightcone projection",
            "P8_Y5_R2FR_4022_OPERATOR_CLASS_STRESS_TEST.csv",
        ),
        (
            "OEM4135_5_bulk_X",
            "bulk_X_force_law",
            "q_X_or_c_X",
            "source charge plus mass/range coefficient",
            "exclude if bulk field is vertical/source-silent/double-zero; otherwise expose q_X, m_X, lambda_X and source charge",
            "EXCISED_BY_VERTICAL_SOURCE_SILENCE_ELSE_FINITE_RANGE_BOUND",
            "R10 alpha(lambda) + WEP/source charge + gamma/beta",
            "q_X, m_X, lambda_X, alpha_X(lambda), source-charge normalization",
            "P8_Y5_R2FR_4022_SURVIVOR_PPN_ROUTE.csv",
        ),
        (
            "OEM4135_6_memory",
            "nonlocal_memory_kernel",
            "c_nonlocal_or_K_norm",
            "kernel norm in compact local branch",
            "exclude only if compact-local memory kernel is vertical/source-silent or has a double-zero norm; linear selector is rejected",
            "EXCISED_BY_DOUBLE_ZERO_MEMORY_KERNEL_ELSE_KERNEL_BOUND",
            "alpha3 + Gdot/G + R10 alpha(lambda)",
            "K_mem^loc norm, support radius, monopole projection, time/range derivative",
            "P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
        ),
        (
            "OEM4135_7_GK_q_loc",
            "Gamma_Khat_q_loc",
            "D_GK_or_Q_loc_profile",
            "q_loc force/source-exchange or dimensionless compact-shell proxy",
            "excisable only if T_GK is Hilbert stress from a diffeo-invariant sector, vertical kernel, on-shell Euler zero, projector-owned and boundary-silent",
            "PRIMARY_RESIDUAL_REQUIRES_ACTION_OR_QLOC_BOUND",
            "delta_beta_q_loc + alpha(lambda) + local force/source-exchange",
            "S_GK action match or D_GK components, P_loc ownership, q_loc amplitude/profile, PPN/R10 projection",
            "P8_GAMMA_KHAT_QLOC_DECISION.csv",
        ),
        (
            "OEM4135_8_source_norm",
            "source_normalization_operator",
            "c_domain_source_normalization_operator",
            "dimensionless source prefactor or domain-normalization coefficient",
            "exclude by same Hilbert source current and no extra mu/source prefactor; otherwise coefficient feeds Newton/PPN source denominator",
            "EXCISED_BY_SAME_SOURCE_THEOREM_ELSE_SOURCE_PREFAC_BOUND",
            "delta_beta_source + alpha1/alpha2/alpha3/xi + Newton GM",
            "same-source theorem flag, source prefactor coefficient, domain dependence, PPN/Newton projection",
            "P8_R11_SOURCE_NORMALIZATION_DECISION.csv",
        ),
    ]
    rows: List[dict] = []
    for operator_id, family, coeff, units, excision, verdict, projections, required, source_name in data:
        source_path = SOURCE_DIR / source_name
        row = row_base()
        row.update(
            {
                "operator_id": operator_id,
                "operator_family": family,
                "coefficient_symbol": coeff,
                "coefficient_units": units,
                "excision_route": excision,
                "verdict": verdict,
                "arena_projection": projections,
                "required_if_not_excised": required,
                "source_path": str(source_path),
                "source_exists": str(source_path.exists()),
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def coefficient_extractor_rows() -> List[dict]:
    data = [
        (
            "CER4135_0_R2_fR",
            "R2_fR_scalar_mode",
            "read coefficient of R^2 or f_RR around local background; derive scalar mass m0^2~1/c_R2 if present",
            "c_R2_or_c_fR, m0, coupling_to_T, lambda0=1/m0",
            "dimensionless alpha(lambda); delta_gamma; delta_beta",
        ),
        (
            "CER4135_1_Ricci_Weyl",
            "Ricci_Weyl_squared",
            "decompose quadratic basis into Gauss-Bonnet plus Ricci^2/Weyl^2 remainders",
            "c_GB, c_Ricci_res, c_Weyl_res, spin2_mass_or_projection",
            "delta_gamma; xi; wave/slip sector",
        ),
        (
            "CER4135_2_scalar_tensor",
            "scalar_tensor_class_metric",
            "linearize F(phi)R and matter coupling around local fixed point",
            "F_phi, F_phiphi, alpha_phi, m_phi, D_t phi, D_r phi",
            "Gdot/G; clocks; gamma/beta; alpha(lambda)",
        ),
        (
            "CER4135_3_vector",
            "vector_preferred_frame",
            "identify local vector/domain selector and compute anisotropic stress/preferred-frame coefficients",
            "u_mu, c_i, norm constraint, domain anisotropy, W_domain_alpha_i",
            "alpha1; alpha2; alpha3; xi",
        ),
        (
            "CER4135_4_torsion",
            "torsion_nonmetricity",
            "split observed connection into Levi-Civita plus torsion/nonmetricity residual",
            "T^a_bc, Q_abc, c_T, c_Q, hypermomentum/source coupling",
            "WEP; clock; lightcone; R11",
        ),
        (
            "CER4135_5_bulk_X",
            "bulk_X_force_law",
            "extract finite-range field source charge and propagator",
            "q_X, m_X, lambda_X, alpha_X, source composition factor",
            "R10 alpha(lambda); WEP; gamma/beta",
        ),
        (
            "CER4135_6_memory",
            "nonlocal_memory_kernel",
            "restrict kernel to compact local branch and compute support/projection norm",
            "K_mem^loc, support radius, monopole projection, D_t/D_r kernel response",
            "alpha3; Gdot/G; R10",
        ),
        (
            "CER4135_7_GK",
            "Gamma_Khat_q_loc",
            "try S_GK match first; if mismatch remains, extract D_GK and q_loc profile",
            "D_trace, D_A_grad, D_gamma_grad, D_cross_AG, D_mass_gap, D_boundary, P_loc",
            "delta_beta_q_loc; alpha(lambda); source-exchange",
        ),
        (
            "CER4135_8_source_norm",
            "source_normalization_operator",
            "compare matter/Hilbert/active/passive/source-denominator normalizations before readout",
            "c_source_prefactor, domain dependence, species dependence, beta_source drift",
            "Newton GM; delta_beta_source; preferred-frame source terms",
        ),
    ]
    rows: List[dict] = []
    for extractor_id, family, extraction_task, required_fields, target_rows in data:
        row = row_base()
        row.update(
            {
                "extractor_id": extractor_id,
                "operator_family": family,
                "extraction_task": extraction_task,
                "required_fields": required_fields,
                "target_score_rows": target_rows,
                "status": "EXTRACTOR_TEMPLATE_READY_NONCLAIM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def reduced_bound_rows() -> List[dict]:
    data = [
        (
            "RBR4135_0_master",
            "R_survivor_ops_4135",
            "sum_abs(R_R2fR,R_RicciWeyl,R_scalar,R_vector,R_connection,R_bulkX,R_memory,R_GKqloc,R_source_norm)",
            "dimensionless master residual",
            "PPN + R10 + WEP + clocks + Newton/source coupling",
            "zero iff every operator is excised by local normal form or has zero coefficient/projection",
        ),
        (
            "RBR4135_1_normal_form_guard",
            "Z_local_normal_form",
            "1 only if actual MTS local <=2PN action is WIT4021 normal form",
            "boolean adoption guard",
            "claim governance",
            "cannot be replaced by private witness alone",
        ),
        (
            "RBR4135_2_coefficient_pack",
            "C_survivor_coefficients",
            "vector(c_R2,c_Ricci,c_Weyl,F_phi,c_vector,c_T,c_Q,q_X,K_mem,D_GK,c_source)",
            "declared per coefficient",
            "coefficient extractor",
            "needed if Z_local_normal_form is false or partial",
        ),
        (
            "RBR4135_3_projection_pack",
            "Pi_survivor_to_arena",
            "weak-field projection from survivor coefficients to PPN/R10/WEP/clock/Newton rows",
            "arena-specific",
            "empirical robustness",
            "prevents symbolic coefficient rows from pretending to be tests",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, arena, condition in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "arena_projection": arena,
                "condition_for_zero_or_score": condition,
                "status": "REDUCED_OPERATOR_BOUND_NONCLAIM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DG4135_0_key_reduction",
            "SURVIVOR_FORK_IS_NOW_EXPLICIT",
            "The hard operator remainder is no longer vague: either adopt the WIT4021 local normal form, or extract a coefficient/projection pack for each survivor.",
            "use this fork instead of circling missing rows",
        ),
        (
            "DG4135_1_best_route",
            "LOCAL_NORMAL_FORM_ADOPTION_IS_BEST_NEXT_ROUTE",
            "Scoring every survivor is possible but expensive; the cleaner theory route is to prove the actual MTS parent local action normal-forms to EH+matter+EM+allowed silent terms through 2PN.",
            "try adoption proof before broad numeric fallback",
        ),
        (
            "DG4135_2_GK_exception",
            "GK_QLOC_REMAINS_PRIMARY_SPECIAL_CASE",
            "Gamma/Khat/q_loc is not just another curvature operator: it has a variational-stress route and a q_loc bound fallback, so it should be handled explicitly in the next normal-form pass.",
            "carry S_GK or q_loc profile gate into 4136",
        ),
        (
            "DG4135_3_claim_ceiling",
            "NO_LOCAL_GR_CLAIM",
            "No survivor operator is claim-zero unless the normal form is parent-adopted or its coefficient/projection is actually sourced.",
            "keep local GR/Newton/PPN/R10 blocked",
        ),
        (
            "DG4135_4_next",
            "NEXT_LOCAL_PARENT_NORMAL_FORM_SELECTED",
            "The next move should attempt actual local parent-action normal-form adoption, with a coefficient extractor generated if any term refuses to normal-form.",
            "4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4135_0",
            "result": DECISION,
            "summary": (
                "4135 converts the survivor-operator remainder into an explicit fork. If the actual MTS local "
                "2PN parent action adopts WIT4021 normal form, R2/fR, Ricci/Weyl remainders, scalar-tensor, vector, "
                "torsion/nonmetricity, bulk_X, memory, and source-normalization survivors are forbidden or silent; "
                "Gamma/Khat/q_loc remains a special variational-stress/q_loc-profile gate. If the normal form is not "
                "adopted, every survivor now has a named coefficient, units, weak-field projection and arena target."
            ),
            "normal_form_theorem_written": "True",
            "operator_map_filled": "True",
            "coefficient_extractor_filled": "True",
            "survivor_ops_zero_signed": "False",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4136 local parent-action normal-form adoption or coefficient extractor",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4135_0",
            "target_doc": "4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md",
            "target_script": "scripts/Y5_R2FR_4136_local_parent_action_normal_form_adoption_or_coefficient_extractor.py",
            "objective": (
                "attempt to prove the actual MTS local <=2PN parent action normal-forms to WIT4021: EH observed metric "
                "operator plus same-source matter/EM/binding, exact/topological boundary terms, vertical-only sectors, "
                "and auxiliary double-zero terms; if any operator refuses, emit the coefficient extractor rows from 4135"
            ),
            "success_gate": "Z_local_normal_form=true parent-signed, or every non-normal-form term has coefficient, units, source path, weak-field projection and arena tolerance",
            "reason": "4135 shows this is the highest-leverage fork: normal-form adoption kills most survivor operators, while failure produces a concrete scoreable coefficient pack.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4135_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4135_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM.csv",
        "P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP": SOURCE_DIR / "P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP.csv",
        "P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS.csv",
        "P8_Y5_R2FR_4135_REDUCED_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4135_REDUCED_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4135_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4135_DECISION_GATES.csv",
        "P8_Y5_R2FR_4135_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4135_STATUS.csv",
        "P8_Y5_R2FR_4135_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4135_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4135 - Survivor Operator Excision or Bound Map",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The survivor-operator remainder is now a precise fork: local normal-form adoption, or coefficient extraction.",
        "- This is the cleanest route because it forbids unwanted operators instead of trying to tune them away.",
        "- No Newton/local-GR/PPN/R10 pass is claimed.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Normal-Form Theorem", "", "| claim piece | status | formula |", "|---|---|---|"])
    for row in normal_form_theorem_rows():
        sections.append(f"| {row['claim_piece']} | {row['status']} | {row['formula']} |")
    sections.extend(["", "## Operator Map", "", "| operator | verdict | coefficient |", "|---|---|---|"])
    for row in operator_excision_rows():
        sections.append(f"| {row['operator_family']} | {row['verdict']} | {row['coefficient_symbol']} |")
    sections.extend(["", "## Coefficient Extractor", "", "| operator | required fields | target rows |", "|---|---|---|"])
    for row in coefficient_extractor_rows():
        sections.append(f"| {row['operator_family']} | {row['required_fields']} | {row['target_score_rows']} |")
    sections.extend(
        [
            "",
            "## Current Meaning",
            "",
            "- If the local parent action normal-form is adopted, most survivor operators are not merely small; they are absent, vertical, topological/exact, or double-zero silent.",
            "- If adoption fails, the branch does not collapse into vibes: it becomes a coefficient/projection extractor for PPN, R10, WEP, clocks and Newton/source coupling.",
            "- `Gamma/Khat/q_loc` remains the special hard case because it may be killed by a variational stress theorem or retained as an explicit q_loc profile.",
            "",
            "## Claim Ceiling",
            "",
            f"- {status['claim_state']}.",
            "- This checkpoint narrows the local-GR proof route; it does not complete it.",
            "",
            "## Next Target",
            "",
            "- `4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4135_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM": normal_form_theorem_rows,
        "P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP": operator_excision_rows,
        "P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS": coefficient_extractor_rows,
        "P8_Y5_R2FR_4135_REDUCED_BOUND_ROWS": reduced_bound_rows,
        "P8_Y5_R2FR_4135_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4135_STATUS": status_rows,
        "P8_Y5_R2FR_4135_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4135_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4135_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4135_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM"]])
    theorem_ok = all(
        token in theorem_text
        for token in ["S_loc^{<=2PN}", "R_survivor_ops=0", "exact/topological", "vertical with Dq=0", "auxiliary double-zero", "coefficient"]
    )
    add("VAL4135_3_theorem", "normal-form theorem states allowed classes and coefficient fallback", theorem_ok, "theorem tokens checked")

    map_text = flatten_rows([outputs["P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP"]])
    map_ok = all(
        token in map_text
        for token in [
            "R2_fR_scalar_mode",
            "Ricci_Weyl_squared",
            "scalar_tensor_class_metric",
            "vector_preferred_frame",
            "torsion_nonmetricity",
            "bulk_X_force_law",
            "nonlocal_memory_kernel",
            "Gamma_Khat_q_loc",
            "source_normalization_operator",
        ]
    )
    add("VAL4135_4_operator_coverage", "operator map covers all named survivors plus source-normalization leak", map_ok, "operator tokens checked")

    verdict_ok = all(
        token in map_text
        for token in [
            "EXCISED_BY_WIT4021_IF_ADOPTED_ELSE_COEFFICIENT_REQUIRED",
            "TOPOLOGICAL_GB_OR_EXCISED_ELSE_COEFFICIENT_REQUIRED",
            "EXCISED_BY_LEVI_CIVITA_OBSERVED_BRANCH_ELSE_CONNECTION_BOUND",
            "PRIMARY_RESIDUAL_REQUIRES_ACTION_OR_QLOC_BOUND",
            "EXCISED_BY_SAME_SOURCE_THEOREM_ELSE_SOURCE_PREFAC_BOUND",
        ]
    )
    add("VAL4135_5_verdicts", "operator map distinguishes normal-form excision, topological route, connection route, GK exception and source-normalization route", verdict_ok, "verdict tokens checked")

    coeff_text = flatten_rows([outputs["P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS"]])
    coeff_ok = all(
        token in coeff_text
        for token in [
            "c_R2_or_c_fR",
            "c_GB",
            "F_phi",
            "c_i",
            "T^a_bc",
            "q_X",
            "K_mem^loc",
            "D_trace",
            "c_source_prefactor",
        ]
    )
    add("VAL4135_6_extractors", "coefficient extractor rows name required fields for survivor scoring", coeff_ok, "extractor tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4135_REDUCED_BOUND_ROWS"]])
    bound_ok = all(token in bound_text for token in ["R_survivor_ops_4135", "Z_local_normal_form", "C_survivor_coefficients", "Pi_survivor_to_arena"])
    add("VAL4135_7_reduced_bounds", "reduced bound rows capture normal-form guard, coefficient pack and arena projection", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4135_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "SURVIVOR_FORK_IS_NOW_EXPLICIT",
            "LOCAL_NORMAL_FORM_ADOPTION_IS_BEST_NEXT_ROUTE",
            "GK_QLOC_REMAINS_PRIMARY_SPECIAL_CASE",
            "NO_LOCAL_GR_CLAIM",
            "NEXT_LOCAL_PARENT_NORMAL_FORM_SELECTED",
        ]
    )
    add("VAL4135_8_decisions", "decision gates record fork, best route, GK exception, no-claim and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4135_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("normal_form_theorem_written") == "True"
        and status[0].get("operator_map_filled") == "True"
        and status[0].get("survivor_ops_zero_signed") == "False"
    )
    add("VAL4135_9_status", "status records theorem/map/extractor and unsigned survivor zero", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4135_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md"
    add("VAL4135_10_next_target", "next target is local parent-action normal-form adoption or coefficient extractor", next_ok, str(nxt))

    op_rows = parse_csv(outputs["P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP"])
    op_sources_ok = all(row.get("source_exists") == "True" for row in op_rows)
    add("VAL4135_11_operator_sources", "each operator map row points to an existing source file", op_sources_ok, f"operator_rows={len(op_rows)}")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4135_12_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4135*")) or any(FORMALIZATION.rglob("4135-Y5-R2FR*"))
    add(
        "VAL4135_13_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4135_14_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4135_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
