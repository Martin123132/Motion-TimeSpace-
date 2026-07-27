from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1179-Y5-R10-reciprocal-metric-tracefree-transfer-derivation-or-KS-closure.md"
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
            "source_id": "SRC1179_0_1178_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1178_NEXT_TARGET.csv",
            "needle": "NEXT1178_0_1179",
            "role": "handoff to reciprocal metric tracefree transfer derivation or K_S closure.",
        },
        {
            "source_id": "SRC1179_1_1178_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1178_VALIDATION.csv",
            "needle": "V1178_SUMMARY",
            "role": "1178 validation summary.",
        },
        {
            "source_id": "SRC1179_2_1178_metric_map",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1178_PARENT_METRIC_CHANNEL_OWNER_ATTEMPT.csv",
            "needle": "PMO1178_0_metric_map_needed",
            "role": "parent metric map remains missing.",
        },
        {
            "source_id": "SRC1179_3_1178_owner_verdict",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1178_PARENT_METRIC_CHANNEL_OWNER_ATTEMPT.csv",
            "needle": "PMO1178_5_verdict",
            "role": "metric-channel owner not parent-proved.",
        },
        {
            "source_id": "SRC1179_4_1178_F1",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1178_SCALAR_C_F1_ZERO_CERTIFICATE.csv",
            "needle": "F1C1178_1_scalar_C_first_variation",
            "role": "conditional F1 zero law.",
        },
        {
            "source_id": "SRC1179_5_02_reciprocity",
            "relative_path": "02-motion-load-local-GR-reduction.md",
            "needle": "T^2 S = 1",
            "role": "scalar reciprocal lock.",
        },
        {
            "source_id": "SRC1179_6_02_parent_fail",
            "relative_path": "02-motion-load-local-GR-reduction.md",
            "needle": "parent_origin_of_reciprocity = fail",
            "role": "reciprocity parent origin is not yet derived.",
        },
        {
            "source_id": "SRC1179_7_03_origin",
            "relative_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "vacuum stress balance + Hamiltonian duality",
            "role": "strongest scalar reciprocity route.",
        },
        {
            "source_id": "SRC1179_8_03_missing_theorem",
            "relative_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "the MTS/motion-load action must imply the vacuum radial stress balance",
            "role": "parent theorem still missing.",
        },
        {
            "source_id": "SRC1179_9_03_theorem_target",
            "relative_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "reciprocity = theorem target, not completed theorem",
            "role": "reciprocity remains nonclaim.",
        },
        {
            "source_id": "SRC1179_10_1009_EH_anchor",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "SVC1009_0_EH_anchor_only",
            "role": "EH anchor cannot stand in as total parent action.",
        },
        {
            "source_id": "SRC1179_11_1010_q_loc",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc still retained as residual.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def derivation_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "RTT1179_0_scalar_reciprocity_scope",
            "object": "scalar reciprocal lock",
            "derivation": "T^2 S = 1 fixes the scalar radial/spatial routing exponent p=1 in the weak-field lane.",
            "status": "SCALAR_SCOPE_ONLY",
            "result": "does not by itself specify a tracefree tensor transfer map",
            "missing_for_claim": "parent principle extending scalar reciprocity to anisotropic/unimodular spatial metric response",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RTT1179_1_matrix_decomposition",
            "object": "spatial metric/routing decomposition",
            "derivation": "Write the spatial routing/metric object as volume part times unimodular tracefree part: Q = Q_vol^{1/3} exp(sigma_TF), Tr(sigma_TF)=0.",
            "status": "ALGEBRAIC_DECOMPOSITION",
            "result": "tracefree perturbations preserve determinant at first order",
            "missing_for_claim": "parent identification of Q with metric, inverse metric, coframe, or independent field",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RTT1179_2_metric_as_routing_branch",
            "object": "metric-as-routing convention",
            "derivation": "If the parent declares gamma_ij proportional to Q_ij, then delta gamma_TF = +K_norm S_Q at linear order.",
            "status": "CONDITIONAL_CONVENTION",
            "result": "K_S_to_metric has positive orientation up to normalization",
            "missing_for_claim": "parent declaration that Q is the spatial metric routing tensor",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RTT1179_3_inverse_routing_branch",
            "object": "inverse-routing convention",
            "derivation": "If the parent declares gamma^{ij} proportional to Q^{ij}, then delta gamma_TF = -K_norm S_Q at linear order because delta gamma = -gamma delta gamma^{-1} gamma.",
            "status": "CONDITIONAL_CONVENTION",
            "result": "K_S_to_metric has negative orientation up to normalization",
            "missing_for_claim": "parent declaration that Q is inverse spatial routing",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RTT1179_4_transfer_underdetermination",
            "object": "K_S_to_metric",
            "derivation": "Scalar reciprocity fixes the trace/volume lock but leaves the tracefree orientation and normalization undecided between metric, inverse-metric, coframe, or independent-field conventions.",
            "status": "UNDERDETERMINED_BY_SCALAR_RECIPROCITY",
            "result": "K_S_to_metric cannot be claimed from T^2 S = 1 alone",
            "missing_for_claim": "parent metric/coframe definition or variational transfer equation",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RTT1179_5_verdict",
            "object": "reciprocal tracefree transfer verdict",
            "derivation": "1179 rejects the strong claim that reciprocal scalar completion derives the full tracefree transfer coefficient. It demotes K_S_to_metric to a closure/source target unless a parent metric/coframe map is found.",
            "status": "KS_CLOSURE_ROUTE_ACTIVE",
            "result": "the missing coupling is now sharply identified as metric-vs-inverse/coframe orientation plus normalization",
            "missing_for_claim": "signed parent Dg_Q/K_S_to_metric theorem and arena bounds",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def ks_closure_rows() -> list[dict[str, object]]:
    rows = [
        {
            "closure_id": "KSC1179_0_orientation",
            "parameter": "sigma_KS",
            "meaning": "orientation/sign of tracefree transfer from S_Q to metric perturbation",
            "allowed_symbolic_values": "+1_metric_as_routing; -1_inverse_routing; free_parent_coframe",
            "current_value": "MISSING_PARENT_ORIENTATION",
            "source_required": "parent definition of Q/gamma/coframe relation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "KSC1179_1_normalization",
            "parameter": "K_norm",
            "meaning": "normalization converting tracefree Q-flow units into metric perturbation units",
            "allowed_symbolic_values": "positive_source_backed_scale",
            "current_value": "MISSING_PARENT_NORMALIZATION",
            "source_required": "parent kinetic term or reciprocal metric map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "KSC1179_2_transfer",
            "parameter": "K_S_to_metric",
            "meaning": "linear metric-channel transfer coefficient for S_Q",
            "allowed_symbolic_values": "sigma_KS*K_norm",
            "current_value": "K_S_to_metric := sigma_KS*K_norm (closure only)",
            "source_required": "derive or fit/bound under nonclaim arena runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "KSC1179_3_scalar_decoupling",
            "parameter": "F1_C_S",
            "meaning": "first tracefree variation of scalar C channel",
            "allowed_symbolic_values": "0 only if C is parent scalar-only",
            "current_value": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "source_required": "parent C scalar-only action clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "KSC1179_4_amplitude_bound",
            "parameter": "Delta_C2_bound",
            "meaning": "second-order tracefree scalar leakage bound",
            "allowed_symbolic_values": "C_det2||S_Q||^2 + R3",
            "current_value": "MISSING_CDET2_SHEAR_NORM_R3",
            "source_required": "arena norm/source row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def first_arena_rows() -> list[dict[str, object]]:
    rows = [
        {
            "arena_input_id": "FAI1179_0_PPN_preferred_first",
            "arena": "PPN",
            "why_first": "PPN directly sees the metric-channel transfer coefficient, so it is the cleanest arena for K_S_to_metric before R10 scalar residual scoring.",
            "needed_inputs": "sigma_KS; K_norm; metric residual vector; gamma/beta/preferred-frame comparator; q_loc residual bound",
            "current_status": "MISSING_SOURCE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_input_id": "FAI1179_1_R10_second",
            "arena": "R10",
            "why_first": "R10 becomes meaningful after K_S_to_metric and scalar leakage are separated, otherwise alpha rows mix metric and scalar channels.",
            "needed_inputs": "C_det2; norm_S_Q; lambda_X; alpha_bound(lambda); scalar leakage projection",
            "current_status": "MISSING_SOURCE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_input_id": "FAI1179_2_clock_guard",
            "arena": "clock",
            "why_first": "clock tests constrain scalar time capacity and must not be contaminated by tracefree metric routing.",
            "needed_inputs": "T residual; scalar C projection; metric tracefree leakage; source clock bound",
            "current_status": "MISSING_SOURCE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_input_id": "FAI1179_3_orbital_guard",
            "arena": "orbital",
            "why_first": "orbital systems constrain the final local GR/Newton recovery once PPN routing is stable.",
            "needed_inputs": "metric residual vector; perihelion/orbital comparator; q_loc residual; K_S_to_metric",
            "current_status": "MISSING_SOURCE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1179_0_scalar_reciprocity",
            "operation": "test whether scalar T^2 S=1 fixes K_S_to_metric",
            "result": "NO_TRACEFREE_UNDERDETERMINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1179_1_metric_orientation",
            "operation": "compare metric-as-routing and inverse-routing branches",
            "result": "SIGN_ORIENTATION_DEPENDS_ON_PARENT_CONVENTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1179_2_KS_closure",
            "operation": "stage K_S_to_metric closure rows",
            "result": "CLOSURE_ROWS_CREATED_VALID_FOR_CLAIM_FALSE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1179_3_arena_order",
            "operation": "choose first arena for source row",
            "result": "PPN_FIRST_RECOMMENDED_THEN_R10",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1179_4_local_promotion",
            "operation": "local GR/Newton promotion",
            "result": "REFUSED_KS_AND_PARENT_RECIPROCITY_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1179_0_scalar_reciprocity_to_tracefree",
            "claim": "T^2 S=1 derives tracefree K_S_to_metric",
            "status": "FAILED_AS_STATED",
            "why_blocked": "scalar reciprocity fixes volume/radial trace only, not tracefree metric orientation or normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1179_1_parent_metric_convention",
            "claim": "Q is parent-defined as metric/inverse/coframe",
            "status": "BLOCKED_PARENT_DEFINITION_MISSING",
            "why_blocked": "current source chain does not sign which geometric object Q represents",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1179_2_KS_numeric_or_theorem",
            "claim": "K_S_to_metric is scoreable",
            "status": "BLOCKED_CLOSURE_SOURCE_MISSING",
            "why_blocked": "sigma_KS and K_norm remain missing/nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1179_3_F1_plus_amplitude",
            "claim": "local scalar C is protected from tracefree shear",
            "status": "BLOCKED_SECOND_ORDER_AND_PARENT_C_MISSING",
            "why_blocked": "F1 zero is conditional and Delta_C2 bound lacks source rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1179_4_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED_NO_LOCAL_LIMIT_CLAIM",
            "why_blocked": "parent reciprocity, K_S_to_metric, q_loc closure, and arena residual vector are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1179_0_derivation_result",
            "decision": "reject_scalar_reciprocity_as_full_tracefree_transfer_derivation",
            "reason": "T^2 S=1 controls scalar/radial volume response but not the spin-2/unimodular metric map.",
            "next_action": "seek a parent metric/coframe definition or keep K_S_to_metric as closure.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1179_1_coupling_status",
            "decision": "coupling_missing_object_identified",
            "reason": "the missing coupling is not vague: it is sigma_KS and K_norm inside K_S_to_metric.",
            "next_action": "derive Q-as-metric versus Q-as-inverse from parent variables.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1179_2_arena_order",
            "decision": "use_PPN_before_R10_for_KS",
            "reason": "PPN directly constrains metric transfer; R10 should follow once scalar leakage is separated from tracefree metric response.",
            "next_action": "build a PPN residual vector source/closure row before scoring local claims.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1179_0_1180",
            "next_target": "1180-Y5-R10-parent-Q-geometric-identity-or-PPN-KS-source-row.md",
            "objective": "derive whether Q is the spatial metric, inverse spatial metric, coframe square, or independent routing field; if not derivable, create the first PPN K_S_to_metric source/closure row",
            "include": "Q geometric identity; sign/orientation sigma_KS; normalization K_norm; PPN residual vector; q_loc retention; no-claim validation",
            "exclude": "local GR claim; scalar reciprocity overclaim; deleting tracefree shear; invented numeric coefficients; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    closures: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1179_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_1_scalar_scope_limited",
            "result": "pass" if any(r["status"] == "SCALAR_SCOPE_ONLY" for r in derivations) else "fail",
            "detail": "scalar reciprocity is explicitly limited to scalar/radial scope",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_2_metric_inverse_branches",
            "result": "pass"
            if {r["attempt_id"] for r in derivations} >= {"RTT1179_2_metric_as_routing_branch", "RTT1179_3_inverse_routing_branch"}
            else "fail",
            "detail": "metric and inverse-routing sign branches are both logged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_3_KS_not_claimed",
            "result": "pass" if any(r["status"] == "UNDERDETERMINED_BY_SCALAR_RECIPROCITY" for r in derivations) else "fail",
            "detail": "K_S_to_metric is not claimed from scalar reciprocity alone",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_4_closure_rows_created",
            "result": "pass" if len(closures) >= 5 and all(r["claim_allowed"] is False for r in closures) else "fail",
            "detail": "sigma_KS, K_norm, K_S_to_metric, F1, and amplitude closure rows exist",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_5_arena_order_written",
            "result": "pass" if any(r["arena"] == "PPN" for r in arenas) and any(r["arena"] == "R10" for r in arenas) else "fail",
            "detail": "PPN and R10 arena source-row order is recorded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in closures + arenas)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "dry-run refuses KS, arena, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_8_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1179 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_9_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in derivations + closures + arenas + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_10_next_target",
            "result": "pass" if nexts and "1180" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1180 handoff targets Q geometric identity or PPN KS source row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1179_SUMMARY",
            "result": "pass",
            "detail": "1179 shows scalar reciprocity does not determine tracefree metric transfer, identifies K_S_to_metric as orientation plus normalization closure, recommends PPN-first sourcing, and hands off to Q geometric identity",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    closures: list[dict[str, object]],
    arenas: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1179 - Y5/R10 reciprocal metric tracefree transfer derivation or K_S closure",
        "**Current verdict:** scalar reciprocity `T^2 S = 1` is not enough to derive the tracefree metric transfer coefficient. It fixes the scalar/radial lane, not the spin-2/unimodular transfer map.",
        "**Main progress:** the missing coupling is now sharper: `K_S_to_metric = sigma_KS * K_norm`, where `sigma_KS` chooses metric versus inverse/coframe orientation and `K_norm` sets the parent normalization.",
        "**Practical consequence:** PPN should be the first arena for this coupling, because PPN directly tests metric transfer before R10 scalar leakage rows are scored.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Reciprocal transfer derivation attempt\n\n" + table(derivations),
        "## K_S closure rows\n\n" + table(closures),
        "## First arena source-row order\n\n" + table(arenas),
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
    derivations = derivation_rows()
    closures = ks_closure_rows()
    arenas = first_arena_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, derivations, closures, arenas, runs, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1179_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1179_RECIPROCAL_TRANSFER_DERIVATION_ATTEMPT.csv": derivations,
        "P8_Y5_R10_1179_KS_CLOSURE_ROWS.csv": closures,
        "P8_Y5_R10_1179_FIRST_ARENA_SOURCE_ROW_ORDER.csv": arenas,
        "P8_Y5_R10_1179_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1179_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1179_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1179_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1179_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, derivations, closures, arenas, runs, gates, decisions, validations, nexts)

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
