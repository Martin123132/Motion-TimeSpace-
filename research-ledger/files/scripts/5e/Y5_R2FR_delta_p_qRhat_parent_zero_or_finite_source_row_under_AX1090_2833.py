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

DOC = ROOT / "2833-Y5-R2FR-delta-p-qRhat-parent-zero-or-finite-source-row-under-AX1090.md"

SRC_2832_NEXT = RESIDUALS / "P8_Y5_R2FR_2832_NEXT_TARGET.csv"
SRC_2832_ALGEBRA = RESIDUALS / "P8_Y5_R2FR_2832_GAMMA_COMBO_ALGEBRA_LEDGER.csv"
SRC_2832_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2832_FINITE_BR_DELTAP_ACQUISITION_CONTRACT.csv"
SRC_1884_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_AUDIT.csv"
SRC_1884_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_SOURCE_DESCENT_PREMISE_MATRIX.csv"
SRC_1884_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_INPUT_CONTRACT.csv"
SRC_1884_TEMPLATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_CANDIDATE_TEMPLATE_NONCLAIM.csv"
SRC_1884_DRYRUN = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_VALIDATOR_DRYRUN_RESULTS.csv"
SRC_2489_KERNEL = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv"
SRC_2631_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2833_SOURCE_REGISTER.csv",
    "parent_zero": RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_PARENT_ZERO_PROOF_AUDIT.csv",
    "finite_instance": RESIDUALS / "P8_Y5_R2FR_2833_FINITE_QRHAT_CONTRACT_INSTANCE_NONCLAIM.csv",
    "validator": RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_ROW_VALIDATOR_DRYRUN.csv",
    "gamma_interface": RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_TO_GAMMA_INTERFACE_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2833_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2833_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2833_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2833_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2833_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_copy": LOCAL_BOUNDS / "delta_p_qRhat_finite_contract_instance_2833_NONCLAIM.csv",
    "parent_zero_copy": SOURCE_WEIGHT / "delta_p_qRhat_parent_zero_audit_2833_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2833_RECIPROCAL_SOURCE_SILENCE_OR_TOPOLOGICAL_ZERO_NEXT.csv",
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
        ("SRC2833_0_2832_next", SRC_2832_NEXT, "NEXT2832_0_2833", "2832 selected delta_p/q_R_hat parent-zero or finite row"),
        ("SRC2833_1_2832_algebra", SRC_2832_ALGEBRA, "ALG2832_2_delta_p_zero_limit;ALG2832_3_qRhat_bridge", "2832 algebra selecting delta_p/q_R_hat as the sharp gamma lever"),
        ("SRC2833_2_2832_contract", SRC_2832_CONTRACT, "CON2832_2_delta_p;CON2832_3_qRhat;CON2832_5_full_vector", "2832 finite acquisition contract"),
        ("SRC2833_3_1884_audit", SRC_1884_AUDIT, "NBC1884_1_exact_zero_flux_lemma;NBC1884_3_qRhat_bridge;NBC1884_6_verdict", "1884 zero-flux lemma, q_R_hat bridge and current no-claim verdict"),
        ("SRC2833_4_1884_matrix", SRC_1884_MATRIX, "SDM1884_1_boundary_charge;SDM1884_2_source_silence;SDM1884_3_matter_action_descent;SDM1884_4_measure_connection_descent", "1884 missing parent-signature premise matrix"),
        ("SRC2833_5_1884_contract", SRC_1884_CONTRACT, "DPQR1884_1_qRhat;DPQR1884_2_delta_p;DPQR1884_6_descent_statuses", "1884 delta_p/q_R_hat validation contract"),
        ("SRC2833_6_1884_template", SRC_1884_TEMPLATE, "DPQR1884_TEMPLATE_PARENT_ZERO;DPQR1884_TEMPLATE_FINITE_QRHAT", "1884 candidate templates"),
        ("SRC2833_7_1884_dryrun", SRC_1884_DRYRUN, "CASE1884_1_missing_finite;CASE1884_4_zero_unsigned;CASE1884_5_gamma_only", "1884 validator refusal precedents"),
        ("SRC2833_8_2489_kernel", SRC_2489_KERNEL, "PPNK2489_1_CR_delta_p_combo_kernel", "2489 gamma combo kernel"),
        ("SRC2833_9_2631_vector", SRC_2631_VECTOR, "PPNV2631_0_delta_p_qR;PPNV2631_8_total_abs", "2631 delta_p and full-vector guard rows"),
    ]
    return [source_row(*spec) for spec in specs]


