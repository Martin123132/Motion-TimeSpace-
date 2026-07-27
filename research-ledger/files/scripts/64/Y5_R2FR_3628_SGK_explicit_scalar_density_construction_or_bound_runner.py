from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3628"
BRANCH_ID = "MTS_R2FR_Y5_SGK_EXPLICIT_SCALAR_DENSITY_CONSTRUCTION_OR_BOUND_RUNNER_3628"
DOC = ROOT / "3628-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3628_SOURCE_REGISTER.csv",
        "scalar_density_candidates": RESIDUALS / "P8_Y5_R2FR_3628_EXPLICIT_SCALAR_DENSITY_CANDIDATES.csv",
        "metric_response_comparison": RESIDUALS / "P8_Y5_R2FR_3628_KMETRIC_KHAT_COMPARISON.csv",
        "fixed_point_gate": RESIDUALS / "P8_Y5_R2FR_3628_FIXED_POINT_DOUBLE_ZERO_GATE.csv",
        "qloc_bound_runner": RESIDUALS / "P8_Y5_R2FR_3628_QLOC_TGK_BOUND_RUNNER_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3628_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3628_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3628_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Gamma_Khat_Kmetric_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3628_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3627",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3627_NEXT_TARGET.csv"),
            "needle": "explicit Gamma_eff scalar-density construction",
            "role": "3627 selected explicit scalar-density and K_metric comparison as the next real derivation target.",
        },
        {
            "source_id": "metric_response_3627",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv"),
            "needle": "K_metric",
            "role": "3627 wrote the conditional metric-response formula to be made explicit here.",
        },
        {
            "source_id": "helmholtz_gate_3627",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3627_SGK_HELMHOLTZ_ACTION_GATE.csv"),
            "needle": "Gamma scalar-density response",
            "role": "3627 identifies candidate A as the least-scrutiny route.",
        },
        {
            "source_id": "double_zero_3627",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3627_EULER_DOUBLE_ZERO_BOUNDARY_GATE.csv"),
            "needle": "F_1/double-zero gate",
            "role": "fixed-point and first-variation gates inherited from 3627.",
        },
        {
            "source_id": "gk_candidates",
            "path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "needle": "GK514_A_metric_response_scalar_density",
            "role": "older scalar-density, positive auxiliary, topological, and residual branch candidates.",
        },
        {
            "source_id": "metric_contract",
            "path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv"),
            "needle": "MR514_1_Khat_metric_response",
            "role": "requirements for Gamma_eff scalar density, K_hat metric response, Ward identity, and double zero.",
        },
        {
            "source_id": "metric_match_audit",
            "path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"),
            "needle": "MA515_1_Khat_metric_response",
            "role": "prior audit showing K_hat was not matched to a metric response in the current corpus.",
        },
        {
            "source_id": "response_doublet_contract",
            "path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "needle": "RD516_1_even_scalar_density",
            "role": "response-doublet route with even scalar density, metric response, positive operator, and source-coupling gates.",
        },
        {
            "source_id": "stress_rewrite",
            "path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv"),
            "needle": "SR513_0_define_extra_stress",
            "role": "q_loc/T_GK algebraic rewrite that all scalar-density candidates must own or bound.",
        },
        {
            "source_id": "residual_demotion",
            "path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv"),
            "needle": "QR513_0_nonvariational_stress",
            "role": "fallback if scalar-density ownership fails.",
        },
        {
            "source_id": "bound_rows_3627",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3627_QLOC_TGK_BOUND_ROWS.csv"),
            "needle": "QTB3627_4_TGK_stress_norm",
            "role": "nonclaim q_loc/T_GK bound rows inherited from 3627.",
        },
        {
            "source_id": "ppn_component_rows_3626",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv"),
            "needle": "MISSING_QLOC_OR_COFRAME_PROJECTION",
            "role": "PPN/Newton local residual rows that remain blocked until q_loc/T_GK is owned or bounded.",
        },
    ]


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in source_map():
        path = Path(source["path"])
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source["source_id"],
                "path": source["path"],
                "exists": exists,
                "needle": source["needle"],
                "needle_found": exists and contains(path, source["needle"]),
                "role": source["role"],
            }
        )
    return rows


