from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1292"
TITLE = "1292-Y5-R10-RAB-F-form-and-m-Lcg-parent-source-match-or-residual-runner-input"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SCAN_SUMMARY_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_MATCH_SCAN_SUMMARY.csv"
F_MATCH_PATH = OUT_DIR / f"{PACK_ID}_F_FORM_SOURCE_MATCH_AUDIT.csv"
M_LCG_MATCH_PATH = OUT_DIR / f"{PACK_ID}_M_LCG_PARENT_SOURCE_MATCH_AUDIT.csv"
ADOPTION_VERDICT_PATH = OUT_DIR / f"{PACK_ID}_STRICT_DOUBLE_ZERO_ADOPTION_VERDICT.csv"
RUNNER_INPUT_PATH = OUT_DIR / f"{PACK_ID}_CHAIN_KERNEL_RESIDUAL_RUNNER_INPUT_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1292_VALIDATION.csv"


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
        SCAN_SUMMARY_PATH,
        F_MATCH_PATH,
        M_LCG_MATCH_PATH,
        ADOPTION_VERDICT_PATH,
        RUNNER_INPUT_PATH,
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


def scan_literal(pattern: str, exclude_prefixes: tuple[str, ...] = ("P8_Y5_R10_1291", "P8_Y5_R10_1292")) -> list[str]:
    matches: list[str] = []
    for path in OUT_DIR.glob("*.csv"):
        if path.name.startswith(exclude_prefixes):
            continue
        try:
            text = read_text(path)
        except OSError:
            continue
        if pattern in text:
            matches.append(path.name)
    return sorted(matches)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1292_0_1291_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_NEXT_TARGET.csv",
            "needle": "NEXT1291_0_1292",
            "role": "handoff into F/m/Lcg source-match or residual runner input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_1_1291_clause",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv",
            "needle": "SDZ1291_1_strict_F_form",
            "role": "strict double-zero theorem target to source-match",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_2_1291_proof",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_VARIATION_PROOF_NONCLAIM.csv",
            "needle": "VP1291_1_metric_variation",
            "role": "conditional chain-zero proof to gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_3_1291_adoption",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_ADOPTION_GATES.csv",
            "needle": "ADG1291_0_actual_F_form",
            "role": "adoption gate requiring actual F source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_4_1291_bounds",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "needle": "KRB1291_3_residual_verdict",
            "role": "residual bound ledger to convert into runner inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_5_1291_DeltaK",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1291_DELTAK_STATUS_UPDATE.csv",
            "needle": "DKS1291_2_DeltaK00",
            "role": "DeltaK remains blocked until chain zero or bounds close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_6_798_gamma",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_0_definition",
            "role": "actual generic Gamma_eff=L_cg^-2 F(m) source row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_7_798_locked",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_2_local_locked_expansion",
            "role": "conditional locked expansion but not actual strict F source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_8_801_double_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_801_DOUBLE_ZERO_LEMMA.csv",
            "needle": "DZ801_1_norm_evenness",
            "role": "conditional norm/evenness double-zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_9_801_parent_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_801_PARENT_FIXED_POINT_CONTRACT.csv",
            "needle": "FPC801_2_even_scalar_readout",
            "role": "conditional even scalar readout contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_10_symbol_map_Lcg",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "L_cg / ell_tr",
            "role": "L_cg/transition scale is open in action map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_11_symbol_gates_Lcg",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
            "needle": "FV512_6_transition_scale",
            "role": "L_cg/ell_tr first-variation gate remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1292_12_fixed_point_transition",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "needle": "FP511_8_local_cosmology_transition_control",
            "role": "transition scale must be action-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    strict_matches = scan_literal("F(m)=(m-m_*)^2")
    generic_matches = scan_literal("Gamma_eff = L_cg^-2 F(m)")
    lcg_matches = scan_literal("L_cg")
    scan_summary = [
        {
            "scan_id": "SCAN1292_0_strict_F_exact",
            "pattern": "F(m)=(m-m_*)^2",
            "scope": "source-intake/mts_residuals/*.csv excluding 1291/1292 generated rows",
            "match_count": len(strict_matches),
            "matched_files": ";".join(strict_matches[:12]) if strict_matches else "NONE",
            "interpretation": "actual strict F source not found outside the theorem-target checkpoint" if not strict_matches else "manual review required; pattern appears outside 1291/1292",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "SCAN1292_1_generic_Gamma",
            "pattern": "Gamma_eff = L_cg^-2 F(m)",
            "scope": "source-intake/mts_residuals/*.csv excluding 1291/1292 generated rows",
            "match_count": len(generic_matches),
            "matched_files": ";".join(generic_matches[:12]) if generic_matches else "NONE",
            "interpretation": "generic Gamma source exists, but generic F(m) is not the strict double-zero form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scan_id": "SCAN1292_2_Lcg_presence",
            "pattern": "L_cg",
            "scope": "source-intake/mts_residuals/*.csv excluding 1291/1292 generated rows",
            "match_count": len(lcg_matches),
            "matched_files": ";".join(lcg_matches[:12]) if lcg_matches else "NONE",
            "interpretation": "L_cg is present, but the inspected action-map rows classify parent ownership as open/missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    f_match = [
        {
            "match_id": "FSM1292_0_generic_F_source",
            "target": "actual Gamma_eff source",
            "required_match": "Gamma_eff=L_cg^-2 F(m) with F(m)=(m-m_*)^2H(m)",
            "best_evidence": "GSE798_0_definition gives Gamma_eff=L_cg^-2 F(m)",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "GSE798_0_definition",
            "result": "GENERIC_F_ONLY_NOT_STRICT_DOUBLE_ZERO",
            "blocks": "ADG1291_0_actual_F_form",
            "next_action": "keep strict clause as theorem target and use residual runner rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "FSM1292_1_locked_expansion",
            "target": "local locked expansion",
            "required_match": "parent law locks m=m_* and actual F has F(m_*)=F_prime(m_*)=0",
            "best_evidence": "GSE798_2 assumes choose F_prime(m_*)=0 and Taylor expands around a locked point",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "GSE798_2_local_locked_expansion",
            "result": "CONDITIONAL_EXPANSION_NOT_PARENT_LOCK",
            "blocks": "ADG1291_1_parent_lock;ADG1291_3_gradient_control",
            "next_action": "source parent local operator or keep m profile missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "FSM1292_2_norm_evenness_theorem",
            "target": "equivalent norm-square F source",
            "required_match": "F depends only on a parent-owned squared norm R_L=G_AB Z_L^A Z_L^B",
            "best_evidence": "DZ801_1 proves double zero if parent-signed; FPC801_2 gives even scalar readout contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_801_DOUBLE_ZERO_LEMMA.csv;source-intake/mts_residuals/P8_Y5_R10_801_PARENT_FIXED_POINT_CONTRACT.csv",
            "source_anchor": "DZ801_1_norm_evenness;FPC801_2_even_scalar_readout",
            "result": "MATHEMATICAL_THEOREM_IF_PARENT_SIGNED_NOT_ACTUAL_SOURCE",
            "blocks": "ADG1291_0_actual_F_form;ADG1291_5_current_MTS_match",
            "next_action": "do not adopt without parent signed Z_L/R_L map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "FSM1292_3_strict_F_verdict",
            "target": "strict double-zero adoption",
            "required_match": "all F-form source rows pass as actual MTS equations",
            "best_evidence": "strict form exists in 1291 as sufficient clause only",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv",
            "source_anchor": "SDZ1291_1_strict_F_form",
            "result": "STRICT_F_SOURCE_MATCH_FAILED_CURRENT_CORPUS",
            "blocks": "chain_zero_adoption",
            "next_action": "stage residual runner input rows from KRB1291",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    m_lcg_match = [
        {
            "match_id": "MLM1292_0_m_parent_definition",
            "target": "m parent definition",
            "required_match": "m is a parent-owned scalar or local fixed-point variable with Euler lock m=m_*",
            "best_evidence": "GSE798 uses m as input; GSE798_2 writes m=m_*+delta m conditionally",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "GSE798_0_definition;GSE798_2_local_locked_expansion",
            "result": "NAMED_SYMBOL_CONDITIONAL_LOCK_NO_PARENT_DEFINITION",
            "blocks": "MISSING_PARENT_DEFINITION_OF_m;MISSING_m_PROFILE",
            "next_action": "runner must keep m profile and F-prime bound missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MLM1292_1_m_marker_counterrisk",
            "target": "m not a readout/material marker",
            "required_match": "m is not a post-readout marker or metric composite",
            "best_evidence": "marker-dependence counterexample rows elsewhere keep m-like marker dependence legal unless no-marker theorem closes",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_987_EM_NORMAL_FORMS.csv",
            "source_anchor": "CEX980_1_theta_material_marker;EMNF987_2_marker_dependent_alpha",
            "result": "NO_MARKER_RISK_NOT_CLOSED",
            "blocks": "ADG1291_5_current_MTS_match",
            "next_action": "do not treat m as safe parent scalar without a no-marker/source theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MLM1292_2_Lcg_parent_definition",
            "target": "L_cg parent definition",
            "required_match": "L_cg is finite/safe parent scalar/global scale or action-derived transition scale",
            "best_evidence": "symbol/action-map rows say L_cg/ell_tr must be derived from spectrum/source/domain and is open",
            "source_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv;source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
            "source_anchor": "L_cg / ell_tr;FV512_6_transition_scale",
            "result": "LCG_PARENT_DEFINITION_OPEN",
            "blocks": "MISSING_PARENT_DEFINITION_OF_L_cg;MISSING_LCG_LOWER_BOUND",
            "next_action": "runner must keep L_cg lower-bound and M_L kernel bound missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MLM1292_3_transition_control",
            "target": "local/cosmology transition scale",
            "required_match": "ell_tr/L_cg or activation functional is action-derived, not arena-switched",
            "best_evidence": "FP511_8 marks local-cosmology transition control open",
            "source_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "source_anchor": "FP511_8_local_cosmology_transition_control",
            "result": "TRANSITION_CONTROL_OPEN",
            "blocks": "unification_gate_open;ADG1291_2_Lcg_finite_safe",
            "next_action": "keep L_cg as residual/source-match target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MLM1292_4_m_Lcg_verdict",
            "target": "m and L_cg adoption",
            "required_match": "both m and L_cg are source-backed parent variables with safe metric variation status",
            "best_evidence": "current inspected rows provide named symbols and contracts, not parent action definitions",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_ADOPTION_GATES.csv",
            "source_anchor": "ADG1291_1_parent_lock;ADG1291_2_Lcg_finite_safe",
            "result": "M_LCG_SOURCE_MATCH_FAILED_CURRENT_CORPUS",
            "blocks": "strict_double_zero_adoption",
            "next_action": "emit residual runner inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    adoption_verdict = [
        {
            "verdict_id": "SDA1292_0_F_form",
            "gate": "actual strict F source",
            "status": "FAIL_CURRENT_CORPUS",
            "evidence": "generic F(m) found; strict F=(m-m_*)^2H exists only as theorem target",
            "residual_if_fail": "KRB1291_0_m_chain_bound;KRB1291_1_Lcg_chain_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "verdict_id": "SDA1292_1_m_parent",
            "gate": "m parent lock/source profile",
            "status": "FAIL_CURRENT_CORPUS",
            "evidence": "m=m_*+delta m is conditional; no parent Euler lock/profile source found in inspected rows",
            "residual_if_fail": "MISSING_m_PROFILE;MISSING_F_PRIME_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "verdict_id": "SDA1292_2_Lcg_parent",
            "gate": "L_cg parent definition/safe lower bound",
            "status": "FAIL_CURRENT_CORPUS",
            "evidence": "L_cg/ell_tr action-map rows explicitly keep transition-scale ownership open",
            "residual_if_fail": "MISSING_LCG_LOWER_BOUND;MISSING_M_L_00_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "verdict_id": "SDA1292_3_boundary_gradient",
            "gate": "gradient and boundary/domain closure",
            "status": "FAIL_CURRENT_CORPUS",
            "evidence": "801 gradient warning and 1291 CDB residual rows remain open",
            "residual_if_fail": "MISSING_GRADIENT_POWER_PROOF;MISSING_K_CONN_DOMAIN_BOUNDARY_BOUNDS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "verdict_id": "SDA1292_4_overall",
            "gate": "strict double-zero adoption",
            "status": "NOT_ADOPTED_RESIDUAL_RUNNER_INPUT_REQUIRED",
            "evidence": "F, m, L_cg, gradient, and CDB gates fail current-corpus source-match",
            "residual_if_fail": "RRI1292_0..3",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_input = [
        {
            "runner_id": "RRI1292_0_m_chain",
            "branch": "chain_kernel_residual",
            "residual_component": "R_m^{00}",
            "prediction_form": "abs_R_m_00 <= abs(C_sign) * L_cg^-2 * abs(F_prime(m)) * abs(M_m_00)",
            "zero_condition": "strict source-matched F_prime(m_*)=0 or M_m_00=0 fixed-field scalar proof",
            "required_inputs": "MISSING_C_SIGN;MISSING_L_cg_VALUE;MISSING_m_PROFILE;MISSING_F_PRIME_BOUND;MISSING_M_m_00_BOUND;MISSING_RESPONSE_OPERATOR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "source_anchor": "KRB1291_0_m_chain_bound",
            "maps_to_tests": "Newton_source;PPN;clock;orbital;R10_if_range_component",
            "current_status": "RUNNER_INPUT_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RRI1292_1_Lcg_chain",
            "branch": "chain_kernel_residual",
            "residual_component": "R_L^{00}",
            "prediction_form": "abs_R_L_00 <= 2 * abs(C_sign) * L_cg^-3 * abs(F(m)) * abs(M_L_00)",
            "zero_condition": "strict source-matched F(m_*)=0, M_L_00=0 fixed-scale proof, or parent-owned background subtraction",
            "required_inputs": "MISSING_C_SIGN;MISSING_L_cg_VALUE;MISSING_LCG_LOWER_BOUND;MISSING_m_PROFILE;MISSING_F_BOUND;MISSING_M_L_00_BOUND;MISSING_RESPONSE_OPERATOR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "source_anchor": "KRB1291_1_Lcg_chain_bound",
            "maps_to_tests": "Newton_source;PPN;clock;orbital;source_normalization",
            "current_status": "RUNNER_INPUT_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RRI1292_2_cdb_chain",
            "branch": "connection_domain_boundary_residual",
            "residual_component": "R_cdb^{00}",
            "prediction_form": "abs_R_cdb_00 <= abs(K_conn_00)+abs(K_domain_00)+abs(K_boundary_00)",
            "zero_condition": "topological/projector metric-silence or no-flux boundary theorem",
            "required_inputs": "MISSING_K_CONN_BOUND;MISSING_K_DOMAIN_BOUND;MISSING_K_BOUNDARY_BOUND;MISSING_NO_FLUX_SOURCE;MISSING_RESPONSE_OPERATOR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "source_anchor": "KRB1291_2_cdb_bound",
            "maps_to_tests": "PPN;clock;orbital;boundary_mass_flux",
            "current_status": "RUNNER_INPUT_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RRI1292_3_chain_vector",
            "branch": "total_chain_kernel_residual",
            "residual_component": "R_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00}",
            "prediction_form": "abs_R_chain_00 <= abs_R_m_00 + abs_R_L_00 + abs_R_cdb_00",
            "zero_condition": "all strict double-zero adoption gates pass, or all component residual bounds are below arena response limits",
            "required_inputs": "MISSING_ALL_COMPONENT_INPUTS;MISSING_LOCAL_RESPONSE_LIMITS;MISSING_OBSERVABLE_RESPONSE_MATRIX",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "source_anchor": "KRB1291_3_residual_verdict",
            "maps_to_tests": "all_local",
            "current_status": "RUNNER_INPUT_TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1292_0_sources",
            "claim": "private source-match provenance",
            "current_status": "SATISFIED_FOR_PRIVATE_CHECKPOINT",
            "reason": "registered local source paths and anchors are validated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1292_1_strict_F_adoption",
            "claim": "strict F=(m-m*)^2H source-matched",
            "current_status": "BLOCKED_GENERIC_F_ONLY",
            "reason": "actual generic Gamma source exists, but strict F form is not sourced as current MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1292_2_m_Lcg_parent",
            "claim": "m and L_cg parent definitions are sourced",
            "current_status": "BLOCKED_PARENT_DEFINITIONS_MISSING",
            "reason": "m lock/profile and L_cg transition-scale ownership are still open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1292_3_residual_runner",
            "claim": "residual runner can score local tests",
            "current_status": "BLOCKED_INPUT_TEMPLATES_ONLY",
            "reason": "runner rows are schema-ready but still contain MISSING inputs and no response matrix",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1292_4_local_GR",
            "claim": "local GR/Newton/PPN recovery",
            "current_status": "BLOCKED_NONCLAIM",
            "reason": "strict adoption failed and residual runner inputs are not numeric/theorem complete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1292_0_source_match",
            "decision": "strict double-zero clause is not adopted from current corpus",
            "because": "the actual inspected Gamma row gives generic F(m), not F=(m-m_*)^2H",
            "next_action": "use residual runner inputs while continuing targeted source search if new files appear",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1292_1_residual_runner",
            "decision": "promote KRB1291 bounds into runner input templates",
            "because": "if the theorem target is not source-matched, the honest route is finite residual scoring",
            "next_action": "build the actual runner/validator that rejects rows until all MISSING inputs are filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1292_2_local_status",
            "decision": "local GR remains blocked but more executable",
            "because": "the missing theorem inputs are now translated into concrete runner fields",
            "next_action": "1293 should create chain-kernel residual runner schema and rejection smoke test",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1292_0_1293",
            "target_file": "1293-Y5-R10-RAB-chain-kernel-residual-runner-schema-and-rejection-smoke.md",
            "target_script": "scripts/Y5_R10_RAB_chain_kernel_residual_runner_schema_and_rejection_smoke.py",
            "task": "build a chain-kernel residual runner schema that consumes RRI1292 rows and rejects scoring until every theorem/numeric input and response operator is sourced",
            "success_condition": "runner input validation passes structurally, all current rows are explicitly rejected as nonclaim due to MISSING inputs, and no local-GR score is emitted",
            "do_not": "do not invent numeric m,L_cg,kernel,response values or use the strict double-zero clause as a current-MTS proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(SCAN_SUMMARY_PATH, scan_summary)
    write_csv(F_MATCH_PATH, f_match)
    write_csv(M_LCG_MATCH_PATH, m_lcg_match)
    write_csv(ADOPTION_VERDICT_PATH, adoption_verdict)
    write_csv(RUNNER_INPUT_PATH, runner_input)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1292_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    strict_scan = next(row for row in scan_summary if row["scan_id"] == "SCAN1292_0_strict_F_exact")
    validations.append(
        validation_row(
            "VAL1292_1_strict_F_not_found_as_actual_source",
            "strict F pattern is not found outside theorem-target generated rows",
            int(strict_scan["match_count"]) == 0,
            f"match_count={strict_scan['match_count']}",
        )
    )
    f_verdict = next(row for row in f_match if row["match_id"] == "FSM1292_3_strict_F_verdict")
    validations.append(
        validation_row(
            "VAL1292_2_F_match_failed_nonclaim",
            "F form source-match fails and remains nonclaim",
            f_verdict["result"] == "STRICT_F_SOURCE_MATCH_FAILED_CURRENT_CORPUS"
            and is_false(f_verdict["claim_allowed"]),
            "FSM1292_3_strict_F_verdict",
        )
    )
    ml_verdict = next(row for row in m_lcg_match if row["match_id"] == "MLM1292_4_m_Lcg_verdict")
    validations.append(
        validation_row(
            "VAL1292_3_m_Lcg_match_failed_nonclaim",
            "m and Lcg parent source-match fails and remains nonclaim",
            ml_verdict["result"] == "M_LCG_SOURCE_MATCH_FAILED_CURRENT_CORPUS"
            and is_false(ml_verdict["claim_allowed"]),
            "MLM1292_4_m_Lcg_verdict",
        )
    )
    overall_adoption = next(row for row in adoption_verdict if row["verdict_id"] == "SDA1292_4_overall")
    validations.append(
        validation_row(
            "VAL1292_4_adoption_rejected_to_runner",
            "strict double-zero adoption is rejected into residual runner input",
            overall_adoption["status"] == "NOT_ADOPTED_RESIDUAL_RUNNER_INPUT_REQUIRED"
            and is_false(overall_adoption["claim_allowed"]),
            "SDA1292_4_overall",
        )
    )
    runner_ok = all("MISSING_" in row["required_inputs"] and row["current_status"] == "RUNNER_INPUT_TEMPLATE_NONCLAIM_MISSING_INPUTS" for row in runner_input)
    validations.append(
        validation_row(
            "VAL1292_5_runner_inputs_nonclaim_missing",
            "all residual runner input rows are nonclaim and missing required inputs",
            runner_ok and all(is_false(row["claim_allowed"]) for row in runner_input),
            f"runner_rows={len(runner_input)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1292_6_claim_gates_blocked",
            "claim gates block local GR/PPN promotion",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        SCAN_SUMMARY_PATH,
        F_MATCH_PATH,
        M_LCG_MATCH_PATH,
        ADOPTION_VERDICT_PATH,
        RUNNER_INPUT_PATH,
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
    validations.append(validation_row("VAL1292_7_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1292_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1292_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, scan_summary, f_match, m_lcg_match, adoption_verdict, runner_input, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1292_10_next_target_1293",
            "next target routes to residual runner schema and rejection smoke",
            next_target[0]["next_id"] == "NEXT1292_0_1293" and "runner schema" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1292_11_overall",
            "overall 1292 validation",
            overall_pass,
            "1292 fails current-corpus source-match for strict F/m/Lcg adoption, emits nonclaim residual runner inputs, and routes to a rejection-smoke runner",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1292 Y5 R10 RAB F-form and m/Lcg parent source-match or residual runner input

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1292 does **not** find an actual current-corpus source for adopting the strict `F(m)=(m-m_*)^2H(m)` clause. The corpus has a generic `Gamma_eff=L_cg^-2 F(m)` row and conditional double-zero theorems, but not a source-backed actual `F`, parent lock for `m=m_*`, or parent definition of `L_cg`.

**Main progress:** the theorem target is now connected to an executable fallback. Since source-match fails, the `m`, `L_cg`, and connection/domain/boundary residuals are converted into runner input rows with explicit missing fields. This keeps the route testable instead of becoming a decorative closure.

**Next derivation target:** build a residual runner schema that consumes the `RRI1292` rows and refuses to score until all theorem/numeric inputs and response operators are sourced.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Source-Match Scan Summary

{markdown_table(scan_summary, ["scan_id", "pattern", "scope", "match_count", "matched_files", "interpretation", "valid_for_claim", "claim_allowed"])}

## F Form Source-Match Audit

{markdown_table(f_match, ["match_id", "target", "required_match", "best_evidence", "source_path", "source_anchor", "result", "blocks", "next_action", "valid_for_claim", "claim_allowed"])}

## m/Lcg Parent Source-Match Audit

{markdown_table(m_lcg_match, ["match_id", "target", "required_match", "best_evidence", "source_path", "source_anchor", "result", "blocks", "next_action", "valid_for_claim", "claim_allowed"])}

## Strict Double-Zero Adoption Verdict

{markdown_table(adoption_verdict, ["verdict_id", "gate", "status", "evidence", "residual_if_fail", "valid_for_claim", "claim_allowed"])}

## Chain-Kernel Residual Runner Input

{markdown_table(runner_input, ["runner_id", "branch", "residual_component", "prediction_form", "zero_condition", "required_inputs", "source_path", "source_anchor", "maps_to_tests", "current_status", "valid_for_claim", "claim_allowed"])}

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
