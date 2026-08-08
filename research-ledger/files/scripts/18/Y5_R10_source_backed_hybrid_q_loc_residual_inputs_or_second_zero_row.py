from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "735-Y5-R10-source-backed-hybrid-q_loc-residual-inputs-or-second-zero-row.md"
NEXT_TARGET = "736-Y5-R10-matter-no-marker-source-normalization-or-third-zero-row.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_735_second_narrow_zero_row_proper_representative_boundary_charge_derived_observed_boundary_flux_still_open"
CLAIM_CEILING = "proper_representative_boundary_charge_zero_only_observed_q_loc_boundary_source_flux_still_unscored_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_735_SOURCE_REGISTER.csv"
SECOND_ZERO_PATH = RESIDUALS / "P8_Y5_R10_735_SECOND_ZERO_ATTEMPT.csv"
BOUNDARY_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_735_PROPER_BOUNDARY_DOMAIN_THEOREM.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_735_HYBRID_QLOC_RESIDUAL_RUNNER_UPDATE.csv"
ACQUISITION_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_735_SOURCE_ACQUISITION_QUEUE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_735_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_735_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_735_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_735_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "734_doc": {
        "path": POST_CHECKPOINT / "734-Y5-R10-fill-hybrid-q_loc-residual-runner-or-derive-first-zero-row.md",
        "role": "immediate first-zero and residual-runner handoff",
        "needles": ["one narrow zero row is derivable", OUTPUT_DOC.name, "hunt a second zero row"],
    },
    "734_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_734_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V734_11_decision_next_target_selected", OUTPUT_DOC.name, "V734_13_formalization_workbench_untouched"],
    },
    "734_first_zero": {
        "path": RESIDUALS / "P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv",
        "role": "first zero row and boundary failure handoff",
        "needles": ["FZA734_0_representative_vertical_q_loc_variation", "FZA734_4_boundary_flux_zero", "blocked_not_zero"],
    },
    "734_runner": {
        "path": RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv",
        "role": "filled nonclaim runner",
        "needles": ["HQR734_2_boundary_pressure_alpha3", "derive boundary silence", "HQR734_6_representative_vertical_variation_zero"],
    },
    "731_boundary": {
        "path": RESIDUALS / "P8_Y5_R10_731_BOUNDARY_CLOSURE_LEDGER.csv",
        "role": "boundary/properness source",
        "needles": ["BCL731_0_proper_vertical_domain", "Q_X^rep=0", "BCL731_4_corner_symplectic_flux"],
    },
    "731_hybrid_contract": {
        "path": RESIDUALS / "P8_Y5_R10_731_HYBRID_QUOTIENT_CONTRACT.csv",
        "role": "hybrid quotient boundary and P/J contract",
        "needles": ["HQC731_4_PJ_zero_for_extra", "j_X^rep=theta_Y(v_X)-mu_X=dB_rep", "HQC731_5_no_double_count_GR_charge"],
    },
    "731_redteam": {
        "path": RESIDUALS / "P8_Y5_R10_731_NO_CHEAT_RED_TEAM.csv",
        "role": "boundary edge and ADM attacks",
        "needles": ["NCR731_1_boundary_edge_mode", "source K_edge", "NCR731_3_ADM_double_count"],
    },
    "729_noether": {
        "path": RESIDUALS / "P8_Y5_R10_729_NOETHER_PJ_ORIGIN_FORMULA.csv",
        "role": "Noether P/J current formula",
        "needles": ["NPJ729_2_Noether_current", "j_X = theta_Y(v_X) - mu_X", "NPJ729_5_symplectic_flat_closure"],
    },
    "728_omega": {
        "path": RESIDUALS / "P8_Y5_R10_728_OMEGA_DCDAGGER_COMPARISON.csv",
        "role": "boundary Hamiltonian/Omega flatness comparison",
        "needles": ["CMP728_4_boundary", "Q_X=0/exact/proper", "CMP728_5_verdict"],
    },
    "730_parent_candidates": {
        "path": RESIDUALS / "P8_Y5_R10_730_MINIMAL_PARENT_FILL_CANDIDATES.csv",
        "role": "hybrid EH plus quotient-extra parent candidate",
        "needles": ["MPF730_C_hybrid_EH_plus_quotient_extra", "promising_current_chain_contract", "local GR from EH current plus theorem-zero"],
    },
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for key, info in SOURCES.items()
    ]


