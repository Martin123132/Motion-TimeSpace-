from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1043-R10-JX-Phi-alpha3-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1043_JX_PHI_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1043_0_1042_next",
            "source-intake/mts_residuals/P8_Y5_R10_1042_NEXT_TARGET.csv",
            "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
            "1042 handoff naming the J_X/Phi_boundary premise target.",
        ),
        (
            "SRC1043_1_1042_nohair_identity",
            "source-intake/mts_residuals/P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
            "NH1042_1_energy_identity",
            "Energy identity whose right-hand side must be zero.",
        ),
        (
            "SRC1043_2_1042_source_zero",
            "source-intake/mts_residuals/P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv",
            "SZ1042_5_verdict",
            "Prior channel audit saying total J_X=0 is not signed.",
        ),
        (
            "SRC1043_3_1042_phi_first_fill",
            "source-intake/mts_residuals/P8_Y5_R10_1042_BOUNDARY_FLUX_PRIOR_FIRST_FILL.csv",
            "PBF1042_0_Phi_boundary_local_definition",
            "Boundary flux definition and alpha3 bound rule.",
        ),
        (
            "SRC1043_4_1039_proper_boundary",
            "source-intake/mts_residuals/P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
            "QK1039_6_verdict",
            "Narrow proper compact representative boundary-zero sublemma.",
        ),
        (
            "SRC1043_5_579_contract",
            "source-intake/mts_residuals/P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
            "PXC579_4_hidden_source_silence",
            "Hidden source silence contract for boundary/projector/memory/domain channels.",
        ),
        (
            "SRC1043_6_parent_action_terms",
            "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "A7_bulk_X_nohair_or_curve",
            "Parent action term owner contract for bulk X no-hair or executable curve.",
        ),
        (
            "SRC1043_7_min_parent",
            "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "A511_3_extra_field_silence",
            "Minimal parent-action extra-field silence requirement.",
        ),
        (
            "SRC1043_8_energy_identity",
            "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "E506_memory_kernel_silence",
            "Existing source-free positive operator and memory silence templates.",
        ),
        (
            "SRC1043_9_boundary_prior_1041",
            "source-intake/mts_residuals/P8_Y5_R10_1041_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
            "BCP1041_1_Phi_boundary_local",
            "Earlier Phi_boundary_local prior schema.",
        ),
        (
            "SRC1043_10_alpha3_projection_1040",
            "source-intake/mts_residuals/P8_Y5_R10_1040_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
            "A3P1040_0_formula",
            "Alpha3 projection formula K_boundary_alpha3 * Phi_boundary_local.",
        ),
        (
            "SRC1043_11_local_alpha3_bound",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R7_alpha3",
            "Will alpha3 bound anchor.",
        ),
        (
            "SRC1043_12_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve used only for runner schema smoke.",
        ),
        (
            "SRC1043_13_R10_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 runner and schema contract.",
        ),
        (
            "SRC1043_14_970_JX_decomposition",
            "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "QMA970_3_source_silence",
            "Previous J_X source decomposition with source/boundary/history blockers.",
        ),
        (
            "SRC1043_15_973_source_free_lemma",
            "source-intake/mts_residuals/P8_Y5_R10_973_SOURCE_FREE_SXKIN_LEMMA.csv",
            "SFL973_5_hidden_source_counterexamples",
            "Hidden source counterexamples to source-free kinetic assumptions.",
        ),
        (
            "SRC1043_16_977_constant_source",
            "source-intake/mts_residuals/P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "CSC977_7_verdict",
            "Conditional source-current universality certificate.",
        ),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def jx_zero_channel_rows() -> list[dict[str, str]]:
    rows = [
        {
            "channel_id": "JX1043_0_matter_pullback",
            "channel": "ordinary matter and constants",
            "j_component": "J_matter",
            "zero_condition": "S_matter = S_matter[Psi, hat_g(q(Phi)), theta0] with partial_X hat_g = 0 and partial_X theta0 = 0 before variation/readout.",
            "attempted_derivation": "Chain rule gives delta_X S_matter = (delta S/delta hat_g) partial_X hat_g + sum_A (partial S/partial theta_A) partial_X theta_A, so this term is zero only if the observed geometry and constants are parent X-blind.",
            "current_status": "CONDITIONAL_CHAIN_RULE_READY_PARENT_UNSIGNED",
            "residual_if_open": "qbar_XT; WEP source charge; clocks; R10 test charge",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "channel_id": "JX1043_1_boundary_worldtube",
            "channel": "boundary and source worldtube",
            "j_component": "J_boundary + J_edge",
            "zero_condition": "Q_edge, B_X, and finite source-worldtube flux vanish or are orthogonal to the measured-mass/source projector.",
            "attempted_derivation": "1039 proves only proper compact representative boundary silence; it does not kill source worldtubes, large transformations, reference subtraction, or range-kernel edge projections.",
            "current_status": "OPEN_BOUNDARY_OWNER_NOT_PARENT_SIGNED",
            "residual_if_open": "Phi_boundary_local; K_boundary_alpha3; Qbar_edge_XH(lambda)",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "channel_id": "JX1043_2_projector_domain",
            "channel": "projector and domain selector",
            "j_component": "J_projector + J_domain",
            "zero_condition": "Projector/domain sector is topological, first-class, or positive source-free with no local preferred-frame/vector/stress projection.",
            "attempted_derivation": "The corpus has strong contracts for topological or positive source-free silence, but the selector/projector owner and no-vector/no-stress theorems remain unsigned.",
            "current_status": "OPEN_PROJECTOR_DOMAIN_SOURCE",
            "residual_if_open": "alpha1; alpha2; alpha3; xi; R10 domain tail; R11 operator leakage",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "channel_id": "JX1043_3_memory_history",
            "channel": "memory and history kernel",
            "j_component": "J_memory",
            "zero_condition": "Compact-local memory kernel is causal, stable, source-free, and relaxes to a constant universal calibration or zero profile in local stationary domains.",
            "attempted_derivation": "Positive-kernel/Lyapunov templates exist, but nonlocal history injection and source-memory couplings have not been excluded by parent variation.",
            "current_status": "OPEN_MEMORY_SOURCE",
            "residual_if_open": "Gdot; alpha3; R10 memory tail; local clock/source drift",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "channel_id": "JX1043_4_source_normalization",
            "channel": "measured source normalization",
            "j_component": "J_source_norm",
            "zero_condition": "The measured source mass/current Pi_M is orthogonal to X hair, or measured GM uses exactly the same parent charge that sources the local metric.",
            "attempted_derivation": "Source-current universality has a conditional certificate, but the source projector, reference subtraction, and non-Hilbert current equality are still not parent-owned.",
            "current_status": "OPEN_SOURCE_MEASURE",
            "residual_if_open": "Qbar_XH; M_H_ref; PPN source normalization; Newtonian GM drift",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "channel_id": "JX1043_5_constants_coupling",
            "channel": "constants and coupling labels",
            "j_component": "J_constants",
            "zero_condition": "kappa, theta_A, material labels, and calibration constants are global/superselected or X-blind before readout.",
            "attempted_derivation": "The one-kappa/constant-source route is structurally useful, but it does not by itself eliminate hidden matter markers, boundary flux, or shifted X-origin counterexamples.",
            "current_status": "CONDITIONAL_CERTIFICATE_READY_PARENT_UNSIGNED",
            "residual_if_open": "qbar_XT; clock redshift; WEP; source-charge R10 response",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "channel_id": "JX1043_6_verdict",
            "channel": "total J_X",
            "j_component": "J_X = J_matter + J_boundary + J_projector + J_domain + J_memory + J_source_norm + J_constants",
            "zero_condition": "Every channel above vanishes by parent identity, or every nonzero channel has its own absolute bound; no post-fit cancellation is allowed.",
            "attempted_derivation": "The structural decomposition is now clean, but not one unified parent identity signs every channel to zero.",
            "current_status": "FAIL_CURRENT_CLAIM_TOTAL_JX_ZERO_NOT_SIGNED",
            "residual_if_open": "positive-X no-hair branch cannot claim local GR; finite residual rows remain required",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def phi_boundary_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "phi_id": "PHIB1043_0_proper_compact_rep",
            "phi_component": "Phi_X^proper",
            "zero_condition": "Representative X generator and all finite jets entering the boundary density vanish on an open boundary collar.",
            "attempted_derivation": "By the 1039 finite-jet argument, proper compact representative transformations give Q_X=0 and K_boundary=0 in the narrow sub-branch.",
            "current_status": "DERIVED_NARROW_SUBBRANCH_NONCLAIM",
            "residual_if_open": "does not cover physical source worldtubes, large charges, reference subtraction, or R10 support",
            "theorem_zero_ready": "true_narrow_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHIB1043_1_edge_worldtube",
            "phi_component": "Phi_edge + Phi_worldtube",
            "zero_condition": "Physical source/test worldtube edge flux either vanishes by parent boundary class or is orthogonal to source normalization.",
            "attempted_derivation": "No parent boundary class currently proves this for finite source/test support.",
            "current_status": "OPEN_SOURCE_EDGE_FLUX",
            "residual_if_open": "K_boundary_alpha3 Phi_boundary_local; R10 edge charge",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHIB1043_2_reference_subtraction",
            "phi_component": "Phi_ref + Phi_ct",
            "zero_condition": "Reference subtraction/counterterm is fixed, topological, or cancels only unphysical representative terms without deleting GR charges.",
            "attempted_derivation": "1039 keeps the GR-charge guard; the exact parent reference map is still unsigned.",
            "current_status": "OPEN_REFERENCE_OWNER",
            "residual_if_open": "source mass shift; beta/gamma/alpha3 boundary rows",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHIB1043_3_corner_harmonic_topology",
            "phi_component": "Phi_corner + Phi_harmonic",
            "zero_condition": "No corner, harmonic, or topological class contributes to local compact exterior X hair.",
            "attempted_derivation": "Topological silence is available as a contract but not as a parent theorem for the active local branch.",
            "current_status": "OPEN_TOPOLOGY_GATE",
            "residual_if_open": "preferred-frame/domain leakage; nonzero boundary hair",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHIB1043_4_memory_kernel_boundary",
            "phi_component": "Phi_kernel",
            "zero_condition": "Local memory/history boundary injection is absent, screened, or constant-universal in compact stationary domains.",
            "attempted_derivation": "The memory energy identity identifies the route, but history injection is still an open source channel.",
            "current_status": "OPEN_MEMORY_BOUNDARY",
            "residual_if_open": "Gdot; alpha3; R10 memory tail",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHIB1043_5_source_measure_boundary",
            "phi_component": "Phi_source_norm",
            "zero_condition": "Boundary flux used in measured GM is the same Hilbert/GR source current, or the X piece is exactly orthogonal.",
            "attempted_derivation": "Source normalization equality remains open even if proper representative X charges vanish.",
            "current_status": "OPEN_SOURCE_MEASURE_BOUNDARY",
            "residual_if_open": "M_eff drift; Qbar_XH; PPN source normalization",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHIB1043_6_verdict",
            "phi_component": "Phi_boundary_local total",
            "zero_condition": "All Phi components vanish channelwise, or every nonzero piece has its own source-backed absolute bound.",
            "attempted_derivation": "Only the proper compact representative sub-branch is actually derived; the physical boundary/source terms remain open.",
            "current_status": "FAIL_CURRENT_CLAIM_PHI_BOUNDARY_ZERO_NOT_SIGNED",
            "residual_if_open": "alpha3 prior stays value-missing; local GR/no-hair pass remains blocked",
            "theorem_zero_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def rhs_zero_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "RHS1043_0_definition",
            "expression": "R_X := int_A X J_X dV + Phi_boundary_local",
            "required": "R_X=0 follows from J_X=0 and Phi_boundary_local=0 channelwise, not from numerical cancellation.",
            "current_status": "STRUCTURAL_GATE_WRITTEN",
            "gate_pass": "false",
            "claim_allowed": "false",
            "no_cancellation_policy": "active",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RHS1043_1_JX_zero",
            "expression": "int_A X J_X dV",
            "required": "all J_X channels theorem-zero, or bounded absolutely before scoring",
            "current_status": "blocked_by_JX1043_6",
            "gate_pass": "false",
            "claim_allowed": "false",
            "no_cancellation_policy": "J channels must pass independently unless a parent identity forces cancellation before variation/readout",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RHS1043_2_Phi_zero",
            "expression": "Phi_boundary_local",
            "required": "all boundary/source/reference/kernel/topology pieces theorem-zero, or bounded absolutely",
            "current_status": "blocked_by_PHIB1043_6",
            "gate_pass": "false",
            "claim_allowed": "false",
            "no_cancellation_policy": "Phi cannot be hidden by J_X cancellation or by deleting GR charges",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RHS1043_3_no_cancellation",
            "expression": "int_A X J_X dV + Phi_boundary_local",
            "required": "do not use fitted sign cancellation between hidden source and boundary flux",
            "current_status": "GUARD_RETAINED",
            "gate_pass": "false",
            "claim_allowed": "false",
            "no_cancellation_policy": "channelwise theorem-zero or channelwise absolute bounds only",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RHS1043_4_verdict",
            "expression": "positive-X no-hair right-hand side",
            "required": "J_X=0, Phi_boundary_local=0, topology/zero-mode gate, and parent positive operator",
            "current_status": "R_X_ZERO_BLOCKED_CURRENT_CORPUS",
            "gate_pass": "false",
            "claim_allowed": "false",
            "no_cancellation_policy": "local GR/no-hair pass remains unavailable",
            "generated_utc": stamp(),
        },
    ]


