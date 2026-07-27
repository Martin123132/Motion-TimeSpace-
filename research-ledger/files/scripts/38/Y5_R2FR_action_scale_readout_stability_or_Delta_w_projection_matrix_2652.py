from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2652"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2652-Y5-R2FR-action-scale-readout-stability-or-Delta-w-projection-matrix.md"

CHECKPOINT = "2652"
BRANCH_ID = "Y5_R2FR_ACTION_SCALE_READOUT_OR_DELTAW_MATRIX_2652"
PREFIX = "P8_Y5_ASR_DELTAW_MATRIX_2652"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "stability_attempt": RESIDUALS / f"{PREFIX}_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
    "stability_gate": RESIDUALS / f"{PREFIX}_STABILITY_GATE.csv",
    "projection_matrix": RESIDUALS / f"{PREFIX}_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "projection_requirements": RESIDUALS / f"{PREFIX}_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_STABILITY_PROJECTION_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_STABILITY_PROJECTION_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2652_DELTAW_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Delta_w_projection_matrix_2652_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "DELTAW_ARENA_PROJECTION_MATRIX_2652_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2652_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2652_STABILITY_PROJECTION_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2651_doc": {
        "path": ROOT / "2651-Y5-R2FR-parent-sort-nohom-constructor-or-finite-Delta-w-basis.md",
        "needles": ["NH2651_5_verdict", "DWB2651_9_acceptance", "NEXT2651_0_selected"],
        "role": "immediate hard-fork handoff into stability/matrix branch",
    },
    "2650_doc": {
        "path": ROOT / "2650-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md",
        "needles": ["NSP2650_4_action_scale_measure_gap", "PMTB2650_6_acceptance"],
        "role": "action-scale owner and material-basis blocker",
    },
    "2647_doc": {
        "path": ROOT / "2647-Y5-R2FR-ordinary-matter-action-signature-or-Delta-w-projection-kernels.md",
        "needles": ["OMC2647_7_verdict", "DK2647_1_WEP", "DK2647_3_PPN"],
        "role": "projection kernel stubs across arenas",
    },
    "2648_doc": {
        "path": ROOT / "2648-Y5-R2FR-source-functor-label-forgetting-or-Delta-w-WEP-kernel-v0.md",
        "needles": ["SFL2648_5_verdict", "WEPK2648_5_acceptance"],
        "role": "WEP kernel v0 refusal and source-label forgetting gap",
    },
    "1066_doc": {
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["FMQ1066_4_verdict", "TWP1066_7_verdict"],
        "role": "action-scale/measure and tau projection debt",
    },
    "1225_doc": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["TAU1225_6_verdict", "ACQ1225_0_official_readout_arrays", "ACQ1225_5_delta_w"],
        "role": "tau/source-worldtube/readout missing-source ledger",
    },
    "1897_doc": {
        "path": ROOT / "1897-Y5-R2FR-action-scale-readout-stability-or-deltaw-projection-matrix.md",
        "needles": ["ASR1897_6_verdict", "DPM1897_0_core_vector", "VAL1897_OVERALL"],
        "role": "older action-scale/readout-stability analogue",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    generated = now()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2652_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def stability_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "ASR2652_0_target",
            "claim_piece": "action-scale/readout stability after tree-level no-Hom",
            "formal_statement": "After parent variation, no measure, radiative, readout, material, source-worldtube, clock, orbital or laboratory map can create Coeff_active_source[species] terms if every such map is a domain-preserving postprocessing functor.",
            "status": "TARGET_EXACT",
            "proof_or_obstruction": "this is the theorem needed so source weights do not come back after the 2651 no-Hom branch",
            "source_anchor": "2651:NH2651_4_action_scale_readout_stability;1897:ASR1897_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ASR2652_1_exact_conditional_theorem",
            "claim_piece": "one-owner stability theorem",
            "formal_statement": "If S_parent has one hbar/action-measure owner, one current/source normalization owner, variation occurs before all readouts, and every readout/effective map preserves the quotient coefficient domain, then D_label R(C_source)=0 and Delta_w tree-zero is stable.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "composition of coefficient-domain-preserving maps cannot enlarge the argument domain to SpeciesLabel",
            "source_anchor": "1066:FMQ1066_4_verdict;1225:TAU1225_6_verdict;1897:ASR1897_1_exact_conditional_theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ASR2652_2_action_scale_gap",
            "claim_piece": "single action scale / measure owner",
            "formal_statement": "hbar_parent, Dmu_parent, current normalization and source normalization must be owned by one parent sector and must not admit species-only Jacobians.",
            "status": "ACTION_SCALE_OWNER_UNSIGNED",
            "proof_or_obstruction": "relative action-scale factors remain a live countermodel and can mimic Delta_w_measure",
            "source_anchor": "2650:NSP2650_4_action_scale_measure_gap;2651:DWB2651_4_action_measure_jacobian",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ASR2652_3_readout_gap",
            "claim_piece": "readout no-reentry",
            "formal_statement": "[delta_parent, R_readout] must not produce source-only coefficient terms; if nonzero, the commutator is a finite residual transfer row.",
            "status": "READOUT_NO_REENTRY_UNSIGNED",
            "proof_or_obstruction": "readout domain separation is conditional and source-worldtube/readout arrays are not imported",
            "source_anchor": "1225:ACQ1225_0_official_readout_arrays;1897:ASR1897_3_readout_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ASR2652_4_radiative_gap",
            "claim_piece": "radiative/effective closure",
            "formal_statement": "S_eff, thresholds, clocks, WEP/R10 kernels and laboratory readouts must preserve the no-species coefficient grammar after coarse-graining.",
            "status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "proof_or_obstruction": "conditional domain preservation is not enough without the observed-lab bridge",
            "source_anchor": "1897:ASR1897_4_radiative_gap;2647:OMC2647_7_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ASR2652_5_variation_order_gap",
            "claim_piece": "variation before readout/source-worldtube",
            "formal_statement": "post-current c_A and selector F(T_A,A) are killed only if they are downstream of Hilbert/Noether source extraction and cannot enter S_parent or S_eff before variation.",
            "status": "VARIATION_BEFORE_READOUT_UNSIGNED",
            "proof_or_obstruction": "post-current/readout factors are conditionally downstream, but pre-action weights and source-worldtube transfers remain live",
            "source_anchor": "2648:SFL2648_5_verdict;1225:ACQ1225_2_source_worldtube",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "ASR2652_6_verdict",
            "claim_piece": "promote stable source-weight zero",
            "formal_statement": "Current MTS parent primitives prove one-owner action scale plus readout/effective no-reentry, so Delta_w=0 is stable across local arenas.",
            "status": "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the exact theorem is sharp, but action-scale owner, readout no-reentry, radiative closure, variation-order/worldtube split and parent Delta_w values are unsigned; finite projection matrix branch remains mandatory",
            "source_anchor": "ASR2652_0_target through ASR2652_5_variation_order_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def stability_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "STG2652_0_action_owner", "required_clause": "single parent hbar/action-measure/current owner", "current_status": "FAIL_OWNER_NOT_DERIVED", "if_pass": "relative pre-action source weights become removable/common-mode only", "if_fail": "Delta_w_species, Delta_w_measure and c_A_current_rescale remain live components", "source_anchor": "ASR2652_2_action_scale_gap", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "STG2652_1_variation_order", "required_clause": "variation-before-readout and source-worldtube maps are downstream only", "current_status": "FAIL_CONDITIONAL_THEOREM_NOT_CURRENT_PROOF", "if_pass": "post-current c_A and selector F(T_A,A) are readout/calibration only", "if_fail": "source-worldtube and selector transfer rows stay finite", "source_anchor": "ASR2652_5_variation_order_gap", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "STG2652_2_readout_no_reentry", "required_clause": "[delta_parent, R_readout] has no source-coefficient codomain", "current_status": "FAIL_READOUT_STABILITY_NOT_PARENT_DERIVED", "if_pass": "downstream readouts cannot regenerate w_A", "if_fail": "readout-transfer projection coefficients remain explicit", "source_anchor": "ASR2652_3_readout_gap", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "STG2652_3_radiative_closure", "required_clause": "loops, thresholds, EFT and lab observables preserve quotient coefficient domains", "current_status": "FAIL_RADIATIVE_READOUT_CLOSURE_UNSIGNED", "if_pass": "effective/readout channels do not create hidden/species source coefficients", "if_fail": "R10/WEP/clock/PPN projection rows remain symbolic/nonclaim", "source_anchor": "ASR2652_4_radiative_gap", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "STG2652_4_parent_values", "required_clause": "finite Delta_w components have parent values or theorem-zero signatures", "current_status": "FAIL_PARENT_DELTAW_VALUES_MISSING", "if_pass": "arena matrix can become prediction runner input", "if_fail": "matrix is schema only and must refuse scoring", "source_anchor": "2651:DWB2651_9_acceptance", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "STG2652_5_verdict", "required_clause": "stable source-weight zero or numeric finite Delta_w projection can be claimed", "current_status": "CLAIM_BLOCKED", "if_pass": "move to local-GR/R10/WEP scoring", "if_fail": "move to commutator proof or first WEP projection row v1", "source_anchor": "STG2652_0_action_owner through STG2652_4_parent_values", "gate_pass": False, "valid_for_claim": False},
    ]


