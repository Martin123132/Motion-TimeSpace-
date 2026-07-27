from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_EH_operator_selection_under_WEP_closure_or_retained_R11_vector.py"
DOC_PATH = ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md"

STATUS = "Y5_R10_EH_operator_selection_under_WEP_closure_fails_R11_vector_retained_template_only_nonclaim"
CLAIM_CEILING = "EH_operator_selection_or_R11_vector_gate_only_no_EH_Newton_PPN_R10_R11_or_local_GR_claim"
NEXT_TARGET = "656-Y5-R10-R11-executable-vector-minimum-skeleton-under-WEP-closure.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S655_0", "checkpoint_654_doc", ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md", "immediate local-GR spine"),
        ("S655_1", "validation_654", OUT / "P8_Y5_BRR545_654_VALIDATION.csv", "prior validation"),
        ("S655_2", "local_GR_spine_654", OUT / "P8_Y5_R10_654_LOCAL_GR_SPINE.csv", "current local-GR spine rungs"),
        ("S655_3", "promotion_gates_654", OUT / "P8_Y5_R10_654_PROMOTION_GATES.csv", "EH gate blocked in 654"),
        ("S655_4", "WEP_closure_import_654", OUT / "P8_Y5_R10_654_WEP_CLOSURE_IMPORT.csv", "closure labels that must not become EH proof"),
        ("S655_5", "EH_retained_ledger_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "canonical EH retained operator ledger"),
        ("S655_6", "R11_contract_438", ROOT / "438-R11-nonEH-coefficient-vector-contract.md", "R11 coefficient-vector contract"),
        ("S655_7", "EH_premise_ladder_439", ROOT / "439-EH-only-exterior-parent-premise-ladder.md", "EH-only parent premise ladder"),
        ("S655_8", "sector_reduction_440", ROOT / "440-metric-only-second-order-sector-reduction-attempt.md", "metric-only/second-order reduction attempt"),
        ("S655_9", "connection_P4_443", ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md", "Levi-Civita compatibility or R11 connection demotion"),
        ("S655_10", "EH_or_R11_gate_463", ROOT / "463-EH-only-or-R11-executable-vector-gate.md", "prior EH-only or R11 executable-vector gate"),
        ("S655_11", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "observable rows affected by EH/R11"),
        ("S655_12", "R11_template", OUT / "R11_nonEH_operator_vector_TEMPLATE.csv", "canonical R11 vector template"),
        ("S655_13", "R11_P4_connection_template", OUT / "R11_P4_connection_rows_TEMPLATE.csv", "connection-specific R11 template"),
        ("S655_14", "generator_script_655", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def WEP_closure_guard_rows() -> list[dict[str, object]]:
    return [
        {
            "guard_id": "WCG655_0_same_frame_not_EH",
            "imported_closure": "one observed geometry / species-blind matter frame",
            "allowed_use": "sets the private matter/source frame inside the branch",
            "forbidden_use": "cannot imply EH equations, metric-only dynamics, second-order field equations, source normalization, or PPN pass",
            "status": "guard_active",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "WCG655_1_no_chi_constants_not_EH",
            "imported_closure": "no local chi_X-dependent constants",
            "allowed_use": "removes direct alpha/mass WEP source only by closure",
            "forbidden_use": "cannot remove scalar/class metric, higher-curvature, boundary, memory, connection, or source-normalization operators",
            "status": "guard_active",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "WCG655_2_selector_stress_not_silent",
            "imported_closure": "selector stress accounting required",
            "allowed_use": "requires any selector enforcing observed geometry to enter Ward/Bianchi ledger",
            "forbidden_use": "cannot declare selector/domain/projector operator harmless without proof or R11 residual row",
            "status": "guard_active",
            "valid_for_claim": "false",
        },
    ]


def EH_only_premise_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "premise_id": "EHP655_P1_observed_frame",
            "premise": "one observed matter/coframe/source frame",
            "required_for_EH": "local observables must be compared in one frame before EH/PPN are meaningful",
            "current_status": "explicit_closure_from_653",
            "result_for_EH": "not_enough",
            "residual_if_failed": "WEP/source-frame closure label remains visible",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P2_Ward_Euler_ownership",
            "premise": "all hidden/projector/domain/boundary/source variables are varied and on shell, harmless, or retained",
            "required_for_EH": "unowned hidden Euler terms cannot source q_loc, flux, preferred-frame, or source-normalization residuals",
            "current_status": "open",
            "result_for_EH": "fail_for_claim",
            "residual_if_failed": "q_loc/source/flux/domain residuals remain active",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P3_no_extra_fields",
            "premise": "scalar, vector, bulk-X, projector/domain, torsion, nonmetricity, and memory sectors are absent/gauge/topological/no-haired",
            "required_for_EH": "extra propagating fields are non-EH operator families unless killed",
            "current_status": "not_derived",
            "result_for_EH": "fail_for_claim",
            "residual_if_failed": "R11 operator vector required",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P4_Levi_Civita",
            "premise": "observed connection is Levi-Civita and universally used",
            "required_for_EH": "torsion/nonmetricity can alter WEP, clocks, light, spin, source, and operator rows",
            "current_status": "not_parent_derived",
            "result_for_EH": "fail_for_claim",
            "residual_if_failed": "P4 R11 connection rows required",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P5_local_4D_metric_action",
            "premise": "surviving exterior action is local, 4D, diffeo-invariant, and metric-only",
            "required_for_EH": "Lovelock-style selection cannot apply to nonlocal, extra-dimensional, fixed-background, or extra-field actions",
            "current_status": "structural_target_not_parent_derived",
            "result_for_EH": "fail_for_claim",
            "residual_if_failed": "nonlocal/memory/domain/R11 rows remain",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P6_second_order",
            "premise": "local metric equations are second order through tested scales",
            "required_for_EH": "higher-curvature/nonlocal operators are legal conserved tensors unless forbidden",
            "current_status": "central_blocker_not_derived",
            "result_for_EH": "fail_for_claim",
            "residual_if_failed": "R2/fR, Ricci/Weyl, nonlocal R11 rows required",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P7_boundary_harmless",
            "premise": "boundary/topological terms have no local stress, flux, radial, shear, or preferred-location hair",
            "required_for_EH": "boundary terms can contaminate gamma, beta, alpha3, xi, Gdot, and source mass",
            "current_status": "conditional_not_derived",
            "result_for_EH": "fail_for_claim",
            "residual_if_failed": "boundary R11/source residual rows required",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P8_source_normalization",
            "premise": "kappa, G_eff, M_eff, and measured GM are constant, conserved, universal, and range independent",
            "required_for_EH": "EH equations alone are not measured Newtonian gravity without source normalization",
            "current_status": "conditional_open",
            "result_for_EH": "fail_for_Newton_PPN",
            "residual_if_failed": "R1/R4/R9/R10/R11 source-normalization rows required",
            "valid_for_claim": "false",
        },
        {
            "premise_id": "EHP655_P9_PPN_completion",
            "premise": "weak-field solution reaches GR PPN values in observed frame",
            "required_for_EH": "Poisson-looking leading order is not full local GR",
            "current_status": "not_reached",
            "result_for_EH": "fail_for_local_GR",
            "residual_if_failed": "R3-R9 PPN/Gdot residuals remain unpromoted",
            "valid_for_claim": "false",
        },
    ]


def R11_operator_vector_status_rows() -> list[dict[str, object]]:
    return [
        {
            "operator_family": "boundary_topological_terms",
            "affected_rows": "R3;R4;R7;R8;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "boundary/topological no-hair theorem or coefficient with gamma/beta/alpha3/xi map",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "R2_fR_scalar_mode",
            "affected_rows": "R3;R4;R10;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "c_R2/c_fR zero theorem, infinite scalar mass/no coupling, or gamma/beta/R10 map",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "Ricci_Weyl_squared",
            "affected_rows": "R3;R8;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "topological combination/zero coefficient theorem or weak-field slip/location map",
            "priority": "medium",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "scalar_tensor_class_metric",
            "affected_rows": "R2;R3;R4;R9;R10;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "scalar/class local silence theorem or clock/PPN/Gdot/R10 map",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "vector_preferred_frame",
            "affected_rows": "R5;R6;R7;R8;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "absent/gauge/aligned vector theorem or alpha1/alpha2/alpha3/xi map",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "torsion_nonmetricity",
            "affected_rows": "R0;R1;R2;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv;R11_P4_connection_rows_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "Levi-Civita parent theorem or torsion/nonmetricity coefficient maps",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "bulk_X_force_law",
            "affected_rows": "R1;R3;R4;R10;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "positive source-free no-hair or alpha_X(lambda_X)/PPN/source map",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "nonlocal_memory_kernel",
            "affected_rows": "R7;R9;R10;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "compact-local kernel silence or alpha3/Gdot/R10 map",
            "priority": "medium",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "source_normalization_operator",
            "affected_rows": "R1;R4;R9;R10;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only_retained_core_blocker",
            "minimum_to_clear": "constant measured-GM theorem or mu_extra/Gdot/range/source residual maps",
            "priority": "highest",
            "valid_for_claim": "false",
        },
        {
            "operator_family": "projector_domain_stress",
            "affected_rows": "R5;R6;R7;R8;R11",
            "current_artifact": "R11_nonEH_operator_vector_TEMPLATE.csv",
            "current_status": "template_only",
            "minimum_to_clear": "topological/metric-independent projector theorem or preferred-frame/location stress map",
            "priority": "high",
            "valid_for_claim": "false",
        },
    ]


def EH_or_R11_decision_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "EHG655_0_WEP_closure_guard",
            "branch": "both",
            "required_evidence": "WEP/common matter frame closure is visible and not counted as EH proof",
            "current_evidence": "653/654 closure import",
            "decision": "pass_guard",
            "claim_credit": "none",
            "next_action": "continue",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_1_EH_only_ladder_closed",
            "branch": "EH_only",
            "required_evidence": "P1-P9 parent-derived, especially P3/P4/P6/P8 and PPN completion",
            "current_evidence": "439/440/443/654 report closure, open, and retained rungs",
            "decision": "fail",
            "claim_credit": "none",
            "next_action": "do_not_claim_EH_only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_2_metric_only_second_order",
            "branch": "EH_only",
            "required_evidence": "all extra sectors eliminated and second-order metric operator derived",
            "current_evidence": "440 reports scalar/vector/bulk/boundary/connection/higher-curvature/nonlocal/source sectors retained",
            "decision": "fail",
            "claim_credit": "none",
            "next_action": "retain_R11_families",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_3_connection_compatibility",
            "branch": "EH_only",
            "required_evidence": "Levi-Civita connection parent-derived or no independent connection in parent branch",
            "current_evidence": "443 reports P4 not parent-derived and P4 template only",
            "decision": "fail",
            "claim_credit": "none",
            "next_action": "retain_P4_connection_rows",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_4_R11_template_present",
            "branch": "R11_vector",
            "required_evidence": "canonical R11 vector schema exists",
            "current_evidence": "R11_nonEH_operator_vector_TEMPLATE.csv exists",
            "decision": "pass_scaffold",
            "claim_credit": "none",
            "next_action": "build branch-specific skeleton",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_5_R11_actual_vector_supplied",
            "branch": "R11_vector",
            "required_evidence": "real coefficients/units/operator forms/weak-field maps/source paths and no placeholders",
            "current_evidence": "template-only rows; valid_for_claim=false",
            "decision": "fail",
            "claim_credit": "none",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_6_observable_score_ready",
            "branch": "both",
            "required_evidence": "R3-R11 predictions numeric or theorem-zero with source paths",
            "current_evidence": "639 and 654 rollup keep prediction_numeric_ready=false",
            "decision": "fail",
            "claim_credit": "none",
            "next_action": "no PPN/local-bound score",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "EHG655_7_local_GR_claim",
            "branch": "both",
            "required_evidence": "EH/R11 gate, source-normalization, extra-sector silence, and PPN vector all pass",
            "current_evidence": "none pass",
            "decision": "fail_policy",
            "claim_credit": "none",
            "next_action": "continue private derivation",
            "valid_for_claim": "false",
        },
    ]


