from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2945"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2945-Y5-R2FR-source-normalized-stationary-q_loc-current-scale-or-denominator-blocker-under-AX1090.md"

SRC_2944_DOC = ROOT / "2944-Y5-R2FR-q_loc-finite-residual-bound-runner-source-inputs-under-AX1090.md"
SRC_2944_INPUTS = RESIDUALS / "P8_Y5_R2FR_2944_QLOC_BOUND_INPUT_STATUS_LEDGER.csv"
SRC_2944_HIERARCHY = RESIDUALS / "P8_Y5_R2FR_2944_BLOCKER_HIERARCHY.csv"
SRC_2944_NEXT = RESIDUALS / "P8_Y5_R2FR_2944_NEXT_TARGET.csv"
SRC_2944_PARTIAL = RESIDUALS / "P8_Y5_R2FR_2944_PARTIAL_DERIVATION_LEDGER.csv"
SRC_2467_DIV = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
SRC_2467_EXCHANGE = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
SRC_2467_WORLDTUBE = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_WORLDTUBE_SURFACE_GATE.csv"
SRC_2932_KAPPA_ELLJ = RESIDUALS / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv"
SRC_2934_ELLJ = RESIDUALS / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv"
SRC_2938_REFLOCK = RESIDUALS / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv"
SRC_2938_WORLD = RESIDUALS / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv"
SRC_2596_MHREF = RESIDUALS / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv"
SRC_2339_MHREF = RESIDUALS / "P8_Y5_PARENT_QLOC_2339_MHREF_FIRST_ROW.csv"
SRC_1518_MHREF = RESIDUALS / "P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv"
SRC_1774_MHREF_GATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1774_MHREF_DENOMINATOR_GATE.csv"
SRC_KAPPA_CONTRACT = RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv"
SRC_KAPPA_SUPER = RESIDUALS / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
SRC_WORLDTUBE_THEOREM = RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"
SRC_PIM_FLUX = RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv"
SRC_PIM_ALGEBRA = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_2615_EXCHANGE = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_2615_ZERO = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_SOURCE_ZERO_STATUS.csv"
SRC_2577_SELECTOR = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2945_SOURCE_REGISTER.csv",
    "stationary": RESIDUALS / "P8_Y5_R2FR_2945_STATIONARY_COLLAR_DERIVATION_ATTEMPT.csv",
    "denominator": RESIDUALS / "P8_Y5_R2FR_2945_DENOMINATOR_BLOCKER_ROWS.csv",
    "source_scale": RESIDUALS / "P8_Y5_R2FR_2945_SOURCE_SCALE_RESIDUAL_ROWS.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2945_ARENA_BLOCKER_ROWS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2945_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2945_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2945_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2945_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2945_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "stationary_copy": PARENT_ACTION / "Stationary_q_loc_source_normalized_derivation_attempt_2945_NONCLAIM.csv",
    "denominator_copy": LOCAL_BOUNDS / "Qloc_denominator_blocker_rows_2945_NONCLAIM.csv",
    "source_scale_copy": LOCAL_BOUNDS / "Qloc_source_scale_residual_rows_2945_NONCLAIM.csv",
    "arena_copy": LOCAL_BOUNDS / "Qloc_arena_blocker_rows_2945_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2945_MHREF_PIM_DENOMINATOR_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2945_00_2944_doc", SRC_2944_DOC, "NEXT2944_0_2945;Validation overall: `True`", "2944 selected source-normalized stationary q_loc target"),
        ("SRC2945_01_2944_inputs", SRC_2944_INPUTS, "IN2944_2_C_source_divergence;IN2944_6_C_denominator", "source divergence and denominator blocker inputs"),
        ("SRC2945_02_2944_hierarchy", SRC_2944_HIERARCHY, "BH2944_0_denominator_source_normalization;BH2944_1_source_divergence_exchange", "blocker hierarchy"),
        ("SRC2945_03_2944_next", SRC_2944_NEXT, "NEXT2944_0_2945", "machine-readable 2945 target"),
        ("SRC2945_04_2944_partial", SRC_2944_PARTIAL, "PD2944_0_source_divergence_identity;PD2944_1_stationary_collar", "partial derivation handoff"),
        ("SRC2945_05_2467_div", SRC_2467_DIV, "DIV2467_4_Killing_clock;DIV2467_5_generic_clock", "Hilbert-current divergence and stationary close condition"),
        ("SRC2945_06_2467_exchange", SRC_2467_EXCHANGE, "EXC2467_0_required_identity;EXC2467_3_local_stationary_escape", "exchange identity requirement"),
        ("SRC2945_07_2467_worldtube", SRC_2467_WORLDTUBE, "WTG2467_1_stationary_surface;WTG2467_4_external_vacuum", "worldtube stationary support"),
        ("SRC2945_08_2932_kappa_ellj", SRC_2932_KAPPA_ELLJ, "KLC2932_0_kappa_route;KLC2932_6_verdict", "kappa/ellJ constant proof audit"),
        ("SRC2945_09_2934_ellj", SRC_2934_ELLJ, "EJO2934_0_definition;EJO2934_5_verdict", "ell_J owner audit"),
        ("SRC2945_10_2938_reflock", SRC_2938_REFLOCK, "REF2938_0_MHref_definition;REF2938_4_no_laundering", "M_H_ref/ell_J reference lock"),
        ("SRC2945_11_2938_worldtube", SRC_2938_WORLD, "HWS2938_0_master_identity;HWS2938_6_verdict", "Hamiltonian/worldtube source measure attempt"),
        ("SRC2945_12_2596_mhref", SRC_2596_MHREF, "MHD2596_0_system;MISSING_SYSTEM_ID", "M_H_ref denominator rows"),
        ("SRC2945_13_2339_mhref", SRC_2339_MHREF, "MHR2339_0_first_row;MHR2339_3_zero_switch", "M_H_ref first row schema"),
        ("SRC2945_14_1518_mhref", SRC_1518_MHREF, "MH1518_0_M_H_ref;MH1518_7_acceptance", "M_H_ref surface lock"),
        ("SRC2945_15_1774_mhref_gate", SRC_1774_MHREF_GATE, "MHG1774_0_definition;MHG1774_4_verdict", "M_H_ref denominator gate"),
        ("SRC2945_16_kappa_contract", SRC_KAPPA_CONTRACT, "CU1_global_coupling_status;CU8_retained_residual_fallback", "constant universal kappa contract"),
        ("SRC2945_17_kappa_super", SRC_KAPPA_SUPER, "T508_0_global_sector;T508_2_no_residual_if_closed", "conditional kappa superselection theorem"),
        ("SRC2945_18_worldtube_theorem", SRC_WORLDTUBE_THEOREM, "T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout", "worldtube source-measure theorem"),
        ("SRC2945_19_pim_flux", SRC_PIM_FLUX, "FC1_stationary_or_Hamiltonian_time_generator;FC7_absolute_calibration_after_closure", "Pi_M flux closure contract"),
        ("SRC2945_20_pim_algebra", SRC_PIM_ALGEBRA, "PM5_projector_variation_owned;PM7_absolute_calibration_deferred", "Pi_M projector algebra contract"),
        ("SRC2945_21_2615_exchange", SRC_2615_EXCHANGE, "NEC2615_2_weight_collapse;NEC2615_5_current_verdict", "conditional source-weight collapse"),
        ("SRC2945_22_2615_zero", SRC_2615_ZERO, "SZ2615_0_derivation_gain;SZ2615_6_next", "source zero status"),
        ("SRC2945_23_2577_selector", SRC_2577_SELECTOR, "SRR2577_0_W_selector;SRR2577_6_delta_ellJ", "source selector and ellJ residuals"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def stationary_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "ST2945_0_define_JM",
            "clause": "Hilbert source current",
            "statement": "J_M^nu := ell_J T_matter^{nu rho} tau_rho",
            "derivation_status": "CANDIDATE_DEFINED",
            "claim_status": "ell_J and source owner unsigned",
            "condition_passed": False,
        },
        {
            "step_id": "ST2945_1_divergence_identity",
            "clause": "product-rule divergence",
            "statement": "nabla_nu J_M^nu = (nabla ell_J)T tau + ell_J(nabla T)tau + ell_J T nabla tau",
            "derivation_status": "EXACT_FORMULA_DERIVED",
            "claim_status": "formula usable for finite residuals",
            "condition_passed": True,
        },
        {
            "step_id": "ST2945_2_stationary_close",
            "clause": "Killing/local stationary collar",
            "statement": "If D ell_J=0, nabla T=0, nabla_(mu tau_nu)=0 and side flux is zero, then nabla.J_M=0.",
            "derivation_status": "CONDITIONAL_THEOREM",
            "claim_status": "stationary support only",
            "condition_passed": True,
        },
        {
            "step_id": "ST2945_3_surface_independence",
            "clause": "worldtube surface charge",
            "statement": "For compact support plus stationary clock, Q[S2]-Q[S1]=0 if no side/boundary/projector flux survives.",
            "derivation_status": "CONDITIONAL_THEOREM",
            "claim_status": "boundary/projector/source selector unsigned",
            "condition_passed": True,
        },
        {
            "step_id": "ST2945_4_source_normalization",
            "clause": "same charge normalizes Newton/R10/PPN",
            "statement": "M_H_ref, Pi_M J_H, G_ref, kappa and ell_J must be fixed in the same frame before readout.",
            "derivation_status": "REQUIRED_NOT_DERIVED",
            "claim_status": "denominator blocker",
            "condition_passed": False,
        },
        {
            "step_id": "ST2945_5_verdict",
            "clause": "source-normalized stationary q_loc route",
            "statement": "The stationary collar is a real conditional route, but not a claim-grade MTS local-GR derivation.",
            "derivation_status": "CONDITIONAL_ONLY_DENOMINATOR_BLOCKED",
            "claim_status": "emit source-scale blocker rows",
            "condition_passed": False,
        },
    ]
    return [add_common(row) for row in rows]