def projection_matrix_rows() -> list[dict[str, Any]]:
    return [
        {"matrix_id": "DPM2652_0_core_vector", "arena": "core_component_vector", "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; Delta_w_measure; J_NH_retained; Delta_mu_projector; R_material_X", "projection_formula": "Delta_w_eff=P_perp(Delta_w_species+c_A_current_rescale+Delta_w_marker_hidden+Delta_w_measure)+retained current/projector/material legs", "required_inputs": "parent component values; common-mode projector; material/source basis; norm; no-cancellation envelope", "current_status": "SYMBOLIC_MATRIX_ONLY_PARENT_VALUES_MISSING", "source_anchor": "2651:DWB2651_0_vector_space", "units": "dimensionless or declared per current channel", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"matrix_id": "DPM2652_1_WEP_MICROSCOPE", "arena": "WEP_MICROSCOPE_TiPt", "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; Delta_w_measure; J_NH_retained; R_material_X", "projection_formula": "eta_TiPt=tau_WEP * K_WEP[Ti,Pt,Earth,readout] dot Delta_w_eff", "required_inputs": "official Ti/Pt material tensor; Earth/source worldtube; tau_WEP; force/readout convention; parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_AND_PARENT_VALUES_MISSING", "source_anchor": "2651:PRJ2651_0_WEP;1225:ACQ1225_4_material_tensor", "units": "dimensionless eta", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"matrix_id": "DPM2652_2_R10", "arena": "R10_short_range", "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; Delta_w_measure; J_NH_retained", "projection_formula": "alpha_Delta_w(lambda)=tau_R10(lambda)*K_R10(lambda)*Qbar_source_test(lambda) dot Delta_w_eff", "required_inputs": "range kernel; source/test composition; tau_R10(lambda); K_R10(lambda); real alpha_bound(lambda); parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_RANGE_KERNEL_AND_PARENT_VALUES_MISSING", "source_anchor": "2651:PRJ2651_1_R10;1066:TWP1066_7_verdict", "units": "dimensionless alpha(lambda)", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"matrix_id": "DPM2652_3_PPN", "arena": "PPN_beta_gamma_source", "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; Delta_w_measure; J_NH_retained; Delta_mu_projector", "projection_formula": "[Delta gamma, Delta beta, alpha_i, xi]_source=M_PPN dot Delta_w_eff + retained source/test legs", "required_inputs": "weak-field solution; PPN operator matrix; source/test split; parent Delta_w_eff; GR limit matching", "current_status": "KERNEL_STUB_NONCLAIM_OPERATOR_MATRIX_AND_GR_LIMIT_MISSING", "source_anchor": "2651:PRJ2651_2_PPN;2647:DK2647_3_PPN", "units": "dimensionless PPN deviations", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"matrix_id": "DPM2652_4_clock", "arena": "clock_and_constant_drift", "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; Delta_w_measure; J_NH_retained", "projection_formula": "Delta ln nu_i=K_clock_i dot Delta_w_eff + retained alpha/mass/readout coefficients", "required_inputs": "clock sensitivity vector; alpha/mass split; source body composition; tau_clock; parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_CLOCK_SENSITIVITY_AND_PARENT_VALUES_MISSING", "source_anchor": "2651:PRJ2651_3_clock;2647:DK2647_4_clock", "units": "dimensionless frequency shift or drift", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"matrix_id": "DPM2652_5_orbital", "arena": "orbital_GM_inverse_square", "components": "Delta_w_species; c_A_current_rescale; Delta_w_marker_hidden; Delta_w_measure; J_NH_retained; Delta_mu_projector", "projection_formula": "Delta ln(GM)_obs=K_orbital dot Delta_w_eff + retained finite-range/source-test/projector terms", "required_inputs": "source body composition; orbital GM convention; inverse-square kernel; tau_orbital; parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_ORBITAL_SOURCE_MAP_AND_PARENT_VALUES_MISSING", "source_anchor": "2651:PRJ2651_4_orbital;2651:DWB2651_6_mass_projector", "units": "dimensionless GM/source deviation", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"matrix_id": "DPM2652_6_no_cancellation_policy", "arena": "all_local_arenas", "components": "all finite Delta_w components", "projection_formula": "use sum_i |K_arena_i Delta_w_i| or a sourced covariance envelope; fitted cancellations cannot produce a pass", "required_inputs": "parent identity for cancellation or no-cancellation envelope plus sourced covariance", "current_status": "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM", "source_anchor": "2651:DWB2651_8_no_cancellation_policy", "units": "policy", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def projection_requirement_rows() -> list[dict[str, Any]]:
    return [
        {"requirement_id": "DPR2652_0_parent_zero_or_values", "needed_for": "all projection rows", "requirement": "each Delta_w component has a parent numeric value, uncertainty/bound, or parent theorem-zero proof", "current_status": "MISSING_PARENT_DELTAW_VALUES", "source_anchor": "2651:DWB2651_9_acceptance", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "DPR2652_1_arena_tau_K", "needed_for": "WEP/R10/PPN/clock/orbital rows", "requirement": "arena-specific tau, K, material/source/readout kernels with units and source paths", "current_status": "MISSING_ARENA_PROJECTION_KERNELS", "source_anchor": "2651:PRJ2651_0_WEP through PRJ2651_4_orbital", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "DPR2652_2_readout_order", "needed_for": "post-current c_A and source-worldtube transfer", "requirement": "prove source-worldtube/readout kernels are downstream and cannot enter parent variation", "current_status": "MISSING_VARIATION_BEFORE_READOUT_SIGNATURE", "source_anchor": "ASR2652_5_variation_order_gap", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "DPR2652_3_no_reentry", "needed_for": "radiative/effective/readout leakage", "requirement": "prove [delta_parent, R_readout] has no source-only coefficient codomain, or introduce finite transfer coefficient", "current_status": "MISSING_READOUT_NO_REENTRY_PROOF", "source_anchor": "ASR2652_3_readout_gap", "blocks_claim": True, "valid_for_claim": False},
        {"requirement_id": "DPR2652_4_bound_inputs", "needed_for": "empirical comparison branch", "requirement": "real bound curves/arrays and matching model kernels before any claim-grade score", "current_status": "BOUND_ANCHOR_OR_SCHEMA_ONLY", "source_anchor": "1225:ACQ1225_0_official_readout_arrays;2651:PRJ2651_1_R10", "blocks_claim": True, "valid_for_claim": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2652_0_action_owner_unsigned", "action_owner_signed": False, "readout_stability_signed": False, "variation_order_signed": False, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_ACTION_SCALE_OWNER_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY2652_1_readout_unsigned", "action_owner_signed": True, "readout_stability_signed": False, "variation_order_signed": False, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_READOUT_STABILITY_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY2652_2_variation_unsigned", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": False, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_VARIATION_BEFORE_READOUT_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY2652_3_radiative_unsigned", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": False, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_RADIATIVE_READOUT_CLOSURE_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY2652_4_parent_values_missing", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": False, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": False, "expected_status": "REFUSED_PARENT_DELTAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2652_5_symbolic_projection", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": True, "projection_numeric": False, "uses_cancellation": False, "bound_only_anchor": False, "expected_status": "REFUSED_PROJECTION_MATRIX_SYMBOLIC", "valid_for_claim": False},
        {"case_id": "DRY2652_6_cancellation", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": True, "projection_numeric": True, "uses_cancellation": True, "bound_only_anchor": False, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
        {"case_id": "DRY2652_7_bound_anchor", "action_owner_signed": True, "readout_stability_signed": True, "variation_order_signed": True, "radiative_closure_signed": True, "parent_values_present": True, "projection_numeric": True, "uses_cancellation": False, "bound_only_anchor": True, "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION", "valid_for_claim": False},
    ]


def evaluate_dryrun(row: dict[str, Any]) -> str:
    if not row["action_owner_signed"]:
        return "REFUSED_ACTION_SCALE_OWNER_UNSIGNED"
    if not row["readout_stability_signed"]:
        return "REFUSED_READOUT_STABILITY_UNSIGNED"
    if not row["variation_order_signed"]:
        return "REFUSED_VARIATION_BEFORE_READOUT_UNSIGNED"
    if not row["radiative_closure_signed"]:
        return "REFUSED_RADIATIVE_READOUT_CLOSURE_UNSIGNED"
    if not row["parent_values_present"]:
        return "REFUSED_PARENT_DELTAW_VALUES_MISSING"
    if not row["projection_numeric"]:
        return "REFUSED_PROJECTION_MATRIX_SYMBOLIC"
    if row["uses_cancellation"]:
        return "REFUSED_CANCELLATION_ONLY"
    if row["bound_only_anchor"]:
        return "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = now()
    return [
        {
            "case_id": row["case_id"],
            "computed_status": evaluate_dryrun(row),
            "expected_status": row["expected_status"],
            "status_match": evaluate_dryrun(row) == row["expected_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2652_0_stability", "condition": "action-scale/readout stability is parent-signed", "current_status": "FAIL_ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED", "source_anchor": f"{OUTPUTS['stability_attempt'].name}:ASR2652_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2652_1_projection_values", "condition": "Delta_w projection matrix has numeric/sourced parent components", "current_status": "FAIL_SYMBOLIC_MATRIX_ONLY_PARENT_VALUES_MISSING", "source_anchor": f"{OUTPUTS['projection_matrix'].name}:DPM2652_0_core_vector", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2652_2_arena_inputs", "condition": "WEP/R10/PPN/clock/orbital tau/K/material/readout kernels are sourced", "current_status": "FAIL_MISSING_ARENA_PROJECTION_KERNELS", "source_anchor": f"{OUTPUTS['projection_requirements'].name}:DPR2652_1_arena_tau_K", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2652_3_no_cancellation", "condition": "claim does not rely on fitted cancellation between residual components", "current_status": "PASS_POLICY_WRITTEN_BUT_NONCLAIM", "source_anchor": f"{OUTPUTS['projection_matrix'].name}:DPM2652_6_no_cancellation_policy", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2652_4_verdict", "condition": "stable zero or finite projection can support local-GR/R10/WEP claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2652_0_stability through CG2652_3_no_cancellation", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2652_0_stability", "decision": "DO_NOT_PROMOTE_STABLE_DELTAW_ZERO", "reason": "one-owner theorem is exact conditionally, but parent action-scale, measure/current owner, readout no-reentry, radiative closure and variation-order clauses are unsigned", "status": "STABLE_ZERO_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "readout-variation commutator or action-scale parent owner", "valid_for_claim": False},
        {"decision_id": "DEC2652_1_projection_matrix", "decision": "DELTAW_ARENA_PROJECTION_MATRIX_STAGED_NONCLAIM", "reason": "local arenas now have symbolic rows, dependencies and refusal modes, but no parent values or full arena kernels", "status": "PROJECTION_MATRIX_STAGED_NONCLAIM", "next_dependency": "derive commutator zero or source first WEP/R10 matrix row", "valid_for_claim": False},
        {"decision_id": "DEC2652_2_next", "decision": "SELECT_2653_READOUT_VARIATION_COMMUTATOR_OR_WEP_ROW_V1", "reason": "the commutator is narrower than full action-scale ownership and directly controls whether downstream kernels can become source couplings", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2653 readout-variation commutator zero or WEP projection row v1", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2652_0_selected",
            "status": "selected",
            "next_doc": "2653-Y5-R2FR-readout-variation-commutator-zero-or-WEP-projection-row-v1.md",
            "next_script": "scripts/Y5_R2FR_readout_variation_commutator_zero_or_WEP_projection_row_v1_2653.py",
            "target": "Try to prove [delta_parent, R_readout] has no source-only coefficient codomain; if it fails, build the first WEP projection row v1 with tau/K/material/source/readout dependencies explicit.",
            "must_include": "commutator target; no-reentry theorem; WEP row v1; tau_WEP; K_WEP; material tensor; source-worldtube/readout dependencies; refusal states",
            "must_exclude": "symbolic Delta_w scoring, cancellation-only passes, bound anchors as predictions, local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2652_0_theory", "area": "source coupling derivation", "summary": "the one-owner/readout-stability theorem is exact but not parent-signed", "risk_level": "NARROW_STABILITY_GAP", "project_meaning": "the coupling problem is action-scale owner plus readout no-reentry plus radiative closure", "next_action": "prove the readout-variation commutator or action-scale owner", "valid_for_claim": False},
        {"status_id": "STAT2652_1_testing", "area": "local empirical branch", "summary": "WEP/R10/PPN/clock/orbital projection rows are staged as symbolic nonclaim matrix rows", "risk_level": "TEST_BRANCH_READY_FOR_INPUTS_NOT_SCORING", "project_meaning": "real inputs can be plugged later without pretending schema rows are a pass", "next_action": "fill WEP row v1 or R10 row after commutator attempt", "valid_for_claim": False},
        {"status_id": "STAT2652_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "source universality remains unsolved but is now governed by explicit theorem and matrix gates", "risk_level": "HARD_LOCAL_BRIDGE_DEBT", "project_meaning": "we are no longer circling the coupling; we are converting it into a proof target or a bounded residual map", "next_action": "2653 commutator/WEP row", "valid_for_claim": False},
    ]


def branch_copy_rows(matrix_rows: list[dict[str, Any]], requirement_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], requirement_rows)
    write_csv(BRANCH_COPIES["local_bounds"], matrix_rows)
    write_csv(BRANCH_COPIES["source_weight"], matrix_rows)
    write_csv(BRANCH_COPIES["microscope"], stability_attempt_rows())
    write_csv(BRANCH_COPIES["quarantine"], dryrun_rows)
    return [
        {"copy_id": copy_id, "path": str(path), "exists": path.exists(), "parseable_csv": path.exists() and len(csv_rows(path)) >= 1, "purpose": "2652 action-scale/readout/projection-matrix nonclaim handoff", "valid_for_claim": False}
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    dryrun_results = dryrun_result_rows(cases)
    matrix = projection_matrix_rows()
    requirements = projection_requirement_rows()
    rows = {
        "source_register": source_register_rows(),
        "stability_attempt": stability_attempt_rows(),
        "stability_gate": stability_gate_rows(),
        "projection_matrix": matrix,
        "projection_requirements": requirements,
        "dryrun_cases": cases,
        "dryrun_results": dryrun_results,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(matrix, requirements, dryrun_results)
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2652-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2652*",
        "*Y5_R2FR_action_scale_readout_stability_or_Delta_w_projection_matrix_2652*",
        "*JR2652*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    stability_ok = any(row["attempt_id"] == "ASR2652_6_verdict" and row["status"] == "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED" for row in rows["stability_attempt"])
    matrix_ok = len(rows["projection_matrix"]) >= 7 and all(not row["score_ready"] and not row["valid_prediction_row"] for row in rows["projection_matrix"])
    requirements_ok = all(row["blocks_claim"] and not row["valid_for_claim"] for row in rows["projection_requirements"])
    dryrun_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = any(row["gate_id"] == "CG2652_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]) and all(not row["gate_pass"] for row in rows["claim_gates"])
    next_ok = any("2653-Y5-R2FR-readout-variation-commutator-zero" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2652_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2652_01_stability_verdict", stability_ok, "stable Delta_w zero remains unsigned"),
        ("VAL2652_02_projection_matrix", matrix_ok, "Delta_w arena projection matrix rows are nonclaim/not score-ready"),
        ("VAL2652_03_requirements_block", requirements_ok, "all projection requirements block claims until sourced"),
        ("VAL2652_04_dryrun", dryrun_ok, "dry-run refuses unsigned owner/readout/variation/radiative gates, missing values, symbolic matrix, cancellation, and anchor-only bounds"),
        ("VAL2652_05_claim_gates_false", claim_ok, "claim remains blocked"),
        ("VAL2652_06_next_target", next_ok, "2653 target is recorded"),
        ("VAL2652_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2652_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2652_09_formalization_untouched", formal_ok, "no 2652 outputs are written under formalization-workbench"),
        ("VAL2652_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = now()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2652_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2652 keeps stable Delta_w zero unsigned, stages the Delta_w projection matrix, and selects readout-variation commutator or WEP row v1 next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2652 - Action-Scale Readout Stability Or Delta_w Projection Matrix

## Purpose

This checkpoint tests whether the no-Hom source-weight zero can survive action-scale, measure, radiative and readout maps. If not, it stages the finite `Delta_w` projection matrix across WEP, R10, PPN, clock and orbital arenas.

## Result

- The one-owner/readout-stability theorem is exact conditionally, but still not parent-signed.
- Stable `Delta_w=0` is therefore not promoted.
- The finite projection matrix is now explicit across WEP, R10, PPN, clock and orbital arenas, but every row remains nonclaim because parent values and arena kernels are missing.
- The next target is the narrower readout-variation commutator: prove no source-only codomain, or build WEP projection row v1.

## Source Register

{markdown_table(rows["source_register"])}

## Action-Scale Readout Stability Attempt

{markdown_table(rows["stability_attempt"])}

## Stability Gate

{markdown_table(rows["stability_gate"])}

## Delta_w Arena Projection Matrix

{markdown_table(rows["projection_matrix"])}

## Projection Requirements

{markdown_table(rows["projection_requirements"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
