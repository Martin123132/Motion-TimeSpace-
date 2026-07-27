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

CHECKPOINT = "2957"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2957-Y5-R2FR-hidden-frame-marker-coefficient-or-no-hidden-visible-hom-theorem-under-AX1090.md"

SRC_2956_DOC = ROOT / "2956-Y5-R2FR-matter-pullback-no-marker-theorem-or-qbarXT-bound-row-under-AX1090.md"
SRC_2956_NEXT = RESIDUALS / "P8_Y5_R2FR_2956_NEXT_TARGET.csv"
SRC_2956_QBAR = RESIDUALS / "P8_Y5_R2FR_2956_QBARXT_BOUND_ROW_NONCLAIM.csv"
SRC_1046_QBAR = RESIDUALS / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"
SRC_1046_CONSTANTS = RESIDUALS / "P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv"
SRC_1046_MARKER = RESIDUALS / "P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv"
SRC_1046_NOSHADOW = RESIDUALS / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
SRC_1046_FORBIDDEN = RESIDUALS / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv"
SRC_1046_GATES = RESIDUALS / "P8_Y5_R10_1046_CLAIM_GATES.csv"
SRC_980_FUNCTOR = RESIDUALS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
SRC_974_COUNTER = RESIDUALS / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"
SRC_736_CONTRACT = RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv"
SRC_2659_HOM = RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv"
SRC_2673_JX = RESIDUALS / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2957_SOURCE_REGISTER.csv",
    "hom": RESIDUALS / "P8_Y5_R2FR_2957_NO_HIDDEN_VISIBLE_HOM_GATE.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_2957_MARKER_COEFFICIENT_COMPONENT_ROWS.csv",
    "first": RESIDUALS / "P8_Y5_R2FR_2957_FIRST_COMPONENT_BOUND_ROW_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2957_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2957_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2957_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2957_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2957_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hom_copy": PARENT_ACTION / "no_hidden_visible_hom_gate_2957_NOT_DERIVED.csv",
    "component_copy": LOCAL_BOUNDS / "qbarXT_marker_component_rows_2957_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2957_BCONF_BMARKER_BOUND_OR_HIDDEN_DOMAIN_THEOREM_NEXT_NONCLAIM.csv",
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
        ("SRC2957_00_2956_doc", SRC_2956_DOC, "NEXT2956_0_2957;Validation overall: `True`", "2956 handoff"),
        ("SRC2957_01_2956_next", SRC_2956_NEXT, "NEXT2956_0_2957", "machine-readable 2957 target"),
        ("SRC2957_02_2956_qbar", SRC_2956_QBAR, "QXT2956_1_b_conf;QXT2956_3_b_marker;QXT2956_5_verdict", "2956 qbar component row"),
        ("SRC2957_03_1046_qbar", SRC_1046_QBAR, "QMC1046_0_b_conf;QMC1046_3_qbar_marker_abs", "older qbar marker component rows"),
        ("SRC2957_04_1046_constants", SRC_1046_CONSTANTS, "QCC1046_0_b_alpha;QCC1046_3_qbar_constants_abs", "constant-sector component rows"),
        ("SRC2957_05_1046_marker", SRC_1046_MARKER, "CMA1046_0_alpha_EM;CMA1046_5_verdict", "constant/marker split audit"),
        ("SRC2957_06_1046_noshadow", SRC_1046_NOSHADOW, "NSF1046_1_conditional_chain_rule_zero;NSF1046_5_verdict", "no-shadow-frame theorem attempt"),
        ("SRC2957_07_1046_forbidden", SRC_1046_FORBIDDEN, "FV1046_0_conformal_frame;FV1046_5_material_marker", "forbidden vertex catalog"),
        ("SRC2957_08_1046_gates", SRC_1046_GATES, "CG1046_0_no_shadow_frame;CG1046_4_R10_WEP_clock_score", "1046 claim gates"),
        ("SRC2957_09_980_functor", SRC_980_FUNCTOR, "NMF980_2_scalar_obstruction_lemma;NMF980_4_co_moving_marker_extension;NMF980_7_verdict", "no-marker functor obstruction"),
        ("SRC2957_10_974_counter", SRC_974_COUNTER, "MCE974_0_linear_marker_covector;MCE974_5_verdict", "marker counterexamples"),
        ("SRC2957_11_736_contract", SRC_736_CONTRACT, "NMC736_0_allowed_functor_domain;NMC736_5_limit", "matter no-marker contract"),
        ("SRC2957_12_2659_hom", SRC_2659_HOM, "RED2659_0_visible_algebra;RED2659_7_verdict", "no-hidden-visible-hom reduction"),
        ("SRC2957_13_2673_jx", SRC_2673_JX, "JX2673_3_constants_markers;JX2673_7_verdict", "J_X/qbarXT source-zero audit"),
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


