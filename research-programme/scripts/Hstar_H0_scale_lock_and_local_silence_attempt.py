from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Hstar-H0-scale-lock-and-local-silence-attempt"
STATUS = "Hstar_equals_H0_not_parent_derived_scale_lock_reduced_to_boundary_condition_local_silence_conditional"
CLAIM_CEILING = "Hstar_scale_lock_not_derived_C3b_still_open_local_silence_conditional"
B_MEM_FIXED = 2.0 / 27.0
SOURCE_258 = ROOT / "runs" / "20260601-000076-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation" / "results"
SOURCE_260 = ROOT / "runs" / "20260601-000078-C3-unit-stress-normalization-parent-action-attempt" / "results"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "179-local-GR-PPN-silence-contract.md", "local PPN effective silence contract"),
        (ROOT / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint/domain local silence gate"),
        (ROOT / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C-gradient and trace-source hazard"),
        (ROOT / "241-C-silence-screening-or-parent-selection-theorem.md", "unscreened conformal C no-go"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "C3 split and Hstar target"),
        (SOURCE_258 / "fixed_vs_kappa_penalty.csv", "258 empirical fixed-vs-kappa anchor"),
        (SOURCE_260 / "C3_theorem_split.csv", "260 C3 split"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def empirical_scale_rows() -> list[dict[str, Any]]:
    penalty = read_csv(SOURCE_258 / "fixed_vs_kappa_penalty.csv")
    if not penalty:
        return [{"quantity": "258_penalty", "value": "missing", "interpretation": "no empirical anchor imported"}]
    row = penalty[0]
    kappa_best = float(row["kappa_best_kappa_mem"])
    h_ratio = math.sqrt(kappa_best)
    return [
        {
            "quantity": "fixed_q",
            "value": B_MEM_FIXED,
            "formula": "q=2/27",
            "interpretation": "strict lead rank-fraction closure target",
        },
        {
            "quantity": "kappa_best",
            "value": kappa_best,
            "formula": "B_free/B_fixed",
            "interpretation": "best free amplitude from 258; not promoted by AIC/BIC",
        },
        {
            "quantity": "Hstar_over_H0_if_free_fit_used",
            "value": h_ratio,
            "formula": "sqrt(kappa_best)",
            "interpretation": "free fit would imply Hstar only 0.3094 percent above H0, a clue not a theorem",
        },
        {
            "quantity": "Bmem_geometric_scale_identity",
            "value": "B_mem=q*(Hstar/H0)^2",
            "formula": "rho_mem=3 M_Pl^2 Hstar^2 q F(N), rho_c0=3 M_Pl^2 H0^2",
            "interpretation": "unit B_mem requires Hstar=H0 if q=2/27",
        },
    ]


def scale_lock_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "present_Hamiltonian_constraint",
            "candidate_derivation": "Use E(0)=1 to set Hstar=H0",
            "result": "fails",
            "reason": "F(0)=0, so the memory term vanishes at the present boundary and E(0)=1 is insensitive to Hstar",
            "status": "no_go",
        },
        {
            "route": "critical_density_normalization",
            "candidate_derivation": "Define A_mem=rho_c0",
            "result": "tautological",
            "reason": "this writes the desired unit normalization into the action rather than deriving it",
            "status": "closure_not_theorem",
        },
        {
            "route": "geometric_EH_Hstar_term",
            "candidate_derivation": "Add -6 Hstar^2 qF to the EH-like action",
            "result": "partial",
            "reason": "derives B_mem=q(Hstar/H0)^2 but leaves Hstar as a new scale",
            "status": "best_formal_route_but_scale_unowned",
        },
        {
            "route": "boundary_York_time_or_domain_age",
            "candidate_derivation": "Set Hstar by the current domain boundary extrinsic curvature",
            "result": "conditional",
            "reason": "would make Hstar=H_D(now), but H_D(now)=H0 is boundary data unless parent boundary equations select it",
            "status": "promising_theorem_target_not_derived",
        },
        {
            "route": "Noether_charge_normalization",
            "candidate_derivation": "Fix Hstar through a conserved dilation/time-translation charge",
            "result": "open",
            "reason": "no current charge equation ties the memory scale to the observed present expansion",
            "status": "needs_parent_symmetry",
        },
        {
            "route": "four_form_flux_quantization",
            "candidate_derivation": "Quantize the vacuum/memory scale through flux units",
            "result": "insufficient",
            "reason": "flux can discretize a scale but still needs a reason to choose the H0 flux sector",
            "status": "not_currently_derived",
        },
        {
            "route": "global_sequestering_constraint",
            "candidate_derivation": "Use a global constraint to tie vacuum response to spacetime average expansion",
            "result": "possible_but_unbuilt",
            "reason": "would be a new global parent mechanism and must preserve local conservation and no fifth force",
            "status": "future_route",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "F_zero_present_no_go",
            "proof": "The lead activation has F(0)=0, so the present Friedmann normalization E(0)=1 contains no memory-amplitude term.",
            "consequence": "the present Hamiltonian constraint cannot fix Hstar or kappa_mem",
        },
        {
            "lemma": "Hstar_rescaling_no_go",
            "proof": "Hstar -> lambda Hstar changes B_mem by lambda^2 while preserving the stress-form variation.",
            "consequence": "metric variation plus Bianchi consistency cannot select lambda=1",
        },
        {
            "lemma": "H0_solution_data_no_go",
            "proof": "H0 is an integration/boundary datum of the cosmological solution unless the parent theory adds a scale-selection equation.",
            "consequence": "Hstar=H0 is a boundary condition, not a theorem, without that extra equation",
        },
        {
            "lemma": "local_trace_revival_no_go",
            "proof": "If the scale-lock field is an ordinary local conformal scalar coupled to matter, local T_hat sources it.",
            "consequence": "any scale-lock mechanism must be a global/domain zero-mode, screened mode, or strict local metric selection",
        },
    ]


def local_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "homogeneous_zero_mode_only",
            "requirement": "Hstar and F(N) are global/domain FLRW data, not local matter-responsive fields",
            "status": "required",
            "local_effect": "only cosmological tidal/common-mode curvature remains",
        },
        {
            "condition": "no_local_trace_coupling",
            "requirement": "delta S_matter/dHstar = 0 and no ordinary local C scalar response to T_hat",
            "status": "required",
            "local_effect": "avoids WEP/clock/fifth-force source",
        },
        {
            "condition": "topological_projector_local_limit",
            "requirement": "local exterior still uses metric-independent P_D with zero bulk projector stress",
            "status": "conditional_from_251_252",
            "local_effect": "keeps N5 route alive",
        },
        {
            "condition": "volume_stress_FLRW_only",
            "requirement": "the metric-volume memory stress contributes only to FLRW/common-mode sector or is locally absorbed into tiny background curvature",
            "status": "open",
            "local_effect": "needed to prevent cosmology stress from spoiling metric-only local EH",
        },
        {
            "condition": "late_domain_saturation",
            "requirement": "dot_C/H and spatial gradients satisfy BAO/local silence bounds in late readout domains",
            "status": "conditional_from_195_205_241",
            "local_effect": "prevents endpoint clock map from leaking into local PPN",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "H1_geometric_identity",
            "question": "Does a geometric scale term produce B_mem=q(Hstar/H0)^2?",
            "result": "pass",
            "evidence": "rho_mem=3M_Pl^2 Hstar^2 qF and rho_c0=3M_Pl^2 H0^2",
            "claim_effect": "useful identity, not unit normalization",
        },
        {
            "gate": "H2_Hstar_equals_H0_theorem",
            "question": "Is Hstar=H0 derived by parent equations?",
            "result": "fail",
            "evidence": "present constraint is insensitive because F(0)=0; all routes leave scale/boundary data",
            "claim_effect": "C3b remains open",
        },
        {
            "gate": "H3_boundary_condition_closure",
            "question": "Can Hstar=H0 be used as a disciplined closure condition?",
            "result": "pass_as_closure",
            "evidence": "it is exact, minimal, and empirically parsimonious after 258",
            "claim_effect": "allowed only as closure theorem-target",
        },
        {
            "gate": "H4_local_silence_compatibility",
            "question": "Can the scale-lock route avoid local trace/fifth-force problems?",
            "result": "conditional",
            "evidence": "requires global/domain zero-mode and strict local metric selection; ordinary local conformal scalar rejected",
            "claim_effect": "local GR not promoted",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "Hstar=H0 is parent-derived",
            "status": "forbidden",
            "reason": "no boundary/Noether/Hamiltonian equation currently selects H0",
        },
        {
            "claim": "Hstar=H0 is a clean closure theorem-target",
            "status": "allowed",
            "reason": "it exactly supplies unit kappa without adding a free fit parameter",
        },
        {
            "claim": "present Friedmann normalization fixes memory amplitude",
            "status": "forbidden",
            "reason": "F(0)=0 makes the memory amplitude absent at the present boundary",
        },
        {
            "claim": "scale-lock is locally safe if implemented as a global/domain zero-mode",
            "status": "conditional",
            "reason": "ordinary local trace-coupled scalar remains rejected",
        },
        {
            "claim": "fixed 2/27 remains the lead branch",
            "status": "allowed",
            "reason": "258 favors parsimony and 261 finds no derived reason to fit kappa",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "meaning": (
                "The geometric identity B_mem=q(Hstar/H0)^2 is clean, but Hstar=H0 is not derived. "
                "The present Friedmann constraint cannot fix it because F(0)=0, and all acceptable scale-lock routes "
                "leave a boundary/Noether/global constraint still to be built. Local silence is compatible only if the scale is "
                "a global/domain zero-mode or screened quantity, not an ordinary local trace-coupled scalar."
            ),
            "next_target": "either_build_boundary_Noether_scale_lock_or_keep_Hstar_equals_H0_as_closure_and_move_to_rank_27_rank_2_or_CMB_bridge",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "geometric_scale_identity.csv": (
            empirical_scale_rows(),
            ["quantity", "value", "formula", "interpretation"],
        ),
        "Hstar_scale_lock_routes.csv": (
            scale_lock_route_rows(),
            ["route", "candidate_derivation", "result", "reason", "status"],
        ),
        "Hstar_no_go_lemmas.csv": (
            no_go_rows(),
            ["lemma", "proof", "consequence"],
        ),
        "local_silence_compatibility.csv": (
            local_silence_rows(),
            ["condition", "requirement", "status", "local_effect"],
        ),
        "scale_lock_gate_results.csv": (
            gate_rows(),
            ["gate", "question", "result", "evidence", "claim_effect"],
        ),
        "claim_policy_after_261.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "Hstar_equals_H0_derived": False,
        "geometric_identity_pass": True,
        "local_silence_compatibility": "conditional_global_domain_zero_mode_only",
        "B_mem_fixed": B_MEM_FIXED,
        "next_target": "either_build_boundary_Noether_scale_lock_or_keep_Hstar_equals_H0_as_closure_and_move_to_rank_27_rank_2_or_CMB_bridge",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Attempt Hstar=H0 scale-lock and local-silence compatibility derivation.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
