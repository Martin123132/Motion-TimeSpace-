from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1266"
TITLE = "1266-Y5-R10-RAB-primitive-auxiliary-grammar-source-hunt-or-finite-ZR-intake-review"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SOURCE_HUNT_PATH = OUT_DIR / f"{PACK_ID}_PRIMITIVE_SOURCE_HUNT_LEDGER.csv"
AP_EVIDENCE_PATH = OUT_DIR / f"{PACK_ID}_AP1265_CLAUSE_EVIDENCE_MAP.csv"
PARENT_SCORECARD_PATH = OUT_DIR / f"{PACK_ID}_PARENT_ORIGIN_SCORECARD.csv"
FINITE_INTAKE_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_INTAKE_REVIEW.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1266_VALIDATION.csv"


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


def live_intake_counts() -> tuple[int, int, int]:
    raw_dir = RAB_INTAKE_DIR / "raw"
    accepted_dir = RAB_INTAKE_DIR / "accepted"
    docs_dir = RAB_INTAKE_DIR / "docs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    raw_rows = sum(len(read_csv(path)) for path in raw_dir.glob("*.csv"))
    accepted_rows = sum(len(read_csv(path)) for path in accepted_dir.glob("*.csv"))
    docs_rows = sum(len(read_csv(path)) for path in docs_dir.glob("*.csv"))
    return raw_rows, accepted_rows, docs_rows


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        SOURCE_HUNT_PATH,
        AP_EVIDENCE_PATH,
        PARENT_SCORECARD_PATH,
        FINITE_INTAKE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_rows, accepted_rows, docs_rows = live_intake_counts()

    source_register = [
        {
            "source_id": "SRC1266_0_1265_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_NEXT_TARGET.csv",
            "needle": "NEXT1265_0_1266",
            "purpose": "handoff to primitive auxiliary grammar source hunt",
            "claim_role": "handoff only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_1_1265_ap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv",
            "needle": "AP1265_0_auxiliary_signature",
            "purpose": "protection clauses that must be source-signed",
            "claim_role": "conditional target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_2_1265_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_AUXILIARY_ELIMINATION_THEOREM.csv",
            "needle": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "purpose": "exact conditional theorem requiring parent signature",
            "claim_role": "not claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_3_1265_finite_dryrun",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_FINITE_ZR_BOUND_RUNNER_DRYRUN.csv",
            "needle": "DR1265_0_intake_counts",
            "purpose": "finite residual runner state before 1266",
            "claim_role": "blocked baseline",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_4_motion_contract",
            "local_path": "01-motion-load-route-contract.md",
            "needle": "The contract is to derive `p=1`, not fit it.",
            "purpose": "primitive route requirement for local GR limit",
            "claim_role": "requirement source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_5_reciprocal_origin",
            "local_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "reciprocal_routing_parent_origin_partial_not_derived",
            "purpose": "reciprocity gives p=1 conditionally but origin is not derived",
            "claim_role": "blocker source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_6_source_neutrality",
            "local_path": "06-reciprocal-charge-source-neutrality.md",
            "needle": "R_AB is not a scalar hair mode at all.",
            "purpose": "cleaner constraint route and boundary/source neutrality target",
            "claim_role": "partial support",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_7_nonprop_constraint",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open",
            "purpose": "candidate nonpropagating R_AB constraint",
            "claim_role": "closure support only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_8_phase_volume",
            "local_path": "08-phase-volume-reciprocity-origin.md",
            "needle": "phase_volume_reciprocity_motivated_not_parent_derived",
            "purpose": "phase-volume motivation for lambda_R constraint",
            "claim_role": "motivation not proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_9_hamiltonian_cell",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "hamiltonian_radial_cell_sharpened_not_parent_derived",
            "purpose": "radial cell derivation sharpened but not parent-derived",
            "claim_role": "blocker source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_10_observer_map",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "observer_map_contract_written_not_satisfied",
            "purpose": "observer-map contract and acceptable parent routes",
            "claim_role": "contract unsatisfied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_11_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "ordinary conserved current leaves Q_R hair",
            "claim_role": "rejection source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_12_gauge_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "purpose": "Noether/gauge route audit and first-class constraint warning",
            "claim_role": "closure-only warning",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1266_13_finite_template",
            "local_path": "source-intake/rab-sector/docs/ZR1264_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1264_TEMPLATE_DO_NOT_SCORE",
            "purpose": "finite-ZR coefficient source-row template",
            "claim_role": "docs-only template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_hunt = [
        {
            "hunt_id": "HUNT1266_0_local_gr_contract",
            "source_id": "SRC1266_4_motion_contract",
            "candidate_source": "motion-load route requires derived p=1/gamma=1",
            "evidence_found": "sets the standard: p=1 must be derived, not fitted",
            "supports_ap_clauses": "none directly",
            "blocking_gap": "requirement only; no auxiliary grammar or lambda_R owner supplied",
            "status": "REQUIREMENT_NOT_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_1_reciprocal_origin",
            "source_id": "SRC1266_5_reciprocal_origin",
            "candidate_source": "reciprocity T^2 S=1 as parent origin",
            "evidence_found": "p=1 follows if reciprocity is exact",
            "supports_ap_clauses": "AP1265_2 conditionally",
            "blocking_gap": "reciprocity itself is explicitly not parent-derived",
            "status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_2_source_neutrality",
            "source_id": "SRC1266_6_source_neutrality",
            "candidate_source": "source neutrality Pi_R=0 -> Q_R=0",
            "evidence_found": "identifies the clean route where R_AB is constraint mode, not scalar hair",
            "supports_ap_clauses": "AP1265_3 partially",
            "blocking_gap": "Pi_R=0 and no boundary/source theorem are not parent-signed",
            "status": "PARTIAL_BOUNDARY_ROUTE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_3_nonpropagating_constraint",
            "source_id": "SRC1266_7_nonprop_constraint",
            "candidate_source": "S_constraint = integral lambda_R R_AB with no kinetic term",
            "evidence_found": "cleanly gives AB=1 if the multiplier is legitimate",
            "supports_ap_clauses": "AP1265_0; AP1265_1; AP1265_2",
            "blocking_gap": "parent origin of lambda_R remains open",
            "status": "BEST_CLOSURE_SUPPORT_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_4_phase_volume",
            "source_id": "SRC1266_8_phase_volume",
            "candidate_source": "phase-volume balance selects T^2 S=1",
            "evidence_found": "motivates radial observer-cell constraint",
            "supports_ap_clauses": "AP1265_0 weakly",
            "blocking_gap": "motivation does not prove parent variational multiplier",
            "status": "MOTIVATED_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_5_hamiltonian_cell",
            "source_id": "SRC1266_9_hamiltonian_cell",
            "candidate_source": "radial t-r Hamiltonian cell preservation",
            "evidence_found": "sharpens why a separate radial cell would force p=1",
            "supports_ap_clauses": "AP1265_0 weakly",
            "blocking_gap": "generic symplectic/Liouville preservation does not derive p=1",
            "status": "SHARPENED_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_6_observer_map_contract",
            "source_id": "SRC1266_10_observer_map",
            "candidate_source": "observer-map symplectic contract",
            "evidence_found": "states acceptable parent routes: genuine constraint or gauge redundancy",
            "supports_ap_clauses": "AP1265_0 route selector",
            "blocking_gap": "contract is written but not satisfied",
            "status": "CONTRACT_WRITTEN_NOT_SATISFIED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_7_cell_current",
            "source_id": "SRC1266_11_cell_current",
            "candidate_source": "conserved radial observer-cell current",
            "evidence_found": "ordinary current conservation gives W R_AB'=Q_R and exterior Q_R/r hair",
            "supports_ap_clauses": "none as theorem-zero",
            "blocking_gap": "does not prove Q_R=0; only recovers closure if constraint is inserted",
            "status": "DERIVATION_REJECTED_FOR_QR_HAIR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1266_8_gauge_noether",
            "source_id": "SRC1266_12_gauge_noether",
            "candidate_source": "Noether/gauge origin forbidding Q_R",
            "evidence_found": "first-class parent constraint remains possible in principle",
            "supports_ap_clauses": "AP1265_0 route selector",
            "blocking_gap": "Noether identity cannot replace a parent constraint; current scaffold is closure-only",
            "status": "NO_CURRENT_PRIMITIVE_SOURCE_FOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ap_evidence = [
        {
            "clause_id": "AP1265_0_auxiliary_signature",
            "1265_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "best_1266_evidence": "nonpropagating constraint and first-class constraint route are internally coherent",
            "source_ids": "SRC1266_7_nonprop_constraint; SRC1266_12_gauge_noether",
            "remaining_gap": "no parent primitive signs lambda_R as a genuine auxiliary/constraint owner",
            "updated_status": "SUPPORTED_AS_CLOSURE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_1_no_derivatives",
            "1265_status": "UNSIGNED_GRAMMAR_PROTECTION",
            "best_1266_evidence": "the clean closure intentionally removes the R_AB kinetic term",
            "source_ids": "SRC1266_7_nonprop_constraint; SRC1266_11_cell_current",
            "remaining_gap": "no parent object-language proof forbids D R_AB or vertical metric constructors",
            "updated_status": "PARTIAL_SUPPORT_NOT_GRAMMAR_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_2_eliminability",
            "1265_status": "EXACT_IF_AUXILIARY_BLOCK_IS_COMPLETE",
            "best_1266_evidence": "algebraic constraint would eliminate R_AB before readout",
            "source_ids": "SRC1266_2_1265_theorem; SRC1266_7_nonprop_constraint",
            "remaining_gap": "block completeness and absence of matter/source terms are not parent-signed",
            "updated_status": "EXACT_CONDITIONAL_STILL_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_3_boundary_silence",
            "1265_status": "UNSIGNED_BOUNDARY_PROTECTION",
            "best_1266_evidence": "source-neutrality route identifies Pi_R=0 -> Q_R=0 as required theorem",
            "source_ids": "SRC1266_6_source_neutrality; SRC1266_11_cell_current",
            "remaining_gap": "ordinary current conservation leaves Q_R hair; Pi_R=0 is not derived",
            "updated_status": "BOUNDARY_ZERO_NOT_PROVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_4_readout_stability",
            "1265_status": "UNSIGNED_READOUT_PROTECTION",
            "best_1266_evidence": "no primitive source in the local trail proves radiative/readout closure",
            "source_ids": "SRC1266_12_gauge_noether",
            "remaining_gap": "no theorem prevents readout/EFT regeneration of finite Z_R",
            "updated_status": "NO_PRIMITIVE_SOURCE_FOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_scorecard = [
        {
            "criterion_id": "PSC1266_0_lambda_owner",
            "criterion": "lambda_R is generated by the parent action, not inserted as closure",
            "best_evidence": "07 and 12 identify the correct multiplier/first-class route",
            "score": "PARTIAL_ROUTE_ONLY",
            "claim_blocker": "MISSING_PARENT_MULTIPLIER_ORIGIN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "PSC1266_1_operator_exclusion",
            "criterion": "parent grammar excludes R_AB derivative and kinetic operators",
            "best_evidence": "closure route excludes them by design",
            "score": "UNSIGNED",
            "claim_blocker": "MISSING_OBJECT_LANGUAGE_OPERATOR_BAN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "PSC1266_2_matter_descent",
            "criterion": "matter action descends through quotient variables and does not source R_AB",
            "best_evidence": "no direct source found in the primitive local trail",
            "score": "MISSING",
            "claim_blocker": "MISSING_MATTER_DESCENT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "PSC1266_3_boundary_nohair",
            "criterion": "boundary/corner sector has no R_AB charge or Pi_R source",
            "best_evidence": "06 states the Pi_R=0 route; 11 shows Q_R hair otherwise",
            "score": "MISSING",
            "claim_blocker": "MISSING_BOUNDARY_ZERO_THEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "PSC1266_4_current_or_gauge",
            "criterion": "current/Noether structure forbids reciprocal charge Q_R",
            "best_evidence": "11 rejects ordinary current; 12 rejects current scaffold as derivation",
            "score": "REJECTED_IN_CURRENT_FORM",
            "claim_blocker": "CURRENT_GIVES_WARD_IDENTITY_OR_QR_HAIR_NOT_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "criterion_id": "PSC1266_5_readout_stability",
            "criterion": "reduced/readout action cannot regenerate finite Z_R",
            "best_evidence": "1265 names the risk; 1266 found no primitive protection source",
            "score": "MISSING",
            "claim_blocker": "MISSING_READOUT_EFT_CLOSURE_THEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_intake = [
        {
            "review_id": "FZI1266_0_counts",
            "item": "live finite-ZR source rows",
            "status": "NO_LIVE_ROWS",
            "details": f"raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "review_id": "FZI1266_1_required_coefficients",
            "item": "Z_R, M_R^2, J_R, B_R coefficient source rows",
            "status": "MISSING_PARENT_INPUTS",
            "details": "no accepted numeric/theorem-zero source row for finite R_AB residuals",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "review_id": "FZI1266_2_arena_projection",
            "item": "R10/PPN/clock/orbital projection weights",
            "status": "MISSING_ARENA_PROJECTIONS",
            "details": "tau_R10, tau_PPN, tau_clock, and tau_orbital are not sourced",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "review_id": "FZI1266_3_template_state",
            "item": "docs-only finite-ZR template",
            "status": "TEMPLATE_ONLY_DO_NOT_SCORE",
            "details": "ZR1264 template remains nonclaim and contains MISSING_* placeholders",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1266_0_aux_theorem",
            "claim": "R_AB auxiliary theorem closes Z_R=0",
            "status": "BLOCKED",
            "reason": "source hunt found closure support but no parent primitive signing AP1265_0 through AP1265_4",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1266_1_current_nohair",
            "claim": "radial observer-cell current derives Q_R=0",
            "status": "BLOCKED",
            "reason": "ordinary current conservation leaves Q_R hair; Noether route needs a real constraint first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1266_2_finite_runner",
            "claim": "finite-ZR residual runner can score local tests",
            "status": "BLOCKED",
            "reason": "no accepted finite coefficient rows and no arena projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1266_3_local_gr",
            "claim": "local GR/Newton/R10/PPN pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor finite-residual branch is source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1266_0_source_hunt_result",
            "decision": "primitive source hunt did not sign the AP1265 auxiliary grammar",
            "because": "the trail repeatedly motivates the nonpropagating constraint but marks parent origin, current no-hair, boundary silence, and readout stability as open",
            "status": "PARENT_SOURCE_NOT_FOUND",
            "next_action": "do not claim theorem-zero; either construct a new first-class constrained parent action or use finite residual source acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1266_1_best_derivation_route",
            "decision": "stop repeating ordinary current conservation as the derivation route",
            "because": "11 and 12 show ordinary current/Noether identities give Q_R hair or Ward identities unless a constraint already exists",
            "status": "ROUTE_NARROWED",
            "next_action": "try an explicit first-class R_AB parent constraint with Dirac/constraint checks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1266_2_finite_residual_route",
            "decision": "finite-ZR source intake remains the empirical fallback",
            "because": "if the parent constraint cannot be signed, R_AB must be treated as a possible small residual and bounded",
            "status": "FALLBACK_READY_AS_SCHEMA_ONLY",
            "next_action": "fill source-backed Z_R/M_R2/J_R/B_R and arena projection rows before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1266_3_project_meaning",
            "decision": "the local branch is not dead; the missing object is now sharply localized",
            "because": "the gap has been reduced to a specific coupling/constraint owner problem rather than a vague local-GR hope",
            "status": "PRIVATE_PROGRESS_NOT_PUBLIC_CLAIM",
            "next_action": "attack the parent constraint syntax next",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1266_0_1267",
            "target_file": "1267-Y5-R10-first-class-RAB-parent-constraint-synthesis-or-finite-ZR-source-acquisition.md",
            "target_script": "scripts/Y5_R10_first_class_RAB_parent_constraint_synthesis_or_finite_ZR_source_acquisition.py",
            "task": "try to synthesize an explicit first-class parent constraint that owns lambda_R, forbids R_AB derivatives, descends through matter/boundary/readout, and closes AP1265; if it fails, start finite-ZR source acquisition",
            "success_condition": "AP1265_0 through AP1265_4 are signed by a concrete parent action check, or finite-ZR acquisition rows are prepared as nonclaim inputs",
            "do_not": "do not treat the closure benchmark or ordinary current conservation as a derived local-GR result",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (SOURCE_HUNT_PATH, source_hunt),
        (AP_EVIDENCE_PATH, ap_evidence),
        (PARENT_SCORECARD_PATH, parent_scorecard),
        (FINITE_INTAKE_PATH, finite_intake),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    ap_ids = {row["clause_id"] for row in ap_evidence}
    expected_ap_ids = {
        "AP1265_0_auxiliary_signature",
        "AP1265_1_no_derivatives",
        "AP1265_2_eliminability",
        "AP1265_3_boundary_silence",
        "AP1265_4_readout_stability",
    }
    all_generated_rows = [
        *source_register,
        *source_hunt,
        *ap_evidence,
        *parent_scorecard,
        *finite_intake,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    finite_blocked = all(is_false(row["runner_eligible"]) for row in finite_intake) and raw_rows == 0 and accepted_rows == 0
    claim_gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    source_hunt_not_claimable = all(is_false(row["valid_for_claim"]) for row in source_hunt) and any(
        row["status"] == "NO_CURRENT_PRIMITIVE_SOURCE_FOUND" for row in source_hunt
    )
    scorecard_has_blockers = all(str(row["claim_blocker"]).startswith("MISSING") or "HAIR" in str(row["claim_blocker"]) for row in parent_scorecard)
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
            "VAL1266_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1266_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1266_2_ap_clause_coverage",
            "all AP1265 clauses have 1266 evidence mapping",
            ap_ids == expected_ap_ids,
            f"covered={len(ap_ids)}; missing={sorted(expected_ap_ids - ap_ids)}",
        ),
        validation_row(
            "VAL1266_3_source_hunt_nonclaim",
            "primitive source hunt remains nonclaim and records missing source",
            source_hunt_not_claimable,
            f"source_hunt_rows={len(source_hunt)}",
        ),
        validation_row(
            "VAL1266_4_parent_scorecard_blocked",
            "parent origin scorecard has explicit blockers",
            scorecard_has_blockers,
            f"scorecard_rows={len(parent_scorecard)}",
        ),
        validation_row(
            "VAL1266_5_finite_intake_blocked",
            "finite-ZR intake is not runner eligible",
            finite_blocked,
            f"raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}",
        ),
        validation_row(
            "VAL1266_6_claim_gates",
            "all claim gates remain blocked",
            claim_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1266_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1266_8_next_target_1267",
            "next target routes to first-class parent constraint or finite-ZR acquisition",
            next_target[0]["next_id"] == "NEXT1266_0_1267",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1266_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1266_10_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1266_11_overall",
            "overall 1266 validation",
            overall_pass,
            "1266 finds no primitive parent source for the R_AB auxiliary grammar; theorem-zero remains blocked and the best next move is first-class parent constraint synthesis or finite-ZR acquisition",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1266 is a useful narrowing, not a local-GR win. The existing corpus supports the nonpropagating `R_AB` constraint as the clean closure benchmark, but it does not yet parent-sign the auxiliary grammar. The missing object is now precise: a parent-owned `lambda_R`/first-class constraint that forbids `R_AB` derivatives, boundary hair, matter sourcing, and readout regeneration.

**Main progress:** the source hunt separates genuine support from wishful closure. `R_AB=0` remains the right target for a derived GR/Newton limit, but ordinary current conservation and simple Noether wording do not prove it because they leave `Q_R` hair or require the constraint first.

**No-claim guard:** no `Z_R=0`, local-GR/Newton, R10, PPN, clock, or orbital claim is made. Finite-`Z_R` scoring remains blocked because there are no accepted coefficient rows or arena projections.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "claim_role", "valid_for_claim", "claim_allowed"])}

## Primitive Source Hunt Ledger
{markdown_table(source_hunt, ["hunt_id", "candidate_source", "evidence_found", "supports_ap_clauses", "blocking_gap", "status", "valid_for_claim", "claim_allowed"])}

## AP1265 Clause Evidence Map
{markdown_table(ap_evidence, ["clause_id", "1265_status", "best_1266_evidence", "remaining_gap", "updated_status", "valid_for_claim", "claim_allowed"])}

## Parent Origin Scorecard
{markdown_table(parent_scorecard, ["criterion_id", "criterion", "best_evidence", "score", "claim_blocker", "valid_for_claim", "claim_allowed"])}

## Finite Z_R Intake Review
{markdown_table(finite_intake, ["review_id", "item", "status", "details", "runner_eligible", "valid_for_claim", "claim_allowed"])}

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
