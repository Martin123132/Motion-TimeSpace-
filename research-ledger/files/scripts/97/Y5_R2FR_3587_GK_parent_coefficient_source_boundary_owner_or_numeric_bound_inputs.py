from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_GK_INPUT_OWNER_OR_NUMERIC_BOUND_3587"
CHECKPOINT_ID = "3587"
DOC = ROOT / "3587-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3586": RESIDUALS / "P8_Y5_R2FR_3586_NEXT_TARGET.csv",
        "status_3586": RESIDUALS / "P8_Y5_R2FR_3586_STATUS.csv",
        "theorem_3586": RESIDUALS / "P8_Y5_R2FR_3586_GK_COERCIVE_NOHAIR_THEOREM.csv",
        "bounds_3586": RESIDUALS / "P8_Y5_R2FR_3586_GK_HAIR_BOUND_ROWS.csv",
        "source_audit_3586": RESIDUALS / "P8_Y5_R2FR_3586_GK_SOURCE_CHARGE_ZERO_AUDIT.csv",
        "gk_operator_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_OPERATOR_ANSATZ.csv",
        "gk_coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "gk_eligibility_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
        "gk_bound_candidates_2475": RESIDUALS / "P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv",
        "gk_bound_rows_2475": RESIDUALS / "P8_Y5_GK_BOUND_SOURCE_2475_CANDIDATE_BOUND_ROWS.csv",
        "gk_units_2475": RESIDUALS / "P8_Y5_GK_BOUND_SOURCE_2475_UNITS_VALIDATION.csv",
        "qloc_interface_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv",
        "qloc_gate_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_DERIVATION_PROOF_GATE.csv",
        "noether_charge_2538": RESIDUALS / "P8_Y5_NO_SHADOW_2538_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv",
        "source_charge_owner_1793": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "boundary_cohom_549": RESIDUALS / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
        "projector_obstruction_549": RESIDUALS / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_OBSTRUCTION_LEDGER.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3587_SOURCE_REGISTER.csv",
        "input_owner_matrix": RESIDUALS / "P8_Y5_R2FR_3587_GK_INPUT_OWNER_MATRIX.csv",
        "candidate_bound_rows": RESIDUALS / "P8_Y5_R2FR_3587_GK_CANDIDATE_BOUND_INPUT_ROWS.csv",
        "runner_readiness": RESIDUALS / "P8_Y5_R2FR_3587_GK_RUNNER_READINESS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3587_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3587_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3587_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_GK_input_owner_or_numeric_bound_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3587_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3587 GK concrete input owner/acquisition source",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def input_owner_matrix_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GIO3587_0_lambda_GK",
            "lambda_GK",
            "min(Z_A lambda1_A + m_A2, Z_G lambda1_G + m_G2) - |c_AG| C_cross",
            "operator/coercivity owner",
            "requires Z_A,Z_G,m_A2,m_G2,c_AG,lambda1_A,lambda1_G,C_cross,domain_id,norm_id",
            "NOT_PARENT_SIGNED_NO_NUMERIC_VALUE",
            "gk_coercivity_2471",
        ),
        (
            "GIO3587_1_J_GK_norm",
            "J_GK_norm",
            "||(J_A,J_gamma)||_* in the dual of the selected GK operator domain",
            "source-current owner",
            "requires proof of J_GK=0 from parent matter/current grammar, or finite source norm with units",
            "NOT_PARENT_ZERO_NO_NUMERIC_VALUE",
            "source_audit_3586",
        ),
        (
            "GIO3587_2_Phi_boundary_GK",
            "Phi_boundary_GK",
            "absolute GK boundary flux from integration by parts in the selected annulus",
            "boundary/reference owner",
            "requires self-adjoint domain, fixed reference class, and no boundary/symplectic leakage or finite flux",
            "NOT_PARENT_ZERO_NO_NUMERIC_VALUE",
            "qloc_gate_2581",
        ),
        (
            "GIO3587_3_Q_top_GK",
            "Q_top_GK",
            "harmonic/topological/projector-kernel GK charge not controlled by local coercivity",
            "topology/projector owner",
            "requires relative cohomology/reference lock and P_loc kernel/gauge audit, or finite topology/projector norm",
            "NOT_PARENT_ZERO_NO_NUMERIC_VALUE",
            "boundary_cohom_549",
        ),
        (
            "GIO3587_4_epsilon_GK_hair",
            "epsilon_GK_hair",
            "K_GK * [(J_GK_norm + sqrt(J_GK_norm^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)]",
            "bound aggregator",
            "requires all four preceding inputs and K_GK; only valid on lambda_GK>0 branch",
            "FORMULA_READY_INPUTS_MISSING",
            "bounds_3586",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
            "symbol": symbol,
            "formula": formula,
            "owner_type": owner_type,
            "required_inputs": required_inputs,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for input_id, symbol, formula, owner_type, required_inputs, status, source_key in rows
    ]


