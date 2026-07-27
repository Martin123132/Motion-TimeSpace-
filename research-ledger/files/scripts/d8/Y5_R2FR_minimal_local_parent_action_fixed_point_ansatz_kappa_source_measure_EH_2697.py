from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2697"
BRANCH_ID = "Y5_R2FR_MINIMAL_LOCAL_PARENT_ACTION_FIXED_POINT_ANSATZ_KAPPA_SOURCE_MEASURE_EH_2697"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2697-Y5-R2FR-minimal-local-parent-action-fixed-point-ansatz-kappa-source-measure-EH.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2697_SOURCE_REGISTER.csv",
    "action_blocks": RESIDUALS / "P8_Y5_R2FR_2697_MINIMAL_PARENT_ACTION_BLOCKS.csv",
    "fixed_point_conditions": RESIDUALS / "P8_Y5_R2FR_2697_FIXED_POINT_CONDITIONS.csv",
    "variation_chain": RESIDUALS / "P8_Y5_R2FR_2697_VARIATION_DERIVATION_CHAIN.csv",
    "symbol_match_queue": RESIDUALS / "P8_Y5_R2FR_2697_MTS_SYMBOL_MATCH_QUEUE_NONCLAIM.csv",
    "residual_demotion": RESIDUALS / "P8_Y5_R2FR_2697_RESIDUAL_DEMOTION_VECTOR_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2697_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2697_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2697_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2697_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2697_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2697_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2697_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_action_blocks": LOCAL_BOUNDS / "minimal_parent_action_blocks_2697_NONCLAIM.csv",
    "local_symbol_match_queue": LOCAL_BOUNDS / "MTS_symbol_match_queue_2697_NONCLAIM.csv",
    "local_residual_demotion": LOCAL_BOUNDS / "local_fixed_point_residual_demotion_2697_NONCLAIM.csv",
    "wep_residual_demotion": WEP_RESIDUALS / "local_fixed_point_residual_demotion_2697_NONCLAIM.csv",
    "source_weight_residual_demotion": SOURCE_WEIGHT / "LOCAL_FIXED_POINT_RESIDUAL_DEMOTION_2697_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2697_MTS_SYMBOLS_TO_FIXED_POINT_ACTION_MAP_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2697_2696_DOC",
        "relative_path": "2696-Y5-R2FR-source-measure-Meff-flux-closure-after-conditional-kappa-gate.md",
        "required_needles": ["NEXT2696_0_selected", "BUILD_MINIMAL_LOCAL_PARENT_FIXED_POINT", "VAL2696_OVERALL"],
        "purpose": "imports selected minimal local parent-action fixed-point target",
    },
    {
        "source_id": "SRC2697_511_FIXED_POINT",
        "relative_path": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "required_needles": ["A511_0_EH_core", "FP511_1_double_zero_nonEH_coupling", "RU511_1"],
        "purpose": "imports historical minimal fixed-point contract and symbol mapping handoff",
    },
    {
        "source_id": "SRC2697_2692_GR_BRIDGE",
        "relative_path": "2692-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "required_needles": ["LHS2692_9_verdict", "NP2692_7_verdict", "CG2692_8_verdict"],
        "purpose": "imports exact EH/Newton conditional bridge and no-claim gates",
    },
    {
        "source_id": "SRC2697_2694_SECTOR_QUEUE",
        "relative_path": "2694-Y5-R2FR-sector-positive-operator-silence-certificates-or-residual-values.md",
        "required_needles": ["CERT2694_10_verdict", "REQ2694_9_total", "LGG2694_4_verdict"],
        "purpose": "imports sector-silence queue and residual requirements",
    },
    {
        "source_id": "SRC2697_2695_KAPPA",
        "relative_path": "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md",
        "required_needles": ["ZFD2695_2_local_equation", "KAD2695_8_verdict", "VAL2695_OVERALL"],
        "purpose": "imports conditional topological kappa derivation route",
    },
    {
        "source_id": "SRC2697_2696_SOURCE_MEASURE",
        "relative_path": "2696-Y5-R2FR-source-measure-Meff-flux-closure-after-conditional-kappa-gate.md",
        "required_needles": ["SMA2696_10_verdict", "CPS2696_6_MTS_transfer", "PIM2696_5_verdict"],
        "purpose": "imports parent Hamiltonian/Noether charge route for M_eff",
    },
    {
        "source_id": "SRC2697_510_WORLDTUBE",
        "relative_path": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "required_needles": ["T510_2_MTS_transfer_condition", "WG510_8_PPN_metric_readout", "MR510_7_PPN_tail"],
        "purpose": "imports worldtube source-measure and PPN residual runner",
    },
    {
        "source_id": "SRC2697_NEWTON_STACK",
        "relative_path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "required_needles": ["SN1_EH_or_R11_operator_zero", "SN7_constant_universal_Geff", "SN11_second_order_PPN_source_stability"],
        "purpose": "imports Newton/source-normalization stack requirements",
    },
    {
        "source_id": "SRC2697_CONSTANT_GM_INPUT",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "required_needles": ["P8_Geff_time_drift", "P8_Meff_conservation", "P8_nonlinear_beta_source_residue"],
        "purpose": "imports local residual runner requirements for coupling, source mass, and PPN tail",
    },
    {
        "source_id": "SRC2697_CC_RESIDUALS",
        "relative_path": "source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "required_needles": ["Delta_nonEH", "Delta_flux", "Delta_cal"],
        "purpose": "imports source-measure residual pieces",
    },
    {
        "source_id": "SRC2697_R11_QUEUE",
        "relative_path": "source-intake/mts_residuals/R11_OPERATOR_VECTOR_FILL_QUEUE.csv",
        "required_needles": ["source_normalization_operator", "vector_preferred_frame", "boundary_topological_terms"],
        "purpose": "imports local operator-vector queue",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


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
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
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


def action_block_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACT2697_0_EH_core", "S_EH=(2*kappa0)^-1 int sqrt(-g_obs)(R[g_obs]-2 Lambda_loc)", "metric/coframe public spin-2 operator and EH covariant charge", "local public branch is 4D, metric/coframe-only, local, second order, diffeo-invariant, boundary controlled", "Lovelock/EH bridge can be used", "MISSING_LOVELOCK_HYPOTHESES_FROM_MTS"),
        ("ACT2697_1_kappa_topological", "S_kappa_top=int kappa_eff dA_3", "global/topological coupling owner", "A_3 and kappa_eff are parent-owned; delta_A3 gives d kappa_eff=0; source/range/frame labels absent", "G_eff has no kappa drift/source/range hair", "MISSING_PARENT_ADOPTION_FROM_2695"),
        ("ACT2697_2_universal_matter", "S_matter[psi,g_obs] with no leading MTS/source-label prefactor", "same-frame Hilbert source and WEP/source universality", "ordinary matter couples to one observed metric/coframe and source variation uses the same frame", "T_H is the RHS source and source charge is species-blind", "MISSING_SOURCE_FRAME_AND_SPECIES_BLINDNESS"),
        ("ACT2697_3_parent_charge", "S_parent supplies theta, J_tau, Q_tau, H_tau", "Hamiltonian/Noether source mass owner", "observed tau is fixed; H_tau is integrable with fixed reference before orbital readout", "M_eff is a parent charge, not fitted GM", "MISSING_PARENT_PHASE_SPACE_AND_REFERENCE"),
        ("ACT2697_4_PiM_descent", "Pi_M J_H = Q_M[tau] or derived mass-channel projection", "projector becomes derived bookkeeping", "Pi_M is parent-derived, variation-owned, charge-preserving, and not fitted per source/radius", "no projector/source-normalization patch", "MISSING_PIM_DESCENT_AND_VARIATION_ZERO"),
        ("ACT2697_5_extra_sector_silence", "S_extra[Phi]=int sqrt(-g)(-1/2 G_AB dPhi^A dPhi^B - V(Phi) + sum_i C_i(Phi) O_i[g])", "motion/time/domain/memory/range fields become locally silent", "Phi=Phi0 solves E_A=0; C_i(Phi0)=0; partial_A C_i(Phi0)=0; positive Hessian/operator gap; no boundary/source flux", "q_loc and extra local fields vanish by variation, not plateau", "MISSING_FIELD_SPECIFIC_DOUBLE_ZERO_OR_GAP"),
        ("ACT2697_6_boundary_reference", "S_boundary=S_GHY+S_ref+S_top/exact", "finite charge and no hidden boundary mass flux", "reference subtraction and exact/topological terms fixed before readout; no linking-sphere flux", "worldtube/source charge is not shifted by bookkeeping", "MISSING_BOUNDARY_NO_FLUX_REFERENCE_LOCK"),
        ("ACT2697_7_weak_field_readout", "g_readout=g_obs+O((Phi-Phi0)^2); H_tau -> Gauss mass; PPN residual vector explicit", "Newton and PPN observable bridge", "linear readout leakage vanishes and second-order gamma/beta/preferred-frame terms are derived or bounded", "Poisson/Newton/PPN can be computed", "MISSING_PPN_SOURCE_OPERATOR_EXPANSION"),
        ("ACT2697_8_transition_scale", "ell_tr/L_cg from operator spectrum/source scale/topological activation", "prevents local/cosmology/galaxy hand switching", "activation scale is derived from the same parent action, not chosen by arena", "local GR and cosmology/galaxy behavior coexist coherently", "MISSING_TRANSITION_SCALE_DERIVATION"),
        ("ACT2697_9_residual_branch", "S_residual or Delta ledger with source-backed coefficients", "honest fallback if any block fails", "failed blocks map to explicit residual rows with units/kernels/observable projections", "closure-only branch remains testable", "MISSING_NUMERIC_RESIDUAL_VALUES"),
    ]
    return [
        {
            "block_id": row[0],
            "action_block": row[1],
            "purpose": row[2],
            "required_signature": row[3],
            "if_signed": row[4],
            "current_gap": row[5],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def fixed_point_condition_rows() -> list[dict[str, Any]]:
    rows = [
        ("FP2697_0_local_branch", "there exists a compact stationary local exterior branch", "E_A(Phi0)=0; L_tau Phi0=0; source support excluded from exterior annulus", "local branch is an actual solution, not a readout patch", "not_matched_to_current_MTS"),
        ("FP2697_1_metric_only_public", "only observed metric/coframe remains long-range and public", "private/vertical/domain/memory fields are auxiliary, gapped, topological, or residual-bounded", "Lovelock/EH hypotheses can become available", "not_parent_signed"),
        ("FP2697_2_double_zero", "all non-EH couplings have double zero at the fixed point", "C_i(Phi0)=0 and partial_A C_i(Phi0)=0; F_1=0", "no first-order scalar/vector/source-normalization hair", "required_not_proved"),
        ("FP2697_3_positive_gap", "non-gauge extra modes have positive source-free operator", "int <delta Phi,L delta Phi> >= m_min^2 ||delta Phi||^2 with zero source/boundary flux", "Delta Phi=0 or exponentially bounded in local exterior", "sector_by_sector_open"),
        ("FP2697_4_topological_kappa", "kappa_eff is a global/topological local integration constant", "delta_A3 S_kappa_top -> d kappa_eff=0", "no Gdot/range/source kappa drift from kappa sector", "conditional_from_2695_not_adopted"),
        ("FP2697_5_parent_source_charge", "M_eff is the parent Hamiltonian/Noether charge", "M_source[W]=H_tau[S]-H_tau[ref]=M_eff before orbital fit", "source mass is not fitted orbital GM", "conditional_from_2696_not_inherited"),
        ("FP2697_6_boundary_no_flux", "boundary/reference terms carry no local mass or PPN flux", "int_boundary Delta(theta,Q,tau)=0 or fixed topological/reference subtraction", "worldtube/Gauss source measure remains stable", "open"),
        ("FP2697_7_Bianchi_Noether", "Noether/Bianchi identity has no hidden exchange owner", "nabla_mu(E_EH+DeltaE)^{mu nu}=kappa nabla_mu T_H^{mu nu}+explicit residuals", "motion is conserved/geodesic after residuals vanish", "open"),
        ("FP2697_8_PPN_readout", "weak-field readout matches GR through required PPN order or residuals are scored", "gamma-1=0; beta-1=0; alpha_i=0; zeta_i=0; xi=0 or bounded", "local GR, not only Newton-leading-order", "not_derived"),
        ("FP2697_9_transition_control", "local fixed point and cosmology/galaxy active branch are separated by derived activation", "ell_tr/L_cg from spectrum/source scale/topological class", "unification not arena switching", "open"),
        ("FP2697_10_verdict", "fixed-point contract status", "ACT2697 and FP2697 clauses would derive the local GR/Newton branch if matched", "contract coherent but not current MTS proof", "CONTRACT_READY_NOT_PARENT_MATCHED"),
    ]
    return [
        {
            "condition_id": row[0],
            "condition": row[1],
            "mathematical_test": row[2],
            "derives": row[3],
            "current_MTS_status": row[4],
            "condition_passed_now": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAR2697_0_kappa", "ACT2697_1", "delta_A3 int kappa_eff dA_3", "d kappa_eff=0", "constant local G_eff if source/range/frame blindness is also signed", "CONDITIONAL_FROM_2695"),
        ("VAR2697_1_extra_fields", "ACT2697_5", "delta_Phi S_extra around Phi0", "L_AB delta Phi^B = source_A + boundary_A", "positive source-free/gap plus zero boundary gives delta Phi=0/bounded", "NOT_FIELD_MATCHED"),
        ("VAR2697_2_metric", "ACT2697_0 + ACT2697_5", "delta_g S_parent", "G_munu+Lambda g_munu = kappa T_H_munu + DeltaE_munu + DeltaS_munu", "EH equation if DeltaE and DeltaS are theorem-zero or bounded", "CONDITIONAL_NOT_SIGNED"),
        ("VAR2697_3_matter", "ACT2697_2", "delta_g S_matter and matter equations", "T_H from same observed frame; source current conserved if no exchange residual", "RHS source is Hilbert/worldtube-compatible", "OPEN"),
        ("VAR2697_4_charge", "ACT2697_3", "Noether current J_tau=dQ_tau+C_tau", "H_tau[S2]-H_tau[S1]=0 in source-free exterior if constraints/flux vanish", "M_eff radial/time closure", "CONDITIONAL_FROM_2696"),
        ("VAR2697_5_PiM", "ACT2697_4", "Pi_M J_H = Q_M[tau] and delta(Pi_M J_H) owned", "projector readout is parent charge descent", "no fitted GM/projector mask", "UNSIGNED"),
        ("VAR2697_6_Gauss", "ACT2697_7", "weak-field 00 equation plus closed source charge", "nabla^2 Phi = 4 pi G_parent rho_H + R_Poisson; exterior Phi=-G_parent M_eff/r if residuals vanish", "Newtonian inverse-square source-normalized limit", "CONDITIONAL_NOT_SIGNED"),
        ("VAR2697_7_PPN", "ACT2697_7", "second-order weak-field expansion", "gamma=1,beta=1,alpha_i=zeta_i=xi=0 plus residual vector", "local GR test branch", "NOT_DERIVED"),
        ("VAR2697_8_transition", "ACT2697_8", "spectrum/source-scale/topological activation calculation", "ell_tr/L_cg or local/cosmology branch selector", "same parent action controls scale separation", "NOT_DERIVED"),
        ("VAR2697_9_verdict", "all blocks", "compose variation chain", "local GR/Newton follows only if every block is matched or residual-bounded", "exact action contract ready; current MTS not promoted", "ROUTE_BUILT_NOT_PROMOTED"),
    ]
    return [
        {
            "chain_id": row[0],
            "action_block_ref": row[1],
            "variation_or_identity": row[2],
            "derived_equation": row[3],
            "meaning_if_closed": row[4],
            "current_status": row[5],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def symbol_match_rows() -> list[dict[str, Any]]:
    rows = [
        ("SYM2697_0_kappa_eff", "kappa_eff;A_3", "ACT2697_1", "topological global coupling sector", "2695 candidate route exists but parent adoption unsigned", "source/range/frame blindness and companion equation"),
        ("SYM2697_1_g_obs", "g_obs;e_obs", "ACT2697_0;ACT2697_2;ACT2697_7", "single observed metric/coframe for matter, charge, clocks, rods, orbits", "same-frame route conditional", "source variation and readout frame proof"),
        ("SYM2697_2_Gamma_eff_Khat_q", "Gamma_eff;K_hat;q_loc", "ACT2697_5;VAR2697_1;VAR2697_2", "extra-sector fixed point and local residual current", "not mapped to positive double-zero operator", "operator L_AB, source term, boundary term, units"),
        ("SYM2697_3_chiD_Qcoh_domain", "chi_D;Qcoh;domain selector", "ACT2697_5;ACT2697_6;ACT2697_8", "domain/projector/topological local silence or transition scale", "sector queue open", "double zero, no-vector stress, transition derivation"),
        ("SYM2697_4_memory_time", "memory kernels;time/flow fields", "ACT2697_5;ACT2697_8", "cosmology active branch but local compact silence", "memory double-zero required not proved", "local kernel gap/support and activation scale"),
        ("SYM2697_5_PiM_JH", "Pi_M;J_H;H_tau;Q_tau", "ACT2697_3;ACT2697_4", "parent Hamiltonian source charge and derived projector", "2696 selected safer charge route but MTS transfer unsigned", "Pi_M descent and variation ledger"),
        ("SYM2697_6_boundary_ref", "boundary/reference/improvement terms", "ACT2697_6", "fixed charge reference and zero mass flux", "boundary no-flux open", "reference subtraction and linking-sphere flux proof"),
        ("SYM2697_7_nonEH_operator", "DeltaE_munu;R11 operator vector", "ACT2697_0;ACT2697_5;ACT2697_7", "EH-only or bounded residual operator branch", "operator vector unfilled", "basis, coefficients, kernels, observable projection"),
        ("SYM2697_8_matter_source", "ordinary matter source labels;species weights", "ACT2697_2", "universal source/current functor", "source classifier narrowed not closed", "no source-prefactor theorem or residual species vector"),
        ("SYM2697_9_ppn_readout", "gamma,beta,alpha_i,zeta_i,xi", "ACT2697_7", "2PN/local-GR observable branch", "not derived", "weak-field expansion after source normalization"),
        ("SYM2697_10_transition", "ell_tr;L_cg;activation functional", "ACT2697_8", "local/cosmology/galaxy scale separation", "open", "derive from operator spectrum/source scale/topology"),
    ]
    return [
        {
            "symbol_id": row[0],
            "MTS_object": row[1],
            "action_block_target": row[2],
            "required_role": row[3],
            "current_status": row[4],
            "next_required_evidence": row[5],
            "matched_now": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def residual_demotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("RDM2697_0_total_operator", "DeltaE_munu", "EH fixed point not matched", "R11/local_GR/PPN/R10", "operator basis, coefficients, kernels", "MISSING_EH_ONLY_OR_OPERATOR_VALUES"),
        ("RDM2697_1_kappa", "Delta_G;kappa drift", "topological kappa not parent-adopted", "Gdot/R10/source WEP", "2695 kappa residual values or parent adoption", "IMPORTED_CONDITIONAL_NOT_SCOREABLE"),
        ("RDM2697_2_source_mass", "Delta_flux;Delta_cal;Delta_PiM", "source-measure/Hamiltonian charge not inherited", "Newton/orbital/PPN", "2696 M_eff residual values or source-charge proof", "MISSING_MEFF_VALUES"),
        ("RDM2697_3_extra_sector", "Delta_extra;mu_extra", "extra fields not double-zero/gapped", "PPN/R10/WEP/clocks", "field-specific F1=0, mass gap, source flux proof or coefficients", "MISSING_DOUBLE_ZERO_GAP_VALUES"),
        ("RDM2697_4_boundary", "Delta_symp;boundary_reference", "boundary/reference no-flux not signed", "Newton/orbital/clocks/PPN", "boundary theorem or source-backed bound", "MISSING_BOUNDARY_ZERO_OR_BOUND"),
        ("RDM2697_5_frame_matter", "Delta_frame;eta_source_AB", "same observed frame/source species functor not signed", "WEP/clocks/preferred frame", "matter functor/source-label forgetting proof or values", "MISSING_FRAME_SOURCE_VALUES"),
        ("RDM2697_6_nonlocal_memory", "K_history;memory_frame", "local memory silence not derived", "Gdot/clocks/orbits/cosmology split", "kernel gap/support and transition scale", "MISSING_KERNEL_BOUND"),
        ("RDM2697_7_PPN", "Delta_PPN;gamma_minus_1;delta_beta_source;alpha_i", "second-order weak-field readout not derived", "solar-system PPN", "2PN expansion or residual vector", "MISSING_PPN_VECTOR"),
        ("RDM2697_8_transition", "ell_tr/L_cg residual", "activation scale not derived", "local/cosmology/galaxy unification", "operator spectrum/source-scale derivation or residual branch", "MISSING_TRANSITION_DERIVATION"),
        ("RDM2697_9_total", "Delta_local_GR_abs", "any open block remains", "all local arenas", "sum/envelope with no cancellation-only credit", "MISSING_COMPONENT_VALUES_AND_KERNELS"),
    ]
    return [
        {
            "residual_id": row[0],
            "symbol": row[1],
            "if_action_block_fails": row[2],
            "observable_link": row[3],
            "required_artifact": row[4],
            "current_status": row[5],
            "numeric_value_present": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    rows = [
        ("DRY2697_0_all_blocks_signed", True, True, True, True, True, True, True, True, True, False, False, "CONDITIONAL_FIXED_POINT_CONTRACT_READY_NOT_PUBLIC_CLAIM"),
        ("DRY2697_1_symbol_mapping_missing", True, True, True, True, True, True, True, True, False, False, False, "REJECT_MTS_SYMBOLS_NOT_MATCHED"),
        ("DRY2697_2_kappa_missing", False, True, True, True, True, True, True, True, True, False, False, "REJECT_KAPPA_UNSIGNED"),
        ("DRY2697_3_EH_missing", True, False, True, True, True, True, True, True, True, False, False, "REJECT_EH_LOVELOCK_UNSIGNED"),
        ("DRY2697_4_source_missing", True, True, False, True, True, True, True, True, True, False, False, "REJECT_SOURCE_MEASURE_UNSIGNED"),
        ("DRY2697_5_double_zero_missing", True, True, True, False, True, True, True, True, True, False, False, "REJECT_DOUBLE_ZERO_MISSING"),
        ("DRY2697_6_gap_missing", True, True, True, True, False, True, True, True, True, False, False, "REJECT_POSITIVE_GAP_MISSING"),
        ("DRY2697_7_boundary_missing", True, True, True, True, True, False, True, True, True, False, False, "REJECT_BOUNDARY_FLUX_OPEN"),
        ("DRY2697_8_PPN_missing", True, True, True, True, True, True, False, True, True, False, False, "CONDITIONAL_NEWTON_ONLY_NO_LOCAL_GR"),
        ("DRY2697_9_transition_missing", True, True, True, True, True, True, True, False, True, False, False, "LOCAL_GR_CONTRACT_ONLY_UNIFICATION_SCALE_OPEN"),
        ("DRY2697_10_residual_values_present", False, False, False, False, False, False, False, False, False, True, False, "NONCLAIM_RESIDUAL_BRANCH_ONLY"),
        ("DRY2697_11_closure_only", False, False, False, False, False, False, False, False, False, False, True, "DEMOTE_TO_CLOSURE_ONLY_NO_DERIVED_LOCAL_GR"),
    ]
    return [
        {
            "case_id": row[0],
            "kappa_signed": as_bool(row[1]),
            "EH_metric_only_signed": as_bool(row[2]),
            "source_measure_signed": as_bool(row[3]),
            "double_zero_signed": as_bool(row[4]),
            "positive_gap_signed": as_bool(row[5]),
            "boundary_silent": as_bool(row[6]),
            "PPN_ready": as_bool(row[7]),
            "transition_derived": as_bool(row[8]),
            "symbols_matched": as_bool(row[9]),
            "residual_values_present": as_bool(row[10]),
            "closure_only": as_bool(row[11]),
            "expected_status": row[12],
            "expected_claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["closure_only"] == "true":
        return "DEMOTE_TO_CLOSURE_ONLY_NO_DERIVED_LOCAL_GR"
    if case["symbols_matched"] == "false" and case["residual_values_present"] == "true":
        return "NONCLAIM_RESIDUAL_BRANCH_ONLY"
    if case["symbols_matched"] == "false":
        return "REJECT_MTS_SYMBOLS_NOT_MATCHED"
    if case["kappa_signed"] == "false":
        return "REJECT_KAPPA_UNSIGNED"
    if case["EH_metric_only_signed"] == "false":
        return "REJECT_EH_LOVELOCK_UNSIGNED"
    if case["source_measure_signed"] == "false":
        return "REJECT_SOURCE_MEASURE_UNSIGNED"
    if case["double_zero_signed"] == "false":
        return "REJECT_DOUBLE_ZERO_MISSING"
    if case["positive_gap_signed"] == "false":
        return "REJECT_POSITIVE_GAP_MISSING"
    if case["boundary_silent"] == "false":
        return "REJECT_BOUNDARY_FLUX_OPEN"
    if case["PPN_ready"] == "false":
        return "CONDITIONAL_NEWTON_ONLY_NO_LOCAL_GR"
    if case["transition_derived"] == "false":
        return "LOCAL_GR_CONTRACT_ONLY_UNIFICATION_SCALE_OPEN"
    return "CONDITIONAL_FIXED_POINT_CONTRACT_READY_NOT_PUBLIC_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        actual = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "actual_status": actual,
                "status_match": as_bool(actual == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2697_0_contract_coherent", "minimal action blocks are sufficient in principle for derived local GR", "PASS_CONDITIONAL_CONTRACT", "ACT2697_0-ACT2697_9;FP2697_10"),
        ("CG2697_1_MTS_symbol_match", "actual MTS objects are matched to every action block with first variations", "FAIL_SYMBOL_MATCH_QUEUE_OPEN", "SYM2697_0-SYM2697_10"),
        ("CG2697_2_kappa", "topological kappa is parent-adopted and source/range/frame blind", "FAIL_KAPPA_PARENT_ADOPTION_UNSIGNED", "ACT2697_1;FP2697_4"),
        ("CG2697_3_EH_Lovelock", "metric-only local second-order diffeo-invariant public branch is parent-signed", "FAIL_EH_LOVELOCK_UNSIGNED", "ACT2697_0;FP2697_1"),
        ("CG2697_4_source_measure", "M_eff is parent Hamiltonian/Noether source charge and Gauss/orbital readout is derived", "FAIL_SOURCE_MEASURE_UNSIGNED", "ACT2697_3;ACT2697_4;FP2697_5"),
        ("CG2697_5_double_zero_gap", "extra sectors have double zeros, positive gaps, and no boundary/source flux", "FAIL_DOUBLE_ZERO_GAP_UNSIGNED", "ACT2697_5;FP2697_2;FP2697_3"),
        ("CG2697_6_boundary_Bianchi", "boundary/reference and Noether/Bianchi exchange are closed or bounded", "FAIL_BOUNDARY_BIANCHI_UNSIGNED", "ACT2697_6;FP2697_6;FP2697_7"),
        ("CG2697_7_PPN", "weak-field readout matches GR through PPN order or residual vector is scored", "FAIL_PPN_READOUT_UNSIGNED", "ACT2697_7;FP2697_8"),
        ("CG2697_8_transition", "local/cosmology/galaxy transition scale is action-derived", "FAIL_TRANSITION_SCALE_UNSIGNED", "ACT2697_8;FP2697_9"),
        ("CG2697_9_verdict", "MTS has derived local GR/Newton now", "CLAIM_BLOCKED", "all gates above"),
    ]
    return [
        {
            "gate_id": row[0],
            "pass_condition": row[1],
            "current_status": row[2],
            "evidence": row[3],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2697_0_contract", "MINIMAL_FIXED_POINT_CONTRACT_BUILT", "A coherent local parent-action fixed point exists as a contract: EH core, topological kappa, universal matter, parent source charge, extra-sector double zeros/gap, boundary silence, PPN readout.", "REAL_PROGRESS", "map actual MTS symbols into blocks"),
        ("DEC2697_1_no_claim", "CURRENT_MTS_NOT_MATCHED", "The contract is not yet a proof because Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory, Pi_M, kappa, and readout variables are not all matched with first variations.", "NO_CLAIM", "do symbol matching next"),
        ("DEC2697_2_double_zero", "F1_ZERO_AND_MASS_GAP_ARE_THE_PRICE", "Derived local GR needs double-zero couplings and positive source-free operators; otherwise local residuals are physical, not embarrassing but not GR.", "DERIVATION_GATE", "field-specific matching or residual values"),
        ("DEC2697_3_PiM", "PIM_MUST_DESCEND_FROM_CHARGE", "Pi_M survives only as a derived projection of the parent Hamiltonian/Noether mass charge.", "ANTI_PATCH_GUARD", "match Pi_M/J_H/H_tau in 2698"),
        ("DEC2697_4_next", "MAP_MTS_SYMBOLS_TO_FIXED_POINT_BLOCKS", "The next non-circular move is a symbol-by-symbol map, not another overview.", "NEXT_ROUTE_SELECTED", "run 2698 symbol-to-action map"),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "rationale": row[2],
            "status": row[3],
            "next_action": row[4],
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT2697_0_selected",
            "selected_symbol_mapping",
            "2698-Y5-R2FR-MTS-symbols-to-minimal-local-fixed-point-action-map.md",
            "scripts/Y5_R2FR_MTS_symbols_to_minimal_local_fixed_point_action_map_2698.py",
            "map kappa_eff, A_3, g_obs/e_obs, Gamma_eff, K_hat, q_loc, chi_D, Qcoh, memory/time fields, Pi_M, J_H, H_tau, boundary reference, and PPN readout variables into the 2697 action blocks",
            "each MTS object is either assigned to an action block with first-variation evidence, or demoted to a residual row with units/kernels/source path",
            "another broad recap; claiming the contract is a proof; hiding unmatched symbols; fitted orbital GM; public/GitHub action; formalization-workbench edits",
        ),
        (
            "NEXT2697_1_fallback",
            "fallback_residual_runner",
            "2698b-Y5-R2FR-local-fixed-point-residual-values-and-kernels.md",
            "scripts/Y5_R2FR_local_fixed_point_residual_values_and_kernels_2698b.py",
            "fill residual values/kernels for every unmatched action block",
            "residual rows become numeric/sourced/units-clean while still nonclaim",
            "pretending unmatched blocks vanish",
        ),
    ]
    return [
        {
            "target_id": row[0],
            "selection_status": row[1],
            "target_doc": row[2],
            "target_script": row[3],
            "purpose": row[4],
            "acceptance_gate": row[5],
            "forbidden_shortcuts": row[6],
            "private_only": "true",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2697_0_fixed_point", "minimal parent action", "CONTRACT_BUILT_NOT_MTS_PROOF", "we now have the smallest coherent local-GR fixed-point contract", False, "map MTS symbols into it"),
        ("STATUS2697_1_kappa", "kappa/G_eff", "CONDITIONAL_BLOCK", "topological route is included but adoption remains unsigned", False, "symbol match and parent signature"),
        ("STATUS2697_2_source_measure", "M_eff/source mass", "CONDITIONAL_BLOCK", "Hamiltonian charge route is included but MTS transfer remains unsigned", False, "map Pi_M/J_H/H_tau"),
        ("STATUS2697_3_extra_sectors", "motion/time/domain/memory", "DOUBLE_ZERO_GAP_REQUIRED", "q_loc silence must follow from variation, not plateau", False, "field-specific F1/gap evidence"),
        ("STATUS2697_4_local_GR", "Newton/PPN/local GR", "CLAIM_BLOCKED_BUT_PATH_SHARP", "exact prerequisites are now finite and auditable", False, "2698 symbol map"),
        ("STATUS2697_5_public", "GitHub/public", "NO_ACTION", "private checkpoint only", False, "no push"),
    ]
    return [
        {
            "status_id": row[0],
            "area": row[1],
            "current_state": row[2],
            "meaning": row[3],
            "claim_ready": as_bool(row[4]),
            "next_action": row[5],
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in BRANCH_OUTPUTS.items():
        ok, count, message = parse_csv(path)
        rows.append(
            {
                "branch_key": key,
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "csv_parse_ok": as_bool(ok),
                "row_count": count,
                "parse_message": message,
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    symbol_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    action_contract_complete = len(action_rows) >= 10 and any(row["block_id"] == "ACT2697_9_residual_branch" for row in action_rows)
    fixed_contract_complete = len(fixed_rows) >= 10 and any(row["condition_id"] == "FP2697_2_double_zero" for row in fixed_rows) and any(row["condition_id"] == "FP2697_3_positive_gap" for row in fixed_rows)
    variation_chain_complete = any(row["chain_id"] == "VAR2697_0_kappa" for row in variation_rows) and any(row["chain_id"] == "VAR2697_4_charge" for row in variation_rows) and any(row["chain_id"] == "VAR2697_9_verdict" for row in variation_rows)
    symbols_nonclaim = all(row["matched_now"] == "false" and row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in symbol_rows)
    residuals_nonclaim = all(row["numeric_value_present"] == "false" and row["score_ready"] == "false" and row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in residual_rows)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates) and any(row["gate_id"] == "CG2697_9_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2698" in read_text(OUTPUTS["next_target"]) and "symbols" in read_text(OUTPUTS["next_target"]).lower()
    no_public_claim = all("claim_allowed" not in row or row["claim_allowed"] == "false" for row in action_rows + fixed_rows + symbol_rows + residual_rows + claim_gates)
    checks = [
        ("VAL2697_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2697_action_contract_complete", action_contract_complete, "minimal parent action blocks cover EH, kappa, matter, charge, Pi_M, extra sectors, boundary, PPN, transition, and residual fallback"),
        ("VAL2697_fixed_point_conditions_complete", fixed_contract_complete, "fixed-point conditions include double-zero and positive-gap gates"),
        ("VAL2697_variation_chain_complete", variation_chain_complete, "variation chain includes kappa, source charge, and no-promotion verdict"),
        ("VAL2697_symbol_queue_nonclaim", symbols_nonclaim, "MTS symbol matching queue remains explicit and nonclaim"),
        ("VAL2697_residual_demotion_nonclaim", residuals_nonclaim, "residual demotion rows remain nonnumeric and nonclaim"),
        ("VAL2697_dryrun_refusals", dryrun_ok, "dry-run refuses unmatched symbols, missing kappa/EH/source/double-zero/gap/boundary/PPN/transition, and closure-only shortcuts"),
        ("VAL2697_claim_gates_block_claims", claim_blocked, "claim gates block local-GR/Newton promotion"),
        ("VAL2697_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2697_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2697_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2697_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2697_next_target_selected", next_target_ok, "2698 MTS symbols to fixed-point action map selected"),
        ("VAL2697_no_public_claim", no_public_claim, "no row allows a public or GitHub claim"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2697_OVERALL",
            "passed": as_bool(overall),
            "detail": "2697 builds the minimal local parent-action fixed-point contract, keeps current MTS unpromoted, and selects symbol-to-action matching as the next concrete derivation step",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    symbol_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
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
                "# 2697 - Y5/R2FR Minimal Local Parent-Action Fixed-Point Ansatz: Kappa, Source Measure, EH",
                "",
                "## Private Verdict",
                "",
                "This is the current best shot at the GR/Newton bridge as an actual derivation contract rather than a pile of closures.",
                "",
                "The minimal local branch is:",
                "",
                "`S_local = S_EH[g_obs] + S_kappa_top[kappa_eff,A_3] + S_matter[psi,g_obs] + S_charge/theta/Q_tau + S_extra[Phi,g_obs] + S_boundary + S_residual`.",
                "",
                "If the current MTS symbols instantiate these blocks with the required first variations, then local GR is no longer being smuggled in. Kappa becomes topological, `M_eff` becomes a parent Hamiltonian/Noether source charge, extra fields vanish by double-zero plus positive-gap fixed-point equations, the EH/Lovelock operator is inherited, and Newton/PPN follow by the standard weak-field readout.",
                "",
                "That is a coherent route. It is not yet a claim. Current MTS has not matched `Gamma_eff`, `K_hat`, `q_loc`, `chi_D`, `Qcoh`, memory/time variables, `Pi_M`, `J_H`, `H_tau`, boundary references, and PPN readout into the action blocks with first-variation evidence. So 2697 builds the contract and selects symbol mapping as the next non-circular move.",
                "",
                "No measured-GM, Newton, PPN, local-GR, R10, WEP, clock, orbital, GitHub, or public claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Minimal Parent Action Blocks",
                "",
                markdown_table(action_rows),
                "",
                "## Fixed-Point Conditions",
                "",
                markdown_table(fixed_rows),
                "",
                "## Variation Derivation Chain",
                "",
                markdown_table(variation_rows),
                "",
                "## MTS Symbol Match Queue",
                "",
                markdown_table(symbol_rows),
                "",
                "## Residual Demotion Vector",
                "",
                markdown_table(residual_rows),
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
    action_rows = action_block_rows()
    fixed_rows = fixed_point_condition_rows()
    variation_rows = variation_chain_rows()
    symbol_rows = symbol_match_rows()
    residual_rows = residual_demotion_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["action_blocks"], action_rows)
    write_csv(OUTPUTS["fixed_point_conditions"], fixed_rows)
    write_csv(OUTPUTS["variation_chain"], variation_rows)
    write_csv(OUTPUTS["symbol_match_queue"], symbol_rows)
    write_csv(OUTPUTS["residual_demotion"], residual_rows)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_action_blocks"], action_rows)
    write_csv(BRANCH_OUTPUTS["local_symbol_match_queue"], symbol_rows)
    write_csv(BRANCH_OUTPUTS["local_residual_demotion"], residual_rows)
    write_csv(BRANCH_OUTPUTS["wep_residual_demotion"], residual_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_residual_demotion"], residual_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_target)

    branch_rows = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validation = validation_rows(
        source_rows=source_rows,
        action_rows=action_rows,
        fixed_rows=fixed_rows,
        variation_rows=variation_rows,
        symbol_rows=symbol_rows,
        residual_rows=residual_rows,
        dryrun_results=dry_results,
        claim_gates=claim_gates,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_document(
        source_rows=source_rows,
        action_rows=action_rows,
        fixed_rows=fixed_rows,
        variation_rows=variation_rows,
        symbol_rows=symbol_rows,
        residual_rows=residual_rows,
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
