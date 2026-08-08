from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1273"
TITLE = "1273-Y5-R10-RAB-parent-Hcore-radial-cell-owner-or-finite-residual-source-acquisition"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
UV_CHANGE_PATH = OUT_DIR / f"{PACK_ID}_UV_RADIAL_CELL_VARIABLE_CHANGE.csv"
HCORE_OWNER_PATH = OUT_DIR / f"{PACK_ID}_HCORE_OWNER_CLASSIFICATION.csv"
DIRAC_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_DIRAC_PRESERVATION_AUDIT.csv"
FINITE_DECISION_PATH = OUT_DIR / f"{PACK_ID}_FINITE_RESIDUAL_DECISION.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1273_VALIDATION.csv"


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
        "scan_id": f"SCAN1273_{intake_class}_{path.stem}_{row_id}",
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
        UV_CHANGE_PATH,
        HCORE_OWNER_PATH,
        DIRAC_AUDIT_PATH,
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
            "source_id": "SRC1273_0_1272_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1272_NEXT_TARGET.csv",
            "needle": "NEXT1272_0_1273",
            "purpose": "handoff into H_core/radial-cell owner attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_1_1272_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1272_PARENT_NECESSITY_CONTRACT.csv",
            "needle": "PNC1272_1_radial_cell_owner",
            "purpose": "missing radial-cell owner clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_2_1272_derivation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1272_RADIAL_CELL_VARIATIONAL_DERIVATION_ATTEMPT.csv",
            "needle": "RCD1272_7_verdict",
            "purpose": "1272 did not derive parent necessity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_3_1248_dirac",
            "local_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "needle": "DIR1248_2_preservation",
            "purpose": "H_core/bracket preservation blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_4_1268_action",
            "local_path": "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            "needle": "CAC1268_1_constraint_action",
            "purpose": "conditional auxiliary compatibility mechanism",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_5_hamiltonian",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "hamiltonian_radial_cell_sharpened_not_parent_derived",
            "purpose": "Hamiltonian radial-cell attempt and failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_6_observer_cell",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "J_q = T sqrt(S)",
            "purpose": "observer-cell Jacobian identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_7_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "boundary/current hair obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_8_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "purpose": "Noether route cannot create constraint without parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1273_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual validator accepts no source-ready rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    uv_change = [
        {
            "variable_id": "UV1273_0_u_cell_volume",
            "definition": "u := ln(J_q) = ln(T sqrt(S)) = 1/2 ln(T^2 S)",
            "inverse_relation": "C_R=R_AB=2u",
            "physical_role": "radial observer configuration-cell volume mode",
            "zero_condition": "u=0 iff J_q=1 iff T sqrt(S)=1 iff R_AB=0",
            "claim_status": "DEFINITION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "variable_id": "UV1273_1_v_cone_ratio",
            "definition": "v := ln(T/sqrt(S))",
            "inverse_relation": "ln T=(u+v)/2; ln sqrt(S)=(u-v)/2",
            "physical_role": "radial clock/routing ratio seen by null-cone style tests",
            "zero_condition": "not required for local reciprocity; v can carry physical potential/routing information",
            "claim_status": "DEFINITION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "variable_id": "UV1273_2_target_split",
            "definition": "H_core may depend on u, v, momenta, matter, and boundary data",
            "inverse_relation": "exact local-GR branch needs an equation setting u=0 before readout",
            "physical_role": "separates cell-volume proof from cone/clock phenomenology",
            "zero_condition": "ordinary dependence on v does not constrain u",
            "claim_status": "CLASSIFICATION_TOOL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    hcore_owner = [
        {
            "owner_id": "HCO1273_0_u_absent",
            "candidate_Hcore_owner": "H_core depends on v and public fields but not on u",
            "Euler_or_constraint_effect": "delta_u H_core=0 gives no equation for u",
            "zero_result": "NO_ZERO_EQUATION",
            "residual_risk": "u remains gauge/flat only if quotient/matter descent is separately proved; 1271 rejected using this after readout",
            "status": "FAILS_AS_HCORE_OWNER",
            "next_requirement": "derive pre-readout quotient or auxiliary elimination",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "HCO1273_1_smooth_potential",
            "candidate_Hcore_owner": "H_core contains V(u) with V'(0)=0 and V''(0)>0",
            "Euler_or_constraint_effect": "V'(u)+J_u=0; for small source J_u, u shifts by roughly -J_u/V''(0)",
            "zero_result": "FINITE_RESIDUAL_NOT_EXACT_ZERO",
            "residual_risk": "requires sourced mass/stiffness and matter coupling coefficients; local tests become bounds, not theorem-zero",
            "status": "FINITE_BRANCH_IF_CHOSEN",
            "next_requirement": "source Z_u, M_u^2, J_u, boundary and arena projection coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "HCO1273_2_kinetic_u",
            "candidate_Hcore_owner": "H_core contains kinetic/gradient terms for u or R_AB",
            "Euler_or_constraint_effect": "u becomes a propagating or elliptic field with exterior charge modes",
            "zero_result": "NO_THEOREM_ZERO",
            "residual_risk": "reopens Q_R hair and R10/PPN/clock/orbital residuals",
            "status": "FINITE_BRANCH_REQUIRED",
            "next_requirement": "source real kinetic coefficient and local bound projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "HCO1273_3_boundary_current",
            "candidate_Hcore_owner": "H_core gives a conserved cell current for u",
            "Euler_or_constraint_effect": "partial_r(W partial_r u)=0 -> W partial_r u=Q_u",
            "zero_result": "NO_ZERO_WITHOUT_NO_CHARGE",
            "residual_risk": "asymptotic conditions alone do not kill reciprocal hair in the existing current audit",
            "status": "BLOCKED_BY_NO_CHARGE",
            "next_requirement": "derive Q_u=0 from parent boundary variational class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "HCO1273_4_linear_multiplier",
            "candidate_Hcore_owner": "H_core/parent action contains Lambda_R C_R = 2 Lambda_R u",
            "Euler_or_constraint_effect": "delta_Lambda_R gives u=0; delta_u fixes Lambda_R only if direct sources vanish",
            "zero_result": "EXACT_CONDITIONAL_ZERO",
            "residual_risk": "multiplier origin, source silence, and Dirac preservation remain unsigned",
            "status": "BEST_CONDITIONAL_MECHANISM",
            "next_requirement": "derive Lambda_R as a parent primitive/constraint, not an appendage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "HCO1273_5_unimodular_radial_cell",
            "candidate_Hcore_owner": "parent coframe/measure grammar imposes det(theta_t,theta_r)=det(theta_t,theta_r)_flat",
            "Euler_or_constraint_effect": "unimodular radial-cell condition is u=0 and can be represented by Lambda_R C_R",
            "zero_result": "WORKS_IF_PARENT_GRAMMAR_SIGNED",
            "residual_risk": "current corpus has motivation but not a derivation of this grammar",
            "status": "NEXT_DERIVATION_TARGET",
            "next_requirement": "prove radial-cell unimodularity from motion/time/space primitives or demote to closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "owner_id": "HCO1273_6_classification_verdict",
            "candidate_Hcore_owner": "ordinary H_core without a constraint multiplier or unimodular cell grammar",
            "Euler_or_constraint_effect": "either gives no u equation, makes u physical/finite, or allows current hair",
            "zero_result": "NO_ORDINARY_HCORE_ZERO_OWNER",
            "residual_risk": "exact local-GR reduction still requires constrained parent origin; otherwise local tests must bound finite residuals",
            "status": "STRICT_DERIVATION_NOT_CLOSED",
            "next_requirement": "try the unimodular radial-cell origin next, then fallback to source-backed finite residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dirac_audit = [
        {
            "audit_id": "DPA1273_0_reparametrize",
            "step": "use u=C_R/2 and v=ln(T/sqrt(S))",
            "formal_condition": "C_R approx 0 is equivalent to u approx 0",
            "status": "PASS_DEFINITIONAL",
            "blocker": "none; this is only a coordinate split on field space",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DPA1273_1_primary_secondary",
            "step": "multiplier action gives primary/secondary constraints",
            "formal_condition": "pi_Lambda approx 0; dot(pi_Lambda)=-2u approx 0",
            "status": "PASS_WITHIN_MULTIPLIER_ANSATZ",
            "blocker": "still assumes Lambda_R is in the parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DPA1273_2_preservation",
            "step": "preserve u approx 0",
            "formal_condition": "dot(u)={u,H_core}+Lambda-sector terms must vanish or fix a multiplier",
            "status": "BLOCKED_BY_UNSIGNED_HCORE",
            "blocker": "no parent bracket table or H_core for u/v exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DPA1273_3_source_silence",
            "step": "solve E_u/E_R without finite force",
            "formal_condition": "J_u + boundary_u + readout_regen_u = 0 on protected branch",
            "status": "BLOCKED_BY_MATTER_BOUNDARY_READOUT",
            "blocker": "matter descent, no-charge boundary, and EFT/readout stability remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DPA1273_4_class",
            "step": "classify the constraint pair",
            "formal_condition": "{pi_Lambda,u}, {u,H_core}, and momentum/Hamiltonian constraints must close without adding u hair",
            "status": "BLOCKED_BY_ALGEBRA",
            "blocker": "no canonical algebra or degree-of-freedom count has been derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DPA1273_5_conditional_theorem",
            "step": "conditional local zero theorem",
            "formal_condition": "if HCO1273_4 or HCO1273_5 is parent-signed and DPA1273_2..4 close, then u=0 before readout",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocker": "parent origin of the constrained cell remains the live problem",
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
            "finite_id": "FRD1273_0_when_finite_needed",
            "trigger": "choose smooth potential, kinetic, or current owner for u/R_AB",
            "needed_rows": "Z_u or Z_R; M_u^2; J_u/J_R; B_u/B_R; tau_R10; tau_PPN; tau_clock; tau_orbital",
            "current_status": "SOURCE_ROWS_MISSING",
            "action_taken": "no finite row created",
            "reason": "no source path, anchor, coefficient, units, normalization, and arena projection exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "finite_id": "FRD1273_1_validator_state",
            "trigger": "rescan rab-sector intake",
            "needed_rows": "raw or accepted source-backed coefficient rows",
            "current_status": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "action_taken": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "reason": "docs templates are rejected and no raw/accepted rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "finite_id": "FRD1273_2_claim_discipline",
            "trigger": "ordinary H_core no-go leaves finite branch as fallback",
            "needed_rows": "all coefficient/projection rows must be validator accepted before scoring",
            "current_status": "FALLBACK_ONLY",
            "action_taken": "kept branch locked",
            "reason": "theorem-zero is not closed and finite coefficients are not sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1273_0_ordinary_Hcore_zero",
            "claim": "ordinary H_core derives u=0/R_AB=0",
            "status": "BLOCKED",
            "reason": "classification shows ordinary H_core either gives no equation, finite residuals, or hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1273_1_multiplier_owner",
            "claim": "Lambda_R C_R has parent origin",
            "status": "BLOCKED",
            "reason": "linear multiplier remains exact but conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1273_2_unimodular_cell",
            "claim": "unimodular radial-cell grammar is parent-derived",
            "status": "OPEN_NEXT_TARGET",
            "reason": "it is the only non-finite route left that can make J_q=1 exact without smuggling the GR result",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1273_3_finite_branch",
            "claim": "finite residual rows can be scored",
            "status": "BLOCKED",
            "reason": "no source-backed accepted rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1273_4_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither parent zero theorem nor finite residual branch is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1273_5_owner_classification",
            "claim": "H_core owner routes are classified",
            "status": "PASS_NONCLAIM",
            "reason": "u/v split makes the ordinary-H_core obstruction precise",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1273_0_no_ordinary_Hcore",
            "decision": "do not pursue an unconstrained ordinary H_core as the exact local-GR proof",
            "because": "it cannot force u=0 without becoming either a finite field model or a hidden constraint",
            "status": "ORDINARY_HCORE_ROUTE_REJECTED_FOR_THEOREM_ZERO",
            "next_action": "try parent unimodular radial-cell grammar as the honest constraint-origin route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1273_1_best_exact_route",
            "decision": "move to unimodular/configuration-cell origin",
            "because": "J_q=1 is exactly the needed condition, but it must be parent grammar rather than a desired endpoint",
            "status": "UNIMODULAR_CELL_ROUTE_SELECTED",
            "next_action": "derive or reject det(theta_t,theta_r)=flat as a parent motion/time/space cell axiom",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1273_2_finite_fallback",
            "decision": "keep finite residual acquisition as fallback",
            "because": "smooth potential/kinetic/current owners are testable but not theorem-zero",
            "status": "FALLBACK_LOCKED",
            "next_action": "only create raw rows after source-backed coefficients and projections exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1273_0_1274",
            "target_file": "1274-Y5-R10-RAB-unimodular-radial-cell-constraint-origin-or-finite-residual-intake.md",
            "target_script": "scripts/Y5_R10_RAB_unimodular_radial_cell_constraint_origin_or_finite_residual_intake.py",
            "task": "try to derive the Lambda_R C_R block from a parent unimodular radial observer-cell/coframe measure grammar; if this fails, demote it to explicit closure and keep only source-backed finite residual intake",
            "success_condition": "det(theta_t,theta_r) radial-cell normalization is derived from parent motion/time/space primitives before local readout, or the exact constraint route is explicitly demoted",
            "do_not": "do not call the unimodular cell condition derived merely because it reproduces AB=1",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (UV_CHANGE_PATH, uv_change),
        (HCORE_OWNER_PATH, hcore_owner),
        (DIRAC_AUDIT_PATH, dirac_audit),
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
    uv_split_ready = any(row["variable_id"] == "UV1273_0_u_cell_volume" and "R_AB=2u" in row["inverse_relation"] for row in uv_change)
    ordinary_hcore_rejected = any(
        row["owner_id"] == "HCO1273_6_classification_verdict"
        and row["zero_result"] == "NO_ORDINARY_HCORE_ZERO_OWNER"
        and row["status"] == "STRICT_DERIVATION_NOT_CLOSED"
        for row in hcore_owner
    )
    multiplier_conditional = any(
        row["owner_id"] == "HCO1273_4_linear_multiplier" and row["zero_result"] == "EXACT_CONDITIONAL_ZERO"
        for row in hcore_owner
    )
    unimodular_next = any(
        row["owner_id"] == "HCO1273_5_unimodular_radial_cell" and row["status"] == "NEXT_DERIVATION_TARGET"
        for row in hcore_owner
    )
    dirac_still_blocked = any(row["audit_id"] == "DPA1273_2_preservation" and row["status"] == "BLOCKED_BY_UNSIGNED_HCORE" for row in dirac_audit)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    finite_locked = any(row["finite_id"] == "FRD1273_2_claim_discipline" and row["current_status"] == "FALLBACK_ONLY" for row in finite_decision)
    claim_gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM", "OPEN_NEXT_TARGET"} for row in claim_gates)
    no_claim_promoted = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] == "GATE1273_5_owner_classification"
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *uv_change,
        *hcore_owner,
        *dirac_audit,
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
            "VAL1273_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1273_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1273_2_uv_split",
            "u/v radial-cell split defines the exact zero target",
            uv_split_ready,
            "u=ln(J_q)=C_R/2; u=0 iff R_AB=0",
        ),
        validation_row(
            "VAL1273_3_hcore_classification",
            "ordinary H_core routes are classified and rejected for theorem-zero",
            ordinary_hcore_rejected and multiplier_conditional and unimodular_next,
            "ordinary H_core no-go; multiplier exact conditional; unimodular cell selected next",
        ),
        validation_row(
            "VAL1273_4_dirac_audit",
            "Dirac preservation remains blocked by unsigned H_core",
            dirac_still_blocked,
            "DPA1273_2_preservation=BLOCKED_BY_UNSIGNED_HCORE",
        ),
        validation_row(
            "VAL1273_5_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows and finite_locked,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1273_6_claim_gates_safe",
            "claim gates remain blocked/open-next-target except owner-classification nonclaim gate",
            claim_gates_safe and no_claim_promoted,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1273_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1273_8_next_target_1274",
            "next target routes to unimodular radial-cell origin or finite residual intake",
            next_target[0]["next_id"] == "NEXT1273_0_1274",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1273_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1273_10_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1273_11_overall",
            "overall 1273 validation",
            overall_pass,
            "1273 classifies H_core owner routes using u=ln(J_q), rejects ordinary H_core as an exact zero owner, keeps multiplier/unimodular routes conditional, and routes to unimodular radial-cell origin next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1273 does not find an ordinary `H_core` that derives the exact local reciprocity condition. In the clean variables `u=ln(J_q)=R_AB/2` and `v=ln(T/sqrt(S))`, exact local GR needs `u=0`. An unconstrained core either leaves `u` free, makes `u` a finite physical residual, or permits current/boundary hair.

**Main progress:** this is a useful no-go, not a dead end. The exact branch now has only one honest route left: derive a parent unimodular radial observer-cell/coframe grammar, equivalent to `det(theta_t,theta_r)=flat`, which would make `Lambda_R C_R` necessary rather than appended.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, zero-residual, or finite-`Z_R` row is claimed. The ordinary `H_core` path is rejected for theorem-zero; finite residuals remain a source-backed fallback only.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## u/v Radial-Cell Variable Change
{markdown_table(uv_change, ["variable_id", "definition", "inverse_relation", "physical_role", "zero_condition", "claim_status", "valid_for_claim", "claim_allowed"])}

## H_core Owner Classification
{markdown_table(hcore_owner, ["owner_id", "candidate_Hcore_owner", "Euler_or_constraint_effect", "zero_result", "residual_risk", "status", "next_requirement", "valid_for_claim", "claim_allowed"])}

## Dirac Preservation Audit
{markdown_table(dirac_audit, ["audit_id", "step", "formal_condition", "status", "blocker", "valid_for_claim", "claim_allowed"])}

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