def observable_impact_rows() -> list[dict[str, object]]:
    matrix = read_csv(OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv")
    rows: list[dict[str, object]] = []
    for row in matrix:
        row_id = row["row_id"]
        if row_id in {"R3_gamma", "R4_beta", "R5_alpha1", "R6_alpha2", "R7_alpha3", "R8_xi", "R11_EH_operator_ledger"}:
            operator_dependency = "EH_operator_or_R11_vector"
        elif row_id in {"R9_Gdot", "R10_fifth_force"}:
            operator_dependency = "EH_operator_plus_source_or_extra_sector_R11_vector"
        elif row_id in {"R0_identity_coframe_direct", "R1_WEP_source_charge", "R2_clock_redshift"}:
            operator_dependency = "WEP_closure_guard_plus_connection_or_source_rows"
        else:
            operator_dependency = "local_bound_matrix_dependency"
        rows.append(
            {
                "impact_id": f"OEI655_{len(rows):02d}",
                "row_id": row_id,
                "observable": row["observable"],
                "bound_value": row["bound_value"],
                "operator_dependency": operator_dependency,
                "current_prediction_status": "symbolic_or_closure_only",
                "score_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def next_action_queue_rows() -> list[dict[str, object]]:
    return [
        {
            "queue_id": "NAQ655_0",
            "priority": 1,
            "target": NEXT_TARGET,
            "work_item": "Create a branch-specific R11 executable-vector skeleton under WEP closure.",
            "acceptance_condition": "every retained family has a row with coefficient symbol, units, normalization, operator form, weak-field map placeholder status, and source path status",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "NAQ655_1",
            "priority": 2,
            "target": "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
            "work_item": "Fill or demote the source-normalization operator first.",
            "acceptance_condition": "mu_extra/Gdot/range/source rows are either theorem-zero or real residual inputs",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "NAQ655_2",
            "priority": 3,
            "target": "658-Y5-R10-P6-P4-theorem-zero-retry-or-connection-vector-fill.md",
            "work_item": "Retry P6/P4 theorem-zero or fill connection/higher-curvature vector rows.",
            "acceptance_condition": "P6/P4 are parent-signed or their retained rows are executable",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "WEP_closure_used_as_EH_proof": "false",
            "EH_only_parent_theorem": "false",
            "R11_template_present": "true",
            "R11_executable_vector_supplied": "false",
            "operator_family_rows": len(R11_operator_vector_status_rows()),
            "observable_score_ready": "false",
            "local_GR_claim": "false",
            "hardest_next_blocker": "real R11 executable vector skeleton/fill or EH-only theorem-zero",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    WEP_rows: list[dict[str, object]],
    premise_rows: list[dict[str, object]],
    R11_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    impact_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V655_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_654_VALIDATION.csv")
    checks.append(("V655_1_prior_654_validation_clean", all(row.get("result") == "pass" for row in prior), "654 validation remains clean"))
    checks.append(("V655_2_WEP_guard_blocks_EH_shortcut", all(row["status"] == "guard_active" for row in WEP_rows), "WEP closure guard rows are active"))
    checks.append(("V655_3_EH_ladder_not_derived", any(row["result_for_EH"] in {"fail_for_claim", "fail_for_Newton_PPN", "fail_for_local_GR"} for row in premise_rows), "EH-only premise ladder remains unclosed"))
    checks.append(("V655_4_R11_family_vector_complete_scaffold", len(R11_rows) >= 10 and all(row["valid_for_claim"] == "false" for row in R11_rows), "R11 retained family scaffold covers at least ten families"))
    checks.append(("V655_5_R11_template_only", all("template_only" in row["current_status"] for row in R11_rows), "R11 rows are template-only and nonclaim"))
    checks.append(("V655_6_EH_only_gate_fails", any(row["gate_id"] == "EHG655_1_EH_only_ladder_closed" and row["decision"] == "fail" for row in gate_rows), "EH-only gate fails"))
    checks.append(("V655_7_actual_R11_vector_fails", any(row["gate_id"] == "EHG655_5_R11_actual_vector_supplied" and row["decision"] == "fail" for row in gate_rows), "actual R11 vector is not supplied"))
    checks.append(("V655_8_local_GR_claim_blocked", any(row["gate_id"] == "EHG655_7_local_GR_claim" and row["decision"] == "fail_policy" for row in gate_rows), "local-GR claim is blocked"))
    matrix = read_csv(OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv")
    checks.append(("V655_9_observable_impact_covers_639", len(impact_rows) == len(matrix) and len(impact_rows) >= 12, "observable impact rows cover 639 matrix"))
    checks.append(("V655_10_no_observable_scores", all(row["score_allowed"] == "false" for row in impact_rows), "no observable row is scoreable"))
    checks.append(("V655_11_next_target_656_R11", queue_rows[0]["target"] == NEXT_TARGET and "R11-executable-vector" in NEXT_TARGET, "next target is R11 executable-vector skeleton"))
    checks.append(("V655_12_summary_blocks_claim", summary[0]["EH_only_parent_theorem"] == "false" and summary[0]["R11_executable_vector_supplied"] == "false" and summary[0]["local_GR_claim"] == "false", "summary blocks EH/R11/local-GR claim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V655_13_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    WEP_rows: list[dict[str, object]],
    premise_rows: list[dict[str, object]],
    R11_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    impact_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 655 Y5/R10 EH Operator Selection Under WEP Closure or Retained R11 Vector",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- WEP closure gives one private matter frame, but it does not select the Einstein-Hilbert operator.",
        "- The EH-only theorem route remains unsigned: extra sectors, Levi-Civita compatibility, second-order metric restriction, boundary harmlessness, source normalization, and PPN completion remain open.",
        "- The fallback R11 route exists only as a template/scaffold; no real executable non-EH coefficient vector is supplied yet.",
        "- Therefore no EH, R11, Newton, PPN, or local-GR claim is allowed.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## WEP Closure Guard",
        "",
        markdown_table(WEP_rows, ["guard_id", "imported_closure", "allowed_use", "forbidden_use", "status"]),
        "",
        "## EH-Only Premise Audit",
        "",
        markdown_table(premise_rows, ["premise_id", "premise", "current_status", "result_for_EH", "residual_if_failed"]),
        "",
        "## R11 Retained Operator Vector Status",
        "",
        markdown_table(R11_rows, ["operator_family", "affected_rows", "current_artifact", "current_status", "minimum_to_clear", "priority"]),
        "",
        "## EH-or-R11 Decision Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "branch", "required_evidence", "decision", "claim_credit", "next_action"]),
        "",
        "## Observable Impact Map",
        "",
        markdown_table(impact_rows, ["impact_id", "row_id", "observable", "bound_value", "operator_dependency", "current_prediction_status", "score_allowed"]),
        "",
        "## Next Action Queue",
        "",
        markdown_table(queue_rows, ["queue_id", "priority", "target", "work_item", "acceptance_condition"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is the clean fork: either earn EH-only from the parent action, or make the retained modified-gravity branch executable.",
        "- Since EH-only is not currently signed and R11 is template-only, the next useful work is not more prose; it is a branch-specific R11 vector skeleton.",
        "- That skeleton still will not be a claim, but it will stop `non-EH operator ledger` being a fog bank.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "WEP_closure_used_as_EH_proof", "EH_only_parent_theorem", "R11_template_present", "R11_executable_vector_supplied", "operator_family_rows", "observable_score_ready", "local_GR_claim", "hardest_next_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    WEP_rows = WEP_closure_guard_rows()
    premise_rows = EH_only_premise_audit_rows()
    R11_rows = R11_operator_vector_status_rows()
    gate_rows = EH_or_R11_decision_gate_rows()
    impact_rows = observable_impact_rows()
    queue_rows = next_action_queue_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, WEP_rows, premise_rows, R11_rows, gate_rows, impact_rows, queue_rows, summary)

    write_csv(OUT / "P8_Y5_R10_655_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_655_WEP_CLOSURE_GUARD.csv", WEP_rows)
    write_csv(OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv", premise_rows)
    write_csv(OUT / "P8_Y5_R10_655_R11_RETAINED_OPERATOR_VECTOR_STATUS.csv", R11_rows)
    write_csv(OUT / "P8_Y5_R10_655_EH_OR_R11_DECISION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_655_OBSERVABLE_IMPACT_MAP.csv", impact_rows)
    write_csv(OUT / "P8_Y5_R10_655_NEXT_ACTION_QUEUE.csv", queue_rows)
    write_csv(OUT / "P8_Y5_R10_655_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_655_VALIDATION.csv", validation)
    write_doc(source_rows, WEP_rows, premise_rows, R11_rows, gate_rows, impact_rows, queue_rows, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"EH_only_parent_theorem={summary[0]['EH_only_parent_theorem']}")
    print(f"R11_executable_vector_supplied={summary[0]['R11_executable_vector_supplied']}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
