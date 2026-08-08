from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_source_backed_edge_row_scout_completed_Qedge_null_action_clause_unsigned_no_claim_rows_found_nonclaim"
CLAIM_CEILING = "source_backed_edge_row_scout_and_Qedge_null_clause_audit_only_no_Qedge_zero_no_R10_no_R11_no_PPN_no_local_GR_claim"
NEXT_TARGET = "676-Y5-R10-Qedge-null-clause-minimal-parent-action-or-first-source-row.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_PATH = ROOT / "675-Y5-R10-source-backed-edge-row-scout-or-Qedge-null-action-clause.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

BAD_MARKERS = (
    "MISSING",
    "DIAGNOSTIC",
    "SMOKE",
    "TEMPLATE",
    "NONCLAIM",
    "NON-CLAIM",
    "PLACEHOLDER",
    "REFERENCE_ONLY",
    "UNSIGNED",
    "NOT_SIGNED",
    "NOT_DERIVED",
    "NOT_CLOSED",
    "CONDITIONAL",
    "FAIL",
    "BLOCKED",
)

SOURCE_PATHS = {
    "222_doc": ROOT / "222-parent-X-sector-degree-count-and-boundary-action.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "544_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "589_validation": RESIDUALS / "P8_Y5_BRR545_589_VALIDATION.csv",
    "589_template": RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv",
    "590_validation": RESIDUALS / "P8_Y5_BRR545_590_VALIDATION.csv",
    "590_status": RESIDUALS / "P8_Y5_R10_590_EDGE_ROW_SOURCE_STATUS.csv",
    "591_validation": RESIDUALS / "P8_Y5_BRR545_591_VALIDATION.csv",
    "591_status": RESIDUALS / "P8_Y5_R10_591_EDGE_SOURCE_INPUT_STATUS.csv",
    "592_validation": RESIDUALS / "P8_Y5_BRR545_592_VALIDATION.csv",
    "592_plan": RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
    "593_validation": RESIDUALS / "P8_Y5_BRR545_593_VALIDATION.csv",
    "593_inputs": RESIDUALS / "P8_Y5_R10_593_EDGE_COEFFICIENT_INPUT_ROWS.csv",
    "583_template": RESIDUALS / "P8_Y5_R10_583_EDGE_ALPHA_TEMPLATE.csv",
    "586_prior_grid": RESIDUALS / "P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv",
    "588_budget": RESIDUALS / "P8_Y5_R10_588_EDGE_PRODUCT_FACTOR_BUDGET.csv",
    "621_doc": ROOT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "622_doc": ROOT / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "629_validation": RESIDUALS / "P8_Y5_BRR545_629_VALIDATION.csv",
    "629_source_search": RESIDUALS / "P8_Y5_R10_629_SOURCE_SEARCH_STATUS.csv",
    "629_curve_audit": RESIDUALS / "P8_Y5_R10_629_R10_CURVE_PROMOTION_AUDIT.csv",
    "bound_live": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "bound_review": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
    "667_validation": RESIDUALS / "P8_Y5_BRR545_667_VALIDATION.csv",
    "667_ansatz": RESIDUALS / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_variation": RESIDUALS / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "668_validation": RESIDUALS / "P8_Y5_BRR545_668_VALIDATION.csv",
    "668_boundary_lock": RESIDUALS / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
    "670_validation": RESIDUALS / "P8_Y5_BRR545_670_VALIDATION.csv",
    "670_no_pole": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "672_validation": RESIDUALS / "P8_Y5_BRR545_672_VALIDATION.csv",
    "672_source_plan": RESIDUALS / "P8_Y5_R10_672_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
    "673_validation": RESIDUALS / "P8_Y5_BRR545_673_VALIDATION.csv",
    "673_pim_audit": RESIDUALS / "P8_Y5_R10_673_HAMILTONIAN_PIM_ORTHOGONALITY_PROOF_AUDIT.csv",
    "673_acquisition": RESIDUALS / "P8_Y5_R10_673_EDGE_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "674_doc": ROOT / "674-Y5-R10-edge-coefficient-row-fill-or-parent-PiM-clause.md",
    "674_validation": RESIDUALS / "P8_Y5_BRR545_674_VALIDATION.csv",
    "674_parent_clause": RESIDUALS / "P8_Y5_R10_674_PARENT_PIM_CLAUSE_TEST.csv",
    "674_requirements": RESIDUALS / "P8_Y5_R10_674_COEFFICIENT_REQUIREMENTS.csv",
    "674_row_pack": RESIDUALS / "P8_Y5_R10_674_EDGE_ROW_FILL_PACK.csv",
    "674_bound_gate": RESIDUALS / "P8_Y5_R10_674_BOUND_CURVE_STATUS_GATE.csv",
    "674_decision": RESIDUALS / "P8_Y5_R10_674_DECISION.csv",
}

