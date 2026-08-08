from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
MICRO = ROOT / "source-intake" / "microscope"
MICRO_Q = MICRO / "quarantine"
MICRO_COEFF = MICRO / "branch_locked_wep" / "coefficients"
MICRO_PRODUCT = MICRO / "product_convention"
MICRO_METADATA = MICRO / "metadata"
WEP = ROOT / "source-intake" / "wep-sources"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2981"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2981-Y5-R2FR-single-action-density-line-and-species-blind-measure-or-deltawe-deproxy-under-AX1090.md"

SRC_2980_DOC = ROOT / "2980-Y5-R2FR-parent-constructor-exhaustion-or-first-real-JZ-coefficient-row-under-AX1090.md"
SRC_2980_NEXT = RESIDUALS / "P8_Y5_R2FR_2980_NEXT_TARGET.csv"
SRC_2980_CONSTRUCTOR = RESIDUALS / "P8_Y5_R2FR_2980_PARENT_GENERATE_EXHAUSTION_ATTEMPT.csv"
SRC_2980_PROMO = RESIDUALS / "P8_Y5_R2FR_2980_FIRST_REAL_JZ_COEFFICIENT_PROMOTION_AUDIT.csv"
SRC_2980_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2980_VALIDATION.csv"

SRC_1478_SAL = MICRO_Q / "1478" / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv"
SRC_1463_PMO = MICRO_COEFF / "parent_measure_owner_contract_1463.csv"
SRC_1477_GRAPH = MICRO_COEFF / "connected_matter_graph_certificate_nonclaim_1477.csv"
SRC_1452_CMT = MICRO_COEFF / "common_measure_current_theorem_attempt_1452.csv"
SRC_2677_GRAMMAR = WEP / "no_species_action_weight_object_language_wip_2677.csv"
SRC_2676_OWNER = WEP / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2774_ASO = BETA_DOCS / "ACTION_SCALE_OWNER_2774_NONCLAIM.csv"
SRC_2329_SBF = BETA_DOCS / "SOURCE_BLIND_FUNCTOR_SIGNATURE_2329_NONCLAIM.csv"
SRC_2344_PSBF = BETA_DOCS / "PARENT_SOURCE_BLIND_FUNCTOR_PROOF_OBLIGATION_2344_NONCLAIM.csv"
SRC_2508_DECISION = BETA_DOCS / "No_source_only_slot_decision_2508_NONCLAIM.csv"
SRC_1479_DW = MICRO_Q / "1479" / "COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"
SRC_1480_SMOKE = MICRO_Q / "1480" / "SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv"
SRC_1481_UPDATE = MICRO_Q / "1481" / "SAME_BRANCH_WEP_SMOKE_UPDATE_NONCLAIM.csv"
SRC_1478_VEC = MICRO_Q / "1478" / "COMPONENT_DELTA_W_VECTOR_INPUT_TEMPLATE_NONCLAIM.csv"
SRC_2688_REQ = LOCAL_BOUNDS / "deltaw_component_value_requirements_2688_NONCLAIM.csv"
SRC_PRODUCT = MICRO_PRODUCT / "P_WEP_eta_product_convention.csv"
SRC_PRODUCT_STATUS = MICRO / "branch_locked_wep" / "product" / "P_WEP_eta_product_status_1482.csv"
SRC_SHORTCUT = MICRO_METADATA / "P8_Y5_R10_1336_ANTI_SHORTCUT_GATES.csv"
SRC_PROD_SCHEMA = MICRO_METADATA / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2981_SOURCE_REGISTER.csv",
    "action_line": RESIDUALS / "P8_Y5_R2FR_2981_SINGLE_ACTION_DENSITY_LINE_AUDIT.csv",
    "deproxy": RESIDUALS / "P8_Y5_R2FR_2981_DELTAWE_DEPROXY_CHECKLIST.csv",
    "candidate": RESIDUALS / "P8_Y5_R2FR_2981_DELTAWE_PROXY_STATUS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2981_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2981_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2981_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2981_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2981_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "action_line_copy": PARENT_ACTION / "single_action_density_line_species_blind_measure_2981_NOT_DERIVED.csv",
    "deproxy_copy": LOCAL_BOUNDS / "delta_w_e_deproxy_checklist_2981_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2981_parent_measure_owner_or_wep_product_convention_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    hay = text(path)
    return path.exists() and all(needle in hay for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2981_00_2980_doc", SRC_2980_DOC, ["Status:", "Best next move"], "2980 markdown handoff"),
        ("SRC2981_01_2980_next", SRC_2980_NEXT, ["NEXT2980_0_2981", "species-blind measure"], "selected 2981 target"),
        ("SRC2981_02_2980_constructor", SRC_2980_CONSTRUCTOR, ["PG2980_4_single_action_density", "PG2980_5_species_blind_measure"], "constructor blockers"),
        ("SRC2981_03_2980_promo", SRC_2980_PROMO, ["PROM2980_0_delta_w_e", "REJECT_PROMOTION_PROXY_ONLY"], "delta_w_e proxy rejection"),
        ("SRC2981_04_2980_validation", SRC_2980_VALIDATION, ["VAL2980_OVERALL"], "2980 validation"),
        ("SRC2981_05_sal1478", SRC_1478_SAL, ["SAL1478_0_target", "SAL1478_4_verdict"], "single action-density line attempt"),
        ("SRC2981_06_pmo1463", SRC_1463_PMO, ["PMO1463_0_action_density_line", "PMO1463_6_verdict"], "parent measure owner contract"),
        ("SRC2981_07_graph1477", SRC_1477_GRAPH, ["GRC1477_1_parent_owned_connectivity", "GRC1477_2_action_density_line"], "connected matter graph"),
        ("SRC2981_08_cmt1452", SRC_1452_CMT, ["CMT1452_2_quantum_measure_route", "CMT1452_6_verdict"], "common measure/current theorem"),
        ("SRC2981_09_grammar2677", SRC_2677_GRAMMAR, ["GRM2677_0_single_action_density_line", "GRM2677_6_verdict"], "no species action-weight grammar"),
        ("SRC2981_10_owner2676", SRC_2676_OWNER, ["OWN2676_0_parent_owner_target", "OWN2676_1_common_measure_route"], "action scale measure owner WIP"),
        ("SRC2981_11_aso2774", SRC_2774_ASO, ["ASO2774_2_path_integral_measure", "ASO2774_5_verdict"], "action scale owner"),
        ("SRC2981_12_sbf2329", SRC_2329_SBF, ["SBF2329_2_single_measure_scale", "SBF2329_6_verdict"], "source-blind functor signature"),
        ("SRC2981_13_psbf2344", SRC_2344_PSBF, ["PSBF2344_2_same_action_owner", "PSBF2344_6_verdict"], "source-blind proof obligation"),
        ("SRC2981_14_decision2508", SRC_2508_DECISION, ["DEC2508_2_loop_guard", "DEC2508_3_next"], "loop guard"),
        ("SRC2981_15_dw1479", SRC_1479_DW, ["CBP1479_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"], "delta_w component pack"),
        ("SRC2981_16_smoke1480", SRC_1480_SMOKE, ["WSR1480_1_electron_unit_kernel_quarantine", "PROXY_COMPUTED_QUARANTINED"], "delta_w_e smoke result"),
        ("SRC2981_17_update1481", SRC_1481_UPDATE, ["WUP1481_1_electron_tau_rescaling_template", "UNIT_TAU_ONLY_QUARANTINED"], "delta_w_e tau template"),
        ("SRC2981_18_vec1478", SRC_1478_VEC, ["CDW1478_0_parent_component_vector", "CDW1478_2_no_cancellation_covariance"], "component vector template"),
        ("SRC2981_19_req2688", SRC_2688_REQ, ["DWBV2688_7_material_tensor", "DWBV2688_10_acceptance"], "delta-w value requirements"),
        ("SRC2981_20_product", SRC_PRODUCT, ["tau_eff", "PENDING_PARENT_SOURCE_BASIS_UNITS"], "partial WEP product convention"),
        ("SRC2981_21_product_status", SRC_PRODUCT_STATUS, ["MAN1482_3_product_convention", "MAN1482_6_C_parent_import"], "product manifest"),
        ("SRC2981_22_shortcut", SRC_SHORTCUT, ["SHORT1336_2_no_unity_tau", "REFUSED"], "anti-shortcut gates"),
        ("SRC2981_23_schema", SRC_PROD_SCHEMA, ["PRODSCHEMA1336_2_tau_eff_definition", "MISSING_PRODUCT_CONVENTION_FILE"], "product convention schema"),
    ]
    return [add({"source_id": sid, "source_path": str(path), "role": role, "required_anchors": ";".join(needles), "exists": path.exists(), "anchors_found": anchors(path, needles)}) for sid, path, needles, role in specs]


