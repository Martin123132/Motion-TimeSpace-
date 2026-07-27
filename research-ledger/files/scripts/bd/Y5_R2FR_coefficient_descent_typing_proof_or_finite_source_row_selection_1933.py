from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1933"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1932_doc": ROOT / "1932-Y5-R2FR-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md",
    "1932_validation": OUT / "P8_Y5_BRR545_1932_VALIDATION.csv",
    "1932_morphism": OUT / "P8_Y5_PARENT_QLOC_1932_MASTER_MORPHISM_ATTEMPT.csv",
    "1932_theorem": OUT / "P8_Y5_PARENT_QLOC_1932_CONDITIONAL_DESCENT_THEOREM.csv",
    "1932_counterexamples": OUT / "P8_Y5_PARENT_QLOC_1932_COUNTEREXAMPLE_LEDGER.csv",
    "1932_closure": OUT / "P8_Y5_PARENT_QLOC_1932_EXPLICIT_CLOSURE_PACK.csv",
    "1932_finite": OUT / "P8_Y5_PARENT_QLOC_1932_FINITE_SOURCE_REQUIREMENTS.csv",
    "1932_claims": OUT / "P8_Y5_PARENT_QLOC_1932_CLAIM_GATE.csv",
    "1932_next": OUT / "P8_Y5_PARENT_QLOC_1932_NEXT_TARGET.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
    "1105_finite": OUT / "P8_Y5_R10_1105_FINITE_SOURCE_REQUIREMENTS.csv",
}