SCOUT_FACTORS = {
    "lambda_edge": ["lambda_edge", "lambda_m", "lambda_value", "edge_range", "F_lambda"],
    "K_edge": ["K_edge", "edge kernel", "kernel normalization"],
    "Qbar_edge_XH": ["Qbar_edge_XH", "Q_edge", "Pi_M^H", "Hamiltonian projection"],
    "qbar_XT": ["qbar_XT", "test-body", "matter quotient", "matter response"],
    "B_X_boundary_momentum": ["B_X", "boundary momentum", "boundary primitive"],
    "M_H_ref": ["M_H_ref", "M_H", "Hamiltonian source mass"],
    "alpha_bound_lambda": ["alpha_bound", "alpha_edge_ceiling", "review_candidate_alpha_bound"],
    "alpha_edge_formula": ["alpha_edge", "alpha_predicted", "K_edge*Qbar_edge_XH*qbar_XT"],
}

SCOUT_SOURCE_IDS = [
    "583_template",
    "586_prior_grid",
    "588_budget",
    "589_template",
    "590_status",
    "591_status",
    "592_plan",
    "593_inputs",
    "671_edge",
    "672_source_plan",
    "673_acquisition",
    "674_requirements",
    "674_row_pack",
    "674_bound_gate",
    "bound_live",
    "bound_review",
]


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def row_text(row: dict[str, str]) -> str:
    return " ".join(str(value) for value in row.values())


def has_bad_marker(text: str) -> bool:
    upper = text.upper()
    return any(marker in upper for marker in BAD_MARKERS)


def is_claim_valid(row: dict[str, str]) -> bool:
    if row.get("valid_for_claim", "").strip().lower() != "true":
        return False
    return not has_bad_marker(row_text(row))


