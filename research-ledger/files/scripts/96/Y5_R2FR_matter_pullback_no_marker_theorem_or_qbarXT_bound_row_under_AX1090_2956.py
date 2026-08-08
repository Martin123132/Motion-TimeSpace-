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

CHECKPOINT = "2956"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2956-Y5-R2FR-matter-pullback-no-marker-theorem-or-qbarXT-bound-row-under-AX1090.md"

SRC_2955_DOC = ROOT / "2955-Y5-R2FR-JX-Phi-source-zero-proof-or-first-residual-coefficient-row-under-AX1090.md"
SRC_2955_NEXT = RESIDUALS / "P8_Y5_R2FR_2955_NEXT_TARGET.csv"
SRC_2955_FIRST = RESIDUALS / "P8_Y5_R2FR_2955_FIRST_RESIDUAL_COEFFICIENT_ROW.csv"
SRC_1027_QZ = RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv"
SRC_1028_NM = RESIDUALS / "P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv"
SRC_980_FUNCTOR = RESIDUALS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
SRC_1046_MARKER = RESIDUALS / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv"
SRC_1046_QBAR = RESIDUALS / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"
SRC_974_COUNTER = RESIDUALS / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"
SRC_736_CONTRACT = RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv"
SRC_2611_PREMISE = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"
SRC_2611_CHAIN = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv"
SRC_2571_COFRAME = RESIDUALS / "P8_Y5_OBS_COFRAME_2571_DOBS_KERNEL_GATE.csv"
SRC_2659_HOM = RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv"
SRC_2673_JX = RESIDUALS / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2956_SOURCE_REGISTER.csv",
    "descent": RESIDUALS / "P8_Y5_R2FR_2956_MATTER_PULLBACK_DESCENT_AUDIT.csv",
    "markers": RESIDUALS / "P8_Y5_R2FR_2956_NO_MARKER_HIDDEN_FRAME_GATE.csv",
    "qbar": RESIDUALS / "P8_Y5_R2FR_2956_QBARXT_BOUND_ROW_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2956_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2956_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2956_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2956_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2956_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "descent_copy": PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv",
    "qbar_copy": LOCAL_BOUNDS / "qbarXT_bound_row_2956_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2956_HIDDEN_FRAME_MARKER_COEFFICIENT_OR_PHI_ROW_NEXT_NONCLAIM.csv",
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
        ("SRC2956_00_2955_doc", SRC_2955_DOC, "NEXT2955_0_2956;Validation overall: `True`", "2955 handoff"),
        ("SRC2956_01_2955_next", SRC_2955_NEXT, "NEXT2955_0_2956", "machine-readable 2956 target"),
        ("SRC2956_02_2955_first", SRC_2955_FIRST, "FIRST2955_0_qbar_XT_matter_marker", "first qbar_XT row"),
        ("SRC2956_03_1027_qz", SRC_1027_QZ, "QZ1027_0_chain_rule;QZ1027_6_verdict", "qbar_XT source-zero proof audit"),
        ("SRC2956_04_1028_nm", SRC_1028_NM, "NM1028_0_parent_q_kernel;NM1028_6_verdict", "no-marker theorem audit"),
        ("SRC2956_05_980_functor", SRC_980_FUNCTOR, "NMF980_2_scalar_obstruction_lemma;NMF980_7_verdict", "no-marker functor obstruction"),
        ("SRC2956_06_1046_marker", SRC_1046_MARKER, "CMA1046_0_alpha_EM;CMA1046_5_verdict", "constant/marker split audit"),
        ("SRC2956_07_1046_qbar", SRC_1046_QBAR, "QMC1046_0_b_conf;QMC1046_3_qbar_marker_abs", "qbar marker coefficient rows"),
        ("SRC2956_08_974_counter", SRC_974_COUNTER, "MCE974_0_linear_marker_covector;MCE974_5_verdict", "marker counterexample audit"),
        ("SRC2956_09_736_contract", SRC_736_CONTRACT, "NMC736_0_allowed_functor_domain;NMC736_5_limit", "matter no-marker contract"),
        ("SRC2956_10_2611_premise", SRC_2611_PREMISE, "PRE2611_0_q_map;PRE2611_8_verdict", "matter descent premise audit"),
        ("SRC2956_11_2611_chain", SRC_2611_CHAIN, "CR2611_0_variation_identity;CR2611_6_direct_vertex", "matter variation chain-rule decomposition"),
        ("SRC2956_12_2571_coframe", SRC_2571_COFRAME, "DOK2571_0_exact_kernel;DOK2571_4_current_verdict", "observed coframe DObs kernel gate"),
        ("SRC2956_13_2659_hom", SRC_2659_HOM, "RED2659_0_visible_algebra;RED2659_7_verdict", "no hidden-visible hom proof reduction"),
        ("SRC2956_14_2673_jx", SRC_2673_JX, "JX2673_3_constants_markers;JX2673_7_verdict", "J_X qbarXT audit"),
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