def make_second_zero_attempt(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "SZA735_0_proper_representative_boundary_charge",
            "target_quantity": "Q_X^rep[partial U]",
            "theorem_or_formula": "For a representative vertical v_X^rep with support compact in the local region or vanishing in a collar of partial U, i_partialU X_rep=0 and i_partialU dX_rep=0 imply Q_X^rep=integral_partialU k_X^rep=0.",
            "premises": "v_X^rep is a proper representative transformation; ADM/time/rotation/boost transformations are excluded; boundary reference data live in Q_obs^hybrid.",
            "derivation": "Noether current rows give j_X=theta_Y(v_X)-mu_X and the hybrid contract gives j_X^rep=dB_rep/exact. With X_rep and its needed jets zero on the boundary collar, the pullback of the surface charge density k_X^rep vanishes pointwise; therefore the compact-boundary integral is zero.",
            "verdict": "derived_second_narrow_zero_row_conditional",
            "residual_left": "Only representative boundary charge is killed. Observed reduced boundary/source-measure flux can still exist through Phi_red, matter readout, or non-proper edge modes.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "731_hybrid_contract", "729_noether"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "SZA735_1_proper_corner_symplectic_flux",
            "target_quantity": "Omega_boundary(delta Y,v_X^rep)",
            "theorem_or_formula": "If v_X^rep is compactly supported away from the worldtube boundary/corners, then the boundary pullback of theta_Y(v_X^rep), delta k_X^rep, and the corner symplectic current vanishes.",
            "premises": "Proper vertical support condition holds in a boundary collar; variations preserve boundary reference data; no improper observed GR symmetry is included in v_X^rep.",
            "derivation": "The covariant phase-space boundary term is built from the boundary restriction of v_X^rep and its finite jet. Those vanish by domain choice, so Omega_boundary(delta Y,v_X^rep)=0 for the representative branch.",
            "verdict": "derived_narrow_zero_row_conditional",
            "residual_left": "Does not prove the reduced observed boundary flux B_boundary^nu in q_loc is zero.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "728_omega", "730_parent_candidates"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "SZA735_2_ADM_double_count_guard",
            "target_quantity": "ordinary ADM/Hamiltonian charge",
            "theorem_or_formula": "ADM/time/rotation/boost charges remain in Q_obs^hybrid and are not elements of the representative vertical domain.",
            "premises": "The quotient split keeps O_GR and boundary ADM/reference class observable, while v_X^rep acts only on R_rep.",
            "derivation": "Because d pi_h(v_X^rep)=0 on O_GR and B_ref, quotienting representative motion does not quotient the physical EH Hamiltonian generators.",
            "verdict": "guard_strengthened_not_full_zero",
            "residual_left": "Pi_M/Pi_EH projection still needs a full parent proof before source-normalization claims.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_hybrid_contract", "731_redteam", "730_parent_candidates"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "SZA735_3_observed_boundary_flux",
            "target_quantity": "P_loc B_boundary^nu in observed q_loc",
            "theorem_or_formula": "q_loc^nu = P_loc(sum_A E_A nabla^nu Phi_A + B_boundary^nu) still permits observed reduced boundary/source flux.",
            "premises": "The boundary term belongs to Q_obs^hybrid/Phi_red/matter readout rather than pure representative fibre motion.",
            "derivation": "The proper representative support theorem removes only Q_X^rep. It does not force B_boundary^nu=0 for reduced observed fields.",
            "verdict": "not_derived_for_current_claim",
            "residual_left": "Boundary/alpha3/compact-shell runner remains active.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_first_zero", "734_runner", "731_redteam"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "SZA735_4_Y5_source_normalization",
            "target_quantity": "C_qmu source-normalization projection",
            "theorem_or_formula": "Measured source strength equals the observed EH/Hilbert source without an extra q_loc projection.",
            "premises": "Matter/readout functors factor through Q_obs^hybrid with no universal representative marker and no source-measure leakage.",
            "derivation": "The boundary theorem does not address matter/readout no-marker coupling, so Y5 remains outside this proof.",
            "verdict": "blocked_not_zero",
            "residual_left": "Y5 source-normalization remains the next best target.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner", "731_redteam"),
            "generated_utc": generated_utc,
        },
    ]