def alpha3_phi_prior_value_rows() -> list[dict[str, str]]:
    return [
        {
            "phi_id": "PHI1043_0_theorem_zero_candidate",
            "symbol": "Phi_boundary_local",
            "value": "0_IF_PHI_ZERO_THEOREM_SIGNED",
            "units": "dimensionless_after_declared_PPN_projection",
            "normalization": "same observed frame, source normalization, boundary collar, and GR-charge guard as the alpha3 row",
            "source_path": "MISSING_PARENT_PHI_ZERO_CERTIFICATE",
            "theorem_zero_path": "source-intake/mts_residuals/P8_Y5_R10_1043_PHI_BOUNDARY_ZERO_CHANNEL_AUDIT.csv::PHIB1043_6",
            "alpha3_bound": "4e-20",
            "K_bound_rule": "if Phi_boundary_local=0 by theorem, alpha3_boundary=0 independent of K_boundary_alpha3 within the theorem domain",
            "status": "THEOREM_ZERO_CANDIDATE_BLOCKED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHI1043_1_numeric_prior_placeholder",
            "symbol": "Phi_boundary_local",
            "value": "MISSING_NUMERIC_PHI_BOUNDARY_LOCAL",
            "units": "MISSING_UNITS",
            "normalization": "MISSING_SOURCE_NORMALIZATION_AND_SURFACE_MEASURE",
            "source_path": "MISSING_SOURCE_FILE",
            "theorem_zero_path": "not_applicable_numeric_route",
            "alpha3_bound": "4e-20",
            "K_bound_rule": "for nonzero sourced Phi, require |K_boundary_alpha3| <= 4e-20/|Phi_boundary_local| and then score alpha3_boundary independently",
            "status": "NUMERIC_VALUE_TEMPLATE_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "phi_id": "PHI1043_2_guard_no_cancellation",
            "symbol": "Phi_boundary_local",
            "value": "not_a_numeric_value",
            "units": "policy",
            "normalization": "all active channels must be individually zero or absolutely bounded",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1043_RIGHT_HAND_SIDE_ZERO_GATE.csv::RHS1043_3_no_cancellation",
            "theorem_zero_path": "guard_only",
            "alpha3_bound": "4e-20",
            "K_bound_rule": "do not combine Phi with opposite-sign J_X or sibling boundary/domain residuals to pass alpha3",
            "status": "NO_CANCELLATION_GUARD_RETAINED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def residual_if_open_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "RIO1043_0_matter",
            "blocker": "J_matter not parent-zero",
            "residual_formula": "qbar_XT = M_T^-1 delta_X S_T",
            "affected_tests": "WEP; R10; clocks; composition source charge",
            "bound_route": "derive matter pullback qbar_XT=0 or fill qbar_XT bound row",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "RIO1043_1_boundary",
            "blocker": "Phi_boundary_local not parent-zero",
            "residual_formula": "alpha3_boundary = K_boundary_alpha3 Phi_boundary_local",
            "affected_tests": "alpha3; beta/gamma boundary; Gdot; R10 edge",
            "bound_route": "derive boundary no-flux or source Phi and K_boundary_alpha3",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "RIO1043_2_domain_projector",
            "blocker": "projector/domain source not parent-zero",
            "residual_formula": "alpha_i_domain = W_i epsilon_domain and/or alpha_R10 = K_X Qbar_XH qbar_XT",
            "affected_tests": "PPN alpha1/alpha2/alpha3/xi; R10; R11",
            "bound_route": "derive no-vector/no-stress topological selector or fill coefficients",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "RIO1043_3_memory",
            "blocker": "memory/history source not parent-zero",
            "residual_formula": "finite memory tail enters J_X or Phi_kernel",
            "affected_tests": "Gdot; clocks; alpha3; R10",
            "bound_route": "derive compact-local memory silence or fill tail amplitude",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "JX_Phi_alpha3_template",
            "curve_id": "MTS_1043_JX_PHI_ALPHA3_TEMPLATE",
            "lambda_value": "MISSING_NOT_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL",
            "alpha_bound": "4e-20",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R7_alpha3",
            "force_law_form": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local; Phi_boundary_local is blocked by PHIB1043_6",
            "derivation_status": "template_invalid_JX_and_Phi_zero_premises_missing",
            "formula_reference": "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md::PHI1043_1",
            "source_file": "MISSING_PHI_OR_K_SOURCE_FILE",
            "assumptions": "private nonclaim template; no cancellation; no local-GR pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject this row until K_boundary_alpha3, Phi_boundary_local, units, and source paths are real.",
        },
        {
            "model_id": "MTS_positive_X_nohair_branch",
            "branch_id": "JX_zero_gate_template",
            "curve_id": "MTS_1043_POSITIVE_X_RIGHT_HAND_SIDE_TEMPLATE",
            "lambda_value": "MISSING_X_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_GREEN_FUNCTION_AMPLITUDE_FROM_NONZERO_JX_OR_PHI",
            "alpha_bound": "MISSING_BOUND_SELECTION",
            "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_1043_RIGHT_HAND_SIDE_ZERO_GATE.csv::RHS1043_4_verdict",
            "force_law_form": "if R_X is nonzero, finite positive-X branch must be mapped to alpha_X(lambda_X)",
            "derivation_status": "template_invalid_RHS_ZERO_GATE_BLOCKED",
            "formula_reference": "1042 energy identity plus 1043 RHS gate",
            "source_file": "MISSING_PARENT_LX_JX_PHI_SOURCE_FILE",
            "assumptions": "diagnostic only",
            "valid_for_claim": "false",
            "notes": "No R10 or local-GR claim can be made from this placeholder.",
        },
    ]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1043_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject placeholders and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def placeholder_refusal_rows(
    jx_rows: list[dict[str, str]],
    phi_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    jx_blockers = [row["channel_id"] for row in jx_rows if row["channel_id"] != "JX1043_6_verdict" and row["theorem_zero_ready"] == "false"]
    phi_blockers = [row["phi_id"] for row in phi_rows if row["phi_id"] != "PHIB1043_6_verdict" and row["theorem_zero_ready"] == "false"]
    return [
        {
            "refusal_id": "REF1043_0_total_JX",
            "object": "J_X=0",
            "current_status": "FAIL_CURRENT_CLAIM_TOTAL_JX_ZERO_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(jx_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1043_1_total_Phi",
            "object": "Phi_boundary_local=0",
            "current_status": "FAIL_CURRENT_CLAIM_PHI_BOUNDARY_ZERO_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(phi_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1043_2_alpha3_phi_value",
            "object": "alpha3_MTS=K_boundary_alpha3 Phi_boundary_local",
            "current_status": "NUMERIC_VALUE_TEMPLATE_ONLY",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(row["phi_id"] for row in alpha3_rows if row["score_ready"] == "false"),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1043_3_R10_runner",
            "object": "R10 placeholder smoke rows",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": "valid_mts_rows=" + smoke_rows[0]["valid_mts_rows"],
            "score_eligible": "false",
            "claim_allowed": smoke_rows[0]["claim_allowed"],
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1043_0_positive_X_nohair",
            "claim": "positive-X theorem proves local compact X=0",
            "gate_pass": "false",
            "reason": "J_X and Phi_boundary_local zero premises are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1043_1_local_GR_reduction",
            "claim": "local-GR/R10 branch passes by theorem",
            "gate_pass": "false",
            "reason": "right-hand side zero gate and topology/source-normalization gates remain blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1043_2_alpha3_score",
            "claim": "alpha3_MTS is scoreable against 4e-20",
            "gate_pass": "false",
            "reason": "K_boundary_alpha3 and Phi_boundary_local numeric/theorem-zero source paths are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1043_3_R10_smoke",
            "claim": "R10 fifth-force branch passes",
            "gate_pass": "false",
            "reason": "MTS rows are placeholders and bound candidate remains nonclaim review data",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1043_0_structural_result",
            "decision": "right-hand side zero condition is now exact",
            "because": "R_X = int_A X J_X dV + Phi_boundary_local must be killed channelwise before no-hair/local-GR can be claimed",
            "next_action": "prove the most local source-zero channel first",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1043_1_derivation_attempt",
            "decision": "J_X=0 and Phi_boundary_local=0 are not yet proved",
            "because": "proper compact representative boundary silence is useful but does not cover matter pullback, source worldtubes, projector/domain, memory, or source normalization",
            "next_action": "do not promote positive-X no-hair; keep residual rows live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1043_2_fallback",
            "decision": "alpha3 Phi prior value template written but value missing",
            "because": "the observable anchor exists at 4e-20, but MTS-side Phi and K are unsourced",
            "next_action": "derive Phi=0 or source Phi/K numerically before any alpha3 score",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1043_3_best_next",
            "decision": "target ordinary matter pullback first",
            "because": "it is the cleanest chain-rule theorem and would remove qbar_XT/WEP/clock/R10 test-charge pressure without touching boundary flux",
            "next_action": "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
            "objective": "try to prove ordinary matter and constants pull back only through X-blind observed geometry so J_matter=0 and qbar_XT=0; if this fails, build a nonclaim qbar_XT source-charge bound row",
            "include": "chain-rule matter variation, quotient descent, test-body action, constants/kappa/theta labels, WEP/R10/clock links, no-marker counterexamples",
            "exclude": "closure postulate, deleting physical source charge, cancellation with boundary/domain terms, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    jx_rows: list[dict[str, str]],
    phi_rows: list[dict[str, str]],
    rhs_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1043_1_sources_exist_and_needles",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "every cited source path exists and every source needle was found",
        )
    )
    expected_jx = {
        "ordinary matter and constants",
        "boundary and source worldtube",
        "projector and domain selector",
        "memory and history kernel",
        "measured source normalization",
        "constants and coupling labels",
        "total J_X",
    }
    checks.append(
        (
            "V1043_2_jx_channels_blocked",
            expected_jx.issubset({row["channel"] for row in jx_rows})
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_TOTAL_JX_ZERO_NOT_SIGNED" for row in jx_rows)
            and all(not flag(row["valid_for_claim"]) for row in jx_rows),
            "J_X channel audit is complete enough and keeps total J_X=0 blocked",
        )
    )
    checks.append(
        (
            "V1043_3_phi_channels_blocked",
            any(row["phi_id"] == "PHIB1043_0_proper_compact_rep" and row["current_status"] == "DERIVED_NARROW_SUBBRANCH_NONCLAIM" for row in phi_rows)
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_PHI_BOUNDARY_ZERO_NOT_SIGNED" for row in phi_rows)
            and all(not flag(row["valid_for_claim"]) for row in phi_rows),
            "Phi boundary audit preserves the useful narrow proper sublemma while blocking full Phi=0",
        )
    )
    checks.append(
        (
            "V1043_4_rhs_zero_gate_blocked",
            any(row["gate_id"] == "RHS1043_4_verdict" and row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in rhs_rows)
            and any(row["gate_id"] == "RHS1043_3_no_cancellation" and row["no_cancellation_policy"] == "channelwise theorem-zero or channelwise absolute bounds only" for row in rhs_rows),
            "R_X=0 gate is explicit and forbids cancellation",
        )
    )
    checks.append(
        (
            "V1043_5_alpha3_phi_template_nonclaim",
            any(
                row["phi_id"] == "PHI1043_1_numeric_prior_placeholder"
                and row["value"] == "MISSING_NUMERIC_PHI_BOUNDARY_LOCAL"
                and row["alpha3_bound"] == "4e-20"
                and row["score_ready"] == "false"
                and row["valid_for_claim"] == "false"
                for row in alpha3_rows
            ),
            "alpha3 Phi value template is present, source-anchored, and nonclaim",
        )
    )
    checks.append(
        (
            "V1043_6_residual_rows_nonclaim",
            len(residual_rows) >= 4 and all(row["status"] == "OPEN_NONCLAIM" and not flag(row["valid_for_claim"]) for row in residual_rows),
            "residual-if-open ledger retains affected tests without claiming a pass",
        )
    )
    checks.append(
        (
            "V1043_7_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1043_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1043 placeholder rows",
        )
    )
    checks.append(
        (
            "V1043_9_claim_gates_blocked",
            all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all local-GR/alpha3/R10 claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1043_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1043_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1043_JX_ZERO_CHANNEL_AUDIT.csv",
        OUT / "P8_Y5_R10_1043_PHI_BOUNDARY_ZERO_CHANNEL_AUDIT.csv",
        OUT / "P8_Y5_R10_1043_RIGHT_HAND_SIDE_ZERO_GATE.csv",
        OUT / "P8_Y5_R10_1043_ALPHA3_PHI_PRIOR_VALUE_TEMPLATE.csv",
        OUT / "P8_Y5_R10_1043_RESIDUAL_IF_OPEN.csv",
        OUT / "P8_Y5_R10_1043_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1043_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1043_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1043_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1043_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1043_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1043_11_generated_files_in_post_checkpoint",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_files if path.exists() or path.parent.exists()),
            "all generated files are under post-checkpoint-work",
        )
    )
    formalization_touches: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
                formalization_touches.append(path)
    checks.append(
        (
            "V1043_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1043_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1043 J_X/Phi zero premise or alpha3 prior value validation summary",
            "generated_utc": stamp(),
        }
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    return rows


def write_doc(
    source_rows: list[dict[str, str]],
    jx_rows: list[dict[str, str]],
    phi_rows: list[dict[str, str]],
    rhs_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1043 Y5 R10 J_X zero and Phi boundary zero premise or alpha3 prior value",
        "",
        "**Progress:** the no-hair right-hand side is now explicit: `R_X := int_A X J_X dV + Phi_boundary_local`. The route to local GR requires `R_X=0` channelwise, not by cancellation.",
        "",
        "**Derivation attempt:** the proper compact representative boundary sublemma survives, but the physical matter, source-worldtube, projector/domain, memory, source-normalization, and constant/coupling channels are not parent-signed to zero.",
        "",
        "**Claim ceiling:** no local-GR, R10, or alpha3 pass is made here. The alpha3 row is a value template only until `Phi_boundary_local`, `K_boundary_alpha3`, units, normalization, and source paths are real or theorem-zero.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## J_X zero channel audit",
        md_table(jx_rows, ["channel_id", "channel", "j_component", "zero_condition", "current_status", "residual_if_open", "theorem_zero_ready", "valid_for_claim"]),
        "## Phi boundary zero channel audit",
        md_table(phi_rows, ["phi_id", "phi_component", "zero_condition", "current_status", "residual_if_open", "theorem_zero_ready", "valid_for_claim"]),
        "## Right-hand-side zero gate",
        md_table(rhs_rows, ["gate_id", "expression", "required", "current_status", "gate_pass", "claim_allowed", "no_cancellation_policy"]),
        "## Alpha3 Phi prior value template",
        md_table(alpha3_rows, ["phi_id", "symbol", "value", "units", "source_path", "alpha3_bound", "K_bound_rule", "status", "score_ready", "valid_for_claim"]),
        "## Residual if open",
        md_table(residual_rows, ["residual_id", "blocker", "residual_formula", "affected_tests", "bound_route", "status", "valid_for_claim"]),
        "## MTS alpha smoke template",
        md_table(mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
        "## Runner smoke status",
        md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
        "## Next target",
        md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    jx_rows = jx_zero_channel_rows()
    phi_rows = phi_boundary_zero_rows()
    rhs_rows = rhs_zero_gate_rows()
    alpha3_rows = alpha3_phi_prior_value_rows()
    residual_rows = residual_if_open_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(jx_rows, phi_rows, alpha3_rows, smoke_rows)
    claim_rows_ = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        jx_rows,
        phi_rows,
        rhs_rows,
        alpha3_rows,
        residual_rows,
        mts_rows,
        smoke_rows,
        claim_rows_,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1043_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1043_JX_ZERO_CHANNEL_AUDIT.csv", jx_rows)
    write_csv(OUT / "P8_Y5_R10_1043_PHI_BOUNDARY_ZERO_CHANNEL_AUDIT.csv", phi_rows)
    write_csv(OUT / "P8_Y5_R10_1043_RIGHT_HAND_SIDE_ZERO_GATE.csv", rhs_rows)
    write_csv(OUT / "P8_Y5_R10_1043_ALPHA3_PHI_PRIOR_VALUE_TEMPLATE.csv", alpha3_rows)
    write_csv(OUT / "P8_Y5_R10_1043_RESIDUAL_IF_OPEN.csv", residual_rows)
    write_csv(OUT / "P8_Y5_R10_1043_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1043_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1043_CLAIM_GATES.csv", claim_rows_)
    write_csv(OUT / "P8_Y5_R10_1043_DECISION_LEDGER.csv", decision_rows_)
    write_csv(OUT / "P8_Y5_R10_1043_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1043_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        jx_rows,
        phi_rows,
        rhs_rows,
        alpha3_rows,
        residual_rows,
        mts_rows,
        smoke_rows,
        refusal_rows,
        claim_rows_,
        decision_rows_,
        validation,
        next_rows,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1043 validation failed: {failed}")


if __name__ == "__main__":
    main()
