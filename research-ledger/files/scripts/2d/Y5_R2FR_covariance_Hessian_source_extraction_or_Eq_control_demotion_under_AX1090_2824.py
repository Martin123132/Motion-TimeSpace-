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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2824-Y5-R2FR-covariance-Hessian-source-extraction-or-Eq-control-demotion-under-AX1090.md"

SRC_2823_NEXT = RESIDUALS / "P8_Y5_R2FR_2823_NEXT_TARGET.csv"
SRC_2823_DECISION = RESIDUALS / "P8_Y5_R2FR_2823_DECISION_LEDGER.csv"
SRC_2823_CARRIER = RESIDUALS / "P8_Y5_R2FR_2823_EQ_CARRIER_CANDIDATE_AUDIT.csv"
SRC_2823_CONDITIONAL = RESIDUALS / "P8_Y5_R2FR_2823_COVARIANCE_HESSIAN_CONDITIONAL_EQ_ROW.csv"
SRC_2823_UNITS = RESIDUALS / "P8_Y5_R2FR_2823_Q_NORMALIZATION_AND_DUAL_UNITS_GATE.csv"
SRC_2823_IMPACT = RESIDUALS / "P8_Y5_R2FR_2823_COMPONENT_ROW_REENTRY_IMPACT.csv"
SRC_2270_MAP = RESIDUALS / "P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv"
SRC_2271_PULLBACK = RESIDUALS / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv"
SRC_2271_HESSIAN = RESIDUALS / "P8_Y5_PARENT_QLOC_2271_HESSIAN_SOURCE_LEDGER.csv"
SRC_2273_SMOOTH = RESIDUALS / "P8_Y5_PARENT_QLOC_2273_SMOOTHING_HODGE_PROJECTION_GATE.csv"
SRC_2276_WKB = RESIDUALS / "P8_Y5_PARENT_QLOC_2276_WKB_COVARIANCE_DERIVATION.csv"
SRC_2281_STIFFNESS = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_Q_STIFFNESS_DERIVATION_AUDIT.csv"
SRC_2281_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_COVARIANCE_MANIFOLD_SELECTOR_GAP.csv"
SRC_2282_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2282_SELECTOR_ROUTE_AUDIT.csv"
SRC_2282_INPUTS = RESIDUALS / "P8_Y5_PARENT_QLOC_2282_PARENT_SELECTOR_INPUT_CONTRACT.csv"
SRC_2282_CLOSURE = RESIDUALS / "P8_Y5_PARENT_QLOC_2282_Q_CLOSURE_DECLARATION.csv"
SRC_2287_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2287_Q_SECTOR_SELECTOR_AUDIT.csv"
SRC_2315_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2315_SELECTOR_REENTRY_AUDIT.csv"
SRC_2342_SOURCE = RESIDUALS / "P8_Y5_PARENT_QLOC_2342_SELECTOR_SOURCE_MEASURE_CONTRACT.csv"
SRC_2359_NOPOLE = RESIDUALS / "P8_Y5_PARENT_QLOC_2359_NOPOLE_SELECTOR_GATE.csv"
SRC_1843_BOUNDARY = RESIDUALS / "P8_Y5_PARENT_QLOC_1843_BOUNDARY_DOMAIN_CERTIFICATE.csv"
SRC_2152_BOUNDARY = RESIDUALS / "P8_Y5_PARENT_QLOC_2152_BOUNDARY_DOMAIN_CERTIFICATE.csv"
SRC_2411_LEMMAS = RESIDUALS / "P8_Y5_PARENT_QLOC_2411_HESSIAN_RANGE_SOURCE_LEMMAS.csv"
SRC_2106_HESSIAN = RESIDUALS / "P8_Y5_PARENT_QLOC_2106_HESSIAN_SOURCE_ATTEMPT.csv"
SRC_2755_PACK = RESIDUALS / "P8_Y5_R2FR_2755_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv"
SRC_2756_PACK = RESIDUALS / "P8_Y5_R2FR_2756_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2824_SOURCE_REGISTER.csv",
    "extraction": RESIDUALS / "P8_Y5_R2FR_2824_COVARIANCE_HESSIAN_SOURCE_EXTRACTION_STATUS.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2824_EQ_CONTROL_ONLY_DEMOTION_LEDGER.csv",
    "runner_contract": RESIDUALS / "P8_Y5_R2FR_2824_CONTROL_ONLY_LOCAL_LOCK_RUNNER_CONTRACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2824_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2824_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2824_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2824_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2824_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "demotion_copy": SOURCE_WEIGHT / "Eq_control_only_demotion_2824_NONCLAIM.csv",
    "local_runner_copy": LOCAL_BOUNDS / "Eq_control_only_local_lock_runner_contract_2824_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2824_CONTROL_ONLY_LOCAL_LOCK_SMOKE_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_COVARIANCE_HESSIAN_SOURCE_EXTRACTION_2824"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2824_0_2823_next", SRC_2823_NEXT, "NEXT2823_0_2824", "2823 handoff to covariance-Hessian source extraction"),
        ("SRC2824_1_2823_decision", SRC_2823_DECISION, "DEC2823_3_next", "carrier source extraction decision"),
        ("SRC2824_2_2823_carrier", SRC_2823_CARRIER, "EQA2823_0_covariance_hessian;EQA2823_6_verdict", "conditional carrier and no parent promotion"),
        ("SRC2824_3_2823_conditional", SRC_2823_CONDITIONAL, "CCR2823_1_Mq2;CCR2823_2_Zq;CCR2823_4_Eq_form", "conditional carrier rows"),
        ("SRC2824_4_2823_units", SRC_2823_UNITS, "QNG2823_2_Eq_units;QNG2823_6_Newton_source", "q units and Newton source debt"),
        ("SRC2824_5_2823_impact", SRC_2823_IMPACT, "RI2823_4_Nlock;RI2823_5_claims", "reentry still blocked"),
        ("SRC2824_6_2270_map", SRC_2270_MAP, "PCM2270_2_q_zero_condition;PCM2270_3_current_corpus", "psi covariance to q map"),
        ("SRC2824_7_2271_pullback", SRC_2271_PULLBACK, "PBF2271_1_q_tangent;PBF2271_3_q_zero_channel_relation", "covariance pullback formulas"),
        ("SRC2824_8_2271_hessian", SRC_2271_HESSIAN, "HSL2271_0_MR2_definition;HSL2271_3_absence_switch", "Hessian source ledger"),
        ("SRC2824_9_2273_smoothing", SRC_2273_SMOOTH, "SHP2273_0_hodge_projection;SHP2273_2_kernel_annihilation", "smoothing/Hodge projection gate"),
        ("SRC2824_10_2276_wkb", SRC_2276_WKB, "WKB2276_2_smoothed_covariance;WKB2276_4_residual_size", "WKB covariance derivation"),
        ("SRC2824_11_2281_stiffness", SRC_2281_STIFFNESS, "QSD2281_2_transverse_q_mass;QSD2281_4_operator", "conditional Hessian derivation"),
        ("SRC2824_12_2281_selector", SRC_2281_SELECTOR, "CSG2281_1_metric_compatibility;CSG2281_4_direct_penalty", "selector gap"),
        ("SRC2824_13_2282_selector", SRC_2282_SELECTOR, "SEL2282_1_metric_compatibility;SEL2282_6_direct_q_penalty", "selector route audit"),
        ("SRC2824_14_2282_inputs", SRC_2282_INPUTS, "PIC2282_0_cell_current;PIC2282_4_source_map", "selector input contract"),
        ("SRC2824_15_2282_closure", SRC_2282_CLOSURE, "QCD2282_0_status;QCD2282_1_equivalence_gain", "closure declaration"),
        ("SRC2824_16_2287_selector", SRC_2287_SELECTOR, "SEL2287_0_constraint_zero;SEL2287_4_boundary_nohair", "q-sector selector audit"),
        ("SRC2824_17_2315_selector", SRC_2315_SELECTOR, "SEL2315_4_verdict", "selector reentry audit"),
        ("SRC2824_18_2342_source", SRC_2342_SOURCE, "SSC2342_2_Hilbert;SSC2342_4_universal_G", "source-measure/Newton normalization contract"),
        ("SRC2824_19_2359_nopole", SRC_2359_NOPOLE, "NPS2359_0_second_class_auxiliary;NPS2359_2_positive_nohair", "no-pole selector gate"),
        ("SRC2824_20_1843_boundary", SRC_1843_BOUNDARY, "BDC1843_0_surface_manifold;BDC1843_5_verdict", "boundary-domain certificate"),
        ("SRC2824_21_2152_boundary", SRC_2152_BOUNDARY, "BDC2152_0_surface_manifold;BDC2152_5_verdict", "later boundary-domain certificate"),
        ("SRC2824_22_2411_lemmas", SRC_2411_LEMMAS, "LEM2411_0_hessian_not_range;LEM2411_4_verdict", "Hessian/range gate lemmas"),
        ("SRC2824_23_2106_hessian", SRC_2106_HESSIAN, "HSA2106_1_ZX;HSA2106_6_verdict", "prior finite Hessian source attempt"),
        ("SRC2824_24_2755_pack", SRC_2755_PACK, "IQH2755_0_Zq;IQH2755_5_claim_gate", "R2FR q Hessian source pack"),
        ("SRC2824_25_2756_pack", SRC_2756_PACK, "FB2756_1_Zq;FB2756_8_score_gate", "R2FR q-removal/Hessian fallback pack"),
    ]
    return [source_row(*spec) for spec in specs]