def action_line_rows() -> list[dict[str, Any]]:
    data = [
        ("AL2981_0_target", "one ordinary-matter action-density line", "S_ord = integral dmu_parent L_ord(Psi_A,gauge,theta_A,e_obs)/hbar_parent", "TARGET_EXACT", "would collapse source weights if parent-owned"),
        ("AL2981_1_conditional", "connected naturality lemma", "w_B F(f)=F(f)w_A on a connected ordinary matter category implies w_A=w_*", "EXACT_CONDITIONAL_LEMMA", "connectedness/action-line ownership not parent-signed"),
        ("AL2981_2_hbar_measure", "one hbar/path/statistical measure owner", "exp(i sum_A S_A/hbar_parent) with no hbar_A,J_A,w_A replicas", "OWNER_NOT_DERIVED", "parent statistical/path-integral measure owner missing"),
        ("AL2981_3_species_blind", "species-blind measure/Jacobian", "D_A log mu_parent = D_A log sqrt(-g_obs) = D_A log J_measure = 0", "CONDITIONAL_CLAUSE_NOT_SIGNED", "species Jacobian countermodel survives"),
        ("AL2981_4_current", "same current owner before readout", "J_src=delta S_ord/delta e_obs before readout, with no c_A or zeta_A bypass", "PARTIAL_HILBERT_ONLY", "non-Hilbert/readout bypass remains open"),
        ("AL2981_5_countermodel", "disconnected/direct-sum matter sectors", "independent constants w_i survive on disconnected components", "COUNTERMODEL_SURVIVES", "parent-owned interaction/morphism graph missing"),
        ("AL2981_6_verdict", "single action-density/species-blind measure proof", "AL2981_0 through AL2981_5 close in one branch", "NOT_PARENT_DERIVED_RETAIN_DELTAW_ROWS", "clean conditional theorem, not a parent derivation"),
    ]
    return [add({"audit_id": i, "object": o, "statement": s, "status": st, "blocking_gap": gap, "theorem_zero": False}) for i, o, s, st, gap in data]


