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

DOC = ROOT / "2842-Y5-R2FR-PPN-bridge-condition-closure-or-finite-tauPPN-profile-under-AX1090.md"

SRC_2841_NEXT = RESIDUALS / "P8_Y5_R2FR_2841_NEXT_TARGET.csv"
SRC_2841_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2841_QREFF_TO_QRHAT_CONDITIONAL_BRIDGE.csv"
SRC_2841_COND = RESIDUALS / "P8_Y5_R2FR_2841_PPN_BRIDGE_CONDITIONS.csv"
SRC_2841_FORMULA = RESIDUALS / "P8_Y5_R2FR_2841_PPN_FORMULA_PACK_NONCLAIM.csv"
SRC_2841_TAU = RESIDUALS / "P8_Y5_R2FR_2841_TAUPPN_SOURCE_ROW_REQUIREMENT.csv"
SRC_2841_VECTOR = RESIDUALS / "P8_Y5_R2FR_2841_FULL_VECTOR_GUARD.csv"
SRC_2841_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2841_VALIDATION.csv"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_1882 = ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md"
SRC_1884 = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_11 = ROOT / "11-cell-current-origin-attempt.md"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"
SRC_2489 = ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2842_SOURCE_REGISTER.csv",
    "condition_audit": RESIDUALS / "P8_Y5_R2FR_2842_PPN_BRIDGE_CONDITION_CLOSURE_AUDIT.csv",
    "tau_profile": RESIDUALS / "P8_Y5_R2FR_2842_FINITE_TAUPPN_PROFILE.csv",
    "cab_ledger": RESIDUALS / "P8_Y5_R2FR_2842_CAB_TARGET_MAP_LEDGER.csv",
    "route_split": RESIDUALS / "P8_Y5_R2FR_2842_ROUTE_SPLIT.csv",
    "requirements": RESIDUALS / "P8_Y5_R2FR_2842_PROFILE_SOURCE_REQUIREMENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2842_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2842_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2842_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2842_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2842_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "tau_profile_copy": LOCAL_BOUNDS / "RAB_finite_tauPPN_profile_2842_NONCLAIM.csv",
    "cab_copy": SOURCE_WEIGHT / "RAB_CAB_target_map_ledger_2842_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2842_CAB_target_or_tauPPN_pack_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_PPN_BRIDGE_CONDITION_OR_TAUPPN_2842_NONCLAIM.csv",
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
        ("SRC2842_0_2841_next", SRC_2841_NEXT, "NEXT2841_0_2842", "2841 selected bridge condition closure or finite tauPPN profile"),
        ("SRC2842_1_2841_bridge", SRC_2841_BRIDGE, "BRG2841_4_qRhat_map;BRG2841_5_delta_p_map", "2841 conditional bridge"),
        ("SRC2842_2_2841_conditions", SRC_2841_COND, "COND2841_0_CR_deltaR;COND2841_6_full_vector", "2841 open condition set"),
        ("SRC2842_3_2841_formula", SRC_2841_FORMULA, "FORM2841_0_qRhat;FORM2841_4_finite_range_warning", "2841 formula pack"),
        ("SRC2842_4_2841_tau", SRC_2841_TAU, "TAU2841_1_finite_range_ppn", "2841 tauPPN requirement"),
        ("SRC2842_5_2841_vector", SRC_2841_VECTOR, "VG2841_5_total", "2841 full-vector guard"),
        ("SRC2842_6_2841_validation", SRC_2841_VALIDATION, "VAL2841_OVERALL", "2841 validation"),
        ("SRC2842_7_2839_kernel", SRC_2839_KERNEL, "KER2839_4_compact_body", "finite compact kernel source"),
        ("SRC2842_8_1882", SRC_1882, "C_R = R_AB = ln(T^2 S);CRID1882_0_definitions;C_R = 2(p-1)u", "C_R/R_AB weak-field identity"),
        ("SRC2842_9_1884", SRC_1884, "NBC1884_3_qRhat_bridge;delta_p=-q_R_hat/2", "q_R_hat bridge convention"),
        ("SRC2842_10_11", SRC_11, "R_AB = -Q_R/r;conserves Q_R but permits hair", "boundary/current hair warning"),
        ("SRC2842_11_10", SRC_10, "R_AB = ln(T^2 S)", "observer map definition"),
        ("SRC2842_12_2489", SRC_2489, "PPNK2489_1_CR_delta_p_combo_kernel;GAMMA_ONLY_PASS_FORBIDDEN", "PPN kernel guard"),
        ("SRC2842_13_2631", SRC_2631, "PPNV2631_8_total_abs;PARENT_NO_SHADOW_FULL_PPN_VECTOR_NOT_CLOSED", "full-vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def condition_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "COND2842_0_CR_RAB_identity",
            "C_R=R_AB",
            "C_R = R_AB = ln(T^2 S) is already in the 1882 identity chain.",
            "PARTIAL_IDENTITY_CLOSED_INTERNAL",
            "does not by itself give C_R=delta_R because delta_R=R_AB-C_AB[Q]",
            True,
        ),
        (
            "COND2842_1_CR_deltaR",
            "C_R=delta_R",
            "requires C_AB[Q]=0 or an exact target-map cancellation in the same readout convention.",
            "NOT_CLOSED_TARGET_MAP_OPEN",
            "C_AB[Q] ownership/value is not supplied by current rows.",
            False,
        ),
        (
            "COND2842_2_boundary",
            "H_R=0/no-hair",
            "requires a boundary/no-edge-current theorem or a finite boundary homogeneous bound.",
            "NOT_CLOSED_BOUNDARY_CLASS_OPEN",
            "11/1884 conserve or define exterior hair but do not kill it.",
            False,
        ),
        (
            "COND2842_3_long_range",
            "r_PPN/ell_R << 1",
            "requires ell_R value/range hierarchy over the PPN domain.",
            "NOT_CLOSED_RANGE_VALUE_MISSING",
            "ell_R remains part of the unfilled normalization pack.",
            False,
        ),
        (
            "COND2842_4_sign",
            "sigma_R source sign",
            "requires source convention for S_R/Z_R or q_R_eff.",
            "NOT_CLOSED_SIGN_MISSING",
            "the sign cannot be inferred from desired GR behavior.",
            False,
        ),
        (
            "COND2842_5_measured_GM",
            "same measured GM convention",
            "requires a source mass convention tied to PPN U=GM/r and q_R_hat normalization.",
            "NOT_CLOSED_GM_CONVENTION_MISSING",
            "old convention rows define the rule but not this finite pack's source mass.",
            False,
        ),
        (
            "COND2842_6_bR_full_vector",
            "b_R/no-shadow and full-vector closure",
            "requires b_R plus beta/preferred/source/endpoint/readout/q_loc channels zeroed or bounded.",
            "NOT_CLOSED_FULL_VECTOR_OPEN",
            "gamma bridge alone is not local GR.",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "condition_id": row_id,
                "condition": condition,
                "attempt": attempt,
                "current_status": status,
                "blocker_or_caveat": caveat,
                "internal_identity_closed": identity_closed,
                "condition_closed_for_claim": False,
                "control_only": True,
            }
        )
        for row_id, condition, attempt, status, caveat, identity_closed in specs
    ]


