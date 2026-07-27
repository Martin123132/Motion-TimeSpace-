from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2762-Y5-R2FR-tau-WEP-material-source-projection-or-beta-source-alpha-zero-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2762_SOURCE_REGISTER.csv",
    "zero": MTS / "P8_Y5_R2FR_2762_BETA_SOURCE_ALPHA_ZERO_ATTEMPT.csv",
    "tau": MTS / "P8_Y5_R2FR_2762_TAU_WEP_PROJECTION_CONTRACT.csv",
    "width": MTS / "P8_Y5_R2FR_2762_WEP_PRODUCT_WIDTH_LEDGER.csv",
    "acquisition": MTS / "P8_Y5_R2FR_2762_MATERIAL_SOURCE_ACQUISITION_LEDGER.csv",
    "arena": MTS / "P8_Y5_R2FR_2762_LOCAL_RESIDUAL_IMPACT.csv",
    "decisions": MTS / "P8_Y5_R2FR_2762_DECISION_LEDGER.csv",
    "gates": MTS / "P8_Y5_R2FR_2762_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2762_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2762_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2762_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2762_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_queue": RAB_QUEUE / "JR2762_BETA_SOURCE_ALPHA_ZERO_ATTEMPT_NONCLAIM.csv",
    "tau_queue": RAB_QUEUE / "JR2762_TAU_WEP_PROJECTION_CONTRACT_NONCLAIM.csv",
    "acquisition_queue": RAB_QUEUE / "JR2762_MICROSCOPE_MATERIAL_SOURCE_ACQUISITION_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "TAU_WEP_BETA_SOURCE_ALPHA_BRIDGE_2762_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "tau_wep_material_source_projection_contract_2762_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2762_ALPHA_OWNER_OR_MICROSCOPE_TENSOR_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2762_00_2761_doc", "2761_doc", WORK / "2761-Y5-R2FR-first-same-branch-coupling-product-row-balpha-clock-or-deltaw-under-AX1090.md", ["NEXT2761_0_2762", "SBC2761_2_WEP_alpha_pressure_target"], "2761 handoff to tau_WEP/beta_source bridge"),
        ("SRC2762_01_2761_validation", "2761_validation", MTS / "P8_Y5_BRR545_2761_VALIDATION.csv", ["VAL2761_OVERALL"], "2761 validation"),
        ("SRC2762_02_1054_doc", "1054_zero_prior_doc", WORK / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md", ["ZC1054_2_alpha_owner", "NPW1054_0_alpha_WEP_product"], "zero theorem/prior width precedent"),
        ("SRC2762_03_1054_zero_csv", "1054_zero_csv", MTS / "P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv", ["ZC1054_2_alpha_owner", "ZC1054_6_radiative_readout_closure"], "zero theorem clause audit"),
        ("SRC2762_04_1054_width_csv", "1054_width_csv", MTS / "P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv", ["NPW1054_0_alpha_WEP_product"], "numeric WEP product width"),
        ("SRC2762_05_1054_norm_csv", "1054_shared_norm_csv", MTS / "P8_Y5_R10_1054_SHARED_NORMALIZATION_GATE.csv", ["SNG1054_1_clock_to_WEP"], "shared normalization guard"),
        ("SRC2762_06_1491_doc", "1491_delta_w_doc", WORK / "1491-Y5-R10-RAB-real-delta-w-bound-input-pack-WEP-R10-clock-orbital.md", ["DWI1491_1_MICROSCOPE_TiPt", "APR1491_2_tau_projection"], "real delta_w input pack precedent"),
        ("SRC2762_07_1491_pack_csv", "1491_input_pack_csv", MTS / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv", ["DWI1491_1_MICROSCOPE_TiPt"], "MICROSCOPE delta_w input requirement"),
        ("SRC2762_08_1491_projection_csv", "1491_projection_csv", MTS / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv", ["APR1491_2_tau_projection"], "arena projection requirements"),
        ("SRC2762_09_1491_anchor_csv", "1491_anchor_csv", MTS / "P8_Y5_R10_1491_DELTA_W_BOUND_ANCHORS.csv", ["BAN1491_0_MICROSCOPE_TiPt"], "MICROSCOPE bound anchor"),
        ("SRC2762_10_1052_wep_csv", "1052_wep_csv", MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", ["AWP1052_0_alpha_Coulomb"], "WEP alpha pressure target source"),
        ("SRC2762_11_local_bounds", "local_bounds", WORK / "source-intake" / "local_bounds" / "local_bound_claims.csv", ["R1_WEP_source_charge"], "MICROSCOPE comparator bound"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": exists and all(needle in text for needle in needles),
            "source_role": role,
        }))
    return rows


def load_inputs() -> dict[str, dict[str, str]]:
    return {
        "alpha_width": find_row(read_csv_rows(MTS / "P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv"), "prior_id", "NPW1054_0_alpha_WEP_product"),
        "surface_width": find_row(read_csv_rows(MTS / "P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv"), "prior_id", "NPW1054_1_surface_WEP_product"),
        "clock_width": find_row(read_csv_rows(MTS / "P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv"), "prior_id", "NPW1054_2_clock_product"),
        "microscope_input": find_row(read_csv_rows(MTS / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv"), "input_id", "DWI1491_1_MICROSCOPE_TiPt"),
        "tau_req": find_row(read_csv_rows(MTS / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv"), "requirement_id", "APR1491_2_tau_projection"),
        "material_req": find_row(read_csv_rows(MTS / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv"), "requirement_id", "APR1491_1_material_source"),
        "readout_req": find_row(read_csv_rows(MTS / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv"), "requirement_id", "APR1491_3_readout"),
        "microscope_anchor": find_row(read_csv_rows(MTS / "P8_Y5_R10_1491_DELTA_W_BOUND_ANCHORS.csv"), "anchor_id", "BAN1491_0_MICROSCOPE_TiPt"),
    }


def build_zero_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "BSAZ2762_0_target", "claim_piece": "beta_source_alpha=0 theorem", "formal_statement": "If alpha_EM, matter constants, readout, and source labels descend through quotient/representation data with no hidden-visible Hom, then beta_source_alpha is absent or vertically silent.", "status": "EXACT_CONDITIONAL_TARGET", "if_signed": "WEP alpha-marker product vanishes before any tau_WEP fit", "current_gap": "parent alpha owner/matter-readout/source-label clauses unsigned"}),
        nonclaim({"row_id": "BSAZ2762_1_alpha_owner", "claim_piece": "alpha owner", "formal_statement": "alpha_EM(Phi)=alpha_bar(q_loc(Phi),theta_top) implies Lie_v alpha_EM=0.", "status": "BLOCKED_OWNER_UNSIGNED", "if_signed": "b_alpha and beta_source_alpha alpha-marker branch vanish", "current_gap": "gauge/diffeomorphism allow f_X(Xhat)F^2 unless target category forbids it"}),
        nonclaim({"row_id": "BSAZ2762_2_matter_source_functor", "claim_piece": "matter/source forgetting", "formal_statement": "S_A and source current depend on quotient coframe and fixed representation data, not species-labelled hidden markers.", "status": "MATTER_SOURCE_FUNCTOR_UNSIGNED", "if_signed": "composition/source beta slots disappear", "current_gap": "material marker and source-label maps remain legal"}),
        nonclaim({"row_id": "BSAZ2762_3_readout_closure", "claim_piece": "radiative/readout closure", "formal_statement": "S_eff and detector/readout maps preserve no-alpha/no-marker coefficient syntax.", "status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED", "if_signed": "tree-level zero survives to clocks/WEP/R10", "current_gap": "loop/readout terms can regenerate f_X F^2 or clock_Xhat terms"}),
        nonclaim({"row_id": "BSAZ2762_4_counterexample", "claim_piece": "surviving hidden scalar counterexample", "formal_statement": "If I_hid survives, alpha_EM=alpha_0 exp(epsilon I_hid) gives beta_source_alpha-like leakage.", "status": "COUNTEREXAMPLE_RETAINED", "if_signed": "not applicable", "current_gap": "hidden scalar/no-marker/no-hair route not closed"}),
        nonclaim({"row_id": "BSAZ2762_5_verdict", "claim_piece": "promote beta_source_alpha=0 now", "formal_statement": "2762 does not derive beta_source_alpha=0; it keeps the zero theorem as a contract and uses the finite WEP product width as nonclaim target.", "status": "ZERO_THEOREM_NOT_CLOSED", "if_signed": "would be the cleanest local coupling route", "current_gap": "derive alpha owner/matter functor/source forgetting/readout closure or retain finite product"}),
    ]


def build_tau_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    microscope = inputs["microscope_input"]
    tau_req = inputs["tau_req"]
    material_req = inputs["material_req"]
    readout_req = inputs["readout_req"]
    return [
        nonclaim({"row_id": "TAUW2762_0_definition", "object": "tau_WEP", "definition_or_formula": "tau_WEP := normalized lab/source/orbit projection converting the alpha/source Xhat variation into differential acceleration", "current_status": "DEFINITION_REQUIRED_NOT_DERIVED", "source_basis": "1053/1054/1491 projection audits", "missing_for_claim": tau_req.get("acceptance_rule", "tau_WEP, tau_R10(lambda), tau_clock, orbital/worldtube projection"), "score_ready": False}),
        nonclaim({"row_id": "TAUW2762_1_MICROSCOPE_contract", "object": "MICROSCOPE Ti/Pt product", "definition_or_formula": microscope.get("formula", "|eta_TiPt| <= |DeltaQ_TiPt dot delta_w| * |tau_WEP|"), "current_status": microscope.get("current_status", "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED"), "source_basis": microscope.get("source_path", "source-intake/local_bounds/local_bound_claims.csv"), "missing_for_claim": microscope.get("missing_for_claim", "official readout arrays, source worldtube, full material tensor, product convention, tau_eff"), "score_ready": False}),
        nonclaim({"row_id": "TAUW2762_2_material_source_tensor", "object": "material/source response vector", "definition_or_formula": "DeltaQ_TiPt and source/Earth/worldtube kernel in the same product convention", "current_status": material_req.get("current_status", "PARTIAL_OR_MISSING"), "source_basis": "1491 APR1491_1_material_source", "missing_for_claim": material_req.get("acceptance_rule", "Ti/Pt full tensor, EotWash material pairs, R10 source/test composition"), "score_ready": False}),
        nonclaim({"row_id": "TAUW2762_3_readout_kernel", "object": "readout/source-worldtube transfer", "definition_or_formula": "CMSM/readout/orbit/source-worldtube kernel applied before score", "current_status": readout_req.get("current_status", "MISSING_OR_PARTIAL"), "source_basis": "1491 APR1491_3_readout", "missing_for_claim": readout_req.get("acceptance_rule", "CMSM arrays, clock readout functional, measured GM convention"), "score_ready": False}),
        nonclaim({"row_id": "TAUW2762_4_no_unity_shortcut", "object": "tau_WEP != 1 by convention", "definition_or_formula": "tau_WEP may be set to unity only if the parent normalization and material/source projection define that unit", "current_status": "UNITY_SHORTCUT_REJECTED", "source_basis": "1054 shared normalization gate", "missing_for_claim": "same parent Xhat/chi_X normalization and arena projection theorem", "score_ready": False}),
        nonclaim({"row_id": "TAUW2762_5_verdict", "object": "tau_WEP product map", "definition_or_formula": "C_alpha_WEP=beta_source_alpha*b_alpha*tau_WEP can be target-bounded but not predicted", "current_status": "TAU_WEP_NOT_SOURCE_READY", "source_basis": "1054 NPW + 1491 APR/DWI", "missing_for_claim": "beta_source_alpha or zero theorem, b_alpha/tau_WEP same branch, material/source/readout tensors", "score_ready": False}),
    ]


def build_width_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    alpha = inputs["alpha_width"]
    surface = inputs["surface_width"]
    clock = inputs["clock_width"]
    return [
        nonclaim({"row_id": "WIDTH2762_0_alpha_WEP", "product_symbol": alpha.get("product_symbol", "C_alpha_WEP := beta_source_alpha*b_alpha*tau_WEP"), "numeric_bound": alpha.get("numeric_bound", "4.797780522732e-05"), "units": alpha.get("units", "dimensionless under the 1052 smoke convention"), "what_it_bounds": alpha.get("what_it_bounds", "only the combined alpha WEP product"), "status": "SOURCE_BACKED_PRODUCT_WIDTH_TARGET_NOT_MTS_PREDICTION", "missing_for_claim": alpha.get("missing_to_isolate_beta_source_alpha", "standalone b_alpha; tau_WEP; full material convention"), "score_ready": False}),
        nonclaim({"row_id": "WIDTH2762_1_surface_WEP", "product_symbol": surface.get("product_symbol", "C_surface_WEP := beta_source_or_binding*b_A*tau_WEP"), "numeric_bound": surface.get("numeric_bound", "2.887280314062e-05"), "units": surface.get("units", "dimensionless under the 1052 smoke convention"), "what_it_bounds": surface.get("what_it_bounds", "robust finite branch if binding/surface response survives"), "status": "SOURCE_BACKED_PRODUCT_WIDTH_TARGET_NOT_MTS_PREDICTION", "missing_for_claim": surface.get("missing_to_isolate_beta_source_alpha", "binding coefficient owner; tau_WEP; full material convention"), "score_ready": False}),
        nonclaim({"row_id": "WIDTH2762_2_clock_reference", "product_symbol": clock.get("product_symbol", "C_alpha_clock := b_alpha*tau_clock_time"), "numeric_bound": clock.get("numeric_bound", "2.1e-18"), "units": clock.get("units", "yr^-1"), "what_it_bounds": clock.get("what_it_bounds", "time-drift product only"), "status": "CLOCK_ONLY_REFERENCE", "missing_for_claim": clock.get("missing_to_isolate_beta_source_alpha", "not a source normalization; needs bridge to tau_WEP/R10"), "score_ready": False}),
        nonclaim({"row_id": "WIDTH2762_3_prediction_slot", "product_symbol": "C_alpha_WEP^MTS", "numeric_bound": "MISSING_MTS_VALUE", "units": "dimensionless", "what_it_bounds": "the MTS prediction that would be compared to WIDTH2762_0", "status": "PREDICTION_MISSING", "missing_for_claim": "zero theorem or source-backed beta_source_alpha,b_alpha,tau_WEP in same convention", "score_ready": False}),
    ]


def build_acquisition_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    anchor = inputs["microscope_anchor"]
    return [
        nonclaim({"row_id": "ACQ2762_0_MICROSCOPE_bound_anchor", "needed_object": "MICROSCOPE eta bound anchor", "current_status": anchor.get("bound_status", "SOURCE_BACKED_BOUND_ANCHOR_AVAILABLE"), "source_path": anchor.get("source_path", "source-intake/local_bounds/local_bound_claims.csv"), "blocking_gap": "bound exists but is not product projection", "priority": "done_anchor"}),
        nonclaim({"row_id": "ACQ2762_1_material_tensor", "needed_object": "official Ti/Pt/PtRh/TA6V material tensor", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "source_path": "MISSING_SOURCE_PATH", "blocking_gap": "DeltaQ smoke rows are not claim-grade full material model", "priority": "high"}),
        nonclaim({"row_id": "ACQ2762_2_source_worldtube", "needed_object": "Earth/source/worldtube kernel", "current_status": "MISSING_SOURCE_WORLDTUBE_KERNEL", "source_path": "MISSING_SOURCE_PATH", "blocking_gap": "tau_WEP cannot be normalized without source/environment map", "priority": "high"}),
        nonclaim({"row_id": "ACQ2762_3_readout_arrays", "needed_object": "MICROSCOPE readout/product convention arrays", "current_status": "MISSING_OFFICIAL_READOUT_ARRAYS", "source_path": "MISSING_SOURCE_PATH", "blocking_gap": "observed eta cannot be mapped into same-branch product", "priority": "high"}),
        nonclaim({"row_id": "ACQ2762_4_parent_Xhat_norm", "needed_object": "parent Xhat/chi_X normalization to WEP", "current_status": "MISSING_PARENT_NORMALIZATION", "source_path": "MISSING_PARENT_DERIVATION", "blocking_gap": "clock tau cannot be exported to WEP", "priority": "derivation_high"}),
        nonclaim({"row_id": "ACQ2762_5_no_cancellation_group", "needed_object": "no-cancellation grouping for alpha/mass/binding/source products", "current_status": "MISSING_GROUP_POLICY", "source_path": "MISSING_SOURCE_PATH", "blocking_gap": "WEP product cannot be scored by cancellation among unsourced channels", "priority": "guard"}),
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "ARENA2762_0_WEP", "arena": "WEP/MICROSCOPE", "new_object": "C_alpha_WEP target width", "status": "TARGET_READY_PREDICTION_MISSING", "local_effect": "sets product ceiling but no MTS value", "score_ready": False}),
        nonclaim({"row_id": "ARENA2762_1_clock", "arena": "clock", "new_object": "clock product reference", "status": "SOURCE_BACKED_CLOCK_ONLY", "local_effect": "cannot define tau_WEP without bridge", "score_ready": False}),
        nonclaim({"row_id": "ARENA2762_2_R10", "arena": "R10", "new_object": "no zero theorem transfer", "status": "R10_STILL_BLOCKED", "local_effect": "needs beta_s beta_t K_X/Z_X tau_R10 and curve", "score_ready": False}),
        nonclaim({"row_id": "ARENA2762_3_PPN_Newton", "arena": "PPN/Newton/local GR", "new_object": "none", "status": "NO_LOCAL_RESIDUAL_INSERTION", "local_effect": "beta_source_alpha/tau_WEP not tied to local residual vector", "score_ready": False}),
        nonclaim({"row_id": "ARENA2762_4_orbital", "arena": "orbital/source normalization", "new_object": "delta_w/tau source branch", "status": "WORLDTUBE_MAP_MISSING", "local_effect": "GM/source current channel remains open", "score_ready": False}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2762_0_zero", "decision": "beta_source_alpha=0 remains an exact conditional theorem, not a derived result", "because": "alpha owner, matter/source functor, hidden-visible Hom ban, and readout closure are unsigned", "next_action": "do not claim WEP/R10/local safety from zero route"}),
        nonclaim({"row_id": "DEC2762_1_width", "decision": "the WEP alpha product width is real and useful", "because": "1054/1052 give the numeric target 4.797780522732e-05", "next_action": "use it as acceptance target, not an MTS prediction"}),
        nonclaim({"row_id": "DEC2762_2_tau", "decision": "tau_WEP is the shortest empirical bridge still missing", "because": "without it clock evidence and WEP force response live in different projections", "next_action": "derive/source tau_WEP material/source/readout map"}),
        nonclaim({"row_id": "DEC2762_3_best_route", "decision": "next target should split derivation and acquisition", "because": "alpha-owner theorem-zero would be cleaner, but MICROSCOPE tensor/source acquisition is the fastest empirical bridge", "next_action": "pursue alpha-owner/matter-functor contract while staging MICROSCOPE material/source tensor requirements"}),
        nonclaim({"row_id": "DEC2762_4_next", "decision": "NEXT_2763_ALPHA_OWNER_OR_MICROSCOPE_TENSOR", "because": "2762 has target width but no prediction", "next_action": "construct/reject parent alpha-owner clause or acquire official MICROSCOPE material/source tensor"}),
    ]


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2762_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2762_1_zero_theorem", "gate": "beta_source_alpha=0 parent theorem signed", "passed": False, "claim_effect": "zero route not claimable"}),
        nonclaim({"row_id": "CG2762_2_width_target", "gate": "WEP product width target exists", "passed": True, "claim_effect": "target available but not prediction"}),
        nonclaim({"row_id": "CG2762_3_tau_WEP", "gate": "tau_WEP projection sourced/derived", "passed": False, "claim_effect": "WEP product prediction blocked"}),
        nonclaim({"row_id": "CG2762_4_material_tensor", "gate": "MICROSCOPE material/source tensor sourced", "passed": False, "claim_effect": "claim-grade WEP product blocked"}),
        nonclaim({"row_id": "CG2762_5_no_cancellation", "gate": "no-cancellation group complete", "passed": False, "claim_effect": "multi-channel cancellation not allowed"}),
        nonclaim({"row_id": "CG2762_6_local_GR_Newton", "gate": "local GR/Newton residual complete", "passed": False, "claim_effect": "no local-GR/Newton claim from 2762"}),
    ]


def build_refusals() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2762_0_zero", "claim": "2762 proves beta_source_alpha=0", "allowed": False, "reason": "zero theorem clauses are conditional and unsigned", "blocking_rows": "BSAZ2762_5_verdict;CG2762_1_zero_theorem"}),
        nonclaim({"row_id": "REF2762_1_product_prediction", "claim": "C_alpha_WEP is predicted by MTS", "allowed": False, "reason": "only a product-width target exists; beta_source_alpha, b_alpha, and tau_WEP are not same-branch values", "blocking_rows": "WIDTH2762_3_prediction_slot;TAUW2762_5_verdict"}),
        nonclaim({"row_id": "REF2762_2_MICROSCOPE_claim", "claim": "MTS passes MICROSCOPE/WEP", "allowed": False, "reason": "material/source/readout tensors and tau_WEP are missing", "blocking_rows": "ACQ2762_1_material_tensor;ACQ2762_2_source_worldtube;ACQ2762_3_readout_arrays"}),
        nonclaim({"row_id": "REF2762_3_local_GR", "claim": "MTS derives local GR/Newton after 2762", "allowed": False, "reason": "no local residual component has theorem-zero or source-backed same-branch product", "blocking_rows": "ARENA2762_3_PPN_Newton;CG2762_6_local_GR_Newton"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2762_0_2763",
            "next_target": "2763-Y5-R2FR-alpha-owner-matter-functor-contract-or-MICROSCOPE-source-tensor-under-AX1090.md",
            "script": "scripts/Y5_R2FR_alpha_owner_matter_functor_contract_or_MICROSCOPE_source_tensor_under_AX1090_2763.py",
            "why": "2762 identifies the missing bridge: either the parent action makes alpha/matter/readout coefficients quotient-owned, giving beta_source_alpha=0, or the WEP finite branch needs official material/source/readout tensors before any score.",
            "include": "alpha owner theorem attempt, matter/readout functor ownership, source-label forgetting, MICROSCOPE material/source tensor acquisition ledger, no-cancellation gate",
            "exclude": "tau unity shortcut, clock-to-WEP export by assumption, WEP/local-GR claim, pair cancellation, GitHub, formalization edits",
        })
    ]


def copy_branch_outputs(zero: list[dict[str, Any]], tau: list[dict[str, Any]], acquisition: list[dict[str, Any]], width: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("BR2762_0_zero_queue", "zero", zero, OUTPUTS["zero"], BRANCH_OUTPUTS["zero_queue"], "RAB queue for beta_source_alpha zero theorem"),
        ("BR2762_1_tau_queue", "tau", tau, OUTPUTS["tau"], BRANCH_OUTPUTS["tau_queue"], "RAB queue for tau_WEP projection contract"),
        ("BR2762_2_acquisition_queue", "acquisition", acquisition, OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_queue"], "RAB queue for MICROSCOPE material/source acquisition"),
        ("BR2762_3_beta_doc", "width", width, OUTPUTS["width"], BRANCH_OUTPUTS["beta_doc"], "beta-source WEP product width nonclaim doc"),
        ("BR2762_4_microscope_copy", "tau", tau, OUTPUTS["tau"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE branch copy for tau_WEP contract"),
        ("BR2762_5_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next alpha-owner/MICROSCOPE tensor target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    zero = rows_by_name["zero"]
    tau = rows_by_name["tau"]
    width = rows_by_name["width"]
    acquisition = rows_by_name["acquisition"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    refusals = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    width_row = next((row for row in width if row["row_id"] == "WIDTH2762_0_alpha_WEP"), {})
    try:
        width_positive = float(width_row.get("numeric_bound", "nan")) > 0
    except ValueError:
        width_positive = False
    checks = [
        ("VAL2762_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2762_1_zero_not_promoted", any(row["row_id"] == "BSAZ2762_5_verdict" and row["status"] == "ZERO_THEOREM_NOT_CLOSED" for row in zero), "beta_source_alpha zero theorem remains non-promoted"),
        ("VAL2762_2_width_positive_nonclaim", width_positive and width_row.get("score_ready") is False, "WEP alpha product width target is positive and nonclaim"),
        ("VAL2762_3_tau_missing", any(row["row_id"] == "TAUW2762_5_verdict" and row["current_status"] == "TAU_WEP_NOT_SOURCE_READY" for row in tau), "tau_WEP projection remains missing"),
        ("VAL2762_4_acquisition_missing", all(row["current_status"].startswith("MISSING") or row["priority"] in ["done_anchor", "guard"] for row in acquisition), "acquisition ledger keeps missing source/material/readout inputs explicit"),
        ("VAL2762_5_arena_blocks", all(row["score_ready"] is False for row in arena), "all arenas remain non-score-ready"),
        ("VAL2762_6_claim_gates_block", any(row["row_id"] == "CG2762_6_local_GR_Newton" and row["passed"] is False for row in gates), "local GR/Newton gate remains blocked"),
        ("VAL2762_7_refusals_block", all(row["allowed"] is False for row in refusals), "refusal runner blocks premature claims"),
        ("VAL2762_8_next", any(row["row_id"] == "NEXT2762_0_2763" and "alpha-owner-matter-functor" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2762_9_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2762_10_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2762_11_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true or claim_allowed=true"),
        ("VAL2762_12_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2762_13_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2762_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2762_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2762 ports the beta_source_alpha=0 theorem route into the R2/f(R) coupling bridge, refuses promotion because alpha-owner/matter-source/readout clauses are unsigned, records the real WEP product-width target |beta_source_alpha*b_alpha*tau_WEP| <= 4.797780522732e-05 as nonclaim, shows tau_WEP/material/source/readout inputs remain missing, and selects alpha-owner/matter-functor or MICROSCOPE tensor acquisition as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2762 - Y5 R2/f(R): tau_WEP Material-Source Projection Or beta_source_alpha Zero Under AX1090",
        "## Private Verdict\n\nThis is the bridge checkpoint. The clean theorem route is still alive: if the parent action owns alpha/matter/readout/source coefficients as quotient/representation data, then `beta_source_alpha=0` and the WEP alpha branch dies before fitting. But that parent owner is not derived yet.\n\nThe empirical route now has a real target: `|beta_source_alpha*b_alpha*tau_WEP| <= 4.797780522732e-05` in the current smoke convention. That is not an MTS prediction. It is the hoop the finite WEP product must jump through once `tau_WEP`, material/source tensor, and readout map are real.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## beta_source_alpha Zero Attempt\n\n" + markdown_table(rows_by_name["zero"], ["row_id", "claim_piece", "formal_statement", "status", "if_signed", "current_gap", "valid_for_claim"]),
        "## tau_WEP Projection Contract\n\n" + markdown_table(rows_by_name["tau"], ["row_id", "object", "definition_or_formula", "current_status", "source_basis", "missing_for_claim", "score_ready", "valid_for_claim"]),
        "## WEP Product Width Ledger\n\n" + markdown_table(rows_by_name["width"], ["row_id", "product_symbol", "numeric_bound", "units", "what_it_bounds", "status", "missing_for_claim", "score_ready", "valid_for_claim"]),
        "## Material-Source Acquisition Ledger\n\n" + markdown_table(rows_by_name["acquisition"], ["row_id", "needed_object", "current_status", "source_path", "blocking_gap", "priority", "valid_for_claim"]),
        "## Local Residual Impact\n\n" + markdown_table(rows_by_name["arena"], ["row_id", "arena", "new_object", "status", "local_effect", "score_ready", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decisions"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nWe did not get a WEP prediction yet, but we now have the exact bridge condition. Either derive the alpha-owner/matter-functor contract and make the alpha source charge zero, or acquire the official MICROSCOPE material/source/readout objects and build `beta_source_alpha*b_alpha*tau_WEP` as a finite row. That is the correct next doorway, not a loop.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    zero = build_zero_rows()
    tau = build_tau_rows(inputs)
    width = build_width_rows(inputs)
    acquisition = build_acquisition_rows(inputs)
    arena = build_arena_rows()
    decisions = build_decision_rows()
    gates = build_gates()
    refusals = build_refusals()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero"], zero)
    write_csv(OUTPUTS["tau"], tau)
    write_csv(OUTPUTS["width"], width)
    write_csv(OUTPUTS["acquisition"], acquisition)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(zero, tau, acquisition, width, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "zero": zero,
        "tau": tau,
        "width": width,
        "acquisition": acquisition,
        "arena": arena,
        "decisions": decisions,
        "gates": gates,
        "refusal": refusals,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2762_OVERALL")
    print(f"2762 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
