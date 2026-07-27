from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1275"
TITLE = "1275-Y5-R10-RAB-GR-style-radial-field-equation-difference-or-local-closure-baseline"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
GR_PATTERN_PATH = OUT_DIR / f"{PACK_ID}_GR_PATTERN_IMPORT_GUARD.csv"
EQUATION_DIFF_PATH = OUT_DIR / f"{PACK_ID}_MTS_EQUATION_DIFFERENCE_ATTEMPT.csv"
CLOSURE_BASELINE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_CLOSURE_BASELINE.csv"
MISSING_PARENT_PATH = OUT_DIR / f"{PACK_ID}_MISSING_PARENT_EULER_SOURCE_MAP.csv"
FINITE_DECISION_PATH = OUT_DIR / f"{PACK_ID}_FINITE_RESIDUAL_DECISION.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1275_VALIDATION.csv"


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
        "scan_id": f"SCAN1275_{intake_class}_{path.stem}_{row_id}",
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
        GR_PATTERN_PATH,
        EQUATION_DIFF_PATH,
        CLOSURE_BASELINE_PATH,
        MISSING_PARENT_PATH,
        FINITE_DECISION_PATH,
        VALIDATOR_RESCAN_PATH,
        CLAIM_GATES_PATH,
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
            "source_id": "SRC1275_0_1274_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1274_NEXT_TARGET.csv",
            "needle": "NEXT1274_0_1275",
            "purpose": "handoff into GR-style equation-difference attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_1_1274_gr_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1274_GR_STYLE_EQUATION_DIFFERENCE_ROUTE.csv",
            "needle": "GED1274_4_best_next_test",
            "purpose": "selected equation-difference route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_2_parent_origin",
            "local_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "if MTS simply imports G^t_t = G^r_r",
            "purpose": "guard against importing GR stress-balance equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_3_contract",
            "local_path": "04-vacuum-reciprocity-action-contract.md",
            "needle": "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R",
            "purpose": "existing reciprocal-strain equation contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_4_theorem_attempt",
            "local_path": "05-reciprocity-theorem-attempt.md",
            "needle": "S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].",
            "purpose": "finite reciprocal-strain action leaves charge/source clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_5_source_neutrality",
            "local_path": "06-reciprocal-charge-source-neutrality.md",
            "needle": "anisotropic/radial routing stress source",
            "purpose": "source neutrality and anisotropy gap",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_6_radial_closure",
            "local_path": "555-Y5-radial-closure-Cterm-zero-or-first-Hamiltonian-residual-fill.md",
            "needle": "the GR/EH annulus closure route remains the target structure",
            "purpose": "GR/EH closure route kept as benchmark but not inherited",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_7_1268_action",
            "local_path": "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            "needle": "CAC1268_5_conditional_theorem",
            "purpose": "auxiliary exact route remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_8_1248_dirac",
            "local_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "needle": "DIR1248_2_preservation",
            "purpose": "parent H_core preservation still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1275_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    gr_pattern = [
        {
            "pattern_id": "GRP1275_0_static_spherical_pattern",
            "structural_pattern": "in static areal spherical GR, the time-radial field-equation difference gives an AB relation in vacuum/source-balanced cases",
            "permitted_use": "benchmark structure only",
            "forbidden_use": "do not import G^t_t=G^r_r as an MTS parent equation",
            "MTS_requirement": "derive an MTS-owned D_R equation from L_MTS_core/Euler data",
            "status": "REFERENCE_ONLY_NOT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pattern_id": "GRP1275_1_target_variable",
            "structural_pattern": "C_R := ln(AB)=ln(T^2S)",
            "permitted_use": "same target variable as earlier R_AB/u work",
            "forbidden_use": "do not set C_R=0 by naming the GR solution",
            "MTS_requirement": "produce D_R[MTS] involving C_R and MTS source terms",
            "status": "TARGET_DEFINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pattern_id": "GRP1275_2_source_balance",
            "structural_pattern": "AB=1 requires vacuum/source-balance plus boundary normalization, not arbitrary matter",
            "permitted_use": "define the source gate explicitly",
            "forbidden_use": "hide anisotropic radial stress or residual source terms",
            "MTS_requirement": "identify S_R[source]=0 conditions in MTS variables",
            "status": "SOURCE_GATE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    equation_diff = [
        {
            "attempt_id": "EDA1275_0_contract_form",
            "MTS_object": "radial reciprocity/equation-difference target",
            "candidate_equation": "D_R[MTS] := E_time - E_radial = partial_r C_R - S_R[source,residual,boundary] = 0",
            "derivation_status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "blocker": "E_time and E_radial have not been derived from L_MTS_core",
            "if_closed": "S_R=0 and boundary normalization imply C_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EDA1275_1_existing_second_order_contract",
            "MTS_object": "reciprocal-strain action contract from 04/05",
            "candidate_equation": "partial_r[W(r,L,fields) partial_r C_R] = J_R",
            "derivation_status": "CONDITIONAL_CONTRACT_ONLY",
            "blocker": "W positivity, J_R=0, and finite/no-charge exterior flux are not parent-signed",
            "if_closed": "with W>0, J_R=0, Q_R=0, and C_R(infinity)=0, C_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EDA1275_2_direct_MTS_Euler_attempt",
            "MTS_object": "derive D_R from motion/time/space parent action",
            "candidate_equation": "delta_T S_parent and delta_S S_parent combine into a C_R equation",
            "derivation_status": "FAIL_CURRENT_CORPUS",
            "blocker": "no explicit L_MTS_core, variational field list, or T/S Euler equations are available in this branch",
            "if_closed": "would be the desired noncircular local GR reduction route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EDA1275_3_source_balance_attempt",
            "MTS_object": "MTS source difference replacing radial/time stress balance",
            "candidate_equation": "S_R = source_time_minus_radial + residual_projector + boundary_readout",
            "derivation_status": "FAIL_CURRENT_CORPUS",
            "blocker": "source neutrality/aniso-radial stress is identified but not derived as zero",
            "if_closed": "local vacuum/source-balanced branch could set S_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EDA1275_4_boundary_normalization",
            "MTS_object": "constant or integrated charge after D_R",
            "candidate_equation": "C_R=constant or W partial_r C_R=Q_R",
            "derivation_status": "FAIL_CURRENT_CORPUS",
            "blocker": "boundary/no-charge theorem is not parent-signed",
            "if_closed": "C_R(infinity)=0 and Q_R=0 would fix AB=1",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EDA1275_5_verdict",
            "MTS_object": "GR-style MTS radial equation-difference derivation",
            "candidate_equation": "D_R[MTS] -> partial_r ln(T^2S)=S_R -> local AB=1",
            "derivation_status": "NOT_DERIVED",
            "blocker": "parent Euler equations/source map/boundary no-charge are missing",
            "if_closed": "local exact branch could reopen",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_baseline = [
        {
            "baseline_id": "LCB1275_0_assumption",
            "closure_item": "local reciprocity closure",
            "assumption": "C_R=R_AB=ln(T^2S)=0 on the local vacuum benchmark branch",
            "purpose": "control baseline for comparing local Newton/PPN/R10/clocks/orbits while derivation remains open",
            "claim_status": "CLOSURE_ONLY_NOT_DERIVED",
            "allowed_use": "internal benchmark and code/control comparison only",
            "forbidden_use": "do not call it parent-derived local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "baseline_id": "LCB1275_1_no_charge",
            "closure_item": "reciprocal no-hair closure",
            "assumption": "Q_R=0, boundary_u=0, readout_regen_u=0",
            "purpose": "prevents the closure benchmark from carrying hidden reciprocal hair",
            "claim_status": "CLOSURE_ONLY_NOT_DERIVED",
            "allowed_use": "explicitly labelled local closure baseline",
            "forbidden_use": "do not hide finite residuals under the closure label",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "baseline_id": "LCB1275_2_source_balance",
            "closure_item": "local vacuum/source-balance closure",
            "assumption": "S_R[source,residual]=0",
            "purpose": "records the source condition that a future parent equation must derive",
            "claim_status": "CLOSURE_ONLY_NOT_DERIVED",
            "allowed_use": "baseline branch only",
            "forbidden_use": "do not apply to arbitrary matter/interiors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "baseline_id": "LCB1275_3_boundary",
            "closure_item": "normalization closure",
            "assumption": "C_R(infinity)=0 or equivalent local matching fixes the integration constant",
            "purpose": "separates equation-derived constant AB from normalized AB=1",
            "claim_status": "CLOSURE_ONLY_NOT_DERIVED",
            "allowed_use": "internal branch bookkeeping",
            "forbidden_use": "do not use boundary choice as a derivation of D_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    missing_parent = [
        {
            "missing_id": "MPE1275_0_Lcore",
            "needed_object": "explicit L_MTS_core/H_core",
            "why_needed": "derive E_time and E_radial rather than importing Einstein equations",
            "current_status": "MISSING",
            "next_action": "assemble minimum parent action/source map or keep closure baseline",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "missing_id": "MPE1275_1_Euler_pair",
            "needed_object": "E_time and E_radial equations for T/S or u/v",
            "why_needed": "compute D_R[MTS]=E_time-E_radial",
            "current_status": "MISSING",
            "next_action": "write symbolic Euler contract with source terms and certificates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "missing_id": "MPE1275_2_source_map",
            "needed_object": "MTS analogue of radial/time stress-source difference",
            "why_needed": "define exactly when local vacuum/source-balance gives S_R=0",
            "current_status": "MISSING",
            "next_action": "map matter/projector/boundary/readout sources into S_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "missing_id": "MPE1275_3_W_positive",
            "needed_object": "positive reciprocal operator coefficient W",
            "why_needed": "second-order contract needs elliptic sign to derive no residual mode",
            "current_status": "UNSIGNED",
            "next_action": "derive W from parent action or source finite coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "missing_id": "MPE1275_4_boundary_no_charge",
            "needed_object": "Q_R=0 / boundary no-hair theorem",
            "why_needed": "integrating D_R or strain equation leaves constants/charges otherwise",
            "current_status": "UNSIGNED",
            "next_action": "derive boundary class or retain closure baseline",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "missing_id": "MPE1275_5_import_guard",
            "needed_object": "no-EH-import certificate",
            "why_needed": "ensure GR equations are only a benchmark pattern",
            "current_status": "REQUIRED",
            "next_action": "mark any EH formula as reference-only until MTS derivation exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    finite_decision = [
        {
            "finite_id": "FRD1275_0_no_finite_rows",
            "trigger": "equation-difference derivation fails current corpus",
            "needed_rows": "W/Z_R, J_R/source_difference, Q_R/boundary, tau_R10, tau_PPN, tau_clock, tau_orbital",
            "current_status": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "action_taken": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "reason": "no source-backed finite residual coefficients exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "finite_id": "FRD1275_1_closure_vs_finite",
            "trigger": "local exact branch demoted to closure baseline",
            "needed_rows": "source-backed finite rows before any scored residual branch",
            "current_status": "FALLBACK_LOCKED",
            "action_taken": "no row created",
            "reason": "closure baseline and finite residual branch must not be mixed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1275_0_GR_difference_derived",
            "claim": "MTS derives GR-style time-radial equation difference",
            "status": "BLOCKED",
            "reason": "parent E_time/E_radial equations are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1275_1_local_exact_branch",
            "claim": "local GR reciprocity is parent-derived",
            "status": "BLOCKED",
            "reason": "D_R/source/boundary gates are not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1275_2_closure_baseline",
            "claim": "local closure baseline is explicitly recorded",
            "status": "PASS_NONCLAIM",
            "reason": "C_R=0/Q_R=0/source-balance/boundary assumptions are labelled closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1275_3_finite_branch",
            "claim": "finite residual rows can be scored",
            "status": "BLOCKED",
            "reason": "no source-backed accepted rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1275_4_local_tests",
            "claim": "R10/PPN/clock/orbital/local-GR pass",
            "status": "BLOCKED",
            "reason": "closure baseline is not a derivation and finite residuals are not sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1275_0_equation_diff_result",
            "decision": "do not claim the GR-style equation-difference route as derived",
            "because": "current corpus lacks the MTS parent Euler pair and source map",
            "status": "DERIVATION_FAILED_CURRENT_CORPUS",
            "next_action": "assemble the parent Euler/source-map contract explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1275_1_closure_baseline",
            "decision": "record C_R=0 as a local closure baseline only",
            "because": "it remains useful as a control branch, but not as evidence of derived GR reduction",
            "status": "CLOSURE_BASELINE_WRITTEN",
            "next_action": "keep closure labels in any future local tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1275_2_next_route",
            "decision": "build the minimum parent Euler/source-map contract next",
            "because": "this is the exact missing object needed to turn the GR-shaped route into an MTS derivation",
            "status": "NEXT_CONTRACT_SELECTED",
            "next_action": "define E_time, E_radial, S_R, W, Q_R, and no-EH-import certificates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1275_0_1276",
            "target_file": "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            "target_script": "scripts/Y5_R10_RAB_parent_Euler_source_map_contract_or_closure_baseline_scorecard.py",
            "task": "assemble the minimum parent Euler/source-map contract required to derive D_R[MTS]=E_time-E_radial and separate it from the explicit local closure baseline; if no parent action pieces exist, produce a closure-baseline scorecard without claim promotion",
            "success_condition": "the missing MTS Euler/source certificates are made executable as rows, or the local branch remains explicitly closure-only with finite residual intake locked",
            "do_not": "do not use the closure baseline as evidence that MTS has reduced to GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (GR_PATTERN_PATH, gr_pattern),
        (EQUATION_DIFF_PATH, equation_diff),
        (CLOSURE_BASELINE_PATH, closure_baseline),
        (MISSING_PARENT_PATH, missing_parent),
        (FINITE_DECISION_PATH, finite_decision),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    import_guard_present = any(row["pattern_id"] == "GRP1275_0_static_spherical_pattern" and row["status"] == "REFERENCE_ONLY_NOT_PROOF" for row in gr_pattern)
    equation_not_derived = any(row["attempt_id"] == "EDA1275_5_verdict" and row["derivation_status"] == "NOT_DERIVED" for row in equation_diff)
    closure_written = len(closure_baseline) >= 4 and all(row["claim_status"] == "CLOSURE_ONLY_NOT_DERIVED" for row in closure_baseline)
    parent_map_missing = len(missing_parent) >= 6 and all(row["valid_for_claim"] is False for row in missing_parent)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    finite_locked = any(row["finite_id"] == "FRD1275_1_closure_vs_finite" and row["current_status"] == "FALLBACK_LOCKED" for row in finite_decision)
    claim_gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} for row in claim_gates)
    no_claim_promoted = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] == "GATE1275_2_closure_baseline"
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *gr_pattern,
        *equation_diff,
        *closure_baseline,
        *missing_parent,
        *finite_decision,
        *validator_rescan,
        *claim_gates,
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
            "VAL1275_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1275_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1275_2_import_guard",
            "GR pattern is marked reference-only, not proof",
            import_guard_present,
            "GRP1275_0_static_spherical_pattern=REFERENCE_ONLY_NOT_PROOF",
        ),
        validation_row(
            "VAL1275_3_equation_diff_not_derived",
            "MTS equation-difference derivation remains blocked",
            equation_not_derived,
            "EDA1275_5_verdict=NOT_DERIVED",
        ),
        validation_row(
            "VAL1275_4_closure_baseline",
            "local closure baseline is explicit and nonclaim",
            closure_written,
            f"closure_rows={len(closure_baseline)}",
        ),
        validation_row(
            "VAL1275_5_missing_parent_map",
            "missing parent Euler/source map is explicit",
            parent_map_missing,
            f"missing_parent_rows={len(missing_parent)}",
        ),
        validation_row(
            "VAL1275_6_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows and finite_locked,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1275_7_claim_gates_safe",
            "claim gates remain blocked except closure-baseline nonclaim gate",
            claim_gates_safe and no_claim_promoted,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1275_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1275_9_next_target_1276",
            "next target routes to parent Euler/source-map contract or closure scorecard",
            next_target[0]["next_id"] == "NEXT1275_0_1276",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1275_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1275_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1275_12_overall",
            "overall 1275 validation",
            overall_pass,
            "1275 attempts the GR-style radial equation-difference route, blocks it because MTS parent Euler/source maps are missing, records C_R=0 as closure-only, and routes to the parent Euler/source-map contract next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1275 does not derive the GR-style time-radial equation-difference from MTS. The GR pattern is useful as a target, but current MTS cannot yet produce its own `E_time - E_radial` equation for `C_R=ln(T^2S)` without missing parent Euler equations, source map, and boundary/no-charge certificates.

**Main progress:** the exact local branch is now honestly labelled. `C_R=0`, `Q_R=0`, source-balance, and boundary normalization are recorded as a **local closure baseline**, not as a derived GR reduction. That keeps future testing clean: closure benchmark over here, finite residual branch over there, no mixing.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, zero-residual, or finite-`Z_R` row is claimed. GR is a structural comparison pattern only, not an imported derivation.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## GR Pattern Import Guard
{markdown_table(gr_pattern, ["pattern_id", "structural_pattern", "permitted_use", "forbidden_use", "MTS_requirement", "status", "valid_for_claim", "claim_allowed"])}

## MTS Equation-Difference Attempt
{markdown_table(equation_diff, ["attempt_id", "MTS_object", "candidate_equation", "derivation_status", "blocker", "if_closed", "valid_for_claim", "claim_allowed"])}

## Local Closure Baseline
{markdown_table(closure_baseline, ["baseline_id", "closure_item", "assumption", "purpose", "claim_status", "allowed_use", "forbidden_use", "valid_for_claim", "claim_allowed"])}

## Missing Parent Euler/Source Map
{markdown_table(missing_parent, ["missing_id", "needed_object", "why_needed", "current_status", "next_action", "valid_for_claim", "claim_allowed"])}

## Finite Residual Decision
{markdown_table(finite_decision, ["finite_id", "trigger", "needed_rows", "current_status", "action_taken", "reason", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

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