def numeric_rows(path: Path, required_columns: tuple[str, ...]) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    rows = read_csv(path)
    numeric_count = 0
    claim_count = 0
    for row in rows:
        if row.get("valid_for_claim", "").lower() == "true":
            claim_count += 1
        try:
            values = [float(row[column]) for column in required_columns]
        except (KeyError, TypeError, ValueError):
            continue
        if all(value > 0 for value in values):
            numeric_count += 1
    return numeric_count, claim_count


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "222_doc": "early parent X-sector and boundary action formula source",
        "235_doc": "projector stress / boundary B_X formula source",
        "539_doc": "Hamiltonian Pi_M candidate definition",
        "544_status": "boundary/reference first-row missing status",
        "589_validation": "589 validation gate",
        "589_template": "source-backed edge product row template",
        "590_validation": "590 validation gate",
        "590_status": "edge row source status",
        "591_validation": "591 validation gate",
        "591_status": "edge source input status",
        "592_validation": "592 validation gate",
        "592_plan": "edge coefficient source plan",
        "593_validation": "593 validation gate",
        "593_inputs": "edge coefficient input rows",
        "583_template": "edge alpha template",
        "586_prior_grid": "private edge numeric prior grid",
        "588_budget": "edge product factor budget",
        "621_doc": "matter quotient/coupling normal-form context",
        "622_doc": "parent matter sector contract context",
        "629_validation": "629 validation gate",
        "629_source_search": "R10 source search status",
        "629_curve_audit": "R10 curve promotion audit",
        "bound_live": "live digitized R10 bound curve file",
        "bound_review": "private vector review candidate curve",
        "667_validation": "667 validation gate",
        "667_ansatz": "explicit parent boundary action ansatz",
        "667_variation": "parent variation ledger",
        "668_validation": "668 validation gate",
        "668_boundary_lock": "boundary condition lock",
        "670_validation": "670 validation gate",
        "670_no_pole": "no-pole quotient proof chain",
        "671_validation": "671 validation gate",
        "671_edge": "edge residual vector",
        "672_validation": "672 validation gate",
        "672_source_plan": "edge coefficient source plan",
        "673_validation": "673 validation gate",
        "673_pim_audit": "Hamiltonian Pi_M orthogonality audit",
        "673_acquisition": "edge coefficient acquisition ledger",
        "674_doc": "immediate predecessor checkpoint",
        "674_validation": "674 validation gate",
        "674_parent_clause": "parent PiM clause test",
        "674_requirements": "edge coefficient requirements",
        "674_row_pack": "edge row fill pack",
        "674_bound_gate": "bound curve status gate",
        "674_decision": "674 decision rows",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def qedge_null_clause_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "QNA675_0_boundary_exact_parent_action",
            "candidate_clause": "edge sector is an exact boundary term with no compact linked charge",
            "mathematical_form": "S_edge=int_boundary dB_edge, Q_edge=int_boundary epsilon B_edge=0",
            "acceptance_test": "B_edge is parent-owned, exact on the allowed boundary class, and does not remove physical ADM/time charge",
            "current_result": "not_signed",
            "blocker": "B_X/B_edge formula exists only as candidate boundary momentum, not as a parent-fixed exact class",
            "repair_or_source": "derive B_edge=d_boundary b_edge with fixed class, or source B_X_boundary_momentum",
            "valid_for_claim": "false",
            "source_paths": source_list("222_doc", "235_doc", "667_variation", "668_boundary_lock", "674_parent_clause"),
            "generated_utc": now,
        },
        {
            "clause_id": "QNA675_1_quotient_null_edge",
            "candidate_clause": "edge direction is removed before variation by the physical quotient",
            "mathematical_form": "S_parent=S_red[q(Phi)], Dq[v_edge]=0, delta_edge S_parent=0",
            "acceptance_test": "same q owns field equations, matter readout, boundary class, and Pi_M projection",
            "current_result": "conditional_not_parent_complete",
            "blocker": "quotient route gives useful verticality but not the full measured edge charge zero",
            "repair_or_source": "construct full q including boundary domain, or source K_edge/Qbar_edge",
            "valid_for_claim": "false",
            "source_paths": source_list("670_no_pole", "671_edge", "672_source_plan", "674_parent_clause"),
            "generated_utc": now,
        },
        {
            "clause_id": "QNA675_2_Hamiltonian_PiM_annihilator",
            "candidate_clause": "Hamiltonian mass projector annihilates the edge charge",
            "mathematical_form": "Pi_M^H[Q_edge^H(lambda)]=0",
            "acceptance_test": "mass representative, edge representative, fixed reference, and source frame are all parent-owned",
            "current_result": "not_derived",
            "blocker": "673/674 keep Pi_M orthogonality unsigned",
            "repair_or_source": "derive mass-cohomology complement or source Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "673_pim_audit", "674_parent_clause", "544_status"),
            "generated_utc": now,
        },
        {
            "clause_id": "QNA675_3_matter_blindness",
            "candidate_clause": "matter/test bodies are blind to edge after quotient",
            "mathematical_form": "S_matter=Sbar[q(Phi),psi,theta_obs], qbar_XT=0",
            "acceptance_test": "matter functor uses only observed quotient variables in the same frame before fitting",
            "current_result": "not_closed",
            "blocker": "matter-coupling normal form exists as a route, not a signed qbar_XT theorem",
            "repair_or_source": "derive qbar_XT=0 or source composition/readout response",
            "valid_for_claim": "false",
            "source_paths": source_list("621_doc", "622_doc", "674_requirements"),
            "generated_utc": now,
        },
        {
            "clause_id": "QNA675_4_empirical_row_escape_hatch",
            "candidate_clause": "if Qedge cannot be killed, fill a source-backed edge product row",
            "mathematical_form": "alpha_edge(lambda)=K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT",
            "acceptance_test": "all factors have numeric/theorem-zero source rows and live alpha_bound(lambda) is promoted",
            "current_result": "no_claim_valid_row_found",
            "blocker": "old rows are templates, diagnostics, budgets, priors, or placeholders",
            "repair_or_source": "source first real row or keep branch blocked",
            "valid_for_claim": "false",
            "source_paths": source_list("589_template", "590_status", "591_status", "592_plan", "593_inputs", "674_row_pack"),
            "generated_utc": now,
        },
        {
            "clause_id": "QNA675_5_verdict",
            "candidate_clause": "Qedge null action clause closes R10 edge branch",
            "mathematical_form": "QNA675_0 through QNA675_3 jointly imply alpha_edge(lambda)=0",
            "acceptance_test": "all clauses pass without missing/conditional/source placeholders",
            "current_result": "failed_for_current_claim",
            "blocker": "the parent-owned boundary representative is still the missing hinge",
            "repair_or_source": "676 must either construct that parent action clause or source the first edge row",
            "valid_for_claim": "false",
            "source_paths": source_list("674_decision", "674_validation"),
            "generated_utc": now,
        },
    ]