def tau_profile_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TAUP2842_0_deltaR_profile",
            "delta_R(r)=sigma_R*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R(r)",
            "finite Green-kernel exterior profile",
            "DERIVED_SYMBOLIC",
            "q_R_eff, sigma_R, ell_R and H_R are not sourced",
        ),
        (
            "TAUP2842_1_CR_target_split",
            "C_R(r)=delta_R(r)+C_AB[Q](r)",
            "because delta_R=R_AB-C_AB[Q] and C_R=R_AB",
            "DERIVED_SYMBOLIC_TARGET_SPLIT",
            "C_AB[Q](r) is not parent-zeroed or sourced",
        ),
        (
            "TAUP2842_2_delta_p_profile",
            "delta_p(r)=c^2*r*C_R(r)/(2*G*M_source)",
            "PPN-style radial residual profile from C_R=2 delta_p U/c^2",
            "DERIVED_CONDITIONAL_PROFILE",
            "requires measured-GM convention and C_R profile",
        ),
        (
            "TAUP2842_3_explicit_profile",
            "delta_p(r)=sigma_R*q_R_eff*c^2*exp(-r/ell_R)/(8*pi*G*M_source)+c^2*r*(H_R(r)+C_AB[Q](r))/(2*G*M_source)",
            "finite tau_PPN profile including range, boundary and target-map terms",
            "DERIVED_CONDITIONAL_PROFILE",
            "not score-ready because every amplitude/source term is missing",
        ),
        (
            "TAUP2842_4_qRhat_profile",
            "q_R_hat(r)=-sigma_R*q_R_eff*c^2*exp(-r/ell_R)/(4*pi*G*M_source)-c^2*r*(H_R(r)+C_AB[Q](r))/(G*M_source)",
            "radial q_R_hat profile using q_R_hat=-2 delta_p",
            "DERIVED_CONDITIONAL_PROFILE",
            "ordinary constant q_R_hat is recovered only if exp(-r/ell_R)->1 and H_R+C_AB=0",
        ),
        (
            "TAUP2842_5_constant_limit",
            "if ell_R>>r_PPN and H_R=C_AB=0, delta_p=sigma_R*q_R_eff*c^2/(8*pi*G*M_source)",
            "recovers 2841 constant bridge",
            "EXACT_LIMIT_NONCLAIM",
            "limit conditions are not closed",
        ),
    ]
    return [
        nonclaim(
            {
                "profile_id": row_id,
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


def cab_rows() -> list[dict[str, Any]]:
    specs = [
        ("CAB2842_0_definition", "delta_R=R_AB-C_AB[Q]", "target map enters the finite auxiliary residual by definition", "TARGET_MAP_INCLUDED", "C_AB cannot be silently erased"),
        ("CAB2842_1_zero_route", "C_AB[Q]=0", "would make C_R=delta_R because C_R=R_AB", "NOT_PARENT_SIGNED", "requires parent target-map zero theorem"),
        ("CAB2842_2_source_route", "C_AB[Q](r)=A_CAB(r)", "if nonzero, it contributes to tau_PPN as c^2*r*C_AB/(2GM)", "LIVE_FALLBACK", "requires source/profile row"),
        ("CAB2842_3_claim_effect", "q_R_eff bridge", "2841 constant q_R_eff -> q_R_hat bridge is claimable only if C_AB and H_R vanish/bound", "BLOCKS_CLAIM", "target-map term must be carried in all future PPN profile rows"),
    ]
    return [
        nonclaim(
            {
                "cab_id": row_id,
                "object": obj,
                "meaning": meaning,
                "current_status": status,
                "next_requirement": req,
                "target_zero_closed": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, obj, meaning, status, req in specs
    ]


def route_split_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROUTE2842_0_constant_PPN", "constant q_R_hat/delta_p bridge", "requires C_AB=0, H_R=0, ell_R>>r_PPN, sign, measured GM, b_R/no-shadow and full vector", "HELD_CONDITIONAL_NOT_CLAIMED"),
        ("ROUTE2842_1_finite_tauPPN", "radial tau_PPN(r) profile", "active whenever ell_R is finite on the test domain or H_R/C_AB survive", "SELECTED_FALLBACK_PROFILE"),
        ("ROUTE2842_2_parent_zero", "parent zero/local GR route", "requires parent-signing reciprocal lock/no-shadow/full-vector clauses", "HELD_CONDITIONAL_NOT_CLAIMED"),
        ("ROUTE2842_3_empirical_pack", "source-backed finite profile pack", "requires ell_R, q_R_eff, sigma_R, H_R, C_AB, measured GM and tau profile projection", "NEXT_WORK_OBJECT"),
    ]
    return [
        nonclaim(
            {
                "route_id": row_id,
                "route": route,
                "requirements": req,
                "status": status,
                "selected_for_claim": False,
                "control_only": True,
            }
        )
        for row_id, route, req, status in specs
    ]


def requirement_rows() -> list[dict[str, Any]]:
    specs = [
        ("REQ2842_0_ell", "ell_R", "range value with units and tested-domain hierarchy", "MISSING_ELL_R"),
        ("REQ2842_1_qeff", "q_R_eff", "source-normalized compact amplitude with sign convention", "MISSING_Q_R_EFF"),
        ("REQ2842_2_boundary", "H_R(r)", "zero/no-hair theorem or finite homogeneous-mode profile", "MISSING_BOUNDARY_CLASS"),
        ("REQ2842_3_cab", "C_AB[Q](r)", "target-map zero theorem or finite target profile", "MISSING_CAB_TARGET_MAP"),
        ("REQ2842_4_gm", "M_source/GM", "same measured source mass convention as PPN U=GM/r", "MISSING_MEASURED_GM_CONVENTION"),
        ("REQ2842_5_projection", "tau_PPN(r)", "map from profile to PPN observable extraction including b_R/no-shadow terms", "MISSING_TAUPPN_PROFILE"),
        ("REQ2842_6_vector", "full vector", "beta/preferred/source/endpoint/readout/q_loc closures or finite components", "MISSING_FULL_VECTOR_CLOSURE"),
    ]
    return [
        nonclaim(
            {
                "requirement_id": row_id,
                "required_input": required,
                "description": description,
                "current_status": status,
                "accepted_ready": False,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, required, description, status in specs
    ]


def gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    profile_written = any(row["profile_id"] == "TAUP2842_3_explicit_profile" for row in rows_by_name["tau_profile"])
    constant_conditions_closed = all(row["condition_closed_for_claim"] for row in rows_by_name["condition_audit"])
    reqs_ready = all(row["accepted_ready"] for row in rows_by_name["requirements"])
    specs = [
        ("GATE2842_0_sources", "all cited source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "audit trail resolves"),
        ("GATE2842_1_partial_identity", "C_R=R_AB identity usable internally", True, "PASS_INTERNAL_NONCLAIM", "1882 already records C_R=R_AB=ln(T^2S)"),
        ("GATE2842_2_constant_bridge", "constant q_R_hat/delta_p bridge accepted", constant_conditions_closed, "BLOCKED", "C_AB, H_R, ell_R, sign, GM, b_R and full vector are open"),
        ("GATE2842_3_tau_profile", "finite tau_PPN profile is written", profile_written, "PASS_PROFILE_NONCLAIM" if profile_written else "BLOCKED", "profile is symbolic, not source-backed"),
        ("GATE2842_4_source_pack", "finite profile source pack is accepted", reqs_ready, "BLOCKED", "required inputs are missing"),
        ("GATE2842_5_local_GR", "local GR/Newton reduction is derived", False, "BLOCKED", "profile plumbing does not close full local-GR theorem"),
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
        ("DEC2842_0_identity", "C_R=R_AB is usable, but C_R=delta_R is not closed.", "PARTIAL_IDENTITY_ONLY", "delta_R subtracts C_AB[Q], so target-map ownership is now a real condition.", "carry C_AB in profile rows"),
        ("DEC2842_1_profile", "Finite tau_PPN(r) profile derived symbolically.", "PROFILE_ROUTE_READY_NONCLAIM", "the long-range constant PPN bridge is only a limit of the finite profile.", "source ell_R/q_eff/H_R/C_AB/GM/projection pack"),
        ("DEC2842_2_next", "Next target is C_AB target-map zero or finite profile pack.", "CAB_TARGET_SELECTED", "without C_AB status we cannot honestly identify q_R_eff with q_R_hat.", "attack C_AB[Q]=0 first; otherwise source C_AB(r)"),
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
                "next_id": "NEXT2842_0_2843",
                "status": "selected_primary",
                "target_doc": "2843-Y5-R2FR-CAB-target-map-zero-or-finite-tauPPN-source-pack-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_CAB_target_map_zero_or_finite_tauPPN_source_pack_under_AX1090_2843.py",
                "mission": "try to derive C_AB[Q]=0 in the local exterior/PPN branch; if not, stage C_AB[Q](r) as part of the finite tau_PPN profile source pack with ell_R, q_R_eff, H_R, measured-GM and full-vector guards",
                "acceptance": "do not identify C_R with delta_R or q_R_eff with q_R_hat unless C_AB and H_R are zero/bounded and the range/GM/full-vector conditions are handled",
                "forbidden": "do not erase the compatibility target by notation; do not assume long range; do not score a profile without source-backed amplitudes",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2842_0_tau_profile", OUTPUTS["tau_profile"], BRANCH_OUTPUTS["tau_profile_copy"], "local-bounds copy of finite tauPPN profile"),
        ("BR2842_1_cab", OUTPUTS["cab_ledger"], BRANCH_OUTPUTS["cab_copy"], "source-weight copy of C_AB target map ledger"),
        ("BR2842_2_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for C_AB target or tauPPN pack"),
        ("BR2842_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable beta-source decision ledger"),
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
            for key in ("condition_closed_for_claim", "source_backed", "accepted_ready", "target_zero_closed", "selected_for_claim"):
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
        ("VAL2842_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2842_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2842_2_partial_identity", any(row["condition_id"] == "COND2842_0_CR_RAB_identity" and row["internal_identity_closed"] for row in rows_by_name["condition_audit"]), "C_R=R_AB internal identity recorded"),
        ("VAL2842_3_constant_not_closed", not any(row["condition_closed_for_claim"] for row in rows_by_name["condition_audit"]), "constant PPN bridge conditions remain unclaimed"),
        ("VAL2842_4_profile_formula", any(row["profile_id"] == "TAUP2842_3_explicit_profile" for row in rows_by_name["tau_profile"]), "finite tau_PPN explicit profile row exists"),
        ("VAL2842_5_cab_open", any(row["cab_id"] == "CAB2842_1_zero_route" and row["current_status"] == "NOT_PARENT_SIGNED" for row in rows_by_name["cab_ledger"]), "C_AB target-map zero route remains unsigned"),
        ("VAL2842_6_requirements_blocked", not any(row["accepted_ready"] for row in rows_by_name["requirements"]), "profile source requirements remain unaccepted"),
        ("VAL2842_7_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows PPN/local scoring"),
        ("VAL2842_8_next_target_2843", any(row["next_id"] == "NEXT2842_0_2843" and row["selected"] for row in rows_by_name["next"]), "C_AB target map selected next"),
        ("VAL2842_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2842_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2842_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2842_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2842_13_no_claim_flags", no_claim_flags(rows_by_name), "no score/source/claim/closed flags are true"),
        ("VAL2842_14_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2842_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2842_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2842_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2842_OVERALL",
            "passed": overall,
            "detail": "2842 records the partial C_R=R_AB identity, refuses the stronger C_R=delta_R bridge because C_AB[Q] remains open, derives the finite tau_PPN(r) profile with H_R and C_AB terms, and selects C_AB target-map zero or finite profile pack next.",
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
    content = f"""# 2842 - Y5 R2FR PPN Bridge Condition Closure Or Finite tauPPN Profile Under AX1090

Status: `Y5_R2FR_2842_CR_RAB_identity_partial_CAB_target_open_tauPPN_profile_derived_nonclaim`

## Private Verdict

2842 closes one useful internal identity and blocks one tempting shortcut.

The usable identity is:

```text
C_R = R_AB = ln(T^2 S)
```

But the finite kernel variable is

```text
delta_R = R_AB - C_AB[Q]
```

Therefore `C_R=delta_R` is **not** automatic. It requires `C_AB[Q]=0` or a sourced/derived target-map term. This is the little trap that would have let us accidentally identify `q_R_eff` with `q_R_hat` too cheaply.

The honest finite profile is now:

```text
delta_R(r)=sigma_R q_R_eff exp(-r/ell_R)/(4*pi*r)+H_R(r)
C_R(r)=delta_R(r)+C_AB[Q](r)
delta_p(r)=c^2 r C_R(r)/(2 G M_source)
```

so

```text
delta_p(r)=sigma_R q_R_eff c^2 exp(-r/ell_R)/(8*pi*G*M_source)
           + c^2 r (H_R(r)+C_AB[Q](r))/(2 G M_source)
```

The old constant PPN bridge is only the clean limit where `ell_R >> r_PPN`, `H_R=0`, and `C_AB[Q]=0`, plus sign, measured-GM, `b_R`, and full-vector conditions. No PPN/local-GR claim is made.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Condition Closure Audit

{markdown_table(rows["condition_audit"], ["condition_id", "condition", "current_status", "blocker_or_caveat", "internal_identity_closed", "condition_closed_for_claim", "valid_for_claim"])}

## Finite tauPPN Profile

{markdown_table(rows["tau_profile"], ["profile_id", "formula", "role", "status", "blocker", "numeric_value_present", "valid_for_claim"])}

## C_AB Target Map Ledger

{markdown_table(rows["cab_ledger"], ["cab_id", "object", "meaning", "current_status", "next_requirement", "target_zero_closed", "valid_for_claim"])}

## Route Split

{markdown_table(rows["route_split"], ["route_id", "route", "requirements", "status", "selected_for_claim", "valid_for_claim"])}

## Profile Source Requirements

{markdown_table(rows["requirements"], ["requirement_id", "required_input", "description", "current_status", "accepted_ready", "numeric_value_present", "valid_for_claim"])}

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
    rows["condition_audit"] = condition_audit_rows()
    rows["tau_profile"] = tau_profile_rows()
    rows["cab_ledger"] = cab_rows()
    rows["route_split"] = route_split_rows()
    rows["requirements"] = requirement_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "condition_audit", "tau_profile", "cab_ledger", "route_split", "requirements", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2842_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2842_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