def parent_zero_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PZ2833_0_exterior_conservation",
            "Exterior reciprocal current has a conserved charge",
            "partial_r(W partial_r C_R)=J_R and J_R=0 outside source imply W partial_r C_R=Q_R",
            "NBC1884_0_exterior_field_equation",
            "DERIVED_CONDITIONAL",
            "This derives conservation, not Q_R=0.",
            True,
        ),
        (
            "PZ2833_1_zero_flux",
            "Zero flux would kill delta_p/q_R_hat",
            "If Q_R=0, W>0, J_R=0 exterior, C_R(infinity)=0, then C_R=0 and delta_p=0",
            "NBC1884_1_exact_zero_flux_lemma;NBC1884_2_delta_p_consequence",
            "EXACT_CONDITIONAL",
            "The missing premise is Q_R=0 from the parent theory.",
            True,
        ),
        (
            "PZ2833_2_boundary_charge",
            "Boundary charge theorem",
            "The reciprocal generator has zero/proper boundary charge for allowed local source class without imposing C_R=0 by hand",
            "SDM1884_1_boundary_charge;NBC1884_4_no_boundary_charge_parent_signature",
            "NOT_PARENT_SIGNED",
            "Exterior hair is allowed until the parent boundary term is proved zero.",
            False,
        ),
        (
            "PZ2833_3_source_silence",
            "Ordinary source reciprocal silence",
            "Ordinary matter carries no reciprocal/R_AB charge, so source current integrates to zero",
            "SDM1884_2_source_silence",
            "NOT_DERIVED",
            "This is the likely next theorem: source representation/topology must force zero reciprocal charge.",
            False,
        ),
        (
            "PZ2833_4_matter_readout_descent",
            "Matter/readout descent",
            "S_matter and observed rods/clocks descend to the quotient with no representative Weyl/disformal/source-prefactor residue",
            "SDM1884_3_matter_action_descent;SDM1884_4_measure_connection_descent",
            "NOT_DERIVED",
            "Even gamma closure is not full local GR unless readout/source/projection tails are killed or bounded.",
            False,
        ),
        (
            "PZ2833_5_parent_zero_verdict",
            "delta_p=q_R_hat=0 parent theorem",
            "Q_R=0, source silence, matter/readout descent and arena projection silence are all parent-signed in one package",
            "NBC1884_6_verdict;DPQR1884_6_descent_statuses",
            "NOT_CLOSED",
            "Zero rows remain unsigned and cannot be used as claims.",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "parent_zero_id": row_id,
                "target": target,
                "statement": statement,
                "source_anchors": anchors,
                "status": status,
                "proof_or_blocker": blocker,
                "conditional_piece_proved": conditional,
                "parent_zero_closed": False,
                "control_only": True,
            }
        )
        for row_id, target, statement, anchors, status, blocker, conditional in specs
    ]


def finite_instance_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "finite_instance_id": "FQ2833_0_first_contract_instance",
                "route_type": "finite_qR_hat_source_row_required",
                "delta_p": "UNSET_NUMERIC_DELTA_P_REQUIRED",
                "q_R_hat": "UNSET_NUMERIC_Q_R_HAT_REQUIRED",
                "relation": "delta_p=-q_R_hat/2",
                "relation_tolerance": "UNSET_TOLERANCE_REQUIRED",
                "units": "dimensionless",
                "GM_convention": "UNSET_MEASURED_GM_SOURCE_CONVENTION_REQUIRED",
                "source_path": "UNSET_SOURCE_PATH_REQUIRED",
                "source_id": "UNSET_SOURCE_ID_REQUIRED",
                "boundary_charge_status": "UNSET_OR_FINITE_CHARGE_BRANCH",
                "source_descent_status": "UNSET_SOURCE_BODY_REQUIRED",
                "matter_descent_status": "UNSIGNED_NONCLAIM",
                "projection_status": "UNSIGNED_NONCLAIM",
                "full_vector_ready": False,
                "closure_used": False,
                "comparator_only": False,
                "gamma_only": False,
                "cancellation_only": False,
                "control_only": True,
            }
        ),
        nonclaim(
            {
                "finite_instance_id": "FQ2833_1_parent_zero_template",
                "route_type": "parent_zero_theorem_required",
                "delta_p": "ZERO_ONLY_IF_PARENT_SIGNED",
                "q_R_hat": "ZERO_ONLY_IF_PARENT_SIGNED",
                "relation": "delta_p=-q_R_hat/2",
                "relation_tolerance": "not_applicable_until_parent_signed",
                "units": "dimensionless",
                "GM_convention": "not_required_for_zero_theorem_but_required_if_scored",
                "source_path": "UNSET_PARENT_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_THEOREM_PATH",
                "source_id": "UNSET_PARENT_SOURCE_ID",
                "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
                "source_descent_status": "MISSING_SOURCE_DESCENT",
                "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
                "projection_status": "MISSING_ARENA_PROJECTION",
                "full_vector_ready": False,
                "closure_used": False,
                "comparator_only": False,
                "gamma_only": False,
                "cancellation_only": False,
                "control_only": True,
            }
        ),
    ]