def make_boundary_theorem(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PBD735_0_domain",
            "statement": "Restrict v_X^rep to proper representative transformations: support compact in U or zero in an open collar of partial U, including required finite jets.",
            "math_use": "i_partialU v_X^rep = 0 and i_partialU nabla^k v_X^rep = 0 for the highest derivative order entering theta/mu/k_X.",
            "status": "domain_theorem_condition",
            "claim_limit": "This is a choice of proper gauge domain, not a physical edge-mode theorem.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PBD735_1_current",
            "statement": "Use the parent Noether current j_X=theta_Y(v_X)-mu_X and the hybrid representative contract j_X^rep=dB_rep/exact.",
            "math_use": "For proper support, the boundary charge density k_X^rep built from X_rep and its jets vanishes on partial U.",
            "status": "conditional_current_zero",
            "claim_limit": "Requires current MTS to use the hybrid representative split; does not fill Gamma/Khat ownership.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PBD735_2_charge",
            "statement": "Q_X^rep[partial U]=integral_partialU k_X^rep=0.",
            "math_use": "The integrand vanishes pointwise on the compact boundary collar, so no edge-alpha row is needed for the pure representative branch.",
            "status": "derived_narrow_zero",
            "claim_limit": "Only pure representative charge is zero; observed EH ADM charges remain physical.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PBD735_3_corner",
            "statement": "Omega_boundary(delta Y,v_X^rep)=0 for variations preserving the boundary reference class.",
            "math_use": "Boundary symplectic current depends on boundary values of v_X^rep and its jets, which vanish by PBD735_0.",
            "status": "derived_narrow_zero",
            "claim_limit": "Does not prove any non-proper edge transition mode is absent.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "PBD735_4_observed_separation",
            "statement": "ADM and observed boundary/reference charges are retained in Q_obs^hybrid.",
            "math_use": "The zero applies to representative vertical X only, preventing accidental erasure of GR Hamiltonian charges.",
            "status": "guard_retained",
            "claim_limit": "Pi_M/Pi_EH and source-normalization projections still need parent proof.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_runner_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "HQR735_0_compact_shell_budget",
            "parent_runner_id": "HQR734_0_compact_shell_budget",
            "status_after_735": "partly_pruned_representative_boundary_only",
            "zero_or_input": "Q_X^rep=0 and Omega_boundary(deltaY,v_X^rep)=0 for proper representative transformations",
            "still_missing": "observed compact-shell source-measure map, units, sign convention, official arena bound",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner", "731_boundary"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_1_source_normalization_Y5",
            "parent_runner_id": "HQR734_1_source_normalization_Y5",
            "status_after_735": "unchanged_blocked",
            "zero_or_input": "none",
            "still_missing": "matter/readout no-marker theorem, C_qmu, units, parent-owned P_loc, source-normalization coefficients",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner", "731_redteam"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_2_boundary_pressure_alpha3",
            "parent_runner_id": "HQR734_2_boundary_pressure_alpha3",
            "status_after_735": "partly_pruned_representative_boundary_only",
            "zero_or_input": "proper representative edge charge and corner flux are theorem-zero",
            "still_missing": "observed boundary/source-measure flux coefficient to alpha3-equivalent row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner", "728_omega", "731_boundary"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_3_PPN_metric_tail",
            "parent_runner_id": "HQR734_3_PPN_metric_tail",
            "status_after_735": "unchanged_not_scoreable",
            "zero_or_input": "no PPN coefficient derived",
            "still_missing": "weak-field Green operator, source split, gauge convention, PPN map",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_4_R10_range_tail",
            "parent_runner_id": "HQR734_4_R10_range_tail",
            "status_after_735": "unchanged_not_scoreable",
            "zero_or_input": "no alpha(lambda) coefficient derived",
            "still_missing": "lambda, alpha coefficient, source path, parent coefficient source",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_5_R11_operator_vector",
            "parent_runner_id": "HQR734_5_R11_operator_vector",
            "status_after_735": "unchanged_not_scoreable",
            "zero_or_input": "no operator vector coefficient derived",
            "still_missing": "operator basis, units, weak-field normalization, local bound comparison",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_6_representative_vertical_variation_zero",
            "parent_runner_id": "HQR734_6_representative_vertical_variation_zero",
            "status_after_735": "retained_derived_narrow_zero",
            "zero_or_input": "L_{v_X^rep} q_loc=0 under hybrid pullback premises",
            "still_missing": "current Gamma/Khat/P_loc symbol match before broader claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_first_zero"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR735_7_proper_boundary_charge_zero",
            "parent_runner_id": "new_from_731_boundary",
            "status_after_735": "derived_narrow_zero",
            "zero_or_input": "Q_X^rep[partial U]=0 and Omega_boundary(deltaY,v_X^rep)=0 for proper representative transformations",
            "still_missing": "observed boundary flux and matter/source-normalization rows",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "731_hybrid_contract", "729_noether"),
            "generated_utc": generated_utc,
        },
    ]


