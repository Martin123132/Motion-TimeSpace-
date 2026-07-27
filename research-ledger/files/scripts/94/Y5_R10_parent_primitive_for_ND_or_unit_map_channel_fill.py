from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill"
DOC_PATH = ROOT / "603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_603_SOURCE_REGISTER.csv"
PRIMITIVE_PATH = RESIDUALS / "P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv"
LEMMA_PATH = RESIDUALS / "P8_Y5_R10_603_ZERO_NONZERO_LEMMA.csv"
OWNERSHIP_GATE_PATH = RESIDUALS / "P8_Y5_R10_603_PARENT_OWNERSHIP_GATE.csv"
UNIT_MAP_FORK_PATH = RESIDUALS / "P8_Y5_R10_603_UNIT_MAP_FORK_STATUS.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_603_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_603_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_603_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_603_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_603_VALIDATION.csv"

PRIOR_602_VALIDATION = RESIDUALS / "P8_Y5_BRR545_602_VALIDATION.csv"
PRIOR_602_SELECTOR = RESIDUALS / "P8_Y5_R10_602_BOUND_DOMAIN_SELECTOR_DERIVATION_ATTEMPT.csv"
PRIOR_602_UNIT_MAP = RESIDUALS / "P8_Y5_R10_602_UNIT_MAP_FORK_STATUS.csv"

STATUS = "Y5_R10_ND_zero_nonzero_primitive_candidate_derived_conditionally_parent_kernel_and_normalization_missing"
CLAIM_CEILING = "conditional_ND_primitive_candidate_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md"
COMPACT_SHELL_PROXY = "7.432631961576971e-06"

