from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2692"
BRANCH_ID = "Y5_R2FR_GR_LEFT_HAND_EINSTEIN_NEWTON_LIMIT_OR_OPERATOR_RESIDUAL_PACK_2692"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2692-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2692_SOURCE_REGISTER.csv",
    "master_theorem": RESIDUALS / "P8_Y5_R2FR_2692_LHS_GR_MASTER_THEOREM_CONTRACT.csv",
    "lovelock_gate": RESIDUALS / "P8_Y5_R2FR_2692_LOVELOCK_HYPOTHESIS_GATE.csv",
    "newton_derivation": RESIDUALS / "P8_Y5_R2FR_2692_NEWTON_POISSON_NORMALIZATION_DERIVATION.csv",
    "operator_pack": RESIDUALS / "P8_Y5_R2FR_2692_OPERATOR_RESIDUAL_PACK_NONCLAIM.csv",
    "observable_map": RESIDUALS / "P8_Y5_R2FR_2692_RESIDUAL_TO_OBSERVABLE_MAP.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2692_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2692_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2692_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2692_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2692_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2692_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2692_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_master_theorem": LOCAL_BOUNDS / "lhs_gr_master_theorem_contract_2692_NONCLAIM.csv",
    "local_operator_pack": LOCAL_BOUNDS / "lhs_operator_residual_pack_2692_NONCLAIM.csv",
    "wep_operator_pack": WEP_RESIDUALS / "lhs_operator_residual_pack_2692_NONCLAIM.csv",
    "source_weight_operator_pack": SOURCE_WEIGHT / "LEFT_HAND_GR_OPERATOR_RESIDUAL_PACK_2692_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2692_LOVELOCK_HYPOTHESIS_OR_OPERATOR_RESIDUAL_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2692_2691_DOC",
        "relative_path": "2691-Y5-R2FR-parent-action-normal-form-source-map-classifier-or-delta-w-value-acquisition.md",
        "required_needles": ["NEXT2691_0_selected", "left-hand Einstein/Newton limit", "formalization-workbench edits"],
        "purpose": "confirms 2691 selected the left-hand GR/Newton bridge",
    },
    {
        "source_id": "SRC2692_2691_GR_BRIDGE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2691_GR_NEWTON_BRIDGE_IMPLICATIONS.csv",
        "required_needles": ["GRB2691_1_lhs_operator", "NEXT_REQUIRED_BRIDGE", "run 2692 LHS bridge"],
        "purpose": "imports the current GR bridge handoff",
    },
    {
        "source_id": "SRC2692_2691_RESIDUAL_PACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2691_RESIDUAL_COEFFICIENT_PACK_NONCLAIM.csv",
        "required_needles": ["RCP2691_5_c_lhs_GR", "Delta_source_map_classifier_abs", "MISSING_GR_LIMIT_DERIVATION"],
        "purpose": "imports current left-hand/source residual rows",
    },
    {
        "source_id": "SRC2692_2619_DOC",
        "relative_path": "2619-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "required_needles": ["ELH2619_5_current_verdict", "NWF2619_1_poisson_conditional", "VAL2619_OVERALL"],
        "purpose": "imports historical exact conditional GR/Newton bridge",
    },
    {
        "source_id": "SRC2692_2619_OPERATOR_PACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv",
        "required_needles": ["ORP2619_0_E_LHS_GR_residual", "ORP2619_8_nonclaim_lock"],
        "purpose": "imports historical operator residual pack",
    },
    {
        "source_id": "SRC2692_2485_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_NORMAL_FORM_CONTRACT.csv",
        "required_needles": ["NF2485_2_public_field_equation", "NF2485_3_Newton_Poisson_gate"],
        "purpose": "imports parent normal-form field equation and Newton gate",
    },
    {
        "source_id": "SRC2692_2485_GRAMMAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_DERIVATIVE_GRAMMAR.csv",
        "required_needles": ["DG2485_1_EH_scalar", "DG2485_3_higher_curvature", "DG2485_6_projector_postvariation"],
        "purpose": "imports derivative grammar for Lovelock/EH hypothesis gate",
    },
    {
        "source_id": "SRC2692_2579_DESCENT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DESCENT_COUPLING_PIM_2579_DESCENT_PACKAGE_AUDIT.csv",
        "required_needles": ["EDP2579_0_EH_core", "EDP2579_7_verdict"],
        "purpose": "imports EH descent package blockers",
    },
    {
        "source_id": "SRC2692_2579_RESIDUALS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv",
        "required_needles": ["ENV2579_0_EH", "ENV2579_9_total"],
        "purpose": "imports local-GR residual envelope",
    },
    {
        "source_id": "SRC2692_2618_GR_STATUS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_GR_BRIDGE_STATUS.csv",
        "required_needles": ["GRB2618_1_lhs_operator", "GRB2618_3_newton"],
        "purpose": "imports prior GR bridge status",
    },
    {
        "source_id": "SRC2692_LOCAL_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "required_needles": ["R3_gamma", "R10_fifth_force", "R11_EH_operator_ledger"],
        "purpose": "imports local observable residual row names",
    },
    {
        "source_id": "SRC2692_CHARGE_CURRENT",
        "relative_path": "source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "required_needles": ["CC2_EH_constraint_source_link", "CC7_closed_flux_and_Gauss_calibration"],
        "purpose": "imports source-normalization/Gauss blocker",
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


def master_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LHS2692_0_target",
            "left-hand target equation",
            "E_LHS[g_obs,Phi,X] = G_munu[g_obs] + Lambda_loc g_munu + DeltaE_munu",
            "TARGET_EXACT",
            "turns local-GR recovery into DeltaE_munu=0/bounded rather than rhetoric",
            "DeltaE_munu remains the live residual",
            "2691:GRB2691_1_lhs_operator;2619:ELH2619_0_target",
            "false",
        ),
        (
            "LHS2692_1_parent_variation",
            "one local variational parent",
            "delta S_parent/delta e_obs = 0 with all source-like and geometry-like terms action-owned before readout",
            "CONTRACT_READY_PARENT_INVENTORY_INCOMPLETE",
            "Noether/Bianchi and source/LHS split become controlled",
            "unlisted parent terms can still alter E_LHS",
            "2618:ANF2618_0_parent_action_partition;2691:CLS2691_10_verdict",
            "false",
        ),
        (
            "LHS2692_2_public_metric_only",
            "local public degrees of freedom",
            "compact local branch has only observed metric/coframe as long-range public gravitational field",
            "MISSING_PRIVATE_SECTOR_ELIMINATION",
            "Lovelock/EH filter can be applied to the public LHS",
            "motion/memory/projector/private fields may contribute extra local stress",
            "2485:DG2485_4_vertical_derivatives;2579:EDP2579_3_positive_gap",
            "false",
        ),
        (
            "LHS2692_3_second_order_locality",
            "second-order local operator",
            "E_LHS is local and second order in the observed metric/coframe after auxiliary descent",
            "MISSING_HIGHER_OPERATOR_ZERO_OR_SCALE",
            "higher-curvature/Yukawa tails are excluded or bounded",
            "R^2/Ricci^2/nonlocal/history terms remain possible",
            "2485:DG2485_1_EH_scalar;2485:DG2485_3_higher_curvature",
            "false",
        ),
        (
            "LHS2692_4_lovelock_filter",
            "four-dimensional diffeomorphism-invariant metric LHS",
            "in 4D local metric-only second-order diffeo-invariant dynamics, E_munu = a G_munu + b g_munu",
            "REFERENCE_THEOREM_CONDITIONAL_NOT_MTS_PROOF",
            "Einstein form follows once LHS2692_1 through LHS2692_3 are parent-signed",
            "cannot be used while extra sectors or higher operators survive",
            "2619:ELH2619_2_lovelock_filter",
            "false",
        ),
        (
            "LHS2692_5_coefficient_owner",
            "EH normalization and local Lambda subtraction",
            "a=1/kappa_MTS and b=Lambda_loc are parent-owned with local background subtraction fixed before scoring",
            "MISSING_A1_KAPPA_OWNER_AND_LOCAL_SUBTRACTION",
            "Newton G and local Lambda convention are not fitted after the fact",
            "G/Lambda can absorb errors if not parent-owned",
            "2485:CS2485_0_a1_kappa;2485:CS2485_1_a0_lambda;2579:EDP2579_5_coupling_baseline",
            "false",
        ),
        (
            "LHS2692_6_residual_silence",
            "all retained non-EH LHS residuals",
            "DeltaE_munu = E_HD + E_projector + E_boundary + E_nonminimal + E_memory + E_nonlocal + E_aux is zero or source-backed bounded",
            "MISSING_RESIDUAL_ZERO_OR_BOUND_VECTOR",
            "local-GR claim can move from template to theorem/bounds",
            "modified-operator residual model remains live",
            "2619:RSS2619_6_verdict;2579:ENV2579_9_total",
            "false",
        ),
        (
            "LHS2692_7_source_and_gauss",
            "RHS source and measured Newton mass",
            "T_active=T_H, kappa fixed, and Hilbert/worldtube/Gauss mass are the same charge before orbital fitting",
            "MISSING_SOURCE_NORMALIZATION_AND_GAUSS_CHAIN",
            "Poisson/Newton follows without GM laundering",
            "can prove field equation shape but not measured inverse-square Newton",
            "2691:SMC2691_7_verdict;P8_charge_current_equality_DIRECT_ATTEMPT:CC7_closed_flux_and_Gauss_calibration",
            "false",
        ),
        (
            "LHS2692_8_bianchi_noether",
            "final divergence identity",
            "nabla_mu(G^{mu nu}+Lambda g^{mu nu}+DeltaE^{mu nu}) = kappa nabla_mu T_H^{mu nu} with residual exchange either zero or retained",
            "MISSING_FINAL_PARENT_NOETHER_CHAIN",
            "no hidden nonconservation/preferred-frame leak remains",
            "alpha3/preferred-frame channels can hide in unowned exchange",
            "2618:GRB2618_2_bianchi;2691:SMC2691_6_no_cancellation",
            "false",
        ),
        (
            "LHS2692_9_verdict",
            "exact local-GR conditional theorem",
            "LHS2692_1..8 imply Einstein equation plus Newton/PPN bridge; current corpus has not parent-signed the hypotheses",
            "EXACT_CONDITIONAL_THEOREM_READY_NOT_PARENT_DERIVED",
            "we now know the precise leap needed for derived local GR",
            "no local-GR/Newton/PPN/R10 claim",
            "LHS2692_0 through LHS2692_8",
            "false",
        ),
    ]
    return [
        {
            "theorem_id": row[0],
            "clause": row[1],
            "formal_requirement": row[2],
            "current_status": row[3],
            "if_signed": row[4],
            "if_unsigned": row[5],
            "source_anchor": row[6],
            "parent_signed": row[7],
            "closes_local_gr_piece": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def lovelock_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("LVK2692_0_dimension", "effective local public branch is four-dimensional", "CONDITIONALLY_ASSUMED_NOT_PARENT_PROVED", "cosmology/extra-dimensional or bulk branch not feeding local lab", "2579:EDP2579_0_EH_core"),
        ("LVK2692_1_locality", "local Markovian LHS after memory/history descent", "MISSING_LOCALITY_REDUCTION_OR_KERNEL_BOUND", "nonlocal/history kernels absent or bounded", "2619:ORP2619_6_nonlocal_history"),
        ("LVK2692_2_metric_only", "observed metric/coframe is the only long-range gravitational public field", "MISSING_PRIVATE_SECTOR_GAP_AND_READOUT_LOCK", "no scalar/vector/private stress remains in compact exterior", "2579:EDP2579_3_positive_gap;2579:EDP2579_6_boundary_readout"),
        ("LVK2692_3_second_order", "field equations are second order in local metric/coframe", "MISSING_HIGHER_CURVATURE_EXCLUSION_OR_SCALE", "R^2/Ricci^2/Weyl/torsion operators are zero or below bounds", "2485:DG2485_3_higher_curvature"),
        ("LVK2692_4_diffeomorphism", "local parent action has the right diffeomorphism/Noether identity", "PARTIAL_CONTRACT_NOT_COMPLETE_PARENT_ACTION", "Bianchi compatibility follows from a complete action", "2618:ANF2618_0_parent_action_partition"),
        ("LVK2692_5_boundary", "boundary/reference/improvement terms are silent or fixed before readout", "MISSING_BOUNDARY_ZERO_OR_BOUND", "no hidden local stress or charge flux from boundary choice", "2579:EDP2579_6_boundary_readout;2691:SMC2691_4_boundary_silence"),
        ("LVK2692_6_matter_coupling", "ordinary matter is minimally and universally coupled to the observed frame", "SOURCE_CLASSIFIER_NARROWED_NOT_CLOSED", "RHS becomes Hilbert source only", "2691:CLS2691_1_hilbert_matter;2691:SMC2691_7_verdict"),
        ("LVK2692_7_verdict", "all Lovelock/EH hypotheses for MTS local branch", "HYPOTHESES_NOT_PARENT_SIGNED", "Lovelock/EH theorem can be used as MTS derivation only after all clauses pass", "LVK2692_0 through LVK2692_6"),
    ]
    return [
        {
            "gate_id": row[0],
            "hypothesis": row[1],
            "current_status": row[2],
            "required_to_pass": row[3],
            "source_anchor": row[4],
            "gate_pass": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def newton_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NP2692_0_einstein_equation",
            "Einstein field equation from signed LHS/RHS",
            "G_munu + Lambda g_munu + DeltaE_munu = kappa T_H_munu + DeltaS_munu",
            "CONDITIONAL_FIELD_EQUATION",
            "DeltaE=0 and DeltaS=0 gives GR equation",
            "LHS/RHS residuals remain nonclaim",
        ),
        (
            "NP2692_1_local_lambda",
            "local background subtraction",
            "Lambda_loc is fixed/subtracted before local Poisson scoring",
            "MISSING_LOCAL_SUBTRACTION_CONVENTION",
            "lab/solar-system Poisson equation not contaminated by cosmology convention",
            "Lambda can become a hidden fit knob",
        ),
        (
            "NP2692_2_weak_field_00",
            "weak-field 00 component",
            "G_00 ~= 2 nabla^2 Phi/c^2, T_00 ~= rho_H c^2",
            "REFERENCE_TEMPLATE_CONDITIONAL",
            "with kappa=8 pi G/c^4, gives Poisson",
            "requires observed-frame metric/coframe lock",
        ),
        (
            "NP2692_3_kappa_source_owner",
            "coupling/source normalization",
            "kappa_MTS and rho_H are parent-owned in the same observed source frame",
            "MISSING_KAPPA_AND_SOURCE_CHARGE_OWNER",
            "G is not fitted into existence after the fact",
            "measured GM can be laundered through normalization",
        ),
        (
            "NP2692_4_poisson_equation",
            "Poisson limit",
            "nabla^2 Phi = 4 pi G_parent rho_H + R_Poisson",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "R_Poisson=0/bounded gives Newtonian field equation",
            "DeltaE_00, source shadow, kappa drift and boundary/projector terms remain",
        ),
        (
            "NP2692_5_exterior_gauss",
            "inverse-square exterior",
            "int nabla^2 Phi dV = 4 pi G_parent M_H, Phi=-G_parent M_H/r outside a closed source",
            "MISSING_WORLDTUBE_GAUSS_CLOSURE",
            "Newton orbit follows without orbital GM backfill",
            "worldtube/source mass and exterior charge equality remain open",
        ),
        (
            "NP2692_6_ppn_extension",
            "PPN completion",
            "gamma=1, beta=1, alpha_i=0 only after nonlinear EH completion and residual silence",
            "MISSING_NONLINEAR_AND_PREFERRED_FRAME_MAP",
            "local GR, not just Newton, becomes testable",
            "Poisson alone cannot prove gamma/beta/preferred-frame silence",
        ),
        (
            "NP2692_7_verdict",
            "Newton/Poisson theorem status",
            "EH LHS + Hilbert source + fixed kappa + Gauss worldtube closure imply Newton/Poisson",
            "EXACT_CONDITIONAL_NOT_CURRENT_CLAIM",
            "precise derivation route is available",
            "claim blocked until source normalization and residual rows close",
        ),
    ]
    return [
        {
            "derivation_id": row[0],
            "step": row[1],
            "formal_statement": row[2],
            "current_status": row[3],
            "if_signed": row[4],
            "if_unsigned": row[5],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def operator_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("ORP2692_0_total_DeltaE", "DeltaE_munu", "total left-hand deviation from Einstein operator", "E_LHS-(G_munu+Lambda g_munu)", "curvature_operator_units", "MISSING_EH_DOMINANCE_OR_BOUND", "local_GR;Newton;PPN;R10;clock;orbital", "2619:ORP2619_0_E_LHS_GR_residual;2691:RCP2691_5_c_lhs_GR"),
        ("ORP2692_1_higher_derivative", "c_HD", "higher-curvature/higher-derivative public metric operators", "c_R2 R^2+c_Ricci2 R_munu R^munu+c_boxR R box R", "length_power_by_operator", "MISSING_OPERATOR_BASIS_AND_SCALE", "R10;PPN;waves;cosmology", "2485:DG2485_3_higher_curvature"),
        ("ORP2692_2_aux_private_stress", "c_aux_private", "vertical/private field stress after attempted descent", "delta S_aux/delta g_obs", "operator_dependent", "MISSING_PRIVATE_SECTOR_GAP_OR_ZERO", "local_GR;PPN;clock;orbital", "2485:DG2485_4_vertical_derivatives;2579:EDP2579_3_positive_gap"),
        ("ORP2692_3_projector_readout", "c_projector_operator", "projector/readout variation or commutator residual", "E_projector or [d,Pi_M]J_H", "dimensionless_or_operator_units", "MISSING_PROJECTOR_IDENTITY_OR_BOUND", "Newton;WEP;PPN;orbital", "2691:RCP2691_4_c_projector"),
        ("ORP2692_4_boundary_reference", "c_boundary_reference", "boundary/reference/improvement LHS or charge residual", "DeltaE_boundary or Q_boundary", "boundary_operator_dependent", "MISSING_BOUNDARY_SILENCE_OR_BOUND", "Newton;local_GR;clock;orbital", "2691:RCP2691_3_c_boundary;2579:ENV2579_7_boundary"),
        ("ORP2692_5_nonminimal_source_geometry", "c_nonminimal", "ordinary matter coupled directly to MTS/geometric scalars", "f(X,Phi,labels)L_m or A(X)J_m", "operator_dependent", "MISSING_FORBID_RECLASSIFY_OR_BOUND", "WEP;clock;PPN;R10", "2691:RCP2691_2_c_nonminimal"),
        ("ORP2692_6_memory_coframe", "c_memory_frame", "memory/coframe/preferred-frame local residual", "E_memory+E_coframe+tau/local-frame residual", "operator_dependent", "MISSING_LOCAL_FRAME_LOCK_OR_PPN_BOUND", "PPN_alpha_i;clock;orbital", "2485:CS2485_6_c_memory_frame;2579:ENV2579_8_readout"),
        ("ORP2692_7_nonlocal_history", "K_history", "nonlocal/history kernel in local branch", "E_nonlocal[g,Phi;history]", "kernel_or_operator_dependent", "MISSING_LOCALITY_REDUCTION_OR_KERNEL_BOUND", "clock;orbital_hysteresis;cosmology;waves", "2619:ORP2619_6_nonlocal_history"),
        ("ORP2692_8_kappa_source_norm", "delta_kappa_source", "G/kappa/source-current normalization mismatch", "delta kappa + delta ell_J + source-frame residual", "dimensionless_or_GM_fraction", "MISSING_CONSTANT_KAPPA_AND_SOURCE_FRAME", "Newton;Gdot;PPN;clock", "2579:ENV2579_5_kappa;2579:ENV2579_6_ellJ"),
        ("ORP2692_9_worldtube_gauss", "delta_worldtube_Gauss", "Hilbert/worldtube/exterior Gauss mass mismatch", "M_Hilbert - M_Gauss_orbital before fitting", "GM_fraction_or_mass", "MISSING_WORLDTUBE_GAUSS_CLOSURE", "Newton;orbital;Cavendish;PPN", "P8_charge_current_equality_DIRECT_ATTEMPT:CC7_closed_flux_and_Gauss_calibration"),
        ("ORP2692_10_total_abs_envelope", "Delta_LHS_GR_abs", "absolute no-cancellation envelope over retained left-hand/Newton residuals", "sum_i |K_i c_i| + |delta_source_norm| + |delta_worldtube_Gauss|", "mixed_declared", "MISSING_COMPONENT_VALUES_AND_ARENA_KERNELS", "all local arenas", "ORP2692_0 through ORP2692_9"),
        ("ORP2692_11_nonclaim_lock", "claim_allowed", "local-GR/Newton/PPN/R10 claim status", "claim_allowed=false until Lovelock hypotheses and residual/source rows pass", "status", "NONCLAIM_LOCK", "all local arenas", "claim policy"),
    ]
    return [
        {
            "row_id": row[0],
            "symbol": row[1],
            "definition": row[2],
            "formal_expression": row[3],
            "units": row[4],
            "current_status": row[5],
            "observable_link": row[6],
            "source_anchor": row[7],
            "numeric_value_present": "false",
            "source_path_present": "true",
            "projection_ready": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def observable_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS2692_0_newton_poisson", "Newton/Poisson", "DeltaE_00;delta_kappa_source;delta_worldtube_Gauss;c_boundary_reference;c_projector_operator", "R_Poisson in nabla^2 Phi=4*pi*G*rho+R_Poisson", "MISSING_SOURCE_NORMALIZATION_AND_LHS_RESIDUAL_KERNELS"),
        ("OBS2692_1_ppn_gamma_beta", "PPN gamma/beta", "DeltaE_munu;c_HD;c_projector_operator;c_memory_frame", "gamma-1,beta-1 after measured source normalization", "MISSING_SECOND_ORDER_WEAK_FIELD_MAP"),
        ("OBS2692_2_preferred_frame", "PPN alpha_i", "c_memory_frame;c_aux_private_stress;boundary/projector exchange", "alpha1,alpha2,alpha3 residual vector", "MISSING_LOCAL_FRAME_LOCK_OR_BOUND"),
        ("OBS2692_3_r10_yukawa", "R10 fifth force", "c_HD;c_aux_private_stress;K_history;c_nonminimal", "alpha(lambda) or non-Yukawa short-range envelope", "MISSING_OPERATOR_TO_ALPHA_LAMBDA_MAP"),
        ("OBS2692_4_clocks", "clock/redshift", "c_nonminimal;c_memory_frame;delta_kappa_source", "alpha_clock and local time drift residual", "MISSING_CLOCK_PROJECTION"),
        ("OBS2692_5_orbital", "orbital/ephemeris", "delta_worldtube_Gauss;c_boundary_reference;c_projector_operator;DeltaE_munu", "perihelion/radial hair/Gdot residuals", "MISSING_ORBITAL_READOUT_WITHOUT_GM_BACKFILL"),
        ("OBS2692_6_cosmology", "cosmology", "DeltaE_munu;c_HD;K_history;c_memory_frame", "background/growth/lensing residuals in separate cosmology branch", "HELD_SEPARATE_NOT_LOCAL_GR_SUBSTITUTE"),
        ("OBS2692_7_verdict", "empirical use", "all retained residuals", "local tests require theorem-zero or source-backed coefficient values/kernels", "OBSERVABLE_MAP_READY_NONCLAIM"),
    ]
    return [
        {
            "map_id": row[0],
            "arena": row[1],
            "residual_inputs": row[2],
            "observable_projection": row[3],
            "current_status": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2692_0_all_signed", "true", "true", "true", "true", "true", "false", "false", "THEOREM_READY_IF_PARENT_SIGNED"),
        ("DRY2692_1_lovelock_missing", "false", "true", "true", "true", "true", "false", "false", "REJECT_LOVELOCK_HYPOTHESES_UNSIGNED"),
        ("DRY2692_2_source_classifier_missing", "true", "false", "true", "true", "true", "false", "false", "REJECT_SOURCE_CLASSIFIER_UNSIGNED"),
        ("DRY2692_3_source_norm_missing", "true", "true", "false", "true", "true", "false", "false", "REJECT_SOURCE_NORMALIZATION_UNSIGNED"),
        ("DRY2692_4_residual_unbounded", "true", "true", "true", "false", "true", "false", "false", "REJECT_LHS_RESIDUALS_UNBOUNDED"),
        ("DRY2692_5_bianchi_missing", "true", "true", "true", "true", "false", "false", "false", "REJECT_BIANCHI_NOETHER_UNSIGNED"),
        ("DRY2692_6_cancellation_only", "false", "false", "false", "false", "false", "true", "false", "REJECT_CANCELLATION_ONLY_PASS"),
        ("DRY2692_7_fitted_gm_backfill", "true", "true", "false", "true", "true", "false", "true", "REJECT_FITTED_GM_BACKFILL"),
    ]
    return [
        {
            "case_id": row[0],
            "lovelock_hypotheses_signed": row[1],
            "source_classifier_signed": row[2],
            "source_normalization_signed": row[3],
            "lhs_residuals_zero_or_bounded": row[4],
            "bianchi_noether_signed": row[5],
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
    if case["cancellation_only"] == "true":
        return "REJECT_CANCELLATION_ONLY_PASS"
    if case["fitted_gm_backfill"] == "true":
        return "REJECT_FITTED_GM_BACKFILL"
    if case["lovelock_hypotheses_signed"] != "true":
        return "REJECT_LOVELOCK_HYPOTHESES_UNSIGNED"
    if case["source_classifier_signed"] != "true":
        return "REJECT_SOURCE_CLASSIFIER_UNSIGNED"
    if case["source_normalization_signed"] != "true":
        return "REJECT_SOURCE_NORMALIZATION_UNSIGNED"
    if case["lhs_residuals_zero_or_bounded"] != "true":
        return "REJECT_LHS_RESIDUALS_UNBOUNDED"
    if case["bianchi_noether_signed"] != "true":
        return "REJECT_BIANCHI_NOETHER_UNSIGNED"
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
        ("CG2692_0_parent_action", "complete local parent action inventory and variation", "FAIL_PARENT_ACTION_INVENTORY_UNSIGNED", "LHS2692_1_parent_variation", "false"),
        ("CG2692_1_lovelock", "Lovelock/EH hypotheses are parent-signed", "FAIL_LOVELOCK_HYPOTHESES_NOT_SIGNED", "LVK2692_7_verdict", "false"),
        ("CG2692_2_lhs_residuals", "DeltaE_munu residual vector is zero or source-backed bounded", "FAIL_OPERATOR_RESIDUAL_PACK_NONCLAIM", "ORP2692_10_total_abs_envelope", "false"),
        ("CG2692_3_source_classifier", "RHS source classifier/source map is complete", "FAIL_SOURCE_CLASSIFIER_LEDGER_READY_NOT_THEOREM", "2691:SMC2691_7_verdict", "false"),
        ("CG2692_4_source_normalization", "kappa/source/worldtube/Gauss charge chain is parent-owned", "FAIL_SOURCE_NORMALIZATION_AND_GAUSS_UNSIGNED", "NP2692_5_exterior_gauss", "false"),
        ("CG2692_5_bianchi", "final Noether/Bianchi identity has no unowned residual exchange", "FAIL_FINAL_PARENT_NOETHER_CHAIN_UNSIGNED", "LHS2692_8_bianchi_noether", "false"),
        ("CG2692_6_observable_maps", "PPN/R10/clock/orbital projections have values/kernels", "FAIL_OBSERVABLE_PROJECTIONS_MISSING", "OBS2692_7_verdict", "false"),
        ("CG2692_7_guardrails", "cancellation-only and fitted-GM backfill shortcuts are refused", "PASS_GUARD_ONLY", "DRY2692_6;DRY2692_7", "true"),
        ("CG2692_8_verdict", "local GR/Newton/PPN/R10 branch can claim pass", "CLAIM_BLOCKED", "CG2692_0 through CG2692_7", "false"),
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
            "decision_id": "DEC2692_0_exact_contract",
            "decision": "LOCAL_GR_REDUCTION_CONTRACT_IS_NOW_EXACT_CONDITIONAL",
            "reason": "The theorem shape is no longer vague: parent-signed Lovelock/EH hypotheses plus source normalization and residual silence imply GR/Newton.",
            "status": "USEFUL_ADVANCE_NOT_CLAIM",
            "next_dependency": "prove Lovelock hypotheses from MTS local branch or fill operator residual vector",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2692_1_no_gr_import",
            "decision": "EH_LOVELOCK_FILTER_IS_A_GATE_NOT_A SMUGGLE",
            "reason": "The EH template is allowed only after MTS proves metric-only, local, second-order, diffeo-invariant, boundary-silent public dynamics.",
            "status": "IMPORT_GUARD_ACTIVE",
            "next_dependency": "MTS proof of public metric-only branch and residual-sector silence",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2692_2_operator_residual",
            "decision": "MODIFIED_OPERATOR_ROUTE_REMAINS EXPLICIT",
            "reason": "If any Lovelock/EH hypothesis fails, the surviving object is a coefficient row tied to local tests, not hand-waving.",
            "status": "RESIDUAL_VECTOR_STAGED",
            "next_dependency": "theorem-zero certificates or source-backed values/kernels for ORP2692 rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2692_3_next",
            "decision": "MOVE_TO_LOVELOCK_HYPOTHESIS_PROVER_NEXT",
            "reason": "The best non-circular leap is to attack the hypotheses directly: public metric-only, second-order locality, residual-sector silence, and source/Gauss owner.",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2693 Lovelock-hypothesis prover or operator residual acquisition",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2692_0_selected",
            "kind": "selected",
            "target_doc": "2693-Y5-R2FR-Lovelock-hypothesis-prover-or-left-hand-operator-residual-acquisition.md",
            "target_script": "scripts/Y5_R2FR_Lovelock_hypothesis_prover_or_left_hand_operator_residual_acquisition_2693.py",
            "purpose": "attempt to parent-sign the local metric-only second-order diffeo-invariant EH/Lovelock hypotheses from MTS primitives; if any clause fails, stage exact operator residual acquisition rows",
            "acceptance_gate": "either LVK2692 clauses are theorem-signed without importing GR, or ORP2692 coefficients/kernels become explicit nonclaim acquisition rows with local observables",
            "forbidden_shortcuts": "EH as axiom; source-side proof as GR proof; orbital GM backfill; cancellation-only pass; unowned boundary/reference choice; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "NEXT2692_1_parallel",
            "kind": "parallel_held",
            "target_doc": "2693b-Y5-R2FR-source-normalization-worldtube-Gauss-owner-or-residual-pack.md",
            "target_script": "scripts/Y5_R2FR_source_normalization_worldtube_Gauss_owner_or_residual_pack_2693b.py",
            "purpose": "close kappa/source/worldtube/Gauss charge equality needed for Newton without fitted GM laundering",
            "acceptance_gate": "Hilbert source mass, parent charge, exterior Gauss flux and measured Newton mass are the same object before orbital fitting, or residual rows are explicit",
            "forbidden_shortcuts": "using fitted orbital GM as source proof; treating Poisson template as measured Newton proof",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2692_0_bridge", "local GR bridge", "EXACT_CONDITIONAL_READY", "we have a precise theorem contract, not a claim"),
        ("STATUS2692_1_lovelock", "EH/Lovelock hypotheses", "NOT_PARENT_SIGNED", "public metric-only, second-order, local and boundary-silent branch remains to prove"),
        ("STATUS2692_2_newton", "Newton/Poisson", "CONDITIONAL_SOURCE_GAUSS_BLOCKED", "source normalization/worldtube/Gauss owner still open"),
        ("STATUS2692_3_residuals", "operator residuals", "FINITE_VECTOR_STAGED_NONCLAIM", "each failure mode is now a named ORP2692 coefficient row"),
        ("STATUS2692_4_claims", "claim status", "ALL_LOCAL_CLAIMS_BLOCKED", "no local-GR/Newton/PPN/R10/clock/orbital claim"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2693 Lovelock-hypothesis prover or operator residual acquisition",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2692_{name}",
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
    theorem: list[dict[str, Any]],
    lovelock: list[dict[str, Any]],
    newton: list[dict[str, Any]],
    operator_pack: list[dict[str, Any]],
    observable_map: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    theorem_conditional = any(
        row["theorem_id"] == "LHS2692_9_verdict"
        and row["current_status"] == "EXACT_CONDITIONAL_THEOREM_READY_NOT_PARENT_DERIVED"
        and row["claim_allowed"] == "false"
        for row in theorem
    )
    lovelock_blocks = any(row["gate_id"] == "LVK2692_7_verdict" and row["gate_pass"] == "false" for row in lovelock)
    newton_conditional = any(row["derivation_id"] == "NP2692_7_verdict" and row["current_status"] == "EXACT_CONDITIONAL_NOT_CURRENT_CLAIM" for row in newton)
    residual_pack_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["score_ready"] == "false"
        and row["numeric_value_present"] == "false"
        for row in operator_pack
    )
    observable_nonclaim = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in observable_map)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2692_8_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2693" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2692_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2692_exact_theorem_contract_not_promoted", theorem_conditional, "exact local-GR conditional theorem contract is written but not promoted"),
        ("VAL2692_lovelock_gate_blocks", lovelock_blocks, "Lovelock/EH hypotheses remain unsigned and block claims"),
        ("VAL2692_newton_conditional_blocks", newton_conditional, "Newton/Poisson bridge is conditional and source/Gauss blocked"),
        ("VAL2692_operator_pack_nonclaim", residual_pack_nonclaim, "operator residual pack remains nonclaim/not score-ready"),
        ("VAL2692_observable_map_nonclaim", observable_nonclaim, "observable map is ready as nonclaim acquisition guidance only"),
        ("VAL2692_dryrun_refusals", dryrun_ok, "dry-run refuses missing Lovelock/source/residual/Bianchi clauses, cancellation-only pass and fitted GM backfill"),
        ("VAL2692_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2692_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2692_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2692_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2692_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2692_next_target_selected", next_target_ok, "2693 Lovelock hypothesis/operator residual target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2692_OVERALL",
            "passed": as_bool(overall),
            "detail": "2692 writes the exact local-GR conditional theorem contract, blocks promotion, and stages the LHS operator residual vector",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    lovelock: list[dict[str, Any]],
    newton: list[dict[str, Any]],
    operator_pack: list[dict[str, Any]],
    observable_map: list[dict[str, Any]],
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
                "# 2692 - Y5/R2FR GR Left-Hand Einstein Newton Limit or Operator Residual Pack",
                "",
                "## Private Verdict",
                "",
                "This is the bridge we actually wanted: local GR is not being assumed, but the exact contract is now sharp. If MTS can parent-sign a local four-dimensional, metric-only/coframe-only, second-order, diffeomorphism-invariant, boundary-silent public branch, then the Lovelock/EH filter forces the left-hand operator into Einstein form up to coefficients and Lambda. With the 2691 source classifier plus source/Gauss normalization, Newton follows conditionally.",
                "",
                "That is a real path, but not yet a win. The current corpus has not proved the Lovelock hypotheses from MTS primitives, has not killed the full DeltaE_munu vector, and has not closed source normalization/worldtube/Gauss without fitted GM backfill.",
                "",
                "So the result is: exact conditional theorem contract written; local-GR/Newton still blocked; surviving failure modes are now finite operator residual/acquisition rows. No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, or R10 claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## LHS GR Master Theorem Contract",
                "",
                markdown_table(theorem),
                "",
                "## Lovelock Hypothesis Gate",
                "",
                markdown_table(lovelock),
                "",
                "## Newton Poisson Normalization Derivation",
                "",
                markdown_table(newton),
                "",
                "## Operator Residual Pack",
                "",
                markdown_table(operator_pack),
                "",
                "## Residual To Observable Map",
                "",
                markdown_table(observable_map),
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
    theorem = master_theorem_rows()
    lovelock = lovelock_gate_rows()
    newton = newton_derivation_rows()
    operator_pack = operator_pack_rows()
    observable_map = observable_map_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["master_theorem"], theorem)
    write_csv(OUTPUTS["lovelock_gate"], lovelock)
    write_csv(OUTPUTS["newton_derivation"], newton)
    write_csv(OUTPUTS["operator_pack"], operator_pack)
    write_csv(OUTPUTS["observable_map"], observable_map)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_master_theorem"], theorem)
    write_csv(BRANCH_OUTPUTS["local_operator_pack"], operator_pack)
    write_csv(BRANCH_OUTPUTS["wep_operator_pack"], operator_pack)
    write_csv(BRANCH_OUTPUTS["source_weight_operator_pack"], operator_pack)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_target)

    branch_rows = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validation = validation_rows(
        source_rows=source_rows,
        theorem=theorem,
        lovelock=lovelock,
        newton=newton,
        operator_pack=operator_pack,
        observable_map=observable_map,
        dryrun_results=dry_results,
        claim_gates=claim_gates,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_document(
        source_rows=source_rows,
        theorem=theorem,
        lovelock=lovelock,
        newton=newton,
        operator_pack=operator_pack,
        observable_map=observable_map,
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