def deproxy_rows() -> list[dict[str, Any]]:
    data = [
        ("DEP2981_0_value", "delta_w_e proxy value", "8.948213306283e-11", "available but proxy", "PROXY_RETAINED_NONCLAIM"),
        ("DEP2981_1_tau", "tau_eff_e", "tau_eff=branch_locked_orbit_average(K_CMSM*R_source*readout_mask)", "pending; unit tau refused", "MISSING_TAU_PRODUCT_CONVENTION"),
        ("DEP2981_2_readout", "K_CMSM/readout units/sign", "official readout and sign/orientation", "partial body order; pending K_CMSM sign/units", "MISSING_READOUT_UNITS_SIGN"),
        ("DEP2981_3_source", "R_source/source kernel", "Earth/source-worldtube source basis units", "pending parent source basis units", "MISSING_SOURCE_KERNEL"),
        ("DEP2981_4_material", "DeltaF/material tensor", "full Ti/Pt parent material tensor", "component proxy only; full parent tensor required", "MISSING_PARENT_MATERIAL_TENSOR"),
        ("DEP2981_5_parent_coeff", "C_parent component map", "MTS parent coefficient vector for electron/source-weight component", "not imported/derived", "MISSING_C_PARENT_COMPONENT_MAP"),
        ("DEP2981_6_branch", "same-branch lock", "coefficient, material, source, readout, tau and bound share one branch", "manifest exists but product convention pending", "PARTIAL_BRANCH_LOCK_NONCLAIM"),
        ("DEP2981_7_acceptance", "deproxy acceptance", "no proxy, no MISSING markers, source paths, units, projection, no-cancellation", "fails current evidence", "DEPROXY_NOT_COMPLETE"),
    ]
    return [add({"deproxy_id": i, "quantity": q, "requirement": req, "current_evidence": ev, "status": st, "accepted_for_scoring": False}) for i, q, req, ev, st in data]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        add({"candidate_id": "CAND2981_0_delta_w_e", "symbol": "delta_w_e", "value": "8.948213306283e-11", "source_basis": "unit-kernel WEP proxy", "status": "QUARANTINED_PROXY", "why_nonclaim": "tau_eff=1 shortcut refused; parent component/readout/source/product convention missing"}),
        add({"candidate_id": "CAND2981_1_action_line_zero", "symbol": "Delta_w_A theorem-zero", "value": "not available", "source_basis": "single action-density line theorem", "status": "CONDITIONAL_ONLY", "why_nonclaim": "hbar/measure owner and connected graph not parent signed"}),
    ]