SOURCE_FILES = [
    ("602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md", "immediate 602 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_602_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_602_BOUND_DOMAIN_SELECTOR_DERIVATION_ATTEMPT.csv", "N_D missing primitive target"),
    ("source-intake/mts_residuals/P8_Y5_R10_602_UNIT_MAP_FORK_STATUS.csv", "unit-map fallback status"),
    ("308-selector-parent-theorem-attempt.md", "spectral/topological selector b_D and c_D"),
    ("309-MTS-boundary-projector-contract-attempt.md", "P_MTS boundary projector contract"),
    ("415-local-trivial-class-selector-theorem-attempt.md", "local trivial class chain and blockers"),
    ("478-determinant-current-parent-ownership-or-demotion.md", "det(Q_coh) shape support but ownership failure"),
    ("481-Qcoh-parent-projector-algebra-or-closure.md", "trace projector algebra and parent ownership contract"),
    ("275-JC-three-form-memory-current-from-Q.md", "J_C determinant memory current shape"),
    ("276-coherent-domain-projector-from-parent-variables.md", "fixed-D coherent trace projector"),
    ("277-domain-free-boundary-Euler-equation.md", "shape derivative/free-boundary route"),
    ("279-representative-selection-boundary-polarization-no-go.md", "selector-function underdetermination no-go"),
    ("60-relative-cohomology-boundary-contract.md", "relative local-zero/FLRW-nonzero contract"),
    ("61-bound-domain-boundary-theorem-attempt.md", "volume-flow identity"),
    ("475-domain-selector-parent-action-clause-or-coefficient-fill.md", "double-zero selector action clause"),
    ("476-double-zero-memory-coupling-origin-or-coefficient-runner.md", "p>=2 requirement and coefficient fallback"),
    ("scripts/Y5_R10_parent_primitive_for_ND_or_unit_map_channel_fill.py", "this checkpoint generator"),
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


def make_primitive_rows() -> list[dict[str, str]]:
    return [
        {
            "primitive_id": "NDP603_0_boundary_spectral_factor",
            "candidate_object": "b_D",
            "mathematical_form": "b_D = lim_{omega->0+} rho_MTS,D(omega)/omega, rho_MTS,D = rho[P_MTS,D B_D, P_MTS,D B_D]",
            "derivation_attempt": "Use a parent boundary spectral density after ordinary baths are removed by P_MTS,D.",
            "local_readout": "closed/gapped projected local boundary channel gives b_D=0",
            "FLRW_readout": "Ohmic coherent MTS boundary channel gives b_D=eta>0",
            "result": "conditional_factor",
            "blocker": "P_MTS,D boundary kernel and ordinary/MTS orthogonality are not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "NDP603_1_relative_class_factor",
            "candidate_object": "c_D",
            "mathematical_form": "c_D = || Pi_rel [J_B]_D ||_rel",
            "derivation_attempt": "Use the norm or topological size of the non-exact relative boundary-memory class.",
            "local_readout": "exact/trivial local relative class gives c_D=0",
            "FLRW_readout": "nontrivial expansion relative class gives c_D>0",
            "result": "conditional_factor",
            "blocker": "relative norm/topological pairing and local trivial class are not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "NDP603_2_activation_product",
            "candidate_object": "A_D = b_D c_D",
            "mathematical_form": "A_D := b_D c_D",
            "derivation_attempt": "Take the product so either local gap or local trivial class switches the branch off, without introducing a fitted threshold.",
            "local_readout": "if b_D=0 or c_D=0 then A_D=0",
            "FLRW_readout": "if b_D>0 and c_D>0 then A_D>0",
            "result": "zero_nonzero_primitive_conditionally_derived",
            "blocker": "A_D still needs parent units/normalization before it can be the action variable chi_D",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "NDP603_3_coherent_trace_factor",
            "candidate_object": "X_D",
            "mathematical_form": "X_D := (1/3)<Tr_h Q>_D or equivalently the coherent trace/volume-flow scalar in the fixed-D branch",
            "derivation_attempt": "Use the unique trace projector from 481 and the fixed-domain coherent projection from 276.",
            "local_readout": "stationary selected domain gives X_D=0 through the scalar volume-flow channel",
            "FLRW_readout": "coherent FLRW gives X_D nonzero and isotropic",
            "result": "fixed_D_algebra_pass",
            "blocker": "Q, D, P_coh, and local X_D=0 are not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "NDP603_4_cubic_memory_current",
            "candidate_object": "J_C",
            "mathematical_form": "J_C = det_h(P_coh Q) Omega_D/V_D = (X_D/3)^3 Omega_D/V_D",
            "derivation_attempt": "Use the determinant of the coherent trace-projected load to supply the p=3/double-zero memory amplitude.",
            "local_readout": "if X_D=0 then J_C=0 with first and second derivative zero in X_D",
            "FLRW_readout": "FLRW coherent trace gives nonzero cubic memory current",
            "result": "shape_derived_conditionally",
            "blocker": "parent ownership of Q_coh/P_coh/D and Ward stress accounting are missing",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "NDP603_5_best_combined_contract",
            "candidate_object": "N_D/A_D plus J_C",
            "mathematical_form": "use A_D=b_D c_D as branch activation and J_C=det_h(P_coh Q) Omega_D/V_D as memory amplitude",
            "derivation_attempt": "Separate the selector question from the amplitude question: A_D decides zero/nonzero branch; J_C supplies the cubic/double-zero current once the branch is active.",
            "local_readout": "A_D=0 and/or J_C=0 can silence the selected local scalar-domain branch",
            "FLRW_readout": "A_D>0 and J_C!=0 keep coherent cosmology active",
            "result": "best_candidate_contract_not_parent_theorem",
            "blocker": "normalization, boundary kernel block, local class theorem, domain selection, R11 and Bianchi debts remain",
            "valid_for_claim": "false",
        },
    ]


def make_lemma_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "ZNL603_0_local_gap",
            "statement": "projected local spectral gap implies b_D=0",
            "proof_status": "proved_from_premise",
            "proof_sketch": "if rho_MTS,D(omega)=0 for 0<omega<omega_gap, then lim rho/omega=0",
            "not_proved": "the parent action forces the projected local gap",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZNL603_1_local_trivial_class",
            "statement": "local exact/trivial relative class implies c_D=0",
            "proof_status": "proved_from_premise",
            "proof_sketch": "Pi_rel kills exact relative representatives, so the projected class norm vanishes",
            "not_proved": "the local branch is always exact/trivial in the parent theory",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZNL603_2_activation_zero",
            "statement": "b_D=0 or c_D=0 implies A_D=b_D c_D=0",
            "proof_status": "algebra_pass",
            "proof_sketch": "product activation has zero if either required local-silence premise holds",
            "not_proved": "A_D normalization and action coupling are parent-owned",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZNL603_3_FLRW_active",
            "statement": "Ohmic coherent bath plus nontrivial expansion class implies A_D>0",
            "proof_status": "conditional_pass",
            "proof_sketch": "b_D=eta>0 and c_D>0 give A_D>0",
            "not_proved": "FLRW bath/class are parent-derived rather than imposed",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZNL603_4_double_zero_gate",
            "statement": "A_D=0 with p>=2 selector gate gives local first-variation silence for the gated memory term",
            "proof_status": "conditional_pass",
            "proof_sketch": "delta(A_D^p L)=p A_D^(p-1)L delta A_D + A_D^p delta L, which vanishes at A_D=0 for p>=2",
            "not_proved": "p>=2 and A_D are both derived by a single deeper parent principle",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "ZNL603_5_counterexample_guard",
            "statement": "without P_MTS,D, ordinary local baths can make b_D>0 and falsely activate N_D",
            "proof_status": "guard_pass",
            "proof_sketch": "generic local EM/matter/environmental spectral density need not be gapped in the unprojected channel",
            "not_proved": "ordinary/MTS sector split by a parent boundary kernel",
            "valid_for_claim": "false",
        },
    ]