NEEDLES = {
    "1932_doc": ["MHM1932_4_verdict", "PACK1932_1_coefficient_descent", "VAL1932_OVERALL"],
    "1932_validation": ["VAL1932_OVERALL", "PASS"],
    "1932_morphism": ["MHM1932_1_vertical_chain_rule", "MHM1932_4_verdict"],
    "1932_theorem": ["THM1932_1_vertical_descent_zero", "THM1932_4_verdict"],
    "1932_counterexamples": ["CEX1932_0_hidden_scalar_F2", "CEX1932_4_boundary_projection"],
    "1932_closure": ["PACK1932_1_coefficient_descent", "PACK1932_5_finite_fallback"],
    "1932_finite": ["FIN1932_1_WEP_source_weight", "FIN1932_5_boundary_projection"],
    "1932_claims": ["CG1932_0_master_morphism", "CG1932_5_finite_rows"],
    "1932_next": ["NEXT1932_0_primary", "coefficient-descent"],
    "1931_signature": ["SIG1931_5_no_hidden_visible_hom", "SIG1931_10_verdict"],
    "1105_finite": ["FIN1105_2_WEP_alpha_product", "FIN1105_5_mass_binding"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1933_SOURCE_REGISTER.csv",
    "typing_audit": OUT / "P8_Y5_PARENT_QLOC_1933_COEFFICIENT_DESCENT_TYPING_AUDIT.csv",
    "quotient_theorem": OUT / "P8_Y5_PARENT_QLOC_1933_QUOTIENT_DESCENT_THEOREM.csv",
    "fiber_residuals": OUT / "P8_Y5_PARENT_QLOC_1933_FIBER_RESIDUAL_LEDGER.csv",
    "minimal_closure": OUT / "P8_Y5_PARENT_QLOC_1933_MINIMAL_CLOSURE.csv",
    "finite_selection": OUT / "P8_Y5_PARENT_QLOC_1933_FINITE_ROW_SELECTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1933_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1933_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1933_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1933_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1933_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_closure": SOURCE_WEIGHT_DOCS / "ORDINARY_SECTOR_COEFFICIENT_DESCENT_CLOSURE_1933_NONCLAIM.csv",
    "microscope_selection": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1933_FINITE_ROW_SELECTION_NONCLAIM.csv",
    "finite_queue": QUEUE / "JR1933_WEP_SOURCE_WEIGHT_FIRST_FINITE_ROW_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1933_CLAIM_GATE.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, source_path in SOURCES.items():
        path_exists = source_path.exists()
        source_text = read_text(source_path) if path_exists else ""
        missing_needles = [needle for needle in NEEDLES[source_key] if needle not in source_text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "needed_for": "1933 coefficient descent typing proof or finite source row selection",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def typing_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TYPE1933_0_required_typing",
            "typing_clause": "visible ordinary-sector coefficient c_vis is a function/section on the quotient-visible object",
            "math_test": "for p~p_prime with q(p)=q(p_prime), require c_vis(p)=c_vis(p_prime)",
            "result": "REQUIRED_FOR_DESCENT",
            "evidence_state": "not parent-signed in current branch",
            "consequence": "without fiber invariance, hidden scalar counterexamples survive",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TYPE1933_1_universal_property",
            "typing_clause": "fiber-invariant c_vis factors uniquely through q",
            "math_test": "if c_vis(p)=c_vis(p_prime) on q-fibers, define c_bar(q(p))=c_vis(p)",
            "result": "EXACT_QUOTIENT_THEOREM",
            "evidence_state": "pure mathematics; needs parent fiber-invariance premise",
            "consequence": "gives c_vis=q^*c_bar and hence dc_vis(v_X)=0",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TYPE1933_2_parent_object_language_route",
            "typing_clause": "parent grammar forbids coefficient slots from accepting hidden scalar invariants",
            "math_test": "Coeff_vis receives only q(Phi), representation labels, and fixed normalizations",
            "result": "POSSIBLE_ROUTE_BUT_UNSIGNED",
            "evidence_state": "1932 closure pack states the clause but does not derive it",
            "consequence": "candidate for future parent action axiom/theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TYPE1933_3_symmetry_failure",
            "typing_clause": "ordinary covariance and gauge symmetry alone imply coefficient descent",
            "math_test": "try f(I_hid)F^2, w_A(I_hid)T_A, nu(I_hid), m_A(I_hid)",
            "result": "FALSE",
            "evidence_state": "counterexamples remain allowed without typing restriction",
            "consequence": "cannot sell this as a symmetry theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TYPE1933_4_verdict",
            "typing_clause": "visible coefficient descent c_vis=q^*c_bar is derived from current parent evidence",
            "math_test": "parent source must prove fiber invariance for all ordinary visible coefficients",
            "result": "COEFFICIENT_DESCENT_NOT_PARENT_SIGNED",
            "evidence_state": "only conditional quotient theorem is available",
            "consequence": "demote descent to minimal closure and select one finite source-row target",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def quotient_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QDT1933_0_fiber_invariance",
            "statement": "Given q:P->Pbar and c:P->V, c descends iff c is constant on every q-fiber.",
            "proof_status": "EXACT_THEOREM",
            "proof_sketch": "If c=cbar o q then equal q-values give equal c-values. Conversely define cbar(q(p))=c(p); fiber invariance makes this well-defined.",
            "mts_use": "coefficient descent is equivalent to fiber invariance",
            "remaining_debt": "prove fiber invariance from the parent ordinary-sector action signature",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QDT1933_1_vertical_zero",
            "statement": "If c descends and v_X in ker(Dq), then dc(v_X)=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Write c=q^*cbar; then dc(v_X)=dcbar(Dq v_X)=0.",
            "mts_use": "local coupling residual vanishes after coefficient descent",
            "remaining_debt": "descent premise is not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QDT1933_2_pullback_action",
            "statement": "If every visible coefficient in S_ord is descended, vertical variations cannot change visible coupling constants.",
            "proof_status": "CONDITIONAL_ACTION_COROLLARY",
            "proof_sketch": "Apply QDT1933_1 coefficient-by-coefficient inside the ordinary-sector action.",
            "mts_use": "turns the coupling problem into one parent typing clause",
            "remaining_debt": "radiative, readout, and boundary maps must preserve descent",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QDT1933_3_verdict",
            "statement": "The quotient theorem proves the MTS parent coefficient-descent premise.",
            "proof_status": "NOT_DERIVED",
            "proof_sketch": "The theorem proves what fiber invariance would imply; it does not supply fiber invariance.",
            "mts_use": "honest closure boundary",
            "remaining_debt": "parent object-language typing or finite coefficient evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def fiber_residual_rows() -> list[dict[str, Any]]:
    residual_data = [
        ("RES1933_0_alpha", "alpha/EM", "R_alpha(v_X)=d b_alpha(v_X) or d c_alpha(v_X)", "f(I_hid)F^2"),
        ("RES1933_1_source_weight", "WEP/source", "R_wA(v_X)=d w_A(v_X)", "w_A(I_hid)T_A"),
        ("RES1933_2_clock", "clock/readout", "R_clock(v_X)=d nu_clock(v_X)", "nu_clock(I_hid)"),
        ("RES1933_3_mass_binding", "mass/binding", "R_mass(v_X), R_bind(v_X)", "m_A(I_hid), E_bind,A(I_hid)"),
        ("RES1933_4_boundary_projection", "local projection/PPN", "R_boundary(v_X)=delta_boundary c_vis", "representative-dependent projection coefficient"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "sector": sector,
            "residual_definition": residual_definition,
            "active_counterexample": active_counterexample,
            "status": "ACTIVE_IF_DESCENT_UNSIGNED",
            "needed_to_zero": "parent-signed coefficient descent, or a sourced finite residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for residual_id, sector, residual_definition, active_counterexample in residual_data
    ]


def minimal_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "closure_id": "CLOS1933_0_minimal_descent_clause",
            "closure_clause": "For every ordinary visible coefficient c_vis in the local action and readout maps, c_vis is constant on q-fibers.",
            "why_minimal": "fiber invariance is exactly equivalent to the existence of c_bar with c_vis=q^*c_bar",
            "what_it_proves_conditionally": "all vertical hidden derivatives dc_vis(v_X) vanish",
            "status": "EXPLICIT_CLOSURE_UNLESS_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "CLOS1933_1_preservation_clause",
            "closure_clause": "Radiative corrections, boundary terms, and measurement/readout maps preserve q-fiber invariance.",
            "why_minimal": "a bulk coefficient zero is not enough if loops/readout/boundaries reintroduce hidden dependence",
            "what_it_proves_conditionally": "protects clock, PPN, R10, and WEP residuals from reappearing downstream",
            "status": "EXPLICIT_CLOSURE_UNLESS_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "CLOS1933_2_public_status",
            "closure_clause": "The closure cannot be advertised as a derived local-GR/WEP/R10/clock result.",
            "why_minimal": "it is a discipline rule preventing overclaiming",
            "what_it_proves_conditionally": "nothing by itself; it labels the branch correctly",
            "status": "NONCLAIM_DISCIPLINE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def finite_selection_rows() -> list[dict[str, Any]]:
    candidates = [
        ("SEL1933_0_alpha", "alpha/EM", "FIN1932_0_alpha_coefficient", 3, 4, 3, "important but less direct for GR/Newton source coupling"),
        ("SEL1933_1_WEP_source_weight", "WEP/source", "FIN1932_1_WEP_source_weight", 5, 4, 5, "selected because universal source coupling is the local-GR/Newton hinge"),
        ("SEL1933_2_clock", "clock/readout", "FIN1932_2_clock_product", 3, 3, 4, "strong precision arena but readout owner is downstream of source coupling"),
        ("SEL1933_3_R10", "R10 short range", "FIN1932_3_R10_product", 4, 3, 4, "excellent local force arena but bound curve/data plumbing already has separate gates"),
        ("SEL1933_4_mass_binding", "mass/binding", "FIN1932_4_mass_binding", 4, 2, 5, "central but harder to source cleanly as first finite row"),
        ("SEL1933_5_boundary_projection", "local q_loc/PPN/orbital", "FIN1932_5_boundary_projection", 5, 2, 5, "central but needs more geometry before a clean numeric row exists"),
    ]
    rows: list[dict[str, Any]] = []
    for selection_id, channel, upstream_requirement, gr_relevance, sourceability, coupling_relevance, rationale in candidates:
        total = gr_relevance + sourceability + coupling_relevance
        selected = selection_id == "SEL1933_1_WEP_source_weight"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "selection_id": selection_id,
                "channel": channel,
                "upstream_requirement": upstream_requirement,
                "gr_newton_relevance_1to5": gr_relevance,
                "near_term_sourceability_1to5": sourceability,
                "coupling_relevance_1to5": coupling_relevance,
                "score": total,
                "selection_status": "SELECTED_FIRST_FINITE_ROW" if selected else "DEFERRED",
                "rationale": rationale,
                "claim_status": "NONCLAIM_ACQUISITION_TARGET",
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    gate_data = [
        ("CG1933_0_coefficient_descent", "coefficient descent is parent-derived", "fiber invariance is not parent-signed"),
        ("CG1933_1_vertical_zero", "all visible vertical coefficient derivatives vanish", "exact only under descent premise"),
        ("CG1933_2_closure_public_claim", "minimal descent closure is a public derivation claim", "closure is not derivation"),
        ("CG1933_3_WEP_finite_row", "WEP/source finite row is sourced and scoreable", "selected but not acquired"),
        ("CG1933_4_local_GR_Newton", "local GR/Newton reduction is derived", "requires source coupling, field operator, Ward/Bianchi, and PPN/readout maps"),
        ("CG1933_5_formalization", "formalization-workbench can be treated as updated", "1933 deliberately made no formalization-workbench edits"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "FAIL_BLOCKED",
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for gate_id, claim, reason in gate_data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1933_0_descent_verdict",
            "decision": "COEFFICIENT_DESCENT_NOT_PARENT_SIGNED",
            "rationale": "The quotient theorem is exact, but the branch lacks a source proving c_vis is fiber-invariant.",
            "next_action": "keep the minimal descent closure explicit and nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1933_1_first_finite_row",
            "decision": "SELECT_WEP_SOURCE_WEIGHT_FIRST",
            "rationale": "Universal source coupling is the most direct GR/Newton hinge; alpha and R10 remain useful but are less central to the source-coupling proof.",
            "next_action": "acquire a source-backed WEP/source-weight row: Delta w_A or beta_source/tau_WEP with units, source path, and claim=false",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1933_2_derivation_path",
            "decision": "DERIVATION_PATH_STILL_OPEN",
            "rationale": "A future parent object-language rule could still sign fiber invariance and collapse the finite residual vector.",
            "next_action": "do not close the derivation route; use finite row as pressure-test fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1933_0_primary",
            "selection_status": "selected",
            "target_doc": "1934-Y5-R2FR-WEP-source-weight-first-finite-row-acquisition-nonclaim.md",
            "target_script": "scripts/Y5_R2FR_WEP_source_weight_first_finite_row_acquisition_nonclaim_1934.py",
            "objective": "acquire or construct the first nonclaim WEP/source-weight finite row for Delta w_A or beta_source*tau_WEP, with units, provenance, source paths, and explicit claim=false gates",
            "success_condition": "one source-backed WEP/source finite row or a blocker ledger proving what source/input is missing, while all local-GR/WEP claims remain blocked",
            "do_not": "do not set tau_WEP=1, absorb composition dependence into measured G, claim WEP pass, claim local GR, modify formalization-workbench, or use unsourced coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1933_0_project_position",
            "status": "COUPLING_GATE_SHARPENED",
            "summary": "Coefficient descent is now reduced to exact fiber invariance on q-fibers.",
            "strongest_result": "fiber invariance is equivalent to c_vis=q^*c_bar, and then dc_vis(v_X)=0 follows exactly",
            "missing_piece": "parent source proving visible coefficients are q-fiber-invariant and preserved by readout/boundary maps",
            "fallback": "selected WEP/source-weight as the first finite nonclaim acquisition row",
            "claim_position": "all local-GR/WEP/R10/clock/alpha claims remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_closure"], rows_by_name["minimal_closure"])
    write_csv(BRANCH_COPIES["microscope_selection"], rows_by_name["finite_selection"])
    write_csv(BRANCH_COPIES["finite_queue"], [row for row in rows_by_name["finite_selection"] if row["selection_status"] == "SELECTED_FIRST_FINITE_ROW"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1933*") if artifact.is_file())


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        validation_rows.append(
            {
                "validation_id": validation_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL1933_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1933_01_typing_audit", any(row["result"] == "EXACT_QUOTIENT_THEOREM" for row in rows_by_name["typing_audit"]) and any(row["result"] == "COEFFICIENT_DESCENT_NOT_PARENT_SIGNED" for row in rows_by_name["typing_audit"]), "typing audit separates exact theorem from unsigned parent premise")
    add("VAL1933_02_quotient_theorem", any(row["proof_status"] == "EXACT_THEOREM" for row in rows_by_name["quotient_theorem"]) and any(row["proof_status"] == "NOT_DERIVED" for row in rows_by_name["quotient_theorem"]), "quotient descent theorem proved conditionally without promoting parent premise")
    add("VAL1933_03_residuals", len(rows_by_name["fiber_residuals"]) == 5 and all(row["status"] == "ACTIVE_IF_DESCENT_UNSIGNED" for row in rows_by_name["fiber_residuals"]), "five live residual families retained")
    add("VAL1933_04_minimal_closure", len(rows_by_name["minimal_closure"]) == 3 and rows_by_name["minimal_closure"][0]["closure_id"] == "CLOS1933_0_minimal_descent_clause", "minimal descent closure recorded explicitly")
    selected = [row for row in rows_by_name["finite_selection"] if row["selection_status"] == "SELECTED_FIRST_FINITE_ROW"]
    add("VAL1933_05_finite_selection", len(selected) == 1 and selected[0]["selection_id"] == "SEL1933_1_WEP_source_weight", "exactly one first finite row selected: WEP/source weight")
    add("VAL1933_06_claim_gates_blocked", len(rows_by_name["claim_gate"]) == 6 and all(row["status"] == "FAIL_BLOCKED" for row in rows_by_name["claim_gate"]), "all claim gates remain blocked")
    add("VAL1933_07_decision", any(row["decision"] == "SELECT_WEP_SOURCE_WEIGHT_FIRST" for row in rows_by_name["decision"]), "WEP/source-weight selected for 1934")
    add("VAL1933_08_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1934-Y5-R2FR-WEP-source-weight"), "1934 WEP source-weight target selected")
    add("VAL1933_09_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1933_10_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1933_11_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1933_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1933_13_formalization_untouched", formalization_count == 0, f"formalization_1933_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1933_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1933 coefficient descent typing proof or finite source row selection",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1933 Y5 R2FR: Coefficient Descent Typing Proof or Finite Source Row Selection",
        "",
        "## Verdict",
        "",
        "The exact theorem is now sharp: `c_vis` descends through `q` if and only if it is constant on every `q`-fiber. Once that premise is signed, `dc_vis(v_X)=0` follows immediately for vertical hidden variations. The current branch still does **not** parent-sign fiber invariance, so coefficient descent remains an explicit closure, not a claim.",
        "",
        "Because the derivation is not closed, 1933 selects one finite nonclaim fallback row: WEP/source-weight coupling. That is the best first fallback because universal source coupling is the local GR/Newton hinge.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Coefficient Descent Typing Audit",
        "",
        markdown_table(rows_by_name["typing_audit"]),
        "",
        "## Quotient Descent Theorem",
        "",
        markdown_table(rows_by_name["quotient_theorem"]),
        "",
        "## Fiber Residual Ledger",
        "",
        markdown_table(rows_by_name["fiber_residuals"]),
        "",
        "## Minimal Closure",
        "",
        markdown_table(rows_by_name["minimal_closure"]),
        "",
        "## Finite Row Selection",
        "",
        markdown_table(rows_by_name["finite_selection"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "typing_audit": typing_audit_rows(),
        "quotient_theorem": quotient_theorem_rows(),
        "fiber_residuals": fiber_residual_rows(),
        "minimal_closure": minimal_closure_rows(),
        "finite_selection": finite_selection_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