def denominator_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEN2945_0_MHref_value", "M_H_ref", "finite positive same-frame H_tau[S_outer]-H_ref", "MISSING_H_TAU;MISSING_H_REF;MISSING_M_H_REF", "Newton;R10;PPN;clock;orbital", "M_H_ref cannot be set to 1, bare mass, or orbital GM"),
        ("DEN2945_1_theta_Qtau", "theta_MTS/Q_tau", "parent Noether charge extracted with all sectors and reference terms", "MISSING_PARENT_THETA_QTAU", "Newton;PPN;orbital", "EH-only charge import rejected"),
        ("DEN2945_2_integrability", "H_tau integrability", "delta H_tau path-independent in allowed branch", "INTEGRABILITY_BLOCKED", "Newton;orbital;clock", "do not use fitted GM to bypass Hamiltonian curl"),
        ("DEN2945_3_fixed_reference", "H_ref/Sigma_ref", "source-blind fixed reference selected before readout", "REFERENCE_SELECTOR_UNSIGNED", "R10;PPN;Newton", "reference cannot absorb source/coupling residuals"),
        ("DEN2945_4_PiM_Hilbert", "Pi_M J_H equality", "(4*pi*G_ref)^-1 int_S Pi_M J_H = M_H_ref on linked surfaces", "MISSING_HILBERT_TO_HTAU_MAP", "Newton;R10;PPN;WEP", "conserved wrong charge is not measured mass"),
        ("DEN2945_5_kappa", "kappa_MTS/G_ref", "same-frame constant universal coupling with no source/range/frame/domain labels", "CONDITIONAL_ROUTE_NOT_PARENT_ADOPTED", "Newton;R10;PPN;clock;orbital", "global constant can calibrate only after no drift/hair is proved"),
        ("DEN2945_6_ellJ", "ell_J", "source-current scale fixed before worldtube/readout and not absorbed into M_H_ref or GM", "SOURCE_SCALE_OWNER_OPEN", "Newton;R10;PPN;clock;orbital;WEP", "ell_J remains active residual"),
        ("DEN2945_7_selector_shadow", "W_source/source-shadow", "same support/current owner and no separate source-shadow functional", "SOURCE_SHADOW_NOT_EXCLUDED", "WEP;R10;Newton;PPN", "source selector cannot be fitted after observing GM"),
    ]
    return [
        add_common(
            {
                "denominator_id": denominator_id,
                "object": obj,
                "required_condition": required,
                "current_status": status,
                "arenas_blocked": arenas,
                "anti_circularity_guard": guard,
            }
        )
        for denominator_id, obj, required, status, arenas, guard in rows
    ]


