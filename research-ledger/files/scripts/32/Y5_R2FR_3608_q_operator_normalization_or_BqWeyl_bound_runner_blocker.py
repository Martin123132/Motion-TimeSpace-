from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3608"
BRANCH_ID = "MTS_R2FR_Y5_Q_OPERATOR_NORMALIZATION_OR_BQWEYL_RUNNER_BLOCKER_3608"
DOC = ROOT / "3608-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3607": (RESIDUALS / "P8_Y5_R2FR_3607_NEXT_TARGET.csv", "NEXT3607_0"),
        "status_3607": (
            RESIDUALS / "P8_Y5_R2FR_3607_STATUS.csv",
            "BQWEYL_PARENT_SIGNATURE_FAILED_FINITE_INPUT_PACK_STAGED",
        ),
        "finite_3607_zq": (
            RESIDUALS / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv",
            "BACQ3607_2_Zq",
        ),
        "finite_3607_dqweyl2": (
            RESIDUALS / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv",
            "BACQ3607_9_DqWeyl2_guard",
        ),
        "dqweyl2_input_contract": (RESIDUALS / "P8_Y5_R2FR_2754_DQWEYL2_INPUT_CONTRACT.csv", "IN2754_1_Zq"),
        "no_pole_gate": (
            RESIDUALS / "P8_Y5_R2FR_2755_NO_POLE_ACTIVATION_GATE.csv",
            "NP2755_5_activation_verdict",
        ),
        "qx_bridge_gate": (
            RESIDUALS / "P8_Y5_R2FR_2755_QX_BRIDGE_GATE.csv",
            "QXB2755_4_activation_verdict",
        ),
        "independent_q_hessian": (
            RESIDUALS / "P8_Y5_R2FR_2755_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv",
            "IQH2755_0_Zq",
        ),
        "independent_q_claim_gate": (
            RESIDUALS / "P8_Y5_R2FR_2755_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv",
            "IQH2755_5_claim_gate",
        ),
        "runner_activation": (
            RESIDUALS / "P8_Y5_R2FR_2755_DQWEYL2_RUNNER_ACTIVATION_GATE.csv",
            "DACT2755_3_bound_route",
        ),
        "weyl2_projection": (
            RESIDUALS / "P8_Y5_R2FR_2754_SCHWARZSCHILD_WEYL2_PROJECTION_GATE.csv",
            "PROJ2754_2_far_field",
        ),
        "bqweyl_bound_rows_3606": (RESIDUALS / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv", "BQB3606_1_BqWeyl"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3608_SOURCE_REGISTER.csv",
        "q_operator_route_audit": RESIDUALS / "P8_Y5_R2FR_3608_Q_OPERATOR_ROUTE_AUDIT.csv",
        "q_operator_input_rows": RESIDUALS / "P8_Y5_R2FR_3608_Q_OPERATOR_INPUT_ROWS.csv",
        "runner_blocker_gates": RESIDUALS / "P8_Y5_R2FR_3608_RUNNER_BLOCKER_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3608_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3608_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_q_operator_normalization_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3608_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def route_audit_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QROUTE3608_0_operator_identity",
            "q operator normal form",
            "L_q = -Z_q Delta_branch + M_q^2 + B_q^bdry + curvature/readout terms, with G_q=L_q^{-1} on a stated domain and norm",
            "DERIVED_CONDITIONAL_NORMAL_FORM",
            "This is algebraic bookkeeping from the Hessian; it does not assign numeric Z_q or a live Green function.",
            "dqweyl2_input_contract",
            False,
        ),
        (
            "QROUTE3608_1_no_pole_delete_route",
            "delete q row by quotient/no-pole theorem",
            "If q is a removed vertical/first-class coordinate and action, matter, boundary and readouts all descend, the physical Hessian has no q row/column.",
            "BLOCKED_BY_NP2755_5",
            "NP2755_1 through NP2755_4 are unsigned, so q cannot be deleted from the finite Weyl runner.",
            "no_pole_gate",
            False,
        ),
        (
            "QROUTE3608_2_qx_bridge_route",
            "borrow X operator through q=aX",
            "If q=aX with sourced nonzero scale a and identical domain/readout, then Z_q=Z_X/a^2, M_q^2=M_X^2/a^2, D_qWeyl2=D_XWeyl2/a.",
            "BLOCKED_BY_QXB2755_4",
            "The bridge identity, scale, units and X-side operator pack are not parent-owned.",
            "qx_bridge_gate",
            False,
        ),
        (
            "QROUTE3608_3_independent_hessian_route",
            "own q Hessian directly",
            "Use delta_q^2 S_parent to source Z_q, M_q^2/lambda_q, D_qWeyl2, J_q, boundary terms and P_arena in one normalization.",
            "BLOCKED_BY_IQH2755_5",
            "The independent source pack exists as a schema but all claim-grade numeric/source rows are missing.",
            "independent_q_claim_gate",
            False,
        ),
        (
            "QROUTE3608_4_weyl_runner_consequence",
            "linear and quadratic Weyl routes share G_q",
            "|q_arena| <= ||G_q||_arena (|B_qWeyl| ||P*C|| + |D_qWeyl2| ||C^2|| + ||J_q|| + boundary tails)",
            "RUNNER_NOT_EXECUTABLE",
            "The formula is now exact enough for a runner contract, but not executable until G_q/domain/norm and coefficients are real.",
            "runner_activation",
            False,
        ),
        (
            "QROUTE3608_5_decision",
            "q operator ownership verdict",
            "No route currently activates: no-pole deletion fails, q-X borrowing fails, and independent q Hessian sourcing is missing.",
            "Q_OPERATOR_NOT_OWNED_CURRENT_CORPUS",
            "Keep finite BqWeyl and D_qWeyl2 scoring blocked; next try must attack q deletion or fill the independent Hessian source pack.",
            "status_3607",
            False,
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": route_id,
            "route": route,
            "derived_contract": contract,
            "current_status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "route_activated": activated,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for route_id, route, contract, status, consequence, source_id, activated in rows
    ]


