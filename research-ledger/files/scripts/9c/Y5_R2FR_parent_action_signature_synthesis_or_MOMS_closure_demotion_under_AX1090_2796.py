from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2796-Y5-R2FR-parent-action-signature-synthesis-or-MOMS-closure-demotion-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2796_SOURCE_REGISTER.csv",
    "synthesis": MTS / "P8_Y5_R2FR_2796_SYNTHESIS_ATTEMPT.csv",
    "dependencies": MTS / "P8_Y5_R2FR_2796_DERIVATION_DEPENDENCY_MATRIX.csv",
    "axioms": MTS / "P8_Y5_R2FR_2796_MISSING_AXIOM_LEDGER.csv",
    "closure": MTS / "P8_Y5_R2FR_2796_CLOSURE_DEMOTION_REGISTER.csv",
    "finite_route": MTS / "P8_Y5_R2FR_2796_FINITE_TEST_ROUTE_REGISTER.csv",
    "candidate": MTS / "P8_Y5_R2FR_2796_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "runner": MTS / "P8_Y5_R2FR_2796_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2796_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2796_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2796_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2796_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2796_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2796_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "synthesis_queue": RAB_QUEUE / "JR2796_SIGNATURE_SYNTHESIS_ATTEMPT_NONCLAIM.csv",
    "axiom_queue": RAB_QUEUE / "JR2796_MISSING_AXIOM_LEDGER_NONCLAIM.csv",
    "closure_queue": RAB_QUEUE / "JR2796_MOMS_CLOSURE_DEMOTION_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_SIGNATURE_SYNTHESIS_OR_CLOSURE_2796_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_signature_synthesis_or_closure_2796_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2796_PARENT_OBJECT_DOMAIN_OR_CLOSURE_BUDGET_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def discover_markdown(prefix: str) -> Path | None:
    matches = sorted(WORK.glob(f"{prefix}-*.md"))
    return matches[0] if matches else None


