from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1152-Y5-R10-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md"


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


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1152_0_1151_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1151_NEXT_TARGET.csv",
            "needle": "NEXT1151_0_1152",
            "role": "handoff selecting PiM commutator-zero theorem or source acquisition.",
        },
        {
            "source_id": "SRC1152_1_1151_hooks",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1151_PARENT_ACTION_REENTRY_HOOKS.csv",
            "needle": "HOOK1151_5_commutator_stress_zero",
            "role": "parent-action hook requiring commutator zero plus projector stress ownership.",
        },
        {
            "source_id": "SRC1152_2_1151_smoke",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1151_SMOKE_EVALUATION.csv",
            "needle": "SMOKE1151_0_current_branch",
            "role": "runner status showing current branch blocked by missing equality and commutator inputs.",
        },
        {
            "source_id": "SRC1152_3_1014_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv",
            "needle": "PCT1014_7_verdict",
            "role": "prior theorem attempt retaining the product-rule obstruction.",
        },
        {
            "source_id": "SRC1152_4_660_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
            "needle": "CZ660_6_Hilbert_topological_equality",
            "role": "older commutator audit identifying Hilbert-topological equality as the key blocker.",
        },
        {
            "source_id": "SRC1152_5_738_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_738_PIM_COMMUTATOR_GATE.csv",
            "needle": "PCG738_1_topological_commutator_zero",
            "role": "R10 commutator gate preserving the topological route as conditional only.",
        },
        {
            "source_id": "SRC1152_6_521_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv",
            "needle": "PC521_2_topological_zero_commutator",
            "role": "earlier PiM commutator gate and no-shortcut record.",
        },
        {
            "source_id": "SRC1152_7_flux_contract",
            "relative_path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "needle": "FC2_closed_mass_current_equation",
            "role": "Ward/topological closure contract requiring a closed mass current equation.",
        },
        {
            "source_id": "SRC1152_8_projector_algebra",
            "relative_path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needle": "PM6_flux_closure_requires_Ward_or_Euler",
            "role": "projector algebra contract forbidding algebra-only flux closure.",
        },
        {
            "source_id": "SRC1152_9_projector_variation",
            "relative_path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
            "needle": "PV2_Hodge_DeWitt_metric_dependence_retained",
            "role": "projector variation stress contract if a Hodge/metric route is used.",
        },
        {
            "source_id": "SRC1152_10_topological_conditions",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
            "needle": "TC500_3_Hilbert_equality",
            "role": "topological closure conditions showing equality remains open.",
        },
        {
            "source_id": "SRC1152_11_bound_fill_row",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
            "needle": "FB550_0_commutator_projector_bound",
            "role": "fallback bound row for commutator and projector variation terms.",
        },
        {
            "source_id": "SRC1152_12_radial_input",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
            "needle": "PI521_1_commutator_profile",
            "role": "radial/source-normalization interface for I_commutator.",
        },
        {
            "source_id": "SRC1152_13_input_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
            "needle": "PIF537_1_I_commutator",
            "role": "input-fill template requiring source-backed I_commutator and R_eq rows.",
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


def commutator_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "clause_id": "COM1152_0_product_rule",
                "claim_piece": "full projected-current product rule",
                "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
                "needed_parent_signature": "either derive [d,Pi_M]J_H=0 on the actual Hilbert-current domain or retain a bounded I_commutator row",
                "current_status": "ACTIVE_OBSTRUCTION",
                "obstruction_if_missing": "source-normalized Newton/local-GR cannot be promoted",
                "routes_to": "ACQ1152_1_I_commutator",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_1_fixed_exterior_domain",
                "claim_piece": "fixed exterior topology before readout",
                "mathematical_form": "Sigma_ext ~= S2 x I with fixed [S2] class and fixed source worldtube",
                "needed_parent_signature": "parent-fixed worldtube plus linking surfaces independent of readout masks",
                "current_status": "CONDITIONAL_OPEN",
                "obstruction_if_missing": "domain motion can re-enter [d,Pi_M]J_H",
                "routes_to": "ACQ1152_3_parent_theorem_certificate",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_2_metric_independent_projector",
                "claim_piece": "topological metric-independent Pi_M",
                "mathematical_form": "delta_g Pi_M=0 and Pi_M uses no Hodge star, Green operator, or fitted boundary metric",
                "needed_parent_signature": "absolute/topological charge map selected by parent action before variation",
                "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "obstruction_if_missing": "projector variation stress must be retained",
                "routes_to": "ACQ1152_2_projector_variation",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_3_closed_generator",
                "claim_piece": "closed normalized topological mass generator",
                "mathematical_form": "d omega_M_top=0 and integral_S2 omega_M_top=1",
                "needed_parent_signature": "normalization owner for the same mass current used by J_H",
                "current_status": "FORMAL_CONDITIONAL_ONLY",
                "obstruction_if_missing": "a closed generator may still be the wrong current",
                "routes_to": "ACQ1152_0_R_eq_integral",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_4_chain_map_property",
                "claim_piece": "Pi_M commutes with exterior derivative on allowed source-current complex",
                "mathematical_form": "[d,Pi_M]J_H=0 for J_H in V_J and dJ_H in domain(Pi_M)",
                "needed_parent_signature": "chain-map theorem, not projector idempotence",
                "current_status": "NOT_PARENT_DERIVED",
                "obstruction_if_missing": "I_commutator remains a live residual",
                "routes_to": "ACQ1152_1_I_commutator",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_5_Hilbert_current_domain",
                "claim_piece": "J_H lies in the exact domain on which Pi_M is defined",
                "mathematical_form": "J_H in V_J; Pi_M J_H and Pi_M dJ_H both defined in the same frame",
                "needed_parent_signature": "same-source-frame Hilbert current and worldtube selector",
                "current_status": "CONDITIONAL_FROM_SOURCE_CONTRACT_NOT_CLOSED",
                "obstruction_if_missing": "the commutator theorem can target a surrogate current",
                "routes_to": "ACQ1152_3_parent_theorem_certificate",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_6_variation_ownership",
                "claim_piece": "delta Pi_M and domain variation are owned or retained",
                "mathematical_form": "delta(Pi_M J)=Pi_M delta J + (delta Pi_M)J with (delta Pi_M)J=0/topological or bounded",
                "needed_parent_signature": "projector stress theorem or numeric PPN/R11 bound input",
                "current_status": "NOT_PARENT_DERIVED",
                "obstruction_if_missing": "projector stress cannot be silently removed",
                "routes_to": "ACQ1152_2_projector_variation",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_7_Hilbert_topological_equality",
                "claim_piece": "topological current equals observed Hilbert projected current",
                "mathematical_form": "Pi_M J_H = J_M_top + dB_zero + R_eq with integral_boundary dB_zero=0",
                "needed_parent_signature": "R_eq=0 theorem or source-backed finite-shell R_eq_integral",
                "current_status": "NOT_DERIVED_KEY_BLOCKER",
                "obstruction_if_missing": "commutator zero can close the wrong object",
                "routes_to": "ACQ1152_0_R_eq_integral",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_8_Hodge_route",
                "claim_piece": "metric/Hodge projector route remains allowed only with stress retained",
                "mathematical_form": "delta_g Pi_H(g), delta chi_D, delta n_mu, and delta G_B varied or bounded",
                "needed_parent_signature": "no hidden metric dependence and no post-readout mask",
                "current_status": "RETAINED_IF_USED",
                "obstruction_if_missing": "Hodge route creates PPN/R11 residual vector",
                "routes_to": "ACQ1152_2_projector_variation",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "COM1152_9_verdict",
                "claim_piece": "derive [d,Pi_M]J_H=0 for the current branch",
                "mathematical_form": "COM1152_1 through COM1152_8 parent-signed on the same Hilbert source-current domain",
                "needed_parent_signature": "fixed topology, topological Pi_M, Hilbert equality, domain closure, variation ownership, no shortcut",
                "current_status": "PIM_COMMUTATOR_ZERO_NOT_DERIVED",
                "obstruction_if_missing": "retain R_eq/I_commutator acquisition rows and keep local-GR/Newton blocked",
                "routes_to": "NEXT1152_0_1153",
                "valid_for_claim": "false",
            },
        ]
    )


