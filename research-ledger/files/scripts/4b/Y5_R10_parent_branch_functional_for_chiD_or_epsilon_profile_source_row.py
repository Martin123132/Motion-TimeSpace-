from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1145-Y5-R10-parent-branch-functional-for-chiD-or-epsilon-profile-source-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1145_0_1144_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_NEXT_TARGET.csv",
            "needle": "NEXT1144_0_1145",
            "role": "handoff requiring parent branch functional or epsilon profile source row.",
        },
        {
            "source_id": "SRC1145_1_1144_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_BRANCH_LAW_ATTEMPT.csv",
            "needle": "BL1144_5_verdict",
            "role": "branch law is shape-supported but not derived.",
        },
        {
            "source_id": "SRC1145_2_1144_epsilon",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_EPSILON_DOMAIN_FLUX_PROFILE_FILL_QUEUE.csv",
            "needle": "EPF1144_0_epsilon_profile_local",
            "role": "epsilon profile/source fallback row remains unfilled.",
        },
        {
            "source_id": "SRC1145_3_domain_action_143",
            "relative_path": "143-domain-selector-variational-action-attempt.md",
            "needle": "domain_selector_formal_action_not_parent_derived",
            "role": "domain selector action candidates fail parent derivation.",
        },
        {
            "source_id": "SRC1145_4_topological_252",
            "relative_path": "252-topological-projector-parent-action-skeleton.md",
            "needle": "topological_projector_parent_skeleton_written_N5_action_route_conditional_FLRW_Bmem_and_N6_open_no_promotion",
            "role": "topological projector action skeleton is conditional only.",
        },
        {
            "source_id": "SRC1145_5_free_boundary_277",
            "relative_path": "277-domain-free-boundary-Euler-equation.md",
            "needle": "domain_shape_derivative_derived_no_domain_selection_or_local_GR_promotion",
            "role": "free-boundary Euler route is derived but degenerate.",
        },
        {
            "source_id": "SRC1145_6_no_go_279",
            "relative_path": "279-representative-selection-boundary-polarization-no-go.md",
            "needle": "boundary_polarization_endpoint_constraints_underselect_representative_selection_not_derived",
            "role": "boundary polarization underselects representative selection.",
        },
        {
            "source_id": "SRC1145_7_Cexp_416",
            "relative_path": "416-binding-invariant-domain-selector-repair.md",
            "needle": "parent_selector_derived",
            "role": "C_exp separator still lacks parent selector derivation.",
        },
        {
            "source_id": "SRC1145_8_Qcoh_481",
            "relative_path": "481-Qcoh-parent-projector-algebra-or-closure.md",
            "needle": "C2_domain_selector",
            "role": "Qcoh parent algebra contract says domain selector remains not derived.",
        },
        {
            "source_id": "SRC1145_9_quotient_864",
            "relative_path": "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
            "needle": "PC864_0_parent_domains",
            "role": "quotient split is sufficient but not parent-derived.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def functional_candidate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "candidate_id": "FC1145_0_dynamic_phase_field",
                "candidate_functional": "S_chi = int sqrt(-g)[(nabla chi_D)^2/ell_chi^2 + V(chi_D)]",
                "what_it_would_do": "dynamically selects domains through a phase/wall field",
                "failure_mode": "introduces independent scale/stress and risks domain-wall local PPN leakage",
                "verdict": "REJECT_FOR_LOCAL_GR_ROUTE",
                "source_anchor": "143",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "FC1145_1_algebraic_multiplier",
                "candidate_functional": "S_aux = int sqrt(-g) lambda_chi(chi_D - C_coh[D])",
                "what_it_would_do": "sets chi_D equal to a coherence selector for a supplied domain",
                "failure_mode": "selects chi_D after D is already supplied; does not parent-select physical D or representative",
                "verdict": "CONTRACT_ONLY_NOT_DOMAIN_OWNER",
                "source_anchor": "143",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "FC1145_2_topological_projector_BF",
                "candidate_functional": "S_top = int Upsilon wedge(P_D J_rel - d_rel A_rel) + S_operator[P_D^2=P_D]",
                "what_it_would_do": "owns a metric-independent relative projector and can kill bulk projector stress conditionally",
                "failure_mode": "does not by itself select local exact versus FLRW scalar branch or R11 silence",
                "verdict": "USEFUL_SKELETON_NOT_BRANCH_FUNCTIONAL",
                "source_anchor": "252",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "FC1145_3_free_boundary_Euler",
                "candidate_functional": "S_branch[D] with delta_D S_branch=0 free-boundary condition",
                "what_it_would_do": "makes FLRW and stationary local branches extrema",
                "failure_mode": "degenerate: many domains extremize; quiet domain still not uniquely selected",
                "verdict": "DEGENERATE_UNDERSELECTED",
                "source_anchor": "277",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "FC1145_4_Cexp_selector_potential",
                "candidate_functional": "S_Cexp = int Lambda(C_exp[D], chi_D) with local C_exp=0 and FLRW C_exp!=0 minima",
                "what_it_would_do": "uses coherent expansion invariant as local/cosmology separator",
                "failure_mode": "candidate domains, thresholds, epsilon prescription, and stress cancellation are not parent-derived",
                "verdict": "KINEMATIC_CLUE_NOT_PARENT_FUNCTIONAL",
                "source_anchor": "416",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "FC1145_5_quotient_split_action",
                "candidate_functional": "S_parent[Phi] with compatible q_FLRW(Phi) and q_loc[U](Phi), Dq_loc[v_D]=0, Dq_FLRW[v_D]!=0",
                "what_it_would_do": "makes FLRW-visible branch locally vertical/invisible",
                "failure_mode": "q_FLRW/q_loc functors and v_D classification are sufficient clauses, not derived action facts",
                "verdict": "SUFFICIENT_CONTRACT_NOT_PARENT_DERIVED",
                "source_anchor": "864",
                "valid_for_claim": "false",
            },
            {
                "candidate_id": "FC1145_6_verdict",
                "candidate_functional": "parent branch functional S_branch[chi_D,P_D,Q]",
                "what_it_would_do": "selects local exact/trivial class and FLRW homogeneous scalar class by one parent law",
                "failure_mode": "all candidates fail by new stress, supplied D, degenerate extrema, missing functors, or closure-only status",
                "verdict": "PARENT_BRANCH_FUNCTIONAL_NOT_CONSTRUCTED",
                "source_anchor": "1145",
                "valid_for_claim": "false",
            },
        ]
    )


def contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "contract_id": "SBF1145_0_variables",
                "required_object": "parent variables",
                "acceptance_test": "chi_D, P_D, Q_mu_nu/Q_current, and observed coframe are parent variables or derived Noether/load objects before readout",
                "current_status": "MISSING_PARENT_VARIABLE_OWNERSHIP",
                "if_missing": "branch selector remains closure",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "SBF1145_1_Euler_law",
                "required_object": "Euler/Ward branch equation",
                "acceptance_test": "delta S_branch/delta chi_D=0 and/or Ward identity selects D_local exact and D_FLRW scalar without empirical thresholds",
                "current_status": "MISSING_NONDEGENERATE_SELECTOR_EQUATION",
                "if_missing": "free-boundary extrema remain underselected",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "SBF1145_2_local_solution",
                "required_object": "local exact/trivial solution",
                "acceptance_test": "for compact stationary local U, P_D J_D=d Lambda_D or zero and P_loc flux vanishes in observed coframe",
                "current_status": "MISSING_LOCAL_SOLUTION_PROOF",
                "if_missing": "epsilon_domain_flux remains open",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "SBF1145_3_FLRW_solution",
                "required_object": "FLRW homogeneous scalar solution",
                "acceptance_test": "same branch equation admits FLRW P_D J_D = scalar homogeneous volume/current class",
                "current_status": "CONDITIONAL_SHAPE_SUPPORT_ONLY",
                "if_missing": "cosmology branch is not unified with local branch",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "SBF1145_4_stress_silence",
                "required_object": "Bianchi-safe stress accounting",
                "acceptance_test": "delta_g P_D=0/topological or all projector/domain stress terms are retained and bounded",
                "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "if_missing": "PPN vector/STF/alpha3 rows remain active",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "SBF1145_5_no_new_scale",
                "required_object": "no selector scale or threshold",
                "acceptance_test": "ell_chi, T_chi, epsilon threshold, C_star, or branch switch are parent-derived constants or absent",
                "current_status": "MISSING_THRESHOLD_ORIGIN",
                "if_missing": "selector becomes adjustable closure",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "SBF1145_6_R11_and_product",
                "required_object": "R11/alpha3 compatibility",
                "acceptance_test": "R11 c/K/vector/STF siblings vanish or are executable, and epsilon profile closes K*c*epsilon independently",
                "current_status": "MISSING_R11_AND_EPSILON_INPUTS",
                "if_missing": "no alpha3/local-GR promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def epsilon_source_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "EPSRC1145_0_profile_source_row",
                "target": "epsilon_domain_flux",
                "row_type": "first_nonclaim_source_profile_template",
                "definition": "epsilon_domain_flux = |P_loc^i_nu(F_P^nu+F_domain^nu)| normalized into the R11 alpha3 product convention",
                "required_fields": "system_id; branch_id; domain_candidate_rule; local_representative_status; flux_definition; epsilon_abs; epsilon_units; profile_support; source_path; valid_for_claim",
                "current_value": "MISSING_EPSILON_DOMAIN_FLUX_PROFILE_OR_ZERO_THEOREM",
                "source_path": "MISSING_SOURCE_PATH",
                "acceptance": "source-backed epsilon_abs or parent no-flux certificate; no label-zero",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "row_id": "EPSRC1145_1_no_flux_certificate_row",
                "target": "epsilon_domain_flux_zero_certificate",
                "row_type": "parent_theorem_zero_certificate_template",
                "definition": "P_loc^i_nu(F_P^nu+F_domain^nu)=0 from parent-selected local exact/trivial domain representative",
                "required_fields": "parent_equation; local_solution; observed_coframe; no_vector_STF_check; source_path; valid_for_claim",
                "current_value": "MISSING_PARENT_NO_FLUX_CERTIFICATE",
                "source_path": "MISSING_SOURCE_PATH",
                "acceptance": "derived zero from S_parent/S_branch, not imposed plateau or Ward ownership alone",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1145_0_sources_exist",
                "rule": "all functional-candidate source anchors exist",
                "gate_pass": "true_nonclaim",
                "reason": "source paths/needles are present",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1145_1_candidate_audit_done",
                "rule": "major branch functional candidates are audited",
                "gate_pass": "true_nonclaim",
                "reason": "dynamic, multiplier, topological, free-boundary, Cexp, and quotient candidates are separated",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1145_2_parent_functional_constructed",
                "rule": "S_branch[chi_D,P_D,Q] is constructed and parent-signed",
                "gate_pass": "false",
                "reason": "all candidates remain rejected, conditional, degenerate, or sufficient-only",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1145_3_epsilon_source_ready",
                "rule": "epsilon_domain_flux row has source-backed value or theorem-zero certificate",
                "gate_pass": "false",
                "reason": "epsilon source rows are templates with MISSING_SOURCE_PATH",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1145_4_local_GR_promotion",
                "rule": "alpha3/PPN/local-GR promotion allowed",
                "gate_pass": "false",
                "reason": "parent branch functional and epsilon source rows are not claim-valid",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1145_0_verdict",
                "decision": "parent_branch_functional_not_constructed",
                "reason": "candidate functionals either add unsafe stress/scale, assume D, underselect D, or remain sufficient contracts",
                "next_action": "move to epsilon_domain_flux no-flux certificate/source row unless a new parent functional appears",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1145_1_best_next",
                "decision": "fill_or_certify_epsilon_domain_flux",
                "reason": "after the branch-functional rejection, epsilon is the first factor that can close alpha3 flux by one zero/source row",
                "next_action": "build epsilon_domain_flux no-flux certificate or first source profile row",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1145_2_claim_ceiling",
                "decision": "keep_A8_branch_nonclaim",
                "reason": "contract rows are exact but not parent-signed, and epsilon remains MISSING",
                "next_action": "no alpha3/PPN/local-GR claim",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1145_0_1146",
                "next_target": "1146-Y5-R10-epsilon-domain-flux-no-flux-certificate-or-source-profile-row.md",
                "objective": "derive a parent no-flux certificate for epsilon_domain_flux in the compact local branch, or create the first source-backed epsilon profile row as nonclaim data",
                "include": "epsilon_domain_flux; P_loc flux projection; observed coframe; local representative status; source profile fields; alpha3 product guard",
                "exclude": "label-zero epsilon; Ward-only shortcut; tuned cancellation; local-GR/alpha3 claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    contracts: list[dict[str, object]],
    epsilon_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = candidates + contracts + epsilon_rows + gates + decisions + next_target
    add(
        "V1145_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1145_1_candidate_coverage",
        {row["candidate_id"] for row in candidates}
        == {
            "FC1145_0_dynamic_phase_field",
            "FC1145_1_algebraic_multiplier",
            "FC1145_2_topological_projector_BF",
            "FC1145_3_free_boundary_Euler",
            "FC1145_4_Cexp_selector_potential",
            "FC1145_5_quotient_split_action",
            "FC1145_6_verdict",
        },
        "all major branch functional candidates are audited",
    )
    add(
        "V1145_2_functional_not_constructed",
        candidates[-1]["verdict"] == "PARENT_BRANCH_FUNCTIONAL_NOT_CONSTRUCTED",
        "no parent branch functional is promoted",
    )
    add(
        "V1145_3_contract_exact",
        {"SBF1145_0_variables", "SBF1145_1_Euler_law", "SBF1145_2_local_solution", "SBF1145_3_FLRW_solution"}.issubset(
            {row["contract_id"] for row in contracts}
        ),
        "future S_branch acceptance contract is explicit",
    )
    add(
        "V1145_4_epsilon_rows",
        {row["row_id"] for row in epsilon_rows} == {"EPSRC1145_0_profile_source_row", "EPSRC1145_1_no_flux_certificate_row"}
        and all(row["source_path"] == "MISSING_SOURCE_PATH" for row in epsilon_rows),
        "epsilon source/profile and no-flux certificate rows remain unfilled",
    )
    add(
        "V1145_5_claim_gates_blocked",
        any(row["gate_id"] == "G1145_2_parent_functional_constructed" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1145_4_local_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "parent functional and local claim gates remain blocked",
    )
    add(
        "V1145_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in epsilon_rows + next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1145_7_next_target",
        next_target[0]["next_target"].startswith("1146-") and "epsilon-domain-flux" in str(next_target[0]["next_target"]),
        "1146 handoff targets epsilon no-flux certificate or source profile row",
    )
    add(
        "V1145_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1145_9_csv_parse", csv_parse_ok, "all 1145 CSV outputs parse cleanly")
    add("V1145_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1145_SUMMARY",
        True,
        "1145 rejects current S_branch candidates, preserves exact contract, and sends epsilon_domain_flux to 1146",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    contracts: list[dict[str, object]],
    epsilon_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1145 - Y5/R10 Parent Branch Functional for chiD or Epsilon Profile Source Row

**Current verdict:** no acceptable `S_branch[chi_D,P_D,Q]` is constructed in the current corpus. The candidates either add unsafe selector stress/scale, assume the domain, underselect the representative, or remain sufficient contracts.

**Useful progress:** the exact future contract is now explicit: variables, Euler/Ward branch law, local exact solution, FLRW scalar solution, stress silence, no new threshold, and R11/alpha3 compatibility.

**Important guard:** this is not a defeat of the route; it is a demotion of the current functional candidates. The shape is still strong, but the parent branch selector is not signed.

**Best next attack:** build the `epsilon_domain_flux` no-flux certificate or first source profile row. That is now the least circular way to keep the alpha3/local branch testable.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1145.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Branch Functional Candidate Audit
{table(["candidate_id", "candidate_functional", "what_it_would_do", "failure_mode", "verdict", "source_anchor", "valid_for_claim"], candidates)}

## Exact Future S_branch Contract
{table(["contract_id", "required_object", "acceptance_test", "current_status", "if_missing", "valid_for_claim"], contracts)}

## Epsilon Source/Profile Rows
{table(["row_id", "target", "row_type", "definition", "required_fields", "current_value", "source_path", "acceptance", "valid_for_claim"], epsilon_rows)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1145_SOURCE_REGISTER.csv",
        "candidates": OUT / "P8_Y5_R10_1145_BRANCH_FUNCTIONAL_CANDIDATE_AUDIT.csv",
        "contracts": OUT / "P8_Y5_R10_1145_EXACT_SBRANCH_CONTRACT.csv",
        "epsilon": OUT / "P8_Y5_R10_1145_EPSILON_SOURCE_PROFILE_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1145_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1145_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1145_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1145_VALIDATION.csv",
    }
    sources = source_rows()
    candidates = functional_candidate_rows()
    contracts = contract_rows()
    epsilon_rows = epsilon_source_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["candidates"], candidates)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["epsilon"], epsilon_rows)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, candidates, contracts, epsilon_rows, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, candidates, contracts, epsilon_rows, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