def is_number(value: Any) -> bool:
    try:
        float(str(value))
        return True
    except ValueError:
        return False


def validate_candidate(row: dict[str, Any]) -> tuple[str, bool, bool]:
    route = str(row.get("route_type", ""))
    if row.get("closure_used") or row.get("comparator_only") or row.get("gamma_only") or row.get("cancellation_only"):
        return "REFUSED_SHORTCUT_FLAG", False, False
    if route == "finite_qR_hat_source_row_required":
        if not is_number(row.get("delta_p")) or not is_number(row.get("q_R_hat")):
            return "REFUSED_MISSING_OR_NONNUMERIC_DELTA_P_OR_QRHAT", False, False
        if str(row.get("GM_convention", "")).startswith("UNSET") or str(row.get("source_path", "")).startswith("UNSET"):
            return "REFUSED_MISSING_GM_CONVENTION_OR_SOURCE_PATH", False, False
        delta_p = float(str(row["delta_p"]))
        q_r_hat = float(str(row["q_R_hat"]))
        if abs(delta_p + 0.5 * q_r_hat) > 1e-12:
            return "REFUSED_DELTA_P_QRHAT_RELATION_MISMATCH", False, False
        return "FINITE_SCHEMA_ONLY_NOT_CLAIM_READY", True, False
    if route == "parent_zero_theorem_required":
        missing_status = any(str(row.get(key, "")).startswith("MISSING_") for key in ["boundary_charge_status", "source_descent_status", "matter_descent_status", "projection_status"])
        if missing_status:
            return "REFUSED_PARENT_ZERO_THEOREM_UNSIGNED", False, False
        return "PARENT_ZERO_SCHEMA_ONLY_NOT_CLAIM_READY", True, False
    return "REFUSED_UNKNOWN_ROUTE_TYPE", False, False