def source_entries() -> list[tuple[str, Path, str]]:
    raw: list[tuple[str, Path | None, str]] = [
        ("2795_next", MTS / "P8_Y5_R2FR_2795_NEXT_TARGET.csv", "authoritative 2796 target"),
        ("2795_hunt", MTS / "P8_Y5_R2FR_2795_SIGNATURE_SOURCE_HUNT.csv", "source hunt verdict"),
        ("2795_coverage", MTS / "P8_Y5_R2FR_2795_MOMS_CLAUSE_COVERAGE_MATRIX.csv", "MOMS2794 clause coverage"),
        ("2795_blockers", MTS / "P8_Y5_R2FR_2795_SIGNATURE_BLOCKER_LEDGER.csv", "signature blocker ledger"),
        ("2795_policy", MTS / "P8_Y5_R2FR_2795_FINITE_INTAKE_REVIEW_POLICY.csv", "finite intake review policy"),
        ("2794_signature", MTS / "P8_Y5_R2FR_2794_MINIMAL_SIGNATURE_CLAUSE.csv", "minimal ordinary-matter signature contract"),
        ("2794_theorem", MTS / "P8_Y5_R2FR_2794_CONDITIONAL_ZERO_THEOREM.csv", "conditional WEP zero theorem"),
        ("2794_intake", MTS / "P8_Y5_R2FR_2794_FINITE_DD_INTAKE_SCHEMA.csv", "finite DD intake schema"),
        ("2793_descent", MTS / "P8_Y5_R2FR_2793_PARENT_MATTER_DESCENT_ATTEMPT.csv", "parent matter descent clause stack"),
        ("2793_pack", MTS / "P8_Y5_R2FR_2793_DD_COEFFICIENT_SOURCE_PACK.csv", "DD coefficient source-pack"),
        ("2711_ax1090_attempt", MTS / "P8_Y5_R2FR_2711_AX1090_DERIVATION_ATTEMPT.csv", "earlier R2FR AX1090 parent-object attempt"),
        ("1090_synthesis_analogue", MTS / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv", "R10 synthesis analogue"),
        ("1090_axiom_analogue", MTS / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv", "R10 missing axiom analogue"),
        ("1009_parent_current_contract", discover_markdown("1009"), "parent current-chain action contract"),
        ("1027_qbar_zero", discover_markdown("1027"), "qbar_XT source-zero counterexample ledger"),
        ("1028_no_marker", discover_markdown("1028"), "no-marker/coupling input pack"),
        ("formalization_10_core", FORMALIZATION / "10-core-consistency-repair.md", "formal action skeleton"),
    ]
    return [(source_id, path, role) for source_id, path, role in raw if path is not None]


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def build_synthesis_rows() -> list[dict[str, Any]]:
    rows = [
        ("SYN2796_0_target", "derive MOMS2794 from existing parent-action/current/coframe/matter/no-marker contracts without adding a new axiom", "2795;2794;2793;2711;1009;1027;1028", "compose one parent action object, quotient observed coframe, matter bundle, no species weights, fixed constants, no shadow/domain, and variation-before-readout", "TARGET_SHARPENED", "the target is exact, but the upstream clauses must be parent-derived rather than merely mutually consistent"),
        ("SYN2796_1_parent_object", "AX1090 parent object supplies the single action/domain owner", "2711 AX1090 attempt; 1009 current-chain contract; formalization 10", "use one parent action object before all readout/material projection choices", "PARENT_OBJECT_AVAILABLE_AS_CONTRACT_NOT_DERIVED", "AX1090 object/domain is still an attempted closure/skeleton, not a derived ordinary-matter action"),
        ("SYN2796_2_quotient_pullback", "observed quotient/coframe/gauge fields are functors of q(Phi)", "2794 MOMS2794_1; 2793 PMD2793_2; 1027 qbar route", "Dq[v_X]=0 gives visible geometry and gauge silence by chain rule", "EXACT_CONDITIONAL_LEMMA", "q, E, Omega, and A_obs are not selected by the parent action in one signed object"),
        ("SYN2796_3_matter_bundle", "ordinary matter fields live in species-complete bundles over observed quotient data", "2793 PMD2793_3; 2795 coverage; 1028 no-marker", "choose zero/gauge/local-Lorentz/diffeomorphism/boundary vertical lift for every species", "LIFT_OPTIONS_AVAILABLE_NOT_OWNED", "freezing the lift is a convention unless parent category assigns it"),
        ("SYN2796_4_constants", "ordinary constants are fixed representation/topological data or explicit residual fields", "2794 MOMS2794_3; 1028 no-marker/coupling pack", "treat alpha_EM, masses, clocks, charges, and representation labels as X-trivial", "CONSTANT_ROUTE_AVAILABLE_UNSIGNED", "hidden-visible coefficient functions remain legal without an operator-domain/no-marker theorem"),
        ("SYN2796_5_no_species_weights", "single action measure/current owner forbids w_A(X)S_A source weights", "2793 PMD2793_5; 2794 MOMS2794_4; 2795 blocker BLK2795_1", "one hbar/measure/source-label-forgetting rule removes material/source weights before variation", "ACTION_MEASURE_OWNER_UNSIGNED", "relative action weights remain legal unless parent quantum/statistical measure is derived"),
        ("SYN2796_6_no_shadow_readout", "no shadow frames, hidden domains, or readout-after-variation selectors", "2794 MOMS2794_5-6; 1027/1028 countermodels", "ban conformal/disformal/mass/domain/readout markers or retain them as explicit residuals", "NO_SHADOW_AND_READOUT_GUARDS_UNSIGNED", "countermodels are classified but not forbidden by a parent operator-domain theorem"),
        ("SYN2796_7_zero_theorem_if_signed", "if SYN2796_1 through SYN2796_6 were parent-signed, MOMS2794 gives qbar_XT=0", "2794 THM2794_5", "vertical variation of S_matter hits no quotient-visible, constant, source-weight, shadow, or post-readout slot", "CONDITIONAL_THEOREM_RECONFIRMED", "the missing parent signatures are exactly the theorem assumptions"),
        ("SYN2796_8_verdict", "MOMS2794 is derivable from the current R2FR corpus", "all synthesis rows", "attempted composition of all available contracts into one parent-action derivation", "SYNTHESIS_FAILS_MISSING_AXIOMS", "contract composition does not derive the parent action object, matter category, constant sector, measure/current owner, or no-shadow operator domain"),
    ]
    return [
        {
            "synthesis_id": row[0],
            "synthesis_statement": row[1],
            "input_sources": row[2],
            "derivation_attempt": row[3],
            "result": row[4],
            "why_not_claim": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_dependency_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEP2796_0_parent_primitives", "MTS primitive configuration category C_parent and ordinary-matter action functional S_parent", "2711 AX1090 attempt; 1009 contract; formalization 10", "SCHEMA_NOT_DERIVED", "all-in-one MOMS2794 adoption"),
        ("DEP2796_1_quotient_functor", "q and observed coframe/gauge functors selected by parent kinematics", "2794;2793;1027", "CONDITIONAL_CHAIN_RULE_ONLY", "Lie_v e_obs=0 promotion"),
        ("DEP2796_2_matter_category", "species-complete matter bundle over observed quotient geometry", "2793;2794;1028", "MATTER_CATEGORY_NOT_CONSTRUCTED", "ordinary matter descent theorem"),
        ("DEP2796_3_vertical_lift", "parent-owned vertical lift on every ordinary matter species", "2793 lift row; 2794 MOMS2794_2", "LIFT_NOT_PARENT_SIGNED", "delta_v Psi_A silence"),
        ("DEP2796_4_constant_sector", "fixed representation/topological data for masses, charges, clocks, alpha_EM", "2794;1028", "SUPERSELECTION_NOT_DERIVED", "no alpha/mass/clock WEP residual"),
        ("DEP2796_5_action_measure", "single hbar/measure/current owner forbidding w_A S_A", "2793;2795 blocker", "MEASURE_OWNER_REQUIRED", "no species-weight theorem"),
        ("DEP2796_6_operator_domain", "no hidden-visible coefficient homs and no shadow/domain/readout markers", "1027;1028;2794", "OPERATOR_DOMAIN_NOT_DERIVED", "no-shadow/no-marker theorem"),
        ("DEP2796_7_variation_order", "variation-before-readout rule tied to same parent action", "2793;2794;2795 policy", "CONDITIONAL_RULE_NOT_PARENT_SIGNED", "post-readout source selector exclusion"),
    ]
    return [
        {
            "dependency_id": row[0],
            "needed_object": row[1],
            "best_current_source": row[2],
            "current_status": row[3],
            "blocks": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_axiom_rows() -> list[dict[str, Any]]:
    rows = [
        ("AX2796_0_parent_object", "there exists one parent ordinary-matter action object whose domain is fixed before all readout/projection/fitting choices", "separate contracts cannot derive each other without a common owner", "2711/1009/formalization-10 schemas", "MISSING_AXIOM_NOT_ADOPTED", "could become a clean but inserted minimality principle rather than an MTS derivation"),
        ("AX2796_1_no_hidden_visible_hom", "hidden/representative variables have no allowed homomorphism into visible matter coefficients except through q_obs or fixed representation data", "kills f_X F^2, m_A(X), conformal/disformal matter frames, and material marker functions", "1027/1028 no-marker and countermodel ledgers", "MISSING_AXIOM_NOT_ADOPTED", "too strong unless tied to a real MTS quotient/category construction"),
        ("AX2796_2_common_quantum_measure", "one hbar/action measure/current normalization applies to all ordinary matter sectors and has no species-dependent Jacobian", "forbids w_A S_A source weights that survive classical EOM rescaling", "2793/2794 action-measure rows", "MISSING_AXIOM_NOT_ADOPTED", "imports quantum/statistical structure not yet derived from MTS primitives"),
        ("AX2796_3_fixed_constant_sector", "ordinary masses, charges, alpha_EM, clocks, and representation labels are fixed by parent topology/representation data or retained as explicit residuals", "removes constant-sector WEP/R10/clock source currents", "2794/1028 constants split", "MISSING_AXIOM_NOT_ADOPTED", "could hide real EM/mass coupling debt unless EM owner is separately derived"),
        ("AX2796_4_variation_domain_order", "all source/current variations are taken before empirical readout, material projection, source-worldtube selection, or calibration", "prevents post-variation selectors from manufacturing or erasing a local current", "2793/2794/2795 variation-order gates", "MISSING_AXIOM_NOT_ADOPTED", "readout physics can be over-constrained if not derived with detector/source model"),
    ]
    return [
        {
            "axiom_id": row[0],
            "axiom_if_adopted": row[1],
            "why_needed": row[2],
            "current_basis": row[3],
            "status": row[4],
            "danger_if_adopted": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_closure_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLOS2796_0_MOMS", "MOMS2794 ordinary-matter signature", "closure_candidate_not_adopted", "private branch organization; conditional theorem; comparison scaffold if explicitly labelled closure_assumed later", "derived WEP/local-GR pass; theorem-zero promotion; hiding finite coefficients", "derive AX2796_0 through AX2796_4 from parent primitives or supply one source signing them"),
        ("CLOS2796_1_qbar_XT_zero", "qbar_XT=0 local WEP/source-current branch", "conditional_only", "if MOMS2794 is assumed, zero theorem follows by THM2794_5", "claiming local WEP safety without MOMS source or finite coefficient bounds", "MOMS parent derivation or source-backed finite DD coefficient/product bound"),
        ("CLOS2796_2_finite_DD", "finite DD coefficient branch", "phenomenological_scaffold_retained", "screening/debugging with source-backed rows and explicit derivation_status", "pair cancellation, invented coefficients, measured-G absorption, unit source proxy as claim", "filled same-branch coefficient/range/profile/readout rows with provenance"),
    ]
    return [
        {
            "closure_id": row[0],
            "object": row[1],
            "new_status": row[2],
            "allowed_use": row[3],
            "forbidden_use": row[4],
            "reopen_condition": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_finite_route_rows() -> list[dict[str, Any]]:
    rows = [
        ("FTR2796_0_coefficients", "c_alpha;c_surface;c_mass_ratio;q_tail", "MISSING_PARENT_OR_EXPLICIT_PHENOMENOLOGICAL_SOURCE", "same-branch coefficient source rows with units/signs"),
        ("FTR2796_1_range_readout", "lambda_X;K_MICROSCOPE;Qeff_E(lambda)", "MISSING_RANGE_READOUT_PROFILE_SOURCE", "same-branch finite-range/profile/readout rows"),
        ("FTR2796_2_product", "eta_AB(lambda)", "MISSING_NUMERIC_PREDICTION", "computed only after FTR2796_0 and FTR2796_1 pass source policy"),
        ("FTR2796_3_guard", "no-cancellation/no-absorption policy", "POLICY_READY_NONCLAIM", "absolute no-cancellation envelope across material channels"),
    ]
    return [
        {
            "route_id": row[0],
            "needed_object": row[1],
            "current_status": row[2],
            "next_input": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "WEP2796_0_no_claim_product",
            "observable": "eta_AB(lambda)",
            "route": "MOMS2794 conditional zero or finite DD product",
            "prediction_status": "NO_NUMERIC_PREDICTION",
            "claim_blocker": "signature synthesis failed and finite rows are unsourced",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2796_0_refuse_synthesis_gap",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_CLAIM",
            "reason": "MOMS2794 synthesis fails missing axioms and finite route lacks source-backed rows",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2796_0_no_numeric_eta",
            "baseline": "WEP/local-GR compatibility",
            "prediction": "MTS R2FR MOMS or finite DD branch",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "no parent signature theorem and no finite source-backed product",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2796_0_synthesis", "MOMS2794 synthesized from current corpus", False, False, "SYN2796_8_verdict=SYNTHESIS_FAILS_MISSING_AXIOMS"),
        ("CG2796_1_missing_axioms", "AX2796 debts adopted as theorem", False, False, "AX2796_0 through AX2796_4 are MISSING_AXIOM_NOT_ADOPTED"),
        ("CG2796_2_closure", "MOMS closure usable as claim", False, False, "closure candidate is not adopted and cannot be used as derived WEP/local-GR pass"),
        ("CG2796_3_finite_route", "finite DD route score-ready", False, False, "coefficients/range/readout/product rows remain unsourced"),
        ("CG2796_4_product_runner", "WEP product runner", True, False, "runner refuses claim safely"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim_component": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2796_0_synthesis_verdict", "MOMS2794 synthesis fails from current R2FR corpus", "available pieces are contracts and conditional lemmas, not one parent action derivation", "do not claim local WEP/GR from MOMS2794 yet"),
        ("DEC2796_1_closure_status", "demote MOMS2794 to closure-candidate-not-adopted", "it is useful for organizing the route but would be an inserted assumption if used now", "reopen only if AX2796 debts are derived or one source signs them"),
        ("DEC2796_2_next_best_attack", "attack AX2796_0 parent object/domain first", "without one ordinary-matter parent action object, the other clauses have no common owner", "derive parent object/domain or set an explicit closure budget"),
        ("DEC2796_3_testing_status", "finite DD route remains the test route if derivation fails", "only source-backed coefficient/range/profile/readout rows can become empirical claims", "keep finite rows nonclaim until provenance exists"),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2796_0_2797",
            "next_target": "2797-Y5-R2FR-AX2796-parent-object-domain-derivation-or-explicit-closure-budget-under-AX1090.md",
            "script": "scripts/Y5_R2FR_AX2796_parent_object_domain_derivation_or_explicit_closure_budget_under_AX1090_2797.py",
            "objective": "try to derive the one ordinary-matter parent action object and pre-readout domain owner required by AX2796_0; if it cannot be derived, define an explicit closure budget and keep MOMS2794/finite DD as nonclaim branches",
            "include": "parent action object; ordinary-matter domain; source/readout-before-variation order; relation to 2711 AX1090; closure budget; finite DD fallback",
            "exclude": "adopting AX2796_0 silently; declaring MOMS derived; invented coefficients; pair cancellation; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["synthesis"], BRANCH_OUTPUTS["synthesis_queue"], "synthesis_queue"),
        (OUTPUTS["axioms"], BRANCH_OUTPUTS["axiom_queue"], "axiom_queue"),
        (OUTPUTS["closure"], BRANCH_OUTPUTS["closure_queue"], "closure_queue"),
        (OUTPUTS["synthesis"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append({"copy_id": f"BC2796_{label}", "source": str(source), "destination": str(destination), "exists": destination.exists(), "valid_for_claim": False, "generated_utc": utc_now()})
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2796_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2796_1_synthesis_target_written", any(row["synthesis_id"] == "SYN2796_0_target" for row in sections["synthesis"]), "synthesis target is stated"),
        ("VAL2796_2_synthesis_fails", any(row["synthesis_id"] == "SYN2796_8_verdict" and row["result"] == "SYNTHESIS_FAILS_MISSING_AXIOMS" for row in sections["synthesis"]), "synthesis fails rather than being claimed"),
        ("VAL2796_3_dependencies_complete", {row["dependency_id"] for row in sections["dependencies"]} >= {f"DEP2796_{index}_{name}" for index, name in [(0, "parent_primitives"), (1, "quotient_functor"), (2, "matter_category"), (3, "vertical_lift"), (4, "constant_sector"), (5, "action_measure"), (6, "operator_domain"), (7, "variation_order")]}, "dependency matrix covers all required objects"),
        ("VAL2796_4_axioms_not_adopted", all(row["status"] == "MISSING_AXIOM_NOT_ADOPTED" for row in sections["axioms"]), "missing axioms are recorded but not adopted"),
        ("VAL2796_5_closure_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" and "claim" not in row["allowed_use"].lower() for row in sections["closure"]), "closure register remains nonclaim"),
        ("VAL2796_6_finite_route_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" for row in sections["finite_route"]), "finite route rows remain nonclaim"),
        ("VAL2796_7_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["runner"]), "runner refuses claim"),
        ("VAL2796_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2796_9_next_target_2797", any(row["next_id"] == "NEXT2796_0_2797" for row in sections["next"]), "next target is 2797"),
        ("VAL2796_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2796_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2796_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2796_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2796_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2796_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2796_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2796_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2796 attempts to synthesize MOMS2794 from current R2FR parent-action/coframe/matter/no-marker contracts. The synthesis fails because five parent debts remain missing and unadopted; MOMS2794 is demoted to closure-candidate-not-adopted and finite DD remains the nonclaim test route.", "generated_utc": utc_now()})
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2796 — Y5 R2FR Parent Action Signature Synthesis Or MOMS Closure Demotion Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2796 takes the leap we wanted to test: can the parent-action, observed coframe, matter functor, current-owner, no-marker, and boundary/domain pieces be synthesized into the MOMS2794 ordinary-matter signature?",
        "",
        "Answer: not yet. The synthesis is coherent and the conditional zero theorem remains valuable, but the current R2FR corpus still lacks a single parent ordinary-matter action object, a species-complete matter category/lift, a fixed constant sector, a common action measure/current owner, and a no-hidden-visible operator-domain theorem.",
        "",
        "So MOMS2794 is demoted to **closure-candidate-not-adopted**. It may organize the private derivation route, but it cannot be used as a WEP/local-GR claim. If the derivation route fails, the finite DD coefficient route remains the nonclaim empirical test branch.",
        "",
        "## Synthesis Attempt",
        markdown_table(sections["synthesis"], ["synthesis_id", "result", "synthesis_statement", "why_not_claim"]),
        "",
        "## Derivation Dependency Matrix",
        markdown_table(sections["dependencies"], ["dependency_id", "needed_object", "current_status", "blocks"]),
        "",
        "## Missing Axiom Ledger",
        markdown_table(sections["axioms"], ["axiom_id", "status", "axiom_if_adopted", "danger_if_adopted"]),
        "",
        "## Closure Demotion Register",
        markdown_table(sections["closure"], ["closure_id", "object", "new_status", "allowed_use", "forbidden_use", "reopen_condition"]),
        "",
        "## Finite Test Route",
        markdown_table(sections["finite_route"], ["route_id", "needed_object", "current_status", "next_input"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "synthesis": build_synthesis_rows(),
        "dependencies": build_dependency_rows(),
        "axioms": build_axiom_rows(),
        "closure": build_closure_rows(),
        "finite_route": build_finite_route_rows(),
        "candidate": build_candidate_rows(),
        "runner": build_runner_rows(),
        "comparisons": build_comparison_rows(),
        "gates": build_gate_rows(),
        "decision": build_decision_rows(),
        "next": build_next_rows(),
    }
    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