def hom_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HOM2957_0_theorem_target",
            "no-hidden-visible-hom theorem",
            "Every ordinary visible coefficient is either q-pulled back or fixed representation data, so D_vX c_visible=0.",
            "EXACT_CONDITIONAL_TARGET",
            "This would kill b_conf, b_dis, b_marker, b_alpha and mass/clock marker derivatives.",
            True,
            False,
        ),
        (
            "HOM2957_1_visible_algebra",
            "visible coefficient algebra",
            "A_ord = q^* A_Q plus A_fixed before readout and before source fitting.",
            "NOT_PARENT_SIGNED",
            "2659 asks for this signature; 2956 still treats it as a live premise.",
            False,
            False,
        ),
        (
            "HOM2957_2_functor_domain",
            "ordinary matter functor domain",
            "S_ord is a functor only of Q_obs, ordinary matter fields and fixed representation data.",
            "NOT_PARENT_SIGNED",
            "Extra hidden X arguments are not yet type errors in the parent action.",
            False,
            False,
        ),
        (
            "HOM2957_3_frame_slot_exclusion",
            "conformal/disformal frame slots",
            "No A_g(Xhat), B_g(Xhat), D_A(Xhat), hidden source frame or source-only frame argument is allowed.",
            "NO_SHADOW_FRAME_NOT_SIGNED",
            "1046 has the exact conditional chain rule but not the parent action-domain exclusion.",
            False,
            False,
        ),
        (
            "HOM2957_4_constant_superselection",
            "alpha, masses and clocks",
            "alpha_EM, masses, charge units and clock constants are fixed representation/superselection data with zero vertical derivative.",
            "CONSTANT_MARKER_ZERO_NOT_SIGNED",
            "1046 keeps alpha/mass/clock rows open as residual coefficients.",
            False,
            False,
        ),
        (
            "HOM2957_5_material_marker_extension",
            "material/source/preparation markers",
            "Co-moving material labels, source domains and preparation markers cannot extend the quotient with X-sensitive data.",
            "COUNTEREXAMPLES_SURVIVE",
            "980 and 974 retain scalar-invariant and co-moving marker counterexamples.",
            False,
            False,
        ),
        (
            "HOM2957_6_boundary_readout_silence",
            "boundary, support and post-readout selectors",
            "Boundary/support/readout operations cannot manufacture hidden visible coefficients after variation.",
            "MISSING_DOMAIN_SILENCE_SIGNATURE",
            "2659 records boundary/domain silence as still unsigned.",
            False,
            False,
        ),
        (
            "HOM2957_7_verdict",
            "parent no-hidden-visible-hom closure",
            "HOM2957_1 through HOM2957_6 all pass in one parent action/domain contract.",
            "NO_HIDDEN_VISIBLE_HOM_NOT_DERIVED",
            "The conditional proof is sharp, but the domain signatures are not parent-owned.",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "parent_signed": signed,
                "theorem_zero_credit": signed,
            }
        )
        for gate_id, obj, statement, status, evidence, conditional, signed in rows
    ]


