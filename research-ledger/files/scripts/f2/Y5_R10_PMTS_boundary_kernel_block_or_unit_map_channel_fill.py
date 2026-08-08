from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill"
DOC_PATH = ROOT / "604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_604_SOURCE_REGISTER.csv"
SECTOR_CHARGE_PATH = RESIDUALS / "P8_Y5_R10_604_SECTOR_CHARGE_THEOREM_ATTEMPT.csv"
KERNEL_BLOCK_PATH = RESIDUALS / "P8_Y5_R10_604_BOUNDARY_KERNEL_BLOCK_GATE.csv"
LEAK_GATE_PATH = RESIDUALS / "P8_Y5_R10_604_LEAK_COUNTEREXAMPLE_GATE.csv"
UNIT_MAP_FORK_PATH = RESIDUALS / "P8_Y5_R10_604_UNIT_MAP_FORK_STATUS.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_604_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_604_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_604_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_604_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_604_VALIDATION.csv"

PRIOR_603_VALIDATION = RESIDUALS / "P8_Y5_BRR545_603_VALIDATION.csv"
PRIOR_603_PRIMITIVE = RESIDUALS / "P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv"
PRIOR_603_OWNERSHIP = RESIDUALS / "P8_Y5_R10_603_PARENT_OWNERSHIP_GATE.csv"

STATUS = "Y5_R10_PMTS_boundary_kernel_block_theorem_written_parent_sector_charge_missing_unit_map_not_filled"
CLAIM_CEILING = "conditional_PMTS_kernel_block_theorem_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "605-Y5-R10-parent-sector-charge-origin-or-unit-map-demotion.md"
COMPACT_SHELL_PROXY = "7.432631961576971e-06"

SOURCE_FILES = [
    ("603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md", "immediate 603 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_603_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv", "A_D=b_D c_D primitive candidate"),
    ("source-intake/mts_residuals/P8_Y5_R10_603_PARENT_OWNERSHIP_GATE.csv", "P_MTS boundary-kernel blocker"),
    ("309-MTS-boundary-projector-contract-attempt.md", "P_MTS projector contract"),
    ("310-ordinary-MTS-sector-split-attempt.md", "ordinary/MTS block-kernel superselection lemma"),
    ("311-sector-label-SD-origin-attempt.md", "support label S_D and activity operator route"),
    ("323-S3-sector-label-combined-gate.md", "S3 singlet cannot replace sector label"),
    ("324-CD-activity-kernel-commutation-gate.md", "C_D activity and kernel-commutation gate"),
    ("328-topological-MTS-support-projector-gate.md", "P_top and P_MTS support projector route"),
    ("348-N5-projector-stress-conservation-theorem.md", "metric-independent/topological projector stress gate"),
    ("356-parent-action-ward-identity-and-projector-variation.md", "Ward ledger for projector/boundary/domain forces"),
    ("582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md", "boundary charge and momentum-map blocker"),
    ("scripts/Y5_R10_PMTS_boundary_kernel_block_or_unit_map_channel_fill.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_sector_charge_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "SCT604_0_boundary_space",
            "object": "boundary data space H_B(D)",
            "mathematical_form": "H_B(D)=H_ord plus H_MTS plus H_edge with boundary quadratic form <u,K_B v>_D",
            "claim_if_true": "ordinary bath, MTS memory, and edge/horizon/domain data can be represented before projection",
            "current_status": "definition_gate",
            "blocker": "physical decomposition is not a theorem until a parent charge labels the subspaces",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCT604_1_parent_sector_charge",
            "object": "Q_sec",
            "mathematical_form": "Q_sec^dagger=Q_sec; Q_sec u=q_ord u; Q_sec v=q_MTS v; Q_sec w=q_edge w with q_MTS distinct",
            "claim_if_true": "P_MTS is the spectral projector onto the nondegenerate q_MTS eigenspace",
            "current_status": "not_parent_derived",
            "blocker": "no current parent action supplies a conserved nondegenerate MTS sector charge",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCT604_2_projector_from_charge",
            "object": "P_MTS,D",
            "mathematical_form": "P_MTS,D = 1_{q_MTS}(Q_sec)",
            "claim_if_true": "P_MTS,D is not a hand filter; it is a spectral projector fixed by Q_sec",
            "current_status": "conditional_spectral_projector",
            "blocker": "depends entirely on SCT604_1 and nondegeneracy against edge/ordinary sectors",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCT604_3_kernel_commutation",
            "object": "boundary kernel K_B",
            "mathematical_form": "[K_B,Q_sec]=0",
            "claim_if_true": "K_B preserves Q_sec eigenspaces, so ordinary/MTS cross terms vanish",
            "current_status": "not_parent_derived",
            "blocker": "requires boundary action invariant under the Q_sec superselection symmetry",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCT604_4_cross_block_zero",
            "object": "K_cross",
            "mathematical_form": "for q_a != q_b, <u_a,K_B u_b>=0 because q_a<u_a,K_B u_b>=<u_a,Q_sec K_B u_b>=q_b<u_a,K_B u_b>",
            "claim_if_true": "ordinary coherent local baths cannot drive b_D through the MTS sector",
            "current_status": "proved_from_Qsec_commutation_premise",
            "blocker": "premises SCT604_1 and SCT604_3 are not derived",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCT604_5_stress_and_charge_ledger",
            "object": "projector/boundary stress",
            "mathematical_form": "delta_g P_MTS=0 if Q_sec is topological/internal and metric-independent; otherwise delta_g P_MTS is retained as residual",
            "claim_if_true": "no hidden Bianchi/projector-stress deletion",
            "current_status": "policy_gate_written",
            "blocker": "actual Q_sec type is missing, so stress fate is unknown",
            "valid_for_claim": "false",
        },
    ]


