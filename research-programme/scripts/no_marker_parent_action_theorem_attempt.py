from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "no-marker-parent-action-theorem-attempt"
CHECKPOINT_DOC = "413-no-marker-parent-action-theorem-attempt.md"
STATUS = "no_marker_parent_action_theorem_attempt_written_fixed_spurion_excluded_but_material_marker_extension_still_legal_no_R0_promotion_no_local_GR_pass"
CLAIM_CEILING = "no_marker_parent_action_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "414-local-quotient-invariant-algebra-triviality-gate.md"


SOURCE_DOCS = [
    {
        "path": "337-exact-parent-pullback-selection-rule-gate.md",
        "role": "exact readout/pullback theorem template",
    },
    {
        "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "fixed active spurion is not a function on the quotient",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "representative-invariance and boundary/domain class caveat",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "selector pullback and no-go branch audit",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive quotient/readout sketch requiring no-marker theorem",
    },
    {
        "path": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "quotient matter functor chain and marker counterexample",
    },
    {
        "path": "412-v4-source-charge-channel-map-review.md",
        "role": "recent local-bound fairness discipline",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
    {
        "path": "runs/20260602-052500-primitive-relational-quotient-action-sketch/results/no_cheat_constraints.csv",
        "role": "primitive no-cheat constraints",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/counterexample_functors.csv",
        "role": "marker-extended quotient counterexample",
    },
    {
        "path": "runs/20260602-062500-v4-source-charge-channel-map-review/results/channel_count_policy.csv",
        "role": "latest anti-cheat channel-count policy",
    },
]


MARKER_DEFINITIONS = [
    {
        "marker_type": "fixed_active_spurion",
        "symbolic_form": "P_active fixed on labelled components",
        "parent_status": "excluded_if_parent_space_is_strict_quotient",
        "reason": "fixed mask is not constant on the S_n/G_rel orbit",
        "local_risk": "low once strict quotient is proven",
    },
    {
        "marker_type": "co_moving_material_marker",
        "symbolic_form": "m transforms with x, then Q_tilde=(x,m)/G_rel",
        "parent_status": "not_excluded_by_quotient_invariance",
        "reason": "marker descends to the extended quotient as legal data",
        "local_risk": "high unless no-extension theorem exists",
    },
    {
        "marker_type": "quotient_invariant_class_scalar",
        "symbolic_form": "I_Q, Q_rel, C_D, topological/domain class",
        "parent_status": "not_excluded",
        "reason": "quotient-invariant can still be locally physical",
        "local_risk": "clock/gamma/fifth-force/domain pressure",
    },
    {
        "marker_type": "species_constant_marker",
        "symbolic_form": "theta_A(m) or q_A(I_Q)",
        "parent_status": "not_excluded",
        "reason": "constants can carry marker dependence unless universality is derived",
        "local_risk": "WEP/source-charge/clock pressure",
    },
    {
        "marker_type": "post_readout_EFT_marker",
        "symbolic_form": "S_reduced[P_active,e_obs]",
        "parent_status": "excluded_only_if_readout_after_variation_is_enforced",
        "reason": "projected terms can be written after readout unless forbidden",
        "local_risk": "closure-zero can be mistaken for theorem-zero",
    },
]


THEOREM_CHAIN = [
    {
        "step": 1,
        "claim": "Strict quotient removes fixed labels.",
        "identity": "P_active(x) != P_active(g.x) while quotient observables are orbit-constant",
        "status": "partial_theorem_from_341_if_parent_quotient_is_proven",
    },
    {
        "step": 2,
        "claim": "Parent action cannot contain non-orbit functions.",
        "identity": "S_parent[Q] cannot depend on fixed labelled mask",
        "status": "conditional_pass_for_fixed_spurion",
    },
    {
        "step": 3,
        "claim": "Material marker extension is also forbidden.",
        "identity": "Q_tilde=(x,m)/G_rel is inadmissible",
        "status": "not_derived",
    },
    {
        "step": 4,
        "claim": "Local quotient invariant algebra has no extra generators.",
        "identity": "I_loc(Q) / I(e_obs) = constants",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "Matter constants are marker independent.",
        "identity": "partial_m theta_A = 0 and partial_IQ theta_A = 0",
        "status": "not_derived",
    },
    {
        "step": 6,
        "claim": "Readout is after variation only.",
        "identity": "vary S_parent first; no independent S_reduced[P_active,e_obs]",
        "status": "conditional_template",
    },
    {
        "step": 7,
        "claim": "No material marker contributes to local matter pullback.",
        "identity": "delta S_matter/delta m = 0 and delta S_matter/delta Z_I|e_obs=0",
        "status": "conditional_target_not_full_theorem",
    },
]


ADMISSIBILITY_TESTS = [
    {
        "test": "fixed_mask_orbit_test",
        "input": "labelled active/inactive swap",
        "pass_condition": "observable changes under relabeling, so it is not a quotient function",
        "result": "conditional_pass",
        "meaning": "fixed P_active is excluded by strict quotient parent space",
    },
    {
        "test": "co_moving_marker_test",
        "input": "marker transforms with the state",
        "pass_condition": "extension must be forbidden by parent configuration, not merely by quotient covariance",
        "result": "fail_open",
        "meaning": "co-moving material marker remains legal unless an extra no-extension theorem exists",
    },
    {
        "test": "invariant_scalar_test",
        "input": "I_Q or domain/topological class",
        "pass_condition": "local invariant algebra has no nonconstant marker scalar beyond observed geometry",
        "result": "fail_open",
        "meaning": "quotient-invariant class scalars remain possible local couplings",
    },
    {
        "test": "constant_sector_test",
        "input": "theta_A(m), q_A(I_Q), mass_A(I_Q)",
        "pass_condition": "species constants are independent of marker/class data",
        "result": "fail_open",
        "meaning": "source/clock rows cannot be promoted",
    },
    {
        "test": "readout_EFT_test",
        "input": "S_reduced[P_active,e_obs]",
        "pass_condition": "readout is defined only after parent variation",
        "result": "conditional_template",
        "meaning": "must remain a no-cheat rule until parent variation is formalized",
    },
]


COUNTEREXAMPLE_MARKERS = [
    {
        "counterexample": "extended_quotient_marker",
        "construction": "Q_tilde=(x,m)/G_rel with S_matter[Psi,e_obs,m]",
        "why_not_blocked": "m is not a fixed label; it is part of the quotient object",
        "required_blocker": "parent configuration-space minimality/no-extension theorem",
    },
    {
        "counterexample": "domain_class_marker",
        "construction": "S_matter[Psi,exp(F(Q_rel))e_obs]",
        "why_not_blocked": "Q_rel is quotient-invariant and may be allowed for cosmology/domain sectors",
        "required_blocker": "local invariant algebra triviality or local class silence theorem",
    },
    {
        "counterexample": "species_charge_marker",
        "construction": "theta_A=theta_A(m) or q_A=q_A(I_Q)",
        "why_not_blocked": "matter constants can be marker functors unless universality is derived",
        "required_blocker": "constant-sector universality theorem",
    },
    {
        "counterexample": "orientation_or_time_arrow_marker",
        "construction": "m is a covariantly selected orientation/time-arrow scalar",
        "why_not_blocked": "natural structure can be quotient-invariant but still physical",
        "required_blocker": "prove it is constant, pure gauge, or already contained in e_obs",
    },
    {
        "counterexample": "post_readout_projector_marker",
        "construction": "effective projected action varied after choosing P_read/P_active",
        "why_not_blocked": "projection can be covariant at the reduced level",
        "required_blocker": "exact parent-readout-after-variation theorem",
    },
]


ROW_TRANSITION_ATTEMPT = [
    {
        "row_id": "R0_identity_coframe_direct",
        "attempted_upgrade": "closure_zero -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "closure_zero",
        "reason": "fixed spurion is excluded conditionally, but material marker and invariant class couplings remain legal",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "species constants/charges can depend on marker or class data",
    },
    {
        "row_id": "R2_clock_redshift",
        "attempted_upgrade": "retained_budget -> metric_clock_only",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "marker-dependent constants or class metrics can affect clock sector",
    },
    {
        "row_id": "R5_alpha1",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "marker leakage/preferred-frame route remains a retained channel",
    },
    {
        "row_id": "R8_xi",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "domain/preferred-location class markers remain possible",
    },
    {
        "row_id": "R10_fifth_force",
        "attempted_upgrade": "unscored_parameterized -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "unscored_parameterized",
        "reason": "marker scalar can mediate fifth-force curve unless range/charge/screening theorem is supplied",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "attempted_upgrade": "retained_residual -> EH_selected",
        "result": "not_upgraded",
        "new_state": "retained_residual",
        "reason": "no-marker theorem alone would not select EH operator ledger",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The no-marker route partially works: if the parent configuration space is a strict quotient, then a fixed active spurion is not an admissible parent-action argument. That is a real anti-cheat theorem shape. But it does not yet prove the full no-marker condition needed for local GR, because a co-moving material marker, quotient-invariant domain/class scalar, marker-dependent species constant, or post-readout EFT marker can still be added consistently unless the parent action supplies a stronger minimality/no-extension theorem. Therefore R0 remains closure_zero, marker-related rows remain retained, and the next derivation target is the local quotient-invariant algebra: prove that the local vacuum quotient has no nonconstant marker generators beyond observed geometry, or keep the no-marker step as explicit closure.",
        "fixed_spurion_excluded_conditionally": True,
        "material_marker_extension_blocked": False,
        "local_invariant_algebra_triviality_derived": False,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "try to prove local invariant algebra triviality for the quotient parent space",
        "pass_condition": "local markers reduce to constants/observed geometry or remain explicit closure variables",
    },
    {
        "priority": 2,
        "target": "414-local-bounds-data-intake-first-pass.md",
        "task": "start filling the real-data local-bound interface from verified sources",
        "pass_condition": "external local-bound rows evaluate with references and no claim leaks",
    },
    {
        "priority": 3,
        "target": "415-direct-WEP-vs-source-normalization-evaluator-update.py",
        "task": "update evaluator outputs to report direct-WEP and full-R1 guardrails side by side",
        "pass_condition": "R1 split is visible without changing runner-v4 claim semantics",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def row_transition_rows() -> list[dict[str, Any]]:
    matrix_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    rows: list[dict[str, Any]] = []
    for transition in ROW_TRANSITION_ATTEMPT:
        matrix_row = matrix_by_id.get(transition["row_id"], {})
        rows.append(
            {
                "row_id": transition["row_id"],
                "previous_state": matrix_row.get("runner_v4_state", "missing"),
                "previous_zero_kind": matrix_row.get("zero_kind", "missing"),
                "attempted_upgrade": transition["attempted_upgrade"],
                "result": transition["result"],
                "new_state": transition["new_state"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
                "reason": transition["reason"],
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_zero_upgrades = [row for row in transition_rows if row["new_state"] == "theorem_zero"]
    claim_rows = [row for row in transition_rows if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "marker_definitions_written",
            "status": "pass",
            "evidence": f"{len(MARKER_DEFINITIONS)} marker types classified",
        },
        {
            "gate": "fixed_active_spurion_excluded",
            "status": "conditional_pass",
            "evidence": "fixed P_active is not a strict quotient function if parent quotient is proven",
        },
        {
            "gate": "material_marker_extension_blocked",
            "status": "fail",
            "evidence": "co-moving marker extension Q_tilde=(x,m)/G_rel remains legal",
        },
        {
            "gate": "local_invariant_algebra_triviality_derived",
            "status": "fail",
            "evidence": "I_loc(Q)/I(e_obs)=constants is the next theorem target, not proven here",
        },
        {
            "gate": "constant_sector_marker_independence_derived",
            "status": "fail",
            "evidence": "theta_A(m) and theta_A(I_Q) remain counterexamples",
        },
        {
            "gate": "readout_after_variation_derived",
            "status": "fail",
            "evidence": "post-readout EFT marker remains a no-cheat rule, not a theorem",
        },
        {
            "gate": "runner_rows_promoted_to_theorem_zero",
            "status": "fail",
            "evidence": f"{len(theorem_zero_upgrades)} theorem-zero upgrades",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "no-marker attempt only; no EH/Newton/PPN/local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    transition_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    marker_table_rows = [
        {
            "marker_type": row["marker_type"],
            "parent_status": row["parent_status"],
            "local_risk": row["local_risk"],
        }
        for row in MARKER_DEFINITIONS
    ]
    theorem_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in THEOREM_CHAIN
    ]
    test_table_rows = [
        {
            "test": row["test"],
            "result": row["result"],
            "meaning": row["meaning"],
        }
        for row in ADMISSIBILITY_TESTS
    ]
    counterexample_table_rows = [
        {
            "counterexample": row["counterexample"],
            "required_blocker": row["required_blocker"],
        }
        for row in COUNTEREXAMPLE_MARKERS
    ]
    transition_table_rows = [
        {
            "row_id": row["row_id"],
            "previous_state": row["previous_state"],
            "new_state": row["new_state"],
            "result": row["result"],
        }
        for row in transition_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 413 - No-Marker Parent-Action Theorem Attempt

Private no-marker/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 410 identified `marker_extended_quotient` as the cleanest counterexample to the quotient-matter route. This checkpoint asks whether the parent action can actually forbid material markers, instead of merely forbidding a fixed active mask by quotient language.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/no_marker_parent_action_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Marker Classification

{markdown_table(marker_table_rows, ["marker_type", "parent_status", "local_risk"])}

## 4. Theorem Chain

{markdown_table(theorem_table_rows, ["step", "claim", "status"])}

## 5. Admissibility Tests

{markdown_table(test_table_rows, ["test", "result", "meaning"])}

## 6. Counterexample Markers

{markdown_table(counterexample_table_rows, ["counterexample", "required_blocker"])}

## 7. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: we got a partial theorem, not the knockout. Fixed active labels are in trouble under strict quotient geometry; material markers are not. To get local GR by derivation, the next target has to be the local invariant algebra: prove there are no extra local marker generators, or keep the no-marker assumption explicitly labelled as closure.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    transition_rows = row_transition_rows()
    gate_result_rows = gate_rows(source_rows, transition_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "marker_definitions.csv", MARKER_DEFINITIONS)
    write_csv(results_dir / "no_marker_theorem_chain.csv", THEOREM_CHAIN)
    write_csv(results_dir / "admissibility_tests.csv", ADMISSIBILITY_TESTS)
    write_csv(results_dir / "counterexample_markers.csv", COUNTEREXAMPLE_MARKERS)
    write_csv(results_dir / "row_transition_attempt.csv", transition_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "marker_types": len(MARKER_DEFINITIONS),
        "fixed_spurion_excluded_conditionally": True,
        "material_marker_extension_blocked": False,
        "local_invariant_algebra_triviality_derived": False,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, transition_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 413 no-marker parent-action theorem attempt artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