def source_scale_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "SSR2945_0_tau_strain",
            "residual": "E_tau_strain",
            "definition": "||T^{mu nu} nabla_(mu tau_nu)|| / source_norm",
            "zero_condition": "tau is Killing/stationary on collar",
            "status": "CONDITIONAL_ZERO_NO_DYNAMIC_PROOF",
        },
        {
            "residual_id": "SSR2945_1_DellJ",
            "residual": "Dln_ell_J",
            "definition": "source-current scale drift before readout",
            "zero_condition": "ell_J parent owner theorem with D_t,D_A,D_lambda derivatives zero",
            "status": "MISSING_PARENT_CONSTANT_ELLJ_PROOF_OR_VALUE",
        },
        {
            "residual_id": "SSR2945_2_Dkappa",
            "residual": "Dln_kappa_MTS",
            "definition": "coupling drift/source/range/frame dependence",
            "zero_condition": "global/superselection or topological kappa sector adopted plus source blindness",
            "status": "CONDITIONAL_KAPPA_ROUTE_NOT_ADOPTED",
        },
        {
            "residual_id": "SSR2945_3_delta_w_block",
            "residual": "delta_w_block",
            "definition": "remaining disconnected source-block prefactor after Noether exchange collapse",
            "zero_condition": "ordinary matter exchange graph connected and no source-shadow bypass",
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "SSR2945_4_side_flux",
            "residual": "worldtube_side_flux",
            "definition": "side/boundary/projector flux in exterior annulus normalized by M_H_ref",
            "zero_condition": "compact support, fixed linked surfaces, Pi_M chain map and boundary no-flux theorem",
            "status": "MISSING_FLUX_ZERO_OR_BOUND",
        },
    ]
    return [add_common(row) for row in rows]