def input_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QIN3608_0_Zq",
            "Z_q",
            "kinetic/operator normalization in delta_q^2 S_parent",
            "operator_normalization",
            "MISSING_PARENT_HESSIAN_OR_BRIDGE",
            "needed for G_q normalization and every finite Weyl bound",
            "independent_q_hessian",
        ),
        (
            "QIN3608_1_Mq2_lambda",
            "M_q^2_or_lambda_q",
            "mass gap/range of q response",
            "mass_squared_or_length",
            "MISSING_RANGE_OR_NO_POLE_THEOREM",
            "needed to decide Coulomb-like, Yukawa, contact, or no-pole branch",
            "independent_q_hessian",
        ),
        (
            "QIN3608_2_domain",
            "D(L_q)",
            "function space and local branch domain for q",
            "domain_statement",
            "MISSING_DOMAIN",
            "needed before norms or Green functions are meaningful",
            "dqweyl2_input_contract",
        ),
        (
            "QIN3608_3_boundary",
            "B_q_boundary_condition",
            "boundary condition/interior matching for q",
            "boundary_statement",
            "MISSING_BOUNDARY_CONDITION",
            "needed to stop finite-body tails being smuggled into the operator",
            "no_pole_gate",
        ),
        (
            "QIN3608_4_norm",
            "||G_q||_arena",
            "operator norm convention for local arenas",
            "arena_norm",
            "MISSING_NORM_CONVENTION",
            "needed to compare R10, PPN, clock and orbital residuals",
            "runner_activation",
        ),
        (
            "QIN3608_5_BqWeyl",
            "B_qWeyl",
            "linear q-Weyl coefficient or zero theorem switch",
            "parent_normalized",
            "MISSING_COEFFICIENT_OR_ZERO_THEOREM",
            "needed for linear Weyl forcing term",
            "finite_3607_zq",
        ),
        (
            "QIN3608_6_DqWeyl2",
            "D_qWeyl2",
            "quadratic Weyl-source coefficient or no-tower theorem",
            "parent_normalized_length_power",
            "MISSING_COEFFICIENT_OR_NO_TOWER_THEOREM",
            "needed for C_abcd C^abcd guard",
            "finite_3607_dqweyl2",
        ),
        (
            "QIN3608_7_Jq",
            "J_q",
            "non-Weyl source, matter, boundary and readout tail",
            "source_density",
            "MISSING_SOURCE_ZERO_OR_BOUND",
            "needed to separate Weyl residual from matter/readout contamination",
            "independent_q_hessian",
        ),
        (
            "QIN3608_8_Parena",
            "P_arena[q]",
            "projection from q profile into R10/PPN/clocks/orbits",
            "arena_projection",
            "MISSING_OBSERVABLE_MAP",
            "needed before any empirical local bound can be claimed",
            "runner_activation",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "input_id": input_id,
            "symbol": symbol,
            "role": role,
            "units": units,
            "current_status": status,
            "why_needed": why_needed,
            "source_path": p[source_id],
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for input_id, symbol, role, units, status, why_needed, source_id in rows
    ]


