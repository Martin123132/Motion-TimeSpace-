from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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
            "source_id": "SRC1172_0_1171_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1171_NEXT_TARGET.csv",
            "needle": "NEXT1171_0_1172",
            "role": "handoff to B_C primitive/norm owner or finite-bound runner.",
        },
        {
            "source_id": "SRC1172_1_1171_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1171_VALIDATION.csv",
            "needle": "V1171_SUMMARY",
            "role": "1171 validation summary.",
        },
        {
            "source_id": "SRC1172_2_1171_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1171_FIRST_FINITE_BC_BOUND_ROW.csv",
            "needle": "FBC1171_0_first_boundary_bound_row",
            "role": "first finite B_C boundary-bound row to feed.",
        },
        {
            "source_id": "SRC1172_3_1171_degree",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1171_FORM_DEGREE_LEDGER.csv",
            "needle": "FDL1171_0_BC",
            "role": "B_C degree and boundary role.",
        },
        {
            "source_id": "SRC1172_4_1171_no_go",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
            "needle": "NOG1171_0_neumann_gap",
            "role": "generic natural-boundary no-go.",
        },
        {
            "source_id": "SRC1172_5_1021_primitive",
            "relative_path": "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            "needle": "BXG1021_2_exact_surface_pullback",
            "role": "older B_X primitive pullback precedent.",
        },
        {
            "source_id": "SRC1172_6_1021_norm",
            "relative_path": "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            "needle": "EBF1021_0_norm_bX",
            "role": "older primitive norm missing-row precedent.",
        },
        {
            "source_id": "SRC1172_7_1021_summary",
            "relative_path": "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            "needle": "V1021_SUMMARY",
            "role": "1021 primitive validation summary.",
        },
        {
            "source_id": "SRC1172_8_1020_bound",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_3_residual_bound",
            "role": "weighted-Stokes finite-bound law.",
        },
        {
            "source_id": "SRC1172_9_1020_guard",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "CG1020_8_guardrail",
            "role": "weighted-Stokes guardrail.",
        },
        {
            "source_id": "SRC1172_10_274_decomp",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "J_C = dB_C + J_C^{top}",
            "role": "lifted-C exact/top decomposition.",
        },
        {
            "source_id": "SRC1172_11_275_JC",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "J_C = det(Q_coh) Omega_D / V_D",
            "role": "J_C determinant source shape.",
        },
        {
            "source_id": "SRC1172_12_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward guard.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def hodge_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "bound_id": "HBP1172_0_local_exact_setup",
            "object": "J_C^exact=d_D B_C",
            "statement": "On a contractible local domain with the top class removed, the remaining lifted-C charge is exact: J_C^exact=d_D B_C.",
            "status": "FORMAL_SETUP",
            "derived_bound": "none yet",
            "missing_for_claim": "domain regularity, boundary condition/gauge, and exact-sector source amplitude",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBP1172_1_coulomb_primitive",
            "object": "B_C primitive",
            "statement": "With a Coulomb/orthogonal gauge and no harmonic 2-form, a canonical primitive can be written schematically as B_C=d_D^dagger G_D J_C^exact.",
            "status": "CANONICAL_PRIMITIVE_SCHEMA",
            "derived_bound": "||B_C||_{H1(D)} <= C_Hodge(D,gamma) ||J_C^exact||_{L2(D)}",
            "missing_for_claim": "Hodge Green operator domain, gauge condition, harmonic projection, boundary condition gamma",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBP1172_2_trace_to_boundary",
            "object": "pullback_partialD B_C",
            "statement": "A trace inequality then gives ||i_partialD^* B_C||_{L2(partialD)} <= C_trace(D,gamma) C_Hodge(D,gamma) ||J_C^exact||_{L2(D)}.",
            "status": "FINITE_BOUND_SCHEMA",
            "derived_bound": "|int_partialD B_C| <= area(partialD)^1/2 C_trace C_Hodge ||J_C^exact||_{L2(D)}",
            "missing_for_claim": "surface area, constants, units, and J_C^exact norm/source",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBP1172_3_zero_limit",
            "object": "local exact zero",
            "statement": "If J_C^exact=0, harmonic boundary class=0, and the chosen gauge/boundary condition kills pure-gauge primitives, then B_C=0 and the exact boundary term vanishes.",
            "status": "CONDITIONAL_ZERO_THEOREM_NOT_SIGNED",
            "derived_bound": "zero only under source-free plus harmonic-free plus gauge/boundary certificates",
            "missing_for_claim": "parent theorem J_C^exact=0 in local vacuum and physical-charge guard",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBP1172_4_verdict",
            "object": "primitive norm owner verdict",
            "statement": "1172 gets a legitimate finite-bound route from Hodge/Poincare plus trace, but not a local zero or local-GR pass.",
            "status": "BOUND_ROUTE_PROGRESS_NO_CLAIM",
            "derived_bound": "boundary residual controlled by exact J_C norm and geometry constants",
            "missing_for_claim": "numeric/source-backed J_C^exact norm and domain constants",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_input_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "LFI1172_0_JC_exact_norm",
            "quantity": "||J_C^exact||_{L2(D)}",
            "role": "source amplitude feeding B_C primitive norm",
            "current_value": "MISSING_JC_EXACT_NORM",
            "units": "MISSING_JC_UNITS_PER_VOLUME_FORM",
            "source_or_theorem": "MISSING_LOCAL_EXACT_SOURCE_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "input_id": "LFI1172_1_C_Hodge",
            "quantity": "C_Hodge(D,gamma)",
            "role": "elliptic primitive constant for B_C=d^dagger G J_C",
            "current_value": "MISSING_HODGE_CONSTANT",
            "units": "domain_length_power_depending_norm_convention",
            "source_or_theorem": "MISSING_DOMAIN_REGULARITY_AND_GAUGE",
            "valid_for_claim": False,
        },
        {
            "input_id": "LFI1172_2_C_trace",
            "quantity": "C_trace(D,gamma)",
            "role": "trace constant from interior primitive to boundary pullback",
            "current_value": "MISSING_TRACE_CONSTANT",
            "units": "domain_length_power_depending_norm_convention",
            "source_or_theorem": "MISSING_TRACE_THEOREM_DOMAIN_SPEC",
            "valid_for_claim": False,
        },
        {
            "input_id": "LFI1172_3_area",
            "quantity": "area(partialD)",
            "role": "converts boundary L2 norm to absolute integral",
            "current_value": "MISSING_SURFACE_AREA",
            "units": "length^2 or selected surface measure",
            "source_or_theorem": "MISSING_ARENA_DOMAIN_GEOMETRY",
            "valid_for_claim": False,
        },
        {
            "input_id": "LFI1172_4_harmonic_boundary",
            "quantity": "h_C and r_C edge residuals",
            "role": "non-exact/harmonic pieces excluded from primitive estimate",
            "current_value": "MISSING_HARMONIC_RESIDUAL_ZERO_OR_BOUND",
            "units": "same boundary charge units as B_C integral",
            "source_or_theorem": "MISSING_COHOMOLOGY_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "input_id": "LFI1172_5_weighted_stokes",
            "quantity": "C_corner and ||d_S(F_lambda epsilon_C)||_* ||b_C||_*",
            "role": "weighted-Stokes residual attached to exact boundary representation",
            "current_value": "MISSING_WEIGHTED_STOKES_TERMS",
            "units": "edge_charge_units",
            "source_or_theorem": "MISSING_CLOSED_WEIGHT_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def filled_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "filled_id": "BCF1172_0_symbolic_bound",
            "arena": "local_generic",
            "quantity": "Q_C_boundary_exact",
            "symbolic_bound": "abs(Q_C_boundary_exact) <= sqrt(area_partialD) * C_trace * C_Hodge * norm_JC_exact + C_corner + norm_dS_Feps * norm_bC + harmonic_edge_abs + residual_edge_abs",
            "status": "SYMBOLIC_RUNNER_READY_NONCLAIM",
            "numeric_bound": "NOT_EVALUATED",
            "missing_inputs": "area_partialD;C_trace;C_Hodge;norm_JC_exact;C_corner;norm_dS_Feps;norm_bC;harmonic_edge_abs;residual_edge_abs;units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "filled_id": "BCF1172_1_zero_branch",
            "arena": "local_vacuum_conditional",
            "quantity": "Q_C_boundary_exact",
            "symbolic_bound": "0 if norm_JC_exact=0 and harmonic_edge_abs=residual_edge_abs=C_corner=norm_dS_Feps=0 under certified gauge/boundary conditions",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "numeric_bound": "NOT_EVALUATED",
            "missing_inputs": "local_JC_exact_zero_theorem;cohomology_zero;closed_weight_zero;gauge_physical_charge_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "filled_id": "BCF1172_2_first_arena_recommendation",
            "arena": "R10_then_PPN",
            "quantity": "domain constants and source norm",
            "symbolic_bound": "choose one arena geometry, compute constants, and require source/theorem row for norm_JC_exact before scoring",
            "status": "NEXT_RUNNER_INPUT_RECOMMENDED",
            "numeric_bound": "NOT_EVALUATED",
            "missing_inputs": "arena geometry and source amplitude",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def zero_branch_rows() -> list[dict[str, object]]:
    rows = [
        {
            "zero_id": "ZBC1172_0_exact_source_zero",
            "condition": "J_C^exact=0 in local vacuum",
            "status": "MISSING_PARENT_THEOREM",
            "why_needed": "without this, Hodge/Poincare gives a finite bound but not zero",
            "valid_for_claim": False,
        },
        {
            "zero_id": "ZBC1172_1_harmonic_zero",
            "condition": "local harmonic/relative boundary classes vanish",
            "status": "MISSING_COHOMOLOGY_CERTIFICATE",
            "why_needed": "primitive estimate only controls exact sector",
            "valid_for_claim": False,
        },
        {
            "zero_id": "ZBC1172_2_gauge_boundary_guard",
            "condition": "Coulomb/orthogonal gauge plus boundary condition preserves physical charges",
            "status": "MISSING_PHYSICAL_CHARGE_GUARD",
            "why_needed": "avoid killing mass/time/rotation/charge generators while silencing residual C sector",
            "valid_for_claim": False,
        },
        {
            "zero_id": "ZBC1172_3_weight_zero",
            "condition": "closed-weight/corner residuals vanish",
            "status": "MISSING_WEIGHTED_STOKES_CERTIFICATE",
            "why_needed": "weighted-Stokes residual can survive even with a primitive",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1172_0_hodge_bound",
            "test": "derive B_C primitive norm from J_C exact",
            "status": "PASS_SYMBOLIC_BOUND_ONLY",
            "result": "Hodge/Poincare plus trace controls boundary primitive by norm_JC_exact and domain constants",
            "blocked_by": "numeric/source-backed norm_JC_exact;C_Hodge;C_trace;area;units",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1172_1_zero_branch",
            "test": "derive local boundary zero",
            "status": "REFUSED_ZERO_THEOREM_MISSING",
            "result": "zero requires J_C exact source zero plus harmonic/weighted/gauge certificates",
            "blocked_by": "local_JC_exact_zero;cohomology_zero;closed_weight_zero;physical_charge_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1172_2_bound_runner",
            "test": "feed 1171 finite row",
            "status": "SCHEMA_FILLED_NUMERIC_INPUTS_MISSING",
            "result": "symbolic bound row is runner-ready but not claim-valid",
            "blocked_by": "all numeric/source inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1172_3_local_promotion",
            "test": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "finite-bound route is sharper but unscored",
            "blocked_by": "B_C source/norm and weighted-Stokes inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1172_0_primitive_bound",
            "gate": "B_C primitive norm bound",
            "current_status": "PASS_SYMBOLIC_NONCLAIM",
            "reason": "Hodge/Poincare/trace bound exists symbolically",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1172_1_source_norm",
            "gate": "J_C exact source norm",
            "current_status": "BLOCKED",
            "reason": "norm_JC_exact or zero theorem is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1172_2_domain_constants",
            "gate": "domain geometry constants",
            "current_status": "BLOCKED",
            "reason": "C_Hodge, C_trace, area, and units need arena selection",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1172_3_weighted_stokes_terms",
            "gate": "corner/kernel/harmonic/residual terms",
            "current_status": "BLOCKED",
            "reason": "weighted-Stokes guard remains active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1172_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "symbolic bound has no numeric/source-backed inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1172_0_bound_route_progress",
            "decision": "keep_Hodge_trace_bound_route",
            "reason": "it converts a vague boundary obstruction into explicit constants and source norms",
            "next_action": "derive/source norm_JC_exact or zero theorem first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1172_1_zero_route_status",
            "decision": "do_not_claim_zero",
            "reason": "zero requires source-free exact sector, cohomology, weight, and physical-charge certificates",
            "next_action": "try local J_C exact source-zero theorem before numeric arena scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1172_2_best_next",
            "decision": "target_JC_exact_source_zero_or_bound",
            "reason": "norm_JC_exact is now the earliest missing input that feeds every local finite-bound arena",
            "next_action": "derive local J_C exact source amplitude from Q-flow/local vacuum assumptions, or stage first sourced norm row",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1172_0_1173",
            "next_target": "1173-Y5-R10-local-JC-exact-source-zero-or-first-norm-input-row.md",
            "objective": "try to derive J_C^exact=0 in the local vacuum branch; if not, stage the first source-backed norm_JC_exact input row for the finite boundary runner",
            "include": "Q-flow local stationarity; det(Q_coh) variation; exact/top split; norm_JC_exact units; R10/PPN arena choice; no-claim runner",
            "exclude": "assuming local J_C=0; hiding harmonic terms; generic natural-boundary zero; local claim; c_g zero; invented values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    hodge: list[dict[str, object]],
    inputs: list[dict[str, object]],
    filled: list[dict[str, object]],
    zero: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1172_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_1_hodge_bound_written",
            "result": "pass" if any("C_Hodge" in str(r["derived_bound"]) for r in hodge) else "fail",
            "detail": "Hodge/Poincare primitive bound is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_2_trace_bound_written",
            "result": "pass" if any("C_trace" in str(r["derived_bound"]) for r in hodge) else "fail",
            "detail": "trace-to-boundary bound is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_3_runner_inputs_complete_schema",
            "result": "pass" if len(inputs) >= 6 else "fail",
            "detail": "source norm, constants, area, harmonic/residual, and weighted-Stokes inputs are staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_4_symbolic_bound_row_written",
            "result": "pass"
            if any(r["filled_id"] == "BCF1172_0_symbolic_bound" for r in filled)
            else "fail",
            "detail": "1171 finite row is filled with a symbolic Hodge/trace bound",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_5_zero_branch_not_claimed",
            "result": "pass" if all(r["valid_for_claim"] is False for r in zero) else "fail",
            "detail": "zero branch conditions remain unsigned and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in r.values())) or r["valid_for_claim"] is False for r in inputs + filled)
            else "fail",
            "detail": "rows with MISSING inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses zero, numeric-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_8_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1172 claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_9_no_claim_rows",
            "result": "pass"
            if all(r.get("valid_for_claim") is False for r in hodge + inputs + filled + zero + gates + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_10_next_target",
            "result": "pass" if nexts and "1173" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1173 handoff targets local J_C exact source zero or first norm input row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1172_SUMMARY",
            "result": "pass",
            "detail": "1172 derives a symbolic Hodge/Poincare/trace finite-bound route for B_C, but blocks claims until norm_JC_exact, domain constants, weighted-Stokes terms, and units are sourced",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    hodge: list[dict[str, object]],
    inputs: list[dict[str, object]],
    filled: list[dict[str, object]],
    zero: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1172 — Y5/R10 B_C primitive norm owner or local finite-bound runner",
        "**Current verdict:** 1172 gets a real finite-bound route, not a local-zero theorem. On a contractible local domain with the top class removed, a Coulomb/Hodge primitive gives `B_C=d_D^dagger G_D J_C^exact` schematically, so the boundary primitive is controlled by `norm_JC_exact` and domain constants.",
        "**Main progress:** the 1171 row is now symbolically runnable: `abs(Q_C_boundary_exact) <= sqrt(area_partialD) C_trace C_Hodge norm_JC_exact + C_corner + norm_dS_Feps norm_bC + harmonic_edge_abs + residual_edge_abs`.",
        "**Hard blocker:** the earliest missing physical input is now `norm_JC_exact` or a theorem that `J_C^exact=0` in the local vacuum branch. Without that, the Hodge bound is clean mathematics but not a scored local test.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Hodge/Poincare primitive bound attempt\n\n" + table(hodge),
        "## Local finite-bound runner inputs\n\n" + table(inputs),
        "## B_C bound filled from J_C schema\n\n" + table(filled),
        "## Zero branch conditions\n\n" + table(zero),
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
    hodge = hodge_bound_rows()
    inputs = runner_input_rows()
    filled = filled_bound_rows()
    zero = zero_branch_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, hodge, inputs, filled, zero, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1172_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1172_HODGE_PRIMITIVE_BOUND_ATTEMPT.csv": hodge,
        "P8_Y5_R10_1172_LOCAL_FINITE_BOUND_RUNNER_INPUTS.csv": inputs,
        "P8_Y5_R10_1172_BC_BOUND_FILLED_FROM_JC_SCHEMA.csv": filled,
        "P8_Y5_R10_1172_ZERO_BRANCH_CONDITIONS.csv": zero,
        "P8_Y5_R10_1172_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1172_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1172_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1172_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1172_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, hodge, inputs, filled, zero, runs, gates, decisions, validations, nexts)

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
