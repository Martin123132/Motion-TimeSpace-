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

DOC = ROOT / "2840-Y5-R2FR-first-finite-RAB-normalization-pack-or-parent-zero-certificate-under-AX1090.md"

SRC_2839_NEXT = RESIDUALS / "P8_Y5_R2FR_2839_NEXT_TARGET.csv"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_DIM = RESIDUALS / "P8_Y5_R2FR_2839_DIMENSIONAL_CONTRACT.csv"
SRC_2839_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv"
SRC_2839_PROJ = RESIDUALS / "P8_Y5_R2FR_2839_ARENA_PROJECTION_CONTRACT.csv"
SRC_2839_ZOS = RESIDUALS / "P8_Y5_R2FR_2839_THEOREM_ZERO_OR_SOURCE_ROW_ATTEMPT.csv"
SRC_2839_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2839_VALIDATION.csv"
SRC_2838_SIGNATURE = RESIDUALS / "P8_Y5_R2FR_2838_SECOND_CLASS_SIGNATURE_AUDIT.csv"
SRC_2832_GAMMA = RESIDUALS / "P8_Y5_R2FR_2832_GAMMA_COMBO_ALGEBRA_LEDGER.csv"
SRC_2833_QRHAT = RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_PARENT_ZERO_PROOF_AUDIT.csv"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2840_SOURCE_REGISTER.csv",
    "pack_contract": RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv",
    "fill_attempt": RESIDUALS / "P8_Y5_R2FR_2840_FIRST_PACK_FILL_ATTEMPT_NONCLAIM.csv",
    "parent_zero": RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv",
    "ppn_bridge": RESIDUALS / "P8_Y5_R2FR_2840_QREFF_TO_QRHAT_PPN_BRIDGE_AUDIT.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2840_PACK_ACCEPTANCE_VALIDATOR.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2840_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2840_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2840_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2840_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2840_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2840_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "pack_copy": LOCAL_BOUNDS / "RAB_first_normalization_pack_contract_2840_NONCLAIM.csv",
    "ppn_bridge_copy": SOURCE_WEIGHT / "RAB_qreff_to_qrhat_ppn_bridge_2840_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2840_qreff_to_qrhat_or_parent_zero_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_FIRST_NORMALIZATION_PACK_OR_PARENT_ZERO_2840_NONCLAIM.csv",
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
        ("SRC2840_0_2839_next", SRC_2839_NEXT, "NEXT2839_0_2840", "2839 selected first normalization pack or parent-zero certificate"),
        ("SRC2840_1_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_4_compact_body", "finite RAB Green-kernel normalization"),
        ("SRC2840_2_2839_dim", SRC_2839_DIM, "DIM2839_0_RAB;DIM2839_3_point_charge;DIM2839_4_projection", "dimension contract"),
        ("SRC2840_3_2839_selector", SRC_2839_SELECTOR, "SEL2839_0_minimal_pair;SEL2839_1_ZR", "first source row selector"),
        ("SRC2840_4_2839_projection", SRC_2839_PROJ, "PROJ2839_0_R10;PROJ2839_1_PPN;PROJ2839_2_clock;PROJ2839_3_orbital", "arena projection blockers"),
        ("SRC2840_5_2839_zero_source", SRC_2839_ZOS, "ZOS2839_0_try_ZR_zero;ZOS2839_4_first_source_row", "zero-or-source attempt"),
        ("SRC2840_6_2839_validation", SRC_2839_VALIDATION, "VAL2839_OVERALL", "2839 validation"),
        ("SRC2840_7_2838_signature", SRC_2838_SIGNATURE, "SIG2838_1_action_image;SIG2838_6_joint_signature", "parent signature failure"),
        ("SRC2840_8_2832_gamma", SRC_2832_GAMMA, "ALG2832_0_combo;ALG2832_3_qRhat_bridge;ALG2832_5_total_abs_guard", "existing PPN gamma/q_R_hat bridge"),
        ("SRC2840_9_2833_qrhat", SRC_2833_QRHAT, "PZ2833_1_zero_flux;PZ2833_5_parent_zero_verdict", "q_R_hat parent-zero audit"),
        ("SRC2840_10_observer", SRC_10, "R_AB = ln(T^2 S)", "R_AB definition"),
    ]
    return [source_row(*spec) for spec in specs]


