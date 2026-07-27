from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2693"
BRANCH_ID = "Y5_R2FR_LOVELOCK_HYPOTHESIS_PROVER_OR_LEFT_HAND_OPERATOR_RESIDUAL_ACQUISITION_2693"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2693-Y5-R2FR-Lovelock-hypothesis-prover-or-left-hand-operator-residual-acquisition.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2693_SOURCE_REGISTER.csv",
    "hypothesis_audit": RESIDUALS / "P8_Y5_R2FR_2693_LOVELOCK_HYPOTHESIS_PROOF_AUDIT.csv",
    "silence_route": RESIDUALS / "P8_Y5_R2FR_2693_POSITIVE_OPERATOR_SILENCE_ROUTE_AUDIT.csv",
    "sector_requirements": RESIDUALS / "P8_Y5_R2FR_2693_SECTOR_CERTIFICATE_REQUIREMENTS_NONCLAIM.csv",
    "acquisition_rows": RESIDUALS / "P8_Y5_R2FR_2693_OPERATOR_RESIDUAL_ACQUISITION_ROWS_NONCLAIM.csv",
    "decision_gate": RESIDUALS / "P8_Y5_R2FR_2693_LOVELOCK_DECISION_GATE.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2693_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2693_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2693_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2693_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2693_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2693_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2693_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_hypothesis_audit": LOCAL_BOUNDS / "lovelock_hypothesis_proof_audit_2693_NONCLAIM.csv",
    "local_sector_requirements": LOCAL_BOUNDS / "sector_certificate_requirements_2693_NONCLAIM.csv",
    "local_acquisition_rows": LOCAL_BOUNDS / "operator_residual_acquisition_rows_2693_NONCLAIM.csv",
    "wep_acquisition_rows": WEP_RESIDUALS / "operator_residual_acquisition_rows_2693_NONCLAIM.csv",
    "source_weight_acquisition_rows": SOURCE_WEIGHT / "LEFT_HAND_OPERATOR_RESIDUAL_ACQUISITION_2693_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2693_SECTOR_POSITIVE_OPERATOR_SILENCE_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2693_2692_DOC",
        "relative_path": "2692-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "required_needles": ["NEXT2692_0_selected", "LVK2692_7_verdict", "VAL2692_OVERALL"],
        "purpose": "imports selected 2693 Lovelock hypothesis target",
    },
    {
        "source_id": "SRC2693_2692_LOVELOCK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2692_LOVELOCK_HYPOTHESIS_GATE.csv",
        "required_needles": ["LVK2692_2_metric_only", "LVK2692_3_second_order", "HYPOTHESES_NOT_PARENT_SIGNED"],
        "purpose": "imports current Lovelock hypothesis blockers",
    },
    {
        "source_id": "SRC2693_2692_OPERATOR_PACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2692_OPERATOR_RESIDUAL_PACK_NONCLAIM.csv",
        "required_needles": ["ORP2692_0_total_DeltaE", "ORP2692_10_total_abs_envelope", "NONCLAIM_LOCK"],
        "purpose": "imports current left-hand residual vector",
    },
    {
        "source_id": "SRC2693_2620_DOC",
        "relative_path": "2620-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
        "required_needles": ["EHD2620_4_current_verdict", "SECTOR_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT", "VAL2620_OVERALL"],
        "purpose": "imports EH-dominance sector-silence branch",
    },
    {
        "source_id": "SRC2693_2620_SECTOR_VARIATION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DOMINANCE_GATE_2620_SECTOR_VARIATION_AUDIT.csv",
        "required_needles": ["SVA2620_2_higher_derivative", "SVA2620_5_memory_coframe", "MISSING_LOCAL_FRAME_LOCK_VARIATION"],
        "purpose": "imports sector variation audit",
    },
    {
        "source_id": "SRC2693_2620_SCALING",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DOMINANCE_GATE_2620_LOCAL_SCALING_SILENCE_AUDIT.csv",
        "required_needles": ["LSS2620_0_exact_zero_path", "LSS2620_4_verdict", "RESIDUAL_SILENCE_NOT_CLOSED"],
        "purpose": "imports local scaling silence audit",
    },
    {
        "source_id": "SRC2693_2620_OPERATOR_COEFFS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DOMINANCE_GATE_2620_OPERATOR_COEFFICIENT_PACK.csv",
        "required_needles": ["OPC2620_0_EH_normalization", "OPC2620_7_total_DeltaE", "NONCLAIM_LOCK"],
        "purpose": "imports older operator coefficient pack",
    },
    {
        "source_id": "SRC2693_506_SILENCE_THEOREM",
        "relative_path": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "required_needles": ["positive source-free local operator", "F506_0_positive_operator_missing", "DEC506_0_partial_derivation"],
        "purpose": "imports the positive-operator silence mechanism",
    },
    {
        "source_id": "SRC2693_2579_DESCENT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DESCENT_COUPLING_PIM_2579_DESCENT_PACKAGE_AUDIT.csv",
        "required_needles": ["EDP2579_2_extra_double_zero", "EDP2579_3_positive_gap", "EDP2579_7_verdict"],
        "purpose": "imports double-zero and positive-gap blockers",
    },
    {
        "source_id": "SRC2693_2485_GRAMMAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_DERIVATIVE_GRAMMAR.csv",
        "required_needles": ["DG2485_1_EH_scalar", "DG2485_4_vertical_derivatives", "DG2485_6_projector_postvariation"],
        "purpose": "imports derivative grammar and retained operator classes",
    },
    {
        "source_id": "SRC2693_2691_CLASSIFIER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2691_PARENT_ACTION_NORMAL_FORM_SOURCE_MAP_CLASSIFIER.csv",
        "required_needles": ["CLS2691_2_lhs_geometry", "CLS2691_8_pim_source_measure", "CLS2691_10_verdict"],
        "purpose": "imports source/LHS classifier status",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def hypothesis_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LHP2693_0_dimension",
            "four-dimensional effective public local branch",
            "local lab/exterior branch is modeled by a 4D observed manifold/coframe",
            "PARTIAL_LOCAL_CHART_ASSUMPTION_NOT_PARENT_PROOF",
            "no bulk/cosmological hidden coordinate feeds local operator",
            "bulk/domain/cosmology bleed-through remains possible",
            "LVK2692_0_dimension",
        ),
        (
            "LHP2693_1_metric_coframe_only",
            "metric/coframe-only long-range public gravitational field",
            "all motion/time/memory/projector/private fields are gauge, auxiliary, massive positive with no source, topological, or bounded",
            "FAIL_SECTOR_CERTIFICATES_MISSING",
            "Lovelock/EH filter can apply to the public LHS",
            "extra public scalar/vector/tensor hair can produce fifth force or PPN residuals",
            "LVK2692_2_metric_only;506:T506_EH_plus_silent_reduction",
        ),
        (
            "LHP2693_2_locality",
            "local Markovian operator",
            "history/memory kernels reduce to local constants or are bounded below local tolerances",
            "FAIL_MEMORY_KERNEL_SILENCE_UNSIGNED",
            "nonlocal/history tails cannot alter local field equations",
            "clock/orbital hysteresis or Gdot-like memory channels remain",
            "LVK2692_1_locality;506:E506_memory_kernel_silence",
        ),
        (
            "LHP2693_3_second_order",
            "second-order public field equations",
            "higher-curvature/torsion/nonmetricity operators are absent, topological, field-redefinition redundant, or source-backed bounded",
            "FAIL_HIGHER_OPERATOR_BASIS_AND_SCALE_MISSING",
            "Einstein operator is the unique low-derivative public LHS",
            "R10/Yukawa/PPN higher-operator rows remain live",
            "LVK2692_3_second_order;2620:SVA2620_2_higher_derivative",
        ),
        (
            "LHP2693_4_diffeomorphism_noether",
            "diffeomorphism-invariant complete parent variation",
            "all retained local sectors arise from one action with a final Noether/Bianchi identity",
            "PARTIAL_CONTRACT_COMPLETE_ACTION_UNSIGNED",
            "divergence-free LHS or explicit residual exchange is controlled",
            "unowned exchange can leak into alpha3/preferred-frame channels",
            "LVK2692_4_diffeomorphism;2691:SMC2691_6_no_cancellation",
        ),
        (
            "LHP2693_5_boundary_silence",
            "boundary/topological/reference silence",
            "surface/reference/improvement terms have zero local variation or fixed-before-readout zero flux",
            "FAIL_BOUNDARY_FLUX_ZERO_UNSIGNED",
            "no hidden mass/PPN/clock term enters through boundaries",
            "boundary charge, radial hair, or reference subtraction can alter measured field",
            "LVK2692_5_boundary;506:E506_boundary_topological_silence",
        ),
        (
            "LHP2693_6_matter_source",
            "minimal universal observed-frame matter coupling",
            "ordinary matter source is Hilbert stress in the same observed frame and no post-variation source projector is applied",
            "SOURCE_CLASSIFIER_PARTIAL_NOT_THEOREM",
            "RHS source no longer spoils GR/Newton once LHS closes",
            "prefactor/shadow/projector/source-normalization rows remain",
            "LVK2692_6_matter_coupling;2691:CLS2691_10_verdict",
        ),
        (
            "LHP2693_7_verdict",
            "current MTS Lovelock-hypothesis proof",
            "MTS parent-signs every Lovelock/EH hypothesis needed for derived local GR",
            "PROOF_FAILS_CURRENT_CORPUS_CERTIFICATE_QUEUE_REQUIRED",
            "local GR would be derivable by theorem rather than imported",
            "do not claim GR/Newton; build sector certificates or residual rows",
            "LHP2693_0 through LHP2693_6",
        ),
    ]
    return [
        {
            "hypothesis_id": row[0],
            "hypothesis": row[1],
            "formal_requirement": row[2],
            "current_status": row[3],
            "if_signed": row[4],
            "if_unsigned": row[5],
            "source_anchor": row[6],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def silence_route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "POS2693_0_energy_identity",
            "positive source-free operator silence",
            "L_X X=0, integral_A <X,L_X X> = positive_norm[X] + boundary_flux",
            "REFERENCE_ROUTE_VALID_CONDITIONAL",
            "positive operator + no source charge + zero boundary flux gives X=0 modulo gauge/topology",
            "MTS has not supplied every sector-specific L_X, sign, charge, and flux",
        ),
        (
            "POS2693_1_double_zero",
            "extra coupling double zero",
            "C_i(Phi0)=0 and partial_A C_i(Phi0)=0 for each retained non-EH coupling",
            "GENERIC_ROUTE_NOT_ACTUAL_INVENTORY",
            "first-order fifth-force/source-normalization/PPN leakage is removed",
            "actual C_i/O_i inventory remains incomplete",
        ),
        (
            "POS2693_2_no_source_charge",
            "compact exterior no-charge condition",
            "J_X=0 or int_source J_X=0 for every extra sector in local exterior",
            "MISSING_SECTOR_SOURCE_LAW",
            "extra field has no radial/fifth-force hair",
            "worldtube/projector/source glue remains open",
        ),
        (
            "POS2693_3_boundary_flux",
            "zero boundary/linking-sphere flux",
            "int_boundary B_X = 0 or fixed background subtraction before readout",
            "MISSING_ZERO_FLUX_THEOREM",
            "boundary/topological terms are silent locally",
            "radial boundary hair/reference charge remains possible",
        ),
        (
            "POS2693_4_scale_bound",
            "fallback controlled bound",
            "|K_X c_X| <= tau_arena with units, kernel and source path declared",
            "BOUND_ROUTE_DEFINED_NOT_FILLED",
            "nonzero residual can be tested honestly",
            "no coefficient values/kernels/tolerances filled yet",
        ),
        (
            "POS2693_5_verdict",
            "positive-operator Lovelock repair route",
            "all extra sectors satisfy POS2693_0..4",
            "ROUTE_VALID_BUT_NOT_PARENT_SIGNED",
            "metric-only/local/second-order hypotheses can close sector-by-sector",
            "certificate queue required before promotion",
        ),
    ]
    return [
        {
            "route_id": row[0],
            "route_piece": row[1],
            "formal_statement": row[2],
            "current_status": row[3],
            "if_signed": row[4],
            "if_unsigned": row[5],
            "source_anchor": "506-local-EH-reduction-and-extra-sector-silence-theorem.md;2579:EDP2579_2_extra_double_zero;2579:EDP2579_3_positive_gap",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def sector_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCR2693_0_higher_derivative", "higher_derivative_public_metric", "R2/Ricci2/boxR/Weyl/torsion/nonmetricity", "parent grammar forbids, topological/redundant, or coefficient has high-scale bound", "MISSING_OPERATOR_BASIS_VARIATION_SCALE", "ORP2692_1_higher_derivative", "R10;PPN;waves;cosmology"),
        ("SCR2693_1_aux_private", "auxiliary_private_vertical_fields", "motion/time/flow/private metric compatibility fields", "positive source-free operator or pure gauge/topological proof", "MISSING_LX_SIGN_GAP_SOURCE_FLUX", "ORP2692_2_aux_private_stress", "local_GR;PPN;clock;orbital"),
        ("SCR2693_2_projector", "domain_projector_readout", "Pi_M/projector/domain selector/readout variation", "identity/commuting chain map plus zero variation or explicit bound", "MISSING_PROJECTOR_VARIATION_COMMUTATOR_ZERO", "ORP2692_3_projector_readout", "Newton;WEP;PPN;orbital"),
        ("SCR2693_3_boundary", "boundary_reference_topological", "boundary/reference/improvement/topological terms", "fixed-before-readout zero flux or declared residual coefficient", "MISSING_BOUNDARY_ZERO_FLUX_REFERENCE_LOCK", "ORP2692_4_boundary_reference", "Newton;local_GR;clock;orbital"),
        ("SCR2693_4_nonminimal", "nonminimal_source_geometry", "f(X,Phi)L_m or A(X)J_m", "forbid, reclassify into geometry with source law, or bound through WEP/clock/PPN/R10", "MISSING_FORBID_RECLASSIFY_BOUND", "ORP2692_5_nonminimal_source_geometry", "WEP;clock;PPN;R10"),
        ("SCR2693_5_memory_coframe", "memory_coframe_preferred_frame", "memory/tau/coframe/local-frame residual", "local frame-lock theorem or positive/stable memory kernel silence", "MISSING_MEMORY_KERNEL_AND_FRAME_LOCK", "ORP2692_6_memory_coframe", "PPN_alpha_i;clock;orbital"),
        ("SCR2693_6_nonlocal_history", "nonlocal_history_kernel", "history-dependent nonlocal LHS kernel", "local Markov/adiabatic reduction or source-backed kernel tail bound", "MISSING_LOCALITY_REDUCTION_KERNEL_BOUND", "ORP2692_7_nonlocal_history", "clock;orbital_hysteresis;cosmology;waves"),
        ("SCR2693_7_kappa_source", "kappa_source_normalization", "kappa/G/source-current frame", "constant kappa and source-current normalization owned before Newton readout", "MISSING_CONSTANT_KAPPA_SOURCE_FRAME", "ORP2692_8_kappa_source_norm", "Newton;Gdot;PPN;clock"),
        ("SCR2693_8_worldtube_gauss", "worldtube_gauss_mass", "Hilbert/worldtube/exterior Gauss mass equality", "same charge maps to exterior potential before fitted orbital GM", "MISSING_WORLDTUBE_GAUSS_CLOSURE", "ORP2692_9_worldtube_gauss", "Newton;orbital;Cavendish;PPN"),
        ("SCR2693_9_verdict", "all sectors", "complete Lovelock hypothesis certificate set", "every sector is ZERO, SUPPRESSED_WITH_UNITS, RECLASSIFIED, or NONCLAIM_BOUND_READY", "CERTIFICATE_SET_INCOMPLETE", "ORP2692_10_total_abs_envelope", "all local arenas"),
    ]
    return [
        {
            "certificate_id": row[0],
            "sector": row[1],
            "object": row[2],
            "required_certificate": row[3],
            "current_status": row[4],
            "residual_row": row[5],
            "observable_link": row[6],
            "operator_written": "false",
            "sign_or_gap_known": "false",
            "source_charge_zero": "false",
            "boundary_flux_zero": "false",
            "coefficient_value_present": "false",
            "projection_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2693_0_c_HD", "c_HD_vector", "higher-derivative operator vector", "operator_basis;principal_order;coefficient_units;weak_field_kernel;R10/PPN map", "SCR2693_0_higher_derivative", "MISSING_OPERATOR_BASIS_AND_SOURCE_BACKED_SCALE", "R10;PPN;waves"),
        ("ACQ2693_1_c_aux", "c_aux_private", "auxiliary/private stress vector", "Euler_operator;energy_identity;mass_gap;source_charge;boundary_flux", "SCR2693_1_aux_private", "MISSING_OPERATOR_SIGN_SOURCE_FLUX_CERTIFICATE", "local_GR;PPN;clock"),
        ("ACQ2693_2_c_projector", "c_projector_operator", "projector/readout commutator residual", "chain_map;commutator_norm;variation_formula;local_kernel", "SCR2693_2_projector", "MISSING_PROJECTOR_CHAIN_MAP_OR_BOUND", "Newton;WEP;PPN;orbital"),
        ("ACQ2693_3_c_boundary", "c_boundary_reference", "boundary/reference residual", "boundary_condition;reference_subtraction;flux_integral;mass_charge_kernel", "SCR2693_3_boundary", "MISSING_ZERO_FLUX_OR_BOUND", "Newton;clock;orbital"),
        ("ACQ2693_4_c_nonminimal", "c_nonminimal", "nonminimal matter-geometry coupling", "forbid_theorem_or_coupling_function;species_derivative;WEP_clock_kernel", "SCR2693_4_nonminimal", "MISSING_FORBID_OR_COUPLING_BOUND", "WEP;clock;PPN;R10"),
        ("ACQ2693_5_c_memory_frame", "c_memory_frame", "memory/coframe/preferred-frame residual", "local_frame_lock;memory_kernel;alpha_i_projection;clock_projection", "SCR2693_5_memory_coframe", "MISSING_FRAME_LOCK_OR_KERNEL_BOUND", "PPN_alpha_i;clock;orbital"),
        ("ACQ2693_6_K_history", "K_history", "nonlocal/history kernel", "kernel_form;locality_limit;decay_scale;orbital_clock_kernel", "SCR2693_6_nonlocal_history", "MISSING_LOCALITY_REDUCTION_OR_DECAY_BOUND", "clock;orbital;cosmology"),
        ("ACQ2693_7_delta_kappa_source", "delta_kappa_source", "kappa/source normalization residual", "constant_kappa_proof;source_frame_map;Gdot_or_fractional_bound", "SCR2693_7_kappa_source", "MISSING_CONSTANT_KAPPA_SOURCE_OWNER", "Newton;Gdot;PPN"),
        ("ACQ2693_8_delta_worldtube_Gauss", "delta_worldtube_Gauss", "worldtube/Gauss mass residual", "Hilbert_mass;worldtube_charge;Gauss_flux;orbital_readout_without_backfill", "SCR2693_8_worldtube_gauss", "MISSING_CHARGE_GAUSS_EQUALITY", "Newton;orbital;Cavendish"),
        ("ACQ2693_9_total_abs", "Delta_LHS_GR_abs", "absolute local-GR residual envelope", "sum absolute projected residuals with no cancellation credit", "SCR2693_9_verdict", "MISSING_COMPONENT_VALUES_AND_KERNELS", "all local arenas"),
    ]
    return [
        {
            "acquisition_id": row[0],
            "symbol": row[1],
            "residual": row[2],
            "required_inputs": row[3],
            "certificate_anchor": row[4],
            "current_status": row[5],
            "observable_link": row[6],
            "numeric_value_present": "false",
            "source_path_present": "true",
            "units_declared": "false",
            "kernel_declared": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("LDG2693_0_lovelock_proof", "all LHP2693 hypotheses parent-signed", "FAIL", "LHP2693_7_verdict", "Lovelock theorem cannot be promoted as MTS derivation"),
        ("LDG2693_1_positive_operator_repair", "all extra sectors have positive/no-source/zero-flux or topology certificates", "FAIL", "POS2693_5_verdict;SCR2693_9_verdict", "metric-only/local/second-order repair not complete"),
        ("LDG2693_2_residual_acquisition", "every failed sector has explicit acquisition row", "PASS_NONCLAIM", "ACQ2693_0 through ACQ2693_9", "fallback route is well-defined but not score-ready"),
        ("LDG2693_3_no_shortcuts", "no EH axiom, cancellation, or fitted-GM backfill", "PASS_GUARD_ONLY", "DRY2693_*", "guardrails remain active"),
        ("LDG2693_4_verdict", "Lovelock hypothesis prover can claim local GR", "CLAIM_BLOCKED", "LDG2693_0 through LDG2693_3", "move to sector-specific certificate proof or fill residual rows"),
    ]
    return [
        {
            "gate_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "source_anchor": row[3],
            "decision": row[4],
            "gate_pass": "true" if row[2].startswith("PASS") else "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2693_0_all_certificates", "true", "true", "true", "true", "false", "false", "false", "THEOREM_READY_IF_PARENT_SIGNED"),
        ("DRY2693_1_lovelock_missing", "false", "true", "true", "true", "false", "false", "false", "REJECT_LOVELOCK_PROOF_MISSING"),
        ("DRY2693_2_positive_operator_missing", "true", "false", "true", "true", "false", "false", "false", "REJECT_POSITIVE_OPERATOR_CERTIFICATES_MISSING"),
        ("DRY2693_3_acquisition_missing", "false", "false", "false", "true", "false", "false", "false", "REJECT_NO_THEOREM_AND_NO_RESIDUAL_ROWS"),
        ("DRY2693_4_bianchi_missing", "true", "true", "true", "false", "false", "false", "false", "REJECT_NOETHER_BIANCHI_UNSIGNED"),
        ("DRY2693_5_eh_axiom", "false", "false", "true", "true", "true", "false", "false", "REJECT_EH_AS_AXIOM"),
        ("DRY2693_6_cancellation_only", "false", "false", "true", "true", "false", "true", "false", "REJECT_CANCELLATION_ONLY_PASS"),
        ("DRY2693_7_fitted_gm_backfill", "true", "true", "true", "true", "false", "false", "true", "REJECT_FITTED_GM_BACKFILL"),
    ]
    return [
        {
            "case_id": row[0],
            "lovelock_hypotheses_signed": row[1],
            "positive_operator_certificates_signed": row[2],
            "residual_acquisition_rows_present": row[3],
            "bianchi_noether_signed": row[4],
            "eh_as_axiom": row[5],
            "cancellation_only": row[6],
            "fitted_gm_backfill": row[7],
            "expected_status": row[8],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in cases
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["eh_as_axiom"] == "true":
        return "REJECT_EH_AS_AXIOM"
    if case["cancellation_only"] == "true":
        return "REJECT_CANCELLATION_ONLY_PASS"
    if case["fitted_gm_backfill"] == "true":
        return "REJECT_FITTED_GM_BACKFILL"
    if case["residual_acquisition_rows_present"] != "true" and case["lovelock_hypotheses_signed"] != "true":
        return "REJECT_NO_THEOREM_AND_NO_RESIDUAL_ROWS"
    if case["lovelock_hypotheses_signed"] != "true":
        return "REJECT_LOVELOCK_PROOF_MISSING"
    if case["positive_operator_certificates_signed"] != "true":
        return "REJECT_POSITIVE_OPERATOR_CERTIFICATES_MISSING"
    if case["bianchi_noether_signed"] != "true":
        return "REJECT_NOETHER_BIANCHI_UNSIGNED"
    return "THEOREM_READY_IF_PARENT_SIGNED"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        computed = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "computed_status": computed,
                "expected_status": case["expected_status"],
                "status_match": as_bool(computed == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2693_0_hypotheses", "all Lovelock/EH hypotheses parent-signed", "FAIL_LOVELOCK_HYPOTHESIS_PROOF_FAILED", "LHP2693_7_verdict", "false"),
        ("CG2693_1_sector_certificates", "all extra sectors have zero/suppression certificates", "FAIL_SECTOR_CERTIFICATE_SET_INCOMPLETE", "SCR2693_9_verdict", "false"),
        ("CG2693_2_residual_values", "residual acquisition rows have values, units, kernels and source paths", "FAIL_ACQUISITION_ROWS_NONCLAIM", "ACQ2693_9_total_abs", "false"),
        ("CG2693_3_source_normalization", "source/Gauss normalization branch closed", "FAIL_PARALLEL_SOURCE_GAUSS_OPEN", "2692:NEXT2692_1_parallel", "false"),
        ("CG2693_4_noether", "final parent Noether/Bianchi identity signed", "FAIL_FINAL_NOETHER_CHAIN_UNSIGNED", "LHP2693_4_diffeomorphism_noether", "false"),
        ("CG2693_5_guardrails", "EH axiom, cancellation and fitted-GM shortcuts refused", "PASS_GUARD_ONLY", "DRY2693_5;DRY2693_6;DRY2693_7", "true"),
        ("CG2693_6_verdict", "local GR/Newton branch can claim pass", "CLAIM_BLOCKED", "CG2693_0 through CG2693_5", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "source_anchor": row[3],
            "gate_pass": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2693_0_lovelock_attempt",
            "decision": "LOVELOCK_PROOF_ATTEMPT_FAILS_CURRENT_CORPUS",
            "reason": "The theorem route is valid, but MTS has not parent-signed metric-only, locality, second-order, boundary silence, source, and Noether clauses.",
            "status": "NO_PROMOTION",
            "next_dependency": "sector-specific certificates",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2693_1_silence_mechanism",
            "decision": "POSITIVE_OPERATOR_SILENCE_IS_THE_BEST_DERIVATION_ROUTE",
            "reason": "It is not a plateau axiom: positive operator plus no source charge plus zero boundary flux proves extra fields vanish or become pure gauge/topological.",
            "status": "CONDITIONAL_ROUTE_SELECTED",
            "next_dependency": "operator/sign/source/boundary certificate per sector",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2693_2_residual_fallback",
            "decision": "FAILED_CERTIFICATES_BECOME_OPERATOR_ACQUISITION_ROWS",
            "reason": "Any sector that cannot be theorem-zeroed must get coefficient values, units, kernels, source paths and observable projections.",
            "status": "NONCLAIM_ACQUISITION_READY",
            "next_dependency": "fill ACQ2693 rows or prove corresponding SCR2693 certificates",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2693_3_next",
            "decision": "MOVE_TO_SECTOR_POSITIVE_OPERATOR_CERTIFICATE_NEXT",
            "reason": "The smallest real leap is no longer another overview; it is proving or failing the higher-derivative/aux/projector/boundary/memory sectors one by one.",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2694 sector-specific positive-operator silence or residual values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2693_0_selected",
            "kind": "selected",
            "target_doc": "2694-Y5-R2FR-sector-positive-operator-silence-certificates-or-residual-values.md",
            "target_script": "scripts/Y5_R2FR_sector_positive_operator_silence_certificates_or_residual_values_2694.py",
            "purpose": "derive field-specific operator/sign/source/boundary certificates for retained non-EH sectors, starting with the sectors most able to close the Lovelock hypotheses; otherwise fill residual value requirements",
            "acceptance_gate": "each sector receives theorem-zero, positive-gap/no-source/zero-flux silence, source-backed bound row, or explicit fail status; no sector disappears by language",
            "forbidden_shortcuts": "EH as axiom; plateau axiom; cancellation-only pass; symbolic-small residuals; missing units/kernels; fitted GM backfill; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "NEXT2693_1_parallel_held",
            "kind": "parallel_held",
            "target_doc": "2694b-Y5-R2FR-source-normalization-worldtube-Gauss-owner-or-residual-values.md",
            "target_script": "scripts/Y5_R2FR_source_normalization_worldtube_Gauss_owner_or_residual_values_2694b.py",
            "purpose": "close the source/Gauss normalization chain needed before Newton can be claimed",
            "acceptance_gate": "same charge owns Hilbert source mass, parent charge, Gauss flux and measured Newton mass before fitting",
            "forbidden_shortcuts": "using orbital GM as premise; source-side cleanup as full GR proof",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2693_0_lovelock", "Lovelock/EH hypothesis proof", "FAILED_CURRENT_CORPUS", "valid theorem route exists but hypotheses are not parent-signed"),
        ("STATUS2693_1_silence", "positive operator silence route", "CONDITIONAL_MECHANISM_READY", "needs field-specific operator/sign/source/boundary certificates"),
        ("STATUS2693_2_residuals", "operator residual acquisition", "FINITE_ROWS_READY_NONCLAIM", "failed clauses are explicit value/kernel/source requirements"),
        ("STATUS2693_3_newton", "Newton/Poisson", "PARALLEL_SOURCE_GAUSS_BLOCKED", "source normalization remains separate and required"),
        ("STATUS2693_4_claims", "claim status", "ALL_LOCAL_CLAIMS_BLOCKED", "no local-GR/Newton/PPN/R10/clock/orbital claim"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2694 sector positive-operator silence certificates or residual values",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2693_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    hypothesis: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    sector_requirements: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    decision_gate: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    hypothesis_fail = any(row["hypothesis_id"] == "LHP2693_7_verdict" and row["current_status"] == "PROOF_FAILS_CURRENT_CORPUS_CERTIFICATE_QUEUE_REQUIRED" for row in hypothesis)
    silence_conditional = any(row["route_id"] == "POS2693_5_verdict" and row["current_status"] == "ROUTE_VALID_BUT_NOT_PARENT_SIGNED" for row in silence)
    sectors_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["operator_written"] == "false"
        and row["coefficient_value_present"] == "false"
        for row in sector_requirements
    )
    acquisition_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["score_ready"] == "false"
        and row["numeric_value_present"] == "false"
        for row in acquisition
    )
    decision_blocks = any(row["gate_id"] == "LDG2693_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in decision_gate)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2693_6_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2694" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2693_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2693_lovelock_proof_refused", hypothesis_fail, "Lovelock hypothesis proof fails current corpus and is not promoted"),
        ("VAL2693_positive_operator_route_conditional", silence_conditional, "positive-operator silence route is recorded as valid conditional but not parent-signed"),
        ("VAL2693_sector_requirements_nonclaim", sectors_nonclaim, "sector certificate requirements remain explicit nonclaim rows"),
        ("VAL2693_acquisition_rows_nonclaim", acquisition_nonclaim, "operator residual acquisition rows have no values/kernels and are not score-ready"),
        ("VAL2693_decision_gate_blocks", decision_blocks, "Lovelock decision gate blocks local-GR promotion"),
        ("VAL2693_dryrun_refusals", dryrun_ok, "dry-run refuses missing certificates, EH-as-axiom, cancellation and fitted-GM shortcuts"),
        ("VAL2693_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2693_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2693_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2693_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2693_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2693_next_target_selected", next_target_ok, "2694 sector certificate target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2693_OVERALL",
            "passed": as_bool(overall),
            "detail": "2693 refuses Lovelock promotion, preserves the positive-operator silence route, and stages sector certificate/residual acquisition rows",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    hypothesis: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    sector_requirements: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    decision_gate: list[dict[str, Any]],
    dry_cases: list[dict[str, Any]],
    dry_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2693 - Y5/R2FR Lovelock Hypothesis Prover or Left-Hand Operator Residual Acquisition",
                "",
                "## Private Verdict",
                "",
                "This checkpoint takes the leap seriously and then refuses to fake it. The Lovelock/EH route is the cleanest route to derived local GR, but current MTS evidence does not yet parent-sign the hypotheses: metric/coframe-only public branch, locality, second order, boundary silence, complete Noether identity, and source normalization remain open.",
                "",
                "The useful progress is sharper than a no. The positive-operator silence mechanism is the right repair: for each extra sector, write its local operator, prove sign/gap, prove no exterior source charge, prove zero boundary/linking flux, or else carry a source-backed residual coefficient into local tests. That is how the branch can become derivable rather than assumed.",
                "",
                "So 2693 does not claim local GR/Newton. It converts the Lovelock failure into a finite certificate/acquisition queue. No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, or R10 claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Lovelock Hypothesis Proof Audit",
                "",
                markdown_table(hypothesis),
                "",
                "## Positive Operator Silence Route Audit",
                "",
                markdown_table(silence),
                "",
                "## Sector Certificate Requirements",
                "",
                markdown_table(sector_requirements),
                "",
                "## Operator Residual Acquisition Rows",
                "",
                markdown_table(acquisition),
                "",
                "## Lovelock Decision Gate",
                "",
                markdown_table(decision_gate),
                "",
                "## Dry-Run Cases",
                "",
                markdown_table(dry_cases),
                "",
                "## Dry-Run Results",
                "",
                markdown_table(dry_results),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    for path in [RESIDUALS, LOCAL_BOUNDS, WEP_RESIDUALS, SOURCE_WEIGHT, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    hypothesis = hypothesis_audit_rows()
    silence = silence_route_rows()
    sector_requirements = sector_requirement_rows()
    acquisition = acquisition_rows()
    decision_gate = decision_gate_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["hypothesis_audit"], hypothesis)
    write_csv(OUTPUTS["silence_route"], silence)
    write_csv(OUTPUTS["sector_requirements"], sector_requirements)
    write_csv(OUTPUTS["acquisition_rows"], acquisition)
    write_csv(OUTPUTS["decision_gate"], decision_gate)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_hypothesis_audit"], hypothesis)
    write_csv(BRANCH_OUTPUTS["local_sector_requirements"], sector_requirements)
    write_csv(BRANCH_OUTPUTS["local_acquisition_rows"], acquisition)
    write_csv(BRANCH_OUTPUTS["wep_acquisition_rows"], acquisition)
    write_csv(BRANCH_OUTPUTS["source_weight_acquisition_rows"], acquisition)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_target)

    branch_rows = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validation = validation_rows(
        source_rows=source_rows,
        hypothesis=hypothesis,
        silence=silence,
        sector_requirements=sector_requirements,
        acquisition=acquisition,
        decision_gate=decision_gate,
        dryrun_results=dry_results,
        claim_gates=claim_gates,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_document(
        source_rows=source_rows,
        hypothesis=hypothesis,
        silence=silence,
        sector_requirements=sector_requirements,
        acquisition=acquisition,
        decision_gate=decision_gate,
        dry_cases=dry_cases,
        dry_results=dry_results,
        claim_gates=claim_gates,
        decisions=decisions,
        next_target=next_target,
        status=status,
        validation=validation,
    )


if __name__ == "__main__":
    main()
