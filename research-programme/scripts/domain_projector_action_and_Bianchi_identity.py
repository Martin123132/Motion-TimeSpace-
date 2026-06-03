#!/usr/bin/env python3
"""Checkpoint 207: domain-projector action and Bianchi identity audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_207_NAME = "domain-projector-action-and-Bianchi-identity"
CHECKPOINT_206_RUN = RUNS_ROOT / "20260601-000023-parent-C-screening-fixed-point-mechanism"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"
CHECKPOINT_204_RUN = RUNS_ROOT / "20260601-000021-matter-metric-action-and-ruler-transport-owner-contract"

STATUS = "domain_projector_action_formal_Bianchi_conditional_representative_missing"
CLAIM_CEILING = "domain_projector_formal_action_only_no_BAO_local_GR_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 207 domain-projector/Bianchi script"),
        (WORK_DIR / "206-parent-C-screening-fixed-point-mechanism.md", "previous C-screening mechanism checkpoint"),
        (CHECKPOINT_206_RUN / "status.json", "checkpoint 206 machine status"),
        (CHECKPOINT_206_RUN / "results" / "Bianchi_and_covariance_contract.csv", "checkpoint 206 Bianchi contract"),
        (CHECKPOINT_206_RUN / "results" / "zero_mode_domain_dilution.csv", "checkpoint 206 zero-mode dilution check"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C-silence source/bounds checkpoint"),
        (CHECKPOINT_205_RUN / "status.json", "checkpoint 205 machine status"),
        (WORK_DIR / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "matter action owner checkpoint"),
        (CHECKPOINT_204_RUN / "status.json", "checkpoint 204 machine status"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "earlier domain selector variational attempt"),
        (WORK_DIR / "68-chiD-gated-memory-conservation-contract.md", "chiD-gated memory conservation contract"),
        (WORK_DIR / "69-minimal-memory-gate-variation-attempt.md", "minimal gate variation attempt"),
        (WORK_DIR / "71-relative-boundary-current-construction-attempt.md", "relative boundary current construction"),
        (WORK_DIR / "72-relative-current-action-owner-attempt.md", "relative current action owner attempt"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "external_average_projector",
            "schematic_action": "none; set C_D=<C>_D after the fact",
            "what_it_derives": "nothing",
            "Bianchi_status": "fails",
            "verdict": "rejected_hidden_closure",
            "reason": "domain and projector are chosen outside the variational problem",
        },
        {
            "candidate": "algebraic_collective_coordinate",
            "schematic_action": "S_Pi = integral sqrt(-g) lambda_Pi (C - C_D - C_perp) + Lambda_D integral_D sqrt(h) W_D C_perp",
            "what_it_derives": "C decomposition plus zero-average residual constraint",
            "Bianchi_status": "conditional_if_D_and_WD_are_varied",
            "verdict": "formal_candidate",
            "reason": "makes the projector a constraint but still needs a domain owner",
        },
        {
            "candidate": "convected_label_domain",
            "schematic_action": "X^A fields with u^mu partial_mu X^A=0 and W_D(X^A) defining the domain measure",
            "what_it_derives": "domain labels can be carried with the matter/coherent flow",
            "Bianchi_status": "conditional",
            "verdict": "best_bulk_candidate",
            "reason": "uses action variables instead of a coordinate hand-pick",
        },
        {
            "candidate": "chiD_auxiliary_gate",
            "schematic_action": "S_aux = integral sqrt(-g)[lambda_chi(chi_D-C_coh[D]) + chi_D L_mem]",
            "what_it_derives": "lambda_chi=-L_mem and action-level gate terms",
            "Bianchi_status": "conditional_delta_g_Ccoh_missing",
            "verdict": "useful_conservation_support",
            "reason": "from checkpoints 68-69, it avoids an external switch but leaves boundary variation",
        },
        {
            "candidate": "relative_boundary_current",
            "schematic_action": "S_rel=<Lambda_rel,d_rel J_rel> plus boundary polarization",
            "what_it_derives": "d_rel J_rel=0 can be imposed variationally",
            "Bianchi_status": "conditional_representative_missing",
            "verdict": "boundary_support_not_selector",
            "reason": "from checkpoints 71-72, closure yes, physical representative no",
        },
        {
            "candidate": "full_projector_plus_boundary_action",
            "schematic_action": "S_parent includes C_D,C_perp,X^A,W_D,lambda_Pi,chi_D,J_rel and varies all of them",
            "what_it_derives": "formal projector and total Noether/Bianchi closure on shell",
            "Bianchi_status": "formal_pass_if_all_fields_varied",
            "verdict": "best_current_contract_not_promotion",
            "reason": "still lacks zero-knob representative/domain scale and transition law",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta_lambda_Pi",
            "equation": "C - C_D - C_perp = 0",
            "meaning": "decomposes C into coherent zero-mode plus residual",
            "status": "formal_pass",
            "remaining_gap": "does not choose the physical domain",
        },
        {
            "variation": "delta_Lambda_D",
            "equation": "integral_D sqrt(h) W_D C_perp = 0",
            "meaning": "residual has zero domain average",
            "status": "formal_pass",
            "remaining_gap": "requires W_D/domain measure to be action-owned",
        },
        {
            "variation": "delta_C_perp",
            "equation": "lambda_Pi + Lambda_D W_D + screened residual operator terms = 0",
            "meaning": "nonzero modes are constrained/suppressed rather than freely trace-sourced",
            "status": "conditional_pass",
            "remaining_gap": "operator and weights must be parent-derived",
        },
        {
            "variation": "delta_C_D",
            "equation": "E_CD(C_D,<T>_D,...) - integral sqrt(-g) lambda_Pi = 0",
            "meaning": "coherent mode gets its own zero-mode equation",
            "status": "formal_pass",
            "remaining_gap": "endpoint amplitude and late transition law are not derived",
        },
        {
            "variation": "delta_XA_or_domain",
            "equation": "bulk advection terms + boundary terms = 0",
            "meaning": "domain motion/boundary exchange must be solved, not frozen",
            "status": "fail_open",
            "remaining_gap": "physical local-zero/FLRW-nonzero representative not selected",
        },
        {
            "variation": "delta_metric",
            "equation": "T_Pi + T_chi + T_rel + T_boundary enter total stress",
            "meaning": "projector stress is conservation bookkeeping, not optional",
            "status": "conditional_Bianchi_support",
            "remaining_gap": "explicit stress tensor not constructed",
        },
    ]


def noether_bianchi_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "A diffeomorphism-invariant total action gives a Noether identity.",
            "equation": "delta_xi S_total = 0",
            "status": "standard_identity",
            "failure_if_omitted": "no conservation proof exists",
        },
        {
            "step": 2,
            "statement": "The identity includes all projector/domain fields.",
            "equation": "nabla_mu E_g^{mu nu} = sum_A E_A L_xi Phi_A",
            "status": "formal_pass_if_all_Phi_A_varied",
            "failure_if_omitted": "frozen domain/projector acts like an external force",
        },
        {
            "step": 3,
            "statement": "On shell, all Euler-Lagrange terms vanish.",
            "equation": "E_A=0 -> nabla_mu T_total^{mu nu}=0",
            "status": "conditional_Bianchi_pass",
            "failure_if_omitted": "Bianchi accounting fails",
        },
        {
            "step": 4,
            "statement": "A gated source inserted directly into field equations is not conserved.",
            "equation": "nabla_mu(chi_D T_mem^{mu nu}) = T_mem^{mu nu} nabla_mu chi_D + ...",
            "status": "rejected_shortcut",
            "failure_if_omitted": "the old external switch comes back",
        },
        {
            "step": 5,
            "statement": "Auxiliary/projector stress must carry exchange terms.",
            "equation": "T_total = T_m + T_C + T_Pi + T_D + T_rel + T_boundary",
            "status": "required_contract",
            "failure_if_omitted": "local silence is fake because exchange is hidden",
        },
        {
            "step": 6,
            "statement": "Formal Bianchi closure is not physical representative selection.",
            "equation": "nabla_mu T_total^{mu nu}=0 does not imply Pi_D is the observed domain",
            "status": "core_blocker",
            "failure_if_omitted": "mathematical closure would be overclaimed as a derivation",
        },
    ]


def representative_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "local stationary class trivial",
            "target": "C_D constant, C_perp screened, J_rel exact/trivial",
            "current_status": "possible_conditional",
            "missing_owner": "action must force this without importing known GR-bound-system facts",
            "promotion_effect": "P08 remains open",
        },
        {
            "requirement": "FLRW coherent class nontrivial",
            "target": "C_D carries endpoint memory and coherent volume expansion",
            "current_status": "possible_contract",
            "missing_owner": "amplitude/transition law and boundary representative",
            "promotion_effect": "P10 and CMB bridge remain theorem debts",
        },
        {
            "requirement": "BAO domain late common-mode",
            "target": "domain average smooth enough for |Delta C| and |dot_C/H| bounds",
            "current_status": "bounded_not_derived",
            "missing_owner": "L_D/coherence rule before scoring",
            "promotion_effect": "BAO no promotion yet",
        },
        {
            "requirement": "no wall/surface PPN stress",
            "target": "relative current is topological/bookkeeping, not physical wall energy",
            "current_status": "conditional",
            "missing_owner": "metric variation of boundary terms",
            "promotion_effect": "local branch unsafe if surface stress appears",
        },
        {
            "requirement": "no data-tuned domain scale",
            "target": "L_D = F[L_cg, chi_D, Q, J_rel] before empirical scoring",
            "current_status": "missing",
            "missing_owner": "zero-knob domain selection equation",
            "promotion_effect": "otherwise the projector is a rescue knob",
        },
    ]


def stress_accounting_rows() -> list[dict[str, Any]]:
    return [
        {
            "stress_piece": "T_C",
            "origin": "C-sector kinetic/potential/zero-mode dynamics",
            "needed_for": "endpoint memory and transition law",
            "danger": "ordinary local scalar response",
            "status": "not_full_parent_derived",
        },
        {
            "stress_piece": "T_Pi",
            "origin": "lambda_Pi and zero-average residual constraint",
            "needed_for": "projector Bianchi bookkeeping",
            "danger": "hidden external force if omitted",
            "status": "formal_contract",
        },
        {
            "stress_piece": "T_D",
            "origin": "domain labels/window/measure variation",
            "needed_for": "covariant domain motion",
            "danger": "data-tuned or frozen domain",
            "status": "missing_physical_equation",
        },
        {
            "stress_piece": "T_chi",
            "origin": "chi_D auxiliary gate",
            "needed_for": "memory gate conservation",
            "danger": "delta_g C_coh and boundary terms unresolved",
            "status": "known_from_68_69_as_open",
        },
        {
            "stress_piece": "T_rel_boundary",
            "origin": "relative current/boundary exchange",
            "needed_for": "transition boundary without wall stress",
            "danger": "physical PPN wall stress or arbitrary counterterm",
            "status": "formal_support_selection_missing",
        },
        {
            "stress_piece": "T_matter",
            "origin": "universal matter metric",
            "needed_for": "ruler/clock common-mode coupling",
            "danger": "trace source for C",
            "status": "owned_conditionally_by_204",
        },
    ]


def forbidden_shortcut_rows() -> list[dict[str, Any]]:
    return [
        {
            "shortcut": "insert Pi_D by hand after solving equations",
            "why_forbidden": "external projector violates the variational/Bianchi discipline",
            "allowed_replacement": "derive Pi_D from auxiliary/domain fields in S_parent",
        },
        {
            "shortcut": "freeze the domain boundary during metric variation",
            "why_forbidden": "hides boundary exchange stress",
            "allowed_replacement": "include domain labels/window and relative current in the variation",
        },
        {
            "shortcut": "claim Noether identity proves the physical representative",
            "why_forbidden": "conservation does not select local-zero versus FLRW-nonzero classes",
            "allowed_replacement": "add a zero-knob representative-selection equation",
        },
        {
            "shortcut": "use BAO success to choose L_D",
            "why_forbidden": "domain scale becomes an empirical rescue knob",
            "allowed_replacement": "derive L_D from L_cg/chi_D/Q/J_rel before scoring",
        },
        {
            "shortcut": "ignore T_Pi or T_boundary because the field is auxiliary",
            "why_forbidden": "auxiliary stress is exactly the conservation bookkeeping",
            "allowed_replacement": "track all metric variations, even multiplier terms",
        },
    ]


def promotion_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal action/Bianchi audit",
        },
        {
            "gate": "external projector rejected",
            "status": "pass",
            "evidence": "external average has no action and fails Bianchi discipline",
            "claim_allowed": "negative route",
        },
        {
            "gate": "formal projector action written",
            "status": "conditional_pass",
            "evidence": "C=C_D+C_perp and zero-average residual can be constrained variationally",
            "claim_allowed": "formal candidate",
        },
        {
            "gate": "Noether/Bianchi accounting closed",
            "status": "conditional_pass",
            "evidence": "only if all projector/domain/boundary fields are varied and stresses included",
            "claim_allowed": "formal conservation contract",
        },
        {
            "gate": "physical representative selected",
            "status": "fail",
            "evidence": "local trivial / FLRW nontrivial / BAO domain representative not derived",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "domain scale not tuned to data",
            "status": "fail",
            "evidence": "L_D = F[L_cg, chi_D, Q, J_rel] still missing",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "local GR or BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A domain-projector action can be written formally: decompose C into C_D plus C_perp, impose zero-average residual constraints, and include all projector/domain/boundary stresses. This gives conditional Noether/Bianchi closure, but it still does not select the physical domain representative or non-tuned domain scale.",
            "main_gain": "Pi_D is upgraded from a hand average to a formal variational constraint candidate",
            "Bianchi_result": "conditional pass only if C_D, C_perp, domain labels, chi_D, and J_rel are all varied",
            "main_blocker": "physical representative and domain scale selection remain missing",
            "next_target": "208-domain-representative-selection-law.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_207_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    action_rows = action_candidate_rows()
    variation_rows = variation_chain_rows()
    bianchi_rows = noether_bianchi_rows()
    representative_rows = representative_selection_rows()
    stress_rows = stress_accounting_rows()
    forbidden_rows = forbidden_shortcut_rows()
    gates = promotion_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "action_candidate_ledger.csv": (
            action_rows,
            ["candidate", "schematic_action", "what_it_derives", "Bianchi_status", "verdict", "reason"],
        ),
        "variation_chain.csv": (
            variation_rows,
            ["variation", "equation", "meaning", "status", "remaining_gap"],
        ),
        "Noether_Bianchi_chain.csv": (
            bianchi_rows,
            ["step", "statement", "equation", "status", "failure_if_omitted"],
        ),
        "representative_selection_obligations.csv": (
            representative_rows,
            ["requirement", "target", "current_status", "missing_owner", "promotion_effect"],
        ),
        "stress_accounting_ledger.csv": (
            stress_rows,
            ["stress_piece", "origin", "needed_for", "danger", "status"],
        ),
        "forbidden_shortcuts.csv": (
            forbidden_rows,
            ["shortcut", "why_forbidden", "allowed_replacement"],
        ),
        "promotion_gates.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "Bianchi_result",
                "main_blocker",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "external_projector_rejected": True,
        "formal_projector_action_candidate_written": True,
        "conditional_Bianchi_closure_written": True,
        "physical_representative_selected": False,
        "domain_scale_parent_derived": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