def make_kernel_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "KBG604_0_block_theorem",
            "requirement": "Q_sec self-adjoint, q_MTS nondegenerate, and [K_B,Q_sec]=0",
            "result_if_satisfied": "K_boundary is block diagonal between ordinary and MTS sectors",
            "current_status": "conditional_theorem",
            "failure_if_missing": "ordinary coherent local baths can leak into rho_MTS,D",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "KBG604_1_relation_to_A_D",
            "requirement": "P_MTS,D from Q_sec is used inside b_D and A_D=b_D c_D",
            "result_if_satisfied": "A_D activation is protected from ordinary bath pollution",
            "current_status": "conditional_support",
            "failure_if_missing": "A_D is a closure filter, not a parent primitive",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "KBG604_2_S3_insufficient",
            "requirement": "do not replace Q_sec with S3/coherent singlet alone",
            "result_if_satisfied": "ordinary isotropic thermal/EM singlets do not falsely count as MTS",
            "current_status": "guard_pass",
            "failure_if_missing": "P_singlet leaks ordinary coherent baths",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "KBG604_3_Ptop_insufficient",
            "requirement": "relative/topological projector P_top must be supplemented by P_MTS",
            "result_if_satisfied": "edge/horizon/topological classes do not degenerate with MTS top class",
            "current_status": "guard_pass",
            "failure_if_missing": "edge/top-class leakage survives",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "KBG604_4_Bianchi",
            "requirement": "projector/boundary/domain variations are zero by theorem or retained",
            "result_if_satisfied": "block split is compatible with the Ward/Bianchi ledger",
            "current_status": "open",
            "failure_if_missing": "hidden projector stress or boundary charge can re-enter q_loc",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "KBG604_5_verdict",
            "requirement": "parent action derives Q_sec and [K_B,Q_sec]=0",
            "result_if_satisfied": "P_MTS,D kernel block becomes a parent theorem",
            "current_status": "fail_current_corpus",
            "failure_if_missing": "selector route remains conditional; unit-map demotion becomes likely",
            "valid_for_claim": "false",
        },
    ]


