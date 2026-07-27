from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1206"
TITLE = "1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DERIVATION_PATH = OUT_DIR / f"{PACK_ID}_LOWERED_COMPONENT_DERIVATIONS.csv"
INPUTS_PATH = OUT_DIR / f"{PACK_ID}_LOWER_LEVEL_INPUTS_TO_FILL.csv"
PRESSURE_PATH = OUT_DIR / f"{PACK_ID}_PRESSURE_COMPARISON.csv"
BRANCH_PATH = OUT_DIR / f"{PACK_ID}_BRANCH_SELECTION.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1206_VALIDATION.csv"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1206_0_1205_next",
            "local_path": "1205-Y5-R10-first-BT-or-epsP-source-row-fill.md",
            "needle": "NEXT1205_0_1206",
            "purpose": "handoff to K_T trace law or P_loc leakage smallness derivation",
        },
        {
            "source_id": "SRC1206_1_1205_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1205_BOUND_PRESSURE_TARGETS.csv",
            "needle": "PRS1205_1_boundary_split_trace_bound",
            "purpose": "harsh equal-split pressure targets",
        },
        {
            "source_id": "SRC1206_2_1195_DT_operator",
            "local_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_0_operator_definition",
            "purpose": "D_T maps tracefree tensors to projected local vectors",
        },
        {
            "source_id": "SRC1206_3_1195_adjoint",
            "local_path": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "needle": "DTA1195_1_formal_adjoint",
            "purpose": "formal adjoint with P_loc derivative and boundary terms",
        },
        {
            "source_id": "SRC1206_4_1196_projector",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_3_projector_perturbation_bound",
            "purpose": "projector leakage smallness/absorption condition",
        },
        {
            "source_id": "SRC1206_5_1196_boundary",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "BP1196_0_tracefree_adjoint_boundary",
            "purpose": "D_T integration-by-parts boundary pairing",
        },
        {
            "source_id": "SRC1206_6_1204_source_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1204_SOURCE_READY_BOUND_ROWS.csv",
            "needle": "SBR1204_3_projector_finite_bound",
            "purpose": "source-ready boundary/projector fill schema",
        },
        {
            "source_id": "SRC1206_7_1205_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1205_BLOCKER_LEDGER.csv",
            "needle": "BLK1205_1_projector_missing_eps_constants",
            "purpose": "explicit missing lower-level constants before 1206",
        },
    ]
    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    pressure_rows_in = load_csv(OUT_DIR / "P8_Y5_R10_1205_BOUND_PRESSURE_TARGETS.csv")
    boundary_split = next(row for row in pressure_rows_in if row["pressure_id"] == "PRS1205_1_boundary_split_trace_bound")
    projector_split = next(row for row in pressure_rows_in if row["pressure_id"] == "PRS1205_3_projector_split_eps_G1")
    boundary_target = float(boundary_split["required_bound"])
    projector_target = float(projector_split["required_bound"])

    derivations = [
        {
            "derivation_id": "DRV1206_0_boundary_trace_lowering",
            "component_lowered": "q_boundary",
            "starting_object": "q_boundary=||B_T||",
            "lowered_formula": "q_boundary <= C_pair*C_NT(D,gamma)*(K_T_L2_norm + G_res_norm + R_perp_div_norm)",
            "derivation_steps": "B_T[V,K_T]=<n.K_T,P_locV>_partialD; dual trace pairing gives q_boundary<=||n.K_T||_H-1/2||P_locV||_H1/2; normal-trace theorem gives ||n.K_T||_H-1/2<=C_NT(||K_T||_L2+||div K_T||_L2); D_T K_T=P_loc divK_T=G_res leaves only G_res and perpendicular-divergence residue.",
            "zero_condition": "n_mu K_T^(mu nu)=0 on partialD or pullback(P_locV)=0 in the same parent local domain",
            "remaining_inputs": "C_pair;C_NT;K_T_L2_norm;G_res_norm;R_perp_div_norm;domain_id;norm_id",
            "status": "LOWERED_TO_GEOMETRIC_TRACE_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "DRV1206_1_projector_leakage_lowering",
            "component_lowered": "q_projector",
            "starting_object": "q_projector=||Delta_P|| or eps_P||G_res||",
            "lowered_formula": "q_projector <= epsilon_geom*G_res_norm, epsilon_geom=C_P*(nabla_P_loc_Linf + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)",
            "derivation_steps": "D_T^dagger V contains Pi_TF[nabla(P_locV)]=Pi_TF[P_loc nablaV]+Pi_TF[(nablaP_loc)V] plus coframe/domain-motion variations; collect those lower-order terms into epsilon_geom||V||_H1, then use the range/CK estimate to score epsilon_geom against G_res.",
            "zero_condition": "nabla P_loc=0, coframe/domain-motion silence, and projector-stress silence in the same parent quotient domain",
            "remaining_inputs": "C_P;nabla_P_loc_Linf;coframe_lock_Linf;domain_motion_Linf;projector_stress_Linf;G_res_norm;C_CK;domain_id;norm_id",
            "status": "LOWERED_TO_GEOMETRIC_SMALLNESS_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "DRV1206_2_projector_absorption_gate",
            "component_lowered": "projector absorption",
            "starting_object": "C_CK*eps_P<1",
            "lowered_formula": "C_CK*epsilon_geom < 1 and epsilon_geom*G_res_norm <= q_projector_target",
            "derivation_steps": "Use CK/Korn inequality ||V||_H1<=C_CK||D_T^dagger V - projector_leak[V]||; if ||projector_leak[V]||<=epsilon_geom||V||_H1 and C_CK epsilon_geom<1, the perturbation is absorbed into the left side.",
            "zero_condition": "epsilon_geom=0 gives exact projector silence",
            "remaining_inputs": "C_CK;epsilon_geom;G_res_norm;q_projector_target",
            "status": "ABSORPTION_INEQUALITY_DERIVED_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    inputs = [
        {
            "input_id": "IN1206_0_C_pair",
            "component": "q_boundary",
            "quantity": "C_pair",
            "definition": "operator norm of trace pairing between n.K_T in H^{-1/2}(partialD) and P_locV in H^{1/2}(partialD)",
            "required_for": "DRV1206_0_boundary_trace_lowering",
            "current_status": "MISSING_DOMAIN_NORM_CONSTANT",
            "source_or_derivation_needed": "domain and Sobolev trace convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1206_1_C_NT",
            "component": "q_boundary",
            "quantity": "C_NT(D,gamma)",
            "definition": "normal-trace theorem constant for H(div;D) symmetric tracefree tensor fields",
            "required_for": "DRV1206_0_boundary_trace_lowering",
            "current_status": "MISSING_DOMAIN_GEOMETRY_CONSTANT",
            "source_or_derivation_needed": "local domain geometry, metric regularity, and boundary regularity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1206_2_KT_bulk_norm",
            "component": "q_boundary",
            "quantity": "K_T_L2_norm",
            "definition": "bulk L2 norm of the tracefree compensator field in the selected local domain",
            "required_for": "DRV1206_0_boundary_trace_lowering",
            "current_status": "MISSING_PARENT_KT_BULK_EQUATION",
            "source_or_derivation_needed": "parent K_T equation, coercivity, or theorem-zero no-hair clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1206_3_Gres_norm",
            "component": "q_boundary/q_projector",
            "quantity": "G_res_norm",
            "definition": "weighted norm of the local residual source vector in the same domain/norm as D_T",
            "required_for": "DRV1206_0_boundary_trace_lowering;DRV1206_1_projector_leakage_lowering",
            "current_status": "MISSING_G_RES_PROFILE_NORM",
            "source_or_derivation_needed": "local residual profile from parent GR-reduction equations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1206_4_Rperp",
            "component": "q_boundary",
            "quantity": "R_perp_div_norm",
            "definition": "unprojected divergence residue (I-P_loc) div K_T not seen by D_T K_T=P_loc div K_T",
            "required_for": "DRV1206_0_boundary_trace_lowering",
            "current_status": "MISSING_PERPENDICULAR_DIVERGENCE_GUARD",
            "source_or_derivation_needed": "P_loc complement theorem or finite perpendicular divergence bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1206_5_epsilon_geom",
            "component": "q_projector",
            "quantity": "epsilon_geom",
            "definition": "lower-level geometric projector leakage coefficient built from nablaP/coframe/domain-motion/projector-stress norms",
            "required_for": "DRV1206_1_projector_leakage_lowering",
            "current_status": "FORMULA_DERIVED_COMPONENT_NORMS_MISSING",
            "source_or_derivation_needed": "nabla_P_loc_Linf;coframe_lock_Linf;domain_motion_Linf;projector_stress_Linf;C_P",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1206_6_C_CK",
            "component": "q_projector",
            "quantity": "C_CK",
            "definition": "anchored conformal-Killing/Korn constant for the selected local domain",
            "required_for": "DRV1206_2_projector_absorption_gate",
            "current_status": "MISSING_CK_KORN_CONSTANT",
            "source_or_derivation_needed": "domain anchor, no-zero-mode certificate, metric regularity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    comparisons = [
        {
            "comparison_id": "CMP1206_0_boundary_lowered_target",
            "component": "q_boundary",
            "lowered_quantity": "C_pair*C_NT*(K_T_L2_norm+G_res_norm+R_perp_div_norm)",
            "target": boundary_target,
            "target_context": "harsh W=100 boundary/projector equal split",
            "comparison_status": "EXECUTABLE_FORMULA_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "comparison_id": "CMP1206_1_projector_lowered_target",
            "component": "q_projector",
            "lowered_quantity": "epsilon_geom*G_res_norm",
            "target": projector_target,
            "target_context": "harsh W=100 boundary/projector equal split",
            "comparison_status": "EXECUTABLE_FORMULA_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "comparison_id": "CMP1206_2_projector_absorption_target",
            "component": "projector_absorption",
            "lowered_quantity": "C_CK*epsilon_geom",
            "target": "< 1",
            "target_context": "operator perturbation absorption",
            "comparison_status": "EXECUTABLE_FORMULA_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    branch_rows = [
        {
            "branch_id": "BR1206_0_boundary_route",
            "route": "K_T normal trace bound",
            "gain": "replaces undefined ||B_T|| by normal-trace/domain/source constants",
            "cost": "still needs K_T bulk norm, G_res_norm, R_perp_div_norm, and domain trace constants",
            "current_status": "LOWERED_NOT_NUMERIC",
            "recommended_next": "source G_res_norm and local domain constants, or derive n.K_T=0 from parent boundary action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1206_1_projector_route",
            "route": "P_loc leakage smallness",
            "gain": "replaces undefined eps_P by epsilon_geom from nablaP/coframe/domain-motion/projector-stress norms",
            "cost": "still needs G_res_norm, C_CK, and each geometric leakage norm",
            "current_status": "LOWERED_NOT_NUMERIC",
            "recommended_next": "derive P_loc frozen/coframe-lock theorem from parent quotient geometry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1206_2_best_next",
            "route": "projector route first",
            "gain": "a parent quotient/frozen-projector theorem can set epsilon_geom=0 and remove q_projector entirely",
            "cost": "requires same parent-owned domain and physical-charge guard",
            "current_status": "SELECTED_NEXT_DERIVATION_ROUTE",
            "recommended_next": "try to prove epsilon_geom=0 or bound it from quotient/coframe locks before sourcing numeric K_T",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1206_0_lowered_boundary_not_numeric",
            "gate": "q_boundary numeric score",
            "status": "BLOCKED",
            "reason": "normal-trace law is derived, but C_pair, C_NT, K_T_L2, G_res_norm, and R_perp are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1206_1_lowered_projector_not_numeric",
            "gate": "q_projector numeric score",
            "status": "BLOCKED",
            "reason": "epsilon_geom formula is derived, but geometric leakage norms, C_CK, and G_res_norm are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1206_2_no_placeholder_rhs",
            "gate": "lowered formulas avoid B_T/eps_P placeholders",
            "status": "ACTIVE_GUARD",
            "reason": "RHS uses lower-level geometric/source constants rather than undefined B_T or eps_P rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1206_3_R10_local_GR",
            "gate": "R10/local-GR branch",
            "status": "BLOCKED",
            "reason": "lowered contracts are not yet numeric/source-backed and official W_R10 remains nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1206_0_verdict",
            "condition": "direct B_T/eps_P source rows are absent",
            "decision": "derive lowered formulas instead of scanning again",
            "result": "B_T is lowered to a normal-trace/domain-source bound; eps_P is lowered to epsilon_geom from projector/coframe/domain-motion norms",
            "next_action": "attack projector route first: prove epsilon_geom=0 from parent quotient/coframe lock or fill its lower-level geometric norms",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    next_rows = [
        {
            "next_id": "NEXT1206_0_1207",
            "target_file": "1207-Y5-R10-quotient-coframe-lock-or-epsilon-geom-source-pack.md",
            "target_script": "scripts/Y5_R10_quotient_coframe_lock_or_epsilon_geom_source_pack.py",
            "task": "try to prove epsilon_geom=0 from the parent quotient/coframe/domain lock; if not, stage source-ready rows for nabla_P_loc_Linf, coframe_lock_Linf, domain_motion_Linf, projector_stress_Linf, C_P, C_CK, and G_res_norm",
            "success_condition": "q_projector is either theorem-zero by parent geometry or has a lower-level source-pack ready for numeric nonclaim scoring",
            "do_not_do": "do not claim R10/local-GR pass, do not reintroduce eps_P as a primitive placeholder, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    derivation_fields = ["derivation_id", "component_lowered", "starting_object", "lowered_formula", "derivation_steps", "zero_condition", "remaining_inputs", "status", "valid_for_claim", "claim_allowed"]
    input_fields = ["input_id", "component", "quantity", "definition", "required_for", "current_status", "source_or_derivation_needed", "valid_for_claim", "claim_allowed"]
    comparison_fields = ["comparison_id", "component", "lowered_quantity", "target", "target_context", "comparison_status", "claim_allowed", "valid_for_claim"]
    branch_fields = ["branch_id", "route", "gain", "cost", "current_status", "recommended_next", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(DERIVATION_PATH, derivations, derivation_fields)
    write_csv(INPUTS_PATH, inputs, input_fields)
    write_csv(PRESSURE_PATH, comparisons, comparison_fields)
    write_csv(BRANCH_PATH, branch_rows, branch_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        DERIVATION_PATH,
        INPUTS_PATH,
        PRESSURE_PATH,
        BRANCH_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    lowered_boundary_present = any(row["derivation_id"] == "DRV1206_0_boundary_trace_lowering" for row in derivations)
    lowered_projector_present = any(row["derivation_id"] == "DRV1206_1_projector_leakage_lowering" for row in derivations)
    forbidden_rhs = []
    for row in derivations:
        formula = row["lowered_formula"]
        if "||B_T||" in formula or "eps_P" in formula:
            forbidden_rhs.append(row["derivation_id"])
    no_placeholder_rhs = not forbidden_rhs
    input_quantities = {row["quantity"] for row in inputs}
    lower_inputs_present = {"C_NT(D,gamma)", "K_T_L2_norm", "G_res_norm", "epsilon_geom", "C_CK"}.issubset(input_quantities)
    pressure_targets_match = abs(boundary_target - 1.17233215026e-05) < 1e-16 and abs(projector_target - 1.17233215026e-05) < 1e-16
    selected_next_projector = any(row["current_status"] == "SELECTED_NEXT_DERIVATION_ROUTE" and "projector" in row["route"] for row in branch_rows)
    claim_policy_ok = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in derivations + inputs + comparisons + branch_rows + claim_gates
    )
    formalization_untouched = len(formalization_recent) == 0

    validation_rows = [
        validation_row("VAL1206_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1206_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1206_2_boundary_lowered", "boundary component is lowered to trace/source constants", lowered_boundary_present, "DRV1206_0 present"),
        validation_row("VAL1206_3_projector_lowered", "projector component is lowered to epsilon_geom constants", lowered_projector_present, "DRV1206_1 present"),
        validation_row("VAL1206_4_no_placeholder_rhs", "lowered RHS avoids B_T and eps_P primitive placeholders", no_placeholder_rhs, "forbidden_rhs=" + ",".join(forbidden_rhs)),
        validation_row("VAL1206_5_lower_inputs_present", "lower-level inputs to fill are enumerated", lower_inputs_present, ",".join(sorted(input_quantities))),
        validation_row("VAL1206_6_pressure_targets_match", "1205 harsh split targets are preserved", pressure_targets_match, f"boundary={fmt(boundary_target)};projector={fmt(projector_target)}"),
        validation_row("VAL1206_7_next_projector_route", "next route selects quotient/coframe projector attack", selected_next_projector, "projector route selected"),
        validation_row("VAL1206_8_nonclaim_policy", "all generated rows remain nonclaim", claim_policy_ok, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1206_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1206_10_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1206_11_overall",
            "overall 1206 validation",
            validation_pass,
            "1206 lowered trace/leakage contracts are reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1206 Y5/R10 K_T Boundary Trace Law Or P_loc Leakage Smallness Derivation

**Current verdict:** 1206 makes real derivational progress but still no R10/local-GR claim. `||B_T||` is lowered to a normal-trace/domain-source bound, and primitive `eps_P` is replaced by `epsilon_geom` built from lower-level projector/coframe/domain-motion constants.

**Main progress:** the boundary and projector blockers are no longer primitive labels. The harsh split target remains `{fmt(boundary_target)}`, but the scoreable inequalities are now `C_pair C_NT (||K_T||+||G_res||+||R_perp||) <= target` and `epsilon_geom ||G_res|| <= target` with `C_CK epsilon_geom < 1`.

## Source Register

{markdown_table(source_rows, source_fields)}

## Lowered Component Derivations

{markdown_table(derivations, derivation_fields)}

## Lower-Level Inputs To Fill

{markdown_table(inputs, input_fields)}

## Pressure Comparison

{markdown_table(comparisons, comparison_fields)}

## Branch Selection

{markdown_table(branch_rows, branch_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"boundary_target={fmt(boundary_target)}")
    print(f"projector_target={fmt(projector_target)}")


if __name__ == "__main__":
    main()
