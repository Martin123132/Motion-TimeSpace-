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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_COEFF = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2990"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2990-Y5-R2FR-sector-normal-form-branch-selection-or-first-epsilon-theta-numeric-source-row-under-AX1090.md"

SRC_2989_DOC = ROOT / "2989-Y5-R2FR-parent-Lagrangian-Theta-sector-extraction-or-first-epsilon-theta-piece-bound-under-AX1090.md"
SRC_2989_NEXT = RESIDUALS / "P8_Y5_R2FR_2989_NEXT_TARGET.csv"
SRC_2989_SECTOR = RESIDUALS / "P8_Y5_R2FR_2989_PARENT_LAGRANGIAN_THETA_SECTOR_AUDIT.csv"
SRC_2989_THETA = RESIDUALS / "P8_Y5_R2FR_2989_THETA_EXTRACTION_ATTEMPT.csv"
SRC_2989_EPS = RESIDUALS / "P8_Y5_R2FR_2989_EPSILON_THETA_PIECE_BOUND_ROWS_NONCLAIM.csv"
SRC_2989_GATES = RESIDUALS / "P8_Y5_R2FR_2989_PROMOTION_GATES.csv"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_1760_DOC = ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"
SRC_MIN_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_RESPONSE_DOUBLET = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_PIM_CONTRACT = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"
SRC_2947_SECTOR = PARENT_ACTION / "Theta_Qtau_sector_charge_matrix_2947_NONCLAIM.csv"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2990_SOURCE_REGISTER.csv",
    "branch_menu": RESIDUALS / "P8_Y5_R2FR_2990_SECTOR_NORMAL_FORM_BRANCH_MENU.csv",
    "normal_form": RESIDUALS / "P8_Y5_R2FR_2990_SELECTED_PARENT_NORMAL_FORM_CONTRACT.csv",
    "sector_contract": RESIDUALS / "P8_Y5_R2FR_2990_SECTOR_BY_SECTOR_THETA_NORMAL_FORM_CONTRACT.csv",
    "epsilon_acquisition": RESIDUALS / "P8_Y5_R2FR_2990_FIRST_EPSILON_THETA_SOURCE_ROW_ACQUISITION_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2990_NORMAL_FORM_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2990_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2990_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2990_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2990_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "normal_form_copy": PARENT_ACTION / "sector_normal_form_branch_selection_2990_NOT_SIGNED.csv",
    "epsilon_acquisition_copy": LOCAL_BOUNDS / "epsilon_theta_first_source_row_acquisition_2990_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2990_boundary_theta_zero_or_epsilon_Bv_next_NONCLAIM.csv",
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


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2990_00_2989_doc", SRC_2989_DOC, ["NEXT2989_0_2990", "sector normal form"], "2989 narrative handoff"),
        ("SRC2990_01_2989_next", SRC_2989_NEXT, ["NEXT2989_0_2990", "parent sector normal form"], "selected 2990 target"),
        ("SRC2990_02_2989_sector", SRC_2989_SECTOR, ["TLS2989_8_total", "TOTAL_THETA_NOT_PARENT_SIGNED"], "Theta sector audit"),
        ("SRC2990_03_2989_theta", SRC_2989_THETA, ["THX2989_5_verdict", "THETA_PARENT_NOT_DERIVED_STAGE_EPSILON_THETA_PIECE"], "Theta extraction verdict"),
        ("SRC2990_04_2989_eps", SRC_2989_EPS, ["ETH2989_09_total", "epsilon_theta_piece_total_abs"], "epsilon theta rows"),
        ("SRC2990_05_2989_gates", SRC_2989_GATES, ["GATE2989_8_promote", "all previous gates must pass"], "2989 promotion gates"),
        ("SRC2990_06_1009_doc", SRC_1009_DOC, ["PCS1009_3_boundary_reference", "PCS1009_4_Gamma_Khat_extra"], "parent current-chain sector contract"),
        ("SRC2990_07_1760_doc", SRC_1760_DOC, ["MWD1760_1_conditional_theorem", "A_matter"], "matter/worldtube descent contract"),
        ("SRC2990_08_min_blocks", SRC_MIN_BLOCKS, ["A511_3_extra_field_silence", "A511_5_boundary_reference"], "minimum parent local-GR blocks"),
        ("SRC2990_09_response_doublet", SRC_RESPONSE_DOUBLET, ["RD516_4_zero_odd_source", "not_derived_hard_block"], "response doublet contract"),
        ("SRC2990_10_pim_contract", SRC_PIM_CONTRACT, ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"], "Pi_M projector contract"),
        ("SRC2990_11_noether_chain", SRC_NOETHER_CHAIN, ["D505_0_local_parent_action_form", "D505_4_zero_premises"], "parent Noether closure chain"),
        ("SRC2990_12_2947_sector", SRC_2947_SECTOR, ["SEC2947_9_total", "TOTAL_CERTIFICATE_FAILS"], "sector charge certificate failure"),
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


def branch_menu_rows() -> list[dict[str, Any]]:
    data = [
        (
            "BNF2990_0_EH_only",
            "EH-only parent action",
            "L_parent=L_EH[g_obs]",
            "REJECTED_AS_TOTAL_MTS_PARENT",
            "fails because boundary, extra, projector/source, matter/worldtube and constraint sectors remain legal and unsigned",
            False,
            "epsilon_EH_reference_guard",
        ),
        (
            "BNF2990_1_fixed_boundary",
            "EH plus fixed exact/topological boundary",
            "L_boundary=dB_ref with B_ref fixed before readout and no fitted subtraction",
            "CONDITIONAL_LOW_SCRUTINY_BRANCH",
            "plausible first theorem-zero target, but fixed-reference convention and no-flux proof are not signed",
            True,
            "epsilon_Bv_ambiguity",
        ),
        (
            "BNF2990_2_silent_extra",
            "quadratic silent extra sector",
            "L_silent[Z]=1/2 <DZ,M DZ>-V(Z), Z=0, dV(0)=0, positive Hessian, no linear readout/source vertex",
            "SELECTED_CONDITIONAL_CORE_NOT_SIGNED",
            "best conservative route for local GR because residuals start at second order if the double-zero and no-source clauses are proved",
            True,
            "epsilon_Qv_extra_piece",
        ),
        (
            "BNF2990_3_response_doublet",
            "even response doublet",
            "Gamma_eff and K_hat arise from exchange-even response variables with zero odd source",
            "CONDITIONAL_EXTENSION_NOT_SIGNED",
            "current response contract says zero odd source is not derived and component map is partial",
            True,
            "epsilon_Qv_extra_piece",
        ),
        (
            "BNF2990_4_projector_constraint",
            "projector/source-measure as parent constraint sector",
            "Pi_M and source-measure variables owned by Ward/Euler/topological constraints, including delta Pi_M",
            "CONDITIONAL_EXTENSION_NOT_SIGNED",
            "projector algebra alone is insufficient; variation owner and flux closure remain open",
            True,
            "epsilon_Qv_projector_piece",
        ),
        (
            "BNF2990_5_q_only_matter",
            "ordinary matter as quotient pullback",
            "S_matter[psi,e_obs(q(Phi))] with fixed representation data and worldtube support descending through Hilbert current",
            "CONDITIONAL_EXTENSION_NOT_SIGNED",
            "chain-rule theorem is clean, but no direct source/worldtube slot remains a live obstruction",
            True,
            "epsilon_Qv_matter_source_piece",
        ),
        (
            "BNF2990_6_residual_bound_fallback",
            "explicit residual-bound parent sector",
            "all unsigned legal pieces remain as epsilon_theta components until theorem-zero or numeric bounds exist",
            "REQUIRED_FALLBACK",
            "prevents closure language from hiding missing sector terms",
            True,
            "epsilon_theta_piece_total_abs",
        ),
        (
            "BNF2990_7_selected_route",
            "least-scrutiny conservative normal form",
            "EH + fixed exact boundary + topological constants + silent quadratic extra + q-only matter + parent-owned projector/constraints + explicit residual fallback",
            "SELECTED_AS_CONDITIONAL_NOT_CLAIM",
            "this is the narrowest route that could reduce to GR without declaring non-EH sectors nonexistent",
            True,
            "epsilon_theta_piece_total_abs",
        ),
    ]
    return [
        add(
            {
                "branch_id_local": branch_id,
                "branch_name": branch_name,
                "normal_form": normal_form,
                "selection_status": status,
                "reason": reason,
                "kept_for_next_stage": kept,
                "fallback_symbol": fallback,
                "promoted_now": False,
            }
        )
        for branch_id, branch_name, normal_form, status, reason, kept, fallback in data
    ]


def normal_form_rows() -> list[dict[str, Any]]:
    data = [
        (
            "NF2990_0_formula",
            "local parent action normal form",
            "L_parent|local = L_EH[g_obs;kappa0,Lambda0] + dB_ref + L_top[kappa,A3] + L_silent[Z] + L_selector/PiM/lambda + L_matter[psi,e_obs(q(Phi))] + L_residual_explicit",
            "selected as working contract only",
            "SELECTED_CONDITIONAL_NOT_SIGNED",
            "needs source path or derivation for every non-EH block",
        ),
        (
            "NF2990_1_EH_limit",
            "GR comparator limit",
            "kappa0 constant, Lambda locally subtracted/background, g_readout=g_obs+O(Z^2)",
            "Theta_EH may seed the comparator, not total MTS",
            "REFERENCE_LIMIT_ONLY",
            "non-EH silence/exactness not signed",
        ),
        (
            "NF2990_2_boundary",
            "fixed boundary/reference",
            "B_ref is chosen before readout and delta_v B_ref=0 or exact/topological on compact local surfaces",
            "would remove epsilon_Bv_ambiguity if proved",
            "FIRST_PROOF_TARGET_NOT_SIGNED",
            "fixed-reference/no-flux theorem missing",
        ),
        (
            "NF2990_3_extra_double_zero",
            "silent extra/double-zero",
            "Z=0, dL_silent|0=0, Hessian positive, no linear stress/readout/source vertex",
            "would push extra-sector leakage to quadratic/bounded order",
            "CONDITIONAL_NOT_SIGNED",
            "zero odd source and metric response not derived",
        ),
        (
            "NF2990_4_projector_owner",
            "projector/source-measure owner",
            "delta(Pi_M J)=Pi_M delta J + (delta Pi_M)J is owned by Ward/Euler/topological sector or retained",
            "prevents projector algebra from erasing source flux",
            "CONDITIONAL_NOT_SIGNED",
            "delta Pi_M and flux closure missing",
        ),
        (
            "NF2990_5_matter_qpullback",
            "q-only matter/worldtube",
            "S_matter descends through e_obs(q(Phi)); no V_m[X,rho_A,W_source] slot; worldtube support descends",
            "chain rule would kill vertical matter source",
            "CONDITIONAL_NOT_SIGNED",
            "hidden source prefactors/support terms remain legal",
        ),
        (
            "NF2990_6_constraint_split",
            "C_v constraint split",
            "C_v=C_EH+C_extra+C_projector+C_matter+C_boundary is constraint-proportional or source-bounded",
            "needed before local current residual vanishes",
            "CONDITIONAL_NOT_SIGNED",
            "common constraint split missing",
        ),
        (
            "NF2990_7_Mref",
            "same-frame denominator",
            "M_ref=H_tau-H_ref or equivalent positive local charge denominator on linked compact surfaces",
            "needed to score epsilon_theta rows",
            "CONDITIONAL_NOT_SIGNED",
            "positive same-frame denominator absent",
        ),
        (
            "NF2990_8_verdict",
            "selected normal form verdict",
            "Use this normal form only as a private derivation scaffold; all unsigned terms stay in epsilon rows.",
            "no local-GR/Newton/PPN claim",
            "NORMAL_FORM_SELECTED_BUT_NOT_PARENT_SIGNED",
            "start with boundary proof or epsilon_Bv source row",
        ),
    ]
    return [
        add(
            {
                "normal_form_id": normal_form_id,
                "clause": clause,
                "mathematical_statement": statement,
                "theta_effect": theta_effect,
                "current_status": status,
                "blocking_gap": gap,
                "selected_working_contract": True,
                "promoted_now": False,
            }
        )
        for normal_form_id, clause, statement, theta_effect, status, gap in data
    ]


def sector_contract_rows() -> list[dict[str, Any]]:
    data = [
        ("SNF2990_0_EH", "EH/local geometry", "retain EH as reference comparator", "Theta_EH allowed only after same metric/coupling/readout locks", "REFERENCE_ONLY", "epsilon_EH_reference_guard", "prove non-EH silence/exactness"),
        ("SNF2990_1_boundary", "boundary/reference", "fixed exact/topological B_ref before readout", "Theta_boundary contribution zero/exact if fixed-reference proof passes", "FIRST_TARGET_UNSIGNED", "epsilon_Bv_ambiguity", "prove delta_v B_ref=0 or source-bound it"),
        ("SNF2990_2_extra", "extra motion/time/domain/memory", "quadratic silent sector plus even response doublet", "Theta_extra vanishes linearly only if double-zero and zero-source clauses pass", "UNSIGNED", "epsilon_Qv_extra_piece", "derive stationary positive operator and no odd source"),
        ("SNF2990_3_projector", "projector/source-measure", "parent-owned constraint/topological projector sector", "Theta_projector includes delta Pi_M or the row remains retained", "UNSIGNED", "epsilon_Qv_projector_piece", "own delta Pi_M and Ward/Euler flux closure"),
        ("SNF2990_4_matter", "matter/source/worldtube", "q-only pullback matter functor", "Theta_matter/source is vertical-silent only by signed descent", "UNSIGNED", "epsilon_Qv_matter_source_piece", "exclude direct source/worldtube slots"),
        ("SNF2990_5_constraint", "constraint / C_v", "shared constraint split across all sectors", "C_v removed only if parent constraint-proportional", "UNSIGNED", "epsilon_Cv_constraint_missing", "write common EOM/Ward split"),
        ("SNF2990_6_Mref", "normalization/surface", "positive same-frame M_ref on linked compact surfaces", "all theta rows unscored until M_ref exists", "UNSIGNED", "epsilon_Mref_normalization", "prove positivity and surface class"),
        ("SNF2990_7_total", "total", "sum of selected conditional sectors plus explicit residual fallback", "Theta_parent remains nonclaim until every row above passes", "TOTAL_NOT_PROMOTED", "epsilon_theta_piece_total_abs", "do not promote Omega/local GR"),
    ]
    return [
        add(
            {
                "sector_contract_id": contract_id,
                "sector": sector,
                "normal_form_clause": clause,
                "theta_implication": implication,
                "current_status": status,
                "fallback_symbol": fallback,
                "next_certificate_needed": needed,
                "sector_promoted": False,
            }
        )
        for contract_id, sector, clause, implication, status, fallback, needed in data
    ]


def epsilon_acquisition_rows() -> list[dict[str, Any]]:
    data = [
        (
            "ACQ2990_0_first_target_boundary",
            "1",
            "epsilon_Bv_ambiguity",
            "boundary/reference theta leakage",
            "prove fixed exact/topological B_ref gives delta_v B_ref=0 on compact local collars; otherwise source-bound abs(int_S delta B_v)/M_ref",
            "THEOREM_ZERO_PREFERRED_NUMERIC_BOUND_FALLBACK",
            "MISSING_FIXED_REFERENCE_NO_FLUX_PROOF",
        ),
        (
            "ACQ2990_1_extra",
            "2",
            "epsilon_Qv_extra_piece",
            "extra-sector theta/current leakage",
            "derive quadratic silent/double-zero law and zero odd source; otherwise source-bound extra surface current",
            "DERIVATION_FIRST",
            "MISSING_DOUBLE_ZERO_AND_ZERO_ODD_SOURCE",
        ),
        (
            "ACQ2990_2_matter",
            "3",
            "epsilon_Qv_matter_source_piece",
            "matter/source/worldtube theta leakage",
            "parent-sign q-only matter functor and worldtube support descent; otherwise bound A_matter contribution",
            "DERIVATION_FIRST",
            "MISSING_NO_DIRECT_SOURCE_SLOT",
        ),
        (
            "ACQ2990_3_projector",
            "4",
            "epsilon_Qv_projector_piece",
            "projector/source-measure theta leakage",
            "own delta Pi_M and Ward/Euler closure; otherwise source-bound projector flux",
            "DERIVATION_FIRST",
            "MISSING_PROJECTOR_VARIATION_OWNER",
        ),
        (
            "ACQ2990_4_constraint",
            "5",
            "epsilon_Cv_constraint_missing",
            "unbounded nonconstraint current leakage",
            "write common constraint split or source-bound nonconstraint term",
            "DERIVATION_FIRST",
            "MISSING_COMMON_CONSTRAINT_SPLIT",
        ),
        (
            "ACQ2990_5_Mref",
            "6",
            "epsilon_Mref_normalization",
            "denominator/surface normalization",
            "prove M_ref positive in same frame or the epsilon rows cannot score",
            "SUPPORTING_GATE",
            "MISSING_POSITIVE_SAME_FRAME_MREF",
        ),
    ]
    return [
        add(
            {
                "acquisition_id": acquisition_id,
                "priority_rank": rank,
                "symbol": symbol,
                "component": component,
                "required_source_or_proof": required,
                "preferred_route": route,
                "current_status": status,
                "numeric_value": "MISSING_NUMERIC_OR_THEOREM_ZERO_SOURCE",
                "numeric_units": "dimensionless_after_M_ref_or_guard",
                "source_path": "MISSING_SOURCE_PATH",
                "valid_numeric_bound": False,
                "valid_for_claim": False,
            }
        )
        for acquisition_id, rank, symbol, component, required, route, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2990_0_branch_selected", "least-scrutiny branch selected as private working contract", True, "SELECTED_CONDITIONAL"),
        ("GATE2990_1_not_promoted", "selected branch is not promoted as parent action", False, "NOT_PARENT_SIGNED"),
        ("GATE2990_2_boundary", "fixed B_ref/no-flux proof closes epsilon_Bv", False, "MISSING_FIXED_REFERENCE_NO_FLUX_PROOF"),
        ("GATE2990_3_extra", "extra double-zero and zero odd source close epsilon_Qv_extra", False, "MISSING_DOUBLE_ZERO_AND_ZERO_ODD_SOURCE"),
        ("GATE2990_4_projector", "projector variation owner closes epsilon_Qv_projector", False, "MISSING_PROJECTOR_VARIATION_OWNER"),
        ("GATE2990_5_matter", "q-only matter/worldtube descent closes epsilon_Qv_matter", False, "MISSING_NO_DIRECT_SOURCE_SLOT"),
        ("GATE2990_6_constraint", "common C_v constraint split closes epsilon_Cv", False, "MISSING_COMMON_CONSTRAINT_SPLIT"),
        ("GATE2990_7_Mref", "positive same-frame M_ref closes scoring denominator", False, "MISSING_POSITIVE_SAME_FRAME_MREF"),
        ("GATE2990_8_promote", "promote parent normal form to Theta/Omega/local-GR branch", False, "all closure gates must pass first"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, passed, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2990_0_selected_branch",
                "decision": "Select the conservative sector normal form as the least-scrutiny private scaffold.",
                "because": "it keeps EH as the GR comparator while forcing every non-EH sector either to be exact/silent/constraint-owned/q-only or to remain an explicit residual.",
                "next_action": "do not call it a parent action theorem until the sector certificates exist.",
            }
        ),
        add(
            {
                "decision_id": "DEC2990_1_no_numeric_row",
                "decision": "Do not create a numeric epsilon_theta row yet.",
                "because": "no source-backed numeric/theorem-zero input exists for boundary, extra, projector, matter, constraint or M_ref rows.",
                "next_action": "create source-ready acquisition rows and attack the boundary theorem-zero first.",
            }
        ),
        add(
            {
                "decision_id": "DEC2990_2_next",
                "decision": "Next target should try the fixed-boundary/reference theta-zero proof before a harder coupling jump.",
                "because": "epsilon_Bv is the lowest-scrutiny closure: if B_ref is fixed before readout and exact/topological, the vertical boundary contribution may be killed cleanly.",
                "next_action": "build 2991 fixed boundary/reference zero proof or epsilon_Bv source-bound row.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2990_0_2991",
                "priority": "selected_primary",
                "next_doc": "2991-Y5-R2FR-fixed-boundary-reference-theta-zero-proof-or-epsilon-Bv-source-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_fixed_boundary_reference_theta_zero_proof_or_epsilon_Bv_source_bound_under_AX1090_2991.py",
                "objective": "Try to prove the fixed exact/topological boundary/reference sector gives delta_v B_ref=0 and no local boundary theta leakage on compact collars; if it fails, create a source-backed epsilon_Bv_ambiguity bound row without claiming local GR.",
                "include": "fixed-before-readout B_ref;allowed local variations;compact collar surface class;corner/improvement convention;delta_v B_ref;zero flux theorem;epsilon_Bv fallback",
                "exclude": "C_parent import;Omega promotion;V_WEP promotion;local-GR claim;Newton claim;public/GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2990*") if path.is_file()) if FORMALIZATION.exists() else 0
    selected_conditional = any(
        row["branch_id_local"] == "BNF2990_7_selected_route"
        and row["selection_status"] == "SELECTED_AS_CONDITIONAL_NOT_CLAIM"
        and not row["promoted_now"]
        for row in all_rows["branch_menu"]
    )
    normal_form_not_signed = any(
        row["normal_form_id"] == "NF2990_8_verdict"
        and row["current_status"] == "NORMAL_FORM_SELECTED_BUT_NOT_PARENT_SIGNED"
        and not row["promoted_now"]
        for row in all_rows["normal_form"]
    )
    acquisition_nonclaim = all(
        row["numeric_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO_SOURCE"
        and row["source_path"] == "MISSING_SOURCE_PATH"
        and not row["valid_numeric_bound"]
        and not row["valid_for_claim"]
        for row in all_rows["epsilon_acquisition"]
    )
    checks = [
        ("VAL2990_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2990_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2990_2_selected_conditional", selected_conditional, "least-scrutiny branch selected only as conditional scaffold", True),
        ("VAL2990_3_normal_form_not_signed", normal_form_not_signed, "normal form verdict remains not parent-signed", True),
        ("VAL2990_4_acquisition_nonclaim", acquisition_nonclaim, "epsilon acquisition rows are nonclaim and nonnumeric", True),
        ("VAL2990_5_no_promotion", all(not row["promotion_allowed_now"] for row in all_rows["gates"]), "no normal-form promotion allowed", True),
        ("VAL2990_6_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2990_7_next_written", any(row["next_id"] == "NEXT2990_0_2991" for row in all_rows["next"]), "2991 next target written", True),
        ("VAL2990_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2990_9_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2990_10_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2990_11_formalization_clean", formal_count == 0, f"no 2990 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2990_12_doc_written", DOC.exists(), "2990 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2990_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2990 validation overall", "required": True}))
    return out_rows


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


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2990 - Sector Normal Form Branch Selection or First epsilon_theta Source Row

Status: `Y5_R2FR_2990_least_scrutiny_sector_normal_form_selected_as_private_scaffold_not_parent_signed_first_epsilon_theta_source_rows_staged_nonclaim`

Claim ceiling: `no_parent_action_theorem_no_Theta_parent_promotion_no_Omega_promotion_no_parent_generator_no_VWEP_promotion_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The selected route is now explicit: `EH + fixed exact boundary + topological constants + silent quadratic extra + q-only matter + parent-owned projector/constraints + explicit residual fallback`.
- This is the least-scrutiny scaffold because it does not pretend the non-EH sectors vanish; it forces them to be exact, silent, constraint-owned, quotient-pulled back, or explicitly bounded.
- The scaffold is not a parent-action theorem yet. It remains private and conditional because boundary, extra, projector, matter, constraint and `M_ref` certificates are unsigned.
- No numeric `epsilon_theta` row is claim-grade yet. The first acquisition target is `epsilon_Bv_ambiguity`, because a fixed exact/topological boundary proof is the cleanest possible first closure.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Sector Normal-Form Branch Menu

{table(all_rows["branch_menu"], ["branch_id_local", "branch_name", "selection_status", "reason", "fallback_symbol", "promoted_now"])}

## Selected Parent Normal Form Contract

{table(all_rows["normal_form"], ["normal_form_id", "clause", "current_status", "theta_effect", "blocking_gap"])}

## Sector-by-Sector Theta Contract

{table(all_rows["sector_contract"], ["sector_contract_id", "sector", "normal_form_clause", "current_status", "fallback_symbol", "next_certificate_needed"])}

## First epsilon_theta Source-Row Acquisition

{table(all_rows["epsilon_acquisition"], ["acquisition_id", "priority_rank", "symbol", "component", "preferred_route", "current_status", "numeric_value", "valid_for_claim"])}

## Promotion Gates

{table(all_rows["gates"], ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

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
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "branch_menu": branch_menu_rows(),
        "normal_form": normal_form_rows(),
        "sector_contract": sector_contract_rows(),
        "epsilon_acquisition": epsilon_acquisition_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"])
    shutil.copyfile(OUTPUTS["epsilon_acquisition"], BRANCH_OUTPUTS["epsilon_acquisition_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2990 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