def validator_rows(finite_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in finite_rows:
        status, valid_prediction_row, score_ready = validate_candidate(candidate)
        rows.append(
            nonclaim(
                {
                    "validator_id": f"VALRUN2833_{candidate['finite_instance_id']}",
                    "candidate_id": candidate["finite_instance_id"],
                    "route_type": candidate["route_type"],
                    "validator_status": status,
                    "schema_math_valid": valid_prediction_row,
                    "score_ready_internal": score_ready,
                    "reason": "2833 intentionally supplies contract instances without live source-backed values or parent-signed zero theorem",
                    "control_only": True,
                }
            )
        )
    return rows


def gamma_interface_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GI2833_0_parent_zero",
            "parent_zero_delta_p",
            "If Q_R=0 is parent-signed, q_R_hat=0 and delta_p=0, so gamma_obs-1=0 in the 2489 common-Weyl combo.",
            "MISSING_PARENT_SIGNED_Q_R_ZERO_SOURCE_DESCENT",
            "PPNK2489_1_CR_delta_p_combo_kernel;ALG2832_2_delta_p_zero_limit",
        ),
        (
            "GI2833_1_finite",
            "finite_qR_hat",
            "With finite q_R_hat, use delta_p=-q_R_hat/2 and gamma_obs-1=delta_p*(1+4*b_R)/(1-2*b_R*delta_p).",
            "MISSING_NUMERIC_Q_R_HAT;MISSING_NUMERIC_b_R;MISSING_DENOMINATOR_GUARD",
            "NBC1884_3_qRhat_bridge;ALG2832_3_qRhat_bridge;PPNK2489_1_CR_delta_p_combo_kernel",
        ),
        (
            "GI2833_2_score_guard",
            "full_vector_guard",
            "Gamma interface cannot be scored as local GR until Delta_PPN_abs includes every active PPN component.",
            "MISSING_FULL_VECTOR_COMPONENT_VALUES_OR_THEOREM_ZEROS",
            "PPNV2631_8_total_abs",
        ),
    ]
    return [
        nonclaim(
            {
                "interface_id": row_id,
                "route": route,
                "interface_statement": statement,
                "missing_for_claim": missing,
                "source_anchors": anchors,
                "interface_ready": True,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for row_id, route, statement, missing, anchors in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    parent_zero_blocked = not any(row["parent_zero_closed"] for row in rows["parent_zero"])
    finite_nonclaim = all(not row["full_vector_ready"] and not row["closure_used"] and not row["comparator_only"] for row in rows["finite_instance"])
    validator_refuses = all("REFUSED" in row["validator_status"] for row in rows["validator"])
    interface_nonclaim = all(row["interface_ready"] and not row["numeric_value_present"] for row in rows["gamma_interface"])
    specs = [
        ("GATE2833_0_sources", "all 2833 source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2833_1_parent_zero", "delta_p=q_R_hat=0 parent theorem is signed", False, "BLOCKED", "Q_R=0/source silence/matter descent/projection silence remain unsigned"),
        ("GATE2833_2_finite_row", "finite q_R_hat row is a valid prediction", False, "BLOCKED", "numeric q_R_hat, delta_p, GM convention and source path are unset"),
        ("GATE2833_3_validator_refusal", "validator refuses current contract instances", validator_refuses, "PASS_GUARDRAIL" if validator_refuses else "BLOCKED", "contract instances are intentionally nonclaim"),
        ("GATE2833_4_gamma_interface", "gamma interface is ready but value-missing", interface_nonclaim, "PASS_INTERNAL_NONCLAIM" if interface_nonclaim else "BLOCKED", "the formula route is explicit but not scored"),
        ("GATE2833_5_full_ppn", "full PPN/local-GR score is allowed", False, "BLOCKED", "full-vector components remain open"),
        ("GATE2833_6_parent_zero_blocked", "parent-zero rows remain unclaimed", parent_zero_blocked, "PASS_NONCLAIM" if parent_zero_blocked else "BLOCKED", "no closure or GR import used"),
        ("GATE2833_7_finite_nonclaim", "finite contract rows remain nonclaim", finite_nonclaim, "PASS_NONCLAIM" if finite_nonclaim else "BLOCKED", "no comparator/gamma/cancellation shortcut allowed"),
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
        ("DEC2833_0_conserved_not_zero", "Exterior conservation is not enough.", "Q_R_REMAINS_LIVE", "1884 derives W*C_R'=Q_R but does not set Q_R=0.", "do not mistake a conserved reciprocal charge for no charge"),
        ("DEC2833_1_parent_zero", "Parent-zero route has a single crisp missing theorem.", "SOURCE_SILENCE_SELECTED", "ordinary source reciprocal silence/topological zero is the missing clause with the biggest payoff.", "try to derive source_silence/topological reciprocal charge zero next"),
        ("DEC2833_2_finite_row", "Finite q_R_hat row is now instantiated as a nonclaim contract.", "CONTRACT_INSTANCE_READY_BUT_REFUSED", "validator correctly refuses it until numeric values and source convention exist.", "future data/model rows can plug into this schema"),
        ("DEC2833_3_no_score", "No gamma, full PPN or local-GR score is allowed.", "CLAIM_BLOCKED", "no parent zero and no source-backed finite row exists.", "keep all claim flags false"),
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
                "next_id": "NEXT2833_0_2834",
                "status": "selected_primary",
                "target_doc": "2834-Y5-R2FR-reciprocal-source-silence-or-topological-zero-charge-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_reciprocal_source_silence_or_topological_zero_charge_under_AX1090_2834.py",
                "mission": "try to derive ordinary-source reciprocal silence: prove rho_R/J_R integrates to zero from the source representation/topology, or keep Q_R finite and route to source-body acquisition without scoring",
                "acceptance": "must cite 1884 source-silence premise, 2833 parent-zero audit and gamma interface; no Q_R=0 claim unless source silence and boundary charge are parent-signed; no local-GR claim",
                "forbidden": "do not set Q_R=0 from asymptotic flatness alone; do not use closure lambda_R by hand; do not replace source silence with WEP or Ward slogans",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2833_0_finite_copy", OUTPUTS["finite_instance"], BRANCH_OUTPUTS["finite_copy"], "local-bounds copy of finite delta_p/q_R_hat contract instance"),
        ("BR2833_1_parent_zero_copy", OUTPUTS["parent_zero"], BRANCH_OUTPUTS["parent_zero_copy"], "source-weight copy of delta_p/q_R_hat parent-zero audit"),
        ("BR2833_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for reciprocal source silence/topological zero"),
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
                    if not item or item.startswith("http") or item.startswith("UNSET_") or item.startswith("MISSING_"):
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
        ("VAL2833_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2833_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2833_2_parent_zero_unclaimed", not any(row["parent_zero_closed"] for row in rows_by_name["parent_zero"]), "no parent-zero theorem is claimed"),
        ("VAL2833_3_finite_instances_nonclaim", all(not row["full_vector_ready"] and not row["closure_used"] and not row["comparator_only"] and not row["gamma_only"] and not row["cancellation_only"] for row in rows_by_name["finite_instance"]), "finite contract instances remain shortcut-free nonclaims"),
        ("VAL2833_4_validator_refuses", all("REFUSED" in row["validator_status"] and not row["schema_math_valid"] for row in rows_by_name["validator"]), "validator refuses current unset/unsigned rows"),
        ("VAL2833_5_gamma_interface_nonclaim", all(row["interface_ready"] and not row["numeric_value_present"] for row in rows_by_name["gamma_interface"]), "gamma interface is ready but value-missing"),
        ("VAL2833_6_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows gamma, full PPN or local GR"),
        ("VAL2833_7_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2833_8_next_target_2834", any(row["next_id"] == "NEXT2833_0_2834" and row["selected"] for row in rows_by_name["next"]), "reciprocal source silence/topological zero selected next"),
        ("VAL2833_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2833_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2833_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2833_12_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2833_13_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2833_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2833_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2833_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2833_OVERALL",
            "passed": overall,
            "detail": "2833 attacks delta_p/q_R_hat directly: it records the exact zero-flux conditional, refuses unsigned Q_R=0 and unset finite rows, writes a nonclaim q_R_hat contract instance and gamma interface, and selects reciprocal source silence/topological zero as the next theorem target.",
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
    content = f"""# 2833 - Y5 R2FR delta_p q_R_hat Parent-Zero Or Finite Source Row Under AX1090

Status: `Y5_R2FR_2833_delta_p_qRhat_contract_instance_source_silence_next_no_claim`

## Private Verdict

2833 attacks `delta_p/q_R_hat` directly.

The result is disciplined but useful: we have an exact conditional chain, not a proof yet.

```text
partial_r(W partial_r C_R)=J_R
J_R=0 outside source
=> W partial_r C_R = Q_R

Q_R=0 plus C_R(infinity)=0
=> C_R=0
=> delta_p=0
=> q_R_hat=0
```

The missing theorem is not the exterior calculation; that part is already clean. The missing theorem is why ordinary sources carry no reciprocal charge and why the boundary charge is zero in the parent action. So the next best shot is source silence / topological zero, not a Cassini score and not a hand-set closure.

2833 also writes the first finite `q_R_hat` contract instance, but the validator correctly refuses it because no numeric `q_R_hat`, no `delta_p`, no measured-GM convention, and no source path are present.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Parent-Zero Proof Audit

{markdown_table(rows["parent_zero"], ["parent_zero_id", "target", "status", "proof_or_blocker", "conditional_piece_proved", "parent_zero_closed", "valid_for_claim"])}

## Finite q_R_hat Contract Instance

{markdown_table(rows["finite_instance"], ["finite_instance_id", "route_type", "delta_p", "q_R_hat", "relation", "GM_convention", "source_path", "full_vector_ready", "valid_for_claim"])}

## q_R_hat Row Validator Dry Run

{markdown_table(rows["validator"], ["validator_id", "candidate_id", "validator_status", "schema_math_valid", "score_ready_internal", "reason", "valid_for_claim"])}

## q_R_hat To Gamma Interface

{markdown_table(rows["gamma_interface"], ["interface_id", "route", "interface_statement", "missing_for_claim", "interface_ready", "valid_for_claim"])}

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
    rows["parent_zero"] = parent_zero_rows()
    rows["finite_instance"] = finite_instance_rows()
    rows["validator"] = validator_rows(rows["finite_instance"])
    rows["gamma_interface"] = gamma_interface_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "parent_zero", "finite_instance", "validator", "gamma_interface", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2833_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2833_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