def candidate_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GIB3587_0_lambda_GK_candidate",
            "lambda_GK",
            "operator lower-bound coefficient",
            "MISSING_NUMERIC_OR_PARENT_POSITIVE",
            "operator energy lower bound",
            "MISSING_PARENT_COEFFICIENTS:Z_A,Z_G,m_A2,m_G2,c_AG;MISSING_DOMAIN_CONSTANTS:lambda1_A,lambda1_G,C_cross",
            "gk_coercivity_2471",
        ),
        (
            "GIB3587_1_J_GK_norm_candidate",
            "J_GK_norm",
            "dual source norm for Gamma/Khat Euler source",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "dual operator/source norm",
            "MISSING_SOURCE_ZERO_THEOREM;MISSING_SOURCE_NORM_UNITS;NONHILBERT_CHANNELS_RETAINED",
            "qloc_interface_2581",
        ),
        (
            "GIB3587_2_Phi_boundary_GK_candidate",
            "Phi_boundary_GK",
            "absolute boundary/symplectic flux in GK integration by parts",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "field-energy boundary flux",
            "MISSING_SELF_ADJOINT_DOMAIN;MISSING_REFERENCE_LOCK;MISSING_BOUNDARY_FLUX_VALUE",
            "positive_pack_1846",
        ),
        (
            "GIB3587_3_Q_top_GK_candidate",
            "Q_top_GK",
            "topological/projector/gauge-kernel charge",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "field/topology/projector norm",
            "MISSING_RELATIVE_COHOMOLOGY_LOCK;MISSING_PROJECTOR_KERNEL_AUDIT;MISSING_GAUGE_FIX",
            "projector_obstruction_549",
        ),
        (
            "GIB3587_4_K_GK_candidate",
            "K_GK",
            "map from ||u_GK|| to selected observable residual envelope",
            "MISSING_NUMERIC_OR_OPERATOR_TO_OBSERVABLE_MAP",
            "observable conversion factor",
            "MISSING_METRIC_RESPONSE_MAP;MISSING_ARENA_PROJECTION;MISSING_UNITS",
            "gk_bound_candidates_2475",
        ),
        (
            "GIB3587_5_R10_external_bound_context",
            "alpha_bound(lambda)",
            "external R10 alpha(lambda) context exists as nonclaim anchor/review candidate",
            "SOURCE_BACKED_EXTERNAL_BOUND_CONTEXT_ONLY",
            "dimensionless alpha at lambda in meters",
            "THEORY_SIDE_GK_INPUTS_MISSING_SO_NO_SCORE",
            "gk_bound_rows_2475",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "candidate_value": candidate_value,
            "units": units,
            "block_reasons": block_reasons,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, definition, candidate_value, units, block_reasons, source_key in rows
    ]


def runner_readiness_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GRR3587_0_theorem_zero_route",
            "GK theorem-zero activation",
            "lambda_GK>0 and J_GK_norm=Phi_boundary_GK=Q_top_GK=0",
            "BLOCKED_CURRENT_CLAIM",
            "no parent-signed coefficient/source/boundary/topology package",
            "theorem_3586",
        ),
        (
            "GRR3587_1_finite_bound_route",
            "GK finite epsilon_GK_hair computation",
            "all candidate rows numeric, positive lambda_GK, K_GK sourced, units consistent",
            "BLOCKED_MISSING_INPUTS",
            "candidate rows retain MISSING markers",
            "bounds_3586",
        ),
        (
            "GRR3587_2_R10_runner_route",
            "R10 runner comparison",
            "E_GK_bound*C_metric*K_R10 <= alpha_bound(lambda)",
            "BLOCKED_THEORY_SIDE_INPUTS",
            "external alpha bound exists but E_GK_bound/C_metric/K_R10 are missing",
            "gk_bound_candidates_2475",
        ),
        (
            "GRR3587_3_claim_guard",
            "no local-GR/PPN/R10 claim",
            "claim=false unless all four GK inputs are parent-signed zero or finite sourced values",
            "PASS_GUARD",
            "prevents bound inversion and placeholder scoring",
            "gk_units_2475",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "readiness_id": readiness_id,
            "route": route,
            "condition": condition,
            "status": status,
            "reason": reason,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for readiness_id, route, condition, status, reason, source_key in rows
    ]


def gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3587_0_sources", "PASS", "all source paths and selected anchors exist", "next_3586"),
        ("GATE3587_1_input_matrix", "PASS", "lambda_GK, J_GK_norm, Phi_boundary_GK, Q_top_GK, and K_GK rows are staged", "bounds_3586"),
        ("GATE3587_2_parent_zero", "FAIL_CURRENT_CLAIM", "no input has parent-signed zero/positive proof sufficient for epsilon_GK_hair=0", "status_3586"),
        ("GATE3587_3_finite_values", "FAIL_CURRENT_SCORE", "finite rows still contain MISSING_NUMERIC_OR_PARENT markers", "gk_bound_candidates_2475"),
        ("GATE3587_4_external_bound", "PASS_CONTEXT_NONCLAIM", "R10 external anchor/review rows exist but cannot score missing theory-side GK inputs", "gk_bound_rows_2475"),
        ("GATE3587_5_no_bound_inversion", "PASS_GUARD", "external alpha bound is not used to define MTS GK coefficients", "gk_units_2475"),
        ("GATE3587_6_local_GR", "FAIL_CURRENT_CLAIM", "GK input fill alone does not solve remaining hair channels, E_stat, gauge/corner, GM calibration, or PPN closure", "status_3586"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "GK_INPUTS_STAGED_NOT_SIGNED_OR_NUMERIC",
            "strongest_result": "3587 converts the 3586 GK theorem/bound into concrete input rows: lambda_GK, J_GK_norm, Phi_boundary_GK, Q_top_GK, and K_GK. Existing evidence supplies formulas, source paths, units context, and blockers, but no parent-signed zero/positive package and no numeric theory-side values.",
            "still_missing": "parent coefficients Z_A,Z_G,m_A2,m_G2,c_AG; domain constants lambda1_A/lambda1_G/C_cross; source-zero or source norm; boundary/reference flux; topology/projector/gauge kernel; K_GK observable map; remaining local-GR gates",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3586"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3587_0",
            "target_doc": "3588-Y5-R2FR-GK-lambda-coefficient-signature-or-noncoercive-switch.md",
            "target_script": "scripts/Y5_R2FR_3588_GK_lambda_coefficient_signature_or_noncoercive_switch.py",
            "objective": "attack lambda_GK first: source/sign Z_A,Z_G,m_A2,m_G2,c_AG and domain constants, or switch the GK channel to the noncoercive finite branch with explicit inputs",
            "success_gate": "lambda_GK is parent-signed positive with source paths and units, or GIB3587_0 is demoted to noncoercive branch with named finite constants still nonclaim",
            "reason": "without positive lambda_GK the GK no-hair theorem and finite bound denominator cannot be used safely",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    owners: list[dict[str, object]],
    candidates: list[dict[str, object]],
    readiness: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3586": "NEXT3586_0",
        "status_3586": "GK_COERCIVE_CHANNEL_BOUND_FILLED_ZERO_THEOREM_CONDITIONAL",
        "theorem_3586": "GKC3586_3_zero_theorem",
        "bounds_3586": "GHB3586_4_epsilon_GK_hair",
        "source_audit_3586": "GSC3586_5_audit_verdict",
        "gk_operator_2471": "OP2471_0_stationary_energy",
        "gk_coercivity_2471": "COER2471_5_current_status",
        "gk_eligibility_2471": "NHG2471_5_eligibility",
        "gk_bound_candidates_2475": "RUN2475_R10_ANCHOR_INPUT",
        "gk_bound_rows_2475": "BOUND2475_R10_ANCHOR_ALPHA1_38P6UM",
        "gk_units_2475": "UNIT2475_RUN2475_R10_ANCHOR_INPUT",
        "qloc_interface_2581": "QLOC2581_3_Euler_source_gap",
        "qloc_gate_2581": "GK2581_6_boundary_silence",
        "noether_charge_2538": "NSCI2538_7_verdict",
        "source_charge_owner_1793": "Y5SC1793_7_verdict",
        "positive_pack_1846": "OP1846_3_self_adjoint_domain",
        "boundary_cohom_549": "BCT549_6_certificate_verdict",
        "projector_obstruction_549": "projector",
    }
    validations.append(("VAL3587_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3587 source paths exist"))
    validations.append(("VAL3587_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3587 anchors found"))
    validations.append(("VAL3587_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3587 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3587_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    required_symbols = {"lambda_GK", "J_GK_norm", "Phi_boundary_GK", "Q_top_GK", "K_GK"}
    validations.append(("VAL3587_4_required_inputs_present", required_symbols.issubset({str(row["symbol"]) for row in candidates}), "all concrete GK input candidate rows present"))
    validations.append(("VAL3587_5_missing_markers_retained", any("MISSING" in str(row["candidate_value"]) or "MISSING" in str(row["block_reasons"]) for row in candidates), "missing markers retained for unsigned inputs"))
    validations.append(("VAL3587_6_no_score_without_inputs", any(row["readiness_id"] == "GRR3587_2_R10_runner_route" and row["status"] == "BLOCKED_THEORY_SIDE_INPUTS" for row in readiness), "R10 scoring blocked until theory-side inputs exist"))
    validations.append(("VAL3587_7_no_bound_inversion", any(row["gate_id"] == "GATE3587_5_no_bound_inversion" and row["status"] == "PASS_GUARD" for row in gates), "external bounds not inverted into coefficients"))
    validations.append(("VAL3587_8_parent_claim_blocked", any(row["gate_id"] == "GATE3587_2_parent_zero" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "parent zero remains blocked"))
    validations.append(("VAL3587_9_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" for row in owners + candidates + readiness + gates + status + next_target), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3587_10_next_target_selected", any(row["next_id"] == "NEXT3587_0" for row in next_target), "lambda_GK next target selected"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in owners + candidates + readiness + gates + status)
    validations.append(("VAL3587_11_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3587*")) or any(FORMALIZATION.rglob("3587-Y5-R2FR*"))
    validations.append(("VAL3587_12_formalization_workbench_untouched", not formalization_touched, "no 3587 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    owners: list[dict[str, object]],
    candidates: list[dict[str, object]],
    readiness: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3587 — GK parent coefficient/source/boundary owner or numeric bound inputs",
        "",
        "## Verdict",
        "3587 tries the concrete GK input-fill step from 3586.  It does not find claim-grade parent-signed or numeric values, but it converts every GK theorem input into an explicit owner/acquisition row:",
        "",
        "`lambda_GK`, `J_GK_norm`, `Phi_boundary_GK`, `Q_top_GK`, and `K_GK`.",
        "",
        "The external R10 bound context exists, but the theory-side GK inputs are still missing, so scoring remains blocked.  This is useful because the next target is now exact: attack `lambda_GK` first or switch the GK channel to the noncoercive branch.",
        "",
        "## Input owner matrix",
    ]
    for row in owners:
        lines.append(f"- `{row['input_id']}` `{row['symbol']}`: {row['status']} — {row['required_inputs']}")
    lines.extend(["", "## Candidate bound rows"])
    for row in candidates:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['candidate_value']} ({row['block_reasons']})")
    lines.extend(["", "## Runner readiness"])
    for row in readiness:
        lines.append(f"- `{row['readiness_id']}`: {row['status']} ({row['reason']})")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    owners = input_owner_matrix_rows(source_paths)
    candidates = candidate_bound_rows(source_paths)
    readiness = runner_readiness_rows(source_paths)
    gates = gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "input_owner_matrix": owners,
        "candidate_bound_rows": candidates,
        "runner_readiness": readiness,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, owners, candidates, readiness, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(owners, candidates, readiness, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3587 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