def arena_rows() -> list[dict[str, Any]]:
    rows = [
        ("ARB2945_0_Newton", "Newton", "M_H_ref + Pi_M/Hilbert equality + kappa/G_ref", "DEN2945_0;DEN2945_4;DEN2945_5", "BLOCKED"),
        ("ARB2945_1_R10", "R10 alpha(lambda)", "same denominator plus ell_J/source scale and lambda source map", "DEN2945_0;DEN2945_6;DEN2945_7", "BLOCKED"),
        ("ARB2945_2_PPN", "PPN gamma/beta/alpha_i", "source-normalized weak-field metric response and no side/projector flux", "DEN2945_4;SSR2945_4", "BLOCKED"),
        ("ARB2945_3_clocks", "clock tests", "tau strain and kappa/ell_J drift bounds", "SSR2945_0;SSR2945_1;SSR2945_2", "BLOCKED"),
        ("ARB2945_4_orbital", "orbital systems", "no fitted GM; parent M_H_ref then downstream orbital readout", "DEN2945_0;DEN2945_2;DEN2945_5", "BLOCKED"),
        ("ARB2945_5_WEP", "WEP/source composition", "connected exchange graph and no source-shadow/non-Hilbert bypass", "SSR2945_3;DEN2945_7", "BLOCKED"),
    ]
    return [
        add_common(
            {
                "arena_block_id": block_id,
                "arena": arena,
                "needed_source_normalization": needed,
                "blocking_rows": blocking,
                "status": status,
            }
        )
        for block_id, arena, needed, blocking, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2945_0_stationary_theorem", "stationary q_loc source current theorem accepted as full local-GR proof", False, "CONDITIONAL_ONLY", False),
        ("CG2945_1_denominator", "M_H_ref/Pi_M/G_ref/ell_J/kappa denominator package is claim-grade", False, "DENOMINATOR_BLOCKED", False),
        ("CG2945_2_source_scale", "source scale residuals zero", False, "ELLJ_KAPPA_SOURCE_SHADOW_UNSIGNED", False),
        ("CG2945_3_q_loc_bound", "source-normalized q_loc finite bound score-ready", False, "NO_NUMERIC_OR_THEOREM_ZERO_ROWS", False),
        ("CG2945_4_Newton_GR", "Newton/local-GR reduction derived", False, "SOURCE_DENOMINATOR_AND_PPN_MAP_OPEN", False),
        ("CG2945_5_public_claim", "public claim allowed from 2945", False, "PRIVATE_NONCLAIM_CHECKPOINT", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2945_0_conditional_win", "stationary collar route is mathematically real", "nabla.J_M closes under constant ell_J, matter shell, Killing tau and no side flux", "keep as conditional theorem skeleton"),
        ("DEC2945_1_no_claim", "source-normalized local-GR not derived", "M_H_ref/Pi_M/G_ref/ell_J/kappa are not parent-signed in one package", "retain nonclaim status"),
        ("DEC2945_2_primary_next", "M_H_ref/Pi_M denominator package is the next wall", "without positive same-frame denominator and Hilbert/Hamiltonian equality every arena remains blocked", "attack denominator theorem or first real row"),
        ("DEC2945_3_source_scale_parallel", "ell_J/kappa/source-shadow remain coupled to denominator", "source-scale drift can mimic or hide local residuals", "carry residual rows into 2946"),
        ("DEC2945_4_anti_circularity", "no measured GM laundering", "orbital GM is downstream evidence, not a definition of M_H_ref", "keep guard active"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2945_0_2946",
                "priority": "selected_primary",
                "next_doc": "2946-Y5-R2FR-MHref-PiM-denominator-package-theorem-or-first-source-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_MHref_PiM_denominator_package_theorem_or_first_source_row_under_AX1090_2946.py",
                "objective": "Try to close the denominator package: prove or source M_H_ref=H_tau-H_ref as finite positive same-frame, Pi_M J_H equals the Hamiltonian/worldtube source charge, kappa/ell_J are fixed before readout, and no orbital-GM laundering occurs. If proof fails, emit first-row acquisition schema for each denominator component.",
                "include": "M_H_ref;H_tau;H_ref;theta_MTS;Q_tau;Pi_M J_H;G_ref;kappa;ell_J;worldtube selector;anti-circularity;R10/PPN/Newton arena rows",
                "exclude": "measured orbital GM as denominator; EH-only import; Gamma zero axiom; public claim; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("stationary_copy", OUTPUTS["stationary"], BRANCH_OUTPUTS["stationary_copy"]),
        ("denominator_copy", OUTPUTS["denominator"], BRANCH_OUTPUTS["denominator_copy"]),
        ("source_scale_copy", OUTPUTS["source_scale"], BRANCH_OUTPUTS["source_scale_copy"]),
        ("arena_copy", OUTPUTS["arenas"], BRANCH_OUTPUTS["arena_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2945 = False
    if FORMALIZATION.exists():
        formalization_has_2945 = any(FORMALIZATION.rglob("*2945*"))
    stationary = read_csv_rows(OUTPUTS["stationary"])
    denominator = read_csv_rows(OUTPUTS["denominator"])
    source_scale = read_csv_rows(OUTPUTS["source_scale"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    checks = [
        ("VAL2945_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2945_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2945_2_stationary_attempted", any(row.get("step_id") == "ST2945_5_verdict" for row in stationary), "stationary derivation verdict exists", True),
        ("VAL2945_3_stationary_not_claimed", any(row.get("step_id") == "ST2945_5_verdict" and row.get("condition_passed") == "False" for row in stationary), "stationary route remains nonclaim", True),
        ("VAL2945_4_denominator_rows", len(denominator) >= 8, "denominator blocker rows emitted", True),
        ("VAL2945_5_source_scale_rows", len(source_scale) >= 5, "source scale residual rows emitted", True),
        ("VAL2945_6_claims_blocked", all(row.get("claim_allowed") == "False" for row in claims), "all claims blocked", True),
        ("VAL2945_7_next_target_selected", any(row.get("next_id") == "NEXT2945_0_2946" for row in next_target), "2946 denominator package target selected", True),
        ("VAL2945_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2945_9_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2945_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2945_11_formalization_clean", not formalization_has_2945, "no 2945 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2945_OVERALL", "passed": overall, "check": "2945 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    stationary: list[dict[str, Any]],
    denominator: list[dict[str, Any]],
    source_scale: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2945_OVERALL")["passed"]
    text = f"""# 2945 - Y5 R2FR: source-normalized stationary q_loc current scale or denominator blocker under AX1090

Status: `Y5_R2FR_2945_stationary_q_loc_conditional_theorem_denominator_package_blocked`

Claim ceiling: `stationary_support_only_no_source_normalized_q_loc_bound_no_Newton_no_local_GR_no_R10_no_PPN_no_public_claim`

2945 tries the least-scrutiny route from 2944. The stationary collar is real as a conditional mathematical path:

`J_M^nu = ell_J T^{{nu rho}} tau_rho`

and

`nabla_nu J_M^nu = (nabla ell_J)T tau + ell_J(nabla T)tau + ell_J T nabla tau`.

So if `ell_J` is fixed, matter is on shell, `tau` is Killing/stationary, and side/boundary/projector flux is zero, then the local source current can be conserved in the collar. That is useful. But it is not yet the MTS-to-GR bridge because the same-frame denominator package is unsigned: `M_H_ref`, `Pi_M J_H`, `G_ref`, `kappa`, `ell_J`, the worldtube selector, and no source-shadow bypass must all be parent-owned before any local arena can be scored.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Stationary Collar Derivation Attempt

{md_table(stationary, ["step_id", "clause", "statement", "derivation_status", "claim_status", "condition_passed"])}

## Denominator Blocker Rows

{md_table(denominator, ["denominator_id", "object", "required_condition", "current_status", "arenas_blocked", "anti_circularity_guard"])}

## Source Scale Residual Rows

{md_table(source_scale, ["residual_id", "residual", "definition", "zero_condition", "status"])}

## Arena Blocker Rows

{md_table(arenas, ["arena_block_id", "arena", "needed_source_normalization", "blocking_rows", "status"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    stationary = stationary_rows()
    denominator = denominator_rows()
    source_scale = source_scale_rows()
    arenas = arena_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["stationary"], stationary)
    write_csv(OUTPUTS["denominator"], denominator)
    write_csv(OUTPUTS["source_scale"], source_scale)
    write_csv(OUTPUTS["arenas"], arenas)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, stationary, denominator, source_scale, arenas, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2945_OVERALL")["passed"]
    print(f"2945 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
