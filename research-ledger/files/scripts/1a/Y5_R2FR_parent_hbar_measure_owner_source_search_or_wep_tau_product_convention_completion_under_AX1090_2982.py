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
MICRO = ROOT / "source-intake" / "microscope"
MICRO_Q = MICRO / "quarantine"
MICRO_COEFF = MICRO / "branch_locked_wep" / "coefficients"
MICRO_PRODUCT = MICRO / "product_convention"
MICRO_METADATA = MICRO / "metadata"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2982"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2982-Y5-R2FR-parent-hbar-measure-owner-source-search-or-wep-tau-product-convention-completion-under-AX1090.md"

SRC_2981_DOC = ROOT / "2981-Y5-R2FR-single-action-density-line-and-species-blind-measure-or-deltawe-deproxy-under-AX1090.md"
SRC_2981_NEXT = RESIDUALS / "P8_Y5_R2FR_2981_NEXT_TARGET.csv"
SRC_2981_ACTION = RESIDUALS / "P8_Y5_R2FR_2981_SINGLE_ACTION_DENSITY_LINE_AUDIT.csv"
SRC_2981_DEPROXY = RESIDUALS / "P8_Y5_R2FR_2981_DELTAWE_DEPROXY_CHECKLIST.csv"
SRC_2981_CANDIDATE = RESIDUALS / "P8_Y5_R2FR_2981_DELTAWE_PROXY_STATUS_NONCLAIM.csv"
SRC_2981_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2981_VALIDATION.csv"