def component_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "COMP2957_0_b_conf",
            "b_conf",
            "vertical derivative of hidden conformal matter/source frame, d ln A_A/dXhat",
            "|qbar_XT| contains |b_conf| times source/test sensitivity and arena projection",
            "dimensionless",
            "R10;WEP;clock;PPN;source_normalization",
            str(SRC_1046_QBAR),
            "MISSING_B_CONF_OR_THEOREM_ZERO",
        ),
        (
            "COMP2957_1_b_dis",
            "b_dis",
            "vertical derivative of disformal/profile-normalized matter frame slot",
            "|qbar_XT| contains |tau_dis b_dis| plus preferred-frame/orbital projections",
            "model_dependent_declared",
            "PPN;preferred_frame;clock;orbital;R10",
            str(SRC_1046_QBAR),
            "MISSING_B_DIS_OR_THEOREM_ZERO",
        ),
        (
            "COMP2957_2_b_marker",
            "b_marker",
            "vertical derivative of material/source/preparation marker",
            "|qbar_XT| contains sum_A |s_A b_marker,A|",
            "dimensionless_after_sensitivity_normalization",
            "WEP_source_charge;composition;clock;R10",
            str(SRC_1046_QBAR),
            "MISSING_MARKER_COEFFICIENTS",
        ),
        (
            "COMP2957_3_b_alpha",
            "b_alpha",
            "vertical derivative of alpha_EM or equivalent gauge kinetic marker",
            "|qbar_XT| contains |s_alpha b_alpha| and clock/spectral sensitivity terms",
            "dimensionless",
            "clock;EM;spectra;WEP;R10",
            str(SRC_1046_CONSTANTS),
            "MISSING_B_ALPHA_OR_SUPERSELECTION_ZERO",
        ),
        (
            "COMP2957_4_b_mass_clock",
            "b_mA;b_clock_i",
            "vertical derivative of mass ratios, binding data and clock transition ratios",
            "|qbar_XT| contains sum_A |s_mA b_mA| + sum_i |s_clock_i b_clock_i|",
            "dimensionless",
            "clock;WEP;composition;orbital",
            str(SRC_1046_CONSTANTS),
            "MISSING_MASS_CLOCK_MARKER_VALUES",
        ),
        (
            "COMP2957_5_qbar_marker_abs",
            "qbar_marker_abs",
            "no-cancellation envelope for hidden frame and material-marker contribution",
            "|qbar_marker| <= |b_conf| + |tau_dis b_dis| + sum_A |s_A b_marker,A| + hidden post-readout terms",
            "dimensionless_or_declared_profile_units",
            "WEP;R10;clock;PPN;R11",
            ";".join(str(path) for path in [SRC_1046_QBAR, SRC_1046_FORBIDDEN, SRC_2956_QBAR]),
            "MISSING_COMPONENT_VALUES",
        ),
        (
            "COMP2957_6_qbar_constants_abs",
            "qbar_constants_abs",
            "no-cancellation envelope for constant-sector contribution",
            "|qbar_constants| <= |s_alpha b_alpha| + sum_A |s_mA b_mA| + sum_i |s_clock_i b_clock_i|",
            "dimensionless",
            "clock;EM;WEP;spectra",
            str(SRC_1046_CONSTANTS),
            "MISSING_CONSTANT_COMPONENT_VALUES",
        ),
    ]
    return [
        add_common(
            {
                "component_id": component_id,
                "symbol": symbol,
                "definition": definition,
                "formula_or_bound": formula,
                "units": units,
                "observable_links": links,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "current_value": value,
                "theorem_zero_status": "NOT_DERIVED",
                "numeric_value_status": "NOT_SOURCED",
                "no_cancellation_policy": True,
                "accepted_for_scoring": False,
            }
        )
        for component_id, symbol, definition, formula, units, links, source_path, value in rows
    ]


