from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3359-Y5-R2FR-left-hand-EH-Newton-operator-recovery-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3359_0_3358_doc", ROOT / "3358-Y5-R2FR-surface-stress-owner-or-contact-multipole-bound-under-AX1090.md", "3358 source-side survivor and left-hand handoff"),
    ("LSRC3359_1_3358_next", OUT / "P8_Y5_R2FR_3358_NEXT_TARGET.csv", "3358 next target"),
    ("LSRC3359_2_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "source-side theorem scope"),
    ("LSRC3359_3_local_residual_template", OUT / "MTS_local_residual_predictions_TEMPLATE.csv", "R11 operator ledger and PPN residual row definitions"),
    ("LSRC3359_4_action_blocks", OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv", "minimum parent local GR action block inventory"),
    ("LSRC3359_5_R11_mapping", OUT / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv", "double-zero R11 operator mapping"),
    ("LSRC3359_6_R11_parent_clause", OUT / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv", "R11 parent clause candidate"),
    ("LSRC3359_7_R11_variation", OUT / "P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv", "double-zero variation proof"),
    ("LSRC3359_8_R11_gates", OUT / "P8_DOUBLE_ZERO_R11_GATES.csv", "R11 promotion gates"),
    ("LSRC3359_9_R11_executable", OUT / "R11_nonEH_operator_vector_executable.csv", "non-EH operator vector rows"),
    ("LSRC3359_10_source_stack", OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv", "Newton source normalization theorem stack"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3359_LOCAL_SOURCE_REGISTER.csv",
    "recovery_conditions": OUT / "P8_Y5_R2FR_3359_EH_NEWTON_RECOVERY_CONDITIONS.csv",
    "operator_matrix": OUT / "P8_Y5_R2FR_3359_NON_EH_OPERATOR_FAMILY_MATRIX.csv",
    "double_zero": OUT / "P8_Y5_R2FR_3359_DOUBLE_ZERO_SELECTOR_PACKET.csv",
    "newton_map": OUT / "P8_Y5_R2FR_3359_WEAK_FIELD_NEWTON_MAP.csv",
    "residual_bound": OUT / "P8_Y5_R2FR_3359_OPERATOR_RESIDUAL_BOUND_SCHEMA.csv",
    "gates": OUT / "P8_Y5_R2FR_3359_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3359_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3359_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3359_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def recovery_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "EHR3359_0_EH_core_present",
            "condition": "local observed metric has an EH core S_EH[g_obs;kappa0,Lambda0]",
            "mathematical_effect": "left-hand operator starts as G_mu_nu[g_obs] + Lambda0 g_mu_nu",
            "source_authority": "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS:A511_0_EH_core",
            "current_status": "CONDITIONAL_ANCHOR_PRESENT_NOT_TOTAL_PARENT",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "EHR3359_1_constant_kappa",
            "condition": "kappa0/G_eff is locally constant, universal, and not a fitted source-normalization patch",
            "mathematical_effect": "fixes Newton coupling in Poisson limit once source normalization is owned",
            "source_authority": "P8_SOURCE_NORMALIZATION_THEOREM_STACK:S1_constant_kappa",
            "current_status": "NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "EHR3359_2_non_EH_silence",
            "condition": "every non-EH operator family is absent, topological, or multiplied by a parent-owned double-zero selector",
            "mathematical_effect": "delta S_nonEH = 0 to first variation on the compact local branch",
            "source_authority": "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE:C2; P8_DOUBLE_ZERO_R11_VARIATION_PROOF:V2",
            "current_status": "THEOREM_TARGET_NOT_DERIVED_FOR_ACTUAL_R11_ROWS",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "EHR3359_3_Bianchi_stress_closure",
            "condition": "selector/projector/domain/boundary stress is zero, topological, ordinary-owned, or retained with a conserved residual",
            "mathematical_effect": "prevents non-EH stress from reappearing through Bianchi consistency",
            "source_authority": "P8_DOUBLE_ZERO_R11_VARIATION_PROOF:V4; P8_DOUBLE_ZERO_R11_GATES:G4",
            "current_status": "OPEN",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "EHR3359_4_source_side_AX1090_packet",
            "condition": "source side is the 3357 AX1090 Hilbert matter+EM packet plus the 3358 surface residual contract",
            "mathematical_effect": "right-hand source is clean enough to test the left-hand EH/Newton reduction",
            "source_authority": "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION; P8_Y5_R2FR_3358_EPSILON_SURFACE_SOURCE_UPDATE",
            "current_status": "CONDITIONAL_SOURCE_PACKET_READY",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "EHR3359_5_weak_field_Newton_map",
            "condition": "stationary weak-field slow-motion expansion of the EH equation maps to Poisson/Gauss with same-frame Hilbert source",
            "mathematical_effect": "nabla^2 Phi = 4 pi G_EH rho_H plus explicit residuals",
            "source_authority": "standard EH weak-field map used only after MTS EH reduction; P8_SOURCE_NORMALIZATION_THEOREM_STACK:S5",
            "current_status": "CONDITIONAL_REFERENCE_MAP_NOT_MTS_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def operator_family_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "OP3359_0_boundary_topological",
            "operator_family": "boundary/topological terms",
            "silence_route": "exact topological variation, scalar no-flux boundary, or double-zero boundary selector",
            "affected_rows": "R3;R4;R7;R8;R11",
            "current_status": "RETAINED_UNTIL_PARENT_TOPOLOGICAL_OR_SELECTOR_CERTIFICATE",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_1_R2_fR_scalar",
            "operator_family": "R^2 / f(R) scalar mode",
            "silence_route": "coefficient absent, scalar infinitely massive/decoupled, or c_R2(Sigma_loc)=O(Sigma_loc^2)",
            "affected_rows": "R3;R4;R10;R11",
            "current_status": "MISSING_COEFFICIENT_OR_DERIVED_ZERO",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_2_Ricci_Weyl_squared",
            "operator_family": "Ricci^2 / Weyl^2",
            "silence_route": "Gauss-Bonnet/topological combination or double-zero curvature-squared coefficient",
            "affected_rows": "R3;R8;R11",
            "current_status": "MISSING_COEFFICIENT_OR_TOPOLOGICAL_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_3_scalar_tensor",
            "operator_family": "scalar-tensor / class-metric coupling",
            "silence_route": "F_phi derivatives vanish locally or coupling is double-zero selected",
            "affected_rows": "R2;R3;R4;R9;R10;R11",
            "current_status": "MISSING_PARENT_LOCAL_SCALAR_SILENCE",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_4_vector_preferred_frame",
            "operator_family": "vector/preferred-frame selector",
            "silence_route": "no-vector theorem or double-zero vector coefficient",
            "affected_rows": "R5;R6;R7;R8;R11",
            "current_status": "RETAINED_UNFILLED",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_5_torsion_nonmetricity",
            "operator_family": "torsion/nonmetricity or independent connection",
            "silence_route": "Levi-Civita branch or double-zero torsion/nonmetricity coefficient",
            "affected_rows": "R0;R1;R2;R11",
            "current_status": "MISSING_CONNECTION_ZERO_OR_BOUND",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_6_bulk_X_force",
            "operator_family": "bulk X force law / finite-range field",
            "silence_route": "source charge zero plus double-zero coupling or executable finite-range bound",
            "affected_rows": "R1;R3;R4;R10;R11",
            "current_status": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_7_nonlocal_memory",
            "operator_family": "nonlocal/memory kernel",
            "silence_route": "compact-local kernel silence or double-zero kernel norm",
            "affected_rows": "R7;R9;R10;R11",
            "current_status": "MISSING_LOCALITY_KERNEL_BOUND_OR_ZERO",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_8_source_normalization",
            "operator_family": "source-normalization operator",
            "silence_route": "measured-GM theorem or double-zero source-normalization coefficient",
            "affected_rows": "R5;R6;R7;R8;R11",
            "current_status": "OPEN_HARD_ROW",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3359_9_projector_domain_stress",
            "operator_family": "projector/domain stress",
            "silence_route": "metric-independent topological projector or double-zero retained-stress coefficient",
            "affected_rows": "R5;R6;R7;R8;R11",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_OWNED",
            "valid_for_claim": "false",
        },
    ]


def double_zero_packet_rows() -> list[dict[str, Any]]:
    return [
        {
            "packet_id": "DZ3359_0_selector_definition",
            "statement": "Let Sigma_loc = G_AB Y_loc^A Y_loc^B with positive G_AB and parent-owned local-silence variables Y_loc^A.",
            "math_effect": "Sigma_loc = 0 and delta Sigma_loc = 0 when Y_loc^A = 0",
            "status": "SUFFICIENT_MECHANISM",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "DZ3359_1_double_zero_variation",
            "statement": "If S_nonEH contains F_A(Sigma_loc) O_A with F_A(0)=F_A'(0)=0, then delta(F_A O_A)=0 on the local branch.",
            "math_effect": "non-EH operator contributes no first variation to the left-hand local field equation",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "DZ3359_2_single_zero_rejected",
            "statement": "F_A(0)=0 alone is insufficient because F_A'(0) O_A delta Sigma can leak if the selector is not double-zero.",
            "math_effect": "blocks a fake closure route",
            "status": "GUARDRAIL",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "DZ3359_3_current_gap",
            "statement": "The corpus has the double-zero mechanism but not the parent Euler equations forcing every Y_loc^A=0 nor the actual factorization of every R11 row.",
            "math_effect": "R11 remains unpromoted",
            "status": "OPEN",
            "valid_for_claim": "false",
        },
    ]


def weak_field_newton_rows() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "WF3359_0_EH_to_Poisson",
            "step": "EH equation in stationary weak-field slow-motion limit",
            "formula": "G_00[g_obs] ~= 2 nabla^2 Phi / c^2; T_00 ~= rho_H c^2; nabla^2 Phi = 4 pi G_EH rho_H",
            "requires": "EH-only left-hand operator, constant kappa0, same-frame Hilbert source",
            "current_status": "CONDITIONAL_REFERENCE_MAP",
            "valid_for_claim": "false",
        },
        {
            "map_id": "WF3359_1_nonEH_residualized",
            "step": "include retained non-EH operator residues",
            "formula": "nabla^2 Phi = 4 pi G_EH rho_H + R_nonEH + R_surface + R_calibration",
            "requires": "absolute bounds or theorem-zero for R_nonEH, R_surface, and calibration residuals",
            "current_status": "RETAINED",
            "valid_for_claim": "false",
        },
        {
            "map_id": "WF3359_2_GR_PPN_warning",
            "step": "Poisson is not full local GR",
            "formula": "gamma-1, beta-1, alpha_i, xi, Gdot, and R10/R11 rows need same-frame weak-field expansion",
            "requires": "PPN coefficient calculation after EH/R11 and source normalization are closed",
            "current_status": "NOT_CLOSED",
            "valid_for_claim": "false",
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "ORB3359_0_operator_abs_envelope",
            "quantity": "epsilon_nonEH_operator_abs",
            "formula": "sum_A |c_A| * |W_A| over retained R11 operator families, no cancellations",
            "needed_inputs": "coefficient c_A, weak-field map W_A, units, cutoff/range, same-frame normalization, source path for each operator family",
            "current_numeric_value": "MISSING_R11_COEFFICIENT_VECTOR",
            "observable_links": "R3;R4;R5;R6;R7;R8;R9;R10;R11",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "ORB3359_1_double_zero_switch",
            "quantity": "epsilon_nonEH_operator_abs",
            "formula": "0 iff every retained non-EH term is absent, topological, or F_A(Sigma_loc)O_A with F_A(0)=F_A'(0)=0 and parent-owned Y_loc=0",
            "needed_inputs": "Y_loc Euler equations, Sigma_loc positivity, actual factorization for every R11 family, stress/Bianchi closure",
            "current_numeric_value": "MISSING_PARENT_YLOC_EULER_AND_R11_FACTORIZATION",
            "observable_links": "local_GR; Newton; PPN; R10; R11",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3359_0_EH_anchor_present",
            "claim": "an EH core exists as the left-hand reference anchor",
            "passed": "true",
            "reason": "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS includes A511_0_EH_core",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3359_1_double_zero_sufficiency",
            "claim": "double-zero selector mechanism is sufficient to silence factorized non-EH first variations",
            "passed": "true",
            "reason": "delta[Sigma_loc O_A]=0 when Sigma_loc=0 and delta Sigma_loc=0",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3359_2_actual_R11_factorization",
            "claim": "every actual R11 operator family is parent-factorized, absent, or topological",
            "passed": "false",
            "reason": "R11 operator rows still contain missing coefficients/selectors and factorization contracts are not derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3359_3_Yloc_Euler_zero",
            "claim": "parent Euler equations force every local-silence multiplet component Y_loc^A=0",
            "passed": "false",
            "reason": "Y_loc multiplet is written as a contract only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3359_4_Newton_operator_recovery",
            "claim": "left-hand operator reduces to EH/Newton with only scored residuals",
            "passed": "false",
            "reason": "actual R11 factorization, Y_loc Euler zero, source normalization, and surface residuals remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3359_5_local_GR_claim",
            "claim": "local GR/Newton branch is claim-ready",
            "passed": "false",
            "reason": "left-hand operator recovery and integrated source calibration are not promoted",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3359_0",
            "question": "Did 3359 derive local GR?",
            "answer": "no, but it identifies the exact left-hand theorem needed",
            "reason": "EH anchor plus double-zero selector is a real sufficiency route; actual R11 factorization and Y_loc Euler equations are missing",
            "next_action": "derive Y_loc Euler equations and actual R11 factorization, or fill operator coefficient bounds",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3359_1",
            "question": "Is the project closer?",
            "answer": "yes: source-side and left-hand blockers are now separated and machine-readable",
            "reason": "source side has AX1090 conditional packet; left-hand side has EH/R11 recovery packet and explicit R11 envelope",
            "next_action": "attack Y_loc parent Euler equations first; this is more valuable than numeric fitting",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3360-Y5-R2FR-Yloc-Euler-equations-or-R11-coefficient-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3360_Yloc_Euler_equations_or_R11_coefficient_bound.py",
            "objective": "derive parent Euler equations forcing Y_loc^A=0 and prove actual R11 factorization, or build the first source-backed absolute R11 coefficient bound row",
            "why_next": "3359 shows this is the central left-hand blocker to EH/Newton recovery",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3361-Y5-R2FR-contact-multipole-source-acquisition-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3361_contact_multipole_source_acquisition.py",
            "objective": "fallback source-side work: acquire concrete contact multipole bounds with source paths, units, and no-cancellation envelope",
            "why_next": "3358 leaves this as the source-side fallback if the surface owner theorem cannot be parent-signed",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    return "\n".join(
        [
            "# 3359 — Left-Hand EH/Newton Operator Recovery Under AX1090",
            "",
            f"Generated: `{RUN_UTC}`",
            "",
            "## Summary",
            "- This checkpoint attacks the left-hand geometric operator after the 3357/3358 source-side cleanup.",
            "- Real gain: it defines a precise sufficient route to EH/Newton recovery — EH core plus absent/topological/double-zero-selected non-EH operators.",
            "- The double-zero mechanism is mathematically useful: if `Sigma_loc=G_AB Y^A Y^B` and `Y=0`, then `Sigma_loc=0` and `delta Sigma_loc=0`, so factorized non-EH terms are silent to first variation.",
            "- Claim ceiling: the corpus has not derived the parent Euler equations forcing `Y_loc=0`, nor actual factorization for every R11 operator family.",
            "- So local GR is closer in structure, but not claim-ready.",
            "",
            "## Local Source Register",
            table(local_source_rows()),
            "## EH / Newton Recovery Conditions",
            table(recovery_condition_rows()),
            "## Non-EH Operator Family Matrix",
            table(operator_family_rows()),
            "## Double-Zero Selector Packet",
            table(double_zero_packet_rows()),
            "## Weak-Field Newton Map",
            table(weak_field_newton_rows()),
            "## Operator Residual Bound Schema",
            table(residual_bound_rows()),
            "## Promotion Gates",
            table(promotion_gate_rows()),
            "## Decision Ledger",
            table(decision_rows()),
            "## Next Target",
            table(next_target_rows()),
        ]
    )


def validate_outputs() -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    conditions = recovery_condition_rows()
    operators = operator_family_rows()
    double_zero = double_zero_packet_rows()
    bounds = residual_bound_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    write_targets_outside_fw = all(not path.resolve().is_relative_to(FW.resolve()) for path in output_paths + [DOC])
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3359_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3359_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3359_2_outputs_parse",
            "check": "all 3359 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3359_3_conditions_complete",
            "check": "EH/Newton recovery conditions include EH core, kappa, non-EH silence, Bianchi stress, source packet, and weak-field map",
            "passed": {row["condition_id"] for row in conditions}
            == {"EHR3359_0_EH_core_present", "EHR3359_1_constant_kappa", "EHR3359_2_non_EH_silence", "EHR3359_3_Bianchi_stress_closure", "EHR3359_4_source_side_AX1090_packet", "EHR3359_5_weak_field_Newton_map"},
            "detail": "",
        },
        {
            "check_id": "VAL3359_4_operator_family_coverage",
            "check": "operator matrix covers ten R11 families",
            "passed": len(operators) == 10 and all(row["valid_for_claim"] == "false" for row in operators),
            "detail": f"operator_rows={len(operators)}",
        },
        {
            "check_id": "VAL3359_5_double_zero_guard",
            "check": "double-zero packet includes sufficiency and single-zero rejection",
            "passed": any(row["packet_id"] == "DZ3359_1_double_zero_variation" for row in double_zero)
            and any(row["packet_id"] == "DZ3359_2_single_zero_rejected" for row in double_zero),
            "detail": "",
        },
        {
            "check_id": "VAL3359_6_bound_schema_nonclaim",
            "check": "operator residual bound schemas are nonclaim and explicitly missing parent/numeric inputs",
            "passed": all(row["valid_for_claim"] == "false" and "MISSING" in row["current_numeric_value"] for row in bounds),
            "detail": "",
        },
        {
            "check_id": "VAL3359_7_no_overclaim",
            "check": "actual R11, Yloc, Newton recovery, and local GR claims remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3359_2_actual_R11_factorization", "GATE3359_3_Yloc_Euler_zero", "GATE3359_4_Newton_operator_recovery", "GATE3359_5_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3359_8_next_target_Yloc",
            "check": "next target attacks Yloc Euler equations or R11 coefficient bound",
            "passed": any("Y_loc" in row["objective"] and "R11" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3359_9_write_scope_outside_formalization",
            "check": "all 3359 write targets are outside formalization-workbench",
            "passed": write_targets_outside_fw,
            "detail": f"write_targets={len(output_paths) + 1}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3359_10_overall",
            "check": "3359 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["recovery_conditions"], recovery_condition_rows())
    write_csv(OUTPUTS["operator_matrix"], operator_family_rows())
    write_csv(OUTPUTS["double_zero"], double_zero_packet_rows())
    write_csv(OUTPUTS["newton_map"], weak_field_newton_rows())
    write_csv(OUTPUTS["residual_bound"], residual_bound_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs())
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