def descent_rows() -> list[dict[str, Any]]:
    rows = [
        ("DESC2956_0_chain_rule", "matter pullback chain rule", "delta_v S_matter vanishes if Dq[v_X]=0, e_obs=Obs(q), S_matter=Sbar[e_obs,theta], and Lie_v theta=0", "CONDITIONAL_THEOREM_VALID", "1027/2571/2611 give the shape", True, False),
        ("DESC2956_1_parent_q", "parent q and Dq kernel", "q exists before readout and Dq[v_X]=0 on the local branch", "NOT_PARENT_SIGNED", "q/v_X remains unsigned", False, False),
        ("DESC2956_2_observed_geometry", "observed coframe/metric descent", "e_obs and g_obs descend through q with no representative frame leakage", "CONDITIONAL_DESCENT_ONLY", "coframe contract exists but not parent-signed", False, False),
        ("DESC2956_3_matter_functor", "ordinary matter functor domain", "ordinary matter depends only on observed geometry, ordinary fields and fixed representation data", "EXACT_CONTRACT_NOT_PARENT_SIGNED", "direct source/worldtube vertices remain legal", False, False),
        ("DESC2956_4_constants", "constants/material markers", "masses, alpha_EM, clock constants, material standards and source labels are X-silent", "MISSING_NO_MARKER_THEOREM", "continuous constants and co-moving markers survive current no-marker theorem", False, False),
        ("DESC2956_5_hidden_frame", "hidden Weyl/disformal/source frame", "no A_g(X), B_g(X), source-only weight or hidden current slot survives", "MISSING_NO_SHADOW_FRAME_THEOREM", "hidden frame and source-weight rows remain live", False, False),
        ("DESC2956_6_boundary_worldtube", "worldtube/support/boundary", "source support and matter boundary terms are parent-owned, exact/proper or bounded", "MISSING_WORLDTUBE_BOUNDARY_OWNER", "support shift and boundary flux can source X", False, False),
        ("DESC2956_7_verdict", "qbar_XT=0 matter descent", "DESC2956_1 through DESC2956_6 all pass in one parent branch", "QBARXT_ZERO_NOT_DERIVED", "conditional chain rule is not enough", False, False),
    ]
    return [
        add_common(
            {
                "descent_id": descent_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "theorem_zero_credit": zero,
            }
        )
        for descent_id, obj, statement, status, evidence, conditional, zero in rows
    ]


def marker_rows() -> list[dict[str, Any]]:
    rows = [
        ("MARK2956_0_scalar_obstruction", "nonconstant invariant scalar obstruction", "one surviving invariant scalar can feed a continuous marker/constant functor", "OBSTRUCTION_PROVED", "980 blocks broad no-marker theorem", "qbar constants remain live"),
        ("MARK2956_1_co_moving_marker", "co-moving material marker", "material marker extends the quotient while remaining covariant", "COUNTEREXAMPLE_SURVIVES", "980/974 keep material/domain marker loopholes", "qbar_marker remains live"),
        ("MARK2956_2_alpha_EM", "alpha_EM/gauge coupling marker", "dimensionless EM constants must be quotient-owned or bounded", "NOT_PARENT_DERIVED_OPEN", "1046 keeps b_alpha open", "clock/EM/WEP rows live"),
        ("MARK2956_3_masses_clocks", "masses, ratios and clock transitions", "mass ratios and clock ratios are fixed representation data or X-silent", "NOT_PARENT_DERIVED_OPEN", "1046 keeps b_mA/b_clock live", "WEP/clock rows live"),
        ("MARK2956_4_hidden_frame", "hidden conformal/disformal frame", "b_conf=b_dis=0 by parent action-domain exclusion or bounded", "MISSING_COMPONENT_VALUES", "1046 qbar marker rows have no values", "R10/WEP/PPN rows live"),
        ("MARK2956_5_no_hidden_visible_hom", "hidden-visible hom theorem", "visible coefficient algebra excludes hidden invariants by parent domain theorem", "DOMAIN_SIGNATURE_MISSING", "2659 leaves ordinary matter interface unsigned", "finite coupling vector remains"),
        ("MARK2956_6_verdict", "no-marker/no-hidden-frame gate", "all marker/hidden clauses are theorem-zero or bounded", "NO_MARKER_GATE_NOT_CLOSED", "counterexamples survive until parent no-extension/triviality theorem closes", "qbar_XT bound row required"),
    ]
    return [
        add_common(
            {
                "marker_id": marker_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "residual_if_open": residual,
                "theorem_zero_credit": False,
            }
        )
        for marker_id, obj, statement, status, evidence, residual in rows
    ]


