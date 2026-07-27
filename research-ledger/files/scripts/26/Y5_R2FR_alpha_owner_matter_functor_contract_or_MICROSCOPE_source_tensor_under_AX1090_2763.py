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
DOC = WORK / "2763-Y5-R2FR-alpha-owner-matter-functor-contract-or-MICROSCOPE-source-tensor-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2763_SOURCE_REGISTER.csv",
    "alpha": MTS / "P8_Y5_R2FR_2763_ALPHA_OWNER_CONTRACT_ATTEMPT.csv",
    "matter": MTS / "P8_Y5_R2FR_2763_MATTER_SOURCE_FUNCTOR_CONTRACT_ATTEMPT.csv",
    "microscope": MTS / "P8_Y5_R2FR_2763_MICROSCOPE_SOURCE_TENSOR_STATUS.csv",
    "bridge": MTS / "P8_Y5_R2FR_2763_BETA_SOURCE_BRIDGE_DECISION_LEDGER.csv",
    "arena": MTS / "P8_Y5_R2FR_2763_LOCAL_GR_IMPACT.csv",
    "gates": MTS / "P8_Y5_R2FR_2763_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2763_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2763_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2763_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2763_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "alpha_queue": RAB_QUEUE / "JR2763_ALPHA_OWNER_CONTRACT_ATTEMPT_NONCLAIM.csv",
    "matter_queue": RAB_QUEUE / "JR2763_MATTER_SOURCE_FUNCTOR_CONTRACT_NONCLAIM.csv",
    "microscope_queue": RAB_QUEUE / "JR2763_MICROSCOPE_SOURCE_TENSOR_STATUS_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "ALPHA_OWNER_MATTER_FUNCTOR_BRIDGE_2763_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "alpha_owner_matter_functor_or_microscope_tensor_2763_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2763_EM_OWNER_OR_MICROSCOPE_EXTRACTION_NEXT.csv",
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
        ("SRC2763_00_2762_doc", "2762_doc", WORK / "2762-Y5-R2FR-tau-WEP-material-source-projection-or-beta-source-alpha-zero-under-AX1090.md", ["NEXT2762_0_2763", "WIDTH2762_0_alpha_WEP", "ACQ2762_1_material_tensor"], "2762 handoff"),
        ("SRC2763_01_2762_validation", "2762_validation", MTS / "P8_Y5_BRR545_2762_VALIDATION.csv", ["VAL2762_OVERALL"], "2762 validation"),
        ("SRC2763_02_1055_doc", "1055_alpha_owner_doc", WORK / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md", ["PAC1055_1_EM_owner", "PAC1055_2_matter_functor", "DEC1055_2_best_next"], "parent action alpha/matter contract precedent"),
        ("SRC2763_03_1055_contract", "1055_contract_csv", MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", ["PAC1055_1_EM_owner", "PAC1055_6_single_parent_action"], "contract candidate rows"),
        ("SRC2763_04_1055_gates", "1055_claim_gates", MTS / "P8_Y5_R10_1055_CLAIM_GATES.csv", ["CG1055_1_alpha_owner", "CG1055_3_beta_source_alpha_zero"], "claim gates"),
        ("SRC2763_05_1054_zero", "1054_zero_clause_csv", MTS / "P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv", ["ZC1054_2_alpha_owner", "ZC1054_4_matter_readout_functor"], "zero clause audit"),
        ("SRC2763_06_1492_doc", "1492_acquisition_doc", WORK / "1492-Y5-R10-RAB-delta-w-source-acquisition-ledger-EotWash-R10-MICROSCOPE.md", ["EXT1492_4_MICROSCOPE_CMSM_PORTAL", "TGT1492_7_MICROSCOPE_tensor"], "MICROSCOPE tensor acquisition precedent"),
        ("SRC2763_07_1492_targets", "1492_targets_csv", MTS / "P8_Y5_R10_1492_LOCAL_TARGET_FILE_MANIFEST.csv", ["TGT1492_4_MICROSCOPE_readout", "TGT1492_7_MICROSCOPE_tensor"], "local target file manifest"),
        ("SRC2763_08_1492_blockers", "1492_blockers_csv", MTS / "P8_Y5_R10_1492_DELTA_W_SCORING_BLOCKERS.csv", ["BLK1492_2_MICROSCOPE"], "source acquisition blockers"),
        ("SRC2763_09_1491_anchors", "1491_delta_w_anchors", MTS / "P8_Y5_R10_1491_DELTA_W_BOUND_ANCHORS.csv", ["BAN1491_0_MICROSCOPE_TiPt"], "MICROSCOPE bound anchor"),
        ("SRC2763_10_1052_WEP", "1052_wep_projection", MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", ["AWP1052_0_alpha_Coulomb"], "WEP alpha product target"),
        ("SRC2763_11_local_bounds", "local_bounds", WORK / "source-intake" / "local_bounds" / "local_bound_claims.csv", ["R1_WEP_source_charge"], "local MICROSCOPE eta anchor"),
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
        "pac_alpha": find_row(read_csv_rows(MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"), "contract_id", "PAC1055_1_EM_owner"),
        "pac_matter": find_row(read_csv_rows(MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"), "contract_id", "PAC1055_2_matter_functor"),
        "pac_source": find_row(read_csv_rows(MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"), "contract_id", "PAC1055_4_source_label_forgetting"),
        "pac_readout": find_row(read_csv_rows(MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"), "contract_id", "PAC1055_5_radiative_readout_closure"),
        "target_tensor": find_row(read_csv_rows(MTS / "P8_Y5_R10_1492_LOCAL_TARGET_FILE_MANIFEST.csv"), "target_id", "TGT1492_7_MICROSCOPE_tensor"),
        "target_readout": find_row(read_csv_rows(MTS / "P8_Y5_R10_1492_LOCAL_TARGET_FILE_MANIFEST.csv"), "target_id", "TGT1492_4_MICROSCOPE_readout"),
        "target_source": find_row(read_csv_rows(MTS / "P8_Y5_R10_1492_LOCAL_TARGET_FILE_MANIFEST.csv"), "target_id", "TGT1492_5_MICROSCOPE_source"),
        "anchor": find_row(read_csv_rows(MTS / "P8_Y5_R10_1491_DELTA_W_BOUND_ANCHORS.csv"), "anchor_id", "BAN1491_0_MICROSCOPE_TiPt"),
        "wep_target": find_row(read_csv_rows(MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"), "projection_id", "AWP1052_0_alpha_Coulomb"),
    }


def build_alpha_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    alpha = inputs["pac_alpha"]
    return [
        nonclaim({"row_id": "AOC2763_0_target", "contract_piece": "alpha_EM owner", "formal_statement": "alpha_EM/g_EM is fixed by parent representation/topological/gauge-fibre data, not by hidden scalar Xhat.", "status": "TARGET_SHARP", "would_buy": "Lie_v alpha_EM=0, b_alpha=0, beta_source_alpha alpha-marker branch absent", "current_gap": "need vertical-generator norm/topological level/index/compact fibre metric derivation"}),
        nonclaim({"row_id": "AOC2763_1_imported_contract", "contract_piece": "1055 EM owner contract", "formal_statement": alpha.get("minimal_form", "S_EM=-1/(4g_*^2) int sqrt(-g_obs) F_Q^2 with Lie_v ell_EM=0"), "status": alpha.get("construction_status", "CLEAN_CONTRACT_NOT_PARENT_DERIVED"), "would_buy": alpha.get("would_buy", "Lie_v alpha_EM=0"), "current_gap": alpha.get("missing_for_derivation", "vertical-generator norm/topological-level inheritance for g_* and current normalization")}),
        nonclaim({"row_id": "AOC2763_2_rescaling_degeneracy", "contract_piece": "charge-current normalization", "formal_statement": "A_Q -> lambda A_Q and J_Q -> J_Q/lambda leave interaction form ambiguous unless the parent fixes both kinetic and current normalization.", "status": "OWNER_DEGENERACY_RETAINED", "would_buy": "separates physical alpha from units/gauge-field normalization", "current_gap": "parent current normalization not derived"}),
        nonclaim({"row_id": "AOC2763_3_hidden_scalar_counterexample", "contract_piece": "forbidden f_X F^2", "formal_statement": "If I_hid survives, S_EM can contain -f(I_hid)F_Q^2/4 without violating ordinary gauge/diffeomorphism symmetry.", "status": "COUNTEREXAMPLE_RETAINED", "would_buy": "not applicable", "current_gap": "operator-domain/hidden-visible Hom ban not derived"}),
        nonclaim({"row_id": "AOC2763_4_verdict", "contract_piece": "derive alpha owner now", "formal_statement": "The alpha-owner contract is exactly the right beam, but 2763 cannot derive it from current MTS primitives.", "status": "ALPHA_OWNER_NOT_DERIVED", "would_buy": "cleanest route to b_alpha=0 and beta_source_alpha=0", "current_gap": "move next to EM vertical-generator norm/topological-level derivation or keep finite WEP product"}),
    ]


def build_matter_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    matter = inputs["pac_matter"]
    source = inputs["pac_source"]
    readout = inputs["pac_readout"]
    return [
        nonclaim({"row_id": "MFC2763_0_matter_pullback", "contract_piece": "ordinary matter functor", "formal_statement": matter.get("minimal_form", "S_matter=sum_A S_A[Psi_A,e_obs(q),omega(q),A_Q,theta_A] with Lie_v theta_A=0"), "status": matter.get("construction_status", "EXACT_CONDITIONAL_MATTER_PULLBACK_NOT_PARENT_SIGNED"), "would_buy": "mass/material/readout hidden derivatives vanish", "current_gap": matter.get("missing_for_derivation", "parent matter bundle/category and fixed vertical lift")}),
        nonclaim({"row_id": "MFC2763_1_source_forgetting", "contract_piece": "species/source label forgetting", "formal_statement": source.get("minimal_form", "source functor Obj(C_matter)->T_total, not Obj(C_matter)->(T_A,A)"), "status": source.get("construction_status", "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED"), "would_buy": "relative source weights and WEP beta_source slots structurally unavailable", "current_gap": source.get("missing_for_derivation", "parent category must forget species labels before source coupling selection")}),
        nonclaim({"row_id": "MFC2763_2_readout_closure", "contract_piece": "radiative/readout closure", "formal_statement": readout.get("minimal_form", "S_vis^eff and clock/readout maps remain in Alg[q_loc,Theta_rep,Level_EM]"), "status": readout.get("construction_status", "REQUIRED_CLOSURE_AXIOM_NOT_DERIVED"), "would_buy": "tree-level zero survives EFT/readout reductions", "current_gap": readout.get("missing_for_derivation", "RG/readout theorem or explicit retained residual priors")}),
        nonclaim({"row_id": "MFC2763_3_counterexample", "contract_piece": "shadow matter/source counterexample", "formal_statement": "m_A(Xhat) psibar_A psi_A, A_A(Xhat)^2 g_obs, or kappa_A T_A remain legal if matter/source functor is unsigned.", "status": "COUNTEREXAMPLE_RETAINED", "would_buy": "not applicable", "current_gap": "no-shadow/source-label forgetting not parent-derived"}),
        nonclaim({"row_id": "MFC2763_4_verdict", "contract_piece": "promote matter/source functor now", "formal_statement": "Matter/source/readout clauses are exact conditional supports, not current derivations.", "status": "MATTER_SOURCE_FUNCTOR_NOT_DERIVED", "would_buy": "would remove composition/source beta slots", "current_gap": "derive matter category/vertical lift/source forgetful functor/readout closure"}),
    ]


def build_microscope_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    tensor = inputs["target_tensor"]
    readout = inputs["target_readout"]
    source = inputs["target_source"]
    anchor = inputs["anchor"]
    wep = inputs["wep_target"]
    return [
        nonclaim({"row_id": "MIC2763_0_bound_anchor", "needed_object": "MICROSCOPE eta bound anchor", "local_target_path": anchor.get("source_path", "source-intake/local_bounds/local_bound_claims.csv"), "current_status": anchor.get("bound_status", "SOURCE_BACKED_BOUND_ANCHOR_AVAILABLE"), "source_url_or_doi": anchor.get("source_url_or_doi", "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102"), "claim_role": "bound anchor only"}),
        nonclaim({"row_id": "MIC2763_1_material_tensor", "needed_object": "official Ti/Pt/PtRh/TA6V material tensor", "local_target_path": tensor.get("target_path", "source-intake/microscope/derived/P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"), "current_status": tensor.get("target_status", "TARGET_FILE_MISSING_OR_UNPROMOTED"), "source_url_or_doi": "CMSM portal plus PRL/CQG papers", "claim_role": "required before product prediction"}),
        nonclaim({"row_id": "MIC2763_2_readout_kernel", "needed_object": "CMSM/readout/product matrix", "local_target_path": readout.get("target_path", "source-intake/microscope/official_readout/P_WEP_K_CMSM_readout.csv"), "current_status": readout.get("target_status", "TARGET_FILE_MISSING_OR_UNPROMOTED"), "source_url_or_doi": "https://cmsm-ds.onera.fr/user/microscope", "claim_role": "defines tau_WEP/readout convention"}),
        nonclaim({"row_id": "MIC2763_3_source_worldtube", "needed_object": "Earth/source worldtube kernel", "local_target_path": source.get("target_path", "source-intake/microscope/source_worldtube/P_WEP_R_source_Earth_worldtube.csv"), "current_status": source.get("target_status", "TARGET_FILE_MISSING_OR_UNPROMOTED"), "source_url_or_doi": "CMSM portal and orbit/readout papers", "claim_role": "source normalization for tau_WEP"}),
        nonclaim({"row_id": "MIC2763_4_product_target", "needed_object": "alpha WEP product target", "local_target_path": str(MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"), "current_status": "TARGET_WIDTH_AVAILABLE_NONCLAIM", "source_url_or_doi": "AWP1052_0_alpha_Coulomb", "claim_role": f"requires MTS product <= {wep.get('required_abs_beta_source_max', '4.797780522732e-05')}"}),
        nonclaim({"row_id": "MIC2763_5_verdict", "needed_object": "claim-grade MICROSCOPE tensor bridge", "local_target_path": "multiple target files", "current_status": "MICROSCOPE_TENSOR_NOT_ACQUIRED", "source_url_or_doi": "1492 source ledger", "claim_role": "empirical fallback remains acquisition task"}),
    ]


def build_bridge_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "BRIDGE2763_0_theory_route", "route": "derive alpha owner/matter functor", "status": "BEST_CLEAN_ROUTE_NOT_CLOSED", "if_success": "b_alpha=0/beta_source_alpha=0 for alpha-marker WEP/R10 branch", "next_action": "derive EM owner from vertical-generator norm/topological level"}),
        nonclaim({"row_id": "BRIDGE2763_1_empirical_route", "route": "MICROSCOPE source tensor acquisition", "status": "BEST_EMPIRICAL_FALLBACK_NOT_FILLED", "if_success": "build finite C_alpha_WEP prediction row with material/source/readout convention", "next_action": "download/extract/parse official MICROSCOPE tensor/readout/source files"}),
        nonclaim({"row_id": "BRIDGE2763_2_no_mix", "route": "no mixed theorem/data shortcut", "status": "ACTIVE_GUARD", "if_success": "prevents clock product or smoke tensors from masquerading as WEP pass", "next_action": "keep theorem-zero and finite product branches separated"}),
        nonclaim({"row_id": "BRIDGE2763_3_verdict", "route": "2763 selection", "status": "DUAL_NEXT_ROUTE_REQUIRED", "if_success": "either EM owner closes or MICROSCOPE finite branch becomes score-ready later", "next_action": "2764 should attack EM owner derivation while preparing MICROSCOPE extraction targets"}),
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "ARENA2763_0_WEP", "arena": "WEP/MICROSCOPE", "effect_if_alpha_owner_signed": "alpha-marker WEP branch theorem-zero", "current_status": "BLOCKED_OR_FINITE_TARGET_ONLY", "missing": "alpha owner or official MICROSCOPE tensor/product map", "score_ready": False}),
        nonclaim({"row_id": "ARENA2763_1_clock", "arena": "clocks", "effect_if_alpha_owner_signed": "b_alpha clock drift branch zero under same owner", "current_status": "CLOCK_PRODUCT_RETAINED_NONCLAIM", "missing": "alpha owner or tau_clock parent map", "score_ready": False}),
        nonclaim({"row_id": "ARENA2763_2_R10", "arena": "R10", "effect_if_alpha_owner_signed": "alpha-marker source/test branch zero; non-alpha tails retained", "current_status": "R10_STILL_BLOCKED", "missing": "EM owner or K_X/Z_X/lambda/tau_R10/curve", "score_ready": False}),
        nonclaim({"row_id": "ARENA2763_3_local_GR", "arena": "local GR/Newton", "effect_if_alpha_owner_signed": "one coupling leak removed from local residual vector", "current_status": "LOCAL_GR_NOT_CLAIMED", "missing": "remaining q_loc/boundary/beta/source/current/curvature residuals", "score_ready": False}),
    ]


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2763_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2763_1_alpha_owner", "gate": "alpha_EM owner derived from parent primitives", "passed": False, "claim_effect": "b_alpha/beta_source_alpha zero not promoted"}),
        nonclaim({"row_id": "CG2763_2_matter_functor", "gate": "matter/source/readout functor derived", "passed": False, "claim_effect": "composition/source beta slots remain possible"}),
        nonclaim({"row_id": "CG2763_3_MICROSCOPE_tensor", "gate": "official MICROSCOPE material/source/readout tensor acquired", "passed": False, "claim_effect": "finite WEP product prediction blocked"}),
        nonclaim({"row_id": "CG2763_4_product_prediction", "gate": "C_alpha_WEP^MTS numeric prediction exists", "passed": False, "claim_effect": "WEP product target cannot be scored"}),
        nonclaim({"row_id": "CG2763_5_local_GR_Newton", "gate": "local GR/Newton residual complete", "passed": False, "claim_effect": "no local-GR/Newton claim from 2763"}),
    ]


def build_refusals() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2763_0_alpha_owner", "claim": "2763 derives alpha_EM owner", "allowed": False, "reason": "contract is constructible but vertical-generator/topological normalization is not derived", "blocking_rows": "AOC2763_4_verdict;CG2763_1_alpha_owner"}),
        nonclaim({"row_id": "REF2763_1_beta_zero", "claim": "beta_source_alpha=0 follows as a current theorem", "allowed": False, "reason": "alpha owner, matter functor, source forgetting, and readout closure are unsigned", "blocking_rows": "MFC2763_4_verdict;CG2763_2_matter_functor"}),
        nonclaim({"row_id": "REF2763_2_MICROSCOPE", "claim": "MICROSCOPE tensor branch is score-ready", "allowed": False, "reason": "official tensor/readout/source target files are missing or unpromoted", "blocking_rows": "MIC2763_1_material_tensor;MIC2763_2_readout_kernel;MIC2763_3_source_worldtube"}),
        nonclaim({"row_id": "REF2763_3_local_GR", "claim": "MTS derives local GR/Newton after 2763", "allowed": False, "reason": "2763 only narrows one coupling route and does not complete the local residual vector", "blocking_rows": "ARENA2763_3_local_GR;CG2763_5_local_GR_Newton"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2763_0_2764",
            "next_target": "2764-Y5-R2FR-EM-vertical-generator-norm-or-MICROSCOPE-extraction-preflight-under-AX1090.md",
            "script": "scripts/Y5_R2FR_EM_vertical_generator_norm_or_MICROSCOPE_extraction_preflight_under_AX1090_2764.py",
            "why": "2763 cannot promote the whole parent-action contract. The sharpest derivation route is now the EM alpha owner itself: derive g_EM from vertical-generator norm/topological level/index/compact fibre metric. In parallel, keep MICROSCOPE extraction preflight ready as empirical fallback.",
            "include": "EM gauge kinetic owner, charge-current normalization, generator rescaling degeneracy, topological/index/fibre metric routes, MICROSCOPE target-file preflight",
            "exclude": "declaring alpha fixed by taste, unit-rescaling, tau unity shortcut, WEP/local-GR claim, GitHub, formalization edits",
        })
    ]


def copy_branch_outputs(alpha: list[dict[str, Any]], matter: list[dict[str, Any]], microscope: list[dict[str, Any]], bridge: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("BR2763_0_alpha_queue", "alpha", alpha, OUTPUTS["alpha"], BRANCH_OUTPUTS["alpha_queue"], "RAB queue for alpha owner contract attempt"),
        ("BR2763_1_matter_queue", "matter", matter, OUTPUTS["matter"], BRANCH_OUTPUTS["matter_queue"], "RAB queue for matter/source functor contract"),
        ("BR2763_2_microscope_queue", "microscope", microscope, OUTPUTS["microscope"], BRANCH_OUTPUTS["microscope_queue"], "RAB queue for MICROSCOPE source tensor status"),
        ("BR2763_3_beta_doc", "bridge", bridge, OUTPUTS["bridge"], BRANCH_OUTPUTS["beta_doc"], "beta/source bridge decision copy"),
        ("BR2763_4_microscope_copy", "microscope", microscope, OUTPUTS["microscope"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE branch copy"),
        ("BR2763_5_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next EM owner/MICROSCOPE extraction target"),
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
            if str(row.get("allowed", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    alpha = rows_by_name["alpha"]
    matter = rows_by_name["matter"]
    microscope = rows_by_name["microscope"]
    bridge = rows_by_name["bridge"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    refusals = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2763_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2763_1_alpha_not_derived", any(row["row_id"] == "AOC2763_4_verdict" and row["status"] == "ALPHA_OWNER_NOT_DERIVED" for row in alpha), "alpha owner remains non-promoted"),
        ("VAL2763_2_matter_not_derived", any(row["row_id"] == "MFC2763_4_verdict" and row["status"] == "MATTER_SOURCE_FUNCTOR_NOT_DERIVED" for row in matter), "matter/source functor remains non-promoted"),
        ("VAL2763_3_MICROSCOPE_missing", any(row["row_id"] == "MIC2763_5_verdict" and row["current_status"] == "MICROSCOPE_TENSOR_NOT_ACQUIRED" for row in microscope), "MICROSCOPE tensor bridge remains acquisition task"),
        ("VAL2763_4_bridge_dual_route", any(row["row_id"] == "BRIDGE2763_3_verdict" and row["status"] == "DUAL_NEXT_ROUTE_REQUIRED" for row in bridge), "dual next route selected"),
        ("VAL2763_5_arena_blocks", all(row["score_ready"] is False for row in arena), "all arenas remain non-score-ready"),
        ("VAL2763_6_claim_gates_block", any(row["row_id"] == "CG2763_5_local_GR_Newton" and row["passed"] is False for row in gates), "local GR/Newton gate remains blocked"),
        ("VAL2763_7_refusals_block", all(row["allowed"] is False for row in refusals), "refusal runner blocks premature claims"),
        ("VAL2763_8_next", any(row["row_id"] == "NEXT2763_0_2764" and "EM-vertical-generator-norm" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2763_9_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2763_10_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2763_11_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true"),
        ("VAL2763_12_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2763_13_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2763_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2763_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2763 imports the alpha-owner/matter-functor parent-action contract into the R2/f(R) coupling bridge, refuses promotion because EM kinetic ownership, matter/source functor, source-label forgetting, and readout closure remain unsigned, records MICROSCOPE tensor/readout/source files as still missing or unpromoted, and selects EM vertical-generator norm/topological-level derivation plus MICROSCOPE extraction preflight as the next route.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2763 - Y5 R2/f(R): Alpha Owner Matter Functor Contract Or MICROSCOPE Source Tensor Under AX1090",
        "## Private Verdict\n\nThis checkpoint joins the two live roads. The theory road is clean: if the parent action owns `alpha_EM`, matter constants, source labels, and readout as quotient/representation data, then the alpha WEP coupling route is theorem-zero. The problem is still ownership: the contract exists, but `g_EM`/`alpha_EM` has not yet been derived from a parent vertical-generator norm, topological level, index, or compact fibre metric.\n\nThe empirical road is also clear but not filled: MICROSCOPE has a real eta anchor, but the official material tensor, readout/product matrix, and Earth/source worldtube kernel are still missing/unpromoted. So 2763 narrows the next attack: derive the EM owner directly, or perform the MICROSCOPE extraction preflight.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Alpha Owner Contract Attempt\n\n" + markdown_table(rows_by_name["alpha"], ["row_id", "contract_piece", "formal_statement", "status", "would_buy", "current_gap", "valid_for_claim"]),
        "## Matter Source Functor Contract Attempt\n\n" + markdown_table(rows_by_name["matter"], ["row_id", "contract_piece", "formal_statement", "status", "would_buy", "current_gap", "valid_for_claim"]),
        "## MICROSCOPE Source Tensor Status\n\n" + markdown_table(rows_by_name["microscope"], ["row_id", "needed_object", "local_target_path", "current_status", "source_url_or_doi", "claim_role", "valid_for_claim"]),
        "## Beta Source Bridge Decision Ledger\n\n" + markdown_table(rows_by_name["bridge"], ["row_id", "route", "status", "if_success", "next_action", "valid_for_claim"]),
        "## Local GR Impact\n\n" + markdown_table(rows_by_name["arena"], ["row_id", "arena", "effect_if_alpha_owner_signed", "current_status", "missing", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThe coupling wall has not moved sideways; it has sharpened. The highest-value derivation target is now not a vague coupling idea but a specific owner: `g_EM`. If `g_EM` is parent-fixed, the alpha leak can die cleanly. If not, the honest empirical fallback is official MICROSCOPE tensor extraction, not pretending the existing eta bound is already a theory prediction.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    alpha = build_alpha_rows(inputs)
    matter = build_matter_rows(inputs)
    microscope = build_microscope_rows(inputs)
    bridge = build_bridge_rows()
    arena = build_arena_rows()
    gates = build_gates()
    refusals = build_refusals()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["alpha"], alpha)
    write_csv(OUTPUTS["matter"], matter)
    write_csv(OUTPUTS["microscope"], microscope)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(alpha, matter, microscope, bridge, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "alpha": alpha,
        "matter": matter,
        "microscope": microscope,
        "bridge": bridge,
        "arena": arena,
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

    overall = next(row for row in validation if row["validation_id"] == "VAL2763_OVERALL")
    print(f"2763 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