def make_ownership_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "POG603_0_boundary_kernel_block",
            "required_parent_input": "K_boundary block diagonalizes ordinary and MTS boundary channels",
            "needed_for": "P_MTS,D and b_D",
            "current_status": "not_derived",
            "failure_if_missing": "ordinary local baths can activate the selector",
            "next_repair": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "gate_id": "POG603_1_relative_topological_pairing",
            "required_parent_input": "Pi_rel and the norm/topological pairing for [J_B]_D are parent-owned",
            "needed_for": "c_D",
            "current_status": "not_derived",
            "failure_if_missing": "relative exactness/triviality remains closure",
            "next_repair": "derive relative complex/topological pairing or retain residual",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "POG603_2_domain_selection",
            "required_parent_input": "physical D and its boundary embedding are selected by Euler/topological law",
            "needed_for": "A_D, X_D, J_C",
            "current_status": "not_derived",
            "failure_if_missing": "fixed-D algebra remains after-the-fact domain choice",
            "next_repair": "bound-domain selector theorem or unit-map demotion",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "POG603_3_normalization",
            "required_parent_input": "units and scale that convert A_D into chi_D without fitted threshold",
            "needed_for": "action variable chi_D",
            "current_status": "open",
            "failure_if_missing": "A_D is zero/nonzero only, not a physical action coefficient",
            "next_repair": "derive normalization from boundary kernel or make closure label explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "POG603_4_Qcoh_parent_variable",
            "required_parent_input": "Q_{mu nu} and P_coh are action/Noether variables with retained metric variation",
            "needed_for": "X_D and J_C",
            "current_status": "algebra_known_parent_ownership_missing",
            "failure_if_missing": "det(P_coh Q) is shape support only, not theorem-zero",
            "next_repair": "derive Q/P_coh owner or keep determinant branch closure-only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "POG603_5_R11_Bianchi",
            "required_parent_input": "R11/source-normalization and Ward/Bianchi stress ledgers are closed or scored",
            "needed_for": "local-GR/PPN/R10 promotion",
            "current_status": "blocked",
            "failure_if_missing": "q_loc/source residuals can survive despite selector zero",
            "next_repair": "R11 zero-or-fill plus local residual vector",
            "valid_for_claim": "false",
        },
    ]


