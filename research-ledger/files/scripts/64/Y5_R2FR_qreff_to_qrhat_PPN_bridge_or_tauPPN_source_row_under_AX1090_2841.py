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
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2841-Y5-R2FR-qreff-to-qrhat-PPN-bridge-or-tauPPN-source-row-under-AX1090.md"

SRC_2840_NEXT = RESIDUALS / "P8_Y5_R2FR_2840_NEXT_TARGET.csv"
SRC_2840_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2840_QREFF_TO_QRHAT_PPN_BRIDGE_AUDIT.csv"
SRC_2840_PACK = RESIDUALS / "P8_Y5_R2FR_2840_FIRST_PACK_FILL_ATTEMPT_NONCLAIM.csv"
SRC_2840_ACCEPT = RESIDUALS / "P8_Y5_R2FR_2840_PACK_ACCEPTANCE_VALIDATOR.csv"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_DIM = RESIDUALS / "P8_Y5_R2FR_2839_DIMENSIONAL_CONTRACT.csv"
SRC_2832_GAMMA = RESIDUALS / "P8_Y5_R2FR_2832_GAMMA_COMBO_ALGEBRA_LEDGER.csv"
SRC_1884 = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_2489 = ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2841_SOURCE_REGISTER.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_2841_QREFF_TO_QRHAT_CONDITIONAL_BRIDGE.csv",
    "conditions": RESIDUALS / "P8_Y5_R2FR_2841_PPN_BRIDGE_CONDITIONS.csv",
    "formula": RESIDUALS / "P8_Y5_R2FR_2841_PPN_FORMULA_PACK_NONCLAIM.csv",
    "tau_row": RESIDUALS / "P8_Y5_R2FR_2841_TAUPPN_SOURCE_ROW_REQUIREMENT.csv",
    "vector_guard": RESIDUALS / "P8_Y5_R2FR_2841_FULL_VECTOR_GUARD.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2841_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2841_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2841_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2841_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2841_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "bridge_copy": LOCAL_BOUNDS / "RAB_qreff_to_qrhat_conditional_bridge_2841_NONCLAIM.csv",
    "formula_copy": SOURCE_WEIGHT / "RAB_PPN_formula_pack_2841_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2841_PPN_bridge_conditions_or_tauPPN_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_QREFF_TO_QRHAT_PPN_BRIDGE_2841_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
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
        ("SRC2841_0_2840_next", SRC_2840_NEXT, "NEXT2840_0_2841", "2840 selected q_R_eff to q_R_hat bridge"),
        ("SRC2841_1_2840_bridge", SRC_2840_BRIDGE, "PPNB2840_1_existing_qRhat_bridge;PPNB2840_2_missing_kernel_to_ppn", "2840 bridge audit"),
        ("SRC2841_2_2840_pack", SRC_2840_PACK, "FILL2840_0_first_RAB_finite_pack;MISSING_QREFF_TO_QRHAT_MAP", "2840 pack fill attempt"),
        ("SRC2841_3_2840_accept", SRC_2840_ACCEPT, "ACC2840_OVERALL", "2840 acceptance validator"),
        ("SRC2841_4_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_4_compact_body", "finite compact kernel"),
        ("SRC2841_5_2839_dimensions", SRC_2839_DIM, "DIM2839_0_RAB;DIM2839_3_point_charge", "q_R_eff unit contract"),
        ("SRC2841_6_2832_gamma", SRC_2832_GAMMA, "ALG2832_0_combo;ALG2832_3_qRhat_bridge;ALG2832_5_total_abs_guard", "current gamma combo and q_R_hat bridge"),
        ("SRC2841_7_1884", SRC_1884, "NBC1884_3_qRhat_bridge;q_R_hat=Q_R c^2/(G M_source);delta_p=-q_R_hat/2", "original Q_R to q_R_hat convention"),
        ("SRC2841_8_2489", SRC_2489, "PPNK2489_1_CR_delta_p_combo_kernel;PPNV2489_7_total_abs", "PPN response kernel and full-vector guard"),
        ("SRC2841_9_2631", SRC_2631, "PPNV2631_0_delta_p_qR;PPNV2631_8_total_abs", "current full PPN vector"),
    ]
    return [source_row(*spec) for spec in specs]