def scalar_density_candidate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "candidate_id": "GSD3628_0_potential_background",
            "ansatz": "S_GK=-int sqrt(-g)[Gamma_0+V(Phi)]",
            "fields": "scalar/order fields Phi^A",
            "units_requirement": "Gamma_eff has stress-density/action-density units in the same local frame as DeltaE_MTS",
            "metric_response_formula": "K_metric^{mu nu}=0 if V has no explicit metric dependence; T_GK^{mu nu}=[Gamma_0+V]g^{mu nu}",
            "khat_match_requirement": "K_hat must be zero/pure background in this sector",
            "fixed_point_zero_gate": "Gamma_0+V(Phi0) must be background-subtracted and partial_A V(Phi0)=0",
            "what_this_buys": "constant vacuum value can be absorbed into Lambda_eff; first leakage vanishes only at a stationary point",
            "current_status": "MATHEMATICALLY_VALID_TOO_WEAK_FOR_GENERAL_KHAT",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "candidate_id": "GSD3628_1_gradient_elastic",
            "ansatz": "S_GK=-int sqrt(-g)[V(Phi)+1/2 G_AB(Phi) g^{rho sigma} nabla_rho Phi^A nabla_sigma Phi^B]",
            "fields": "scalar/elastic local fields Phi^A",
            "units_requirement": "G_AB and V must set stress-density units without fitted readout selectors",
            "metric_response_formula": "K_metric^{mu nu}=G_AB nabla^mu Phi^A nabla^nu Phi^B plus metric-dependence terms from G_AB",
            "khat_match_requirement": "K_hat must equal the gradient/elastic anisotropic response tensor under the same convention",
            "fixed_point_zero_gate": "nabla Phi0=0, V(Phi0) subtracted, partial_A V(Phi0)=0, positive Hessian/gap",
            "what_this_buys": "standard variational route from a local action to Ward-owned q_loc and mass-gap/no-hair suppression",
            "current_status": "PROMISING_TEMPLATE_SYMBOL_MATCH_MISSING",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "candidate_id": "GSD3628_2_even_response_doublet",
            "ansatz": "S_GK=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB g^{rho sigma} nabla_rho Z^A nabla_sigma Z^B+O(Z^4)]",
            "fields": "exchange-even response doublet variables Z^A built from R_+^A-R_-^A or equivalent local residual coordinates",
            "units_requirement": "M_AB Z^A Z^B and H_AB nabla Z nabla Z must carry stress-density units with source-independent normalization",
            "metric_response_formula": "K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B plus metric/coefficient response terms",
            "khat_match_requirement": "K_hat must be identified with this K_metric and Z^A must be the physical q_loc/PPN residual vector, not a bookkeeping shadow",
            "fixed_point_zero_gate": "Z=0 and nabla Z=0 gives T_GK=0 after Gamma_0 subtraction; evenness gives partial_A T_GK|0=0",
            "what_this_buys": "this is the first clean construction where F_1=0 follows by symmetry instead of being asserted",
            "current_status": "BEST_CONDITIONAL_ROUTE_F1_ZERO_BY_EVENNESS_PARENT_MAPPING_MISSING",
            "source_path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "candidate_id": "GSD3628_3_exact_topological_or_improvement",
            "ansatz": "S_GK=int dB_GK or int topological_density",
            "fields": "boundary/topological data",
            "units_requirement": "boundary charge units must map to the same Hamiltonian/source normalization as local mass",
            "metric_response_formula": "bulk K_metric is zero or an improvement tensor; all physical content moves to boundary/symplectic terms",
            "khat_match_requirement": "K_hat must be an exact/improvement stress and all linked-surface flux must be zero or fixed-reference",
            "fixed_point_zero_gate": "bulk q_loc can vanish, but source mass and alpha3 channels still require no-flux/handoff proof",
            "what_this_buys": "can remove bulk leakage without adding propagating fields, but cannot erase boundary physics",
            "current_status": "BOUNDARY_FLUX_RISK_OPEN_NONCLAIM",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "candidate_id": "GSD3628_4_wave_flux_Poynting_Maxwell_like",
            "ansatz": "S_flux=-int sqrt(-g)[1/4 W_AB F^A_{rho sigma}F^{B rho sigma}]",
            "fields": "antisymmetric wave/flux strengths F^A_{mu nu} and constitutive matrix W_AB",
            "units_requirement": "W_AB F^2 must be normalized as physical stress density; Poynting/vector flux cannot be hidden inside a scalar closure",
            "metric_response_formula": "K_metric^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}; T_flux^{mu nu}=Gamma_flux g^{mu nu}-K_metric^{mu nu}",
            "khat_match_requirement": "K_hat may contain this stress only if the MTS EM/wave sector declares F, W, current J, and boundary flux",
            "fixed_point_zero_gate": "local gravitational-vacuum silence requires F=0 or a separately conserved physical EM/radiation stress already present in T_matter",
            "what_this_buys": "keeps the Poynting-vector intuition alive as an owned action branch, but prevents using wave flux to fake a local-GR zero",
            "current_status": "USEFUL_EM_STRESS_TEMPLATE_NOT_QLOC_ZERO_PROOF",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "candidate_id": "GSD3628_5_composite_minimal_spine",
            "ansatz": "S_GK=S_even_response_doublet+S_exact_boundary+S_physical_flux_if_present",
            "fields": "Z^A response doublets, boundary charge variables, and explicit physical flux fields",
            "units_requirement": "all pieces must share one local source-normalization frame and one G_eff/kappa_eff convention",
            "metric_response_formula": "K_metric=K_Z+K_boundary_improvement+K_flux; T_GK=Gamma_total g-K_metric",
            "khat_match_requirement": "existing K_hat must decompose into exactly these pieces with no residual knob",
            "fixed_point_zero_gate": "Z branch gives F1=0; boundary branch no-flux; flux branch either absent or counted as ordinary physical stress",
            "what_this_buys": "most defensible route from MTS symbols to local GR without a plateau axiom",
            "current_status": "SELECTED_CONDITIONAL_SPINE_NOT_PARENT_SIGNED",
            "source_path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def metric_response_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "comparison_id": "KMC3628_0_convention",
            "target_piece": "stress convention",
            "computed_from_candidate": "For S_GK=-int sqrt(-g) Gamma_eff, use T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}, K_metric^{mu nu}:=-2 E_g^{mu nu}[Gamma_eff] with derivative/boundary terms included.",
            "required_existing_match": "all existing Gamma_eff/K_hat appearances must use this one sign and volume convention",
            "current_evidence": "3627 writes the convention conditionally; older files do not yet enforce one canonical convention everywhere",
            "residual_if_unmatched": "R_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}",
            "status": "CONVENTION_DECLARED_FOR_3628_NOT_GLOBAL_PARENT_LOCKED",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "comparison_id": "KMC3628_1_potential",
            "target_piece": "potential/background scalar",
            "computed_from_candidate": "K_metric=0, so T_GK=[Gamma_0+V]g after background subtraction",
            "required_existing_match": "K_hat=0 in this sector and V_A(Phi0)=0",
            "current_evidence": "no source-backed K_hat=0 sector declaration found in current corpus",
            "residual_if_unmatched": "R_K=K_hat",
            "status": "TOO_WEAK_FOR_CURRENT_KHAT_MATCH",
            "source_path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "comparison_id": "KMC3628_2_gradient_elastic",
            "target_piece": "gradient/elastic anisotropic stress",
            "computed_from_candidate": "K_metric^{mu nu}=G_AB nabla^mu Phi^A nabla^nu Phi^B plus coefficient metric-response terms",
            "required_existing_match": "K_hat must decompose as G_AB nabla Phi nabla Phi plus declared coefficient terms",
            "current_evidence": "no explicit K_hat tensor decomposition with G_AB/Phi fields found in the current source set",
            "residual_if_unmatched": "R_K=K_hat-G_AB nabla Phi nabla Phi-coefficient_response",
            "status": "MATCH_MISSING_RESIDUAL_RETAINED",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "comparison_id": "KMC3628_3_even_response_doublet",
            "target_piece": "response doublet metric stress",
            "computed_from_candidate": "K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B plus metric/coefficient terms; mass potential contributes to Gamma g, not anisotropic K",
            "required_existing_match": "Z^A must be the actual local residual/PPN vector and K_hat must equal this metric response",
            "current_evidence": "RD516 marks this route candidate_written_not_matched / not_checked_current_MTS",
            "residual_if_unmatched": "R_K=K_hat-K_Z and R_Z=physical_residual_vector-Z",
            "status": "BEST_ROUTE_BUT_PARENT_MAP_UNSIGNED",
            "source_path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "comparison_id": "KMC3628_4_wave_flux",
            "target_piece": "Poynting/Maxwell-like stress",
            "computed_from_candidate": "K_metric^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}; Ward residual becomes a current/flux exchange term, not a free zero",
            "required_existing_match": "F, W, J, and boundary flux must be explicit; physical EM/radiation stress must not be double-counted or hidden",
            "current_evidence": "current Gamma/Khat local-GR branch has no declared F/W/J owner in the inspected source set",
            "residual_if_unmatched": "R_flux=unowned Poynting/current stress contribution",
            "status": "VALID_ACTION_SHAPE_RETAINED_FOR_EM_BRANCH_NOT_LOCAL_GR_CLAIM",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "comparison_id": "KMC3628_5_verdict",
            "target_piece": "K_hat=K_metric claim",
            "computed_from_candidate": "candidate K_metric formulas exist for potential, gradient, even doublet, exact boundary, and flux branches",
            "required_existing_match": "existing MTS K_hat must be one of these formulas or a declared sum with no remainder",
            "current_evidence": "match audit still says K_hat metric response is missing",
            "residual_if_unmatched": "R_K^{mu nu} remains a scored local residual",
            "status": "KMETRIC_CONSTRUCTED_KHAT_MATCH_NOT_CLAIMED",
            "source_path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def fixed_point_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_0_fixed_point_definition",
            "condition": "local compact vacuum fixed point",
            "exact_requirement": "Z^A=0, nabla Z^A=0, Phi^A=Phi0 stationary, unforced physical flux absent or counted as T_matter, boundary reference fixed",
            "derivation_status": "CONSTRUCTED_AS_CANDIDATE_NOT_PARENT_SELECTED",
            "effect_if_true": "T_GK zeroth-order local residual can be zero/background only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_1_background_subtraction",
            "condition": "Gamma_0 and V(Phi0) subtraction",
            "exact_requirement": "Gamma_eff(Phi0) is absorbed into Lambda_eff or reference Hamiltonian before local PPN/source readout",
            "derivation_status": "STANDARD_ROUTE_WRITTEN_NOT_PARENT_LOCKED",
            "effect_if_true": "constant scalar value does not act as a local force",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_2_F1_zero",
            "condition": "first variation zero",
            "exact_requirement": "partial_A T_GK^{mu nu}|0=0; in the even Z action this follows from Z-parity and Gamma_0 subtraction",
            "derivation_status": "F1_ZERO_DERIVED_FOR_EVEN_RESPONSE_TEMPLATE_ONLY",
            "effect_if_true": "linear fifth-force/PPN/source-normalization leakage is removed for that template",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_3_positive_operator",
            "condition": "local no-hair/mass gap",
            "exact_requirement": "M_AB positive and H_AB elliptic/self-adjoint after constraints/gauge removal",
            "derivation_status": "FORMAL_REQUIREMENT_WRITTEN_NUMERIC_OR_PARENT_PROOF_MISSING",
            "effect_if_true": "source-free compact exterior gives Z=0 or exponentially bounded hair",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_4_source_coupling_zero",
            "condition": "coupling/source silence",
            "exact_requirement": "J_Z=0 for compact local vacuum, or the coupling coefficient is source-backed and below local bounds",
            "derivation_status": "HARD_BLOCK_REMAINS_COUPLING_NOT_DERIVED",
            "effect_if_true": "Euler equations do not re-source Z around ordinary matter",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_5_boundary_no_flux",
            "condition": "boundary/symplectic no flux",
            "exact_requirement": "boundary terms from variation of S_GK have zero/fixed linked-surface force and Hamiltonian mass handoff is retained",
            "derivation_status": "OPEN_BOUNDARY_HANDOFF_REQUIRED",
            "effect_if_true": "bulk q_loc silence does not leak through alpha3/source-normalization channels",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "FPG3628_6_verdict",
            "condition": "local-GR reduction from S_GK",
            "exact_requirement": "all fixed point, K_hat=K_metric, Z=physical residual, J_Z=0, positive operator, and boundary gates pass",
            "derivation_status": "DOUBLE_ZERO_MECHANISM_FOUND_PARENT_OWNERSHIP_MISSING_NO_CLAIM",
            "effect_if_true": "would turn q_loc/T_GK from closure into a derived local-GR silence mechanism",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def qloc_bound_runner_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "QBR3628_0_RK_residual",
            "quantity": "R_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}",
            "new_reduction": "explicit K_metric formulas are now available for candidate action classes",
            "missing_input": "MISSING_KHAT_TENSOR_DECOMPOSITION_AND_SYMBOL_MATCH",
            "fallback_bound": "score ||R_K|| through PPN/Newton/source-normalization envelope if not zero",
            "status": "BLOCKED_NONCLAIM",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3627_QLOC_TGK_BOUND_ROWS.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "QBR3628_1_RZ_map",
            "quantity": "R_Z^A=physical local residual vector - Z^A",
            "new_reduction": "even response doublet gives automatic F1=0 only for variables that are the actual residual coordinates",
            "missing_input": "MISSING_Z_TO_QLOC_PPN_NEWTON_SOURCE_MAP",
            "fallback_bound": "retain q_loc, alpha3, gamma, beta, xi, Gdot and source-mass residual rows",
            "status": "BLOCKED_NONCLAIM",
            "source_path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "QBR3628_2_JZ_coupling",
            "quantity": "J_Z source/coupling coefficient",
            "new_reduction": "the coupling is now isolated as the next hard variable: local source can regenerate Z even when the action is even",
            "missing_input": "MISSING_PARENT_COUPLING_ZERO_OR_NUMERIC_COEFFICIENT",
            "fallback_bound": "derive J_Z=0 from quotient/current symmetry or fill numeric coefficient against local bounds",
            "status": "NEXT_HARD_TARGET_BLOCKED_NONCLAIM",
            "source_path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "QBR3628_3_flux_branch",
            "quantity": "Poynting/wave flux stress",
            "new_reduction": "Maxwell-like scalar density gives a legitimate stress-action shape rather than vibes",
            "missing_input": "MISSING_F_W_J_BOUNDARY_OWNER_IN_CURRENT_MTS_LOCAL_GR_BRANCH",
            "fallback_bound": "route to EM/charge branch or count as ordinary physical stress, not local-GR residual silence",
            "status": "EM_BRANCH_RETAINED_NONCLAIM",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "QBR3628_4_boundary",
            "quantity": "boundary/symplectic flux",
            "new_reduction": "exact/topological route remains viable only with no-flux or Hamiltonian handoff rows",
            "missing_input": "MISSING_BOUNDARY_NO_FLUX_OR_MHREF_HANDOFF",
            "fallback_bound": "fill boundary alpha3/source-normalization coefficient products if no theorem-zero",
            "status": "BOUNDARY_BLOCKED_NONCLAIM",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3627_QLOC_TGK_BOUND_ROWS.csv"),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3628_0_real_progress",
            "decision": "A real scalar-density mechanism now exists on paper: an even response-doublet action makes F_1=0 by symmetry, not by assertion.",
            "status": "DERIVATION_PROGRESS_CONDITIONAL",
            "next_action": "map Z^A to the actual q_loc/PPN/Newton/source residual vector and prove or bound its coupling J_Z",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3628_1_current_ceiling",
            "decision": "Do not claim local GR or q_loc silence: K_hat=K_metric, Z=physical residual, J_Z=0, positive operator, and boundary no-flux are still unsigned.",
            "status": "NO_CLAIM",
            "next_action": "carry residual rows R_K, R_Z, J_Z, boundary flux and score them if derivation fails",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3628_2_poynting_vector",
            "decision": "The Poynting/wave intuition is not discarded; it is put into an explicit Maxwell-like action branch where flux is physical stress/current, not a hidden plateau.",
            "status": "EM_FLUX_BRANCH_RETAINED",
            "next_action": "use it later for EM/charge or radiation stress mapping, not as a local-GR zero proof unless F/J/boundary vanish",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3628_3_next_target",
            "decision": "The next best target is the source coupling: prove J_Z=0 from parent quotient/current symmetry or fill a coefficient row.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3629-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3628_0",
            "result": "EVEN_RESPONSE_SCALAR_DENSITY_CONSTRUCTED_PARENT_MATCH_UNSIGNED_NO_CLAIM",
            "summary": "3628 constructs explicit scalar-density candidates for S_GK, identifies the even response-doublet action as the best derivation route because F_1=0 follows by parity, and retains Poynting/Maxwell-like flux as a legitimate action branch; the framework still cannot claim local GR because K_hat=K_metric, Z=physical residual, J_Z=0, positive operator, and boundary no-flux are not parent-signed.",
            "F1_mechanism_found": True,
            "Kmetric_constructed": True,
            "Khat_match_claimed": False,
            "source_coupling_zero_claimed": False,
            "bound_rows_staged": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3628_0",
            "target_doc": "3629-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md",
            "target_script": "scripts/Y5_R2FR_3629_response_doublet_source_coupling_zero_or_coefficient.py",
            "objective": "attempt to parent-own the response doublet by mapping Z^A to the actual local residual vector and proving J_Z=0; if not, create source-ready coupling coefficient rows for PPN/Newton/R10/clock/orbital bounds",
            "success_gate": "Z^A equals q_loc/PPN/Newton/source residual coordinates, K_hat=K_metric has no remainder or retained R_K row, J_Z is theorem-zero or numeric/source-backed, and boundary flux remains explicit",
            "reason": "3628 found the clean double-zero mechanism; the coupling is now the bottleneck that decides whether the mechanism is physics or just a formal closure.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "Gamma_eff/K_hat/S_GK",
            "canonical_status": "S_GK_EVEN_RESPONSE_TEMPLATE_CONSTRUCTED_KHAT_MATCH_AND_COUPLING_UNSIGNED",
            "usable_result": "F_1=0 can be derived for an even response-doublet scalar density after background subtraction.",
            "hard_block": "need parent map Z^A=physical residual vector, K_hat=K_metric, J_Z=0 or coefficient, positive operator, boundary no-flux",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, object]],
    scalar_density_candidates: list[dict[str, object]],
    metric_response_comparison: list[dict[str, object]],
    fixed_point_gate: list[dict[str, object]],
    qloc_bound_runner: list[dict[str, object]],
    decision_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3628 Y5 R2FR S_GK explicit scalar-density construction or bound runner",
            f"**Status:** {status[0]['summary']}",
            "**Claim ceiling:** no local-GR, PPN, Newton, R10/R11, q_loc=0, K_hat=K_metric, or source-coupling-zero claim is allowed from 3628.",
            "## Core result",
            (
                "The useful move is no longer just another missing-input ledger. 3628 writes an explicit variational shape that can make the "
                "local first variation vanish for a real mathematical reason:\n\n"
                "```text\n"
                "S_GK = -int sqrt(-g)[Gamma_0 + 1/2 M_AB Z^A Z^B + 1/2 H_AB g^{rho sigma} nabla_rho Z^A nabla_sigma Z^B + O(Z^4)]\n"
                "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}\n"
                "K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B + metric/coefficient response terms\n"
                "```\n\n"
                "At `Z=0`, `nabla Z=0`, with `Gamma_0` background-subtracted, this gives `T_GK=0` and `partial_A T_GK|0=0` by evenness. "
                "That is the cleanest route so far to the double-zero/local plateau mechanism. It still does not prove local GR, because the parent map "
                "`Z^A = physical q_loc/PPN/Newton/source residual`, the match `K_hat=K_metric`, source-coupling silence `J_Z=0`, positivity, and boundary no-flux remain unsigned."
            ),
            "## Source register",
            md_table(source_register, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Explicit scalar-density candidates",
            md_table(
                scalar_density_candidates,
                [
                    "candidate_id",
                    "ansatz",
                    "metric_response_formula",
                    "khat_match_requirement",
                    "fixed_point_zero_gate",
                    "current_status",
                ],
            ),
            "## K_metric / K_hat comparison",
            md_table(
                metric_response_comparison,
                [
                    "comparison_id",
                    "target_piece",
                    "computed_from_candidate",
                    "required_existing_match",
                    "residual_if_unmatched",
                    "status",
                ],
            ),
            "## Fixed-point and coupling gates",
            md_table(
                fixed_point_gate,
                ["gate_id", "condition", "exact_requirement", "derivation_status", "effect_if_true"],
            ),
            "## q_loc / T_GK bound runner rows",
            md_table(
                qloc_bound_runner,
                ["row_id", "quantity", "new_reduction", "missing_input", "fallback_bound", "status"],
            ),
            "## Decisions",
            md_table(decision_gates, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            md_table(next_target, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate_outputs(paths: dict[str, Path], source_register: list[dict[str, object]]) -> list[dict[str, object]]:
    timestamp = utc_now()
    validation: list[dict[str, object]] = []

    def add(validation_id: str, result: bool, detail: str) -> None:
        validation.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if result else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3628_0_sources_exist", all(row["exists"] for row in source_register), "all sources exist")
    add("VAL3628_1_needles_found", all(row["needle_found"] for row in source_register), "all source anchors found")

    pre_validation_outputs = {name: path for name, path in paths.items() if name != "validation"}
    add("VAL3628_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()) and DOC.exists(), "all pre-validation outputs written")

    parse_details: list[str] = []
    csv_parse_ok = True
    for name, path in pre_validation_outputs.items():
        try:
            row_count = len(read_csv(path))
            parse_details.append(f"{name}:{row_count}")
            csv_parse_ok = csv_parse_ok and row_count > 0
        except Exception as exc:
            parse_details.append(f"{name}:ERR:{exc}")
            csv_parse_ok = False
    add("VAL3628_3_csv_parse", csv_parse_ok, "; ".join(parse_details))

    candidates = read_csv(paths["scalar_density_candidates"])
    metric_rows = read_csv(paths["metric_response_comparison"])
    fixed_rows = read_csv(paths["fixed_point_gate"])
    bound_rows = read_csv(paths["qloc_bound_runner"])
    decision_rows_loaded = read_csv(paths["decision_gates"])
    status_rows_loaded = read_csv(paths["status"])
    next_rows = read_csv(paths["next_target"])

    add(
        "VAL3628_4_scalar_density_formulas_written",
        any("S_GK=-int sqrt(-g)" in row["ansatz"] for row in candidates),
        "explicit S_GK scalar-density ansatz written",
    )
    add(
        "VAL3628_5_Kmetric_formula_written",
        any("K_metric" in row["computed_from_candidate"] for row in metric_rows),
        "K_metric comparison formulas written",
    )
    add(
        "VAL3628_6_F1_evenness_mechanism_written",
        any("F1_ZERO" in row["derivation_status"] for row in fixed_rows),
        "even response doublet gives conditional F1 zero",
    )
    add(
        "VAL3628_7_poynting_flux_branch_considered",
        any("Poynting" in row["what_this_buys"] or "Maxwell" in row["ansatz"] for row in candidates),
        "Poynting/Maxwell-like flux branch retained explicitly",
    )
    add(
        "VAL3628_8_Khat_match_not_claimed",
        all(row["valid_for_claim"].lower() == "false" for row in metric_rows)
        and any("NOT_CLAIMED" in row["status"] for row in metric_rows),
        "K_hat=K_metric remains unsigned",
    )
    add(
        "VAL3628_9_bound_rows_blocked",
        all(row["valid_for_claim"].lower() == "false" and row["score_ready"].lower() == "false" for row in bound_rows),
        "all q_loc/T_GK bound runner rows remain blocked/nonclaim",
    )
    add(
        "VAL3628_10_no_claim_allowed",
        all(row["valid_for_claim"].lower() == "false" for row in status_rows_loaded + decision_rows_loaded + next_rows),
        "all status/decision/next rows remain nonclaim",
    )
    formalization_leak = list(FORMALIZATION.rglob("*3628*")) if FORMALIZATION.exists() else []
    add("VAL3628_11_no_formalization_leak", not formalization_leak, "no 3628 files in formalization-workbench")
    add(
        "VAL3628_12_next_target_written",
        bool(next_rows) and "3629" in next_rows[0]["target_doc"],
        "3629 coupling/source target written",
    )
    add(
        "VAL3628_13_canonical_status_written",
        paths["canonical_status"].exists() and "COUPLING_UNSIGNED" in paths["canonical_status"].read_text(encoding="utf-8", errors="replace"),
        "canonical Gamma/Khat/Kmetric status written",
    )
    return validation


def main() -> None:
    timestamp = utc_now()
    paths = output_paths()

    source_register = source_register_rows(timestamp)
    scalar_density_candidates = scalar_density_candidate_rows(timestamp)
    metric_response_comparison = metric_response_rows(timestamp)
    fixed_point_gate = fixed_point_rows(timestamp)
    qloc_bound_runner = qloc_bound_runner_rows(timestamp)
    decisions = decision_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_target_rows(timestamp)
    canonical_status = canonical_status_rows(timestamp)

    write_csv(paths["source_register"], source_register)
    write_csv(paths["scalar_density_candidates"], scalar_density_candidates)
    write_csv(paths["metric_response_comparison"], metric_response_comparison)
    write_csv(paths["fixed_point_gate"], fixed_point_gate)
    write_csv(paths["qloc_bound_runner"], qloc_bound_runner)
    write_csv(paths["decision_gates"], decisions)
    write_csv(paths["status"], status)
    write_csv(paths["next_target"], next_target)
    write_csv(paths["canonical_status"], canonical_status)

    write_doc(
        source_register,
        scalar_density_candidates,
        metric_response_comparison,
        fixed_point_gate,
        qloc_bound_runner,
        decisions,
        status,
        next_target,
    )

    validation = validate_outputs(paths, source_register)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3628 validation failed: {failed}")
    print(f"wrote 3628 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