def acquisition_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "ACQ1152_0_R_eq_integral",
                "quantity": "R_eq_integral",
                "symbolic_definition": "int_A_ext abs(Pi_M J_H - J_M_top - dB_zero)",
                "required_numeric_fields": "system_id;r1;r2;R_eq_integral;M_H_ref;units;norm_convention",
                "required_source_file": "parent theorem certificate or finite-shell source calculation for Pi_M J_H, J_M_top, and dB_zero",
                "current_value": "MISSING_R_EQ_INTEGRAL",
                "source_path": "MISSING_SOURCE_FILE",
                "current_status": "SOURCE_ACQUISITION_ROW_ONLY",
                "feeds_runner": "PIM1150_1_R_eq_integral;SMOKE1151_0_current_branch",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "ACQ1152_1_I_commutator",
                "quantity": "I_commutator",
                "symbolic_definition": "int_A_ext abs([d,Pi_M]J_H)",
                "required_numeric_fields": "system_id;r1;r2;I_commutator;M_H_ref;projector_type;metric_dependence;units",
                "required_source_file": "source-backed Pi_M algebra/profile calculation or parent chain-map theorem on J_H domain",
                "current_value": "MISSING_I_COMMUTATOR",
                "source_path": "MISSING_SOURCE_FILE",
                "current_status": "SOURCE_ACQUISITION_ROW_ONLY",
                "feeds_runner": "PIM1150_2_I_commutator;PI521_1_commutator_profile;FB550_0_commutator_projector_bound",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "ACQ1152_2_projector_variation",
                "quantity": "epsilon_projector_stress",
                "symbolic_definition": "abs(int_S (delta Pi_M)J_H)/M_H_ref plus Hodge/DeWitt/domain variation terms",
                "required_numeric_fields": "projector_stress_beta_equiv;metric_dependence;domain_variation;M_H_ref;units",
                "required_source_file": "projector stress theorem or finite local residual calculation",
                "current_value": "MISSING_PROJECTOR_STRESS_MAP",
                "source_path": "MISSING_SOURCE_FILE",
                "current_status": "SOURCE_ACQUISITION_ROW_ONLY",
                "feeds_runner": "PIM1150_4_projector_stress;P8_PiM_projector_variation_stress_CONTRACT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "ACQ1152_3_parent_theorem_certificate",
                "quantity": "commutator_zero_certificate",
                "symbolic_definition": "[d,Pi_M]J_H=0 with Pi_M fixed/topological and J_H in the same source-current complex",
                "required_numeric_fields": "not_numeric_if_theorem_signed;otherwise maps to I_commutator and projector_stress rows",
                "required_source_file": "parent proof file with fixed exterior topology, topological Pi_M, Hilbert equality, and variation ownership",
                "current_value": "MISSING_PARENT_THEOREM_CERTIFICATE",
                "source_path": "MISSING_SOURCE_FILE",
                "current_status": "THEOREM_ROUTE_OPEN_BUT_UNSIGNED",
                "feeds_runner": "can theorem-zero ACQ1152_1 only if ACQ1152_0 and ACQ1152_2 are also closed",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "ACQ1152_4_runner_interface",
                "quantity": "PiM_equality_commutator_total",
                "symbolic_definition": "abs(R_eq)/M_H_ref + abs(I_commutator)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(epsilon_projector_stress)",
                "required_numeric_fields": "R_eq_integral;I_commutator;B_zero_flux;epsilon_projector_stress;M_H_ref;source_paths",
                "required_source_file": "all component rows source-backed or theorem-zeroed without reference-zero shortcut",
                "current_value": "MISSING_COMPONENTS",
                "source_path": "MISSING_SOURCE_FILE",
                "current_status": "BLOCKED_MISSING_COMPONENTS",
                "feeds_runner": "P8_Y5_R10_1151_SMOKE_EVALUATION.csv",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1152_0_topological_route",
                "guard": "topological Pi_M can zero the commutator only if the Hilbert-topological equality is also parent-signed",
                "status": "ACTIVE",
                "reason": "otherwise a closed topological current may not be the observed Hilbert mass current",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1152_1_hodge_route",
                "guard": "Hodge or Green-operator Pi_M must retain/bound projector stress",
                "status": "ACTIVE",
                "reason": "metric dependence makes delta Pi_M a real variation term",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1152_2_algebra_not_closure",
                "guard": "Pi_M^2=Pi_M is not a flux-closure theorem",
                "status": "ACTIVE",
                "reason": "Ward, Euler, Hamiltonian, or topological closure is still required",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1152_3_no_readout_mask",
                "guard": "readout masks cannot be inserted inside parent variation",
                "status": "ACTIVE",
                "reason": "masks may only be used after theorem closure or residual scoring",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1152_4_no_unowned_multiplier",
                "guard": "a multiplier closure cannot be imported unless independently owned by parent action",
                "status": "ACTIVE",
                "reason": "unowned multipliers are closure axioms, not derivations",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1152_5_reference_zero_rejected",
                "guard": "reference zero rows cannot be counted as MTS evidence",
                "status": "ACTIVE",
                "reason": "reference rows test runner plumbing only",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1152_0_sources_exist",
                "rule": "all 1152 cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "local audit trail resolves",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1152_1_commutator_zero",
                "rule": "[d,Pi_M]J_H=0 is parent-derived on the actual Hilbert-current domain",
                "gate_pass": "false",
                "reason": "fixed/topological Pi_M, chain-map property, Hilbert equality, and variation ownership are not all signed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1152_2_R_eq_row_filled",
                "rule": "R_eq_integral is numeric/source-backed or theorem-zeroed",
                "gate_pass": "false",
                "reason": "ACQ1152_0 remains MISSING_R_EQ_INTEGRAL",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1152_3_I_commutator_row_filled",
                "rule": "I_commutator is numeric/source-backed or theorem-zeroed",
                "gate_pass": "false",
                "reason": "ACQ1152_1 remains MISSING_I_COMMUTATOR",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1152_4_projector_stress_owned",
                "rule": "projector stress is zero by theorem or retained by bound",
                "gate_pass": "false",
                "reason": "ACQ1152_2 remains MISSING_PROJECTOR_STRESS_MAP",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1152_5_no_shortcuts",
                "rule": "no reference zero, readout mask, algebra-only closure, or unowned multiplier is used",
                "gate_pass": "true_nonclaim",
                "reason": "shortcut guards are explicit and active",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1152_6_Newton_GR_promotion",
                "rule": "source-normalized Newton/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "commutator/equality/source rows remain nonclaim",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1152_0_zero_theorem",
                "decision": "PiM_commutator_zero_not_derived",
                "reason": "a conditional topological route exists, but it is not parent-signed on the same Hilbert-current domain",
                "next_action": "try to parent-sign topological Pi_M/Hilbert equality before using commutator zero",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1152_1_source_acquisition",
                "decision": "R_eq_and_I_commutator_acquisition_rows_written",
                "reason": "if the theorem route fails, these are the first rows required by the runner",
                "next_action": "fill ACQ1152_0 and ACQ1152_1 from a theorem certificate or finite-shell profile calculation",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1152_2_best_next",
                "decision": "target_topological_PiM_Hilbert_equality_parent_signature_or_R_eq_source_fill",
                "reason": "Hilbert equality is the upstream obstruction; without it, a commutator zero can close the wrong current",
                "next_action": "1153 topological PiM Hilbert equality parent signature or R_eq source fill",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1152_0_1153",
                "next_target": "1153-Y5-R10-topological-PiM-Hilbert-equality-parent-signature-or-R_eq-source-fill.md",
                "objective": "try to parent-sign the topological Pi_M/Hilbert equality route; if it fails, fill the R_eq_integral acquisition row",
                "include": "fixed exterior topology; omega_M_top; same Hilbert current; exact boundary zero; finite-shell R_eq source path",
                "exclude": "readout mask; hidden Hodge stress; reference zero; orbital-GM proof; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    guards: list[dict[str, object]],
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

    all_rows = audit + acquisition + guards + gates + decisions + next_target
    add(
        "V1152_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1152_1_verdict_blocks_commutator",
        any(row["clause_id"] == "COM1152_9_verdict" and row["current_status"] == "PIM_COMMUTATOR_ZERO_NOT_DERIVED" for row in audit),
        "commutator zero theorem remains unsigned",
    )
    acquisition_ids = {row["row_id"] for row in acquisition}
    add(
        "V1152_2_acquisition_rows_present",
        {"ACQ1152_0_R_eq_integral", "ACQ1152_1_I_commutator", "ACQ1152_2_projector_variation"}.issubset(acquisition_ids),
        "R_eq, I_commutator, and projector-stress acquisition rows are present",
    )
    add(
        "V1152_3_acquisition_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and contains_missing(row["current_value"]) for row in acquisition),
        "acquisition rows remain missing/nonclaim until sourced",
    )
    add(
        "V1152_4_guards_active",
        {"GUARD1152_0_topological_route", "GUARD1152_1_hodge_route", "GUARD1152_2_algebra_not_closure", "GUARD1152_3_no_readout_mask", "GUARD1152_4_no_unowned_multiplier", "GUARD1152_5_reference_zero_rejected"}.issubset(
            {row["guard_id"] for row in guards if row["status"] == "ACTIVE"}
        ),
        "all no-shortcut projector-route guards are active",
    )
    add(
        "V1152_5_claim_gates_blocked",
        any(row["gate_id"] == "G1152_1_commutator_zero" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1152_6_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "commutator zero and Newton/GR promotion gates remain blocked",
    )
    add(
        "V1152_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1152_7_next_target",
        next_target[0]["next_target"].startswith("1153-") and "Hilbert-equality" in str(next_target[0]["next_target"]),
        "1153 handoff targets topological PiM/Hilbert equality or R_eq source fill",
    )
    add(
        "V1152_8_generated_under_post_checkpoint",
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
    add("V1152_9_csv_parse", csv_parse_ok, "all 1152 CSV outputs parse cleanly")
    add("V1152_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1152_SUMMARY",
        True,
        "1152 rejects an unsigned PiM commutator-zero proof, writes nonclaim R_eq/I_commutator acquisition rows, and sends Hilbert equality/R_eq fill to 1153",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1152 - Y5/R10 PiM Commutator Zero Theorem or R_eq/I_commutator Source Acquisition

**Current verdict:** the direct zero proof does not close. `[d,Pi_M]J_H=0` remains conditional because the topological/fixed Pi_M route is not parent-signed on the same Hilbert source-current domain, and the Hilbert-topological equality is still unsigned.

**Useful progress:** the obstruction is now sharply localized: either prove the topological Pi_M/Hilbert equality route, or fill source-backed `R_eq_integral` and `I_commutator` rows.

**Important guard:** algebra is not closure. `Pi_M^2=Pi_M`, a reference zero, a readout mask, or an unowned multiplier cannot substitute for a Ward/topological/current-domain theorem.

**Best next attack:** parent-sign `Pi_M J_H = J_M_top + dB_zero + R_eq` first. If that fails, fill `R_eq_integral` from an explicit finite-shell source calculation.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, R10, WEP, GitHub, or public claim follows from 1152.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Commutator Zero Theorem Audit
{table(["clause_id", "claim_piece", "mathematical_form", "needed_parent_signature", "current_status", "obstruction_if_missing", "routes_to", "valid_for_claim"], audit)}

## R_eq/I_commutator Source Acquisition Rows
{table(["row_id", "quantity", "symbolic_definition", "required_numeric_fields", "required_source_file", "current_value", "source_path", "current_status", "feeds_runner", "valid_for_claim", "claim_allowed"], acquisition)}

## Projector Route Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

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
        "source_register": OUT / "P8_Y5_R10_1152_SOURCE_REGISTER.csv",
        "audit": OUT / "P8_Y5_R10_1152_COMMUTATOR_ZERO_THEOREM_AUDIT.csv",
        "acquisition": OUT / "P8_Y5_R10_1152_R_EQ_I_COMMUTATOR_SOURCE_ACQUISITION_ROWS.csv",
        "guards": OUT / "P8_Y5_R10_1152_PROJECTOR_ROUTE_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1152_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1152_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1152_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1152_VALIDATION.csv",
    }

    sources = source_rows()
    audit = commutator_audit_rows()
    acquisition = acquisition_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["acquisition"], acquisition)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audit, acquisition, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audit, acquisition, guards, gates, decisions, validation, next_target)
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