def extraction_rows() -> list[dict[str, Any]]:
    specs = [
        ("EXT2824_0_q_map", "q map", "q=ln(AB) or covariance-channel q", "FORMAL_MAP_SHAPE_AVAILABLE", "sign/frame/areal and parent covariance normalization are not fully signed", SRC_2270_MAP, "PCM2270_0_covariance_definition", False),
        ("EXT2824_1_q_tangent", "n_q=dq/dC", "partial_q C_tt=-A/2, partial_q C_rr=B/2", "EXACT_TANGENT_AVAILABLE", "usable for conditional Hessian projection only", SRC_2271_PULLBACK, "PBF2271_1_q_tangent", False),
        ("EXT2824_2_HAB", "H_AB", "positive covariance Hessian around equilibrium", "MISSING_EFFECTIVE_ACTION_AND_LIFT", "effective action Gamma, psi lift delta_q psi, units, background Phi, density convention missing", SRC_2271_HESSIAN, "HSL2271_0_MR2_definition", False),
        ("EXT2824_3_Mq2", "M_q^2", "n_q^A H_AB n_q^B", "CONDITIONAL_NOT_SOURCED", "depends on H_AB and parent-selected q=0 equilibrium", SRC_2281_STIFFNESS, "QSD2281_2_transverse_q_mass", False),
        ("EXT2824_4_xiq", "xi_q", "smoothing/correlation length", "BOUND_TEMPLATE_NOT_NUMERIC", "WKB residual and smoothing leakage have no numeric/source-backed scale", SRC_2276_WKB, "WKB2276_4_residual_size", False),
        ("EXT2824_5_Zq", "Z_q", "xi_q^2 n_q^A H_AB n_q^B", "CONDITIONAL_NOT_SOURCED", "requires H_AB and xi_q in one normalization", SRC_2281_STIFFNESS, "QSD2281_3_gradient_expansion", False),
        ("EXT2824_6_selector", "q=0 selector", "q=0 iff radial observer-cell reciprocity", "CLOSURE_NOT_PARENT_DERIVED", "selector routes remain unsigned or circular", SRC_2282_SELECTOR, "SEL2282_1_metric_compatibility", False),
        ("EXT2824_7_boundary", "boundary/domain class", "boundary terms vanish or are bounded", "FAIL_CURRENT_CLAIM", "one parent boundary class/corner/cohomology/kernel certificate missing", SRC_2152_BOUNDARY, "BDC2152_5_verdict", False),
        ("EXT2824_8_Newton_source", "Newton/source normalization", "same source recovers Newtonian mechanics and measured GM", "MISSING_SOURCE_MEASURE_EQUALITY", "Hilbert/source equality, Poisson/Gauss bridge, and universal G not signed", SRC_2342_SOURCE, "SSC2342_2_Hilbert", False),
        ("EXT2824_9_verdict", "claim-grade E_q source", "all carrier inputs source-backed in one branch", "NOT_EXTRACTED_CONTROL_ONLY", "at least one required object remains missing in every route", SRC_2823_CARRIER, "EQA2823_6_verdict", False),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "extraction_id": extraction_id,
                "input": obj,
                "formula_or_requirement": formula,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "parent_signed": parent_signed,
                "numeric_value_present": False,
                "source_backed": False,
            }
        )
        for extraction_id, obj, formula, status, blocker, source_path, anchor, parent_signed in specs
    ]


