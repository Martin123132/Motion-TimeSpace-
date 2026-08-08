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

DOC = ROOT / "2832-Y5-R2FR-epsilon-vmq-first-finite-PPN-component-value-or-parent-zero-certificate-under-AX1090.md"

SRC_2831_NEXT = RESIDUALS / "P8_Y5_R2FR_2831_NEXT_TARGET.csv"
SRC_2831_KERNEL = RESIDUALS / "P8_Y5_R2FR_2831_PPN_COMPONENT_KERNEL_FILL_ROWS_NONCLAIM.csv"
SRC_2831_GUARD = RESIDUALS / "P8_Y5_R2FR_2831_NO_CANCELLATION_AND_FULL_VECTOR_GUARD.csv"
SRC_2831_THEOREM = RESIDUALS / "P8_Y5_R2FR_2831_PPN_COMMON_FRAME_THEOREM_ZERO_ATTEMPT.csv"
SRC_2489_KERNEL = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv"
SRC_2488_ZERO = RESIDUALS / "P8_Y5_NO_SHADOW_2488_ZERO_THEOREM.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2631_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"
SRC_1884_DOC = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"
SRC_1884_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_AUDIT.csv"
SRC_1884_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_SOURCE_DESCENT_PREMISE_MATRIX.csv"
SRC_1884_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_INPUT_CONTRACT.csv"
SRC_1884_TEMPLATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_CANDIDATE_TEMPLATE_NONCLAIM.csv"
SRC_1884_DRYRUN = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_VALIDATOR_DRYRUN_RESULTS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2832_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2832_BR_DELTAP_CERTIFICATE_AUDIT.csv",
    "algebra": RESIDUALS / "P8_Y5_R2FR_2832_GAMMA_COMBO_ALGEBRA_LEDGER.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2832_FINITE_BR_DELTAP_ACQUISITION_CONTRACT.csv",
    "guard": RESIDUALS / "P8_Y5_R2FR_2832_COMMON_CONVENTION_GUARD.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2832_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2832_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2832_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2832_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2832_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": LOCAL_BOUNDS / "bR_deltaP_gamma_combo_acquisition_contract_2832_NONCLAIM.csv",
    "algebra_copy": SOURCE_WEIGHT / "bR_deltaP_gamma_combo_algebra_2832_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2832_DELTAP_QRHAT_PARENT_ZERO_OR_FINITE_ROW_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
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
        ("SRC2832_0_2831_next", SRC_2831_NEXT, "NEXT2831_0_2832", "2831 selected the first finite PPN component or parent-zero certificate"),
        ("SRC2832_1_2831_kernel", SRC_2831_KERNEL, "KF2831_0_bR_gamma;KF2831_4_total_abs", "2831 b_R/gamma symbolic kernel row and total vector guard"),
        ("SRC2832_2_2831_guard", SRC_2831_GUARD, "GUARD2831_0_no_gamma_only;GUARD2831_4_common_convention", "2831 no gamma-only and common-convention guards"),
        ("SRC2832_3_2831_theorem", SRC_2831_THEOREM, "TZ2831_1_common_weyl_bR;TZ2831_6_verdict", "2831 theorem-zero status for common Weyl and current verdict"),
        ("SRC2832_4_2489_kernel", SRC_2489_KERNEL, "PPNK2489_1_CR_delta_p_combo_kernel;PPNK2489_0_conformal_gamma_kernel", "2489 gamma combo and conformal gamma kernels"),
        ("SRC2832_5_2488_zero", SRC_2488_ZERO, "ZTH2488_0_exact_conditional;ZTH2488_2_current_verdict", "2488 exact conditional no-shadow theorem"),
        ("SRC2832_6_2488_counter", SRC_2488_COUNTER, "CM2488_0_common_weyl;CM2488_4_qshape_forgetting", "common-Weyl and observable-functor countermodels"),
        ("SRC2832_7_2631_vector", SRC_2631_VECTOR, "PPNV2631_0_delta_p_qR;PPNV2631_1_bR;PPNV2631_8_total_abs", "2631 delta_p, b_R and total absolute PPN vector rows"),
        ("SRC2832_8_1884_doc", SRC_1884_DOC, "partial_r(W partial_r C_R)=J_R;delta_p=-q_R_hat/2", "1884 no-boundary-charge zero-flux lemma and delta_p/q_R_hat bridge"),
        ("SRC2832_9_1884_audit", SRC_1884_AUDIT, "NBC1884_1_exact_zero_flux_lemma;NBC1884_6_verdict", "1884 no-boundary-charge audit"),
        ("SRC2832_10_1884_matrix", SRC_1884_MATRIX, "SDM1884_1_boundary_charge;SDM1884_5_GM_normalization", "1884 source-descent premise matrix"),
        ("SRC2832_11_1884_contract", SRC_1884_CONTRACT, "DPQR1884_1_qRhat;DPQR1884_2_delta_p;DPQR1884_5_zero_theorem_status", "1884 delta_p/q_R_hat input contract"),
        ("SRC2832_12_1884_template", SRC_1884_TEMPLATE, "DPQR1884_TEMPLATE_PARENT_ZERO;DPQR1884_TEMPLATE_FINITE_QRHAT", "1884 candidate template for parent-zero or finite rows"),
        ("SRC2832_13_1884_dryrun", SRC_1884_DRYRUN, "CASE1884_5_gamma_only;CASE1884_7_schema_complete_nonclaim", "1884 validator dry-run refusal modes"),
    ]
    return [source_row(*spec) for spec in specs]


