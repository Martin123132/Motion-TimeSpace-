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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2958"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2958-Y5-R2FR-b-conf-b-marker-bound-row-or-hidden-domain-theorem-under-AX1090.md"

SRC_2957_DOC = ROOT / "2957-Y5-R2FR-hidden-frame-marker-coefficient-or-no-hidden-visible-hom-theorem-under-AX1090.md"
SRC_2957_NEXT = RESIDUALS / "P8_Y5_R2FR_2957_NEXT_TARGET.csv"
SRC_2957_FIRST = RESIDUALS / "P8_Y5_R2FR_2957_FIRST_COMPONENT_BOUND_ROW_NONCLAIM.csv"
SRC_2957_COMPONENTS = RESIDUALS / "P8_Y5_R2FR_2957_MARKER_COEFFICIENT_COMPONENT_ROWS.csv"
SRC_2957_HOM = RESIDUALS / "P8_Y5_R2FR_2957_NO_HIDDEN_VISIBLE_HOM_GATE.csv"
SRC_1046_QBAR = RESIDUALS / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"
SRC_1046_NOSHADOW = RESIDUALS / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
SRC_1046_FORBIDDEN = RESIDUALS / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv"
SRC_1046_MARKER = RESIDUALS / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv"
SRC_980_FUNCTOR = RESIDUALS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
SRC_974_COUNTER = RESIDUALS / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"
SRC_736_CONTRACT = RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv"
SRC_2659_HOM = RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv"
SRC_2673_JX = RESIDUALS / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
SRC_CLOCK_ALPHA = RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2958_SOURCE_REGISTER.csv",
    "bconf": RESIDUALS / "P8_Y5_R2FR_2958_BCONF_NO_SHADOW_THEOREM_GATE.csv",
    "bmarker": RESIDUALS / "P8_Y5_R2FR_2958_BMARKER_NO_MARKER_THEOREM_GATE.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_2958_COMPONENT_BOUND_ROWS_NONCLAIM.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2958_ARENA_PROJECTION_REQUIREMENTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2958_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2958_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2958_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2958_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2958_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "domain_copy": PARENT_ACTION / "b_conf_b_marker_domain_theorem_gate_2958_NOT_DERIVED.csv",
    "bound_copy": LOCAL_BOUNDS / "b_conf_b_marker_component_bound_rows_2958_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2958_SINGLE_FRAME_OR_MARKER_BOUND_NEXT_NONCLAIM.csv",
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
        ("SRC2958_00_2957_doc", SRC_2957_DOC, "NEXT2957_0_2958;Validation overall: `True`", "2957 handoff"),
        ("SRC2958_01_2957_next", SRC_2957_NEXT, "NEXT2957_0_2958", "machine-readable 2958 target"),
        ("SRC2958_02_2957_first", SRC_2957_FIRST, "FIRST2957_0_b_conf;FIRST2957_1_b_marker", "first component target rows"),
        ("SRC2958_03_2957_components", SRC_2957_COMPONENTS, "COMP2957_0_b_conf;COMP2957_2_b_marker;COMP2957_5_qbar_marker_abs", "2957 component rows"),
        ("SRC2958_04_2957_hom", SRC_2957_HOM, "HOM2957_3_frame_slot_exclusion;HOM2957_5_material_marker_extension;HOM2957_7_verdict", "2957 hom gate"),
        ("SRC2958_05_1046_qbar", SRC_1046_QBAR, "QMC1046_0_b_conf;QMC1046_2_b_marker;QMC1046_3_qbar_marker_abs", "qbar marker coefficient rows"),
        ("SRC2958_06_1046_noshadow", SRC_1046_NOSHADOW, "NSF1046_1_conditional_chain_rule_zero;NSF1046_2_no_extra_frame_slot;NSF1046_5_verdict", "no-shadow theorem attempt"),
        ("SRC2958_07_1046_forbidden", SRC_1046_FORBIDDEN, "FV1046_0_conformal_frame;FV1046_5_material_marker", "forbidden vertex catalog"),
        ("SRC2958_08_1046_marker", SRC_1046_MARKER, "CMA1046_3_material_markers;CMA1046_5_verdict", "constant/marker split audit"),
        ("SRC2958_09_980_functor", SRC_980_FUNCTOR, "NMF980_2_scalar_obstruction_lemma;NMF980_4_co_moving_marker_extension;NMF980_7_verdict", "no-marker functor obstruction"),
        ("SRC2958_10_974_counter", SRC_974_COUNTER, "MCE974_0_linear_marker_covector;MCE974_2_material_domain_marker;MCE974_5_verdict", "marker counterexamples"),
        ("SRC2958_11_736_contract", SRC_736_CONTRACT, "NMC736_1_one_observed_coframe;NMC736_3_shadow_frame_forbidden;NMC736_5_limit", "matter no-marker contract"),
        ("SRC2958_12_2659_hom", SRC_2659_HOM, "RED2659_1_functor_domain;RED2659_3_single_frame_slot;RED2659_7_verdict", "parent hom reduction matrix"),
        ("SRC2958_13_2673_jx", SRC_2673_JX, "JX2673_3_constants_markers;JX2673_4_hidden_frame;JX2673_7_verdict", "J_X/qbarXT source-zero audit"),
        ("SRC2958_14_local_bounds", SRC_LOCAL_BOUNDS, "R1_WEP_source_charge;R2_clock_redshift;R3_gamma", "local WEP/clock/PPN bound anchors"),
        ("SRC2958_15_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 review-candidate curve, nonclaim"),
        ("SRC2958_16_clock_alpha", SRC_CLOCK_ALPHA, "CAS646_0_AlHg;CAS646_1_YbE3E2", "clock alpha sensitivity rows"),
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