def runner_gate_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "QRUN3608_0_linear_BqWeyl",
            "linear B_qWeyl finite runner",
            "BLOCKED",
            "requires B_qWeyl or Z_BqWeyl_linear=true plus Z_q/G_q, domain, boundary, norm, C_Weyl profile and arena projection",
            "finite_3607_zq",
        ),
        (
            "QRUN3608_1_quadratic_DqWeyl2",
            "quadratic Weyl guard runner",
            "BLOCKED",
            "requires D_qWeyl2 or no-tower theorem plus Z_q/G_q, M_q/lambda_q, C^2 profile, body cutoff and P_arena",
            "dqweyl2_input_contract",
        ),
        (
            "QRUN3608_2_no_pole",
            "delete q operator route",
            "BLOCKED",
            "requires parent quotient object, vertical generator, action/matter/readout descent and boundary/source silence",
            "no_pole_gate",
        ),
        (
            "QRUN3608_3_qx_borrow",
            "q-X bridge route",
            "BLOCKED",
            "requires q=aX, scale/units, shared domain/boundary/readout and X-side operator values",
            "qx_bridge_gate",
        ),
        (
            "QRUN3608_4_independent_q",
            "independent q Hessian route",
            "BLOCKED",
            "requires Z_q, M_q^2/lambda_q, D_qWeyl2, J_q and P_arena in one parent normalization",
            "independent_q_hessian",
        ),
        (
            "QRUN3608_5_acceptance",
            "finite local Weyl score",
            "REFUSED_CURRENT",
            "no finite score until one complete operator ownership route is activated and all live rows are source-backed",
            "runner_activation",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "requirement": requirement,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, requirement, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "Q_OPERATOR_NORMAL_FORM_DERIVED_BUT_NOT_OWNED",
            "strongest_result": "3608 pins the shared q operator contract: L_q=-Z_q Delta_branch+M_q^2+B_q^bdry+curvature/readout terms and G_q=L_q^{-1}. The same G_q gates both linear B_qWeyl and quadratic D_qWeyl2 residual scoring.",
            "decision": "do not run finite BqWeyl or D_qWeyl2 scoring; first activate no-pole deletion, q-X bridge borrowing, or independent q Hessian ownership",
            "still_missing": "Z_q, M_q^2/lambda_q, q domain, q boundary condition, q norm, B_qWeyl or zero theorem, D_qWeyl2 or no-tower theorem, J_q source-tail bound, and P_arena projections",
            "next_best_attack": "try q deletion/no-pole one more time at the parent-action level; if it cannot close, fill independent q Hessian rows rather than circling the same missing list",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["runner_activation"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3608_0",
            "target_doc": "3609-Y5-R2FR-q-no-pole-parent-action-certificate-or-independent-Hessian-fill.md",
            "target_script": "scripts/Y5_R2FR_3609_q_no_pole_parent_action_certificate_or_independent_Hessian_fill.py",
            "objective": "take the leap at the parent-action level: either prove q is quotient/vertical and delete the operator, or fill the independent q Hessian source rows enough to make the finite Weyl runner executable",
            "success_gate": "must produce a signed q-removal certificate or real rows for Z_q, M_q^2/lambda_q, domain, boundary, norm, source tail and P_arena; another missing-list-only pass is not acceptable",
            "reason": "3608 shows the operator normal form is clear; the remaining problem is ownership, not notation",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    route_rows: list[dict[str, object]],
    input_rows_: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3608_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3608 source paths exist"))
    validations.append(("VAL3608_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3608 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3608_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3608 csv outputs written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3608_3_csv_parse", parse_ok, "; ".join(parse_details)))
    route_names = {str(row["route"]) for row in route_rows}
    validations.append(
        (
            "VAL3608_4_three_routes_covered",
            {"delete q row by quotient/no-pole theorem", "borrow X operator through q=aX", "own q Hessian directly"}.issubset(route_names),
            "no-pole, q-X bridge, and independent Hessian routes audited",
        )
    )
    required_symbols = {"Z_q", "M_q^2_or_lambda_q", "D(L_q)", "B_q_boundary_condition", "||G_q||_arena", "B_qWeyl", "D_qWeyl2", "J_q", "P_arena[q]"}
    validations.append(
        (
            "VAL3608_5_required_inputs_present",
            required_symbols.issubset({str(row["symbol"]) for row in input_rows_}),
            "shared q-operator and Weyl-runner inputs present",
        )
    )
    validations.append(
        (
            "VAL3608_6_all_runner_gates_blocked",
            all(str(row["status"]) in {"BLOCKED", "REFUSED_CURRENT"} for row in runner_rows),
            "no finite runner is accidentally activated",
        )
    )
    validations.append(
        (
            "VAL3608_7_no_claim_flags",
            not any(str(row.get("claim_allowed", "False")) == "True" or str(row.get("valid_for_claim", "False")) == "True" for table in [route_rows, input_rows_, runner_rows, status, next_target] for row in table),
            "all generated physics rows remain nonclaim",
        )
    )
    validations.append(
        (
            "VAL3608_8_status_blocks_scoring",
            status[0]["status"] == "Q_OPERATOR_NORMAL_FORM_DERIVED_BUT_NOT_OWNED",
            "operator normal form is derived, ownership remains blocked",
        )
    )
    validations.append(
        (
            "VAL3608_9_next_target_selected",
            next_target[0]["next_id"] == "NEXT3608_0",
            "3609 parent-action/no-pole or independent-Hessian target selected",
        )
    )
    formalization_leaks: list[str] = []
    if FORMALIZATION.exists():
        for pattern in ["*3608*", "P8_Y5_R2FR_3608*", "P8_Y5_BRR545_3608*"]:
            formalization_leaks.extend(str(path) for path in FORMALIZATION.rglob(pattern) if ".venv" not in path.parts and "__pycache__" not in path.parts)
    validations.append(
        (
            "VAL3608_10_formalization_workbench_untouched",
            len(formalization_leaks) == 0,
            "no 3608 checkpoint output appears in formalization-workbench outside package/venv noise",
        )
    )
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    route_rows_: list[dict[str, object]],
    input_rows_: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    status_: list[dict[str, object]],
    next_target_: list[dict[str, object]],
    validation_: list[dict[str, object]],
) -> None:
    status_row = status_[0]
    lines = [
        "# 3608 - q operator normalization or BqWeyl bound runner blocker",
        "",
        "## Verdict",
        "3608 makes the `q` bottleneck sharper rather than merely repeating that rows are missing.",
        "",
        "The derived local operator contract is:",
        "",
        "`L_q = -Z_q Delta_branch + M_q^2 + B_q^bdry + curvature/readout terms`, with `G_q=L_q^{-1}` only after a domain, boundary condition, and norm are owned.",
        "",
        "That same `G_q` controls the finite linear `B_qWeyl` route and the quadratic `D_qWeyl2` guard:",
        "",
        "`|q_arena| <= ||G_q||_arena (|B_qWeyl| ||P*C|| + |D_qWeyl2| ||C^2|| + ||J_q|| + boundary tails)`.",
        "",
        "So the immediate win is conceptual: the route is now one operator problem, not two unrelated loose ends. The immediate block is also honest: no current source owns that operator.",
        "",
        "## Route Audit",
    ]
    for row in route_rows_:
        lines.append(f"- `{row['route_id']}` / `{row['route']}`: {row['current_status']} - {row['consequence']}")
    lines.extend(["", "## Required Inputs"])
    for row in input_rows_:
        lines.append(f"- `{row['input_id']}` / `{row['symbol']}`: {row['current_status']} - {row['why_needed']}")
    lines.extend(["", "## Runner Gates"])
    for row in runner_rows_:
        lines.append(f"- `{row['gate_id']}` / `{row['gate']}`: {row['status']} - {row['requirement']}")
    lines.extend(
        [
            "",
            "## Status",
            f"- `{status_row['status']}`: {status_row['strongest_result']}",
            f"- Decision: {status_row['decision']}",
            f"- Still missing: {status_row['still_missing']}",
            f"- Next best attack: {status_row['next_best_attack']}",
            "",
            "## Validation",
        ]
    )
    for row in validation_:
        lines.append(f"- `{row['validation_id']}`: {row['result']} ({row['detail']})")
    next_row = next_target_[0]
    lines.extend(
        [
            "",
            "## Next Target",
            f"- `{next_row['next_id']}` -> `{next_row['target_doc']}`",
            f"- Objective: {next_row['objective']}",
            f"- Success gate: {next_row['success_gate']}",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    source_rows = source_register_rows(source_map)
    route_rows_ = route_audit_rows(source_map)
    input_rows_ = input_rows(source_map)
    runner_rows_ = runner_gate_rows(source_map)
    status_ = status_rows(source_map)
    next_target_ = next_target_rows()

    write_csv(out_paths["source_register"], source_rows)
    write_csv(out_paths["q_operator_route_audit"], route_rows_)
    write_csv(out_paths["q_operator_input_rows"], input_rows_)
    write_csv(out_paths["runner_blocker_gates"], runner_rows_)
    write_csv(out_paths["status"], status_)
    write_csv(out_paths["next_target"], next_target_)
    write_csv(out_paths["canonical_status"], status_)

    validation_ = validation_rows(source_map, out_paths, route_rows_, input_rows_, runner_rows_, status_, next_target_)
    write_doc(route_rows_, input_rows_, runner_rows_, status_, next_target_, validation_)
    write_csv(out_paths["validation"], validation_)

    failures = [row for row in validation_ if row["result"] != "PASS"]
    if failures:
        for failure in failures:
            print(f"{failure['validation_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote 3608 q operator gate outputs under {RESIDUALS}")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