def first_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FIRST2957_0_b_conf",
            "b_conf",
            "selected_first_component",
            "universal conformal hidden-frame coefficient is the cleanest first target: theorem-zero follows from single observed frame/no-shadow action domain, while a finite value immediately feeds R10/WEP/clock/PPN.",
            "dimensionless",
            ";".join(str(path) for path in [SRC_1046_QBAR, SRC_1046_NOSHADOW, SRC_1046_FORBIDDEN, SRC_2659_HOM]),
            "MISSING_B_CONF_VALUE_OR_PARENT_NO_SHADOW_THEOREM",
            "prove b_conf=0 from parent action domain, else source a nonclaim absolute bound with declared arena projections",
        ),
        (
            "FIRST2957_1_b_marker",
            "b_marker",
            "second_component_if_b_conf_stalls",
            "material marker is the dangerous composition/source route; it needs either a no-marker domain theorem or sourced material sensitivity rows.",
            "dimensionless_after_sensitivity_normalization",
            ";".join(str(path) for path in [SRC_1046_QBAR, SRC_1046_MARKER, SRC_980_FUNCTOR, SRC_974_COUNTER]),
            "MISSING_B_MARKER_VALUES_OR_NO_MARKER_THEOREM",
            "prove co-moving markers cannot extend the quotient, else source material-pair nonclaim sensitivities",
        ),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "priority": priority,
                "why_this_row": why,
                "units": units,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "numeric_or_theorem_value": value,
                "next_action": action,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, priority, why, units, source_path, value, action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2957_0_no_hidden_visible_hom", "parent no-hidden-visible-hom theorem", False, "DOMAIN_SIGNATURES_UNSIGNED"),
        ("CG2957_1_no_shadow_frame", "b_conf=b_dis=0 no-shadow-frame theorem", False, "NO_EXTRA_FRAME_SLOT_NOT_PARENT_SIGNED"),
        ("CG2957_2_no_marker", "b_marker=0 no-material-marker theorem", False, "COUNTEREXAMPLES_SURVIVE"),
        ("CG2957_3_constant_superselection", "b_alpha=b_mass=b_clock=0", False, "CONSTANT_MARKER_SUPERSELECTION_NOT_SIGNED"),
        ("CG2957_4_component_bounds", "component rows numeric/source-backed", False, "COMPONENT_VALUES_MISSING"),
        ("CG2957_5_qbarXT_zero", "qbar_XT=0 theorem-zero", False, "HIDDEN_MARKER_COMPONENTS_OPEN"),
        ("CG2957_6_R10_WEP_PPN_clock", "local arena scoring allowed", False, "MTS_SIDE_COEFFICIENTS_NONCLAIM"),
        ("CG2957_7_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2957_8_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
            "DEC2957_0_result",
            "no-hidden-visible-hom theorem is not derived",
            "the chain-rule zero is exact only after the parent ordinary-matter domain is signed; current corpus still permits hidden frame, material marker and constant-sector countermodels",
            "keep b_conf, b_dis, b_marker, b_alpha and mass/clock rows live",
        ),
        (
            "DEC2957_1_good_news",
            "the proof target is now sharply finite",
            "if ordinary matter is typed as q-pulled visible data plus fixed representation constants, every vertical derivative in this channel vanishes by chain rule",
            "attack the action-domain typing rather than inventing new phenomenology",
        ),
        (
            "DEC2957_2_fallback",
            "first component rows are explicit and nonclaim",
            "b_conf is the least messy first row; b_marker is the dangerous material/source route if b_conf stalls",
            "source theorem-zero or numeric bounds before any arena score",
        ),
        (
            "DEC2957_3_next",
            "next target should go after b_conf/b_marker directly",
            "this is the narrowest coupling bottleneck left by 2956/2957 and sits directly between MTS and local GR/PPN/R10 tests",
            "build 2958 b_conf/b_marker bound row or hidden-domain theorem",
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
                "next_id": "NEXT2957_0_2958",
                "priority": "selected_primary",
                "next_doc": "2958-Y5-R2FR-b-conf-b-marker-bound-row-or-hidden-domain-theorem-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_b_conf_b_marker_bound_row_or_hidden_domain_theorem_under_AX1090_2958.py",
                "objective": "Try to prove b_conf=0 from a parent single-observed-frame/no-shadow action-domain theorem, then try b_marker=0 from a no-material-marker domain theorem. If either theorem remains unsigned, fill source-ready nonclaim component-bound rows with units, source paths, arena projections and no-cancellation policy.",
                "include": "b_conf;b_marker;single observed frame;ordinary matter domain;co-moving marker obstruction;R10/WEP/clock/PPN arena projections;units;source paths",
                "exclude": "quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("hom_copy", OUTPUTS["hom"], BRANCH_OUTPUTS["hom_copy"]),
        ("component_copy", OUTPUTS["components"], BRANCH_OUTPUTS["component_copy"]),
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
        ("VAL2957_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2957_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2957_2_hom_blocked", any(row["gate_id"] == "HOM2957_7_verdict" and row["theorem_zero_credit"] is False for row in all_rows["hom"]), "no-hidden-visible-hom verdict remains blocked", True),
        ("VAL2957_3_components_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["components"]), "component rows remain nonclaim", True),
        ("VAL2957_4_component_paths_exist", all(row["source_path_exists"] is True for row in all_rows["components"]), "component rows cite existing paths", True),
        ("VAL2957_5_first_rows_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False and row["source_path_exists"] is True for row in all_rows["first"]), "first component rows are nonclaim with existing paths", True),
        ("VAL2957_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2957_7_next_target_written", any(row["next_id"] == "NEXT2957_0_2958" for row in all_rows["next"]), "2958 next target selected", True),
        ("VAL2957_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2957_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2957_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2957_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2957 outputs were written to formalization-workbench", True),
        ("VAL2957_12_doc_written", DOC.exists(), "2957 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2957_OVERALL", "passed": overall, "check": "2957 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2957 - Y5 R2FR: hidden-frame marker coefficient or no-hidden-visible-hom theorem under AX1090

Status: `Y5_R2FR_2957_no_hidden_visible_hom_not_derived_marker_component_rows_emitted_nonclaim`

Claim ceiling: `no_no_hidden_visible_hom_no_no_shadow_frame_no_marker_zero_no_constant_superselection_no_qbarXT_zero_no_R10_WEP_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2957 asks whether the surviving hidden-frame/material-marker coupling can be erased by a parent domain theorem instead of being fitted as a residual. The result is:

- The exact chain-rule route is real: if ordinary matter coefficients are only `q`-pulled visible data plus fixed representation constants, their vertical derivatives vanish.
- The parent domain theorem is not yet signed: visible coefficient algebra, ordinary matter functor domain, frame-slot exclusion, constant superselection, marker exclusion, and boundary/readout silence are still open.
- Therefore `b_conf`, `b_dis`, `b_marker`, `b_alpha`, and mass/clock marker coefficients remain live nonclaim rows.
- The best next attack is narrow: prove `b_conf=0` by a single-observed-frame/no-shadow parent action-domain theorem, then attack `b_marker=0`; otherwise source component bounds.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## No-Hidden-Visible-Hom Gate

{md_table(all_rows["hom"], ["gate_id", "object", "current_status", "conditional_math_available", "parent_signed", "theorem_zero_credit", "evidence_summary"])}

## Marker Coefficient Component Rows

{md_table(all_rows["components"], ["component_id", "symbol", "current_value", "units", "source_path_exists", "accepted_for_scoring", "observable_links"])}

## First Component Bound Rows

{md_table(all_rows["first"], ["row_id", "symbol", "priority", "numeric_or_theorem_value", "units", "source_path_exists", "next_action"])}

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
        "hom": hom_gate_rows(),
        "components": component_rows(),
        "first": first_bound_rows(),
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

    print(f"2957 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