def bconf_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BCONF2958_0_definition",
            "define b_conf",
            "If an ordinary matter/source frame has g_A = exp(2 a_A) g_obs, then b_conf,A := D_vX a_A on the local branch.",
            "DEFINITION_SHARP",
            "b_conf is the vertical derivative of a hidden conformal matter/source frame.",
            True,
            False,
        ),
        (
            "BCONF2958_1_chain_rule_zero",
            "conditional quotient zero",
            "If a_A(Phi)=abar_A(q(Phi)) plus a constant calibration and Dq[v_X]=0, then b_conf,A = D abar_A[Dq(v_X)] = 0.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the clean derivation route: no phenomenology is needed once the domain is signed.",
            True,
            False,
        ),
        (
            "BCONF2958_2_single_frame_domain",
            "single observed frame",
            "Parent S_matter admits e_obs(q) and omega[e_obs] only, not exp(a_A(Xhat)) e_obs or source-specific hidden frame slots.",
            "NOT_PARENT_SIGNED",
            "1046/2659 have this as a contract target, not a parent theorem.",
            False,
            False,
        ),
        (
            "BCONF2958_3_common_calibration",
            "constant common calibration",
            "A constant A_0 may be absorbed into units/G calibration; only D_vX ln A_A is a finite coupling.",
            "CONDITIONAL_GAUGE_STATEMENT",
            "Safe only after source/readout order is fixed so calibration cannot hide a source-only weight.",
            True,
            False,
        ),
        (
            "BCONF2958_4_countermodel",
            "legal retained countermodel",
            "S_A[psi_A, exp(2 epsilon Xhat) g_obs] is covariant and can be universal, so WEP alone does not forbid it.",
            "COUNTERMODEL_RETAINED",
            "This gives b_conf=epsilon and creates trace/source-normalization/fifth-force pressure unless parent domain forbids it.",
            False,
            False,
        ),
        (
            "BCONF2958_5_verdict",
            "b_conf theorem-zero",
            "BCONF2958_1 plus BCONF2958_2 plus readout/source calibration silence hold in the parent action.",
            "BCONF_ZERO_NOT_DERIVED",
            "The chain-rule proof is exact, but the single-frame parent action-domain clause is unsigned.",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "parent_signed": signed,
                "theorem_zero_credit": signed,
            }
        )
        for gate_id, obj, statement, status, evidence, conditional, signed in rows
    ]


