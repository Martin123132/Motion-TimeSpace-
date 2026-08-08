from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def terminal_projection_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "TPT4496_0_standard_matter_descent",
            "target": "ordinary matter interface descent",
            "evidence": "4277 derives S_matter[Psi;Phi]=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))] for the standard branch.",
            "result": "CONDITIONAL_STANDARD_BRANCH_DERIVED",
            "applies_to_DeltaKTF_shell": False,
            "reason": "It closes g_X/b_dis/Dq_geom in the ordinary matter interface, but does not by itself prove the transition-shell metric response is absent.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "TPT4496_1_terminal_metric_alone",
            "target": "terminal public metric alone",
            "evidence": "4276 countermodels show terminality does not eliminate labels, source weights, field-renames or kernel motion.",
            "result": "REJECTED",
            "applies_to_DeltaKTF_shell": False,
            "reason": "Terminality alone cannot set C_DeltaKTF=0.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "TPT4496_2_DeltaKTF_kernel_membership",
            "target": "DeltaKTF is q-kernel / public-projection silent",
            "evidence": "4494/4495 leave Dg_public[DeltaK_TF]=0 as an unproved theorem target.",
            "result": "NOT_DERIVED",
            "applies_to_DeltaKTF_shell": False,
            "reason": "No current row proves DeltaKTF belongs to the same quotient-kernel silence class as the 4277 standard matter branch.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "TPT4496_3_nonlocal_owner_kernel",
            "target": "transition shell removed from local metric response by parent nonlocal owner/kernel",
            "evidence": "4284 says direct shell profile fails and a parent nonlocal owner/kernel theorem is required.",
            "result": "BEST_REMAINING_THEOREM_TARGET",
            "applies_to_DeltaKTF_shell": "future_only",
            "reason": "Would rescue the shell if derived; current corpus has not derived it.",
            "valid_for_claim": False,
        },
    ]


def shell_input_import_rows(shell_inputs: List[Dict[str, str]]) -> List[Dict[str, object]]:
    keep = {
        "SHELL4284_U_B",
        "SHELL4284_Pi_B",
        "SHELL4284_trace_gradient_proxy",
        "SHELL4284_u_shell",
        "SHELL4284_A_curv",
        "SHELL4284_B_env",
    }
    rows: List[Dict[str, object]] = []
    for row in shell_inputs:
        if row.get("input_id") not in keep:
            continue
        rows.append(
            {
                "import_id": "DSI4496_" + row["input_id"],
                "source_input_id": row["input_id"],
                "quantity": row["quantity"],
                "value": row["value"],
                "source_path": row["source_path"],
                "source_status": row["status"],
                "interpretation": "real transition-shell source-model input imported from 4284",
                "valid_for_claim": False,
            }
        )
    return rows