SRC_1463_PMO = MICRO_COEFF / "parent_measure_owner_contract_1463.csv"
SRC_1477_GRAPH = MICRO_COEFF / "connected_matter_graph_certificate_nonclaim_1477.csv"
SRC_1452_CMT = MICRO_COEFF / "common_measure_current_theorem_attempt_1452.csv"
SRC_PRODUCT = MICRO_PRODUCT / "P_WEP_eta_product_convention.csv"
SRC_PRODUCT_STATUS = MICRO / "branch_locked_wep" / "product" / "P_WEP_eta_product_status_1482.csv"
SRC_SHORTCUT = MICRO_METADATA / "P8_Y5_R10_1336_ANTI_SHORTCUT_GATES.csv"
SRC_PROD_SCHEMA = MICRO_METADATA / "P8_Y5_R10_1336_PRODUCT_CONVENTION_SCHEMA.csv"
SRC_1479_DW = MICRO_Q / "1479" / "COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"
SRC_1480_SMOKE = MICRO_Q / "1480" / "SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv"
SRC_1481_UPDATE = MICRO_Q / "1481" / "SAME_BRANCH_WEP_SMOKE_UPDATE_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2982_SOURCE_REGISTER.csv",
    "hbar_owner": RESIDUALS / "P8_Y5_R2FR_2982_PARENT_HBAR_MEASURE_OWNER_SOURCE_SEARCH.csv",
    "wep_product": RESIDUALS / "P8_Y5_R2FR_2982_WEP_TAU_PRODUCT_CONVENTION_COMPLETION_AUDIT.csv",
    "deltawe": RESIDUALS / "P8_Y5_R2FR_2982_DELTAWE_DEPROXY_STATUS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2982_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2982_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2982_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2982_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2982_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hbar_owner_copy": PARENT_ACTION / "parent_hbar_measure_owner_source_search_2982_NOT_DERIVED.csv",
    "wep_product_copy": LOCAL_BOUNDS / "wep_tau_product_convention_completion_audit_2982_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2982_wep_product_completion_or_parent_measure_owner_next_NONCLAIM.csv",
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
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


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
        ("SRC2982_00_2981_doc", SRC_2981_DOC, ["Status:", "Next target"], "2981 markdown handoff"),
        ("SRC2982_01_2981_next", SRC_2981_NEXT, ["NEXT2981_0_2982", "hbar_parent"], "selected 2982 target"),
        ("SRC2982_02_2981_action", SRC_2981_ACTION, ["AL2981_2_hbar_measure", "AL2981_6_verdict"], "action-line audit"),
        ("SRC2982_03_2981_deproxy", SRC_2981_DEPROXY, ["DEP2981_1_tau", "DEP2981_7_acceptance"], "delta_w_e deproxy checklist"),
        ("SRC2982_04_2981_candidate", SRC_2981_CANDIDATE, ["CAND2981_0_delta_w_e", "QUARANTINED_PROXY"], "delta_w_e proxy status"),
        ("SRC2982_05_2981_validation", SRC_2981_VALIDATION, ["VAL2981_OVERALL"], "2981 validation"),
        ("SRC2982_06_pmo1463", SRC_1463_PMO, ["PMO1463_0_action_density_line", "PMO1463_6_verdict"], "parent measure owner contract"),
        ("SRC2982_07_graph1477", SRC_1477_GRAPH, ["GRC1477_1_parent_owned_connectivity", "FAIL_NOT_PARENT_SIGNED"], "connected matter graph"),
        ("SRC2982_08_cmt1452", SRC_1452_CMT, ["CMT1452_2_quantum_measure_route", "CMT1452_6_verdict"], "common measure/current theorem"),
        ("SRC2982_09_product", SRC_PRODUCT, ["tau_eff", "PRODUCT_CONVENTION_OFFICIAL_PARTIAL_EXTRACTION_NONCLAIM"], "partial WEP product convention"),
        ("SRC2982_10_product_status", SRC_PRODUCT_STATUS, ["MAN1482_0_live_readout", "MAN1482_6_C_parent_import"], "required WEP live-file manifest"),
        ("SRC2982_11_shortcut", SRC_SHORTCUT, ["SHORT1336_2_no_unity_tau", "REFUSED"], "anti-shortcut gate"),
        ("SRC2982_12_prod_schema", SRC_PROD_SCHEMA, ["PRODSCHEMA1336_2_tau_eff_definition", "MISSING_PRODUCT_CONVENTION_FILE"], "product convention schema"),
        ("SRC2982_13_delta_pack", SRC_1479_DW, ["CBP1479_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"], "delta_w component pack"),
        ("SRC2982_14_smoke1480", SRC_1480_SMOKE, ["WSR1480_1_electron_unit_kernel_quarantine", "PROXY_COMPUTED_QUARANTINED"], "same-branch WEP smoke"),
        ("SRC2982_15_update1481", SRC_1481_UPDATE, ["WUP1481_1_electron_tau_rescaling_template", "UNIT_TAU_ONLY_QUARANTINED"], "tau rescaling smoke update"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def parent_hbar_owner_rows() -> list[dict[str, Any]]:
    data = [
        (
            "HMO2982_0_hbar_parent",
            "single parent hbar/action scale",
            "A real owner would put ordinary matter under one hbar_parent, not hbar_A or w_A slots.",
            "contracts found in PMO1463/CMT1452, but no parent action source constructs the owner",
            "CONTRACT_FOUND_NOT_PARENT_SIGNED",
            False,
        ),
        (
            "HMO2982_1_action_density_line",
            "one ordinary-matter action-density line",
            "S_ord = integral dmu_parent L_ord / hbar_parent with no species-only source prefactor.",
            "2981/1463 make the exact conditional theorem; line owner remains unsigned",
            "CONDITIONAL_THEOREM_ONLY",
            False,
        ),
        (
            "HMO2982_2_species_blind_measure",
            "species-blind measure/Jacobian descent",
            "The parent measure must descend without species-only J_A factors.",
            "CMT1452 identifies the species-Jacobian countermodel and leaves it open",
            "MEASURE_JACOBIAN_NOT_SIGNED",
            False,
        ),
        (
            "HMO2982_3_connected_matter_graph",
            "connected ordinary-matter morphism graph",
            "Connected naturality would force w_A=w_* across ordinary matter.",
            "GRC1477 has a template component but parent-owned connectivity fails",
            "TEMPLATE_ONLY_PARENT_GRAPH_UNSIGNED",
            False,
        ),
        (
            "HMO2982_4_current_owner",
            "source/current extraction owner",
            "J_src must come from the same action owner before readout, with no c_A/zeta_A bypass.",
            "Hilbert route is partial and non-Hilbert bypass remains open",
            "CURRENT_OWNER_PARTIAL_NONHILBERT_BYPASS_OPEN",
            False,
        ),
        (
            "HMO2982_5_search_verdict",
            "parent hbar/measure owner source search",
            "Sufficient source would explicitly construct hbar_parent, dmu_parent, action line, connected graph, and current owner.",
            "no such parent-signed source found in the active branch evidence",
            "NO_PARENT_SIGNED_OWNER_FOUND",
            False,
        ),
        (
            "HMO2982_6_impact",
            "local-GR/source-weight impact",
            "Without the owner, delta_w, J_A, c_A, and non-Hilbert slots cannot be theorem-zeroed.",
            "the branch must stay residual/bound-input rather than theorem-zero",
            "DEMOTE_PARENT_OWNER_TO_CLOSURE_UNLESS_NEW_SOURCE",
            False,
        ),
    ]
    return [
        add(
            {
                "audit_id": audit_id,
                "target": target,
                "required_parent_clause": required,
                "evidence": evidence,
                "status": status,
                "parent_signed": parent_signed,
            }
        )
        for audit_id, target, required, evidence, status, parent_signed in data
    ]


def product_manifest_audit_rows() -> list[dict[str, Any]]:
    out_rows: list[dict[str, Any]] = []
    manifest = rows(SRC_PRODUCT_STATUS)
    for index, row in enumerate(manifest):
        target_path = Path(row.get("target_path", ""))
        target_exists_actual = target_path.exists() if str(target_path) else False
        promotion_allowed = str(row.get("promotion_allowed_now", "")).lower() == "true"
        current_status = row.get("current_status", "")
        if promotion_allowed and target_exists_actual and "MISSING" not in current_status and "NONCLAIM" not in current_status:
            row_status = "PROMOTION_CANDIDATE_REQUIRES_REVIEW"
        elif target_exists_actual:
            row_status = "EXISTS_BUT_NONCLAIM_OR_REQUIREMENTS_ONLY"
        else:
            row_status = "MISSING_REQUIRED_LIVE_FILE"
        out_rows.append(
            add(
                {
                    "audit_id": f"WEP2982_{index}_{row.get('pack_item', 'unknown')}",
                    "pack_item": row.get("pack_item", ""),
                    "target_path": row.get("target_path", ""),
                    "expected_file": row.get("expected_file", ""),
                    "file_expectation": row.get("file_expectation", ""),
                    "manifest_target_exists": row.get("target_exists", ""),
                    "target_exists_actual": target_exists_actual,
                    "current_status": current_status,
                    "promotion_allowed_now": promotion_allowed,
                    "audit_status": row_status,
                }
            )
        )
    product_convention = rows(SRC_PRODUCT)
    if product_convention:
        row = product_convention[0]
        out_rows.append(
            add(
                {
                    "audit_id": "WEP2982_product_formula",
                    "pack_item": "product_convention_formula",
                    "target_path": str(SRC_PRODUCT),
                    "expected_file": SRC_PRODUCT.name,
                    "file_expectation": row.get("tau_eff_definition", ""),
                    "manifest_target_exists": True,
                    "target_exists_actual": SRC_PRODUCT.exists(),
                    "current_status": row.get("row_status", ""),
                    "promotion_allowed_now": False,
                    "audit_status": "PARTIAL_TAU_FORMULA_PRESENT_BUT_SIGN_UNITS_MASKS_PENDING",
                }
            )
        )
    out_rows.append(
        add(
            {
                "audit_id": "WEP2982_no_unity_tau",
                "pack_item": "anti_shortcut_gate",
                "target_path": str(SRC_SHORTCUT),
                "expected_file": SRC_SHORTCUT.name,
                "file_expectation": "tau_eff=1 shortcut must be refused until readout/source/product are real",
                "manifest_target_exists": True,
                "target_exists_actual": SRC_SHORTCUT.exists(),
                "current_status": "SHORT1336_2_no_unity_tau_ENFORCED",
                "promotion_allowed_now": False,
                "audit_status": "UNITY_TAU_REFUSED",
            }
        )
    )
    missing_required = [row for row in out_rows if row.get("audit_status") == "MISSING_REQUIRED_LIVE_FILE"]
    out_rows.append(
        add(
            {
                "audit_id": "WEP2982_verdict",
                "pack_item": "wep_tau_product_completion",
                "target_path": "manifest+product_convention",
                "expected_file": "K_CMSM,R_source,full_material_tensor,C_parent plus sign/units/orbit mask",
                "file_expectation": "all live files must exist in same parent branch before delta_w_e can score",
                "manifest_target_exists": "mixed",
                "target_exists_actual": len(missing_required) == 0,
                "current_status": f"missing_required_live_files={len(missing_required)}",
                "promotion_allowed_now": False,
                "audit_status": "PRODUCT_CONVENTION_NOT_COMPLETE",
            }
        )
    )
    return out_rows


def deltawe_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DW2982_0_proxy_value",
            "delta_w_e",
            "8.948213306283e-11",
            "CBP1479/WSR1480/WUP1481",
            "unit-kernel electron proxy",
            "QUARANTINED_PROXY",
            False,
        ),
        (
            "DW2982_1_tau_formula",
            "tau_eff",
            "branch_locked_orbit_average(K_CMSM * R_source * readout_mask)",
            "P_WEP_eta_product_convention.csv",
            "shape exists, but K_CMSM sign/units, source units, official masks, and orbit weighting are pending",
            "FORMULA_PRESENT_INPUTS_MISSING",
            False,
        ),
        (
            "DW2982_2_bound_template",
            "epsilon_e_bound(tau_eff)",
            "eta_bound/(DeltaF_e_abs*abs(tau_eff))",
            "SAME_BRANCH_WEP_SMOKE_UPDATE_NONCLAIM.csv",
            "template useful only after tau_eff is real",
            "NONCLAIM_TEMPLATE",
            False,
        ),
        (
            "DW2982_3_product_missing",
            "claim-grade WEP product",
            "eta_pred=abs(K_CMSM * R_source dot C_parent dot R_material)",
            "P_WEP_eta_product_status_1482.csv",
            "K_CMSM, R_source, full material tensor, and C_parent live files are missing or requirements-only",
            "BLOCKED_MISSING_PRODUCT_FACTORS",
            False,
        ),
        (
            "DW2982_4_acceptance",
            "delta_w_e deproxy acceptance",
            "no proxy rows, no MISSING markers, sourced units, no-cancellation/covariance, same branch",
            "2982 audit",
            "fails because product convention and parent coefficient are not complete",
            "DEPROXY_NOT_COMPLETE",
            False,
        ),
    ]
    return [
        add(
            {
                "deproxy_id": deproxy_id,
                "quantity": quantity,
                "value_or_formula": value,
                "source": source,
                "evidence": evidence,
                "status": status,
                "accepted_for_scoring": accepted,
            }
        )
        for deproxy_id, quantity, value, source, evidence, status, accepted in data
    ]