def scout_factor_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []
    for factor, patterns in SCOUT_FACTORS.items():
        candidate_files: set[str] = set()
        candidate_rows = 0
        claim_valid_rows = 0
        blocked_reasons: set[str] = set()
        examples: list[str] = []
        for source_id in SCOUT_SOURCE_IDS:
            path = SOURCE_PATHS[source_id]
            if not path.exists() or path.suffix.lower() != ".csv":
                continue
            for index, row in enumerate(read_csv(path), start=1):
                text = row_text(row)
                if any(pattern.lower() in text.lower() for pattern in patterns):
                    candidate_files.add(source_id)
                    candidate_rows += 1
                    if len(examples) < 4:
                        examples.append(f"{source_id}:row{index}")
                    if is_claim_valid(row):
                        claim_valid_rows += 1
                    else:
                        upper = text.upper()
                        if row.get("valid_for_claim", "").lower() != "true":
                            blocked_reasons.add("valid_for_claim_false_or_absent")
                        if any(marker in upper for marker in ("MISSING", "PLACEHOLDER")):
                            blocked_reasons.add("missing_or_placeholder")
                        if any(marker in upper for marker in ("DIAGNOSTIC", "SMOKE", "PRIOR", "BUDGET")):
                            blocked_reasons.add("diagnostic_or_prior_only")
                        if any(marker in upper for marker in ("CONDITIONAL", "NOT_DERIVED", "NOT_SIGNED", "UNSIGNED", "FAIL", "BLOCKED")):
                            blocked_reasons.add("theorem_unsigned_or_blocked")
        rows.append(
            {
                "factor_id": f"SBS675_{len(rows)}_{factor}",
                "factor": factor,
                "patterns": ";".join(patterns),
                "candidate_files": ";".join(sorted(candidate_files)),
                "candidate_rows_found": str(candidate_rows),
                "claim_valid_rows_found": str(claim_valid_rows),
                "status": "source_backed_claim_row_found_REVIEW_BEFORE_USE" if claim_valid_rows else "no_claim_valid_source_row_found",
                "blocked_reasons": ";".join(sorted(blocked_reasons)) if blocked_reasons else "none",
                "example_hits": ";".join(examples),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def blocker_matrix_rows(scout_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []
    for row in scout_rows:
        factor = row["factor"]
        claim_rows = int(row["claim_valid_rows_found"])
        rows.append(
            {
                "blocker_id": f"EBM675_{len(rows)}_{factor}",
                "factor": factor,
                "current_status": "open" if claim_rows == 0 else "review_candidate",
                "blocks": "alpha_edge(lambda);R10_comparator;local_edge_branch",
                "minimum_repair": repair_for_factor(factor),
                "why_not_claim": "no source-backed claim-valid row found in local scout" if claim_rows == 0 else "candidate found but 675 does not promote automatically",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def repair_for_factor(factor: str) -> str:
    repairs = {
        "lambda_edge": "derive edge support/range or provide positive length envelope with source path",
        "K_edge": "derive parent boundary kernel normalization or prove edge kernel inactive",
        "Qbar_edge_XH": "derive Pi_M^H[Q_edge]=0 or source Hamiltonian projection numerator/denominator",
        "qbar_XT": "derive same-frame matter quotient blindness or source test-body response",
        "B_X_boundary_momentum": "derive parent boundary representative/counterterm or source boundary momentum",
        "M_H_ref": "derive same-frame Hamiltonian source mass and fixed reference denominator",
        "alpha_bound_lambda": "promote live digitized bound curve from source-backed QA, not review candidate",
        "alpha_edge_formula": "fill all active factors and declare Yukawa/envelope force-law mapping",
    }
    return repairs[factor]


def pressure_status_rows() -> list[dict[str, str]]:
    now = generated_utc()
    live_numeric, live_claim = numeric_rows(SOURCE_PATHS["bound_live"], ("lambda_value", "alpha_bound"))
    review_numeric, review_claim = numeric_rows(SOURCE_PATHS["bound_review"], ("lambda_value", "alpha_bound"))
    prior_rows = len(read_csv(SOURCE_PATHS["586_prior_grid"])) if SOURCE_PATHS["586_prior_grid"].exists() else 0
    budget_rows = len(read_csv(SOURCE_PATHS["588_budget"])) if SOURCE_PATHS["588_budget"].exists() else 0
    return [
        {
            "pressure_id": "PS675_0_live_bound_curve",
            "artifact": str(SOURCE_PATHS["bound_live"]),
            "numeric_rows": str(live_numeric),
            "claim_rows": str(live_claim),
            "status": "not_ready_for_claim",
            "use_allowed": "schema/protection_check_only",
            "valid_for_claim": "false",
            "source_paths": source_list("bound_live", "629_curve_audit"),
            "generated_utc": now,
        },
        {
            "pressure_id": "PS675_1_review_candidate_curve",
            "artifact": str(SOURCE_PATHS["bound_review"]),
            "numeric_rows": str(review_numeric),
            "claim_rows": str(review_claim),
            "status": "private_pressure_wall_only",
            "use_allowed": "private coefficient pressure estimates, not claim scoring",
            "valid_for_claim": "false",
            "source_paths": source_list("bound_review", "629_source_search", "629_curve_audit"),
            "generated_utc": now,
        },
        {
            "pressure_id": "PS675_2_old_prior_and_budget_rows",
            "artifact": "P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv;P8_Y5_R10_588_EDGE_PRODUCT_FACTOR_BUDGET.csv",
            "numeric_rows": str(prior_rows + budget_rows),
            "claim_rows": "0",
            "status": "diagnostic_only",
            "use_allowed": "pressure intuition only; replace with source-backed factors",
            "valid_for_claim": "false",
            "source_paths": source_list("586_prior_grid", "588_budget"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    qedge_rows: list[dict[str, str]],
    scout_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    qedge_claim_rows = sum(1 for row in qedge_rows if row["valid_for_claim"] == "true")
    scout_claim_candidates = sum(int(row["claim_valid_rows_found"]) for row in scout_rows)
    pressure_claim_rows = sum(int(row["claim_rows"]) for row in pressure_rows)
    return [
        {
            "evaluator_id": "EV675_0_Qedge_null_clause",
            "target": "derive Qedge null parent action clause",
            "status": "fail_nonclaim",
            "reason": f"qedge_claim_rows={qedge_claim_rows}; parent-owned boundary representative still missing",
            "claim_effect": "Qedge_zero and Qbar_edge_zero remain false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV675_1_source_backed_scout",
            "target": "find source-backed edge row inputs",
            "status": "blocked_nonclaim",
            "reason": f"claim_valid_factor_rows_found={scout_claim_candidates}",
            "claim_effect": "edge row remains unfilled",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV675_2_pressure_artifacts",
            "target": "use existing curves/priors",
            "status": "pass_nonclaim",
            "reason": f"pressure_claim_rows={pressure_claim_rows}; review curve and priors stay private diagnostic only",
            "claim_effect": "no R10 evidence promoted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV675_3_next",
            "target": "select next target",
            "status": "minimal_parent_Qedge_clause_or_first_source_row",
            "reason": "the branch needs either a real null-edge action clause or one first source-backed coefficient row",
            "claim_effect": "next private checkpoint only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D675_0_Qedge_null_clause",
            "target": "Qedge=0 from parent action",
            "result": "not_signed",
            "reason": "no parent-owned exact boundary representative plus mass-projector annihilator exists yet",
            "next_action": "try minimal parent action clause only if it fixes B_edge and boundary class explicitly",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D675_1_source_backed_row",
            "target": "first edge source row",
            "result": "not_found",
            "reason": "local scout found templates, diagnostics, priors, and blockers, but no claim-valid source-backed factor row",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D675_2_no_promotion",
            "target": "R10/R11/PPN/local-GR claims",
            "result": "blocked",
            "reason": "Qedge not zero and alpha_edge row lacks source-backed inputs",
            "next_action": "continue private derivation/source-scouting",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "NCS675_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Qedge null action clause unsigned and no source-backed edge row found",
            "blocked_claims": "Qedge_zero;Qbar_edge_zero;R10;R11;PPN;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    scout_rows: list[dict[str, str]],
    blocker_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    rows.append(
        {
            "check_id": "V675_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
            "generated_utc": now,
        }
    )

    validation_ids = [
        "589_validation",
        "590_validation",
        "591_validation",
        "592_validation",
        "593_validation",
        "629_validation",
        "667_validation",
        "668_validation",
        "670_validation",
        "671_validation",
        "672_validation",
        "673_validation",
        "674_validation",
    ]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append(
        {
            "check_id": "V675_1_prior_validations_clean",
            "result": "pass" if all(count == 0 for count in prior_failures.values()) else "fail",
            "detail": ";".join(f"{source_id}={count}" for source_id, count in prior_failures.items()),
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V675_2_Qedge_null_clause_coverage",
            "result": "pass" if len(qedge_rows) >= 6 else "fail",
            "detail": f"qedge_clause_rows={len(qedge_rows)}",
            "generated_utc": now,
        }
    )

    qedge_promoted = [row for row in qedge_rows if row["valid_for_claim"] == "true"]
    rows.append(
        {
            "check_id": "V675_3_Qedge_not_promoted",
            "result": "pass" if not qedge_promoted and any(row["current_result"] == "failed_for_current_claim" for row in qedge_rows) else "fail",
            "detail": "Qedge null clause remains unsigned and nonclaim",
            "generated_utc": now,
        }
    )

    covered_factors = {row["factor"] for row in scout_rows}
    rows.append(
        {
            "check_id": "V675_4_scout_factor_coverage",
            "result": "pass" if set(SCOUT_FACTORS).issubset(covered_factors) else "fail",
            "detail": "missing=" + ";".join(sorted(set(SCOUT_FACTORS) - covered_factors)),
            "generated_utc": now,
        }
    )

    claim_valid_scout_rows = sum(int(row["claim_valid_rows_found"]) for row in scout_rows)
    rows.append(
        {
            "check_id": "V675_5_no_source_backed_edge_rows_found",
            "result": "pass" if claim_valid_scout_rows == 0 else "fail",
            "detail": f"claim_valid_scout_rows={claim_valid_scout_rows}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V675_6_blocker_matrix_complete",
            "result": "pass" if len(blocker_rows) == len(SCOUT_FACTORS) and all(row["valid_for_claim"] == "false" for row in blocker_rows) else "fail",
            "detail": f"blocker_rows={len(blocker_rows)}",
            "generated_utc": now,
        }
    )

    pressure_claim_rows = sum(int(row["claim_rows"]) for row in pressure_rows)
    rows.append(
        {
            "check_id": "V675_7_pressure_artifacts_nonclaim",
            "result": "pass" if pressure_claim_rows == 0 and any(int(row["numeric_rows"]) > 0 for row in pressure_rows) else "fail",
            "detail": f"pressure_claim_rows={pressure_claim_rows}",
            "generated_utc": now,
        }
    )

    generated = qedge_rows + scout_rows + blocker_rows + pressure_rows + evaluator + decision
    claim_rows = [row for row in generated if row.get("valid_for_claim") == "true"]
    rows.append(
        {
            "check_id": "V675_8_no_claim_rows_promoted",
            "result": "pass" if not claim_rows else "fail",
            "detail": "all generated rows remain valid_for_claim=false" if not claim_rows else f"claim_rows={len(claim_rows)}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V675_9_next_target_selected",
            "result": "pass" if any(row["next_action"] == NEXT_TARGET for row in decision) else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        }
    )

    output_paths = [
        RESIDUALS / "P8_Y5_R10_675_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_675_QEDGE_NULL_ACTION_CLAUSE_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_675_SOURCE_BACKED_EDGE_ROW_SCOUT.csv",
        RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
        RESIDUALS / "P8_Y5_R10_675_PRESSURE_ONLY_STATUS.csv",
        RESIDUALS / "P8_Y5_R10_675_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_675_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_675_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append(
        {
            "check_id": "V675_10_generated_outputs_scoped",
            "result": "pass" if all(str(path).startswith(str(ROOT)) for path in output_paths) else "fail",
            "detail": "all 675 outputs target post-checkpoint-work",
            "generated_utc": now,
        }
    )

    changed_count = formalization_changed_count()
    rows.append(
        {
            "check_id": "V675_11_formalization_workbench_untouched",
            "result": "pass" if changed_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed_count}",
            "generated_utc": now,
        }
    )

    rows.append(
        {
            "check_id": "V675_12_status_nonclaim",
            "result": "pass" if "no_Qedge_zero" in CLAIM_CEILING and "no_R10" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        }
    )

    evaluator_statuses = [row["status"] for row in evaluator]
    rows.append(
        {
            "check_id": "V675_13_evaluator_nonclaim_passes",
            "result": "pass" if all("claim" in status or status == "minimal_parent_Qedge_clause_or_first_source_row" for status in evaluator_statuses) else "fail",
            "detail": ";".join(evaluator_statuses),
            "generated_utc": now,
        }
    )

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    scout_rows: list[dict[str, str]],
    blocker_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    evaluator: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 675 - Y5 R10 Source-Backed Edge Row Scout Or Qedge Null Action Clause

## Verdict

675 did two things in the right order.

First it tried the theorem route:

```text
S_edge = int_boundary dB_edge
Dq[v_edge] = 0
Pi_M^H[Q_edge^H(lambda)] = 0
```

That still does not close, because the parent-owned boundary representative and mass-projector annihilator are not signed.

Second it scouted the local corpus for source-backed edge row inputs. It found templates, diagnostic budgets, private priors, and review-curve pressure rows — but no claim-valid source-backed row for `lambda_edge`, `K_edge`, `Qbar_edge_XH`, `qbar_XT`, `B_X`, `M_H_ref`, or the live R10 bound curve.

So the branch stays blocked but cleaner: the next target must either write a real minimal `Q_edge` null action clause, or source one first coefficient row honestly.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Qedge Null Action Clause Audit

{markdown_table(qedge_rows, ["clause_id", "candidate_clause", "mathematical_form", "acceptance_test", "current_result", "blocker", "repair_or_source", "valid_for_claim"])}

## Source-Backed Edge Row Scout

{markdown_table(scout_rows, ["factor_id", "factor", "candidate_files", "candidate_rows_found", "claim_valid_rows_found", "status", "blocked_reasons", "example_hits", "valid_for_claim"])}

## Edge Row Blocker Matrix

{markdown_table(blocker_rows, ["blocker_id", "factor", "current_status", "blocks", "minimum_repair", "why_not_claim", "valid_for_claim"])}

## Pressure-Only Status

{markdown_table(pressure_rows, ["pressure_id", "artifact", "numeric_rows", "claim_rows", "status", "use_allowed", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default route: do not keep circling old diagnostic rows. Either construct a minimal parent action clause that explicitly owns `B_edge` and kills `Q_edge`, or source the first real edge coefficient row with units, source path, and no missing markers.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    qedge_rows = qedge_null_clause_rows()
    scout_rows = scout_factor_rows()
    blocker_rows = blocker_matrix_rows(scout_rows)
    pressure_rows = pressure_status_rows()
    evaluator = evaluator_rows(qedge_rows, scout_rows, pressure_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, qedge_rows, scout_rows, blocker_rows, pressure_rows, evaluator, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_675_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_QEDGE_NULL_ACTION_CLAUSE_AUDIT.csv",
        qedge_rows,
        ["clause_id", "candidate_clause", "mathematical_form", "acceptance_test", "current_result", "blocker", "repair_or_source", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_SOURCE_BACKED_EDGE_ROW_SCOUT.csv",
        scout_rows,
        ["factor_id", "factor", "patterns", "candidate_files", "candidate_rows_found", "claim_valid_rows_found", "status", "blocked_reasons", "example_hits", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_EDGE_ROW_BLOCKER_MATRIX.csv",
        blocker_rows,
        ["blocker_id", "factor", "current_status", "blocks", "minimum_repair", "why_not_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_PRESSURE_ONLY_STATUS.csv",
        pressure_rows,
        ["pressure_id", "artifact", "numeric_rows", "claim_rows", "status", "use_allowed", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_EVALUATOR.csv",
        evaluator,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_DECISION.csv",
        decision,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_675_NONCLAIM_SUMMARY.csv",
        summary,
        ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_675_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, qedge_rows, scout_rows, blocker_rows, pressure_rows, evaluator, decision, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    claim_valid_scout_rows = sum(int(row["claim_valid_rows_found"]) for row in scout_rows)
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"qedge_clause_rows={len(qedge_rows)}")
    print(f"scout_factors={len(scout_rows)}")
    print(f"claim_valid_scout_rows={claim_valid_scout_rows}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