def bridge_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BRG2841_0_kernel_exterior",
            "delta_R(r)=sigma_R*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R",
            "from 2839 compact-body finite kernel",
            "DERIVED_SYMBOLIC",
            "requires boundary class H_R and sign sigma_R",
        ),
        (
            "BRG2841_1_ppn_long_range_limit",
            "if r_PPN/ell_R << 1 and H_R=0, then delta_R(r)=sigma_R*q_R_eff/(4*pi*r)+O(r/ell_R)",
            "PPN 1/r matching is only valid in the long-range/asymptotic regime",
            "DERIVED_CONDITIONAL",
            "finite-range case is not a standard constant PPN delta_p",
        ),
        (
            "BRG2841_2_identify_CR",
            "if C_R=delta_R in the same measured-GM/coframe convention, compare to C_R=-Q_R/r",
            "identifies the finite Green amplitude with the old reciprocal exterior charge",
            "CONDITIONAL_MATCH",
            "C_R=delta_R and measured-GM convention are not signed",
        ),
        (
            "BRG2841_3_charge_map",
            "Q_R=-sigma_R*q_R_eff/(4*pi)",
            "coefficient match between delta_R=sigma_R*q_R_eff/(4*pi*r) and C_R=-Q_R/r",
            "DERIVED_IF_MATCH_CONDITIONS_HOLD",
            "sign and 4*pi normalization must be carried explicitly",
        ),
        (
            "BRG2841_4_qRhat_map",
            "q_R_hat=-sigma_R*q_R_eff*c^2/(4*pi*G*M_source)",
            "uses 1884 convention q_R_hat=Q_R*c^2/(G*M_source)",
            "DERIVED_IF_MATCH_CONDITIONS_HOLD",
            "requires source mass convention and q_R_eff source value",
        ),
        (
            "BRG2841_5_delta_p_map",
            "delta_p=sigma_R*q_R_eff*c^2/(8*pi*G*M_source)",
            "uses delta_p=-q_R_hat/2",
            "DERIVED_IF_MATCH_CONDITIONS_HOLD",
            "does not score without b_R, full-vector closure and source-backed q_R_eff",
        ),
    ]
    return [
        nonclaim(
            {
                "bridge_id": row_id,
                "statement": statement,
                "role": role,
                "status": status,
                "condition_or_blocker": blocker,
                "bridge_closed_for_claim": False,
                "control_only": True,
            }
        )
        for row_id, statement, role, status, blocker in specs
    ]


def condition_rows() -> list[dict[str, Any]]:
    specs = [
        ("COND2841_0_CR_deltaR", "C_R=delta_R in the same observed coframe/readout", "MISSING_COFAME_CONVENTION", "needed before matching to 1884 C_R=-Q_R/r"),
        ("COND2841_1_boundary", "H_R=0 or bounded no-hair boundary homogeneous mode", "MISSING_BOUNDARY_CLASS", "otherwise the 1/r coefficient is not the full exterior profile"),
        ("COND2841_2_long_range", "r_PPN/ell_R << 1 over the tested solar-system domain", "MISSING_ELL_R_VALUE", "otherwise finite-range profile is not a constant PPN parameter"),
        ("COND2841_3_sign", "sigma_R source sign convention fixed", "MISSING_SOURCE_SIGN", "needed to decide sign of q_R_hat and delta_p"),
        ("COND2841_4_GM", "M_source is the same measured GM convention used by PPN U=GM/r", "MISSING_MEASURED_GM_CONVENTION", "prevents fitted-GM absorption or wrong mass normalization"),
        ("COND2841_5_bR", "b_R zero/value and denominator guard supplied", "MISSING_b_R_VALUE_OR_ZERO", "gamma combo still depends on b_R"),
        ("COND2841_6_full_vector", "beta/preferred/source/endpoint/readout components zeroed or bounded", "MISSING_FULL_VECTOR_CLOSURE", "gamma bridge alone is not local GR"),
    ]
    return [
        nonclaim(
            {
                "condition_id": row_id,
                "condition": condition,
                "current_status": status,
                "why_required": why,
                "condition_closed": False,
                "control_only": True,
            }
        )
        for row_id, condition, status, why in specs
    ]


