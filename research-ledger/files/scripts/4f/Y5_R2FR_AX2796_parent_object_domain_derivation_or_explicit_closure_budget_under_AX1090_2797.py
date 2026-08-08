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
DOC = WORK / "2797-Y5-R2FR-AX2796-parent-object-domain-derivation-or-explicit-closure-budget-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2797_SOURCE_REGISTER.csv",
    "derivation": MTS / "P8_Y5_R2FR_2797_PARENT_OBJECT_DOMAIN_DERIVATION_ATTEMPT.csv",
    "domain_audit": MTS / "P8_Y5_R2FR_2797_DOMAIN_OWNER_CLAUSE_AUDIT.csv",
    "closure_budget": MTS / "P8_Y5_R2FR_2797_EXPLICIT_CLOSURE_BUDGET_REGISTER.csv",
    "cost_matrix": MTS / "P8_Y5_R2FR_2797_CLOSURE_COST_MATRIX.csv",
    "finite_route": MTS / "P8_Y5_R2FR_2797_FINITE_ROUTE_STATUS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2797_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "runner": MTS / "P8_Y5_R2FR_2797_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2797_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2797_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2797_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2797_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2797_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2797_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "derivation_queue": RAB_QUEUE / "JR2797_PARENT_OBJECT_DOMAIN_DERIVATION_NONCLAIM.csv",
    "budget_queue": RAB_QUEUE / "JR2797_EXPLICIT_CLOSURE_BUDGET_NONCLAIM.csv",
    "cost_queue": RAB_QUEUE / "JR2797_CLOSURE_COST_MATRIX_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "AX2796_PARENT_OBJECT_CLOSURE_BUDGET_2797_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_ax2796_parent_object_budget_2797_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2797_SECTOR_CERTIFICATE_PACK_NEXT.csv",
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