def make_leak_rows() -> list[dict[str, str]]:
    return [
        {
            "leak_id": "LCG604_0_ordinary_isotropic_bath",
            "counterexample": "ordinary isotropic EM/thermal bath is coherent/IR but not MTS",
            "why_it_matters": "P_coh or S3 singlet alone would retain it",
            "required_blocker": "Q_sec with q_ord != q_MTS and P_MTS=1_{q_MTS}(Q_sec)",
            "current_status": "not_blocked_by_current_parent",
            "valid_for_claim": "false",
        },
        {
            "leak_id": "LCG604_1_edge_top_class",
            "counterexample": "edge/horizon/domain topological class has non-exact relative support",
            "why_it_matters": "P_top alone cannot distinguish it from MTS top class",
            "required_blocker": "nondegenerate sector charge with q_edge != q_MTS",
            "current_status": "not_blocked_by_current_parent",
            "valid_for_claim": "false",
        },
        {
            "leak_id": "LCG604_2_generic_boundary_mixing",
            "counterexample": "generic K_B has nonzero <H_ord,K_B H_MTS>",
            "why_it_matters": "even a defined P_MTS does not block mixing unless K_B commutes with Q_sec",
            "required_blocker": "boundary action symmetry giving [K_B,Q_sec]=0",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "leak_id": "LCG604_3_metric_projector_stress",
            "counterexample": "metric-dependent spectral/Hodge projector varies with g",
            "why_it_matters": "projector stress can act as a hidden local source",
            "required_blocker": "topological/internal Q_sec or explicit retained stress row",
            "current_status": "open",
            "valid_for_claim": "false",
        },
        {
            "leak_id": "LCG604_4_hard_support_instability",
            "counterexample": "tiny ordinary/MTS mixing makes hard support projector activate",
            "why_it_matters": "exact superselection is required; approximate separation is a numeric residual problem",
            "required_blocker": "exact Q_sec theorem or demote to unit-map/residual scoring",
            "current_status": "open",
            "valid_for_claim": "false",
        },
    ]


def make_unit_map_rows() -> list[dict[str, str]]:
    return [
        {
            "fork_id": "UMF604_0_derivation_status",
            "route": "P_MTS boundary-kernel derivation",
            "status": "conditional_theorem_written_parent_charge_missing",
            "why": "Q_sec would derive both P_MTS and K_cross=0, but Q_sec itself is absent",
            "required_next_input": "derive parent sector charge origin or demote",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "UMF604_1_unit_map_warning",
            "route": "compact-shell unit map",
            "status": "likely_next_if_Qsec_fails",
            "why": "without Q_sec, further selector work risks circling the same projector closure",
            "required_next_input": "choose R10 alpha(lambda), PPN vector, WEP, or clock channel",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "UMF604_2_no_score",
            "route": "local-bound evidence",
            "status": "no_claim",
            "why": f"proxy {COMPACT_SHELL_PROXY} remains unconverted and no P_MTS theorem-zero certificate exists",
            "required_next_input": "source-backed coefficient/unit map or accepted theorem-zero gate",
            "valid_for_claim": "false",
        },
    ]