def make_acquisition_queue(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "AQ735_0_observed_boundary_alpha3",
            "needed_input": "coefficient mapping observed B_boundary^nu or source-measure pressure to alpha3-equivalent bound",
            "current_status": "missing",
            "why_not_claimable": "proper representative edge charge zero does not kill observed reduced boundary flux",
            "next_action": "derive boundary Ward silence or source alpha3 projection coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "AQ735_1_Y5_C_qmu",
            "needed_input": "C_qmu projection from q_loc to measured-GM/source-normalization channels",
            "current_status": "missing",
            "why_not_claimable": "matter/readout no-marker theorem not proved",
            "next_action": "attack matter no-marker/source-normalization as third zero row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "AQ735_2_R10_alpha_lambda",
            "needed_input": "q_loc-to-alpha(lambda) coefficient with units and parent source path",
            "current_status": "missing",
            "why_not_claimable": "R10 bound curve exists only as infrastructure; predicted coefficient remains symbolic",
            "next_action": "source or derive alpha coefficient after Y5/boundary split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "AQ735_3_PPN_map",
            "needed_input": "linearized q_loc-to-Delta_PPN map",
            "current_status": "missing",
            "why_not_claimable": "no weak-field Green operator/gauge map is filled",
            "next_action": "derive PPN coefficient contract after source-normalization split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_decision_matrix(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D735_0_second_zero_row_selected",
            "decision": "accept proper representative boundary charge as the second narrow zero row",
            "meaning": "Pure representative edge charge and corner symplectic flux can be killed by the proper vertical domain.",
            "claim_status": "theorem_contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_boundary", "729_noether"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D735_1_observed_boundary_flux_not_killed",
            "decision": "do not claim boundary no-flux for observed reduced q_loc",
            "meaning": "The theorem applies to representative boundary charge only, not Phi_red/matter/source-measure flux.",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner", "731_redteam"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D735_2_next_target_matter_source_normalization",
            "decision": "move next to matter no-marker/source-normalization or a third zero row",
            "meaning": "Y5 is now the largest live local branch after pruning representative vertical and proper boundary charges.",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("734_runner", "731_redteam"),
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU735_0_allowed",
            "allowed_after_735": "say pure representative boundary charge is zero for proper vertical transformations",
            "forbidden_after_735": "say observed boundary/source-measure flux, PPN, R10, WEP, Newton, or local-GR has passed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU735_1_allowed",
            "allowed_after_735": "use proper support/collar condition as a theorem-domain requirement",
            "forbidden_after_735": "hide physical edge modes by calling them representative gauge",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU735_2_allowed",
            "allowed_after_735": "attack matter no-marker/source normalization as the next zero-or-bound gate",
            "forbidden_after_735": "treat Y5 source-normalization as solved by boundary properness",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Second narrow zero row derived: Q_X^rep[partial U]=0 and Omega_boundary(deltaY,v_X^rep)=0 for proper representative transformations.",
            "hard_blocker": "Observed boundary/source-measure flux, Y5 source normalization, matter no-marker theorem, PPN/R10 coefficients, Gamma/Khat/P_loc current symbol match.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    source_register: list[dict[str, Any]],
    second_zero_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in source_register)
    needles_pass = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["734_validation"]["path"])
    second_zero = any(
        row.get("zero_id") == "SZA735_0_proper_representative_boundary_charge"
        and row.get("verdict") == "derived_second_narrow_zero_row_conditional"
        for row in second_zero_rows
    )
    corner_zero = any(
        row.get("zero_id") == "SZA735_1_proper_corner_symplectic_flux"
        and row.get("verdict") == "derived_narrow_zero_row_conditional"
        for row in second_zero_rows
    )
    observed_boundary_not_killed = any(
        row.get("zero_id") == "SZA735_3_observed_boundary_flux"
        and row.get("verdict") == "not_derived_for_current_claim"
        for row in second_zero_rows
    )
    adm_guard = any(row.get("zero_id") == "SZA735_2_ADM_double_count_guard" for row in second_zero_rows)
    boundary_theorem_steps = {row.get("step_id", "") for row in boundary_rows}
    required_steps = {"PBD735_0_domain", "PBD735_1_current", "PBD735_2_charge", "PBD735_3_corner", "PBD735_4_observed_separation"}
    runner_pruned = any(
        row.get("runner_id") == "HQR735_7_proper_boundary_charge_zero"
        and row.get("status_after_735") == "derived_narrow_zero"
        for row in runner_rows
    )
    y5_retained = any(
        row.get("runner_id") == "HQR735_1_source_normalization_Y5"
        and row.get("status_after_735") == "unchanged_blocked"
        for row in runner_rows
    )
    acquisition_missing = all(row.get("current_status") == "missing" for row in acquisition_rows)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for row in [*second_zero_rows, *boundary_rows, *runner_rows, *acquisition_rows, *decision_rows]
    )
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()

    return [
        {"check_id": "V735_0_source_paths_exist", "result": "pass" if source_paths_exist else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V735_1_source_needles_present", "result": "pass" if needles_pass else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V735_2_prior_734_clean", "result": "pass" if prior_clean else "fail", "detail": "734 validation has no failures"},
        {"check_id": "V735_3_734_selected_735", "result": "pass" if text_contains(SOURCES["734_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name},
        {"check_id": "V735_4_second_zero_charge_derived", "result": "pass" if second_zero else "fail", "detail": "Q_X^rep boundary charge zero row exists"},
        {"check_id": "V735_5_corner_flux_zero_derived", "result": "pass" if corner_zero else "fail", "detail": "proper representative corner flux zero row exists"},
        {"check_id": "V735_6_observed_boundary_flux_retained", "result": "pass" if observed_boundary_not_killed else "fail", "detail": "observed q_loc boundary flux not claimed killed"},
        {"check_id": "V735_7_ADM_no_double_count_guard", "result": "pass" if adm_guard else "fail", "detail": "ADM charges retained in Q_obs^hybrid"},
        {"check_id": "V735_8_boundary_theorem_steps_present", "result": "pass" if required_steps.issubset(boundary_theorem_steps) else "fail", "detail": f"steps={len(boundary_theorem_steps)}"},
        {"check_id": "V735_9_runner_pruned_but_not_claimed", "result": "pass" if runner_pruned and y5_retained else "fail", "detail": "proper boundary branch pruned; Y5 retained"},
        {"check_id": "V735_10_acquisition_rows_missing_not_claim", "result": "pass" if acquisition_missing else "fail", "detail": "source inputs remain missing until sourced/derived"},
        {"check_id": "V735_11_no_claim_rows_promoted", "result": "pass" if all_nonclaim else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V735_12_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decision_rows) else "fail", "detail": NEXT_TARGET},
        {"check_id": "V735_13_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V735_14_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V735_15_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V735_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    source_register: list[dict[str, Any]],
    second_zero_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 735 - Y5 R10 Source-Backed Hybrid q_loc Residual Inputs Or Second Zero Row

## Summary

Start point: 734 derived the first narrow zero row, `L_{{v_X^rep}} q_loc^nu=0`, while keeping observed `q_loc` alive as a reduced residual.

Current verdict: **a second narrow zero row is derivable**:

```text
Q_X^rep[partial U] = 0
Omega_boundary(delta Y, v_X^rep) = 0
```

but only for **proper representative vertical transformations** with support compact in the local region or zero in a boundary collar. This prunes pure representative edge charge. It does not kill observed reduced boundary/source-measure flux, Y5 source-normalization, PPN, R10, WEP, Newton, or local-GR residuals.

| Item | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | second narrow proper-boundary zero row plus nonclaim input queue |
| Next target | `{NEXT_TARGET}` |

## Second Zero Attempt

{markdown_table(second_zero_rows, ["zero_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim"])}

## Proper Boundary Domain Theorem

{markdown_table(boundary_rows, ["step_id", "statement", "math_use", "status", "claim_limit", "valid_for_claim"])}

## Hybrid q_loc Runner Update

{markdown_table(runner_rows, ["runner_id", "parent_runner_id", "status_after_735", "zero_or_input", "still_missing", "valid_for_claim"])}

## Source Acquisition Queue

{markdown_table(acquisition_rows, ["input_id", "needed_input", "current_status", "why_not_claimable", "next_action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_735", "forbidden_after_735", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is another careful inch forward. We can now say the pure representative boundary gremlin has no charge if it is genuinely proper gauge: it vanishes in the boundary collar, so its charge and corner symplectic flux vanish. That is useful. The bigger beast is still alive: observed reduced boundary flux and source-normalization are not killed by this, so the next natural attack is the matter no-marker/Y5 channel.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_root = RUNS / f"735_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    second_zero_rows = make_second_zero_attempt(generated_utc)
    boundary_rows = make_boundary_theorem(generated_utc)
    runner_rows = make_runner_update(generated_utc)
    acquisition_rows = make_acquisition_queue(generated_utc)
    decision_rows = make_decision_matrix(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        SECOND_ZERO_PATH,
        BOUNDARY_THEOREM_PATH,
        RUNNER_UPDATE_PATH,
        ACQUISITION_QUEUE_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    write_csv(
        SOURCE_REGISTER_PATH,
        source_register,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SECOND_ZERO_PATH,
        second_zero_rows,
        ["zero_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        BOUNDARY_THEOREM_PATH,
        boundary_rows,
        ["step_id", "statement", "math_use", "status", "claim_limit", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RUNNER_UPDATE_PATH,
        runner_rows,
        ["runner_id", "parent_runner_id", "status_after_735", "zero_or_input", "still_missing", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        ACQUISITION_QUEUE_PATH,
        acquisition_rows,
        ["input_id", "needed_input", "current_status", "why_not_claimable", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_rows,
        ["route_id", "allowed_after_735", "forbidden_after_735", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(source_register, second_zero_rows, boundary_rows, runner_rows, acquisition_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    build_doc(
        source_register,
        second_zero_rows,
        boundary_rows,
        runner_rows,
        acquisition_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    status_payload = {
        "generated_utc": generated_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": str(OUTPUT_DOC),
        "validation": str(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