def claim_rows() -> list[dict[str, Any]]:
    data = [
        ("CG2982_0_hbar_owner", "parent hbar/action-measure owner derived", False, "no parent-signed source found", False),
        ("CG2982_1_action_line_zero", "single action-density theorem-zero for source weights", False, "closure clause only", False),
        ("CG2982_2_deltawe", "delta_w_e promoted to real coefficient/bound", False, "WEP product convention incomplete", False),
        ("CG2982_3_JZ", "J_Z/source-current residual theorem-zero", False, "source-weight/current-owner slots remain open", False),
        ("CG2982_4_local_GR", "local GR/Newton reduction claim", False, "coupling bridge not closed", False),
        ("CG2982_5_empirical", "WEP/R10/PPN/clock/orbital scoring", False, "no claim-grade coefficient row", False),
    ]
    return [add({"claim_gate_id": gate_id, "claim": claim, "condition_passed": passed, "status": status, "claim_allowed": allowed}) for gate_id, claim, passed, status, allowed in data]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2982_0_parent_owner",
                "decision": "Do not promote the parent hbar/action-measure route.",
                "because": "the exact conditional theorem is still missing a parent-signed owner, measure/Jacobian descent, connected graph, and current owner.",
                "next_action": "treat parent owner as an explicit closure clause unless a new parent action source is introduced",
            }
        ),
        add(
            {
                "decision_id": "DEC2982_1_product",
                "decision": "Move from abstract coupling hunt to concrete WEP live-file completion.",
                "because": "the product manifest identifies missing K_CMSM, R_source, full material tensor, and C_parent files, so this is no longer a vague blocker.",
                "next_action": "build or source the four live files in one branch before reusing delta_w_e",
            }
        ),
        add(
            {
                "decision_id": "DEC2982_2_claim_ceiling",
                "decision": "Keep all local-GR/WEP/R10/PPN/orbital claims blocked.",
                "because": "neither theorem-zero nor finite claim-grade coefficient is available yet.",
                "next_action": "next checkpoint should be file-acquisition/plumbing, not another no-source loop",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2982_0_2983",
                "priority": "selected_primary",
                "next_doc": "2983-Y5-R2FR-WEP-live-file-acquisition-or-parent-measure-owner-closure-demotion-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_WEP_live_file_acquisition_or_parent_measure_owner_closure_demotion_under_AX1090_2983.py",
                "objective": "Stop circling the coupling gap: either acquire/build the WEP live files K_CMSM, R_source, full material tensor, and C_parent in one branch, or explicitly demote parent hbar/measure owner to a closure clause.",
                "include": "P_WEP_K_CMSM_readout.csv;P_WEP_R_source_Earth_worldtube.csv;P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv;C_parent_WEP_slot_import.csv;sign units masks source paths same branch",
                "exclude": "local-GR claim;unit tau shortcut;proxy promotion;new galaxy work;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for p in FORMALIZATION.rglob("*2982*") if p.is_file()) if FORMALIZATION.exists() else 0
    product_missing = any(row.get("audit_status") == "MISSING_REQUIRED_LIVE_FILE" for row in all_rows["wep_product"])
    checks = [
        ("VAL2982_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2982_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2982_2_hbar_not_parent_signed", any(row["audit_id"] == "HMO2982_5_search_verdict" and row["status"] == "NO_PARENT_SIGNED_OWNER_FOUND" for row in all_rows["hbar_owner"]), "parent hbar/measure owner search stays unclaimed", True),
        ("VAL2982_3_product_missing_visible", product_missing, "required WEP live-file gaps are visible", True),
        ("VAL2982_4_deltawe_nonclaim", any(row["deproxy_id"] == "DW2982_4_acceptance" and row["status"] == "DEPROXY_NOT_COMPLETE" for row in all_rows["deltawe"]), "delta_w_e deproxy remains blocked", True),
        ("VAL2982_5_claims_blocked", all(not row["claim_allowed"] for row in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2982_6_next_written", any(row["next_id"] == "NEXT2982_0_2983" for row in all_rows["next"]), "2983 concrete live-file target selected", True),
        ("VAL2982_7_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2982_8_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2982_9_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2982_10_formalization_clean", formal_count == 0, f"no 2982 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2982_11_doc_written", DOC.exists(), "2982 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2982_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2982 validation overall", "required": True}))
    return out_rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2982 - Parent hbar/Measure Owner Source Search or WEP Product Convention Completion

Status: `Y5_R2FR_2982_parent_hbar_measure_owner_not_found_wep_product_live_files_missing_deltawe_nonclaim`

Claim ceiling: `no_parent_hbar_owner_no_action_line_theorem_zero_no_deltawe_deproxy_no_JZ_zero_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The parent `hbar_parent`/action-measure owner route was searched against the active branch evidence and remains unsigned, not disproven.
- The clean 2981 theorem is therefore still a closure/theorem-if-parent-signed result, not a derived local-GR bridge.
- The WEP side is now less foggy: the live missing pieces are `K_CMSM`, `R_source`, full material tensor, and `C_parent` in one same-parent branch.
- `delta_w_e = 8.948213306283e-11` remains quarantined because `tau_eff=1` is explicitly refused and the WEP product is incomplete.
- Best next move is no longer another broad coupling loop: acquire/build the missing WEP live files or demote the parent measure owner to an explicit closure clause.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Parent hbar/Measure Owner Search

{table(all_rows["hbar_owner"], ["audit_id", "target", "required_parent_clause", "evidence", "status", "parent_signed"])}

## WEP Product Convention Audit

{table(all_rows["wep_product"], ["audit_id", "pack_item", "target_exists_actual", "current_status", "promotion_allowed_now", "audit_status"])}

## delta_w_e Deproxy Status

{table(all_rows["deltawe"], ["deproxy_id", "quantity", "value_or_formula", "evidence", "status", "accepted_for_scoring"])}

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
        "hbar_owner": parent_hbar_owner_rows(),
        "wep_product": product_manifest_audit_rows(),
        "deltawe": deltawe_rows(),
        "claims": claim_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["hbar_owner"], BRANCH_OUTPUTS["hbar_owner_copy"])
    shutil.copyfile(OUTPUTS["wep_product"], BRANCH_OUTPUTS["wep_product_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2982 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
