from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1272"
TITLE = "1272-Y5-R10-RAB-auxiliary-parent-necessity-from-radial-cell-variational-principle-or-finite-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DERIVATION_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_RADIAL_CELL_VARIATIONAL_DERIVATION_ATTEMPT.csv"
CELL_TEST_PATH = OUT_DIR / f"{PACK_ID}_CELL_PRINCIPLE_TEST_MATRIX.csv"
PARENT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_NECESSITY_CONTRACT.csv"
FINITE_FALLBACK_PATH = OUT_DIR / f"{PACK_ID}_FINITE_SOURCE_FALLBACK_STATUS.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1272_VALIDATION.csv"


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
        "scan_id": f"SCAN1272_{intake_class}_{path.stem}_{row_id}",
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
        DERIVATION_ATTEMPT_PATH,
        CELL_TEST_PATH,
        PARENT_CONTRACT_PATH,
        FINITE_FALLBACK_PATH,
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
            "source_id": "SRC1272_0_1271_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1271_NEXT_TARGET.csv",
            "needle": "NEXT1271_0_1272",
            "purpose": "handoff into radial-cell parent-necessity derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_1_1271_aux_target",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1271_AUXILIARY_PARENT_NECESSITY_TARGET.csv",
            "needle": "AUXN1271_4_theorem_target",
            "purpose": "exact auxiliary theorem target inherited from 1271",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_2_1268_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
            "needle": "CAC1268_1_constraint_action",
            "purpose": "second-class compatibility action candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_3_observer_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "R_AB = ln(T^2 S) = 2 ln(J_q).",
            "purpose": "radial observer-cell identity and local-GR target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_4_nonprop_constraint",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB.",
            "purpose": "algebraic hard-constraint effect",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_5_phase_volume",
            "local_path": "08-phase-volume-reciprocity-origin.md",
            "needle": "phase_volume_reciprocity_motivated_not_parent_derived",
            "purpose": "phase-volume motivation and obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_6_hamiltonian_cell",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "hamiltonian_radial_cell_sharpened_not_parent_derived",
            "purpose": "Hamiltonian radial-cell sharpening and H_core blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_7_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "current/no-charge obstruction for R_AB hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_8_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "purpose": "Noether/gauge route obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_9_1247_gate",
            "local_path": "1247-Y5-R10-parent-lambdaR-constraint-legitimacy-gate.md",
            "needle": "GATE1247_1_parent_origin",
            "purpose": "earlier lambda_R parent-origin gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_10_1248_dirac",
            "local_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "needle": "DIR1248_2_preservation",
            "purpose": "minimal ansatz Dirac preservation blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1272_11_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite-ZR validator accepts no source-ready rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    derivation_attempt = [
        {
            "attempt_id": "RCD1272_0_observer_cell_identity",
            "input_principle": "local observer radial configuration cell",
            "local_equation": "theta_0=T c dt; theta_1=sqrt(S) dr; J_q=T sqrt(S); C_R=R_AB=ln(T^2 S)=2 ln(J_q)",
            "variational_effect": "defines the target variable C_R but supplies no Euler-Lagrange equation by itself",
            "result": "EXACT_IDENTITY_NOT_DYNAMICS",
            "blocker": "identity alone cannot require C_R=0",
            "source_hint": "10-observer-map-symplectic-contract.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_1_liouville_phase_volume",
            "input_principle": "canonical phase-volume/Liouville preservation",
            "local_equation": "J_q J_p = (T sqrt(S)) * (1/(T sqrt(S))) = 1",
            "variational_effect": "preserves full radial phase cell for any J_q if momentum cell compensates",
            "result": "FAILS_TO_DERIVE_C_R_ZERO",
            "blocker": "Liouville fixes product J_qJ_p, not J_q=1",
            "source_hint": "10-observer-map-symplectic-contract.md; 09-hamiltonian-radial-cell-derivation.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_2_radial_configuration_cell_normalization",
            "input_principle": "parent primitive preserves the radial observer configuration cell separately",
            "local_equation": "J_q=1 -> T sqrt(S)=1 -> C_R=ln(T^2S)=0",
            "variational_effect": "a multiplier term int mu_parent Lambda_R C_R would enforce the local reciprocal constraint",
            "result": "WORKS_IF_PARENT_PRIMITIVE",
            "blocker": "separate configuration-cell normalization is not yet derived from the parent action",
            "source_hint": "08-phase-volume-reciprocity-origin.md; 10-observer-map-symplectic-contract.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_3_motion_time_space_reciprocity",
            "input_principle": "motion/time/space capacities must remain reciprocally calibrated for local vacuum observers",
            "local_equation": "time capacity T and radial routing sqrt(S) must satisfy T sqrt(S)=1",
            "variational_effect": "would produce the right C_R constraint if promoted to a variational principle",
            "result": "MOTIVATED_NOT_DERIVED",
            "blocker": "current corpus states the calibration idea but does not derive the parent source term",
            "source_hint": "07-nonpropagating-reciprocity-constraint.md; 08-phase-volume-reciprocity-origin.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_4_radial_null_propagation",
            "input_principle": "radial light propagation and null cone consistency",
            "local_equation": "dr/dt can be written using T/sqrt(S)",
            "variational_effect": "constrains a ratio but does not separately fix T sqrt(S)",
            "result": "FAILS_TO_FIX_RADIAL_CELL",
            "blocker": "null propagation tolerates families of p/exponent choices",
            "source_hint": "09-hamiltonian-radial-cell-derivation.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_5_newtonian_clock_limit",
            "input_principle": "weak-field Newtonian slow-particle limit",
            "local_equation": "T^2=1-L plus a spatial exponent/routing choice",
            "variational_effect": "fixes lapse/clock normalization but not S or C_R alone",
            "result": "FAILS_TO_FIX_RADIAL_ROUTING",
            "blocker": "Newtonian recovery does not derive the p=1/AB=1 radial spatial law",
            "source_hint": "09-hamiltonian-radial-cell-derivation.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_6_minimal_dirac_action",
            "input_principle": "minimal constrained parent action ansatz",
            "local_equation": "S_min contains Lambda_R ln(T^2 S)",
            "variational_effect": "delta_Lambda_R gives C_R=0; delta_R can remove Lambda_R only under source-silence clauses",
            "result": "PASS_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocker": "H_core, brackets, preservation, class, matter descent, and boundary silence remain unsigned",
            "source_hint": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md; 1268 compatibility candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "RCD1272_7_verdict",
            "input_principle": "derive Lambda_R C_R necessity from radial-cell variational principle",
            "local_equation": "needed theorem: parent radial-cell owner -> Lambda_R C_R -> C_R=0 -> auxiliary pair eliminated before readout",
            "variational_effect": "not closed in the present corpus",
            "result": "PARENT_NECESSITY_NOT_DERIVED",
            "blocker": "the step from motivated radial-cell normalization to parent action necessity is still an extra axiom/contract",
            "source_hint": "this 1272 synthesis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    cell_tests = [
        {
            "test_id": "CPT1272_0_canonical_liouville",
            "candidate_principle": "full radial phase-volume conservation",
            "derives_C_R_zero": False,
            "status": "FAILS_PRODUCT_ONLY",
            "reason": "J_qJ_p=1 is tautologically compatible with arbitrary J_q",
            "next_use": "do not use as local-GR proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1272_1_configuration_cell",
            "candidate_principle": "radial observer configuration-cell normalization",
            "derives_C_R_zero": "conditional",
            "status": "WORKS_IF_PARENT_AXIOM",
            "reason": "J_q=1 exactly implies T sqrt(S)=1 and C_R=0",
            "next_use": "hunt for parent H_core/action owner that makes this non-optional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1272_2_capacity_reciprocity",
            "candidate_principle": "time capacity and radial motion capacity reciprocally calibrate",
            "derives_C_R_zero": "motivated",
            "status": "MOTIVATED_NOT_PARENT_DERIVED",
            "reason": "physically coherent, but still needs a variational owner",
            "next_use": "translate into an H_core or constrained-cell action clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1272_3_cell_current",
            "candidate_principle": "conserved radial cell current",
            "derives_C_R_zero": False,
            "status": "FAILS_NO_ZERO_CHARGE",
            "reason": "conservation permits nonzero reciprocal charge/hair",
            "next_use": "only useful if a no-charge theorem is added from the parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1272_4_noether_gauge",
            "candidate_principle": "Noether identity for reciprocal gauge generator",
            "derives_C_R_zero": False,
            "status": "FAILS_WITHOUT_PARENT_CONSTRAINT",
            "reason": "Noether explains preservation of an already-owned constraint, not its existence",
            "next_use": "revisit after parent constrained action is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1272_5_constrained_action",
            "candidate_principle": "add Lambda_R C_R as second-class auxiliary compatibility block",
            "derives_C_R_zero": "conditional",
            "status": "PASS_CONDITIONAL_NOT_SIGNED",
            "reason": "variation works exactly but parent necessity/source silence is not derived",
            "next_use": "keep as best current mechanism, not claim evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "CPT1272_6_finite_residual",
            "candidate_principle": "finite Z_R/J_R/B_R residual source row",
            "derives_C_R_zero": False,
            "status": "BLOCKED_NO_SOURCE_READY_ROWS",
            "reason": "validator accepts no raw/accepted coefficient rows",
            "next_use": "source real coefficients only if derivation branch remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_contract = [
        {
            "contract_id": "PNC1272_0_parent_field_grammar",
            "clause": "parent variables include the radial-cell compatibility pair",
            "required_content": "T, S, C_R=ln(T^2S), and Lambda_R or equivalent auxiliary variables appear before local readout",
            "current_evidence": "1248 ansatz and 1268 compatibility candidate",
            "status": "PROPOSED_NOT_SIGNED",
            "missing_parent_input": "actual parent field grammar and quotient/readout order",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_1_radial_cell_owner",
            "clause": "parent action owns radial observer configuration-cell normalization",
            "required_content": "a primitive or derived term whose Euler-Lagrange equation is J_q=1 or C_R=0",
            "current_evidence": "08/09/10 motivate J_q=T sqrt(S) and show why full phase volume is insufficient",
            "status": "OPEN_CORE_GAP",
            "missing_parent_input": "L_core/H_core term that makes J_q normalization non-optional",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_2_multiplier_necessity",
            "clause": "Lambda_R is required rather than appended",
            "required_content": "constraint analysis or variational reduction forces Lambda_R C_R as an auxiliary compatibility block",
            "current_evidence": "07 shows algebraic effect; 1268 gives clean conditional action",
            "status": "OPEN",
            "missing_parent_input": "derivation of Lambda_R from parent degeneracy/compatibility, not closure choice",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_3_dirac_chain",
            "clause": "primary/secondary/preservation/classification close",
            "required_content": "pi_Lambda≈0, C_R≈0, dot(C_R)=0, no tertiary leak, second-class or protected first-class status",
            "current_evidence": "1248 passes primary/secondary only inside an ansatz",
            "status": "BLOCKED_BY_H_CORE",
            "missing_parent_input": "canonical brackets and H_core for T,S/R_AB",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_4_no_direct_R_source",
            "clause": "matter, boundary, and readout do not source R_AB in E_R",
            "required_content": "delta_R(S_matter+B_R+S_eff)=0 on the protected local branch",
            "current_evidence": "1271 identifies matter/readout/boundary as separate open clauses",
            "status": "OPEN",
            "missing_parent_input": "matter descent, boundary no-hair, and local projection silence",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_5_no_kinetic_operator",
            "clause": "R_AB has no parent kinetic owner",
            "required_content": "no D R_AB or gradient-energy constructor survives the allowed parent grammar",
            "current_evidence": "1269 says operator exclusion is conditional, not signed",
            "status": "OPEN",
            "missing_parent_input": "complete object-language/sort exclusion proof",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_6_boundary_no_charge",
            "clause": "reciprocal charge/hair is forbidden",
            "required_content": "Q_R=B_R=Pi_R^n=0 or boundary term vanishes by parent variational principle",
            "current_evidence": "11 shows current conservation alone does not kill the charge",
            "status": "OPEN",
            "missing_parent_input": "no-charge theorem or boundary condition derived from parent action",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PNC1272_7_parent_signed_zero_theorem",
            "clause": "local zero theorem follows without closure smuggling",
            "required_content": "PNC1272_0..6 jointly imply R_AB,Lambda_R eliminate before local readout and Z_R=J_R=B_R=0",
            "current_evidence": "all necessary clauses are now explicit but not jointly signed",
            "status": "EXACT_CONTRACT_NOT_CLOSED",
            "missing_parent_input": "radial-cell owner plus source-silence and Dirac closure",
            "closes_zero_theorem": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    finite_fallback = [
        {
            "fallback_id": "FFB1272_0_docs_templates",
            "branch": "docs templates",
            "rows_seen": len(docs_rows),
            "accepted_ready": 0,
            "status": "REJECTED_AS_TEMPLATES",
            "reason": "docs templates are not live source-backed intake",
            "next_action": "leave templates as nonclaim instructions only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fallback_id": "FFB1272_1_raw_intake",
            "branch": "raw finite Z_R rows",
            "rows_seen": len(raw_rows),
            "accepted_ready": len([row for row in accepted_ready if row["intake_class"] == "raw"]),
            "status": "NO_RAW_ROWS",
            "reason": "no source-backed raw coefficient row exists",
            "next_action": "do not fabricate finite residual coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fallback_id": "FFB1272_2_accepted_intake",
            "branch": "accepted finite Z_R rows",
            "rows_seen": len(accepted_rows),
            "accepted_ready": len([row for row in accepted_ready if row["intake_class"] == "accepted"]),
            "status": "NO_ACCEPTED_ROWS",
            "reason": "no validator-accepted finite residual source row exists",
            "next_action": "finite branch remains unscored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "fallback_id": "FFB1272_3_no_row_created",
            "branch": "1272 generation",
            "rows_seen": len(validator_rescan),
            "accepted_ready": len(accepted_ready),
            "status": "NO_SOURCE_BACKED_ROW_CREATED",
            "reason": "1272 is a derivation checkpoint; it did not identify a real coefficient source",
            "next_action": "only create a raw row after source path, anchor, units, coefficient, and projection are real",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1272_0_radial_cell_derivation",
            "claim": "radial-cell variational principle derives C_R=0",
            "status": "BLOCKED",
            "reason": "J_q=1 works only as a new parent-owned principle; full Liouville does not derive it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1272_1_lambda_parent_necessity",
            "claim": "Lambda_R C_R is parent-necessary",
            "status": "BLOCKED",
            "reason": "multiplier necessity still lacks H_core/constraint-chain derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1272_2_zero_residual_theorem",
            "claim": "Z_R=J_R=B_R=0 follows on the local branch",
            "status": "BLOCKED",
            "reason": "matter descent, kinetic exclusion, and boundary no-charge clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1272_3_finite_source_branch",
            "claim": "finite Z_R residual can be scored",
            "status": "BLOCKED",
            "reason": "no raw/accepted source-backed coefficient row exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1272_4_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor finite residual branch is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1272_5_contract_written",
            "claim": "exact parent contract for future derivation is written",
            "status": "PASS_NONCLAIM",
            "reason": "1272 narrows the missing proof to parent H_core/radial-cell owner plus source-silence clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1272_0_derivation_result",
            "decision": "do not promote the radial-cell route as derived",
            "because": "generic phase volume and known limits fail to force J_q=1; the only working condition is a parent-owned configuration-cell normalization",
            "status": "STRICT_DERIVATION_BLOCKED",
            "next_action": "hunt for the H_core/action term that owns the radial configuration cell",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1272_1_best_route",
            "decision": "target the parent H_core/radial-cell owner next",
            "because": "1248 already showed the Dirac check is blocked exactly where H_core/brackets are missing",
            "status": "NEXT_ROUTE_SELECTED",
            "next_action": "write the candidate L_core/H_core grammar and test whether it yields Lambda_R C_R without appendage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1272_2_finite_branch",
            "decision": "keep finite residual sourcing as fallback only",
            "because": "there are no accepted source-ready rows and no source-backed coefficients were found in this step",
            "status": "FALLBACK_LOCKED",
            "next_action": "source real Z_R/J_R/B_R/tau coefficients only if parent derivation remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1272_3_no_claim",
            "decision": "make no local-GR/R10/PPN/clock/orbital claim",
            "because": "the exact obstruction is known but not solved",
            "status": "NONCLAIM_DISCIPLINE_MAINTAINED",
            "next_action": "continue derivation-first rather than shifting to public prose",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1272_0_1273",
            "target_file": "1273-Y5-R10-RAB-parent-Hcore-radial-cell-owner-or-finite-residual-source-acquisition.md",
            "target_script": "scripts/Y5_R10_RAB_parent_Hcore_radial_cell_owner_or_finite_residual_source_acquisition.py",
            "task": "try to derive the actual L_core/H_core term whose constraint chain makes radial configuration-cell normalization parent-owned; if this fails, keep theorem-zero blocked and source only real finite-residual inputs",
            "success_condition": "H_core/brackets make Lambda_R C_R necessary without appendage, or the finite branch remains the only live path with source-backed nonclaim rows",
            "do_not": "do not treat J_q=1 as proven merely because it gives the desired GR limit",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (DERIVATION_ATTEMPT_PATH, derivation_attempt),
        (CELL_TEST_PATH, cell_tests),
        (PARENT_CONTRACT_PATH, parent_contract),
        (FINITE_FALLBACK_PATH, finite_fallback),
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
    derivation_not_claimed = any(
        row["attempt_id"] == "RCD1272_7_verdict" and row["result"] == "PARENT_NECESSITY_NOT_DERIVED"
        for row in derivation_attempt
    )
    configuration_cell_is_conditional = any(
        row["test_id"] == "CPT1272_1_configuration_cell" and row["status"] == "WORKS_IF_PARENT_AXIOM"
        for row in cell_tests
    )
    liouville_rejected = any(
        row["test_id"] == "CPT1272_0_canonical_liouville" and row["status"] == "FAILS_PRODUCT_ONLY"
        for row in cell_tests
    )
    contract_explicit = any(
        row["contract_id"] == "PNC1272_7_parent_signed_zero_theorem" and row["status"] == "EXACT_CONTRACT_NOT_CLOSED"
        for row in parent_contract
    )
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    fallback_locked = any(row["fallback_id"] == "FFB1272_3_no_row_created" and row["status"] == "NO_SOURCE_BACKED_ROW_CREATED" for row in finite_fallback)
    claim_gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} for row in claim_gates)
    no_claim_promoted = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] == "GATE1272_5_contract_written"
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *derivation_attempt,
        *cell_tests,
        *parent_contract,
        *finite_fallback,
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
            "VAL1272_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1272_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1272_2_derivation_not_claimed",
            "radial-cell derivation result remains nonclaim",
            derivation_not_claimed,
            "RCD1272_7_verdict=PARENT_NECESSITY_NOT_DERIVED",
        ),
        validation_row(
            "VAL1272_3_cell_principle_matrix",
            "cell-principle matrix separates failing and conditional routes",
            configuration_cell_is_conditional and liouville_rejected,
            "configuration-cell normalization works only if parent-owned; canonical Liouville rejected",
        ),
        validation_row(
            "VAL1272_4_parent_contract",
            "parent necessity contract is explicit and not closed",
            contract_explicit and len(parent_contract) >= 8,
            f"parent_contract_rows={len(parent_contract)}",
        ),
        validation_row(
            "VAL1272_5_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows and fallback_locked,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1272_6_claim_gates_safe",
            "claim gates remain blocked except contract-written nonclaim gate",
            claim_gates_safe and no_claim_promoted,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1272_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1272_8_next_target_1273",
            "next target routes to parent H_core/radial-cell owner",
            next_target[0]["next_id"] == "NEXT1272_0_1273",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1272_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1272_10_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1272_11_overall",
            "overall 1272 validation",
            overall_pass,
            "1272 tries the radial-cell variational derivation, rejects generic Liouville as insufficient, keeps J_q=1 as a parent-owned contract rather than a proof, and routes to H_core/radial-cell owner next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1272 does not derive the local reciprocity/`R_AB` zero theorem from existing radial-cell material. The exact identity `R_AB=ln(T^2S)=2 ln(J_q)` is clean, and `J_q=1` would give the desired local-GR branch, but ordinary Liouville/phase-volume preservation only fixes `J_q J_p=1`, not `J_q=1`.

**Main progress:** the missing proof is now sharply located. The theory needs a parent-owned radial observer configuration-cell normalization, or an equivalent `L_core/H_core` clause, that makes `Lambda_R C_R` necessary instead of appended.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, zero-residual, or finite-`Z_R` row is claimed. The working statement is: `J_q=1` is the right mechanism if parent-signed, not yet a theorem.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Radial Cell Variational Derivation Attempt
{markdown_table(derivation_attempt, ["attempt_id", "input_principle", "local_equation", "variational_effect", "result", "blocker", "source_hint", "valid_for_claim", "claim_allowed"])}

## Cell Principle Test Matrix
{markdown_table(cell_tests, ["test_id", "candidate_principle", "derives_C_R_zero", "status", "reason", "next_use", "valid_for_claim", "claim_allowed"])}

## Parent Necessity Contract
{markdown_table(parent_contract, ["contract_id", "clause", "required_content", "current_evidence", "status", "missing_parent_input", "closes_zero_theorem", "valid_for_claim", "claim_allowed"])}

## Finite Source Fallback Status
{markdown_table(finite_fallback, ["fallback_id", "branch", "rows_seen", "accepted_ready", "status", "reason", "next_action", "valid_for_claim", "claim_allowed"])}

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
