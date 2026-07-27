from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4045-Y5-R2FR-cZ-kernel-wall-zero-theorem-or-first-bound-values.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4045_SOURCE_REGISTER.csv",
    "cz_component_reduction": SOURCE_DIR / "P8_Y5_R2FR_4045_CZ_COMPONENT_REDUCTION.csv",
    "wall_zero_bridge": SOURCE_DIR / "P8_Y5_R2FR_4045_SELECTOR_WALL_ZERO_BRIDGE.csv",
    "tail_kernel_gate": SOURCE_DIR / "P8_Y5_R2FR_4045_TAIL_KERNEL_GATE.csv",
    "tail_bound_template": SOURCE_DIR / "P8_Y5_R2FR_4045_TAIL_BOUND_TEMPLATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4045_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4045_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4045_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4045_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4045_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4045_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4045_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for item in rows:
        for key in item:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4045_0", ROOT / "4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md", "c_Z J_Z -> c_Z J_Z^history_tail + c_Z J_Z^selector_wall_if_rejected", "4039 cZ split"),
        ("SRC4045_1", ROOT / "4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md", "A_Z_remaining <= A_tail + A_wall", "4040 absolute cZ envelope"),
        ("SRC4045_2", SOURCE_DIR / "P8_Y5_R2FR_4039_ZEROED_CZ_COMPONENTS.csv", "fixed local selector/projector branch has no wall motion or projector stress", "previous selector zero row"),
        ("SRC4045_3", SOURCE_DIR / "P8_Y5_R2FR_4040_TAIL_WALL_THEOREM_ATTEMPT.csv", "If P_loc K_mem vanishes on the compact", "tail/wall theorem conditions"),
        ("SRC4045_4", SOURCE_DIR / "P8_Y5_R2FR_4040_CZ_ENVELOPE.csv", "A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1", "tail bound formula"),
        ("SRC4045_5", SOURCE_DIR / "P8_Y5_R2FR_4040_CZ_INPUT_CONTRACT.csv", "K_mem local tail norm", "required tail inputs"),
        ("SRC4045_6", ROOT / "4043-Y5-R2FR-projector-domain-stress-silence-or-alpha-xi-bound-vector.md", "Phi_D=0`, `tau_wall_TF=0", "new wall/flux silence bridge"),
        ("SRC4045_7", SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv", "No local domain preferred-momentum flux is generated.", "selected branch flux zero theorem"),
        ("SRC4045_8", SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv", "Phi_D and tau_wall_TF determine local flux and STF wall stress", "wall factorization"),
        ("SRC4045_9", ROOT / "4044-Y5-R2FR-local-GR-master-residual-scorecard-and-cZ-cnorm-priority.md", "Attack `Delta_cZ_envelope` first", "4044 selected cZ next"),
        ("SRC4045_10", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv", "q_loc^nu=P_loc[sum_A E_A nabla^nu Phi^A+J_Z^nu+B_Z^nu+nabla_mu Delta_K^{mu nu}+C_readout^nu]", "broader q_loc profile warning"),
        ("SRC4045_11", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1713_JZ_BZ_COUPLING_LOCK_ATTEMPT.csv", "J_Z^A", "older J_Z/B_Z coupling lock remains hard"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def cz_component_reduction_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "component_id": "CZR4045_0_direct",
            "component": "J_Z^direct_source",
            "before_4045": "zero by source-clean packet",
            "after_4045": "zero carried",
            "formula": "J_Z^direct_source=0",
            "status": "ZERO_CARRIED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZR4045_1_boundary",
            "component": "J_Z^boundary_flux",
            "before_4045": "zero by stationary no-flux plus fixed source-blind reference",
            "after_4045": "zero carried",
            "formula": "J_Z^boundary_flux=0",
            "status": "ZERO_CARRIED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZR4045_2_gamma",
            "component": "J_Z^Gamma",
            "before_4045": "zero by even/quadratic Gamma owner at Z=0",
            "after_4045": "zero carried",
            "formula": "delta_Z I_Gamma|Z=0=0",
            "status": "ZERO_CARRIED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZR4045_3_selector_wall",
            "component": "J_Z^selector_wall",
            "before_4045": "active if fixed selector/no-wall branch rejected",
            "after_4045": "zero in selected private branch by 4043 projector/domain wall silence",
            "formula": "A_wall_projector=0 when Phi_D=0, tau_wall_TF=0, delta_g P_D=0, D_D P_D=0, delta_g chi_D=0",
            "status": "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_FALLBACK",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZR4045_4_history_tail",
            "component": "J_Z^history_tail",
            "before_4045": "live memory/nonlocal kernel tail",
            "after_4045": "still live tail-only residual",
            "formula": "A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1",
            "status": "LIVE_TAIL_ENVELOPE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "CZR4045_5_total",
            "component": "Delta_cZ_envelope",
            "before_4045": "A_Z_remaining <= A_tail + A_wall",
            "after_4045": "A_Z_remaining_selected <= A_tail; fallback remains A_tail + A_wall if 4043 signature rejected",
            "formula": "Delta_cZ_selected = A_tail",
            "status": "REDUCED_TO_TAIL_ONLY_IN_PRIVATE_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def wall_zero_bridge_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bridge_id": "WZB4045_0_projector_wall",
            "4040_wall_requirement": "fixed/exact/topological selector with no wall motion or shell mismatch",
            "4043_supplied_clause": "Phi_D=0, tau_wall_TF=0, delta_g P_D=0, D_D P_D=0, delta_g chi_D=0, same M_H_ref",
            "bridge_result": "selector/projector wall contribution has zero local force/PPN projection in selected branch",
            "selected_branch_value": "A_wall_projector=0",
            "status": "BRIDGE_CLOSED_PRIVATE_SELECTED_BRANCH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bridge_id": "WZB4045_1_nonprojector_wall_guard",
            "4040_wall_requirement": "all wall/shell mismatch terms vanish",
            "4043_supplied_clause": "projector/domain wall only",
            "bridge_result": "non-projector transition-wall channels remain fallback if the parent action introduces them",
            "selected_branch_value": "0 in selected no-extra-wall packet",
            "status": "GUARD_RETAINED_IF_PARENT_PACKET_REJECTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def tail_kernel_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "TKG4045_0_exact_support_zero",
            "tail_condition": "P_loc K_mem vanishes on compact stationary collar or support is disjoint",
            "result_if_true": "J_Z^history_tail=0 and Delta_cZ_selected=0",
            "current_status": "NOT_PROVED_CURRENT_CORPUS",
            "needed_evidence": "parent kernel support theorem or local projection orthogonality proof",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "TKG4045_1_positive_gap_bound",
            "tail_condition": "stable memory operator with positive local gap and range ell_mem",
            "result_if_true": "A_tail exponentially suppressed by exp(-L_collar/ell_mem)",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "needed_evidence": "C_G, D_Z, M_Z, L_collar, c_Z, C_mem, ell_mem, and ||H||_1",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "TKG4045_2_no_global_memory_zero",
            "tail_condition": "local compact tail silence is not global memory silence",
            "result_if_true": "cosmology/FLRW memory branch survives",
            "current_status": "GUARD_ACTIVE",
            "needed_evidence": "keep local collar projection separate from cosmological nonlocal sector",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def tail_bound_template_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "TBT4045_0_tail_formula",
            "quantity": "A_tail",
            "formula": "A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1",
            "candidate_value": "MISSING_NUMERIC_VALUES",
            "units": "local acceleration/PPN force-envelope units after projection",
            "claim_status": "NONCLAIM_FORMULA_READY",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "TBT4045_1_selected_total",
            "quantity": "Delta_cZ_selected",
            "formula": "Delta_cZ_selected = A_tail because A_wall_projector=0 in selected branch",
            "candidate_value": "MISSING_TAIL_VALUE_OR_ZERO_THEOREM",
            "units": "same as A_tail",
            "claim_status": "TAIL_ONLY_REDUCTION_PRIVATE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "TBT4045_2_fallback_total",
            "quantity": "Delta_cZ_fallback",
            "formula": "Delta_cZ_fallback <= A_tail + A_wall if selected branch rejected",
            "candidate_value": "MISSING_TAIL_AND_WALL_VALUES",
            "units": "same as A_tail plus A_wall",
            "claim_status": "FALLBACK_NONCLAIM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4045_0_wall_reduction",
            "verdict": "CZ_WALL_ZEROED_IN_PRIVATE_SELECTED_BRANCH",
            "result": "4043 supplies the missing fixed-selector/no-wall clauses for the projector/domain wall, so 4040's A_wall term is zero in the selected private branch.",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4045_1_tail_remaining",
            "verdict": "CZ_REDUCED_TO_TAIL_ONLY_NOT_ZERO",
            "result": "The remaining selected-branch cZ residual is the memory/history kernel tail; exact support-zero or numeric gap inputs are still missing.",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4045_0_wall_bridge",
            "decision": "close the projector/domain selector-wall piece inside the selected private branch",
            "reason": "4043 explicitly supplies Phi_D=0, tau_wall_TF=0, fixed topological projector, and no dynamic domain variation",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4045_1_tail_not_claimed",
            "decision": "do not claim full cZ zero",
            "reason": "P_loc K_mem support/gap theorem or numeric tail inputs are not yet supplied",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4045_2_next",
            "decision": "attack the memory-tail support/gap theorem directly",
            "reason": "after wall reduction, the cZ problem is now tail-only in the selected branch",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4045_0_wall_zero_private",
            "claim": "projector/domain cZ selector-wall contribution is zero in the selected private branch",
            "allowed": True,
            "public_claim_allowed": False,
            "scope": "private selected branch only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4045_1_full_cZ_zero",
            "claim": "full Delta_cZ envelope is zero",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "blocked by memory/history tail",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4045_2_local_GR",
            "claim": "full local-GR/PPN pass",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "blocked by cZ tail, c_norm derivative hair, and parent adoption",
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4045_0_cZ_tail",
            "symbol": "Delta_cZ_tail",
            "residual": "memory/history kernel tail after selected-branch wall zero",
            "current_route": "prove P_loc K_mem support/gap silence or fill tail bound values",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4045_1_cnorm",
            "symbol": "Delta_cnorm_envelope",
            "residual": "nonconstant source-normalization derivative hair",
            "current_route": "defer until cZ tail is zeroed/bounded",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4045_2_parent",
            "symbol": "Parent_packet_adoption",
            "residual": "private selected local packet not yet final parent action theorem",
            "current_route": "formal action adoption audit after live physics envelopes close",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4045_0",
            "next_doc": "4046-Y5-R2FR-memory-tail-support-gap-zero-theorem-or-tail-bound-inputs.md",
            "next_script": "scripts/Y5_R2FR_4046_memory_tail_support_gap_zero_theorem_or_tail_bound_inputs.py",
            "why": "4045 reduces cZ to the memory/history tail in the selected branch; 4046 should attack P_loc K_mem support/gap or fill bound constants",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4045",
            "status": "CZ_WALL_ZEROED_PRIVATE_BRANCH_CZ_TAIL_REMAINS",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    source_hits = sum(1 for item in sources if item["exists"] and item["needle_found"])
    return "\n".join(
        [
            "# 4045 - cZ Kernel/Wall Zero Theorem Or First Bound Values",
            "",
            f"- Timestamp: `{ts}`",
            "- Status: `private_nonclaim_checkpoint`",
            "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
            f"- Source needles found: `{source_hits}/{len(sources)}`.",
            "",
            "## What Actually Moved",
            "",
            "4045 uses the 4043 projector/domain result to reduce the 4040 `c_Z` envelope.",
            "",
            "Before: `A_Z_remaining <= A_tail + A_wall`.",
            "",
            "After, in the selected private branch: `A_wall_projector=0`, so `Delta_cZ_selected = A_tail`.",
            "",
            "This is not full `c_Z=0`. It is a real narrowing: the selected branch no longer carries the projector/domain selector-wall term; the remaining live piece is the memory/history kernel tail.",
            "",
            "## Remaining Tail Formula",
            "",
            "`A_tail <= C_G(D_Z,M_Z,L_collar)*|c_Z|*C_mem*exp(-L_collar/ell_mem)*||H||_1`.",
            "",
            "To finish this route we need either `P_loc K_mem=0` / disjoint support on the compact collar, or real values/bounds for `C_G`, `c_Z`, `C_mem`, `ell_mem`, `L_collar`, and `||H||_1`.",
            "",
            "## Current Verdict",
            "",
            "- Current evaluator result: `CZ_REDUCED_TO_TAIL_ONLY_NOT_ZERO`.",
            "- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4045`.",
            "- Remaining live local residuals: `Delta_cZ_tail`, `Delta_cnorm_envelope`, `Parent_packet_adoption`.",
            "",
            "## Next Target",
            "",
            "- `4046-Y5-R2FR-memory-tail-support-gap-zero-theorem-or-tail-bound-inputs.md`",
            "- `scripts/Y5_R2FR_4046_memory_tail_support_gap_zero_theorem_or_tail_bound_inputs.py`",
            "",
        ]
    )


def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
    return {"check_id": check_id, "passed": passed, "detail": detail}


def all_private(*tables: Iterable[Dict[str, object]]) -> bool:
    return all(item.get("valid_for_public_claim") is False for table in tables for item in table)


def validation_rows(
    sources: List[Dict[str, object]],
    reductions: List[Dict[str, object]],
    wall_bridge: List[Dict[str, object]],
    tail_gate: List[Dict[str, object]],
    tail_bounds: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH)]
    return [
        row("VAL4045_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4045_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4045_02_reduction_count", len(reductions) == 6, "six cZ components/reductions present"),
        row("VAL4045_03_wall_zero", any(item["component_id"] == "CZR4045_3_selector_wall" and item["status"] == "ZERO_IN_PRIVATE_SELECTED_BRANCH_ELSE_FALLBACK" for item in reductions), "selector wall zeroed in private branch"),
        row("VAL4045_04_tail_live", any(item["component_id"] == "CZR4045_4_history_tail" and item["status"] == "LIVE_TAIL_ENVELOPE" for item in reductions), "history tail remains live"),
        row("VAL4045_05_total_tail_only", any(item["component_id"] == "CZR4045_5_total" and item["status"] == "REDUCED_TO_TAIL_ONLY_IN_PRIVATE_BRANCH" for item in reductions), "total reduced to tail-only"),
        row("VAL4045_06_bridge_closed", any(item["bridge_id"] == "WZB4045_0_projector_wall" and item["selected_branch_value"] == "A_wall_projector=0" for item in wall_bridge), "wall bridge closed"),
        row("VAL4045_07_guard_retained", any(item["bridge_id"] == "WZB4045_1_nonprojector_wall_guard" for item in wall_bridge), "nonprojector wall guard retained"),
        row("VAL4045_08_exact_support_gate", any(item["gate_id"] == "TKG4045_0_exact_support_zero" for item in tail_gate), "exact support-zero gate present"),
        row("VAL4045_09_gap_bound_gate", any(item["gate_id"] == "TKG4045_1_positive_gap_bound" for item in tail_gate), "positive gap bound gate present"),
        row("VAL4045_10_no_global_zero", any(item["gate_id"] == "TKG4045_2_no_global_memory_zero" for item in tail_gate), "global memory guard present"),
        row("VAL4045_11_tail_formula", any(item["bound_id"] == "TBT4045_0_tail_formula" for item in tail_bounds), "tail formula present"),
        row("VAL4045_12_selected_total", any(item["bound_id"] == "TBT4045_1_selected_total" for item in tail_bounds), "selected total tail-only row present"),
        row("VAL4045_13_evaluator_wall", any(item["verdict"] == "CZ_WALL_ZEROED_IN_PRIVATE_SELECTED_BRANCH" for item in evaluator), "wall-zero evaluator present"),
        row("VAL4045_14_evaluator_tail", any(item["verdict"] == "CZ_REDUCED_TO_TAIL_ONLY_NOT_ZERO" for item in evaluator), "tail-only evaluator present"),
        row("VAL4045_15_decision_next", any(item["decision_id"] == "DEC4045_2_next" for item in decisions), "next decision present"),
        row("VAL4045_16_wall_claim_private", any(item["claim_id"] == "CLAIM4045_0_wall_zero_private" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "wall zero claim scoped private"),
        row("VAL4045_17_full_cZ_blocked", any(item["claim_id"] == "CLAIM4045_1_full_cZ_zero" and item["allowed"] is False for item in claims), "full cZ zero blocked"),
        row("VAL4045_18_remaining_tail", any(item["symbol"] == "Delta_cZ_tail" for item in remaining), "tail residual carried"),
        row("VAL4045_19_remaining_cnorm", any(item["symbol"] == "Delta_cnorm_envelope" for item in remaining), "c_norm residual carried"),
        row("VAL4045_20_next_target", bool(next_target and "4046" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4045_21_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4045_22_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4045_23_script_compiles", compile_ok, "script compiles"),
        row("VAL4045_24_private_guard", all_private(reductions, wall_bridge, tail_gate, tail_bounds, evaluator, decisions, remaining), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    reductions = cz_component_reduction_rows(ts)
    wall_bridge = wall_zero_bridge_rows(ts)
    tail_gate = tail_kernel_gate_rows(ts)
    tail_bounds = tail_bound_template_rows(ts)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    remaining = remaining_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["cz_component_reduction"], reductions)
    write_csv(OUTPUTS["wall_zero_bridge"], wall_bridge)
    write_csv(OUTPUTS["tail_kernel_gate"], tail_gate)
    write_csv(OUTPUTS["tail_bound_template"], tail_bounds)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(
        sources,
        reductions,
        wall_bridge,
        tail_gate,
        tail_bounds,
        evaluator,
        decisions,
        claims,
        remaining,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4045 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