def claim_rows() -> list[dict[str, Any]]:
    data = [
        ("CG2981_0_action_line", "single action-density/species-blind measure theorem-zero", False, "not parent-derived", False),
        ("CG2981_1_deltawe", "delta_w_e deproxied as first real coefficient", False, "proxy remains quarantined", False),
        ("CG2981_2_JZ", "J_Z source-current suppression", False, "delta_w/source weights retained", False),
        ("CG2981_3_local_GR", "local GR/Newton reduction", False, "coupling lock not closed", False),
        ("CG2981_4_empirical", "WEP/R10/PPN/clock/orbital claims", False, "no promoted coefficient/theorem-zero", False),
    ]
    return [add({"claim_gate_id": i, "claim": c, "condition_passed": p, "status": s, "claim_allowed": a}) for i, c, p, s, a in data]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add({"decision_id": "DEC2981_0_action_line", "decision": "Do not promote the action-density line theorem.", "because": "the theorem is clean but hbar/measure owner and connected matter graph remain unsigned.", "next_action": "search/derive parent hbar-measure owner specifically"}),
        add({"decision_id": "DEC2981_1_deltawe", "decision": "Do not deproxy delta_w_e.", "because": "unit tau is explicitly refused and the WEP product convention is only partial.", "next_action": "fill tau_eff/readout/source/product convention before using the value"}),
        add({"decision_id": "DEC2981_2_route", "decision": "Split the next move into parent-owner search versus WEP product completion.", "because": "one is derivation-first, the other is empirical plumbing for a finite coefficient.", "next_action": "attempt parent hbar/measure owner source search, with WEP product convention as fallback"}),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add({
            "next_id": "NEXT2981_0_2982",
            "priority": "selected_primary",
            "next_doc": "2982-Y5-R2FR-parent-hbar-measure-owner-source-search-or-wep-tau-product-convention-completion-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_parent_hbar_measure_owner_source_search_or_wep_tau_product_convention_completion_under_AX1090_2982.py",
            "objective": "Search for a real parent hbar/action-measure owner that signs one ordinary-matter action-density line; if absent, complete the WEP tau_eff/readout/source product convention needed to deproxy delta_w_e.",
            "include": "hbar_parent;action measure owner;species-blind measure;connected matter graph;MICROSCOPE product convention;tau_eff;K_CMSM;R_source;material tensor;C_parent",
            "exclude": "broad no-source-slot loop;B_Z full boundary proof;full K_metric certificate;local-GR claim;GitHub action;formalization-workbench edits",
        })
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for p in FORMALIZATION.rglob("*2981*") if p.is_file()) if FORMALIZATION.exists() else 0
    checks = [
        ("VAL2981_0_sources_exist", all(r["exists"] for r in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2981_1_anchors_found", all(r["anchors_found"] for r in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2981_2_action_not_derived", any(r["audit_id"] == "AL2981_6_verdict" and r["status"].startswith("NOT_PARENT_DERIVED") for r in all_rows["action_line"]), "action-density theorem remains unclaimed", True),
        ("VAL2981_3_deproxy_blocked", any(r["deproxy_id"] == "DEP2981_7_acceptance" and r["status"] == "DEPROXY_NOT_COMPLETE" for r in all_rows["deproxy"]), "delta_w_e deproxy remains blocked", True),
        ("VAL2981_4_proxy_nonclaim", all(not r["accepted_for_scoring"] for r in all_rows["deproxy"]), "deproxy rows remain nonclaim", True),
        ("VAL2981_5_claims_blocked", all(not r["claim_allowed"] for r in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2981_6_next_written", any(r["next_id"] == "NEXT2981_0_2982" for r in all_rows["next"]), "2982 parent measure/product target selected", True),
        ("VAL2981_7_branches_exist", all(r["exists"] for r in all_rows["branches"]), "branch copies exist", True),
        ("VAL2981_8_csvs_parse", all(csv_ok(p) for p in csv_paths), "all generated CSVs parse", True),
        ("VAL2981_9_outputs_under_post", all(under(p, ROOT) for p in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2981_10_formalization_clean", formal_count == 0, f"no 2981 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2981_11_doc_written", DOC.exists(), "2981 markdown checkpoint exists", True),
    ]
    out = [add({"validation_id": i, "passed": bool(p), "check": c, "required": req}) for i, p, c, req in checks]
    out.append(add({"validation_id": "VAL2981_OVERALL", "passed": all(r["passed"] for r in out), "check": "2981 validation overall", "required": True}))
    return out


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2981 - Single Action-Density Line and Species-Blind Measure, or delta_w_e Deproxy

Status: `Y5_R2FR_2981_action_density_line_clean_conditional_not_parent_derived_deltawe_deproxy_blocked_tau_product_pending_nonclaim`

Claim ceiling: `no_action_line_theorem_zero_no_deltawe_deproxy_no_JZ_zero_no_q_loc_zero_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The single action-density line route is clean but conditional: connected naturality would collapse relative source weights to a common calibration mode.
- It is not parent-derived yet because `hbar_parent`, the parent measure/Jacobian, and the connected ordinary-matter graph are not signed.
- The `delta_w_e = 8.948213306283e-11` row remains a useful smoke value, but it is still a unit-tau proxy and cannot score.
- The deproxy blockers are now explicit: `tau_eff`, `K_CMSM` sign/units, source kernel, full material tensor, `C_parent`, and same-branch convention.
- Next target is either a real parent hbar/measure owner source search or completion of the WEP product convention.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Action-Line Audit

{table(all_rows["action_line"], ["audit_id", "object", "statement", "status", "blocking_gap", "theorem_zero"])}

## delta_w_e Deproxy Checklist

{table(all_rows["deproxy"], ["deproxy_id", "quantity", "requirement", "current_evidence", "status", "accepted_for_scoring"])}

## Candidate Status

{table(all_rows["candidate"], ["candidate_id", "symbol", "value", "source_basis", "status", "why_nonclaim"])}

## Claim Gates

{table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows = {
        "sources": source_rows(),
        "action_line": action_line_rows(),
        "deproxy": deproxy_rows(),
        "candidate": candidate_rows(),
        "claims": claim_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["action_line"], BRANCH_OUTPUTS["action_line_copy"])
    shutil.copyfile(OUTPUTS["deproxy"], BRANCH_OUTPUTS["deproxy_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2981 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
