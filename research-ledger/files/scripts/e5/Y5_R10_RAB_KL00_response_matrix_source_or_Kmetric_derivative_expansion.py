from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1289"
TITLE = "1289-Y5-R10-RAB-KL00-response-matrix-source-or-Kmetric-derivative-expansion"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
VARIATION_EXPANSION_PATH = OUT_DIR / f"{PACK_ID}_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv"
FIRST_DERIVATIVE_ROW_PATH = OUT_DIR / f"{PACK_ID}_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv"
RESPONSE_HUNT_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_COEFFICIENT_HUNT_LEDGER.csv"
DELTAK_COMPARISON_PATH = OUT_DIR / f"{PACK_ID}_DELTAK00_COMPARISON_TEMPLATE.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1289_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        VARIATION_EXPANSION_PATH,
        FIRST_DERIVATIVE_ROW_PATH,
        RESPONSE_HUNT_PATH,
        DELTAK_COMPARISON_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1289_0_1288_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_NEXT_TARGET.csv",
            "needle": "NEXT1288_0_1289",
            "role": "handoff into response coefficient source or Kmetric derivative expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_1_1288_gamma_metric_dependence",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "needle": "KMR1288_1_Gamma_metric_dependence",
            "role": "specific blocker for metric dependence of Gamma_eff",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_2_1288_derivative_terms",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "needle": "KMR1288_2_derivative_terms",
            "role": "specific blocker for derivative terms beyond volume response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_3_1286_gamma_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv",
            "needle": "RFR1286_0_Gamma_memory_scalar_projection",
            "role": "Gamma_eff=L_cg^-2 F(m) formula row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_4_798_definition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_0_definition",
            "role": "Gamma_eff source definition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_5_798_gradient",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_1_gradient_expansion",
            "role": "ordinary product-rule expansion for Gamma_eff",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_6_776_metric_dependence",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "KGL776_1_G_metric_dependence",
            "role": "existing metric-dependence blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_7_776_derivative",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "needle": "KGL776_2_derivative_terms",
            "role": "existing derivative/projector stress blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_8_514_candidate_A",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "needle": "GK514_A_metric_response_scalar_density",
            "role": "candidate action S_GK=-int sqrt(-g) Gamma_eff",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_9_514_contract",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_1_Khat_metric_response",
            "role": "contract requiring K_hat to equal metric response of Gamma_eff",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_10_515_audit",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            "needle": "MA515_1_Khat_metric_response",
            "role": "prior audit says metric response was not computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_11_1281_variation_requirement",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1281_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv",
            "needle": "GKM1281_2_metric_variation",
            "role": "requirement to compute K_metric formula and derivative accounting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_12_1287_KL00",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
            "needle": "KTC1287_0_flat_Ricci_scalar_KL00",
            "role": "formal KL00 candidate for later Delta_K comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1289_13_1288_response_hunt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "needle": "RMR1288_7_response_verdict",
            "role": "response coefficients still absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    variation_expansion = [
        {
            "expansion_id": "KVE1289_0_action_convention",
            "target": "Kmetric[Gamma_eff]",
            "formula": "S_Gamma=-int sqrt(-g) Gamma_eff; T_GK^{mu nu}=Gamma_eff g^{mu nu}-Kmetric^{mu nu} up to the fixed sign/volume convention",
            "source_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv;source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "source_anchor": "GK514_A_metric_response_scalar_density;MR514_1_Khat_metric_response",
            "what_is_fixed": "the variational route and the need for a metric-response object",
            "what_is_not_fixed": "overall sign, volume convention, derivative terms, and Khat equality",
            "current_status": "CONVENTION_BRANCH_WRITTEN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "expansion_id": "KVE1289_1_chain_rule_scalar_variation",
            "target": "delta Gamma_eff",
            "formula": "delta Gamma_eff=L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg plus any metric dependence hidden in derivative/domain/projector definitions",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "RFR1286_0_Gamma_memory_scalar_projection;GSE798_0_definition;GSE798_1_gradient_expansion",
            "what_is_fixed": "ordinary chain-rule part of the metric variation",
            "what_is_not_fixed": "delta m/delta g, delta L_cg/delta g, derivative/projector stress, boundary terms",
            "current_status": "FIRST_CHAIN_RULE_VARIATION_WRITTEN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "expansion_id": "KVE1289_2_metric_response_kernels",
            "target": "Kmetric_chain^{00}",
            "formula": "Kmetric_chain^{00}=C_sign[L_cg^-2 F_prime(m) M_m^{00}-2 L_cg^-3 F(m) M_L^{00}]+K_conn^{00}+K_domain^{00}+K_boundary^{00}",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "source_anchor": "KGL776_1_G_metric_dependence;KGL776_2_derivative_terms;KMR1288_1_Gamma_metric_dependence;KMR1288_2_derivative_terms",
            "what_is_fixed": "the first symbolic derivative component can be written as metric-response kernels for m and L_cg",
            "what_is_not_fixed": "M_m^{00}, M_L^{00}, K_conn^{00}, K_domain^{00}, K_boundary^{00}, and sign convention",
            "current_status": "FIRST_DERIVATIVE_KERNEL_ROW_WRITTEN_NOT_COMPUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "expansion_id": "KVE1289_3_local_fixed_point_implication",
            "target": "local silence condition for chain term",
            "formula": "if F_prime(m_*)=0, delta L_cg/delta g_{00}=0, K_conn=K_domain=K_boundary=0, and the branch is locked to m=m_*, then the first chain response can vanish",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "MR514_5_double_zero;GSE798_2_local_locked_expansion",
            "what_is_fixed": "the exact algebraic zero conditions for this chain term",
            "what_is_not_fixed": "parent lock to m_*, L_cg metric silence, and boundary/domain silence",
            "current_status": "CONDITIONAL_ZERO_CONDITIONS_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    first_derivative = [
        {
            "row_id": "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "component": "Kmetric_chain^{00}",
            "input_scalar": "Gamma_eff=L_cg^-2 F(m)",
            "variation_formula": "delta Gamma_eff=L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg",
            "kernel_formula": "Kmetric_chain^{00}=C_sign[L_cg^-2 F_prime(m) M_m^{00}-2 L_cg^-3 F(m) M_L^{00}] plus K_conn^{00}+K_domain^{00}+K_boundary^{00}",
            "kernel_definitions": "M_m^{00}:=metric response kernel for m; M_L^{00}:=metric response kernel for L_cg; C_sign fixed by Hilbert-stress convention",
            "units": "same_as_Gamma_eff_if_kernels_are_dimensionless; otherwise requires M_m/M_L units ledger",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "source_anchor": "RFR1286_0_Gamma_memory_scalar_projection;KGL776_1_G_metric_dependence;KGL776_2_derivative_terms",
            "needed_values": "MISSING_C_SIGN;MISSING_M_m_00_KERNEL;MISSING_M_L_00_KERNEL;MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00;MISSING_UNITS_LEDGER",
            "current_status": "FIRST_DERIVATIVE_TERM_SYMBOLIC_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "KDR1289_1_local_zero_condition_for_chain_kernel",
            "component": "Kmetric_chain^{00}_zero_gate",
            "input_scalar": "locked local fixed point m=m_* and locally silent L_cg",
            "variation_formula": "F_prime(m_*)=0 removes the m-kernel term; M_L^{00}=0 or F(m_*)=0 removes the L_cg metric response term",
            "kernel_formula": "Kmetric_chain^{00}=0 only if both chain channels and all connection/domain/boundary terms vanish or are bounded",
            "kernel_definitions": "double-zero/stationary m gate plus L_cg metric-silence gate",
            "units": "logic_gate",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "MR514_5_double_zero;GSE798_2_local_locked_expansion",
            "needed_values": "MISSING_PARENT_LOCK_TO_m_STAR;MISSING_PROOF_F_PRIME_ZERO;MISSING_LCG_METRIC_SILENCE;MISSING_BOUNDARY_NO_FLUX",
            "current_status": "ZERO_GATE_CONDITIONAL_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    response_hunt = [
        {
            "hunt_id": "RCH1289_0_response_matrix_route",
            "target": "first local response coefficient for K_L^{00}",
            "searched_source": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "result": "NO_NUMERIC_OR_SOURCE_BACKED_RESPONSE_COEFFICIENT_FOUND",
            "why": "1288 contains requirement rows only; every arena row remains MISSING_* or NONCLAIM_TEMPLATE_ONLY",
            "next_action": "derive response from weak-field equation after Kmetric/Khat comparison, or source a PPN/R10/clock/orbital kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "RCH1289_1_Newton_source_route",
            "target": "K00 projection fraction and matter curvature norm",
            "searched_source": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "result": "PLACEHOLDER_INPUTS_ONLY",
            "why": "K00_projection_fraction and matter_curvature_norm are required but still marked missing",
            "next_action": "obtain the Khat/Kmetric component convention before scoring epsilon_K00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "RCH1289_2_best_route_selection",
            "target": "choose 1289 path",
            "searched_source": "1288 blockers plus 514/515 response contract",
            "result": "KMETRIC_DERIVATIVE_EXPANSION_IS_BETTER_ROUTE_NOW",
            "why": "response coefficients need the very tensor/readout convention that Kmetric expansion begins to define",
            "next_action": "turn M_m^{00} and M_L^{00} from symbols into parent-sourced kernels or prove they vanish locally",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    deltak_comparison = [
        {
            "comparison_id": "DTC1289_0_KL_candidate",
            "object": "K_hat^{00}_candidate",
            "formula": "K_L^{00}=2 nabla^0 nabla^0 phi - (1/2)g^{00}Box phi",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
            "source_anchor": "KTC1287_0_flat_Ricci_scalar_KL00",
            "status": "FORMAL_KHAT_CANDIDATE_EXISTS_NONCLAIM",
            "missing_before_comparison": "MISSING_PARENT_ORIGIN_FOR_PHI;MISSING_CURRENT_MTS_KHAT_MATCH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "DTC1289_1_Kmetric_partial",
            "object": "Kmetric^{00}_partial",
            "formula": "Kmetric^{00}=Kmetric_volume^{00}+Kmetric_chain^{00}+K_conn^{00}+K_domain^{00}+K_boundary^{00}",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "KMC1287_0_volume_metric_response;KDR1289_0_Gamma_m_L_chain_kernel_00",
            "status": "PARTIAL_KMETRIC_STRUCTURE_WRITTEN_NOT_COMPUTABLE",
            "missing_before_comparison": "MISSING_C_SIGN;MISSING_M_m_00;MISSING_M_L_00;MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "DTC1289_2_DeltaK00_template",
            "object": "Delta_K^{00}",
            "formula": "Delta_K^{00}=K_L^{00}-[Kmetric_volume^{00}+Kmetric_chain^{00}+K_conn^{00}+K_domain^{00}+K_boundary^{00}]",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "DKS1287_2_component_comparison;KDR1289_0_Gamma_m_L_chain_kernel_00",
            "status": "DELTAK00_TEMPLATE_IMPROVED_BUT_NOT_COMPUTABLE",
            "missing_before_comparison": "MISSING_FULL_KMETRIC;MISSING_CURRENT_KHAT_MATCH;MISSING_BOUNDARY_AND_RESPONSE_LIMITS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1289_0_source_provenance",
            "claim": "private checkpoint source provenance",
            "current_status": "SATISFIED_FOR_PRIVATE_CHECKPOINT",
            "reason": "all registered local source paths and anchors are validated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1289_1_first_derivative_component",
            "claim": "first Kmetric derivative term is exact and scoreable",
            "current_status": "BLOCKED_SYMBOLIC_KERNELS_ONLY",
            "reason": "M_m^{00}, M_L^{00}, sign convention, units, and connection/domain/boundary terms are not parent-sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1289_2_response_coefficient",
            "claim": "first local response coefficient has been sourced",
            "current_status": "BLOCKED_NO_RESPONSE_COEFFICIENT_FOUND",
            "reason": "1288 response rows are requirements, not coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1289_3_DeltaK00",
            "claim": "Delta_K^{00} computable",
            "current_status": "BLOCKED_PARTIAL_KMETRIC_ONLY",
            "reason": "Delta_K template is sharper, but full Kmetric and current Khat match remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1289_4_local_GR",
            "claim": "local GR/PPN recovery",
            "current_status": "BLOCKED_NONCLAIM",
            "reason": "no metric-silence theorem, amplitude score, or response-vector pass exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1289_0_route_taken",
            "decision": "derive the Kmetric chain-rule expansion before hunting numeric response coefficients",
            "because": "the response matrix needs a defined tensor/readout convention, while Gamma_eff already supplies a source-backed scalar formula",
            "next_action": "source or prove zero for M_m^{00} and M_L^{00}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1289_1_progress",
            "decision": "Kmetric is no longer volume-only",
            "because": "the first derivative kernel structure is now explicit",
            "next_action": "turn the kernels into parent-derived tensor rows or show the local fixed point kills them",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1289_2_no_claim",
            "decision": "do not claim Delta_K or local GR",
            "because": "the new row exposes missing kernels rather than filling them numerically",
            "next_action": "1289 routes to m/L_cg metric-kernel source or fixed-point chain-zero proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1289_0_1290",
            "target_file": "1290-Y5-R10-RAB-m-Lcg-metric-kernel-source-or-fixed-point-chain-zero.md",
            "target_script": "scripts/Y5_R10_RAB_m_Lcg_metric_kernel_source_or_fixed_point_chain_zero.py",
            "task": "derive or source the metric-response kernels M_m^{00} and M_L^{00}, or prove the local fixed-point conditions that make the chain kernel vanish",
            "success_condition": "one kernel becomes source-backed/zero with stated assumptions, or the chain-zero route is rejected and carried as a finite residual",
            "do_not": "do not treat the chain-rule expansion itself as a Kmetric computation or a local-GR/PPN pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(VARIATION_EXPANSION_PATH, variation_expansion)
    write_csv(FIRST_DERIVATIVE_ROW_PATH, first_derivative)
    write_csv(RESPONSE_HUNT_PATH, response_hunt)
    write_csv(DELTAK_COMPARISON_PATH, deltak_comparison)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1289_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    first_chain = next(row for row in variation_expansion if row["expansion_id"] == "KVE1289_1_chain_rule_scalar_variation")
    validations.append(
        validation_row(
            "VAL1289_1_chain_rule_written",
            "delta Gamma_eff chain-rule variation is written",
            "delta Gamma_eff=L_cg^-2 F_prime(m) delta m" in first_chain["formula"]
            and is_false(first_chain["claim_allowed"]),
            "KVE1289_1_chain_rule_scalar_variation",
        )
    )
    derivative_row = next(row for row in first_derivative if row["row_id"] == "KDR1289_0_Gamma_m_L_chain_kernel_00")
    validations.append(
        validation_row(
            "VAL1289_2_first_derivative_row_nonclaim",
            "first Kmetric derivative kernel row exists, has missing inputs, and remains nonclaim",
            "MISSING_" in derivative_row["needed_values"]
            and derivative_row["current_status"] == "FIRST_DERIVATIVE_TERM_SYMBOLIC_NOT_SCOREABLE"
            and is_false(derivative_row["valid_for_claim"])
            and is_false(derivative_row["claim_allowed"]),
            "KDR1289_0_Gamma_m_L_chain_kernel_00",
        )
    )
    response_verdict = next(row for row in response_hunt if row["hunt_id"] == "RCH1289_0_response_matrix_route")
    validations.append(
        validation_row(
            "VAL1289_3_response_coefficients_not_claimed",
            "response coefficient route remains explicitly unfilled",
            response_verdict["result"] == "NO_NUMERIC_OR_SOURCE_BACKED_RESPONSE_COEFFICIENT_FOUND"
            and is_false(response_verdict["claim_allowed"]),
            "RCH1289_0_response_matrix_route",
        )
    )
    deltak_template = next(row for row in deltak_comparison if row["comparison_id"] == "DTC1289_2_DeltaK00_template")
    validations.append(
        validation_row(
            "VAL1289_4_DeltaK_template_improved_not_computable",
            "DeltaK00 comparison template is improved but still blocked",
            deltak_template["status"] == "DELTAK00_TEMPLATE_IMPROVED_BUT_NOT_COMPUTABLE"
            and "MISSING_FULL_KMETRIC" in deltak_template["missing_before_comparison"],
            "DTC1289_2_DeltaK00_template",
        )
    )
    validations.append(
        validation_row(
            "VAL1289_5_claim_gates_blocked",
            "claim gates block local GR/PPN promotion",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        VARIATION_EXPANSION_PATH,
        FIRST_DERIVATIVE_ROW_PATH,
        RESPONSE_HUNT_PATH,
        DELTAK_COMPARISON_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1289_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1289_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1289_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, variation_expansion, first_derivative, response_hunt, deltak_comparison, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1289_9_next_target_1290",
            "next target routes to m/Lcg metric kernel source or fixed-point chain zero",
            next_target[0]["next_id"] == "NEXT1289_0_1290" and "M_m" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1289_10_overall",
            "overall 1289 validation",
            overall_pass,
            "1289 writes the first Kmetric chain-rule derivative kernel row, keeps response coefficients and DeltaK00 nonclaim, and routes to m/Lcg kernels or fixed-point zero",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1289 Y5 R10 RAB KL00 response matrix source or Kmetric derivative expansion

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1289 takes the derivation route. The first real `Kmetric[Gamma_eff]` derivative structure is now written: `delta Gamma_eff=L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg`, giving a symbolic `Kmetric_chain^{{00}}` row. This is progress, but still not a computable `Kmetric^{{00}}` component.

**Main progress:** `Kmetric` is no longer just “volume term plus unknowns.” The unknowns are now split into specific kernels: `M_m^{{00}}`, `M_L^{{00}}`, `K_conn^{{00}}`, `K_domain^{{00}}`, and `K_boundary^{{00}}`. That is exactly the right place to attack next.

**Next derivation target:** derive/source `M_m^{{00}}` and `M_L^{{00}}`, or prove the fixed-point chain-zero conditions that make both metric-response channels silent.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Kmetric Variation Expansion

{markdown_table(variation_expansion, ["expansion_id", "target", "formula", "source_path", "source_anchor", "what_is_fixed", "what_is_not_fixed", "current_status", "valid_for_claim", "claim_allowed"])}

## First Derivative Term Rows

{markdown_table(first_derivative, ["row_id", "component", "input_scalar", "variation_formula", "kernel_formula", "kernel_definitions", "units", "source_path", "source_anchor", "needed_values", "current_status", "valid_for_claim", "claim_allowed"])}

## Response Coefficient Hunt Ledger

{markdown_table(response_hunt, ["hunt_id", "target", "searched_source", "result", "why", "next_action", "valid_for_claim", "claim_allowed"])}

## DeltaK00 Comparison Template

{markdown_table(deltak_comparison, ["comparison_id", "object", "formula", "source_path", "source_anchor", "status", "missing_before_comparison", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