def certificate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CERT2832_0_no_weyl",
            "b_R_to_vmq parent zero",
            "S_matter and observed coframe/readout contain no exp(b_R C_R), no C_R-dependent measured-GM/gauge morphism, and no hidden representative argument.",
            "ZTH2488_0_exact_conditional;CM2488_0_common_weyl;TZ2831_1_common_weyl_bR",
            "NOT_PARENT_SIGNED",
            "common Weyl countermodel survives covariance/WEP/same-frame language",
            "b_R=0 would simplify the gamma combo but would not close gamma unless delta_p is also zero or finite-bounded",
        ),
        (
            "CERT2832_1_no_boundary_charge",
            "delta_p/q_R_hat parent zero",
            "Q_R=0, W>0, J_R=0 outside the source, C_R(infinity)=0, and source/matter/readout/projection descent all hold in the same parent package.",
            "NBC1884_1_exact_zero_flux_lemma;NBC1884_4_no_boundary_charge_parent_signature;SDM1884_1_boundary_charge",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "zero-flux lemma is exact, but Q_R=0 and source descent are still unsigned",
            "delta_p=0 would collapse gamma_obs-1 to zero for the 2489 combo regardless of finite b_R",
        ),
        (
            "CERT2832_2_joint_gamma_zero",
            "common-Weyl gamma zero certificate",
            "Either delta_p=0 by parent no-boundary-charge/source descent, or both b_R=0 and delta_p=0/finite-bounded are supplied with full-vector guard.",
            "PPNK2489_1_CR_delta_p_combo_kernel;PPNV2631_0_delta_p_qR;PPNV2631_1_bR",
            "NOT_CLOSED",
            "b_R=0 alone leaves gamma_obs-1=delta_p; no-boundary-charge is therefore the sharper gamma lever",
            "route next work to delta_p/q_R_hat parent-zero or finite row before any score",
        ),
        (
            "CERT2832_3_full_vector",
            "full PPN/local-GR certificate",
            "All active PPN components are theorem-zero or finite/source-backed in one convention; no cancellation identity is assumed.",
            "PPNV2631_8_total_abs;GUARD2831_0_no_gamma_only;GUARD2831_1_no_cancellation_shortcut",
            "NOT_CLOSED",
            "beta, preferred-frame, source-weight, endpoint/readout and q_loc channels remain open",
            "even a closed gamma combo would not be a local-GR proof",
        ),
    ]
    return [
        nonclaim(
            {
                "certificate_id": row_id,
                "target": target,
                "required_certificate": required,
                "source_anchors": anchors,
                "status": status,
                "blocker": blocker,
                "effect_if_closed": effect,
                "certificate_closed": False,
                "control_only": True,
            }
        )
        for row_id, target, required, anchors, status, blocker, effect in specs
    ]