def demotion_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEM2824_0_control_carrier", "E_q carrier", "CONTROL_ONLY_CONDITIONAL", "covariance-Hessian carrier may organize nonclaim rows, not claims"),
        ("DEM2824_1_no_component_claim", "J_q component rows", "CONTROL_ONLY", "component bounds cannot be interpreted as predictions until E_q is parent-signed"),
        ("DEM2824_2_no_Nlock", "2818 N_lock", "NO_REENTRY", "T_source_norm and C_qm remain uncomputable"),
        ("DEM2824_3_no_R10_PPN", "R10/PPN/clock/orbital", "NO_SCORE", "arena projection requires source-backed carrier and source vector"),
        ("DEM2824_4_no_GR_Newton", "local GR/Newton", "NO_DERIVATION_CLAIM", "q=0 selector and Newton source normalization are still missing"),
        ("DEM2824_5_allowed_use", "allowed use", "PRIVATE_SMOKE_AND_BOOKKEEPING_ONLY", "can test pipeline sensitivity and expose which inputs matter"),
    ]
    return [
        nonclaim(
            {
                "demotion_id": demotion_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "control_only": True,
                "claim_use_forbidden": True,
            }
        )
        for demotion_id, obj, status, reason in specs
    ]


def runner_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2824_0_inputs", "control inputs", "H_AB_shape, xi_q_placeholder, q_units_flag, selector_flag, boundary_flag, component_bounds", "all placeholders/nonclaim unless source-backed", "never claim"),
        ("RUN2824_1_operator", "operator form", "L_q=-div(Z_q grad)+M_q^2 with Z_q=xi_q^2 M_q^2 conditionally", "conditional covariance-Hessian form only", "no range claim"),
        ("RUN2824_2_source_vector", "J_q components", "j_matter, j_const, j_weight, j_shadow, j_readout, j_boundary, j_curvature", "component vector from 2822, all nonclaim", "no cancellation"),
        ("RUN2824_3_outputs", "private outputs", "T_source_norm_placeholder, C_qm_placeholder, S_cg_control, N_lock_control", "diagnostic only", "no score_ready flags"),
        ("RUN2824_4_acceptance", "future promotion", "all carrier/source/boundary/selector rows source-backed or theorem-zero in one branch", "required before any arena score", "block claims otherwise"),
    ]
    return [
        nonclaim(
            {
                "contract_id": contract_id,
                "object": obj,
                "formula_or_fields": formula,
                "status": status,
                "claim_policy": policy,
                "control_only": True,
            }
        )
        for contract_id, obj, formula, status, policy in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    all_inputs_signed = all(row["parent_signed"] and row["source_backed"] for row in rows["extraction"] if row["extraction_id"] != "EXT2824_9_verdict")
    any_numeric = any(row["numeric_value_present"] for row in rows["extraction"])
    demoted = all(row["control_only"] and row["claim_use_forbidden"] for row in rows["demotion"])
    specs = [
        ("CG2824_0_sources", "source anchors present", sources_ok, "all imported source-extraction ledgers are reproducible"),
        ("CG2824_1_HAB", "H_AB source-backed", False, "effective action and q-lift missing"),
        ("CG2824_2_xiq", "xi_q source-backed", False, "smoothing/correlation scale is template-only"),
        ("CG2824_3_selector", "q=0 selector parent-signed", False, "selector remains closure/target not derivation"),
        ("CG2824_4_boundary", "boundary/domain parent class signed", False, "boundary certificate fails current claim"),
        ("CG2824_5_all_inputs", "all E_q carrier inputs accepted in one branch", all_inputs_signed and any_numeric, "no numeric/source-backed carrier extraction"),
        ("CG2824_6_control_demotion", "E_q demoted to control-only", demoted, "safe nonclaim path selected"),
        ("CG2824_7_local_claim", "local GR/Newton/PPN/R10 claim allowed", False, "control-only carrier cannot support claims"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2824_0_extraction", "Covariance-Hessian source extraction did not close.", "NO_PARENT_SOURCE_ROW", "H_AB, xi_q, q=0 selector, q units, boundary/domain, and Newton source normalization remain unsigned", "do not feed E_q into claims"),
        ("DEC2824_1_gain", "The conditional carrier remains valuable.", "CONTROL_SHAPE_RETAINED", "it gives a coherent diagnostic operator and range relation without hand-inserting G_AB/mu_q", "use as private smoke/control scaffold"),
        ("DEC2824_2_demotion", "E_q is demoted to explicit control-only status.", "CONTROL_ONLY_DEMOTION", "this prevents component rows from masquerading as predictions", "build only nonclaim runner rows"),
        ("DEC2824_3_next", "Next target is a control-only local-lock smoke runner.", "NEXT_2825_CONTROL_RUNNER", "a runner can test sensitivity and reveal which sourced inputs would matter, while all claim gates remain false", "write dry-run nonclaim runner contract and placeholder data schema"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2824_0_2825",
                "status": "selected_primary",
                "target_doc": "2825-Y5-R2FR-Eq-control-only-local-lock-smoke-runner-and-source-input-schema-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Eq_control_only_local_lock_smoke_runner_and_source_input_schema_under_AX1090_2825.py",
                "mission": "build a nonclaim control-only runner/schema using the conditional covariance-Hessian E_q carrier, J_q component placeholders, and local-lock amplitude chain to expose sensitivity without claiming local GR/Newton/PPN/R10",
                "acceptance": "runner/schema parses, all placeholders valid_for_claim=false, no score_ready flags, and promotion requires source-backed H_AB, xi_q, selector, boundary/domain, J_q components, and Dq[v_m]",
                "forbidden": "do not treat control outputs as predictions; do not insert carrier/source coefficients by hand; do not claim local GR/Newton/PPN/R10; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2824_0_demotion_copy", OUTPUTS["demotion"], BRANCH_OUTPUTS["demotion_copy"], "source-weight copy of E_q control-only demotion"),
        ("BR2824_1_runner_copy", OUTPUTS["runner_contract"], BRANCH_OUTPUTS["local_runner_copy"], "local-bound copy of control-only runner contract"),
        ("BR2824_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for control-only local-lock smoke runner"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2824_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2824_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2824_2_no_parent_source", not any(row["parent_signed"] and row["source_backed"] for row in rows_by_name["extraction"]), "no parent-signed/source-backed carrier input was extracted"),
        ("VAL2824_3_no_numeric_values", not any(row["numeric_value_present"] for row in rows_by_name["extraction"]), "no numeric carrier coefficient values were introduced"),
        ("VAL2824_4_control_demotion", all(row["control_only"] for row in rows_by_name["demotion"]), "E_q was demoted to control-only status"),
        ("VAL2824_5_runner_nonclaim", all(row["control_only"] for row in rows_by_name["runner_contract"]), "control-only runner contract is nonclaim"),
        ("VAL2824_6_next_target_2825", any(row["next_id"] == "NEXT2824_0_2825" and row["selected"] for row in rows_by_name["next"]), "control-only local-lock smoke runner selected next"),
        ("VAL2824_7_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2824_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2824_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2824_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2824_11_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2824_12_generated_under_post_checkpoint", all(str(path).startswith(str(ROOT)) for path in output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2824_13_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2824_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2824_OVERALL",
            "passed": overall,
            "detail": "2824 attempts covariance-Hessian source extraction, finds no parent-signed/numeric carrier inputs, demotes E_q to explicit control-only status, and selects a nonclaim local-lock smoke runner/schema next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2824 - Y5 R2FR Covariance Hessian Source Extraction Or Eq Control Demotion Under AX1090

Status: `Y5_R2FR_2824_covariance_Hessian_source_not_extracted_Eq_control_only_demoted`

## Private Verdict

2824 tries to turn the conditional covariance-Hessian carrier into a sourced `E_q`. It does not close.

The useful structure remains:

`E_q[delta q]^2 = int_W (Z_q |nabla delta q|^2 + M_q^2 delta q^2) dV_e`

with `M_q^2` and `Z_q` conditionally projected from a covariance Hessian. But the source hunt does not supply the claim-grade inputs: parent effective action/Hessian `H_AB`, `xi_q`, q-normalization, q=0 selector, boundary/domain class, or Newton/source normalization.

Therefore `E_q` is explicitly demoted to a control-only carrier. It may be used for private smoke tests and bookkeeping, but not for claims, scores, or local-lock reentry.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Covariance Hessian Source Extraction Status

{markdown_table(rows["extraction"], ["extraction_id", "input", "status", "blocker", "parent_signed", "numeric_value_present", "source_backed", "valid_for_claim"])}

## Eq Control Only Demotion Ledger

{markdown_table(rows["demotion"], ["demotion_id", "object", "status", "reason", "control_only", "claim_use_forbidden", "valid_for_claim"])}

## Control Only Local Lock Runner Contract

{markdown_table(rows["runner_contract"], ["contract_id", "object", "status", "formula_or_fields", "claim_policy", "control_only", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["extraction"] = extraction_rows()
    rows["demotion"] = demotion_rows()
    rows["runner_contract"] = runner_contract_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "extraction", "demotion", "runner_contract", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2824_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2824_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