def source_entries() -> list[tuple[str, Path, str]]:
    raw = [
        ("2796_next", MTS / "P8_Y5_R2FR_2796_NEXT_TARGET.csv", "authoritative 2797 target"),
        ("2796_synthesis", MTS / "P8_Y5_R2FR_2796_SYNTHESIS_ATTEMPT.csv", "MOMS2794 synthesis failure feeding AX2796_0"),
        ("2796_axioms", MTS / "P8_Y5_R2FR_2796_MISSING_AXIOM_LEDGER.csv", "AX2796_0 parent-object debt"),
        ("2796_closure", MTS / "P8_Y5_R2FR_2796_CLOSURE_DEMOTION_REGISTER.csv", "closure-candidate status"),
        ("2711_derivation", MTS / "P8_Y5_R2FR_2711_AX1090_DERIVATION_ATTEMPT.csv", "earlier AX1090_0 derivation attempt"),
        ("2711_clause_audit", MTS / "P8_Y5_R2FR_2711_PARENT_OBJECT_CLAUSE_AUDIT.csv", "parent-object clause audit"),
        ("2711_closure_ledger", MTS / "P8_Y5_R2FR_2711_EXPLICIT_CLOSURE_AXIOM_LEDGER.csv", "prior explicit closure axiom ledger"),
        ("2710_normal_form", MTS / "P8_Y5_R2FR_2710_PARENT_OBJECT_NORMAL_FORM.csv", "parent object normal form"),
        ("2710_falsifier", MTS / "P8_Y5_R2FR_2710_IRREDUCIBLE_FALSIFIER_GATE.csv", "irreducible parent-object falsifier gate"),
        ("1009_doc", WORK / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md", "parent current-chain contract"),
        ("formalization_10", FORMALIZATION / "10-core-consistency-repair.md", "formal action skeleton and conservation repair"),
    ]
    return [(source_id, path, role) for source_id, path, role in raw]


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


def build_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        ("POD2797_0_target", "derive AX2796_0 parent object/domain owner", "one ordinary-matter parent action object with domain fixed before readout/projection/fitting", "compose 2710 normal form, 2711 primitive attempt, 2796 MOMS debt, and 1009 current-chain contract", "TARGET_SHARPENED", "exact target stated but not yet derived"),
        ("POD2797_1_configuration_space", "construct Conf_parent", "observed geometry, relational MTS variables, finite-cell fibre, matter variables, readout maps, and boundary/domain class live in one admissible space", "import POA2711_0 and PO2710_0", "SKETCHED_NOT_CONSTRUCTED", "finite-cell fibre, equivalence relation, and boundary/domain class are not one variational object"),
        ("POD2797_2_action_normal_form", "construct S_parent on Conf_parent", "S_parent[Phi,Psi;theta]=int_M L_parent + int_boundary B_parent before projection", "use PO2710_0 normal form and formalization 10 action skeleton", "NORMAL_FORM_NOT_OWNER", "normal form names the object but does not supply sector certificates or first variation ownership"),
        ("POD2797_3_sector_certificates", "certify every retained sector", "field list, first variation, stress tensor, boundary term, tau action, source path, and residual policy exist for every block", "F2710_1 identifies this as active blocker", "MISSING_SECTOR_CERTIFICATES", "declaring S_parent=sum sectors is not enough"),
        ("POD2797_4_pre_readout_domain", "fix domain before readout", "q, readout maps, source-worldtube selection, material projection, and calibration are declared before variation", "POA2711_2/6 and AX2796_4 provide the contract", "ORDER_CONTRACT_NOT_DERIVED", "detector/source model that derives this ordering is still absent"),
        ("POD2797_5_matter_domain", "own ordinary matter domain", "S_matter lives on the observed quotient coframe with no hidden marker/weight/frame slot unless retained as residual", "MOMS2794 and PO2710_3 show sufficient form", "MOMS_DEPENDS_ON_PARENT_OBJECT", "matter descent needs the same parent owner it is trying to help prove"),
        ("POD2797_6_circularity", "test for circular derivation", "parent object is derived from clauses that themselves require parent object ownership", "combine POD2797_1 through POD2797_5", "DERIVATION_CIRCULAR_WITHOUT_SECTOR_CERTIFICATES", "the escape route is sector certificates or explicit closure budget"),
        ("POD2797_7_verdict", "AX2796_0 parent object/domain owner", "derive rather than assume the parent action object", "full 2797 attempt", "PARENT_OBJECT_DOMAIN_NOT_DERIVED", "explicit closure budget required before using AX2796_0 in private local branch"),
    ]
    return [
        {
            "attempt_id": row[0],
            "required_clause": row[1],
            "target_statement": row[2],
            "attempted_derivation": row[3],
            "result": row[4],
            "gap": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_domain_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("DOA2797_0_configuration_owner", "Conf_parent owns fields, matter, readout maps, and boundary/domain class", "SKETCHED_NOT_CONSTRUCTED", "formal configuration category and admissible domain"),
        ("DOA2797_1_action_owner", "S_parent is defined before all projections/readouts", "NORMAL_FORM_ONLY", "sector-certified L_parent and B_parent"),
        ("DOA2797_2_sector_variations", "each sector has field list, Euler equation, theta/Q, stress, boundary, tau/source path", "MISSING_SECTOR_CERTIFICATES", "sector certificate pack"),
        ("DOA2797_3_quotient_readout", "q/readout/observer maps are declared before variation", "REQUIRED_NOT_BUILT", "parent quotient object and detector/source domain model"),
        ("DOA2797_4_matter_action", "ordinary matter descends through common observed coframe/no-marker domain", "SUFFICIENT_CLOSURE_NOT_DERIVED", "matter quotient functor and no-marker theorem"),
        ("DOA2797_5_boundary_readout", "boundary/domain/support shifts are owned or residualized before scoring", "MISSING_BOUNDARY_DOMAIN_CERTIFICATE", "zero-flux/no-charge/readout-order theorem or finite residual rows"),
        ("DOA2797_6_Htau_source", "Hamiltonian/source charge and Newtonian source equality come from same current chain", "MISSING_HTAU_OWNER", "theta/Q_tau extraction, fixed reference, tau lock, source equality"),
        ("DOA2797_7_EH_fixed_point", "local branch reduces to EH plus matter plus silent/topological extras", "CANDIDATE_NOT_DERIVED", "A511 action blocks and vanishing/bounded extra variations"),
        ("DOA2797_8_verdict", "AX2796_0 can be treated as derived", "FALSE", "derive domain owner or use explicit closure budget only"),
    ]
    return [
        {
            "audit_id": row[0],
            "domain_clause": row[1],
            "current_status": row[2],
            "needed_to_close": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_closure_budget_rows() -> list[dict[str, Any]]:
    rows = [
        ("CB2797_0_AX2796_0", "parent_object_domain_closure", "assume one parent action object/domain exists for the private local branch only", "conditional theorem bookkeeping; organize local derivation attempts; require closure_assumed label", "derived WEP/local-GR/Newton/PPN/R10 pass; theorem-zero promotion", "derive sector certificates or one source signing AX2796_0"),
        ("CB2797_1_configuration", "configuration_owner_budget", "Conf_parent is treated as one owner of fields, matter, readout maps, and boundary/domain class", "audit later steps for owner consistency", "inventing new owners after variation", "construct formal configuration category"),
        ("CB2797_2_action", "action_owner_budget", "all retained blocks must be inside S_parent or listed as residuals", "force sector certificates and residual ledgers", "importing fitted equations as Euler equations", "sector certificate pack"),
        ("CB2797_3_readout_order", "pre_readout_budget", "q/readout/source/material/calibration maps are declared before variation", "prevent post-hoc zeroing of residuals", "choosing frames/ranges to erase c_g, qbar_XT, PPN, WEP rows", "detector/source domain derivation"),
        ("CB2797_4_matter", "matter_domain_budget", "ordinary matter uses common observed coframe unless finite residual coefficient is retained", "conditional MOMS/WEP analysis", "claiming WEP universality from the closure", "matter functor/no-marker theorem or finite coefficient rows"),
        ("CB2797_5_EH", "local_EH_budget", "EH fixed-point work can proceed only with closure label and extra terms silent/bounded", "private local-GR derivation attempts", "full GR/Newton claim without A511 and PPN gates", "A511 parent blocks plus PPN/source readout proof"),
        ("CB2797_6_residual", "residual_budget", "every unowned current/coefficient remains valid_for_claim=false until derived or bounded", "keeps falsifiability", "dropping awkward couplings", "source-backed bound rows"),
    ]
    return [
        {
            "budget_id": row[0],
            "budget_name": row[1],
            "closure_if_used": row[2],
            "allowed_use": row[3],
            "forbidden_use": row[4],
            "reopen_condition": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_cost_rows() -> list[dict[str, Any]]:
    rows = [
        ("COST2797_0_MOMS_WEP", "MOMS2794/qbar_XT zero theorem", "conditional_private_only", "closure_assumed label plus no WEP/local-GR claim", "finite DD coefficients remain live"),
        ("COST2797_1_Newton_PPN", "Newton/PPN/local GR reduction", "not_claimable_from_AX2796_0_closure", "requires A511/EH, source mass, Poisson/Gauss, and PPN residual gates", "local branch remains proof target"),
        ("COST2797_2_R10_clock_orbital", "R10/clock/orbital arenas", "cannot inherit source-zero", "must use sourced residual/bound rows unless parent clauses close", "test route stays nonclaim"),
        ("COST2797_3_finite_DD", "finite DD WEP route", "still allowed as phenomenological scaffolding", "source-backed coefficients/range/profile/readout only", "pair cancellation and measured-G absorption forbidden"),
        ("COST2797_4_public_claim", "public claim ceiling", "private_internal_only", "no claim beyond conditional closure bookkeeping", "derive AX2796_0 or source finite rows first"),
    ]
    return [
        {
            "cost_id": row[0],
            "affected_branch": row[1],
            "status_under_closure": row[2],
            "cost_paid_by": row[3],
            "remaining_route": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_finite_route_rows() -> list[dict[str, Any]]:
    rows = [
        ("FR2797_0_coefficients", "c_alpha;c_surface;c_mass_ratio;q_tail", "MISSING_SOURCE_BACKED_VALUES", "fill from parent derivation or explicit phenomenological provenance"),
        ("FR2797_1_range_readout", "lambda_X;K_MICROSCOPE;Qeff_E", "MISSING_SAME_BRANCH_READOUT", "source finite-range/profile/readout rows"),
        ("FR2797_2_product", "eta_AB(lambda)", "NO_NUMERIC_PREDICTION", "compute only after coefficients and readout pass policy"),
        ("FR2797_3_guard", "absolute no-cancellation envelope", "POLICY_READY_NONCLAIM", "retain all unowned channels in an absolute bound"),
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
            "prediction_id": "WEP2797_0_no_claim_product",
            "observable": "eta_AB(lambda)",
            "prediction_status": "NO_NUMERIC_PREDICTION",
            "claim_blocker": "AX2796_0 closure budget is not a derivation and finite rows are unsourced",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2797_0_refuse_closure_budget",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_CLAIM",
            "reason": "parent object/domain not derived; closure budget cannot score a WEP product",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2797_0_no_numeric_eta",
            "baseline": "WEP/local-GR compatibility",
            "prediction": "MTS R2FR closure-budget or finite DD branch",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "no derived parent object and no finite source-backed product",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2797_0_parent_object", "AX2796_0 parent object/domain derived", False, False, "POD2797_7_verdict=PARENT_OBJECT_DOMAIN_NOT_DERIVED"),
        ("CG2797_1_closure_budget", "AX2796_0 closure budget usable as claim", False, False, "budget is explicit private scaffolding only"),
        ("CG2797_2_sector_certificates", "sector certificate pack complete", False, False, "field/variation/stress/boundary/tau/source certificates are missing"),
        ("CG2797_3_finite_route", "finite DD route score-ready", False, False, "coefficients and readout rows are unsourced"),
        ("CG2797_4_product_runner", "WEP product runner", True, False, "runner refuses claim safely"),
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
        ("DEC2797_0_derivation_verdict", "AX2796_0 remains not derived", "the attempt is circular until sector certificates or a real parent action source exist", "do not claim local GR/WEP from AX2796_0"),
        ("DEC2797_1_budget", "explicit closure budget is now the only allowed temporary use", "this keeps conditional derivation work possible without hiding the assumption", "label any use as closure_assumed and keep valid_for_claim=false"),
        ("DEC2797_2_next_attack", "sector certificate pack is the next best attack", "declaring S_parent=sum sectors is the active blocker identified by F2710_1", "build field-list/variation/stress/boundary/tau/source certificates or reduce the parent action"),
        ("DEC2797_3_empirical_route", "finite DD remains nonclaim test route", "if derivation fails, sourced finite coefficients are the only honest empirical route", "fill source-backed rows before any scoring"),
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
            "next_id": "NEXT2797_0_2798",
            "next_target": "2798-Y5-R2FR-minimal-sector-certificate-pack-or-smaller-parent-action-with-residuals-under-AX1090.md",
            "script": "scripts/Y5_R2FR_minimal_sector_certificate_pack_or_smaller_parent_action_with_residuals_under_AX1090_2798.py",
            "objective": "try to build the minimal sector certificate pack needed for S_parent: field list, first variation, stress, boundary, tau/source path, and residual policy; if this cannot be done, reduce to the smallest owned parent action and route all other blocks to explicit residuals",
            "include": "sector field lists; first variations; stress tensors; boundary terms; tau/source ownership; residual routing; relation to 1009/2710/2711",
            "exclude": "declaring S_parent by sum without certificates; hidden closure use; invented coefficients; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["derivation"], BRANCH_OUTPUTS["derivation_queue"], "derivation_queue"),
        (OUTPUTS["closure_budget"], BRANCH_OUTPUTS["budget_queue"], "budget_queue"),
        (OUTPUTS["cost_matrix"], BRANCH_OUTPUTS["cost_queue"], "cost_queue"),
        (OUTPUTS["domain_audit"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append({"copy_id": f"BC2797_{label}", "source": str(source), "destination": str(destination), "exists": destination.exists(), "valid_for_claim": False, "generated_utc": utc_now()})
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
        ("VAL2797_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2797_1_derivation_attempted", any(row["attempt_id"] == "POD2797_0_target" for row in sections["derivation"]), "parent-object derivation target is attempted"),
        ("VAL2797_2_parent_not_derived", any(row["attempt_id"] == "POD2797_7_verdict" and row["result"] == "PARENT_OBJECT_DOMAIN_NOT_DERIVED" for row in sections["derivation"]), "AX2796_0 remains not derived"),
        ("VAL2797_3_circularity_recorded", any(row["attempt_id"] == "POD2797_6_circularity" and row["result"] == "DERIVATION_CIRCULAR_WITHOUT_SECTOR_CERTIFICATES" for row in sections["derivation"]), "circularity is explicit"),
        ("VAL2797_4_domain_audit_complete", {row["audit_id"] for row in sections["domain_audit"]} >= {f"DOA2797_{index}_{name}" for index, name in [(0, "configuration_owner"), (1, "action_owner"), (2, "sector_variations"), (3, "quotient_readout"), (4, "matter_action"), (5, "boundary_readout"), (6, "Htau_source"), (7, "EH_fixed_point"), (8, "verdict")]}, "domain audit covers all parent-object clauses"),
        ("VAL2797_5_budget_written", any(row["budget_id"] == "CB2797_0_AX2796_0" for row in sections["closure_budget"]), "explicit closure budget is written"),
        ("VAL2797_6_cost_matrix_written", any(row["cost_id"] == "COST2797_4_public_claim" for row in sections["cost_matrix"]), "closure cost matrix includes public claim ceiling"),
        ("VAL2797_7_finite_route_nonclaim", all(str(row["valid_for_claim"]).lower() == "false" for row in sections["finite_route"]), "finite route rows remain nonclaim"),
        ("VAL2797_8_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["runner"]), "runner refuses claim"),
        ("VAL2797_9_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2797_10_next_target_2798", any(row["next_id"] == "NEXT2797_0_2798" for row in sections["next"]), "next target is 2798 sector certificates"),
        ("VAL2797_11_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2797_12_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2797_13_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2797_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2797_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2797_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2797_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2797_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2797 tries to derive AX2796_0, identifies circular dependence on sector certificates, and writes an explicit closure budget. The parent object/domain remains not derived; all local-GR/WEP uses stay nonclaim.", "generated_utc": utc_now()})
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
        "# 2797 — Y5 R2FR AX2796 Parent Object Domain Derivation Or Explicit Closure Budget Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2797 attacks AX2796_0 directly: can the one ordinary-matter parent action object and pre-readout domain owner be derived rather than assumed?",
        "",
        "Answer: not yet. The derivation remains circular because the available clauses need a common parent owner before they can prove the common parent owner. The active missing object is now sharper: sector certificates. A parent action cannot be declared by summing sectors unless each retained sector has a field list, first variation, stress tensor, boundary term, tau/source path, and residual policy.",
        "",
        "The fallback is therefore an explicit closure budget: AX2796_0 may organize private conditional work only under a closure label. It does not permit WEP, Newton, PPN, R10, or local-GR claims.",
        "",
        "## Parent Object Derivation Attempt",
        markdown_table(sections["derivation"], ["attempt_id", "result", "required_clause", "gap"]),
        "",
        "## Domain Owner Clause Audit",
        markdown_table(sections["domain_audit"], ["audit_id", "domain_clause", "current_status", "needed_to_close"]),
        "",
        "## Explicit Closure Budget",
        markdown_table(sections["closure_budget"], ["budget_id", "budget_name", "allowed_use", "forbidden_use", "reopen_condition"]),
        "",
        "## Closure Cost Matrix",
        markdown_table(sections["cost_matrix"], ["cost_id", "affected_branch", "status_under_closure", "cost_paid_by", "remaining_route"]),
        "",
        "## Finite Route Status",
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
        "derivation": build_derivation_rows(),
        "domain_audit": build_domain_audit_rows(),
        "closure_budget": build_closure_budget_rows(),
        "cost_matrix": build_cost_rows(),
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