def algebra_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ALG2832_0_combo",
            "gamma_obs_minus_1",
            "gamma_obs-1 = delta_p*(1+4*b_R)/(1-2*b_R*delta_p)",
            "derived symbolic combo from 2489",
            "PPNK2489_1_CR_delta_p_combo_kernel",
            "MISSING_b_R_VALUE_OR_ZERO;MISSING_delta_p_VALUE_OR_ZERO;MISSING_DENOMINATOR_GUARD",
        ),
        (
            "ALG2832_1_bR_zero_limit",
            "b_R=0 limit",
            "gamma_obs-1 -> delta_p",
            "no-Weyl alone does not close gamma",
            "PPNV2631_0_delta_p_qR;PPNV2631_1_bR",
            "MISSING_delta_p_VALUE_OR_ZERO",
        ),
        (
            "ALG2832_2_delta_p_zero_limit",
            "delta_p=0 limit",
            "gamma_obs-1 -> 0 with denominator -> 1",
            "no-boundary-charge/source descent closes this gamma combo even if b_R is finite",
            "NBC1884_1_exact_zero_flux_lemma;NBC1884_2_delta_p_consequence",
            "MISSING_PARENT_SIGNED_Q_R_ZERO_AND_SOURCE_DESCENT",
        ),
        (
            "ALG2832_3_qRhat_bridge",
            "finite q_R_hat bridge",
            "delta_p=-q_R_hat/2",
            "finite rows must source q_R_hat and delta_p in the same measured-GM convention",
            "NBC1884_3_qRhat_bridge;DPQR1884_2_delta_p;DPQR1884_3_GM_convention",
            "MISSING_NUMERIC_Q_R_HAT;MISSING_MEASURED_GM_SOURCE_CONVENTION",
        ),
        (
            "ALG2832_4_future_bound_inequality",
            "future comparator-only inequality",
            "|delta_p*(1+4*b_R)/(1-2*b_R*delta_p)| <= gamma_bound only after values and full-vector caveat are supplied",
            "formal inequality is not a prediction row",
            "GATE2489_2_ppn_gamma_score;GUARD2831_0_no_gamma_only",
            "MISSING_SOURCE_BACKED_VALUES;MISSING_FULL_VECTOR_CAVEAT",
        ),
        (
            "ALG2832_5_total_abs_guard",
            "full vector rule",
            "Delta_PPN_abs includes gamma combo plus every active beta/preferred/source/endpoint/readout/q_loc component",
            "gamma closure cannot replace local GR",
            "PPNV2631_8_total_abs",
            "MISSING_ALL_COMPONENT_VALUES_OR_THEOREM_ZEROS",
        ),
    ]
    return [
        nonclaim(
            {
                "algebra_id": row_id,
                "object": obj,
                "relation": relation,
                "interpretation": interpretation,
                "source_anchors": anchors,
                "missing_for_claim": missing,
                "algebra_ready": True,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for row_id, obj, relation, interpretation, anchors, missing in specs
    ]


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CON2832_0_route",
            "route_type",
            "parent_zero_delta_p | parent_zero_bR | finite_bR_delta_p_nonclaim",
            "closure_benchmark, comparator_only, gamma_only or cancellation_tuned",
            "declares whether the row is a theorem route or a finite residual route",
        ),
        (
            "CON2832_1_bR",
            "b_R",
            "parent-signed zero or finite dimensionless coefficient with source path and convention",
            "missing, placeholder, extracted from comparator bound alone, or no-Weyl asserted without parent action/readout signature",
            "b_R modulates the C_R common-Weyl gamma/readout channel",
        ),
        (
            "CON2832_2_delta_p",
            "delta_p",
            "parent-signed zero or finite number satisfying delta_p=-q_R_hat/2 when finite",
            "missing, inconsistent with q_R_hat, or zero because GR/Newton was assumed",
            "delta_p is the first-order spatial-curvature/reciprocal-lock input",
        ),
        (
            "CON2832_3_qRhat",
            "q_R_hat",
            "finite dimensionless q_R_hat=Q_R*c^2/(G*M_source) or parent-signed Q_R=0",
            "missing Q_R, missing measured-GM convention, or closure-only zero",
            "prevents gamma rows from mixing unrelated source normalizations",
        ),
        (
            "CON2832_4_denominator",
            "denominator_guard",
            "|1-2*b_R*delta_p| is explicitly nonzero for finite rows",
            "omitted when b_R or delta_p finite values are supplied",
            "keeps the gamma combo formula well-defined",
        ),
        (
            "CON2832_5_full_vector",
            "full_vector_status",
            "every non-gamma PPN component is theorem-zero or finite/source-backed before any PPN pass claim",
            "gamma-only, b_R-only, delta_p-only, or tuned cancellation rows",
            "protects local-GR reduction from one-channel overclaim",
        ),
        (
            "CON2832_6_claim_flags",
            "valid_for_claim; claim_allowed",
            "false in this checkpoint",
            "true while any source, value, theorem or full-vector clause is missing",
            "2832 is a private derivation/input-contract checkpoint",
        ),
    ]
    return [
        nonclaim(
            {
                "contract_id": row_id,
                "field": field,
                "accepted_content": accepted,
                "reject_if": reject,
                "reason": reason,
                "ready_for_future_row": True,
                "numeric_value_present": False,
                "source_backed_value": False,
                "theorem_zero": False,
                "control_only": True,
            }
        )
        for row_id, field, accepted, reject, reason in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2832_0_bR_not_enough", "b_R=0 is not a gamma pass unless delta_p is also closed or finite-bounded", "gamma_obs-1 -> delta_p when b_R=0", "redirects the next surgical target toward delta_p/q_R_hat"),
        ("GUARD2832_1_delta_p_sharp_lever", "delta_p=0 closes the symbolic gamma combo", "gamma_obs-1 -> 0 and denominator -> 1 when delta_p=0", "makes parent no-boundary-charge/source descent the cleanest gamma route"),
        ("GUARD2832_2_finite_convention", "finite b_R and delta_p rows must share the same source-normalized convention", "b_R, q_R_hat and GM/source normalization enter one formula", "blocks accidental mixing of unrelated coefficients"),
        ("GUARD2832_3_no_score", "no Cassini/gamma score from symbolic rows", "no source-backed b_R, delta_p or full-vector closure exists", "all score flags remain false"),
        ("GUARD2832_4_local_gr", "gamma closure is not local GR", "full PPN and local operator gates include beta, d_R, source, endpoint/readout and q_loc", "local-GR/Newton claim remains blocked"),
    ]
    return [
        nonclaim(
            {
                "guard_id": guard_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for guard_id, guard, because, effect in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    certificates_open = not any(row["certificate_closed"] for row in rows["certificate"])
    algebra_ready = all(row["algebra_ready"] and not row["numeric_value_present"] for row in rows["algebra"])
    contract_ready = all(row["ready_for_future_row"] and not row["numeric_value_present"] and not row["source_backed_value"] for row in rows["contract"])
    guards_active = all(row["guard_active"] for row in rows["guard"])
    specs = [
        ("GATE2832_0_sources", "all 2832 cited source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2832_1_bR_zero", "parent no-Weyl certificate sets b_R=0", False, "BLOCKED", "common-Weyl countermodel still survives; parent action/readout signature missing"),
        ("GATE2832_2_delta_p_zero", "parent no-boundary-charge/source descent sets delta_p=q_R_hat=0", False, "BLOCKED", "zero-flux lemma is exact but Q_R=0/source descent are not parent-signed"),
        ("GATE2832_3_gamma_combo", "gamma common-Weyl combo is a valid prediction row", False, "BLOCKED", "b_R/delta_p values or theorem zeros are missing and full-vector caveat remains open"),
        ("GATE2832_4_algebra", "gamma combo algebra and limit logic are recorded", algebra_ready, "PASS_INTERNAL_NONCLAIM" if algebra_ready else "BLOCKED", "relations are symbolic and nonclaim"),
        ("GATE2832_5_contract", "finite b_R/delta_p/q_R_hat acquisition contract is source-ready", contract_ready, "PASS_INTERNAL_NONCLAIM" if contract_ready else "BLOCKED", "future row fields and refusal rules are explicit"),
        ("GATE2832_6_guards", "no b_R-only, gamma-only, cancellation or local-GR shortcut survives", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "guard rows remain active"),
        ("GATE2832_7_certificates_open", "certificate rows remain open and unclaimed", certificates_open, "PASS_NONCLAIM" if certificates_open else "BLOCKED", "2832 does not overstate the derivation"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2832_0_bR", "b_R is not the master gamma switch by itself.", "B_R_ALONE_INSUFFICIENT", "setting b_R=0 leaves gamma_obs-1=delta_p", "do not spend the next pass trying to score b_R alone"),
        ("DEC2832_1_delta_p", "delta_p/q_R_hat is the sharper gamma lever.", "DELTAP_SELECTED", "delta_p=0 collapses the 2489 common-Weyl gamma combo cleanly", "go after parent no-boundary-charge/source descent or a finite q_R_hat row"),
        ("DEC2832_2_contract", "Finite route is now exact enough to accept real data later.", "FINITE_CONTRACT_READY_NONCLAIM", "required fields, relation, denominator guard and full-vector caveat are explicit", "future sourced values can be validated without rewriting the theory rule"),
        ("DEC2832_3_no_claim", "No PPN/gamma/local-GR claim is allowed.", "CLAIM_BLOCKED", "certificates are unsigned and no source-backed values exist", "keep all claim flags false"),
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
                "next_id": "NEXT2832_0_2833",
                "status": "selected_primary",
                "target_doc": "2833-Y5-R2FR-delta-p-qRhat-parent-zero-or-finite-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_delta_p_qRhat_parent_zero_or_finite_source_row_under_AX1090_2833.py",
                "mission": "attack delta_p/q_R_hat directly: either parent-sign Q_R=0/source descent from the no-boundary-charge route or create the first finite source-normalized q_R_hat row contract instance without scoring",
                "acceptance": "must cite 1884 zero-flux lemma, 2832 algebra, 2489 gamma combo and 2631 full-vector guard; no gamma score unless source-backed values and full-vector caveat exist; no local-GR claim",
                "forbidden": "do not treat b_R=0 as enough; do not use comparator bounds as predictions; do not set q_R_hat=0 by closure or GR import",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2832_0_contract_copy", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"], "local-bounds copy of finite b_R/delta_p/q_R_hat acquisition contract"),
        ("BR2832_1_algebra_copy", OUTPUTS["algebra"], BRANCH_OUTPUTS["algebra_copy"], "source-weight copy of gamma combo algebra and limit logic"),
        ("BR2832_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for delta_p/q_R_hat parent-zero or finite source row"),
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
    keys = {"source_path", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
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
    return True


def no_numeric_prediction_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "predicted_value", "coefficient_value", "alpha_bound", "lambda_value"}
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
        if path.is_file():
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
        ("VAL2832_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2832_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2832_2_certificates_unclaimed", not any(row["certificate_closed"] for row in rows_by_name["certificate"]), "no b_R/delta_p certificate is claimed"),
        ("VAL2832_3_algebra_symbolic", all(row["algebra_ready"] and not row["numeric_value_present"] for row in rows_by_name["algebra"]), "gamma combo algebra rows are symbolic and value-free"),
        ("VAL2832_4_contract_nonclaim", all(row["ready_for_future_row"] and not row["numeric_value_present"] and not row["source_backed_value"] and not row["theorem_zero"] for row in rows_by_name["contract"]), "finite acquisition contract is ready but contains no live value/theorem-zero"),
        ("VAL2832_5_guards_active", all(row["guard_active"] for row in rows_by_name["guard"]), "all shortcut guards remain active"),
        ("VAL2832_6_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows gamma, full PPN or local GR"),
        ("VAL2832_7_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2832_8_next_target_2833", any(row["next_id"] == "NEXT2832_0_2833" and row["selected"] for row in rows_by_name["next"]), "delta_p/q_R_hat parent-zero or finite source row selected next"),
        ("VAL2832_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2832_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2832_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2832_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2832_13_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2832_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2832_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2832_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2832_OVERALL",
            "passed": overall,
            "detail": "2832 proves the key branch logic: b_R=0 alone leaves gamma_obs-1=delta_p, while delta_p=0 collapses the symbolic common-Weyl gamma combo. It keeps all certificates unclaimed, writes a finite b_R/delta_p/q_R_hat acquisition contract, blocks scores, and selects delta_p/q_R_hat parent-zero or finite source row next.",
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
    content = f"""# 2832 - Y5 R2FR epsilon_vmq First Finite PPN Component Value Or Parent-Zero Certificate Under AX1090

Status: `Y5_R2FR_2832_bR_not_master_switch_delta_p_selected_no_claim`

## Private Verdict

2832 takes the promised `b_R/gamma` shot and finds a sharper route.

The algebra says:

```text
gamma_obs - 1 = delta_p (1 + 4 b_R) / (1 - 2 b_R delta_p)
```

So `b_R=0` is **not** enough; it leaves `gamma_obs-1 = delta_p`. The cleaner gamma lever is `delta_p/q_R_hat`. If the no-boundary-charge/source-descent route proves `delta_p=0`, the symbolic common-Weyl gamma combo collapses to zero regardless of finite `b_R`.

That is not a claim yet. The zero-flux lemma is exact, but the parent still has to sign `Q_R=0`, source descent, matter/readout descent, and projection silence. The finite fallback is now explicit: source `b_R`, `delta_p`, and `q_R_hat` in one measured-GM convention, with a denominator guard and full-vector caveat.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## b_R / delta_p Certificate Audit

{markdown_table(rows["certificate"], ["certificate_id", "target", "status", "blocker", "effect_if_closed", "certificate_closed", "valid_for_claim"])}

## Gamma Combo Algebra Ledger

{markdown_table(rows["algebra"], ["algebra_id", "object", "relation", "interpretation", "missing_for_claim", "algebra_ready", "valid_for_claim"])}

## Finite b_R / delta_p Acquisition Contract

{markdown_table(rows["contract"], ["contract_id", "field", "accepted_content", "reject_if", "reason", "ready_for_future_row", "valid_for_claim"])}

## Common Convention Guard

{markdown_table(rows["guard"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

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
    rows["certificate"] = certificate_rows()
    rows["algebra"] = algebra_rows()
    rows["contract"] = contract_rows()
    rows["guard"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "certificate", "algebra", "contract", "guard", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2832_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2832_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