def make_unit_map_rows() -> list[dict[str, str]]:
    return [
        {
            "fork_id": "UMF603_0_derivation_status",
            "route": "N_D derivation",
            "status": "partial_conditionally_sharpened",
            "why": "A_D=b_D c_D gives a clean zero/nonzero activation primitive if P_MTS and relative class are parent-owned",
            "required_next_input": "parent boundary kernel block for P_MTS,D",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "UMF603_1_unit_map_status",
            "route": "compact-shell unit map",
            "status": "still_deferred_but_closer",
            "why": "if the boundary kernel block cannot be derived next, the primitive route should demote and the unit-map channel should be chosen",
            "required_next_input": "R10 alpha(lambda), PPN vector, WEP, or clock channel plus units/coefficient",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "UMF603_2_no_score",
            "route": "local-bound evidence",
            "status": "no_claim",
            "why": f"proxy {COMPACT_SHELL_PROXY} still lacks channel conversion and A_D/J_C are not observable residuals",
            "required_next_input": "source-backed coefficient rows or theorem-zero certificates",
            "valid_for_claim": "false",
        },
    ]


def make_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RU603_0_ND_primitive",
            "previous_status": "N_D_parent_primitive_missing",
            "new_status": "zero_nonzero_candidate_A_D_written",
            "reason": "A_D=b_D c_D is threshold-free and has the desired local-zero/FLRW-active branch logic",
            "still_needed": "parent-owned P_MTS,D, relative class theorem, and normalization",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU603_1_cubic_memory_amplitude",
            "previous_status": "det_Qcoh_shape_support_not_owned",
            "new_status": "retained_as_amplitude_not_selector_owner",
            "reason": "J_C=det_h(P_coh Q) supplies p=3 shape once Qcoh/domain are owned, but it does not by itself select D",
            "still_needed": "Q/P_coh/D parent ownership and Ward stress accounting",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU603_2_local_GR_stack",
            "previous_status": "q_loc_and_R11_open",
            "new_status": "still_open",
            "reason": "A_D zero would silence only the selector-gated scalar/domain term, not all local residuals",
            "still_needed": "R11, source normalization, boundary charge, and q_loc exchange-owner terms",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU603_3_unit_map",
            "previous_status": "fallback_unfilled",
            "new_status": "defer_one_more_step_or_demote_after_P_MTS",
            "reason": "P_MTS boundary kernel is now the decisive derivation target",
            "still_needed": "if P_MTS fails, choose physical unit-map channel and score closure",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D603_0_activation_primitive",
            "decision": "accept A_D=b_D c_D as the best N_D candidate primitive",
            "meaning": "it is threshold-free and gives the right zero/nonzero branch logic when the spectral and relative factors are owned",
            "claim_status": "conditional_candidate_only",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D603_1_memory_amplitude",
            "decision": "keep J_C=det_h(P_coh Q) as the amplitude/current clue",
            "meaning": "J_C gives the cubic/double-zero memory shape but does not solve selector/domain ownership",
            "claim_status": "shape_support_only",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D603_2_main_blocker",
            "decision": "attack P_MTS boundary kernel next",
            "meaning": "without a parent ordinary/MTS sector split, A_D can be polluted by ordinary local baths",
            "claim_status": "next_derivation_gate",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D603_3_promotion",
            "decision": "forbid local-GR/PPN/R10 promotion",
            "meaning": "N_D is not parent-normalized or action-owned; q_loc/R11/boundary debts remain open",
            "claim_status": "forbidden",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU603_0_allowed",
            "allowed_after_603": "use A_D=b_D c_D as the precise N_D theorem target",
            "forbidden_after_603": "call A_D a parent action variable before P_MTS, c_D pairing, and normalization are derived",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU603_1_allowed",
            "allowed_after_603": "use J_C=det_h(P_coh Q) as the cubic memory amplitude clue",
            "forbidden_after_603": "use determinant shape support as local-GR or alpha3 evidence",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU603_2_allowed",
            "allowed_after_603": "demote to unit-map scoring if P_MTS kernel block fails",
            "forbidden_after_603": "continue stacking conditional selectors without choosing scoring fallback",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S603_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "ND_status": "A_D_zero_nonzero_candidate_conditionally_derived",
            "amplitude_status": "J_C_cubic_shape_support_only",
            "main_blocker": "P_MTS_boundary_kernel_block_and_normalization",
            "unit_map_status": "fallback_unfilled",
            "best_private_read": "603 gets a real theorem target: N_D should be A_D=b_D c_D, while J_C supplies the cubic memory amplitude. This is a stronger derivation shape, but not a parent theorem because P_MTS, c_D pairing, normalization, domain selection, R11 and Bianchi debts remain open.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    primitive_rows: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    ownership_rows: list[dict[str, str]],
    unit_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_602_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result", "").strip().lower() != "pass"]
    prior_selector = read_csv(PRIOR_602_SELECTOR)
    prior_unit = read_csv(PRIOR_602_UNIT_MAP)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in primitive_rows if row["valid_for_claim"] == "true"],
        *[row for row in lemma_rows if row["valid_for_claim"] == "true"],
        *[row for row in ownership_rows if row["valid_for_claim"] == "true"],
        *[row for row in unit_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    activation_product = any(
        row["primitive_id"] == "NDP603_2_activation_product"
        and row["result"] == "zero_nonzero_primitive_conditionally_derived"
        for row in primitive_rows
    )
    cubic_shape = any(row["primitive_id"] == "NDP603_4_cubic_memory_current" for row in primitive_rows)
    local_zero_lemma = any(row["lemma_id"] == "ZNL603_2_activation_zero" for row in lemma_rows)
    flrw_lemma = any(row["lemma_id"] == "ZNL603_3_FLRW_active" for row in lemma_rows)
    counterexample_guard = any(row["lemma_id"] == "ZNL603_5_counterexample_guard" for row in lemma_rows)
    pmts_blocker = any(row["gate_id"] == "POG603_0_boundary_kernel_block" and row["current_status"] == "not_derived" for row in ownership_rows)
    normalization_open = any(row["gate_id"] == "POG603_3_normalization" and row["current_status"] == "open" for row in ownership_rows)
    unit_unfilled = any(row["fork_id"] == "UMF603_1_unit_map_status" and "deferred" in row["status"] for row in unit_rows)
    local_gr_open = any(row["runner_id"] == "RU603_2_local_GR_stack" and row["new_status"] == "still_open" for row in runner_rows)
    return [
        {
            "check_id": "V603_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V603_1_prior_602_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};selector_rows={len(prior_selector)};unit_rows={len(prior_unit)}",
        },
        {
            "check_id": "V603_2_ND_activation_candidate_written",
            "result": "pass" if activation_product else "fail",
            "detail": "A_D=b_D c_D zero/nonzero primitive present",
        },
        {
            "check_id": "V603_3_cubic_amplitude_kept_separate",
            "result": "pass" if cubic_shape else "fail",
            "detail": "J_C determinant is amplitude/shape support, not selector ownership",
        },
        {
            "check_id": "V603_4_zero_nonzero_lemma_and_counterguard",
            "result": "pass" if local_zero_lemma and flrw_lemma and counterexample_guard else "fail",
            "detail": f"local_zero={local_zero_lemma};FLRW={flrw_lemma};guard={counterexample_guard}",
        },
        {
            "check_id": "V603_5_parent_blockers_visible",
            "result": "pass" if pmts_blocker and normalization_open and local_gr_open else "fail",
            "detail": f"P_MTS_blocker={pmts_blocker};normalization_open={normalization_open};local_GR_open={local_gr_open}",
        },
        {
            "check_id": "V603_6_unit_map_unfilled_and_no_claim_rows",
            "result": "pass" if unit_unfilled and not claim_rows else "fail",
            "detail": f"unit_unfilled={unit_unfilled};claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V603_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    primitive_rows: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    ownership_rows: list[dict[str, str]],
    unit_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 603 Y5 R10 parent primitive for N_D or unit-map channel fill

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- We can sharpen `N_D`: the best selector primitive is the activation product `A_D=b_D c_D`, where `b_D` is the projected MTS boundary IR spectral factor and `c_D` is the non-exact relative boundary-class factor.
- This gives the right threshold-free branch logic: local projected gap or local trivial relative class makes `A_D=0`; coherent FLRW with an Ohmic projected bath and nontrivial expansion class gives `A_D>0`.
- The determinant current `J_C=det_h(P_coh Q) Omega_D/V_D` should not be the selector by itself; it is better treated as the cubic/double-zero memory amplitude once the branch is active.
- This is a conditional derivation, not a parent theorem. The decisive missing parent input is now the `P_MTS,D` boundary kernel block and the normalization that turns `A_D` into an action variable.

## Candidate Primitive
```text
b_D = lim_(omega->0+) rho[P_MTS,D B_D, P_MTS,D B_D](omega)/omega
c_D = || Pi_rel [J_B]_D ||_rel
A_D = b_D c_D
```

Then:

```text
local gap or local trivial class -> A_D = 0
FLRW Ohmic bath plus nontrivial class -> A_D > 0
```

This is the strongest version of `N_D` so far because it does not need an empirical threshold. But it still needs a parent-owned projector, pairing, and normalization.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## N_D Primitive Derivation Attempt
{markdown_table(primitive_rows, ["primitive_id", "candidate_object", "mathematical_form", "derivation_attempt", "local_readout", "FLRW_readout", "result", "blocker", "valid_for_claim"])}

## Zero-Nonzero Lemma
{markdown_table(lemma_rows, ["lemma_id", "statement", "proof_status", "proof_sketch", "not_proved", "valid_for_claim"])}

## Parent Ownership Gate
{markdown_table(ownership_rows, ["gate_id", "required_parent_input", "needed_for", "current_status", "failure_if_missing", "next_repair", "valid_for_claim"])}

## Unit-Map Fork Status
{markdown_table(unit_rows, ["fork_id", "route", "status", "why", "required_next_input", "valid_for_claim"])}

## Runner Update
{markdown_table(runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_603", "forbidden_after_603", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a good squeeze. `N_D` is no longer a foggy placeholder; it has a concrete best candidate, `A_D=b_D c_D`. The remaining lock is brutally specific: prove the parent boundary kernel really splits ordinary bath channels from MTS memory channels. If that block structure fails, we stop calling this derivation and take the compact-shell unit-map scoring branch.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    primitive_rows = make_primitive_rows()
    lemma_rows = make_lemma_rows()
    ownership_rows = make_ownership_rows()
    unit_rows = make_unit_map_rows()
    runner_rows = make_runner_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, primitive_rows, lemma_rows, ownership_rows, unit_rows, runner_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        PRIMITIVE_PATH,
        primitive_rows,
        ["primitive_id", "candidate_object", "mathematical_form", "derivation_attempt", "local_readout", "FLRW_readout", "result", "blocker", "valid_for_claim"],
    )
    write_csv(LEMMA_PATH, lemma_rows, ["lemma_id", "statement", "proof_status", "proof_sketch", "not_proved", "valid_for_claim"])
    write_csv(OWNERSHIP_GATE_PATH, ownership_rows, ["gate_id", "required_parent_input", "needed_for", "current_status", "failure_if_missing", "next_repair", "valid_for_claim"])
    write_csv(UNIT_MAP_FORK_PATH, unit_rows, ["fork_id", "route", "status", "why", "required_next_input", "valid_for_claim"])
    write_csv(RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_603", "forbidden_after_603", "next_action"])
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
            "ND_status",
            "amplitude_status",
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
        primitive_rows,
        lemma_rows,
        ownership_rows,
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