def qbar_rows() -> list[dict[str, Any]]:
    source_paths = ";".join(str(path) for path in [SRC_1046_QBAR, SRC_1046_MARKER, SRC_2673_JX])
    rows = [
        ("QXT2956_0_formula", "qbar_XT_abs", "|qbar_XT| <= |b_conf| + |tau_dis b_dis| + sum_A |s_A b_marker,A| + |b_alpha| + |b_mass/clock| + hidden source tails", "dimensionless", source_paths, "MISSING_COMPONENT_VALUES", False),
        ("QXT2956_1_b_conf", "b_conf", "vertical derivative of hidden conformal matter/source frame", "dimensionless", str(SRC_1046_QBAR), "MISSING_B_CONF_OR_THEOREM_ZERO", False),
        ("QXT2956_2_b_dis", "b_dis", "vertical derivative of disformal/profile-normalized matter frame slot", "model_dependent_declared", str(SRC_1046_QBAR), "MISSING_B_DIS_OR_THEOREM_ZERO", False),
        ("QXT2956_3_b_marker", "b_marker", "vertical derivative of material/source/preparation marker", "dimensionless_after_sensitivity_normalization", str(SRC_1046_QBAR), "MISSING_MARKER_COEFFICIENTS", False),
        ("QXT2956_4_b_alpha_mass_clock", "b_alpha;b_mA;b_clock", "EM, mass-ratio and clock transition marker derivatives", "dimensionless", str(SRC_1046_MARKER), "MISSING_CONSTANT_MARKER_VALUES", False),
        ("QXT2956_5_verdict", "qbar_XT", "first matter/test charge row remains nonclaim until every component is theorem-zero or source-backed", "dimensionless", source_paths, "NOT_SCORE_READY", False),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition_or_bound": definition,
                "units": units,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "numeric_or_theorem_value": status,
                "source_backed_value": source_backed,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, definition, units, source_path, status, source_backed in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2956_0_chain_rule", "visible matter chain-rule theorem claim", False, "PARENT_Q_OBS_MATTER_MARKERS_UNSIGNED"),
        ("CG2956_1_no_marker", "no-marker/no-hidden-frame theorem claim", False, "COUNTEREXAMPLES_SURVIVE"),
        ("CG2956_2_qbarXT_zero", "qbar_XT=0 theorem-zero", False, "QBARXT_ZERO_NOT_DERIVED"),
        ("CG2956_3_qbarXT_bound", "qbar_XT bound row score-ready", False, "COMPONENT_VALUES_MISSING"),
        ("CG2956_4_source_zero", "J_X source-zero closes", False, "MATTER_TEST_CHARGE_OPEN"),
        ("CG2956_5_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2956_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
        ("DEC2956_0_result", "qbar_XT=0 is not derived", "matter pullback descent is conditional, but parent q, observed coframe, matter functor, constants/markers and hidden-frame exclusion are not jointly signed", "keep qbar_XT as live residual"),
        ("DEC2956_1_counterexample", "broad no-marker theorem is blocked by surviving marker/functor counterexamples", "nonconstant invariant scalars and co-moving markers can feed continuous constants unless parent no-extension/triviality closes", "do not erase marker coefficients"),
        ("DEC2956_2_bound_row", "qbar_XT bound row is now explicit but nonclaim", "component rows b_conf, b_dis, b_marker, b_alpha and mass/clock markers all need theorem-zero or sourced values", "fill the first component next"),
        ("DEC2956_3_next", "next target should fill hidden-frame/marker coefficient or prove no-hidden-visible hom", "this is the narrowest repair for qbar_XT and WEP/clock/R10 source charge", "build 2957 hidden-frame marker coefficient or no-hidden-visible-hom theorem"),
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
                "next_id": "NEXT2956_0_2957",
                "priority": "selected_primary",
                "next_doc": "2957-Y5-R2FR-hidden-frame-marker-coefficient-or-no-hidden-visible-hom-theorem-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_hidden_frame_marker_coefficient_or_no_hidden_visible_hom_theorem_under_AX1090_2957.py",
                "objective": "Try to prove hidden conformal/disformal/material marker coefficients vanish by a parent no-hidden-visible-hom/domain theorem. If this fails, fill the first qbar_XT component row, starting with b_conf or b_marker, as nonclaim with units, source path and no-cancellation policy.",
                "include": "b_conf;b_dis;b_marker;b_alpha;mass/clock markers;visible coefficient algebra;hidden invariant obstruction;component bound row;source paths;units",
                "exclude": "quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("descent_copy", OUTPUTS["descent"], BRANCH_OUTPUTS["descent_copy"]),
        ("qbar_copy", OUTPUTS["qbar"], BRANCH_OUTPUTS["qbar_copy"]),
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
        ("VAL2956_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2956_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2956_2_descent_blocked", any(row["descent_id"] == "DESC2956_7_verdict" and row["theorem_zero_credit"] is False for row in all_rows["descent"]), "matter descent theorem-zero verdict is blocked", True),
        ("VAL2956_3_marker_blocked", any(row["marker_id"] == "MARK2956_6_verdict" and row["theorem_zero_credit"] is False for row in all_rows["markers"]), "no-marker theorem verdict is blocked", True),
        ("VAL2956_4_qbar_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["qbar"]), "qbar_XT rows remain nonclaim", True),
        ("VAL2956_5_qbar_paths_exist", all(row["source_path_exists"] is True for row in all_rows["qbar"]), "qbar_XT rows have existing source paths", True),
        ("VAL2956_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates are blocked", True),
        ("VAL2956_7_next_target_written", any(row["next_id"] == "NEXT2956_0_2957" for row in all_rows["next"]), "2957 next target selected", True),
        ("VAL2956_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2956_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2956_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2956_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2956 outputs were written to formalization-workbench", True),
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
    rows.append(add_common({"validation_id": "VAL2956_OVERALL", "passed": overall, "check": "2956 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2956 - Y5 R2FR: matter pullback no-marker theorem or qbarXT bound row under AX1090

Status: `Y5_R2FR_2956_qbarXT_zero_not_derived_marker_hidden_frame_bound_rows_emitted_nonclaim`

Claim ceiling: `no_qbarXT_zero_no_no_marker_theorem_no_hidden_frame_zero_no_qbarXT_score_no_source_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2956 asks whether ordinary matter is truly `X`-silent. The result is:

- The matter pullback chain-rule theorem is valid only conditionally: it needs parent `q`, `Dq[v_X]=0`, observed coframe descent, matter functor descent, and `X`-silent constants.
- The broad no-marker theorem is not available; the corpus retains scalar-invariant and co-moving marker counterexamples.
- Hidden conformal/disformal/source-frame and material-marker coefficients remain live, so `qbar_XT=0` is not derived.
- A nonclaim `qbar_XT` absolute bound row is now explicit, decomposed into `b_conf`, `b_dis`, `b_marker`, `b_alpha`, mass/clock markers, and hidden tails.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Matter Pullback Descent Audit

{md_table(all_rows["descent"], ["descent_id", "object", "current_status", "conditional_math_available", "theorem_zero_credit", "evidence_summary"])}

## No-Marker Hidden-Frame Gate

{md_table(all_rows["markers"], ["marker_id", "object", "current_status", "theorem_zero_credit", "residual_if_open"])}

## qbarXT Bound Row

{md_table(all_rows["qbar"], ["row_id", "symbol", "numeric_or_theorem_value", "units", "source_path_exists", "accepted_for_scoring"])}

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
        "descent": descent_rows(),
        "markers": marker_rows(),
        "qbar": qbar_rows(),
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

    print(f"2956 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
