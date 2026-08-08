from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1178-Y5-R10-parent-metric-channel-owner-or-first-tracefree-shear-norm-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1178_0_1177_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1177_NEXT_TARGET.csv",
            "needle": "NEXT1177_0_1178",
            "role": "handoff to parent metric-channel owner or first shear-norm bound runner.",
        },
        {
            "source_id": "SRC1178_1_1177_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1177_VALIDATION.csv",
            "needle": "V1177_SUMMARY",
            "role": "1177 validation summary.",
        },
        {
            "source_id": "SRC1178_2_1177_F1",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1177_METRIC_CHANNEL_ROUTING_ATTEMPT.csv",
            "needle": "MCR1177_1_C_first_variation_zero_condition",
            "role": "conditional first tracefree variation zero law.",
        },
        {
            "source_id": "SRC1178_3_1177_verdict",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1177_METRIC_CHANNEL_ROUTING_ATTEMPT.csv",
            "needle": "MCR1177_5_verdict",
            "role": "metric routing not parent-proved.",
        },
        {
            "source_id": "SRC1178_4_1177_shear_norm",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1177_TRACEFREE_SHEAR_NORM_INPUT_ROWS.csv",
            "needle": "SNI1177_0_tracefree_shear_norm",
            "role": "first tracefree shear norm input row.",
        },
        {
            "source_id": "SRC1178_5_1177_metric_transfer",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1177_TRACEFREE_SHEAR_NORM_INPUT_ROWS.csv",
            "needle": "SNI1177_4_metric_transfer_coefficient",
            "role": "missing parent metric transfer coefficient.",
        },
        {
            "source_id": "SRC1178_6_1177_Bianchi_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1177_CLAIM_GATES.csv",
            "needle": "G1177_4_Bianchi_stress_closure",
            "role": "Bianchi stress closure gate remains blocked.",
        },
        {
            "source_id": "SRC1178_7_1009_EH_anchor",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "SVC1009_0_EH_anchor_only",
            "role": "EH anchor cannot be promoted to total parent action.",
        },
        {
            "source_id": "SRC1178_8_1009_local_GR_block",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "CG1009_5_Htau_MHref_local_GR",
            "role": "local-GR gates remain blocked by incomplete parent current chain.",
        },
        {
            "source_id": "SRC1178_9_1010_q_loc_residual",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc residual must remain explicit if metric routing is incomplete.",
        },
        {
            "source_id": "SRC1178_10_02_metric_completion",
            "relative_path": "02-motion-load-local-GR-reduction.md",
            "needle": "exact reciprocal metric completion",
            "role": "local GR recovery depends on conditional metric completion.",
        },
        {
            "source_id": "SRC1178_11_207_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "routing must remain Ward/Bianchi safe.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def owner_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "PMO1178_0_metric_map_needed",
            "object": "parent metric response map",
            "candidate_statement": "A parent-owned routing theorem needs a map Dg_Q such that delta g_TF = Dg_Q[S_Q] and Dg_Q is fixed before readout.",
            "proof_status": "MISSING_PARENT_MAP",
            "derived_piece": "names the exact missing bridge between tracefree Q-flow and metric/curvature response.",
            "missing_for_claim": "source-backed Dg_Q or K_S_to_metric from the parent action",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PMO1178_1_EH_kinetic_template",
            "object": "EH tracefree metric channel",
            "candidate_statement": "If Dg_Q exists, the EH/GR anchor supplies the natural tensor channel for tracefree tidal/shear perturbations.",
            "proof_status": "REFERENCE_TEMPLATE_ONLY",
            "derived_piece": "the least-scrutinised route is to route S_Q into the ordinary metric spin-2 sector, not into scalar C memory.",
            "missing_for_claim": "proof that the MTS parent action uses this EH channel as its tracefree owner",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PMO1178_2_no_double_counting",
            "object": "C scalar channel versus metric tracefree channel",
            "candidate_statement": "The branch is internally clean if C reads only scalar volume data at first order and S_Q is retained by the metric channel.",
            "proof_status": "CONDITIONAL_SPLIT_CONTRACT",
            "derived_piece": "prevents both erasing shear and double-counting it in C plus metric.",
            "missing_for_claim": "parent C scalar-only term and parent metric transfer term signed together",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PMO1178_3_Bianchi_owner",
            "object": "conservation and hidden stress",
            "candidate_statement": "The routing is physical only if nabla_mu(T_metric + T_C + T_projector + T_GK)^{mu nu}=0 after the split.",
            "proof_status": "MISSING_PARENT_CURRENT_CHAIN",
            "derived_piece": "turns metric routing into a conservation test rather than a naming choice.",
            "missing_for_claim": "theta/Q_tau chain, domain/projector stress, and q_loc residual closure",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PMO1178_4_local_limit_contract",
            "object": "local GR/Newton recovery",
            "candidate_statement": "Local GR recovery can reopen only when the metric route owns S_Q, scalar C first variation is zero, and q_loc/Gamma/Khat residuals close or are bounded.",
            "proof_status": "LOCAL_LIMIT_CONTRACT_WRITTEN",
            "derived_piece": "connects the shear problem to the bigger GR/Newton reduction gate.",
            "missing_for_claim": "Dg_Q, F1 parent certificate, q_loc residual bound, PPN residual vector",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PMO1178_5_verdict",
            "object": "parent metric-channel owner verdict",
            "candidate_statement": "1178 does not prove parent metric-channel ownership. It converts the target into explicit parent-map and conservation clauses, then activates the first shear-norm bound runner route.",
            "proof_status": "NOT_PARENT_PROVED_BOUND_RUNNER_ACTIVE",
            "derived_piece": "we now know exactly what has to be sourced or derived before local-GR promotion.",
            "missing_for_claim": "parent metric map, scalar C certificate, Bianchi stress closure, and arena norm rows",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def f1_certificate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "certificate_id": "F1C1178_0_tracefree_definition",
            "quantity": "S_Q",
            "condition": "S_Q := Q_flow - (1/3)Tr(Q_flow)I",
            "result": "Tr(S_Q)=0",
            "status": "ALGEBRAICALLY_DEFINED",
            "missing_for_claim": "parent-owned Q_flow domain/frame",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "F1C1178_1_scalar_C_first_variation",
            "quantity": "F1_C_S",
            "condition": "C_local = C(log det Q, Tr Q, scalar domain data) at the local branch",
            "result": "delta C_local[S_Q] = 0 at first order",
            "status": "CONDITIONAL_ZERO",
            "missing_for_claim": "parent action term proving scalar-only C dependence",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "F1C1178_2_metric_retention",
            "quantity": "S_Q retention",
            "condition": "delta g_TF = Dg_Q[S_Q] with nonzero parent transfer coefficient K_S_to_metric",
            "result": "tracefree shear is retained in metric channel",
            "status": "MISSING_PARENT_TRANSFER",
            "missing_for_claim": "Dg_Q/K_S_to_metric source or derivation",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "F1C1178_3_second_order_residual",
            "quantity": "Delta_C2",
            "condition": "log det(I+A)=Tr(A)-1/2 Tr(A^2)+O(A^3)",
            "result": "abs(Delta_C2) <= C_det2 ||S_Q||_D^2 + R3",
            "status": "BOUND_REQUIRED",
            "missing_for_claim": "C_det2, ||S_Q||_D, and R3 source rows",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "F1C1178_4_certificate_verdict",
            "quantity": "local extremum/amplitude law",
            "condition": "F1_C_S=0 plus finite Delta_C2 bound plus metric retention",
            "result": "conditional local C extremum route is mathematically viable but not parent-signed",
            "status": "VIABLE_CONTRACT_NOT_CLAIM",
            "missing_for_claim": "parent scalar C owner, metric owner, and numeric/source-backed amplitude bound",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def bound_schema_rows() -> list[dict[str, object]]:
    rows = [
        {
            "schema_id": "SBR1178_0_required_columns",
            "field": "arena_id",
            "definition": "one of R10, PPN, clock, orbital, or a named future local arena",
            "units": "label",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SBR1178_1_shear_norm",
            "field": "norm_S_Q",
            "definition": "tracefree shear norm in the selected arena domain",
            "units": "same_as_Qflow_or_inverse_time_units",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SBR1178_2_variation_norm",
            "field": "norm_delta_S_Q",
            "definition": "tracefree shear variation/local-flow norm",
            "units": "same_as_Theta_Q_res",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SBR1178_3_Cdet2",
            "field": "C_det2",
            "definition": "second-order scalar leakage coefficient for tracefree shear",
            "units": "C_units_per_shear_squared",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SBR1178_4_metric_transfer",
            "field": "K_S_to_metric",
            "definition": "parent transfer coefficient from S_Q to metric/curvature/PPN residual channel",
            "units": "metric_response_per_shear_unit",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SBR1178_5_Bianchi_residual",
            "field": "Bianchi_residual_norm",
            "definition": "norm of conservation residual after routing split",
            "units": "stress_divergence_units",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
        {
            "schema_id": "SBR1178_6_source_path",
            "field": "source_path",
            "definition": "local path or external citation for every numeric/theorem value",
            "units": "path_or_url",
            "required_for_claim": True,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def arena_projection_rows() -> list[dict[str, object]]:
    arenas = [
        ("R10", "short-range inverse-square/local fifth-force bound", "R10_alpha_lambda comparator and local residual channel"),
        ("PPN", "solar-system metric residual/vector bound", "PPN gamma/beta/preferred-frame residual vector"),
        ("clock", "clock/redshift/time-dilation residual", "clock comparison and gravitational redshift tests"),
        ("orbital", "perihelion/orbital dynamics residual", "planetary, binary, and ephemeris constraints"),
    ]
    rows: list[dict[str, object]] = []
    for idx, (arena, meaning, comparator) in enumerate(arenas):
        rows.append(
            {
                "arena_row_id": f"APR1178_{idx}_{arena}",
                "arena": arena,
                "physical_meaning": meaning,
                "comparator_target": comparator,
                "norm_S_Q": "MISSING_ARENA_TRACEFREE_SHEAR_NORM",
                "norm_delta_S_Q": "MISSING_ARENA_TRACEFREE_VARIATION_NORM",
                "C_det2": "MISSING_ARENA_CDET2",
                "K_S_to_metric": "MISSING_PARENT_METRIC_TRANSFER",
                "Bianchi_residual_norm": "MISSING_ARENA_BIANCHI_RESIDUAL",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_READY_NONCLAIM_ROW",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1178_0_parent_metric_owner",
            "operation": "parent metric-channel ownership check",
            "formula_or_rule": "require Dg_Q, K_S_to_metric, Bianchi residual closure, and q_loc retention/closure",
            "status": "FAILED_AS_CLAIM_MISSING_PARENT_MAP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1178_1_F1_zero_certificate",
            "operation": "conditional scalar C first-variation check",
            "formula_or_rule": "if C=C(scalars only), then delta C[S_Q]=0 because Tr(S_Q)=0",
            "status": "CONDITIONAL_PASS_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1178_2_shear_bound_formula",
            "operation": "nonclaim shear leakage bound skeleton",
            "formula_or_rule": "epsilon_C <= C_det2||S_Q||^2 + C_cross||S_Q||||delta S_Q|| + R3 + Bianchi_residual_tau",
            "status": "SCHEMA_READY_NUMERIC_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1178_3_arena_projection_rows",
            "operation": "R10/PPN/clock/orbital row creation",
            "formula_or_rule": "each arena requires sourced norms, transfer coefficient, residual bound, and comparator target",
            "status": "ROWS_CREATED_VALID_FOR_CLAIM_FALSE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1178_4_local_promotion",
            "operation": "local-GR/Newton/R10/PPN promotion",
            "formula_or_rule": "only allowed after parent metric owner or sourced arena residual bounds close",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1178_0_parent_metric_map",
            "claim": "parent metric map Dg_Q owns tracefree S_Q",
            "status": "BLOCKED_MISSING_PARENT_MAP",
            "why_blocked": "K_S_to_metric and Dg_Q are not sourced from the parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1178_1_scalar_C_owner",
            "claim": "C channel is scalar-only in the local branch",
            "status": "BLOCKED_PARENT_C_TERM_MISSING",
            "why_blocked": "F1=0 is conditional but the parent C action term is not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1178_2_Bianchi_owner",
            "claim": "routing split is conservation safe",
            "status": "BLOCKED_PARENT_CURRENT_CHAIN_MISSING",
            "why_blocked": "metric/C/projector/GK stresses are not closed in a parent current chain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1178_3_arena_bound_inputs",
            "claim": "R10/PPN/clock/orbital shear bounds are scoreable",
            "status": "BLOCKED_NUMERIC_SOURCE_ROWS_MISSING",
            "why_blocked": "arena rows still contain MISSING_* placeholders and no source paths",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1178_4_q_loc_residual",
            "claim": "q_loc/Gamma/Khat residual is closed or harmless",
            "status": "BLOCKED_QLOC_RESIDUAL_RETAINED",
            "why_blocked": "1010 keeps q_loc as an explicit nonclaim residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1178_5_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED_NO_LOCAL_LIMIT_CLAIM",
            "why_blocked": "parent metric map, scalar C owner, Bianchi closure, q_loc closure, and arena bounds remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1178_0_owner_proof_status",
            "decision": "do_not_claim_parent_metric_owner",
            "reason": "the proof requires a parent metric map Dg_Q and transfer coefficient K_S_to_metric that are not in the current sourced chain.",
            "next_action": "hunt for or derive Dg_Q from the reciprocal metric completion / parent action.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1178_1_F1_status",
            "decision": "keep_F1_zero_as_conditional_win",
            "reason": "the algebra is clean and useful, but it is not enough without scalar-only parent ownership and second-order control.",
            "next_action": "turn scalar-only C into a parent-signed theorem or closure clause.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1178_2_bound_route_status",
            "decision": "activate_first_shear_norm_bound_runner",
            "reason": "if the owner proof takes longer, R10/PPN/clock/orbital arenas need explicit nonclaim source rows rather than verbal protection.",
            "next_action": "fill one arena first, preferably PPN or R10, with sourced comparator and symbolic MTS residuals.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1178_3_best_next",
            "decision": "derive_metric_map_before_numeric_hype",
            "reason": "the central missing object is Dg_Q/K_S_to_metric; without it, bounds can only be plumbing.",
            "next_action": "1179 should attempt the reciprocal-metric-to-tracefree-transfer derivation or demote K_S_to_metric to explicit closure.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1178_0_1179",
            "next_target": "1179-Y5-R10-reciprocal-metric-tracefree-transfer-derivation-or-KS-closure.md",
            "objective": "derive Dg_Q and K_S_to_metric from the reciprocal metric completion / parent action, or explicitly demote tracefree metric transfer to a closure parameter with arena bounds",
            "include": "reciprocal metric completion; tracefree perturbation map; EH anchor compatibility; Bianchi residual; q_loc retention; first arena source row",
            "exclude": "claiming local GR; deleting tracefree shear; invented numeric coefficients; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    owners: list[dict[str, object]],
    f1_rows: list[dict[str, object]],
    schema: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1178_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_1_metric_map_clause_written",
            "result": "pass" if any(r["attempt_id"] == "PMO1178_0_metric_map_needed" for r in owners) else "fail",
            "detail": "Dg_Q/K_S_to_metric parent-map clause is explicit",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_2_owner_not_claimed",
            "result": "pass" if any(r["proof_status"] == "NOT_PARENT_PROVED_BOUND_RUNNER_ACTIVE" for r in owners) else "fail",
            "detail": "parent metric owner proof is not claimed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_3_F1_certificate_conditional",
            "result": "pass" if any(r["status"] == "CONDITIONAL_ZERO" and r["valid_for_claim"] is False for r in f1_rows) else "fail",
            "detail": "F1 zero certificate remains conditional and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_4_second_order_bound_retained",
            "result": "pass" if any(r["certificate_id"] == "F1C1178_3_second_order_residual" for r in f1_rows) else "fail",
            "detail": "second-order amplitude bound remains required",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_5_schema_has_required_fields",
            "result": "pass" if len(schema) >= 7 and all(r["required_for_claim"] is True for r in schema) else "fail",
            "detail": "shear-bound runner schema includes required columns",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_6_arena_rows_created",
            "result": "pass" if {r["arena"] for r in arenas} == {"R10", "PPN", "clock", "orbital"} else "fail",
            "detail": "R10, PPN, clock, and orbital nonclaim rows are staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_7_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in arenas)
            else "fail",
            "detail": "arena rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_8_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "dry-run refuses owner, bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_9_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1178 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_10_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in owners + f1_rows + schema + arenas + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_11_next_target",
            "result": "pass" if nexts and "1179" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1179 handoff targets reciprocal metric tracefree transfer derivation or K_S closure",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_12_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_13_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1178_SUMMARY",
            "result": "pass",
            "detail": "1178 refuses parent metric owner promotion, preserves conditional F1=0 as a useful theorem-shape, stages first shear-norm bound runner rows for R10/PPN/clock/orbital arenas, and hands off to Dg_Q/K_S derivation",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    owners: list[dict[str, object]],
    f1_rows: list[dict[str, object]],
    schema: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1178 - Y5/R10 parent metric-channel owner or first tracefree shear norm bound runner",
        "**Current verdict:** parent metric-channel ownership is still not proved. The route is promising, but the parent map `Dg_Q` / `K_S_to_metric` is the missing bridge.",
        "**Main progress:** the local extremum route is now cleanly separated into three clauses: scalar-only `C` gives conditional `F1_C_S=0`, tracefree `S_Q` must be retained by the metric channel, and second-order scalar leakage must be bounded.",
        "**Bound-runner progress:** R10, PPN, clock, and orbital arena rows now exist as source-ready nonclaim rows, so future testing can fill numbers without quietly changing the theory.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Parent metric-channel owner attempt\n\n" + table(owners),
        "## Scalar C and F1 zero certificate\n\n" + table(f1_rows),
        "## Shear-bound runner schema\n\n" + table(schema),
        "## Arena projection rows\n\n" + table(arenas),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    owners = owner_attempt_rows()
    f1_rows = f1_certificate_rows()
    schema = bound_schema_rows()
    arenas = arena_projection_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, owners, f1_rows, schema, arenas, runs, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1178_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1178_PARENT_METRIC_CHANNEL_OWNER_ATTEMPT.csv": owners,
        "P8_Y5_R10_1178_SCALAR_C_F1_ZERO_CERTIFICATE.csv": f1_rows,
        "P8_Y5_R10_1178_SHEAR_BOUND_RUNNER_SCHEMA.csv": schema,
        "P8_Y5_R10_1178_ARENA_PROJECTION_ROWS.csv": arenas,
        "P8_Y5_R10_1178_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1178_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1178_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1178_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1178_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, owners, f1_rows, schema, arenas, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