def bmarker_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BMARK2958_0_definition",
            "define b_marker",
            "For a material/source/preparation marker m_A, b_marker,A := D_vX ln M_A or D_vX theta_A(m_A) after sensitivity normalization.",
            "DEFINITION_SHARP",
            "The row captures composition/source markers that can survive even when the metric frame is common.",
            True,
            False,
        ),
        (
            "BMARK2958_1_fixed_label_zero",
            "fixed representation label zero",
            "If m_A is fixed representation data or a discrete species label independent of X, then D_vX m_A=0 and b_marker,A=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the clean theorem-zero route for true species labels.",
            True,
            False,
        ),
        (
            "BMARK2958_2_no_extension_domain",
            "no co-moving marker extension",
            "The parent ordinary-matter category excludes Q_tilde=(Q_obs,m(X)) extensions that feed constants, source weights or preparation labels.",
            "NOT_PARENT_SIGNED",
            "980 explicitly keeps co-moving marker extensions legal until no-extension/triviality is derived.",
            False,
            False,
        ),
        (
            "BMARK2958_3_scalar_obstruction",
            "scalar invariant obstruction",
            "Any surviving nonconstant invariant scalar I can generate m=m0+epsilon I unless the invariant algebra is trivial or the marker codomain is discrete and connected-domain locked.",
            "COUNTEREXAMPLE_RETAINED",
            "This blocks a broad no-marker theorem.",
            False,
            False,
        ),
        (
            "BMARK2958_4_source_preparation_marker",
            "source/preparation marker",
            "Isotope fraction, material preparation, source domain, or post-readout P_active labels must be fixed inputs, pure gauge, or explicit residuals.",
            "MATERIAL_MARKER_NOT_ERASED",
            "974/1046 retain material-domain marker counterexamples.",
            False,
            False,
        ),
        (
            "BMARK2958_5_verdict",
            "b_marker theorem-zero",
            "BMARK2958_1 plus BMARK2958_2 plus no scalar-marker counterexample and no post-readout source marker all hold.",
            "BMARKER_ZERO_NOT_DERIVED",
            "Fixed labels can be silent, but the parent no-extension theorem is not signed.",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "parent_signed": signed,
                "theorem_zero_credit": signed,
            }
        )
        for gate_id, obj, statement, status, evidence, conditional, signed in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BOUND2958_0_b_conf",
            "b_conf",
            "|b_conf| <= B_conf := min_i B_i/|tau_i_conf| over declared R10, PPN gamma, clock/redshift and source-normalization projections",
            "dimensionless",
            "tau_R10_conf;tau_PPN_gamma_conf;tau_clock_conf;tau_source_conf;lambda_X;normalization_Xhat",
            ";".join(str(path) for path in [SRC_1046_QBAR, SRC_1046_NOSHADOW, SRC_LOCAL_BOUNDS, SRC_R10_CURVE]),
            "MISSING_TAU_PROJECTIONS_AND_PARENT_ZERO",
        ),
        (
            "BOUND2958_1_b_marker",
            "b_marker",
            "sum_A |s_A b_marker,A| <= B_marker := min_i B_i/|tau_i_marker| over WEP composition, R10 source charge, clock and source-preparation projections",
            "dimensionless_after_sensitivity_normalization",
            "material_pair;s_A;tau_WEP_marker;tau_R10_marker;tau_clock_marker;source_preparation_taxonomy",
            ";".join(str(path) for path in [SRC_1046_QBAR, SRC_1046_MARKER, SRC_980_FUNCTOR, SRC_974_COUNTER, SRC_LOCAL_BOUNDS]),
            "MISSING_MARKER_SENSITIVITIES_AND_PARENT_ZERO",
        ),
        (
            "BOUND2958_2_joint_envelope",
            "qbarXT_hidden_marker_abs",
            "|qbar_XT| <= |tau_conf b_conf| + |tau_marker sum_A s_A b_marker,A| + retained b_dis/b_alpha/mass/clock tails",
            "dimensionless_or_declared_profile_units",
            "b_conf;b_marker;tau_conf;tau_marker;b_dis;b_alpha;b_mass_clock;no_cancellation_policy",
            ";".join(str(path) for path in [SRC_2957_COMPONENTS, SRC_1046_QBAR, SRC_2673_JX]),
            "MISSING_COMPONENT_VALUES",
        ),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula_or_bound": formula,
                "units": units,
                "required_inputs": required,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "numeric_or_theorem_value": value,
                "source_backed_value": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, formula, units, required, source_path, value in rows
    ]