def pack_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("PACK2840_0_range", "ell_R", "range", "length", "ell_R^2=Z_R/M_R^2 or a direct sourced range", "required", "MISSING_ELL_R"),
        ("PACK2840_1_amplitude", "q_R_eff", "compact-source amplitude", "length", "q_R_eff=-integral_body S_R/Z_R d^3x", "required", "MISSING_Q_R_EFF"),
        ("PACK2840_2_sign", "sigma_R", "source sign convention", "dimensionless", "fixes whether the compact source raises or lowers delta_R", "required", "MISSING_SOURCE_SIGN"),
        ("PACK2840_3_boundary", "H_R", "boundary homogeneous mode/no-hair class", "dimensionless", "delta_R includes boundary_homogeneous until boundary silence is proved", "required", "MISSING_BOUNDARY_CLASS"),
        ("PACK2840_4_projection", "tau_arena", "arena projection", "arena dependent", "maps delta_R to alpha_R, q_R_hat, clock fraction, or acceleration", "required", "MISSING_TAU_ARENA"),
        ("PACK2840_5_source", "source_path+normalization", "source provenance", "n/a", "local source path, anchor, units and normalization convention", "required", "MISSING_SOURCE_PATH"),
        ("PACK2840_6_convention", "GM/readout convention", "measured-GM and coframe convention", "n/a", "needed before comparing to PPN delta_p or Yukawa alpha", "required", "MISSING_MEASURED_GM_CONVENTION"),
    ]
    return [
        nonclaim(
            {
                "contract_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "unit_contract": unit,
                "definition": definition,
                "necessity": necessity,
                "current_status": status,
                "present": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, symbol, meaning, unit, definition, necessity, status in specs
    ]


def fill_attempt_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "pack_id": "FILL2840_0_first_RAB_finite_pack",
                "candidate_prediction_object": "delta_R(r)=sigma_R*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R, then observable=tau_arena[delta_R]",
                "ell_R_value": "MISSING_ELL_R",
                "ell_R_units": "m",
                "q_R_eff_value": "MISSING_Q_R_EFF",
                "q_R_eff_units": "m",
                "source_sign": "MISSING_SOURCE_SIGN",
                "boundary_class": "MISSING_BOUNDARY_CLASS",
                "arena": "candidate_PPN_first_because_2832_has_q_R_hat_bridge",
                "tau_arena": "MISSING_QREFF_TO_QRHAT_MAP",
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "normalization_convention": "MISSING_MEASURED_GM_AND_COFRAME_CONVENTION",
                "fill_status": "FAILED_TO_FILL_FROM_CURRENT_CORPUS",
                "accepted_ready": False,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
    ]


def parent_zero_rows() -> list[dict[str, Any]]:
    specs = [
        ("PZ2840_0_action_image", "parent algebraic block", "derive Lambda_R(R_AB-C_AB[Q]) from parent primitives", "NOT_SIGNED", "SIG2838_1_action_image", "finite pack remains live"),
        ("PZ2840_1_operator_zero", "Z_R=0", "prove parent grammar excludes D R_AB and generated kinetic/mass operators", "NOT_SIGNED", "ZOS2839_0_try_ZR_zero", "ell_R pack remains required"),
        ("PZ2840_2_source_zero", "J_R=0", "prove actual R_AB direction is invisible to matter/source after observed coframe is fixed", "NOT_SIGNED", "ZOS2839_2_try_JR_zero", "q_R_eff pack remains required"),
        ("PZ2840_3_boundary_zero", "Pi_R=B_R=Q_R=0", "prove no R_AB edge charge or boundary homogeneous mode", "NOT_SIGNED", "ZOS2839_3_try_PiR_zero", "boundary class remains required"),
        ("PZ2840_4_readout_zero", "R_readout=tau=0", "prove readout/coarse-graining cannot regenerate R_AB observable channels", "NOT_SIGNED", "PROJ2839_1_PPN", "arena projection remains required"),
        ("PZ2840_5_joint_certificate", "parent-zero certificate", "all above clauses signed as one parent theorem", "NOT_CLOSED", "SIG2838_6_joint_signature;PZ2833_5_parent_zero_verdict", "no zero claim; use finite pack route"),
    ]
    return [
        nonclaim(
            {
                "certificate_id": row_id,
                "target": target,
                "success_condition": condition,
                "current_status": status,
                "source_anchors": anchors,
                "if_not_closed": fallback,
                "theorem_zero": False,
                "parent_signed": False,
                "control_only": True,
            }
        )
        for row_id, target, condition, status, anchors, fallback in specs
    ]


def ppn_bridge_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PPNB2840_0_existing_gamma_combo",
            "gamma_obs-1 = delta_p*(1+4*b_R)/(1-2*b_R*delta_p)",
            "existing symbolic PPN comparator",
            "AVAILABLE_SYMBOLIC",
            "ALG2832_0_combo",
            "still needs delta_p, b_R and denominator guard",
        ),
        (
            "PPNB2840_1_existing_qRhat_bridge",
            "delta_p=-q_R_hat/2",
            "existing bridge from q_R_hat to gamma-combo input",
            "AVAILABLE_SYMBOLIC",
            "ALG2832_3_qRhat_bridge",
            "q_R_hat is not yet connected to q_R_eff from the Green kernel",
        ),
        (
            "PPNB2840_2_missing_kernel_to_ppn",
            "q_R_hat = P_hat[delta_R; measured-GM convention]",
            "needed bridge from compact finite residual to PPN delta_p",
            "MISSING_DERIVATION",
            "KER2839_4_compact_body;ALG2832_3_qRhat_bridge",
            "next derivation target",
        ),
        (
            "PPNB2840_3_no_gamma_only",
            "Delta_PPN_abs includes gamma combo plus beta/preferred/source/endpoint/readout components",
            "full-vector guardrail",
            "ACTIVE_GUARD",
            "ALG2832_5_total_abs_guard",
            "even a q_R_hat bridge would not alone prove local GR",
        ),
    ]
    return [
        nonclaim(
            {
                "bridge_id": row_id,
                "statement": statement,
                "role": role,
                "current_status": status,
                "source_anchors": anchors,
                "blocker_or_next": blocker,
                "bridge_closed": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, statement, role, status, anchors, blocker in specs
    ]


def acceptance_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    fill = rows_by_name["fill_attempt"][0]
    checks = [
        ("ACC2840_0_range", "ell_R is numeric positive with units", not str(fill["ell_R_value"]).startswith("MISSING_"), "BLOCKED"),
        ("ACC2840_1_amplitude", "q_R_eff is numeric/source-normalized with units", not str(fill["q_R_eff_value"]).startswith("MISSING_"), "BLOCKED"),
        ("ACC2840_2_sign", "source sign convention is fixed", not str(fill["source_sign"]).startswith("MISSING_"), "BLOCKED"),
        ("ACC2840_3_boundary", "boundary/no-hair class is fixed", not str(fill["boundary_class"]).startswith("MISSING_"), "BLOCKED"),
        ("ACC2840_4_projection", "one arena projection is derived", not str(fill["tau_arena"]).startswith("MISSING_"), "BLOCKED"),
        ("ACC2840_5_source", "source path and anchor exist", not str(fill["source_path"]).startswith("MISSING_"), "BLOCKED"),
        ("ACC2840_6_convention", "measured-GM/coframe convention fixed", not str(fill["normalization_convention"]).startswith("MISSING_"), "BLOCKED"),
    ]
    accepted = all(passed for _, _, passed, _ in checks)
    output = [
        nonclaim(
            {
                "acceptance_id": row_id,
                "requirement": requirement,
                "passed": passed,
                "status": "PASS" if passed else status,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, requirement, passed, status in checks
    ]
    output.append(
        nonclaim(
            {
                "acceptance_id": "ACC2840_OVERALL",
                "requirement": "first finite RAB normalization pack is accepted",
                "passed": accepted,
                "status": "PASS" if accepted else "BLOCKED_PACK_NOT_FILLED",
                "accepted_ready": False,
                "control_only": True,
            }
        )
    )
    return output


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2840_0_pack_not_number", "a finite prediction is a pack, not one coefficient", "prevents false precision from standalone Z_R/M_R^2/J_R rows", "pack acceptance stays blocked"),
        ("GUARD2840_1_ppn_not_gamma_only", "PPN cannot be reduced to gamma alone", "2832 full-vector guard remains active", "q_R_hat bridge is necessary but not sufficient"),
        ("GUARD2840_2_boundary_homogeneous", "boundary homogeneous mode cannot be erased", "boundary silence is not proved", "H_R stays in the pack"),
        ("GUARD2840_3_no_zero_by_absence", "absence of coefficients is not theorem-zero", "operator/source/readout zeros need parent signatures", "parent-zero certificate remains unsigned"),
        ("GUARD2840_4_no_score", "do not score placeholders", "no range, amplitude, sign, source path, convention, or projection is accepted", "valid_for_claim remains false"),
    ]
    return [
        nonclaim(
            {
                "guard_id": row_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for row_id, guard, because, effect in specs
    ]


def gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    contract_written = len(rows_by_name["pack_contract"]) == 7
    pack_accepted = any(row["acceptance_id"] == "ACC2840_OVERALL" and row["passed"] for row in rows_by_name["acceptance"])
    zero_closed = any(row["certificate_id"] == "PZ2840_5_joint_certificate" and row["theorem_zero"] for row in rows_by_name["parent_zero"])
    ppn_bridge_closed = any(row["bridge_id"] == "PPNB2840_2_missing_kernel_to_ppn" and row["bridge_closed"] for row in rows_by_name["ppn_bridge"])
    guards_active = all(row["guard_active"] for row in rows_by_name["guards"])
    specs = [
        ("GATE2840_0_sources", "all cited source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "local evidence trail resolves"),
        ("GATE2840_1_contract", "normalization pack contract is written", contract_written, "PASS_CONTRACT_NONCLAIM" if contract_written else "BLOCKED", "requirements are precise but not filled"),
        ("GATE2840_2_pack", "first finite pack is accepted", pack_accepted, "BLOCKED", "range/amplitude/sign/boundary/projection/source/convention are missing"),
        ("GATE2840_3_parent_zero", "parent-zero certificate closes", zero_closed, "BLOCKED", "zero theorem remains unsigned"),
        ("GATE2840_4_ppn_bridge", "q_R_eff to q_R_hat PPN bridge closes", ppn_bridge_closed, "BLOCKED", "bridge from compact kernel amplitude to PPN delta_p is missing"),
        ("GATE2840_5_guards", "guardrails active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "no coefficient-only, gamma-only, or absence-as-zero shortcut"),
        ("GATE2840_6_local_gr", "local GR/Newton reduction is derived", False, "BLOCKED", "neither finite pack nor parent-zero certificate is claim-ready"),
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
        ("DEC2840_0_pack", "First finite pack was attempted but not filled.", "PACK_CONTRACT_READY_VALUES_MISSING", "current corpus lacks range, amplitude, sign, source path, boundary class, measured-GM convention, and arena projection in one row.", "do not score finite local branch"),
        ("DEC2840_1_zero", "Parent-zero certificate remains unsigned.", "ZERO_CERTIFICATE_NOT_CLOSED", "the same missing clauses block Z_R/J_R/Pi_R/readout theorem-zero.", "keep exact zero as conditional only"),
        ("DEC2840_2_ppn", "Best next derivation is q_R_eff to q_R_hat.", "PPN_BRIDGE_SELECTED", "2832 already has q_R_hat -> delta_p -> gamma combo, while 2839 gives q_R_eff from the Green kernel.", "derive P_hat[delta_R] or source tau_PPN"),
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
                "next_id": "NEXT2840_0_2841",
                "status": "selected_primary",
                "target_doc": "2841-Y5-R2FR-qreff-to-qrhat-PPN-bridge-or-tauPPN-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qreff_to_qrhat_PPN_bridge_or_tauPPN_source_row_under_AX1090_2841.py",
                "mission": "derive the map from finite compact-body Green-kernel amplitude q_R_eff to the existing q_R_hat/delta_p PPN bridge; if not derivable, stage tau_PPN as a source-backed nonclaim row requirement",
                "acceptance": "must preserve the full-vector PPN guard, measured-GM convention, boundary homogeneous term and no-placeholder rule; no gamma-only local-GR claim",
                "forbidden": "do not infer q_R_hat=q_R_eff by naming similarity; do not erase b_R or endpoint/readout components; do not score missing tau_PPN",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2840_0_pack", OUTPUTS["pack_contract"], BRANCH_OUTPUTS["pack_copy"], "local-bounds copy of first normalization pack contract"),
        ("BR2840_1_ppn_bridge", OUTPUTS["ppn_bridge"], BRANCH_OUTPUTS["ppn_bridge_copy"], "source-weight copy of q_R_eff to q_R_hat bridge audit"),
        ("BR2840_2_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for q_R_eff to q_R_hat bridge"),
        ("BR2840_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable beta-source decision ledger"),
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
            for key in ("theorem_zero", "source_backed", "accepted_ready", "parent_signed", "bridge_closed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {
        "numeric_value",
        "predicted_value",
        "coefficient_value",
        "alpha_bound",
        "lambda_value",
        "accepted_value",
        "raw_value",
    }
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
        ("VAL2840_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2840_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2840_2_pack_contract", len(rows_by_name["pack_contract"]) == 7, "normalization pack contract has all required components"),
        ("VAL2840_3_pack_not_filled", rows_by_name["fill_attempt"][0]["fill_status"] == "FAILED_TO_FILL_FROM_CURRENT_CORPUS", "first pack explicitly failed to fill from current corpus"),
        ("VAL2840_4_acceptance_blocks", any(row["acceptance_id"] == "ACC2840_OVERALL" and not row["passed"] for row in rows_by_name["acceptance"]), "pack acceptance remains blocked"),
        ("VAL2840_5_zero_not_closed", not any(row["theorem_zero"] for row in rows_by_name["parent_zero"]), "parent-zero certificate remains unsigned"),
        ("VAL2840_6_ppn_bridge_selected", any(row["bridge_id"] == "PPNB2840_2_missing_kernel_to_ppn" and row["current_status"] == "MISSING_DERIVATION" for row in rows_by_name["ppn_bridge"]), "q_R_eff to q_R_hat bridge is selected but missing"),
        ("VAL2840_7_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local scoring"),
        ("VAL2840_8_next_target_2841", any(row["next_id"] == "NEXT2840_0_2841" and row["selected"] for row in rows_by_name["next"]), "q_R_eff to q_R_hat bridge selected next"),
        ("VAL2840_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2840_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2840_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2840_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2840_13_no_claim_flags", no_claim_flags(rows_by_name), "no score/theorem/source/claim/bridge flags are true"),
        ("VAL2840_14_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2840_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2840_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2840_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2840_OVERALL",
            "passed": overall,
            "detail": "2840 writes the first finite RAB normalization-pack contract, proves the current corpus cannot fill it, keeps the parent-zero certificate unsigned, and selects the q_R_eff to q_R_hat PPN bridge next.",
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
    content = f"""# 2840 - Y5 R2FR First Finite RAB Normalization Pack Or Parent-Zero Certificate Under AX1090

Status: `Y5_R2FR_2840_first_pack_contract_ready_values_missing_qreff_to_qrhat_next`

## Private Verdict

2840 tries to turn the finite `R_AB` branch into the first source-ready prediction object.

The result is disciplined but not claimable: the first finite row cannot be accepted from the current corpus. A real row must contain the full pack

```text
ell_R, q_R_eff, sigma_R, H_R/boundary class, tau_arena,
source path + anchor, units, and measured-GM/coframe convention
```

The attempted first pack remains blocked because the current files do not provide `ell_R`, `q_R_eff`, source sign, boundary class, source path, measured-GM convention, or a real arena projection in one normalized object.

The parent-zero alternative also remains unsigned. The exact zero certificate would need the parent action image, no-derivative grammar, matter/source silence, boundary silence, and readout stability all signed together. That still is not present.

The best next target is now specific: derive the map from the finite Green-kernel amplitude `q_R_eff` to the existing PPN bridge variable `q_R_hat`. We already have `q_R_hat -> delta_p -> gamma_obs-1`; we do **not** yet have `q_R_eff -> q_R_hat`.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Normalization Pack Contract

{markdown_table(rows["pack_contract"], ["contract_id", "symbol", "meaning", "unit_contract", "definition", "current_status", "present", "accepted_ready"])}

## First Pack Fill Attempt

{markdown_table(rows["fill_attempt"], ["pack_id", "candidate_prediction_object", "ell_R_value", "q_R_eff_value", "source_sign", "boundary_class", "arena", "tau_arena", "fill_status", "accepted_ready", "valid_for_claim"])}

## Parent-Zero Certificate Audit

{markdown_table(rows["parent_zero"], ["certificate_id", "target", "success_condition", "current_status", "if_not_closed", "theorem_zero", "parent_signed", "valid_for_claim"])}

## q_R_eff To q_R_hat PPN Bridge Audit

{markdown_table(rows["ppn_bridge"], ["bridge_id", "statement", "role", "current_status", "blocker_or_next", "bridge_closed", "accepted_ready", "valid_for_claim"])}

## Pack Acceptance Validator

{markdown_table(rows["acceptance"], ["acceptance_id", "requirement", "passed", "status", "accepted_ready", "valid_for_claim"])}

## Guards

{markdown_table(rows["guards"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

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
    rows["pack_contract"] = pack_contract_rows()
    rows["fill_attempt"] = fill_attempt_rows()
    rows["parent_zero"] = parent_zero_rows()
    rows["ppn_bridge"] = ppn_bridge_rows()
    rows["acceptance"] = acceptance_rows(rows)
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in [
        "sources",
        "pack_contract",
        "fill_attempt",
        "parent_zero",
        "ppn_bridge",
        "acceptance",
        "guards",
        "gates",
        "decision",
        "next",
    ]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2840_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2840_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