def make_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RU604_0_PMTS_kernel",
            "previous_status": "P_MTS_boundary_kernel_block_missing",
            "new_status": "conditional_Qsec_kernel_theorem_written",
            "reason": "self-adjoint Q_sec plus [K_B,Q_sec]=0 proves ordinary/MTS cross block zero",
            "still_needed": "parent origin of Q_sec and its nondegenerate MTS eigenvalue",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU604_1_ND_primitive",
            "previous_status": "A_D_zero_nonzero_candidate_conditionally_derived",
            "new_status": "blocked_on_Qsec_parent_origin",
            "reason": "b_D is protected only if P_MTS,D is parent-derived by Q_sec",
            "still_needed": "Q_sec or explicit residual/unit-map demotion",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU604_2_q_loc_local_GR",
            "previous_status": "q_loc_R11_boundary_open",
            "new_status": "still_open",
            "reason": "kernel block theorem does not close boundary charge, R11, source-normalization, or full q_loc",
            "still_needed": "local residual rows zeroed or scored",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU604_3_unit_map",
            "previous_status": "fallback_deferred",
            "new_status": "queued_if_Qsec_origin_fails",
            "reason": "604 narrows the final derivation lock to a parent sector charge",
            "still_needed": "if Q_sec fails, choose channel and fill physical unit map",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D604_0_kernel_theorem",
            "decision": "accept Q_sec commutation as the exact P_MTS kernel theorem target",
            "meaning": "if Q_sec exists and [K_B,Q_sec]=0, ordinary/MTS boundary mixing is zero by superselection",
            "claim_status": "conditional_not_promoted",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D604_1_missing_parent_charge",
            "decision": "do not claim P_MTS is parent-derived",
            "meaning": "the current corpus has no conserved nondegenerate MTS sector charge",
            "claim_status": "no_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D604_2_unit_map_pressure",
            "decision": "put unit-map demotion on deck",
            "meaning": "if the next step cannot derive Q_sec, the disciplined move is to stop stacking conditional projector clauses and score the closure branch",
            "claim_status": "fallback_queued",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D604_3_promotion",
            "decision": "forbid local-GR/PPN/R10 promotion",
            "meaning": "P_MTS kernel theorem is conditional and does not close q_loc/R11/boundary debts",
            "claim_status": "forbidden",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU604_0_allowed",
            "allowed_after_604": "try one focused parent-sector-charge origin step",
            "forbidden_after_604": "relabel P_MTS as derived from S3, P_coh, P_top, or ordinary gauge invariance alone",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU604_1_allowed",
            "allowed_after_604": "use Q_sec commutation theorem as a conditional exact result",
            "forbidden_after_604": "use conditional block algebra as local-bound evidence",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU604_2_allowed",
            "allowed_after_604": "demote to compact-shell unit-map scoring if Q_sec origin fails",
            "forbidden_after_604": "continue indefinitely through equivalent projector closures",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S604_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "kernel_status": "Qsec_commutation_theorem_conditional",
            "P_MTS_status": "spectral_projector_if_parent_sector_charge_exists",
            "main_blocker": "parent_Qsec_origin_and_non_degeneracy_missing",
            "unit_map_status": "queued_if_Qsec_fails",
            "best_private_read": "604 proves the exact algebra we need: a self-adjoint parent sector charge commuting with the boundary kernel gives P_MTS and kills ordinary/MTS cross mixing. The theory still lacks the parent charge, so this is not a P_MTS theorem yet.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    leak_rows: list[dict[str, str]],
    unit_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_603_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result", "").strip().lower() != "pass"]
    prior_primitive = read_csv(PRIOR_603_PRIMITIVE)
    prior_ownership = read_csv(PRIOR_603_OWNERSHIP)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in sector_rows if row["valid_for_claim"] == "true"],
        *[row for row in kernel_rows if row["valid_for_claim"] == "true"],
        *[row for row in leak_rows if row["valid_for_claim"] == "true"],
        *[row for row in unit_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    qsec_missing = any(row["theorem_id"] == "SCT604_1_parent_sector_charge" and row["current_status"] == "not_parent_derived" for row in sector_rows)
    cross_block = any(row["theorem_id"] == "SCT604_4_cross_block_zero" for row in sector_rows)
    verdict_fail = any(row["gate_id"] == "KBG604_5_verdict" and row["current_status"] == "fail_current_corpus" for row in kernel_rows)
    ordinary_leak = any(row["leak_id"] == "LCG604_0_ordinary_isotropic_bath" for row in leak_rows)
    edge_leak = any(row["leak_id"] == "LCG604_1_edge_top_class" for row in leak_rows)
    unit_queued = any(row["fork_id"] == "UMF604_1_unit_map_warning" and "likely_next" in row["status"] for row in unit_rows)
    local_gr_open = any(row["runner_id"] == "RU604_2_q_loc_local_GR" and row["new_status"] == "still_open" for row in runner_rows)
    return [
        {
            "check_id": "V604_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V604_1_prior_603_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};primitive_rows={len(prior_primitive)};ownership_rows={len(prior_ownership)}",
        },
        {
            "check_id": "V604_2_Qsec_block_theorem_written",
            "result": "pass" if qsec_missing and cross_block else "fail",
            "detail": f"Qsec_missing={qsec_missing};cross_block_theorem={cross_block}",
        },
        {
            "check_id": "V604_3_kernel_not_promoted",
            "result": "pass" if verdict_fail else "fail",
            "detail": "parent Q_sec and kernel commutation not derived",
        },
        {
            "check_id": "V604_4_leak_guards_retained",
            "result": "pass" if ordinary_leak and edge_leak else "fail",
            "detail": f"ordinary_leak_guard={ordinary_leak};edge_leak_guard={edge_leak}",
        },
        {
            "check_id": "V604_5_unit_map_queued_and_local_GR_open",
            "result": "pass" if unit_queued and local_gr_open else "fail",
            "detail": f"unit_queued={unit_queued};local_GR_open={local_gr_open};proxy={COMPACT_SHELL_PROXY}",
        },
        {
            "check_id": "V604_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V604_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    leak_rows: list[dict[str, str]],
    unit_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 604 Y5 R10 P_MTS boundary-kernel block or unit-map channel fill

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The exact block-kernel theorem is now written: if a self-adjoint parent sector charge `Q_sec` has a nondegenerate MTS eigenvalue and `[K_B,Q_sec]=0`, then the MTS spectral projector `P_MTS,D=1_(q_MTS)(Q_sec)` is parent-fixed and ordinary/MTS cross-kernel terms vanish.
- This is the right derivation shape for protecting `b_D` and therefore `A_D=b_D c_D` from ordinary bath pollution.
- The theorem is not promoted: the current corpus does not derive `Q_sec`, its nondegeneracy against ordinary/edge sectors, or the boundary action symmetry that gives `[K_B,Q_sec]=0`.
- This puts real pressure on the next step: derive the parent sector charge, or stop circling the projector lock and demote to compact-shell unit-map scoring.

## Kernel Theorem
For boundary eigenmodes:

```text
Q_sec u_a = q_a u_a
Q_sec u_b = q_b u_b
[K_B,Q_sec]=0
```

then:

```text
q_a <u_a,K_B u_b> = <u_a,Q_sec K_B u_b>
                 = <u_a,K_B Q_sec u_b>
                 = q_b <u_a,K_B u_b>.
```

So if `q_a != q_b`:

```text
<u_a,K_B u_b> = 0.
```

That is the clean ordinary/MTS block split. The missing physics is the parent origin of `Q_sec`.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Sector-Charge Theorem Attempt
{markdown_table(sector_rows, ["theorem_id", "object", "mathematical_form", "claim_if_true", "current_status", "blocker", "valid_for_claim"])}

## Boundary Kernel Block Gate
{markdown_table(kernel_rows, ["gate_id", "requirement", "result_if_satisfied", "current_status", "failure_if_missing", "valid_for_claim"])}

## Leak Counterexample Gate
{markdown_table(leak_rows, ["leak_id", "counterexample", "why_it_matters", "required_blocker", "current_status", "valid_for_claim"])}

## Unit-Map Fork Status
{markdown_table(unit_rows, ["fork_id", "route", "status", "why", "required_next_input", "valid_for_claim"])}

## Runner Update
{markdown_table(runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_604", "forbidden_after_604", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a clean theorem-shaped result, but it is still a conditional shot. The good news: if `Q_sec` exists, the ordinary/MTS split is not handwaving. The hard news: without `Q_sec`, `P_MTS` is still a smart filter rather than a parent-owned object. Next we either derive that sector charge or we stop burning rounds and build the unit-map scorer.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    sector_rows = make_sector_charge_rows()
    kernel_rows = make_kernel_rows()
    leak_rows = make_leak_rows()
    unit_rows = make_unit_map_rows()
    runner_rows = make_runner_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, sector_rows, kernel_rows, leak_rows, unit_rows, runner_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        SECTOR_CHARGE_PATH,
        sector_rows,
        ["theorem_id", "object", "mathematical_form", "claim_if_true", "current_status", "blocker", "valid_for_claim"],
    )
    write_csv(KERNEL_BLOCK_PATH, kernel_rows, ["gate_id", "requirement", "result_if_satisfied", "current_status", "failure_if_missing", "valid_for_claim"])
    write_csv(LEAK_GATE_PATH, leak_rows, ["leak_id", "counterexample", "why_it_matters", "required_blocker", "current_status", "valid_for_claim"])
    write_csv(UNIT_MAP_FORK_PATH, unit_rows, ["fork_id", "route", "status", "why", "required_next_input", "valid_for_claim"])
    write_csv(RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_604", "forbidden_after_604", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "claim_allowed",
            "R10_pass",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "kernel_status",
            "P_MTS_status",
            "main_blocker",
            "unit_map_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        sector_rows,
        kernel_rows,
        leak_rows,
        unit_rows,
        runner_rows,
        decision_rows,
        route_update_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
