from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1274"
TITLE = "1274-Y5-R10-RAB-unimodular-radial-cell-constraint-origin-or-finite-residual-intake"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
UNIMODULAR_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_UNIMODULAR_CELL_ORIGIN_AUDIT.csv"
GR_ROUTE_PATH = OUT_DIR / f"{PACK_ID}_GR_STYLE_EQUATION_DIFFERENCE_ROUTE.csv"
ROUTE_COMPARISON_PATH = OUT_DIR / f"{PACK_ID}_ROUTE_COMPARISON.csv"
FINITE_DECISION_PATH = OUT_DIR / f"{PACK_ID}_FINITE_RESIDUAL_DECISION.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1274_VALIDATION.csv"


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
        "scan_id": f"SCAN1274_{intake_class}_{path.stem}_{row_id}",
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
        UNIMODULAR_AUDIT_PATH,
        GR_ROUTE_PATH,
        ROUTE_COMPARISON_PATH,
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
            "source_id": "SRC1274_0_1273_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1273_NEXT_TARGET.csv",
            "needle": "NEXT1273_0_1274",
            "purpose": "handoff into unimodular radial-cell origin attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_1_1273_hcore",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv",
            "needle": "HCO1273_5_unimodular_radial_cell",
            "purpose": "1273 selected unimodular radial cell as next exact route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_2_1273_uv",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1273_UV_RADIAL_CELL_VARIABLE_CHANGE.csv",
            "needle": "UV1273_0_u_cell_volume",
            "purpose": "u=ln(J_q)=R_AB/2 target split",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_3_observer_cell",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "J_q = T sqrt(S)",
            "purpose": "radial observer-cell Jacobian",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_4_hamiltonian_cell",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "separate radial cell gives p=1 exactly",
            "purpose": "separate radial cell gives the desired exponent but was not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_5_1248_dirac",
            "local_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "needle": "DIR1248_2_preservation",
            "purpose": "H_core/bracket preservation blocker remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_6_1268_action",
            "local_path": "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            "needle": "CAC1268_1_constraint_action",
            "purpose": "conditional multiplier mechanism",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_7_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "current route leaves hair without no-charge theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_8_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "purpose": "Noether cannot conjure the constraint without parent ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1274_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows still absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    unimodular_audit = [
        {
            "audit_id": "URO1274_0_cell_measure_identity",
            "candidate_origin": "radial observer two-cell measure",
            "equation": "theta_0 wedge theta_1 = c T sqrt(S) dt wedge dr = c J_q dt wedge dr",
            "effect_if_true": "defines the cell-volume mode u=ln(J_q)=R_AB/2",
            "status": "EXACT_IDENTITY_NOT_DYNAMICS",
            "blocker": "an identity does not produce an Euler equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "URO1274_1_imposed_unimodular_cell",
            "candidate_origin": "fix radial observer configuration-cell measure to the flat/reference cell",
            "equation": "theta_0 wedge theta_1 = c dt wedge dr -> J_q=1 -> R_AB=0",
            "effect_if_true": "gives the local reciprocal/GR branch exactly",
            "status": "WORKS_IF_IMPOSED",
            "blocker": "imposition is not a derivation from parent dynamics",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "URO1274_2_multiplier_representation",
            "candidate_origin": "represent the unimodular cell with a constraint term",
            "equation": "S_cell = integral mu_parent Lambda_U ln(J_q) = 1/2 integral mu_parent Lambda_U R_AB",
            "effect_if_true": "variation in Lambda_U gives R_AB=0",
            "status": "EXACT_CONDITIONAL",
            "blocker": "same parent-origin problem as Lambda_R C_R unless Lambda_U is forced by parent grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "URO1274_3_gauge_danger",
            "candidate_origin": "call J_q=1 a gauge choice",
            "equation": "choose coordinates/coframe so T sqrt(S)=1",
            "effect_if_true": "would hide the target in the readout map",
            "status": "REJECT_AS_NONCIRCULAR_DERIVATION",
            "blocker": "A, B, clocks, radial rulers, matter coframe, and boundary data are observed after readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "URO1274_4_source_danger",
            "candidate_origin": "cell-volume equation survives matter/boundary/readout",
            "equation": "E_u: Lambda_U + J_u + B_u + readout_u = 0",
            "effect_if_true": "Lambda_U=0 and no finite residual only if sources vanish or descend",
            "status": "BLOCKED_BY_SOURCE_SILENCE",
            "blocker": "matter descent, boundary no-charge, and readout stability remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "URO1274_5_verdict",
            "candidate_origin": "parent unimodular radial-cell grammar",
            "equation": "J_q=1 before local readout",
            "effect_if_true": "would close the exact branch if parent-signed",
            "status": "CLOSURE_ONLY_NOT_DERIVED",
            "blocker": "current corpus does not derive why the parent action must preserve the radial configuration cell separately",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "URO1274_6_less_scrutiny_rule",
            "candidate_origin": "derive AB=1 from field equations rather than impose cell unimodularity",
            "equation": "field-equation difference -> partial_r ln(AB)=source_R",
            "effect_if_true": "closer to how GR earns the Schwarzschild/vacuum AB=1 relation",
            "status": "SELECT_BETTER_NEXT_ROUTE",
            "blocker": "MTS parent Euler equations for the time/radial sectors must be written",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    gr_route = [
        {
            "route_id": "GED1274_0_GR_pattern",
            "known_pattern": "static spherical GR obtains AB=constant from the time-radial field-equation difference in vacuum/source-balanced cases",
            "MTS_analogue_needed": "derive an MTS equation-difference for C_R=ln(T^2S)=ln(AB)",
            "target_equation": "partial_r C_R = S_R[source, anisotropy, residual]",
            "closure_condition": "S_R=0 plus boundary/asymptotic normalization gives C_R=0",
            "status": "REFERENCE_PATTERN_NOT_MTS_DERIVATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "GED1274_1_parent_equations_needed",
            "known_pattern": "Euler equations for lapse/time and radial routing must be available before the difference can be computed",
            "MTS_analogue_needed": "E_T and E_S or E_u/E_v from L_MTS_core",
            "target_equation": "E_time - E_radial -> differential or algebraic equation for C_R",
            "closure_condition": "local vacuum/no radial anisotropic stress removes the source term",
            "status": "MISSING_PARENT_EULER_EQUATIONS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "GED1274_2_source_condition",
            "known_pattern": "AB=1 is not generic with arbitrary matter; source conditions matter",
            "MTS_analogue_needed": "define the MTS source combination that replaces T^t_t-T^r_r or radial anisotropic stress",
            "target_equation": "partial_r C_R proportional to source_difference + residual_terms",
            "closure_condition": "source_difference=0 on local vacuum/controlled branch",
            "status": "SOURCE_MAP_OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "GED1274_3_boundary_condition",
            "known_pattern": "constant AB becomes 1 only after normalization/matching",
            "MTS_analogue_needed": "asymptotic flatness, local matching, or clock/radial reference normalization",
            "target_equation": "C_R=constant -> C_R=0",
            "closure_condition": "constant fixed by boundary/readout normalization without hiding dynamics",
            "status": "BOUNDARY_NORMALIZATION_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "GED1274_4_best_next_test",
            "known_pattern": "field-equation difference is less ad hoc than unimodular imposition",
            "MTS_analogue_needed": "write symbolic E_time/E_radial contract and check whether existing MTS action pieces can supply it",
            "target_equation": "D_R[MTS] := E_time - E_radial = partial_r C_R - S_R = 0",
            "closure_condition": "D_R plus source/boundary gates imply local GR branch",
            "status": "SELECTED_NEXT_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    route_comparison = [
        {
            "comparison_id": "RC1274_0_unimodular_cell",
            "route": "impose parent radial-cell unimodularity",
            "strength": "exactly gives J_q=1 and R_AB=0",
            "weakness": "looks like an axiom unless parent action/equation forces it",
            "decision": "DEMOTE_TO_CLOSURE_UNLESS_DERIVED",
            "selected": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "RC1274_1_ordinary_Hcore",
            "route": "ordinary H_core potential/kinetic/current owner",
            "strength": "testable finite residual model",
            "weakness": "does not produce theorem-zero",
            "decision": "FINITE_FALLBACK_ONLY",
            "selected": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "RC1274_2_GR_style_difference",
            "route": "derive local reciprocity from time-radial field-equation difference",
            "strength": "closest to how GR earns AB=1 in vacuum spherical systems",
            "weakness": "requires parent Euler equations and source map not yet written",
            "decision": "SELECTED_NEXT_DERIVATION_ROUTE",
            "selected": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "RC1274_3_finite_source_intake",
            "route": "source finite residual rows",
            "strength": "empirically honest if exact derivation fails",
            "weakness": "no accepted source-backed rows exist",
            "decision": "LOCKED_FALLBACK",
            "selected": False,
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
            "finite_id": "FRD1274_0_no_intake",
            "trigger": "exact route remains unproved",
            "needed_rows": "Z_R/M_R^2/J_R/B_R/tau_R10/tau_PPN/tau_clock/tau_orbital",
            "current_status": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "action_taken": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "reason": "no source-backed row exists; templates remain rejected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "finite_id": "FRD1274_1_do_not_fabricate",
            "trigger": "temptation to score finite residual after exact derivation stalls",
            "needed_rows": "real source path, source anchor, coefficient value, units, normalization, arena projection",
            "current_status": "FALLBACK_LOCKED",
            "action_taken": "no row created",
            "reason": "finite rows without source-backed coefficients would fake robustness",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1274_0_unimodular_derived",
            "claim": "unimodular radial-cell condition is parent-derived",
            "status": "BLOCKED",
            "reason": "it works if imposed but current corpus does not derive it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1274_1_GR_difference_route",
            "claim": "MTS field-equation difference derives AB=1",
            "status": "OPEN_NEXT_TARGET",
            "reason": "selected as best next derivation route, not yet written",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1274_2_lambda_constraint",
            "claim": "Lambda_R C_R is parent-necessary",
            "status": "BLOCKED",
            "reason": "unimodular representation reuses the same multiplier-origin problem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1274_3_finite_branch",
            "claim": "finite residual rows can be scored",
            "status": "BLOCKED",
            "reason": "no source-backed accepted rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1274_4_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "no exact or finite local branch is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1274_5_route_selection",
            "claim": "best next route selected",
            "status": "PASS_NONCLAIM",
            "reason": "GR-style equation-difference route is selected as less axiom-like than cell imposition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1274_0_unimodular_status",
            "decision": "do not claim the unimodular cell as derived",
            "because": "J_q=1 exactly solves the problem only when imposed; the parent origin is not present",
            "status": "DEMOTED_TO_CLOSURE_IF_USED",
            "next_action": "prefer a field-equation difference derivation before accepting closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1274_1_best_route",
            "decision": "try the GR-style time-radial equation-difference route next",
            "because": "it derives AB=1 from equations and source/boundary conditions rather than a chosen cell determinant",
            "status": "GR_STYLE_DIFFERENCE_SELECTED",
            "next_action": "write symbolic MTS E_time/E_radial contract and attempt the C_R equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1274_2_finite_discipline",
            "decision": "keep finite residual rows locked",
            "because": "there are still no source-backed local residual coefficients",
            "status": "FALLBACK_LOCKED",
            "next_action": "only source rows after real coefficients/projections exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1274_0_1275",
            "target_file": "1275-Y5-R10-RAB-GR-style-radial-field-equation-difference-or-local-closure-baseline.md",
            "target_script": "scripts/Y5_R10_RAB_GR_style_radial_field_equation_difference_or_local_closure_baseline.py",
            "task": "try to derive an MTS time-radial field-equation difference D_R that gives partial_r ln(T^2S)=source_R and AB=1 under local vacuum/source-balance plus boundary normalization; if this fails, record the local constraint as a closure baseline and keep finite residual intake locked",
            "success_condition": "a noncircular MTS equation-difference produces the local GR reciprocity condition, or the exact branch is explicitly demoted to closure-only",
            "do_not": "do not import Einstein equations as the MTS derivation; use them only as the structural comparison pattern",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (UNIMODULAR_AUDIT_PATH, unimodular_audit),
        (GR_ROUTE_PATH, gr_route),
        (ROUTE_COMPARISON_PATH, route_comparison),
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
    unimodular_not_derived = any(row["audit_id"] == "URO1274_5_verdict" and row["status"] == "CLOSURE_ONLY_NOT_DERIVED" for row in unimodular_audit)
    gr_route_selected = any(row["route_id"] == "GED1274_4_best_next_test" and row["status"] == "SELECTED_NEXT_TARGET" for row in gr_route)
    comparison_selects_gr = any(row["comparison_id"] == "RC1274_2_GR_style_difference" and str(row["selected"]).lower() == "true" for row in route_comparison)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    finite_locked = any(row["finite_id"] == "FRD1274_1_do_not_fabricate" and row["current_status"] == "FALLBACK_LOCKED" for row in finite_decision)
    claim_gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM", "OPEN_NEXT_TARGET"} for row in claim_gates)
    no_claim_promoted = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] == "GATE1274_5_route_selection"
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *unimodular_audit,
        *gr_route,
        *route_comparison,
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
            "VAL1274_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1274_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1274_2_unimodular_not_derived",
            "unimodular radial-cell route is not promoted as derived",
            unimodular_not_derived,
            "URO1274_5_verdict=CLOSURE_ONLY_NOT_DERIVED",
        ),
        validation_row(
            "VAL1274_3_gr_route_selected",
            "GR-style equation-difference route is selected next",
            gr_route_selected and comparison_selects_gr,
            "GED1274_4_best_next_test selected; RC1274_2 selected=True",
        ),
        validation_row(
            "VAL1274_4_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows and finite_locked,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1274_5_claim_gates_safe",
            "claim gates remain blocked/open-next-target except route-selection nonclaim gate",
            claim_gates_safe and no_claim_promoted,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1274_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1274_7_next_target_1275",
            "next target routes to GR-style field-equation difference",
            next_target[0]["next_id"] == "NEXT1274_0_1275",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1274_8_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1274_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1274_10_overall",
            "overall 1274 validation",
            overall_pass,
            "1274 rejects unimodular radial-cell imposition as a derived theorem, keeps finite rows locked, and selects the GR-style time-radial equation-difference route as the next best derivation target",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1274 does not derive the unimodular radial observer-cell condition. `J_q=1` exactly gives `R_AB=0`, but making `theta_0 wedge theta_1` equal to the flat/reference radial cell is still an imposed constraint unless the parent action forces it.

**Main progress:** the best route is now changed. Rather than pretending a pretty cell-normalization axiom is a derivation, 1274 selects the GR-style route: derive `AB=1` from a time-radial field-equation difference plus local source/boundary conditions. That is the less-scrutinized, more respectable route.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, zero-residual, or finite-`Z_R` row is claimed. The unimodular cell remains closure-only unless a parent equation derives it.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Unimodular Cell Origin Audit
{markdown_table(unimodular_audit, ["audit_id", "candidate_origin", "equation", "effect_if_true", "status", "blocker", "valid_for_claim", "claim_allowed"])}

## GR-Style Equation-Difference Route
{markdown_table(gr_route, ["route_id", "known_pattern", "MTS_analogue_needed", "target_equation", "closure_condition", "status", "valid_for_claim", "claim_allowed"])}

## Route Comparison
{markdown_table(route_comparison, ["comparison_id", "route", "strength", "weakness", "decision", "selected", "valid_for_claim", "claim_allowed"])}

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