def formula_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FORM2841_0_qRhat",
            "q_R_hat=-sigma_R*q_R_eff*c^2/(4*pi*G*M_source)",
            "conditional q_R_eff to q_R_hat map",
            "FORMAL_CONDITIONAL_NONCLAIM",
            "requires all COND2841 rows",
        ),
        (
            "FORM2841_1_delta_p",
            "delta_p=sigma_R*q_R_eff*c^2/(8*pi*G*M_source)",
            "conditional q_R_eff to delta_p map",
            "FORMAL_CONDITIONAL_NONCLAIM",
            "inherits q_R_hat bridge and sign convention",
        ),
        (
            "FORM2841_2_gamma_combo",
            "gamma_obs-1 = delta_p*(1+4*b_R)/(1-2*b_R*delta_p)",
            "current branch gamma response after inserting delta_p",
            "FORMAL_CONDITIONAL_NONCLAIM",
            "needs b_R and denominator guard",
        ),
        (
            "FORM2841_3_gamma_bR_zero_limit",
            "if b_R=0, gamma_obs-1=delta_p=sigma_R*q_R_eff*c^2/(8*pi*G*M_source)",
            "clean special case but still not local GR",
            "FORMAL_LIMIT_NONCLAIM",
            "requires b_R theorem-zero and full-vector closure",
        ),
        (
            "FORM2841_4_finite_range_warning",
            "if r_PPN/ell_R is not small, replace constant delta_p by a radial profile tau_PPN(r)",
            "finite-range branch becomes profile testing, not ordinary PPN",
            "ROUTE_SPLIT_NONCLAIM",
            "requires tau_PPN source/projection row",
        ),
    ]
    return [
        nonclaim(
            {
                "formula_id": row_id,
                "formula": formula,
                "role": role,
                "status": status,
                "blocker": blocker,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, formula, role, status, blocker in specs
    ]


def tau_row_requirements() -> list[dict[str, Any]]:
    specs = [
        ("TAU2841_0_long_range_ppn", "long_range_PPN", "r_PPN/ell_R << 1 plus q_R_hat map", "q_R_hat formula above", "MISSING_CONDITIONS", "can use 1884/2832 PPN bridge only after conditions close"),
        ("TAU2841_1_finite_range_ppn", "finite_range_profile", "radial tau_PPN(r;ell_R) map", "profile response kernel", "MISSING_TAUPPN_PROFILE", "needed if ell_R is not much larger than solar-system baseline"),
        ("TAU2841_2_source_mass", "source_mass_convention", "same measured GM in q_R_hat and PPN U", "GM convention row", "MISSING_MEASURED_GM_CONVENTION", "prevents hidden calibration errors"),
        ("TAU2841_3_bound", "bound_comparator", "Cassini/PPN bound use only after prediction row exists", "external comparator", "COMPARATOR_ONLY", "not an MTS coefficient source"),
    ]
    return [
        nonclaim(
            {
                "tau_id": row_id,
                "route": route,
                "required_object": required,
                "row_type": row_type,
                "current_status": status,
                "reason": reason,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, route, required, row_type, status, reason in specs
    ]


def vector_guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("VG2841_0_delta_p", "delta_p/q_R_hat", "partially bridged conditionally", "still missing q_R_eff value and bridge conditions"),
        ("VG2841_1_bR", "b_R", "not filled", "gamma combo still depends on b_R unless no-shadow theorem closes"),
        ("VG2841_2_beta", "Delta_beta_total_abs", "not filled", "local GR needs beta/source second-order channel"),
        ("VG2841_3_dR", "d_R/preferred-frame", "not filled", "preferred-frame response matrix remains open"),
        ("VG2841_4_source_endpoint_readout", "w_R/endpoint/readout/q_loc", "not filled", "full vector must keep no-cancellation guard"),
        ("VG2841_5_total", "Delta_PPN_abs", "blocked", "no PPN/local-GR pass from q_R_hat bridge alone"),
    ]
    return [
        nonclaim(
            {
                "guard_id": row_id,
                "component": component,
                "status": status,
                "reason": reason,
                "component_closed": False,
                "control_only": True,
            }
        )
        for row_id, component, status, reason in specs
    ]


def gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    conditional_formula_present = any(row["formula_id"] == "FORM2841_0_qRhat" for row in rows_by_name["formula"])
    conditions_closed = all(row["condition_closed"] for row in rows_by_name["conditions"])
    vector_closed = all(row["component_closed"] for row in rows_by_name["vector_guard"])
    specs = [
        ("GATE2841_0_sources", "all cited source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "local evidence trail resolves"),
        ("GATE2841_1_bridge_formula", "q_R_eff to q_R_hat formula is derived conditionally", conditional_formula_present, "PASS_CONDITIONAL_NONCLAIM" if conditional_formula_present else "BLOCKED", "formula exists but is not claim-ready"),
        ("GATE2841_2_bridge_claim", "q_R_eff to q_R_hat bridge is accepted for scoring", conditions_closed, "BLOCKED", "bridge conditions remain open"),
        ("GATE2841_3_tauPPN", "tau_PPN row is source-backed", False, "BLOCKED", "finite-range/profile route remains a requirement only"),
        ("GATE2841_4_full_vector", "full PPN vector is closed", vector_closed, "BLOCKED", "delta_p bridge alone is not local GR"),
        ("GATE2841_5_local_GR", "local GR/Newton reduction is derived", False, "BLOCKED", "PPN bridge is conditional and incomplete"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": row_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for row_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2841_0_formula", "Conditional q_R_eff to q_R_hat bridge derived.", "CONDITIONAL_BRIDGE_FOUND", "matching the 2839 exterior kernel to 1884 C_R=-Q_R/r gives q_R_hat=-sigma_R*q_R_eff*c^2/(4*pi*G*M_source).", "use this as the pack formula, not as a score"),
        ("DEC2841_1_conditions", "Bridge conditions remain open.", "NOT_ACCEPTED_FOR_CLAIM", "C_R=delta_R, H_R=0, long-range limit, sign, measured GM, b_R and full vector are not closed.", "attack conditions before scoring"),
        ("DEC2841_2_next", "Best next route is condition closure or tau_PPN profile.", "PPN_CONDITION_CLOSURE_SELECTED", "this is now sharper than generic source hunting.", "derive/lock the C_R=delta_R, boundary, long-range and measured-GM conditions"),
    ]
    return [
        nonclaim(
            {
                "decision_id": row_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for row_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2841_0_2842",
                "status": "selected_primary",
                "target_doc": "2842-Y5-R2FR-PPN-bridge-condition-closure-or-finite-tauPPN-profile-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_PPN_bridge_condition_closure_or_finite_tauPPN_profile_under_AX1090_2842.py",
                "mission": "try to close the q_R_eff to q_R_hat bridge conditions: C_R=delta_R, H_R=0/no-hair, long-range ell_R regime, source sign, measured-GM convention, b_R/no-shadow, and full-vector guard; if not, build finite tau_PPN(r) profile requirements",
                "acceptance": "must not score the conditional formula until all conditions and full-vector guard are closed or source-backed",
                "forbidden": "do not set H_R=0 by asymptotic wish; do not assume ell_R is long range; do not drop b_R/beta/disformal/readout channels",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2841_0_bridge", OUTPUTS["bridge"], BRANCH_OUTPUTS["bridge_copy"], "local-bounds copy of conditional q_R_eff to q_R_hat bridge"),
        ("BR2841_1_formula", OUTPUTS["formula"], BRANCH_OUTPUTS["formula_copy"], "source-weight copy of PPN formula pack"),
        ("BR2841_2_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for PPN bridge condition closure"),
        ("BR2841_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable beta-source decision ledger"),
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
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("source_path", "source_table", "copy_path"):
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
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
            for key in ("bridge_closed_for_claim", "source_backed", "accepted_ready", "condition_closed", "component_closed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "predicted_value", "coefficient_value", "alpha_bound", "lambda_value", "accepted_value", "raw_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2841_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2841_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2841_2_bridge_formula", any(row["bridge_id"] == "BRG2841_4_qRhat_map" for row in rows_by_name["bridge"]), "conditional q_R_hat map row exists"),
        ("VAL2841_3_delta_p_formula", any(row["formula_id"] == "FORM2841_1_delta_p" for row in rows_by_name["formula"]), "conditional delta_p formula exists"),
        ("VAL2841_4_conditions_open", not any(row["condition_closed"] for row in rows_by_name["conditions"]), "bridge conditions remain open"),
        ("VAL2841_5_vector_guard_open", not any(row["component_closed"] for row in rows_by_name["vector_guard"]), "full-vector guard remains open"),
        ("VAL2841_6_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows PPN/local scoring"),
        ("VAL2841_7_next_target_2842", any(row["next_id"] == "NEXT2841_0_2842" and row["selected"] for row in rows_by_name["next"]), "PPN bridge condition closure selected next"),
        ("VAL2841_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2841_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2841_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2841_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2841_12_no_claim_flags", no_claim_flags(rows_by_name), "no score/source/claim/closed flags are true"),
        ("VAL2841_13_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2841_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2841_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2841_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2841_OVERALL",
            "passed": overall,
            "detail": "2841 derives a conditional q_R_eff to q_R_hat bridge and delta_p formula, keeps all bridge/full-vector conditions unclaimed, and selects PPN bridge condition closure or finite tau_PPN profile next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2841 - Y5 R2FR q_R_eff To q_R_hat PPN Bridge Or tauPPN Source Row Under AX1090

Status: `Y5_R2FR_2841_conditional_qreff_to_qrhat_bridge_found_conditions_open_nonclaim`

## Private Verdict

2841 gets a real conditional bridge.

From the finite Green kernel,

```text
delta_R(r)=sigma_R q_R_eff exp(-r/ell_R)/(4 pi r)+H_R
```

If the PPN domain is long-range (`r_PPN/ell_R << 1`), the boundary homogeneous mode is absent or bounded (`H_R=0`), and the same readout identifies `C_R=delta_R`, then matching to the older exterior convention

```text
C_R=-Q_R/r
q_R_hat=Q_R c^2/(G M_source)
delta_p=-q_R_hat/2
```

gives

```text
Q_R = -sigma_R q_R_eff/(4 pi)
q_R_hat = -sigma_R q_R_eff c^2/(4 pi G M_source)
delta_p = sigma_R q_R_eff c^2/(8 pi G M_source)
```

This is useful. It is also **not claimable** yet. The bridge conditions are open: `C_R=delta_R`, boundary class, long-range `ell_R`, source sign, measured-GM convention, `b_R`, and the full PPN vector all remain unclosed. If the long-range condition fails, this becomes a finite `tau_PPN(r)` profile problem rather than ordinary PPN.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Conditional Bridge

{markdown_table(rows["bridge"], ["bridge_id", "statement", "role", "status", "condition_or_blocker", "bridge_closed_for_claim", "valid_for_claim"])}

## Bridge Conditions

{markdown_table(rows["conditions"], ["condition_id", "condition", "current_status", "why_required", "condition_closed", "valid_for_claim"])}

## PPN Formula Pack

{markdown_table(rows["formula"], ["formula_id", "formula", "role", "status", "blocker", "numeric_value_present", "valid_for_claim"])}

## tauPPN Source Row Requirement

{markdown_table(rows["tau_row"], ["tau_id", "route", "required_object", "row_type", "current_status", "reason", "accepted_ready", "valid_for_claim"])}

## Full Vector Guard

{markdown_table(rows["vector_guard"], ["guard_id", "component", "status", "reason", "component_closed", "valid_for_claim"])}

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
    rows["bridge"] = bridge_rows()
    rows["conditions"] = condition_rows()
    rows["formula"] = formula_rows()
    rows["tau_row"] = tau_row_requirements()
    rows["vector_guard"] = vector_guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "bridge", "conditions", "formula", "tau_row", "vector_guard", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2841_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2841_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