def arena_rows() -> list[dict[str, Any]]:
    rows = [
        ("ARENA2958_0_R10_b_conf", "R10", "b_conf", "tau_R10_conf(lambda_X) maps conformal frame coupling into alpha(lambda)", "MISSING_ARENA_PROJECTION", str(SRC_R10_CURVE)),
        ("ARENA2958_1_WEP_b_marker", "WEP/composition", "b_marker", "tau_WEP_marker and material sensitivities map b_marker,A into eta_AB", "MISSING_MATERIAL_SENSITIVITIES", str(SRC_LOCAL_BOUNDS)),
        ("ARENA2958_2_PPN_b_conf", "PPN/Cassini", "b_conf", "tau_PPN_gamma_conf maps universal conformal coupling into gamma_minus_1 or source-normalization residual", "MISSING_PPN_PROJECTION", str(SRC_LOCAL_BOUNDS)),
        ("ARENA2958_3_clock_b_conf", "clock/redshift", "b_conf", "tau_clock_conf maps local Xhat response into redshift/LPI observable", "MISSING_CLOCK_PROJECTION", str(SRC_LOCAL_BOUNDS)),
        ("ARENA2958_4_clock_b_marker", "clock/alpha", "b_marker;b_alpha", "clock sensitivities exist but MTS projection from Xhat to clock ratio remains missing", "MISSING_MTS_PROJECTION", str(SRC_CLOCK_ALPHA)),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "component": component,
                "projection_requirement": requirement,
                "current_status": status,
                "source_path": source_path,
                "source_path_exists": Path(source_path).exists(),
                "ready_for_score": False,
            }
        )
        for arena_id, arena, component, requirement, status, source_path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2958_0_b_conf_zero", "b_conf=0 theorem-zero", False, "SINGLE_OBSERVED_FRAME_PARENT_DOMAIN_UNSIGNED"),
        ("CG2958_1_b_marker_zero", "b_marker=0 theorem-zero", False, "NO_MARKER_EXTENSION_THEOREM_UNSIGNED"),
        ("CG2958_2_b_conf_bound", "b_conf numeric/source bound score-ready", False, "TAU_PROJECTIONS_MISSING"),
        ("CG2958_3_b_marker_bound", "b_marker numeric/source bound score-ready", False, "MATERIAL_SENSITIVITIES_MISSING"),
        ("CG2958_4_qbarXT_hidden_marker", "hidden-marker qbarXT envelope score-ready", False, "COMPONENT_VALUES_MISSING"),
        ("CG2958_5_R10_WEP_PPN_clock", "arena scoring allowed", False, "MTS_SIDE_ROWS_NONCLAIM"),
        ("CG2958_6_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2958_7_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2958_0_b_conf",
            "b_conf is conditionally killed but not parent-derived",
            "the chain-rule proof is exact if the parent action has one observed frame and no hidden conformal source slot; that action-domain signature is still unsigned",
            "do not claim b_conf=0; pursue single-frame parent action clause or source tau_conf bounds",
        ),
        (
            "DEC2958_1_b_marker",
            "b_marker is not killed by covariance alone",
            "co-moving markers and scalar invariant marker maps remain legal counterexamples unless no-extension/triviality is derived",
            "do not claim b_marker=0; either prove no-marker domain theorem or source material-pair rows",
        ),
        (
            "DEC2958_2_bounds",
            "component bound rows are source-ready but nonclaim",
            "local bound anchors exist, but MTS arena projections tau_i and component values/theorem-zeros are missing",
            "keep all arena scoring blocked",
        ),
        (
            "DEC2958_3_next",
            "next target should isolate the single-frame parent action clause",
            "b_conf is less messy than b_marker and directly gates the no-shadow frame route to local GR/PPN/R10",
            "build 2959 single-observed-frame parent action clause or b_conf source-bound intake",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2958_0_2959",
                "priority": "selected_primary",
                "next_doc": "2959-Y5-R2FR-single-observed-frame-parent-action-clause-or-bconf-bound-intake-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_single_observed_frame_parent_action_clause_or_bconf_bound_intake_under_AX1090_2959.py",
                "objective": "Try to derive the single-observed-frame parent action clause that forbids hidden conformal matter/source frames and gives b_conf=0. If the clause remains unsigned, fill a b_conf source-bound intake row with tau_R10, tau_PPN, tau_clock and source-normalization projections as nonclaim inputs.",
                "include": "single observed frame;ordinary matter domain;source frame exclusion;common calibration;readout order;tau_R10_conf;tau_PPN_gamma_conf;tau_clock_conf;source paths;units",
                "exclude": "b_marker full material taxonomy unless b_conf closes;quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("domain_copy", OUTPUTS["bconf"], BRANCH_OUTPUTS["domain_copy"]),
        ("bound_copy", OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2958_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2958_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2958_2_bconf_blocked", any(row["gate_id"] == "BCONF2958_5_verdict" and row["theorem_zero_credit"] is False for row in all_rows["bconf"]), "b_conf theorem-zero remains blocked", True),
        ("VAL2958_3_bmarker_blocked", any(row["gate_id"] == "BMARK2958_5_verdict" and row["theorem_zero_credit"] is False for row in all_rows["bmarker"]), "b_marker theorem-zero remains blocked", True),
        ("VAL2958_4_bounds_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["bounds"]), "component bound rows remain nonclaim", True),
        ("VAL2958_5_bound_paths_exist", all(row["source_path_exists"] is True for row in all_rows["bounds"]), "component bound rows cite existing paths", True),
        ("VAL2958_6_arenas_blocked", all(row["ready_for_score"] is False and row["valid_for_claim"] is False for row in all_rows["arenas"]), "arena projections remain blocked", True),
        ("VAL2958_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2958_8_next_target_written", any(row["next_id"] == "NEXT2958_0_2959" for row in all_rows["next"]), "2959 next target selected", True),
        ("VAL2958_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2958_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2958_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2958_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2958 outputs were written to formalization-workbench", True),
        ("VAL2958_13_doc_written", DOC.exists(), "2958 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2958_OVERALL", "passed": overall, "check": "2958 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2958 - Y5 R2FR: b_conf/b_marker bound row or hidden-domain theorem under AX1090

Status: `Y5_R2FR_2958_bconf_bmarker_zero_not_parent_derived_component_bound_rows_emitted_nonclaim`

Claim ceiling: `no_b_conf_zero_no_b_marker_zero_no_qbarXT_hidden_marker_score_no_R10_WEP_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2958 tries the least hand-wavy route for the surviving coupling: prove the two sharp coefficients vanish from the parent action domain. The result is:

- `b_conf=0` is conditionally derived if ordinary matter has exactly one observed frame and every hidden conformal factor is either quotient-pulled or constant calibration.
- That single-frame/no-shadow parent action clause is not signed, and a covariant countermodel `S_A[psi_A, exp(2 epsilon Xhat) g_obs]` remains legal.
- `b_marker=0` is conditionally derived only for fixed representation/species labels; broad material-marker erasure fails because co-moving/scalar marker counterexamples survive.
- Nonclaim bound rows now exist for `b_conf`, `b_marker`, and the joint hidden-marker envelope, but arena projections are still missing.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## b_conf No-Shadow Theorem Gate

{md_table(all_rows["bconf"], ["gate_id", "object", "current_status", "conditional_math_available", "parent_signed", "theorem_zero_credit", "evidence_summary"])}

## b_marker No-Marker Theorem Gate

{md_table(all_rows["bmarker"], ["gate_id", "object", "current_status", "conditional_math_available", "parent_signed", "theorem_zero_credit", "evidence_summary"])}

## Component Bound Rows

{md_table(all_rows["bounds"], ["row_id", "symbol", "numeric_or_theorem_value", "units", "source_path_exists", "accepted_for_scoring", "required_inputs"])}

## Arena Projection Requirements

{md_table(all_rows["arenas"], ["arena_id", "arena", "component", "current_status", "source_path_exists", "projection_requirement"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "bconf": bconf_rows(),
        "bmarker": bmarker_rows(),
        "bounds": bound_rows(),
        "arenas": arena_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2958 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
