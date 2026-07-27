from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1276"
TITLE = "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ACTION_COVERAGE_PATH = OUT_DIR / f"{PACK_ID}_A511_ACTION_BLOCK_COVERAGE.csv"
EULER_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_EULER_SOURCE_CONTRACT.csv"
CLOSURE_SCORECARD_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_BASELINE_SCORECARD.csv"
PROMOTION_GATES_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_GATES.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1276_VALIDATION.csv"


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
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source_raw = str(row.get("source_path", "")).strip()
    anchor = str(row.get("source_anchor", "")).strip()
    source = None if not source_raw or source_raw.startswith("MISSING_") else source_path(source_raw)
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1276_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        ACTION_COVERAGE_PATH,
        EULER_CONTRACT_PATH,
        CLOSURE_SCORECARD_PATH,
        PROMOTION_GATES_PATH,
        VALIDATOR_RESCAN_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1276_0_1275_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1275_NEXT_TARGET.csv",
            "needle": "NEXT1275_0_1276",
            "purpose": "handoff into parent Euler/source-map contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_1_1275_missing",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1275_MISSING_PARENT_EULER_SOURCE_MAP.csv",
            "needle": "MPE1275_0_Lcore",
            "purpose": "missing parent Euler/source objects from 1275",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_2_1275_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1275_LOCAL_CLOSURE_BASELINE.csv",
            "needle": "LCB1275_0_assumption",
            "purpose": "closure baseline rows to score without promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_3_A511_blocks",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "A511_0_EH_core",
            "purpose": "candidate minimum parent local-GR action block scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_4_symbol_map",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "g_obs / g_readout",
            "purpose": "symbol-to-action placement map for local GR branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_5_zero_chain",
            "local_path": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
            "needle": "V5_delta_g_stress",
            "purpose": "local-zero variation chain and remaining metric-stress debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_6_import_guard",
            "local_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "if MTS simply imports G^t_t = G^r_r",
            "purpose": "no-GR-import warning for equation-difference route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_7_strain_contract",
            "local_path": "04-vacuum-reciprocity-action-contract.md",
            "needle": "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R",
            "purpose": "second-order reciprocal-strain parent theorem contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_8_1268_aux",
            "local_path": "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            "needle": "CAC1268_5_conditional_theorem",
            "purpose": "conditional auxiliary theorem remains unpromoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1276_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    action_coverage = [
        {
            "coverage_id": "AC1276_0_EH_core",
            "block_id": "A511_0_EH_core",
            "covers": "local spin-2 metric Euler equations if the EH core is parent-inherited",
            "helps_contract": "E_time/E_radial and GR-style D_R can be obtained after EH inheritance",
            "current_status": "CANDIDATE_REFERENCE_NOT_MTS_DERIVED",
            "remaining_gap": "prove MTS local fixed point reduces to EH core without simply importing GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coverage_id": "AC1276_1_kappa_topological",
            "block_id": "A511_1_kappa_topological",
            "covers": "constant local gravitational coupling/source normalization",
            "helps_contract": "prevents G_eff drift from contaminating the D_R/source map",
            "current_status": "CANDIDATE_NOT_ADOPTED_AS_PARENT_THEOREM",
            "remaining_gap": "derive topological kappa clause or retain drift residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coverage_id": "AC1276_2_universal_matter",
            "block_id": "A511_2_universal_matter",
            "covers": "same observed metric/coframe for matter and clocks",
            "helps_contract": "defines Hilbert source current and source-balance condition",
            "current_status": "CONTRACT_ANCHOR_NOT_SOURCE_MAP_DERIVED",
            "remaining_gap": "prove universal matter descent and same-frame source measure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coverage_id": "AC1276_3_extra_silence",
            "block_id": "A511_3_extra_field_silence",
            "covers": "motion/time/domain/memory/range fields silent in local branch",
            "helps_contract": "removes extra stress terms from S_R[source,residual]",
            "current_status": "OPEN",
            "remaining_gap": "derive double-zero/Hessian/source silence for all retained extra fields",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coverage_id": "AC1276_4_projector_selector",
            "block_id": "A511_4_domain_projector_selector",
            "covers": "domain/projector variables before local readout",
            "helps_contract": "prevents preferred-frame/source-normalization leakage into E_time-E_radial",
            "current_status": "OPEN",
            "remaining_gap": "derive local stationary compact branch X_D=0,Qcoh_D=0,projector stress=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coverage_id": "AC1276_5_boundary_reference",
            "block_id": "A511_5_boundary_reference",
            "covers": "Hamiltonian/reference subtraction and boundary flux class",
            "helps_contract": "needed for Q_R=0 and C_R normalization after integration",
            "current_status": "OPEN",
            "remaining_gap": "prove boundary variation vanishes or is fixed topological constant",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coverage_id": "AC1276_6_metric_readout",
            "block_id": "A511_6_metric_readout",
            "covers": "observed metric and mass projector readout",
            "helps_contract": "prevents first-order extra-field leakage into Newton/PPN/R10 readout",
            "current_status": "OPEN",
            "remaining_gap": "prove readout stability and Pi_M=Pi_EH+silent higher order",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    euler_contract = [
        {
            "contract_id": "ESC1276_0_field_variables",
            "needed_certificate": "parent field/readout list",
            "contract_expression": "Phi_parent -> {g_obs/coframe, T,S or u,v, matter psi, extra/projector/boundary fields}",
            "current_evidence": "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "status": "PARTIAL_MAP_NOT_PARENT_SIGNED",
            "promotes_local_GR_if": "field list is parent-owned and local readout order is fixed before closure selection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_1_local_EH_fixed_point",
            "needed_certificate": "MTS -> local EH fixed point",
            "contract_expression": "S_parent|local = S_EH[g_obs,kappa0] + S_matter[psi,g_obs] + silent/topological extras + boundary",
            "current_evidence": "A511_0..A511_6 candidate action blocks",
            "status": "CANDIDATE_NOT_DERIVED",
            "promotes_local_GR_if": "all A511 blocks are parent-derived and all extra first variations vanish or are source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_2_E_time",
            "needed_certificate": "time/lapse Euler equation",
            "contract_expression": "E_time := delta S_parent / delta ln(T) or equivalent tt/coframe equation",
            "current_evidence": "not extracted",
            "status": "MISSING_EULER_EQUATION",
            "promotes_local_GR_if": "explicit equation is derived from S_parent, not copied from Einstein equations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_3_E_radial",
            "needed_certificate": "radial routing Euler equation",
            "contract_expression": "E_radial := delta S_parent / delta ln(sqrt(S)) or equivalent rr/coframe equation",
            "current_evidence": "not extracted",
            "status": "MISSING_EULER_EQUATION",
            "promotes_local_GR_if": "explicit radial equation is derived from S_parent with all MTS residual terms shown",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_4_difference_operator",
            "needed_certificate": "D_R equation-difference",
            "contract_expression": "D_R[MTS] := E_time - E_radial = partial_r C_R - S_R[source,residual,boundary] = 0",
            "current_evidence": "1275 writes target form only",
            "status": "CONTRACT_ONLY",
            "promotes_local_GR_if": "D_R is algebraically derived from ESC1276_2 and ESC1276_3",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_5_source_map",
            "needed_certificate": "source-balance map",
            "contract_expression": "S_R = S_time_minus_radial + S_extra + S_projector + S_boundary + S_readout",
            "current_evidence": "06 identifies anisotropic/radial routing stress source; A511 rows identify source sectors",
            "status": "MISSING_SOURCE_MAP",
            "promotes_local_GR_if": "local vacuum/source-balance proves S_R=0 without hiding residual terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_6_operator_positive_or_first_order",
            "needed_certificate": "operator sign/order",
            "contract_expression": "either partial_r C_R=S_R or partial_r(W partial_r C_R)=J_R with W>0",
            "current_evidence": "04 contract supplies W form but not parent derivation",
            "status": "UNSIGNED_OPERATOR",
            "promotes_local_GR_if": "operator follows from S_parent and W positivity/no ghost clauses are signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_7_boundary_no_charge",
            "needed_certificate": "boundary/no-hair normalization",
            "contract_expression": "Q_R=0 and C_R(infinity)=0 or equivalent matching",
            "current_evidence": "1275 closure baseline labels this as an assumption",
            "status": "CLOSURE_ONLY_CURRENTLY",
            "promotes_local_GR_if": "boundary/reference class derives Q_R=0 and fixes integration constant",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_8_no_EH_import",
            "needed_certificate": "EH import guard",
            "contract_expression": "EH equations may be used only after ESC1276_1 proves EH local fixed point",
            "current_evidence": "03 warns against importing G^t_t=G^r_r",
            "status": "REQUIRED_GUARD",
            "promotes_local_GR_if": "proof path states whether D_R is inherited from derived EH fixed point or newly derived from MTS action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ESC1276_9_verdict",
            "needed_certificate": "parent Euler/source contract closure",
            "contract_expression": "ESC1276_0..8 pass -> C_R=0 theorem; otherwise closure-only or finite residual rows",
            "current_evidence": "this 1276 contract",
            "status": "EXECUTABLE_CONTRACT_NOT_DERIVATION",
            "promotes_local_GR_if": "all certificates become parent-signed or source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_scorecard = [
        {
            "score_id": "CS1276_0_C_R_zero",
            "closure_baseline_id": "LCB1275_0_assumption",
            "assumption": "C_R=R_AB=ln(T^2S)=0",
            "safe_internal_use": "benchmark/control branch for local tests",
            "claim_risk": "would fake derived GR reduction if unlabeled",
            "score": "SAFE_NONCLAIM_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "CS1276_1_no_charge",
            "closure_baseline_id": "LCB1275_1_no_charge",
            "assumption": "Q_R=0, boundary_u=0, readout_regen_u=0",
            "safe_internal_use": "prevents hidden-hair benchmark branch",
            "claim_risk": "boundary/no-hair theorem remains unproved",
            "score": "SAFE_NONCLAIM_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "CS1276_2_source_balance",
            "closure_baseline_id": "LCB1275_2_source_balance",
            "assumption": "S_R[source,residual]=0",
            "safe_internal_use": "local vacuum/source-balance control",
            "claim_risk": "arbitrary matter/interior branch would be overclaimed",
            "score": "SAFE_NONCLAIM_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "CS1276_3_boundary",
            "closure_baseline_id": "LCB1275_3_boundary",
            "assumption": "C_R(infinity)=0 or matching fixes constant",
            "safe_internal_use": "normalization bookkeeping",
            "claim_risk": "normalization is not a dynamical equation",
            "score": "SAFE_NONCLAIM_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "CS1276_4_overall",
            "closure_baseline_id": "LCB1275_all",
            "assumption": "local closure branch = C_R=0 + no-charge + source-balance + boundary normalization",
            "safe_internal_use": "explicitly labelled closure/control route",
            "claim_risk": "not evidence that MTS reduces to GR",
            "score": "CLOSURE_BASELINE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    promotion_gates = [
        {
            "gate_id": "PG1276_0_EH_fixed_point",
            "gate": "MTS derives local EH fixed point",
            "required_evidence": "A511_0..A511_6 parent-signed with silent extras",
            "status": "BLOCKED",
            "reason": "A511 blocks are candidate scaffold, not derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "PG1276_1_Euler_pair",
            "gate": "E_time and E_radial are extracted",
            "required_evidence": "explicit variation of S_parent with respect to T/S or u/v",
            "status": "BLOCKED",
            "reason": "no parent Euler pair exists yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "PG1276_2_D_R_source_map",
            "gate": "D_R and S_R are derived",
            "required_evidence": "E_time-E_radial algebra and full source/residual decomposition",
            "status": "BLOCKED",
            "reason": "source map is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "PG1276_3_boundary_no_charge",
            "gate": "boundary/no-charge normalization closes",
            "required_evidence": "Q_R=0 and integration constant fixed by parent boundary class",
            "status": "BLOCKED",
            "reason": "currently closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "PG1276_4_closure_baseline",
            "gate": "closure branch is clearly separated from claims",
            "required_evidence": "closure scorecard labels all assumptions nonclaim",
            "status": "PASS_NONCLAIM",
            "reason": "closure baseline is safe for internal controls only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "PG1276_5_finite_residual",
            "gate": "finite residual rows are source-ready",
            "required_evidence": "raw/accepted finite Z_R rows pass validator",
            "status": "BLOCKED",
            "reason": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1276_0_contract_written",
            "decision": "turn missing Euler/source map into executable certificate rows",
            "because": "1275 showed the GR-style route fails only because the parent action/source certificates are absent",
            "status": "CONTRACT_WRITTEN_NOT_CLOSED",
            "next_action": "attempt local EH fixed-point inheritance from A511 blocks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1276_1_best_derivation_route",
            "decision": "try EH local fixed-point inheritance before giving up to closure-only",
            "because": "if MTS derives an EH local effective action plus silent extras, the GR equation-difference becomes legitimate rather than smuggled",
            "status": "EH_FIXED_POINT_ROUTE_SELECTED",
            "next_action": "prove or reject A511_0..A511_6 as parent-signed local fixed point",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1276_2_closure_discipline",
            "decision": "keep the local closure branch as an explicit nonclaim benchmark",
            "because": "closure is useful for testing but cannot stand in for the derivation",
            "status": "CLOSURE_SCORECARD_INSTALLED",
            "next_action": "future tests must state closure baseline versus finite residual branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1276_0_1277",
            "target_file": "1277-Y5-R10-RAB-local-EH-fixed-point-inheritance-or-explicit-closure-runner.md",
            "target_script": "scripts/Y5_R10_RAB_local_EH_fixed_point_inheritance_or_explicit_closure_runner.py",
            "task": "try to prove that A511_0..A511_6 are parent-signed so MTS inherits the local EH Euler equations and the GR-style D_R relation; if this fails, keep the local branch as an explicit closure runner with finite residual rows locked",
            "success_condition": "local EH fixed point plus silent extra sectors is parent-signed, or the closure-only status is executable and separated from finite residual scoring",
            "do_not": "do not treat the A511 scaffold as proof merely because it contains an EH core block",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (ACTION_COVERAGE_PATH, action_coverage),
        (EULER_CONTRACT_PATH, euler_contract),
        (CLOSURE_SCORECARD_PATH, closure_scorecard),
        (PROMOTION_GATES_PATH, promotion_gates),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    all_action_blocks_covered = {row["block_id"] for row in action_coverage} == {
        "A511_0_EH_core",
        "A511_1_kappa_topological",
        "A511_2_universal_matter",
        "A511_3_extra_field_silence",
        "A511_4_domain_projector_selector",
        "A511_5_boundary_reference",
        "A511_6_metric_readout",
    }
    contract_written = any(
        row["contract_id"] == "ESC1276_9_verdict" and row["status"] == "EXECUTABLE_CONTRACT_NOT_DERIVATION"
        for row in euler_contract
    )
    closure_safe = len(closure_scorecard) == 5 and all(row["score"] in {"SAFE_NONCLAIM_ONLY", "CLOSURE_BASELINE_ONLY"} for row in closure_scorecard)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} for row in promotion_gates)
    no_claim_promoted = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] == "PG1276_4_closure_baseline"
        for row in promotion_gates
    )
    all_generated_rows = [
        *source_register,
        *action_coverage,
        *euler_contract,
        *closure_scorecard,
        *promotion_gates,
        *validator_rescan,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1276_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1276_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1276_2_action_coverage",
            "all A511 local-GR action blocks are covered",
            all_action_blocks_covered,
            f"action_coverage_rows={len(action_coverage)}",
        ),
        validation_row(
            "VAL1276_3_euler_contract",
            "Euler/source-map contract is executable but not a derivation",
            contract_written and len(euler_contract) >= 10,
            f"euler_contract_rows={len(euler_contract)}",
        ),
        validation_row(
            "VAL1276_4_closure_scorecard",
            "closure baseline is separated as nonclaim",
            closure_safe,
            f"closure_scorecard_rows={len(closure_scorecard)}",
        ),
        validation_row(
            "VAL1276_5_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1276_6_promotion_gates",
            "promotion gates remain blocked except closure-baseline nonclaim gate",
            gates_safe and no_claim_promoted,
            f"promotion_gate_rows={len(promotion_gates)}",
        ),
        validation_row(
            "VAL1276_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1276_8_next_target_1277",
            "next target routes to local EH fixed-point inheritance or explicit closure runner",
            next_target[0]["next_id"] == "NEXT1276_0_1277",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1276_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1276_10_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1276_11_overall",
            "overall 1276 validation",
            overall_pass,
            "1276 turns the missing MTS parent Euler/source map into executable certificate rows, covers the A511 action-block scaffold, keeps the closure baseline nonclaim, and routes to local EH fixed-point inheritance next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1276 does not derive the `E_time - E_radial` equation, but it makes the missing route executable. The least-ad-hoc path is now: prove MTS has a parent-signed local EH fixed point using the A511 action blocks, then inherit the GR-style radial equation difference only after all extra sectors, coupling drift, boundary terms, and readout leakage are silent.

**Main progress:** the project now has a clean contract instead of a vague gap. The local closure baseline is separated from the derivation route, and every certificate needed to promote `C_R=ln(T^2S)=0` is listed as a row that can be attacked or refused.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, zero-residual, or finite-`Z_R` row is claimed. The A511 scaffold is not treated as proof merely because it contains an EH core.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## A511 Action Block Coverage
{markdown_table(action_coverage, ["coverage_id", "block_id", "covers", "helps_contract", "current_status", "remaining_gap", "valid_for_claim", "claim_allowed"])}

## Parent Euler/Source Contract
{markdown_table(euler_contract, ["contract_id", "needed_certificate", "contract_expression", "current_evidence", "status", "promotes_local_GR_if", "valid_for_claim", "claim_allowed"])}

## Closure Baseline Scorecard
{markdown_table(closure_scorecard, ["score_id", "closure_baseline_id", "assumption", "safe_internal_use", "claim_risk", "score", "valid_for_claim", "claim_allowed"])}

## Promotion Gates
{markdown_table(promotion_gates, ["gate_id", "gate", "required_evidence", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