def shell_projection_comparator_rows(profile_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in profile_rows:
        if row.get("comparator_id") == "COMP4284_3_sector_tuned":
            status = "FORBIDDEN_CONTROL_NOT_EVIDENCE"
        elif row.get("comparator_id") == "COMP4284_4_exact_zero":
            status = "CONTROL_PASS_ONLY_IF_PARENT_THEOREM_EXISTS"
        else:
            status = "FAILS_WITHOUT_ADDITIONAL_SUPPRESSION"
        ratio = float(row["PPN_ratio_to_budget"])
        required_projection = (1.0 / ratio) if ratio > 0.0 else 0.0
        rows.append(
            {
                "shell_score_id": "DSP4496_" + row["comparator_id"],
                "source_comparator_id": row["comparator_id"],
                "scenario": row["scenario"],
                "S_PPN": row["S_PPN"],
                "PPN_ratio_to_budget": row["PPN_ratio_to_budget"],
                "required_projection_factor_to_pass": f"{required_projection:.15e}",
                "source_verdict": row["verdict"],
                "status": status,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def closure_crosswalk_rows(shell_rows: List[Dict[str, object]], closure_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    representative_closure = [
        row
        for row in closure_rows
        if row["profile_id"] == "PSEL4489_0_smoothstep_minN4_candidate"
        and row["abs_sK2_kappaSTF"] == "1.000000000000000e+09"
    ]
    closure_limit = float(representative_closure[0]["required_CDeltaKTF_max"]) if representative_closure else float("nan")
    rows: List[Dict[str, object]] = []
    for row in shell_rows:
        if row["scenario"] in {"sector_tuned_budget_row", "exact_theorem_zero_control"}:
            relation = "control_row_not_physical_input"
            harder_factor = ""
        else:
            required_projection = float(row["required_projection_factor_to_pass"])
            harder = required_projection / closure_limit if closure_limit > 0 else float("inf")
            relation = "shell_projection_requirement_is_looser_than_DeltaKTF_1e9_closure" if harder > 1.0 else "shell_projection_requirement_is_tighter_or_equal"
            harder_factor = f"{harder:.15e}"
        rows.append(
            {
                "crosswalk_id": "SCW4496_" + row["source_comparator_id"],
                "scenario": row["scenario"],
                "shell_required_projection_factor": row["required_projection_factor_to_pass"],
                "representative_DeltaKTF_1e9_CDeltaKTF_limit": f"{closure_limit:.15e}" if closure_limit == closure_limit else "",
                "ratio_shell_requirement_to_DeltaKTF_limit": harder_factor,
                "relation": relation,
                "interpretation": "4284 shell comparator and 4494 DeltaKTF comparator are separate but both demand tiny or exact projection coefficients",
                "valid_for_claim": False,
            }
        )
    return rows


def branch_verdict_rows() -> List[Dict[str, object]]:
    return [
        {
            "branch_id": "BV4496_0_standard_matter",
            "branch": "standard ordinary matter interface",
            "verdict": "CONDITIONALLY_CLOSED_FOR_GX_BDIS_DQGEOM",
            "basis": "4277 chain-rule descent through q(Phi)",
            "next_need": "left-hand EH/Newton operator limit and branch selector",
            "local_GR_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "BV4496_1_support_separated_collar",
            "branch": "support-separated compact collar",
            "verdict": "CONDITIONAL_ZERO_SELECTOR",
            "basis": "192/4176 no-flux plus 4288 finite-margin import",
            "next_need": "do not apply outside collar/no-flux hypotheses",
            "local_GR_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "BV4496_2_generic_transition_shell",
            "branch": "generic DeltaKTF / transition shell",
            "verdict": "DIRECT_PROFILE_FAILS_LARGE_FACTOR",
            "basis": "4284 direct shell profile comparator fails by ~2.3e16 for bare/U_B^2 rows",
            "next_need": "parent nonlocal owner/kernel theorem or explicit projection coefficient below threshold",
            "local_GR_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "BV4496_3_exact_zero_control",
            "branch": "exact theorem-zero control",
            "verdict": "WOULD_PASS_IF_PARENT_THEOREM_EXISTS",
            "basis": "4284 exact-zero control row",
            "next_need": "derive theorem; do not treat control as evidence",
            "local_GR_claim": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4496_0_matter_descent_crosswalk",
            "finding": "4277 helps the standard matter-interface branch but does not generically zero DeltaKTF shell response",
            "reason": "It closes g_X/b_dis/Dq_geom by quotient matter descent, while DeltaKTF public metric kernel membership remains unsigned.",
            "effect": "do not overextend standard branch descent to shell safety",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4496_1_real_shell_profile_imported",
            "finding": "real transition shell source-model rows are already present from 4284",
            "reason": "bare, U_B^2, and wide-shell scenarios fail by huge factors against PPN proxy budgets",
            "effect": "generic shell path needs nonlocal owner/kernel theorem or explicit tiny projection",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4496_2_next_route",
            "finding": "best next target is nonlocal owner/kernel theorem or arena transfer comparator",
            "reason": "direct local shell projection is not viable and exact zero remains a theorem target",
            "effect": "build owner-kernel conditions or make all arena rows consume the explicit shell projection factor",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    shell_rows: List[Dict[str, object]],
    crosswalk_rows: List[Dict[str, object]],
    branch_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    failing_shell = [row for row in shell_rows if row.get("status") == "FAILS_WITHOUT_ADDITIONAL_SUPPRESSION"]
    standard = [row for row in theorem_rows if row.get("theorem_id") == "TPT4496_0_standard_matter_descent"]
    return [
        {
            "gate_id": "CG4496_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "source-backed private theorem/comparator checkpoint",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4496_1_standard_branch_not_overextended",
            "requirement": "standard matter descent is present but not applied to generic DeltaKTF",
            "passed": bool(standard) and standard[0].get("result") == "CONDITIONAL_STANDARD_BRANCH_DERIVED" and standard[0].get("applies_to_DeltaKTF_shell") is False,
            "claim_allowed": False,
            "reason": "prevents theorem overreach",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4496_2_real_shell_failures_imported",
            "requirement": "4284 failing shell scenarios are imported",
            "passed": len(failing_shell) >= 3,
            "claim_allowed": False,
            "reason": "generic shell is empirically/comparator hard",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4496_3_crosswalk_rows",
            "requirement": "shell projection factors are crosswalked to DeltaKTF closure scale",
            "passed": len(crosswalk_rows) >= 5,
            "claim_allowed": False,
            "reason": "separate lanes made comparable without conflation",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4496_4_branch_verdicts",
            "requirement": "standard, collar, generic shell, and exact-zero branches are separated",
            "passed": len(branch_rows) >= 4 and any(row.get("verdict") == "DIRECT_PROFILE_FAILS_LARGE_FACTOR" for row in branch_rows),
            "claim_allowed": False,
            "reason": "branch hygiene preserved",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4496_5_local_GR",
            "requirement": "local-GR/J2/PPN claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "generic transition shell still requires nonlocal owner/kernel theorem or sourced projection coefficient",
            "valid_for_claim": False,
        },
    ]
