from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4086-Y5-R2FR-parent-EH-operator-signature-or-nonEH-R11-projection.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "PARENT_EH_SIGNATURE_REDUCED_TO_EXACT_LADDER_ELSE_NON_EH_R11_PPN_PROJECTION_VECTOR_SELECTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4086_00_4085_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_NEXT_TARGET.csv",
        "4086-Y5-R2FR-parent-EH-operator-signature-or-nonEH-R11-projection.md",
        "4085 selects the parent EH/operator or non-EH/R11 projection fork.",
    ),
    "SRC4086_01_4085_ppn_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_SOURCE_STABLE_PPN_THEOREM.csv",
        "EXACT_CONDITIONAL_GAMMA_THEOREM_SOURCE_STABLE",
        "4085 supplies the PPN consequence if the EH/no-extra-R11 antecedents are signed.",
    ),
    "SRC4086_02_4085_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_0_gamma_cassini",
        "4085 supplies the empirical component bounds that non-EH residuals must face.",
    ),
    "SRC4086_03_3906_selector": (
        SOURCE_DIR / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv",
        "CONDITIONAL_OPERATOR_SELECTION_THEOREM",
        "3906 already states the EH selector contract and non-EH filter.",
    ),
    "SRC4086_04_3906_low_energy": (
        SOURCE_DIR / "P8_Y5_R2FR_3906_LOW_ENERGY_GR_BRANCH_CONTRACT.csv",
        "MTS local-GR branch",
        "3906 separates EH shape, G owner and non-EH residual sectors.",
    ),
    "SRC4086_05_4019_no_extra": (
        SOURCE_DIR / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv",
        "EXACT_CONDITIONAL_NO_EXTRA_OPERATOR_THEOREM",
        "4019 supplies the previous no-extra-operator theorem and finite scorer interface.",
    ),
    "SRC4086_06_4019_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_4019_EH_ONLY_R11_ADOPTION_CLAUSES.csv",
        "Allowed(O_R11",
        "4019 lists the adoption clauses for the EH-only/R11-silent branch.",
    ),
    "SRC4086_07_4019_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4019_EH_ONLY_R11_AUDIT.csv",
        "EHAUD4019_2_R11_family",
        "4019 records that R11 family absence remains unsigned.",
    ),
    "SRC4086_08_4042_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4042_NONEH_THEOREM_CONTRACT.csv",
        "NTC4042_4_ppn_projector_fallback",
        "4042 supplies the non-EH theorem contract and projector fallback.",
    ),
    "SRC4086_09_4042_families": (
        SOURCE_DIR / "P8_Y5_R2FR_4042_R11_FAMILY_CLASSIFICATION.csv",
        "R11F4042_09",
        "4042 classifies the retained R11/non-EH operator families.",
    ),
    "SRC4086_10_3918_gamma_projection": (
        SOURCE_DIR / "P8_Y5_R2FR_3918_DELTA_GAMMA_R11_THEOREM_AND_BOUND.csv",
        "delta_gamma_R11",
        "3918 gives the tracefree spatial slip projection formula for gamma.",
    ),
    "SRC4086_11_eh_or_vector_gate": (
        SOURCE_DIR / "R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv",
        "EHV1_EH_only_ladder_closed",
        "The earlier EH-only gate already fails broad ladder closure and selects the R11 vector fallback.",
    ),
    "SRC4086_12_r11_executable": (
        SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv",
        "R2_fR_scalar_mode",
        "The retained executable vector schema names the non-EH/R11 families and missing coefficient fields.",
    ),
}


WEB_SOURCES = [
    {
        "source_id": "WEB4086_0_lovelock_1971",
        "title": "The Einstein Tensor and Its Generalizations",
        "authors": "David Lovelock",
        "year": "1971",
        "url": "https://pubs.aip.org/aip/jmp/article/12/3/498/223441/The-Einstein-Tensor-and-Its-Generalizations",
        "source_role": "external theorem support for the 4D local metric-only second-order EH selector",
        "extracted_result": "In four dimensions, the only symmetric divergence-free rank-two concomitants of the metric and its first two derivatives are the metric and Einstein tensors.",
        "confidence": "primary_lovelock_journal_page",
        "timestamp_utc": TIMESTAMP,
    }
]


FAMILIES = [
    {
        "family_id": "R11F4086_00",
        "operator_family": "boundary_topological_terms",
        "coefficient_symbol": "c_boundary_or_c_GB",
        "primary_projection": "boundary_or_reference_flux; gamma/beta only if boundary stress survives",
        "closure_condition": "topological/exact boundary term or fixed source-blind no-flux reference",
        "if_unsigned_formula_id": "PROJ4086_0_total; PROJ4086_4_conservation",
        "next_fill_requirement": "prove metric-independent/topological boundary ownership or supply boundary stress normalization",
        "current_status": "CONDITIONAL_ZERO_IF_PARENT_OWNS_BOUNDARY_ELSE_RESIDUAL",
    },
    {
        "family_id": "R11F4086_01",
        "operator_family": "R2_fR_scalar_mode",
        "coefficient_symbol": "c_R2_or_c_fR",
        "primary_projection": "gamma_minus_1; beta_minus_1; alpha(lambda)",
        "closure_condition": "operator absent, auxiliary double zero, or positive-mass scalar with sourced bound",
        "if_unsigned_formula_id": "PROJ4086_1_gamma; PROJ4086_2_beta; PROJ4086_6_range",
        "next_fill_requirement": "derive coefficient zero/mass gap or bound c_R2/f_R against gamma and R10",
        "current_status": "HIGH_PRIORITY_FIRST_NUMERIC_OR_ZERO_FILL",
    },
    {
        "family_id": "R11F4086_02",
        "operator_family": "Ricci_Weyl_squared",
        "coefficient_symbol": "c_Ricci_or_c_Weyl",
        "primary_projection": "gamma_minus_1; xi; wave_sector_bound",
        "closure_condition": "Gauss-Bonnet/topological combination, direct absence, or double-zero curvature-squared coefficient",
        "if_unsigned_formula_id": "PROJ4086_1_gamma; PROJ4086_3_preferred_frame",
        "next_fill_requirement": "separate topological GB part from live Weyl/Ricci response and bound tracefree projection",
        "current_status": "HIGH_PRIORITY_TRACEFREE_SLIP_FILL",
    },
    {
        "family_id": "R11F4086_03",
        "operator_family": "scalar_tensor_class_metric",
        "coefficient_symbol": "F_phi_C_or_c_scalar",
        "primary_projection": "gamma_minus_1; beta_minus_1; Gdot_over_G; alpha(lambda)",
        "closure_condition": "constant scalar prefactor absorbed into kappa, nonconstant scalar has double zero plus mass gap",
        "if_unsigned_formula_id": "PROJ4086_1_gamma; PROJ4086_2_beta; PROJ4086_5_gdot; PROJ4086_6_range",
        "next_fill_requirement": "prove local scalar is fixed/source-free or compute Brans-Dicke-like coupling envelope",
        "current_status": "LIVE_IF_NONCONSTANT_SCALAR_HAIR_SURVIVES",
    },
    {
        "family_id": "R11F4086_04",
        "operator_family": "vector_preferred_frame",
        "coefficient_symbol": "c_domain_vector_or_selector_marker",
        "primary_projection": "alpha1; alpha2; alpha3; xi",
        "closure_condition": "no-vector/domain-selector theorem or vector coefficient double zero",
        "if_unsigned_formula_id": "PROJ4086_3_preferred_frame",
        "next_fill_requirement": "prove no independent local vector/domain normal survives observed projection or compute alpha_i products",
        "current_status": "LIVE_STRICT_PREFERRED_FRAME_BOUND_VECTOR",
    },
    {
        "family_id": "R11F4086_05",
        "operator_family": "torsion_nonmetricity",
        "coefficient_symbol": "c_T_or_c_Q",
        "primary_projection": "WEP; clocks; lightcone; spin/source; gamma if connection affects metric branch",
        "closure_condition": "Levi-Civita metric connection selected or connection variation kills torsion/nonmetricity and hypermomentum",
        "if_unsigned_formula_id": "PROJ4086_0_total; PROJ4086_1_gamma",
        "next_fill_requirement": "derive no-independent-connection theorem or fill connection residual rows",
        "current_status": "LIVE_CONNECTION_SIGNATURE_RUNG",
    },
    {
        "family_id": "R11F4086_06",
        "operator_family": "bulk_X_force_law",
        "coefficient_symbol": "q_X_or_c_X",
        "primary_projection": "alpha(lambda); gamma_minus_1; beta_minus_1; source_eta",
        "closure_condition": "source charge zero plus double-zero coupling or finite-range screened bound",
        "if_unsigned_formula_id": "PROJ4086_6_range; PROJ4086_1_gamma; PROJ4086_2_beta",
        "next_fill_requirement": "derive X source charge zero/mass gap or tie to sourced alpha(lambda) curve",
        "current_status": "LIVE_R10_RANGE_BRANCH_IF_NOT_ZERO",
    },
    {
        "family_id": "R11F4086_07",
        "operator_family": "nonlocal_memory_kernel",
        "coefficient_symbol": "c_nonlocal_or_K_norm",
        "primary_projection": "alpha3; Gdot_over_G; alpha(lambda); hysteresis",
        "closure_condition": "compact-local kernel silence, double-zero kernel norm, or causal kernel bound",
        "if_unsigned_formula_id": "PROJ4086_3_preferred_frame; PROJ4086_5_gdot; PROJ4086_6_range",
        "next_fill_requirement": "prove local-vacuum kernel has zero monopole/vector/Gdot projection or bound kernel norm",
        "current_status": "LIVE_MEMORY_BRANCH_IF_LOCAL_SILENCE_NOT_PROVED",
    },
    {
        "family_id": "R11F4086_08",
        "operator_family": "source_normalization_operator",
        "coefficient_symbol": "c_domain_source_normalization_operator",
        "primary_projection": "beta_source; alpha_i; xi; source normalization",
        "closure_condition": "common mode absorbed into G_ref only; derivative/source/domain hair zero or bounded",
        "if_unsigned_formula_id": "PROJ4086_2_beta; PROJ4086_3_preferred_frame",
        "next_fill_requirement": "prove no source-dependent G hair or compute derivative/source normalized residual",
        "current_status": "LIVE_ANTI_ORBITAL_LAUNDERING_SOURCE_BRANCH",
    },
    {
        "family_id": "R11F4086_09",
        "operator_family": "projector_domain_stress",
        "coefficient_symbol": "c_projector_domain_stress",
        "primary_projection": "gamma_minus_1; beta_minus_1; alpha_i; xi; zeta_i",
        "closure_condition": "parent owns projector as metric-independent topological selection, or bulk projector stress coefficient is zero",
        "if_unsigned_formula_id": "PROJ4086_1_gamma; PROJ4086_2_beta; PROJ4086_3_preferred_frame; PROJ4086_4_conservation",
        "next_fill_requirement": "prove metric-independent projector ownership or compute projector stress PPN products",
        "current_status": "LIVE_PROJECTOR_STRESS_BRANCH_IF_TOPOLOGICAL_OWNERSHIP_UNSIGNED",
    },
]


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    for row in WEB_SOURCES:
        rows.append(
            {
                "source_id": row["source_id"],
                "source_type": "web_literature",
                "path_or_url": row["url"],
                "needle": row["extracted_result"],
                "role": row["source_role"],
                "exists": "web_checked",
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4086_13_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4086 EH-signature/R11-projection outputs.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def eh_signature_rows() -> List[dict]:
    return [
        {
            "theorem_id": "EH4086_0_lovelock_selector",
            "claim_piece": "EH/EC operator signature",
            "statement": "If the observed local gravitational branch is 4D, local, diffeomorphism invariant, metric/coframe-only after connection constraints, second-order in the observed metric equations through 2PN, and divergence-free, then its rank-two metric equation is A_* G_munu + B_* g_munu.",
            "derivation": "This is the Lovelock-style selector applied to the observed local branch. In four dimensions the only allowed symmetric divergence-free second-order natural metric tensors are the metric and Einstein tensors. The B_* term is a cosmological/common background term; the dynamical local operator is EH.",
            "formula": "E_obs^{munu}=A_* G^{munu}[g_obs]+B_* g_obs^{munu}",
            "result": "EXACT_CONDITIONAL_LOVELOCK_EH_SIGNATURE",
            "current_MTS_status": "PARENT_SIGNATURE_LADDER_NOT_ALL_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "EH4086_1_action_normal_form",
            "claim_piece": "action branch normal form",
            "statement": "Under the same selector assumptions, the local action is equivalent through PPN order to EH plus cosmological, topological/exact boundary, matter/EM and explicitly retained non-EH residual sectors.",
            "derivation": "Integrating the selected Euler equation gives S_EH with kappa_* and Lambda_*. Terms whose variations vanish locally are topological/exact. Every other term is not part of the EH proof and must enter DeltaE_nonEH.",
            "formula": "S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter+S_EM+dB+S_top+S_nonEH_residual",
            "result": "EXACT_CONDITIONAL_ACTION_NORMAL_FORM_WITH_RESIDUAL_SPLIT",
            "current_MTS_status": "S_NON_EH_RESIDUAL_NOT_GLOBALLY_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "EH4086_2_parent_signature_contract",
            "claim_piece": "what the parent action must prove",
            "statement": "MTS earns local GR only if the parent action signs the selector premises, not if they are inserted at the observed-branch level. The parent must own the observed metric, locality, Ward/Bianchi identity, connection reduction, no-extra-fields, second-order truncation, boundary silence and same-source coupling.",
            "derivation": "The theorem is valid, but theorem premises are not free. Each premise corresponds to a possible MTS escape channel already present in R11/q_loc/source-normalization files.",
            "formula": "claim_EH_local := AND(P1_observed_metric,...,P8_same_source_constant_kappa)",
            "result": "PARENT_SIGNATURE_LADDER_REQUIRED",
            "current_MTS_status": "NOT_YET_PARENT_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "EH4086_3_escape_channel_projection",
            "claim_piece": "non-EH fallback",
            "statement": "If any selector premise is unsigned, its escape channel is not a philosophical objection; it is a PPN projection residual DeltaE_nonEH that must be zeroed by a theorem or bounded against the 4085 empirical table.",
            "derivation": "Move every non-EH or q_loc contribution to the left-hand residual of the observed field equation and apply the gamma, beta, alpha, xi, zeta and Gdot projectors componentwise.",
            "formula": "DeltaE_nonEH^{munu}=sum_i c_i E_i^{munu}+E_q^{munu}+E_proj^{munu}+E_readout^{munu}",
            "result": "NON_EH_PPN_PROJECTION_FORMULAS_SELECTED",
            "current_MTS_status": "EXECUTABLE_RESIDUAL_ROUTE_SELECTED_WHERE_EH_SIGNATURE_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "EH4086_4_4085_unlock",
            "claim_piece": "PPN consequence",
            "statement": "If the EH signature ladder closes and DeltaE_nonEH=0 through 2PN, the 4085 theorem immediately gives gamma=beta=1 and alpha_i=xi=zeta_i=Gdot/G=0 in the fixed-source PPN convention.",
            "derivation": "4085 already proved the source-stable PPN vector conditional on EH/EC, same readout, no extra R11/q_loc/projector stress and Bianchi source closure. 4086 defines the exact parent signature needed to satisfy those antecedents.",
            "formula": "P1...P8 and DeltaE_nonEH=0 => Delta_PPN_abs_4085=0",
            "result": "CONDITIONAL_LOCAL_GR_UNLOCK_IF_PARENT_SIGNATURE_SIGNED",
            "current_MTS_status": "LOCAL_GR_FALSE_UNTIL_PARENT_SIGNATURE_OR_RESIDUAL_PASS",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def ladder_rows() -> List[dict]:
    return [
        {
            "rung_id": "P1_observed_metric_owner",
            "requirement": "The parent quotient/readout selects one observed 4D metric/coframe branch as the public local gravitational variable.",
            "why_needed": "Lovelock/EH selection applies to the public metric branch, not to an undefined mixture of parent variables.",
            "current_evidence": "3906 and 4019 provide a selected branch contract; adoption remains parent-level conditional.",
            "status": "CONDITIONAL_NOT_FINAL",
            "residual_if_failed": "readout_frame_residual; preferred-frame marker",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P2_local_product_chart",
            "requirement": "The local compact branch is genuinely local through 2PN, with no nonlocal memory kernel contributing to the solar-system readout.",
            "why_needed": "Nonlocal kernels evade the local second-order selector.",
            "current_evidence": "4042 retains nonlocal_memory_kernel as a family if compact-local silence is not proved.",
            "status": "OPEN_IF_MEMORY_KERNEL_NOT_ZEROED",
            "residual_if_failed": "alpha3; Gdot_over_G; alpha(lambda); hysteresis",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P3_diffeomorphism_Ward_Bianchi",
            "requirement": "The observed branch owns diffeomorphism/Ward identity and Bianchi-compatible source conservation.",
            "why_needed": "PPN zeta_i vanish only if the same field equation and same Hilbert source are conserved.",
            "current_evidence": "3906 Bianchi clause and 4085 conservation theorem; source-current closure remains parent unsigned.",
            "status": "CONDITIONAL_SOURCE_CURRENT_UNSIGNED",
            "residual_if_failed": "zeta1; zeta2; zeta3; source_current_leak",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P4_Levi_Civita_connection",
            "requirement": "Connection variation reduces to Levi-Civita or kills torsion/nonmetricity/hypermomentum in the observed local branch.",
            "why_needed": "Independent torsion/nonmetricity gives non-EH connection residues and may affect clocks, spin, WEP or PPN.",
            "current_evidence": "R11 family classification retains torsion_nonmetricity unless the no-independent-connection theorem is signed.",
            "status": "OPEN_CONNECTION_SIGNATURE",
            "residual_if_failed": "torsion_nonmetricity_R11; WEP; clock; lightcone; spin_source",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P5_metric_only_no_extra_fields",
            "requirement": "No independent scalar/vector/tensor/domain/projector variables survive linearly in the observed PPN branch.",
            "why_needed": "Extra fields evade Lovelock by being non-metric degrees of freedom.",
            "current_evidence": "4019/4042 allow auxiliary double-zero or residual projection, but not global parent adoption.",
            "status": "OPEN_EXTRA_FIELD_SIGNATURE",
            "residual_if_failed": "scalar_tensor; vector_preferred_frame; bulk_X; projector_domain_stress",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P6_second_order_operator",
            "requirement": "The observed metric equations contain no higher-curvature/higher-derivative operator through 2PN, except topological/exact or double-zero silent terms.",
            "why_needed": "R2, Ricci^2, Weyl^2 and f(R) evade the EH selector by adding higher derivative metric equations.",
            "current_evidence": "3906 states the filter; 4042 retains R2_fR_scalar_mode and Ricci_Weyl_squared until zero/bound filled.",
            "status": "OPEN_HIGHER_CURVATURE_SIGNATURE",
            "residual_if_failed": "delta_gamma_R11; delta_beta_R11; xi; alpha(lambda)",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P7_boundary_topological_silence",
            "requirement": "Boundary, topological and projector selection pieces are metric-independent or have zero local Euler/stress contribution.",
            "why_needed": "Boundary/projector stress can mimic preferred-frame or conservation anomalies even when bulk EH looks right.",
            "current_evidence": "4042 marks boundary and projector stress as conditional, not parent-owned proof.",
            "status": "CONDITIONAL_BOUNDARY_PROJECTOR_UNSIGNED",
            "residual_if_failed": "alpha_i; xi; zeta_i; beta_boundary",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "P8_same_source_constant_kappa",
            "requirement": "The same Hilbert source and constant calibrated kappa/G feed both Newton and PPN order.",
            "why_needed": "Otherwise beta/source normalization, Gdot and orbital-GM laundering re-enter.",
            "current_evidence": "4084 fixed source denominator and 4085 locks PPN source; parent Pi_M/H_tau/Hilbert equality remains unsigned.",
            "status": "CONDITIONAL_SOURCE_DENOMINATOR_UNSIGNED",
            "residual_if_failed": "delta_beta_source; Gdot_over_G; source_normalization_operator",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def auxiliary_double_zero_rows() -> List[dict]:
    return [
        {
            "lemma_id": "ADZ4086_0_statement",
            "piece": "auxiliary double-zero decoupling",
            "statement": "For a non-EH operator C_i(X) O_i[g] carried by auxiliary/local fields X^A, if C_i(X0)=0, partial_A C_i(X0)=0, the auxiliary Hessian H_AB at X0 is positive/source-free, and readout/projector maps have no linear X-X0 term, then O_i gives no linear or 2PN local PPN source.",
            "formula": "C_i(X0)=0; dC_i|X0=0; H_AB>0; dg_readout/dX|X0=0 => Pi_PPN[delta_g(C_i O_i)]_{<=2PN}=0",
            "result": "EXACT_CONDITIONAL_AUXILIARY_DOUBLE_ZERO_LEMMA",
            "status": "DERIVED_CONDITIONAL_NOT_PARENT_SIGNED",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "lemma_id": "ADZ4086_1_metric_variation",
            "piece": "why metric Euler term vanishes",
            "statement": "At fixed X=X0, the metric variation of C_i(X)O_i is C_i(X0) delta_g O_i plus metric-readout terms. The first term vanishes by C_i(X0)=0; the readout term vanishes if readout is quadratic in X-X0.",
            "formula": "delta_g[C_i O_i]|X0 = C_i(X0) delta_g O_i + O_i partial_A C_i(X0) delta_g X^A_readout = 0",
            "result": "LINEAR_METRIC_EULER_ZERO",
            "status": "DERIVED_CONDITIONAL",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "lemma_id": "ADZ4086_2_field_displacement_bound",
            "piece": "why finite auxiliary response does not sneak back",
            "statement": "If the auxiliary equation is H_AB delta X^B=J_A and dC_i|X0=0, then C_i(X)=O(delta X^2). With positive mass gap and no local source J_A through the PPN order being scored, the induced metric operator starts beyond the retained order or is explicitly bounded.",
            "formula": "||delta X|| <= ||H^{-1}|| ||J||; C_i(X)=1/2 C_{i,AB} delta X^A delta X^B+...; residual <= ||C_{i,AB}|| ||H^{-1}J||^2 ||Pi O_i||",
            "result": "FINITE_FALLBACK_BOUND_IF_SOURCE_NOT_ZERO",
            "status": "BOUND_FORMULA_NOT_NUMERIC_UNTIL_H_AND_J_SOURCED",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "lemma_id": "ADZ4086_3_failure_routes",
            "piece": "if the lemma premises fail",
            "statement": "A single zero C_i(X0)=0 is not enough. If dC_i is nonzero, H has a massless/tachyonic mode, or readout has a linear X component, the family becomes a live R11 residual and must be projected against 4085 bounds.",
            "formula": "not(C=0 and dC=0 and H>0 and linear_readout=0) => use PROJ4086_j",
            "result": "NO_SINGLE_ZERO_SHORTCUT",
            "status": "ANTI_CLOSURE_GUARD",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def projection_formula_rows() -> List[dict]:
    return [
        {
            "projection_id": "PROJ4086_0_total",
            "component": "total non-EH observed equation residual",
            "formula": "DeltaE_nonEH^{munu}=sum_i c_i E_i^{munu}+E_q^{munu}+E_projector^{munu}+E_boundary^{munu}+E_readout^{munu}",
            "meaning": "Everything not earned by the EH selector is carried as an explicit left-hand residual.",
            "feeds_4085_bound": "master Delta_PPN_abs_4085 componentwise",
            "status": "EXECUTABLE_SYMBOLIC_INTERFACE",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "PROJ4086_1_gamma",
            "component": "spatial tracefree slip / gamma",
            "formula": "delta_gamma_nonEH ~= -(kappa_ref/(C_TF*U)) nabla^{-2} P_TF[DeltaE_nonEH_ij]",
            "meaning": "Tracefree spatial stress from non-EH/R11 operators sources Psi-Phi and is compared to the Cassini gamma bound.",
            "feeds_4085_bound": "|gamma-1| <= 2.3e-5",
            "status": "DERIVED_FROM_3918_AND_4085_BOUND_READY",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "PROJ4086_2_beta",
            "component": "second-order 00 nonlinear / beta",
            "formula": "delta_beta_nonEH := Pi_beta[DeltaE_nonEH] = (1/U^2) N_beta^{-1} P_00^{2PN}[DeltaE_nonEH_00 plus source-normalization terms]",
            "meaning": "Any non-EH O(U^2) correction is scored after the 4084 source denominator is fixed; it cannot be absorbed into GM.",
            "feeds_4085_bound": "|beta-1| <= 8.0e-5",
            "status": "SOURCE_NORMALIZED_SYMBOLIC_INTERFACE",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "PROJ4086_3_preferred_frame",
            "component": "preferred-frame/location",
            "formula": "alpha_i_nonEH=Pi_alpha_i[DeltaE_nonEH, V_extra, domain normal, coframe marker]; xi_nonEH=Pi_xi[anisotropic/domain marker]",
            "meaning": "Surviving vector/domain/coframe/projector markers go straight to alpha1, alpha2, alpha3 and xi.",
            "feeds_4085_bound": "alpha1 <= 4.0e-5 companion row; alpha2 <= 2.0e-9; alpha3 <= 4.0e-20; xi <= 4.0e-9",
            "status": "PROJECTOR_DEFINED_NEEDS_COEFFICIENT_PRODUCTS",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "PROJ4086_4_conservation",
            "component": "conservation/zeta",
            "formula": "zeta_j_nonEH=Pi_zeta_j[nabla_mu DeltaE_nonEH^{munu} - kappa_ref DeltaJ_source^nu]",
            "meaning": "Hidden source-current leaks or non-Bianchi residuals are scored as zeta_i rather than hand-waved.",
            "feeds_4085_bound": "zeta1 <= 2.0e-2; zeta2 <= 4.0e-5; zeta3 <= 1.0e-8",
            "status": "BIANCHI_SOURCE_CURRENT_INTERFACE",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "PROJ4086_5_gdot",
            "component": "local coupling drift",
            "formula": "Gdot_over_G_nonEH = partial_t kappa_eff/kappa_eff + source_prefactor_drift",
            "meaning": "A time-varying scalar/source prefactor is not an EH operator correction; it is a Gdot/source-normalization residual.",
            "feeds_4085_bound": "|Gdot/G| <= 1.3e-12 yr^-1 staged envelope",
            "status": "DRIFT_INTERFACE",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "PROJ4086_6_range",
            "component": "finite-range/fifth-force tail",
            "formula": "alpha_X(lambda_X) ~ (q_source q_test)/(4*pi G_ref m_source m_test) with lambda_X=m_X^{-1}; zero if q_X=0 or m_X*L_local >> 1",
            "meaning": "Scalar/bulk/nonlocal tails that do not vanish locally become R10/alpha(lambda) rows before any local-GR claim.",
            "feeds_4085_bound": "routes outside 4085 to R10 bound table, then returns as gamma/beta/source residual if long range",
            "status": "R10_LINK_REQUIRED_IF_RANGE_MODE_SURVIVES",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def family_route_rows() -> List[dict]:
    rows = []
    for family in FAMILIES:
        row = dict(family)
        row.update({"valid_for_claim": "False", "timestamp_utc": TIMESTAMP})
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4086_0_main",
            "decision": DECISION,
            "meaning": "The EH route is now a precise parent-signature ladder, and the fallback is a precise non-EH/R11 projection vector. Since the ladder is not fully parent-signed, the next honest work is first residual projection fill, not repeating the missing-list.",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_required_move": "Fill the first executable R11 projection row against the 4085 bounds, starting with gamma/beta tracefree higher-curvature or projector stress.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4086_1_best_route",
            "decision": "RESIDUAL_PROJECTION_ROUTE_BEATS_BROAD_PARENT_ASSERTION_RIGHT_NOW",
            "meaning": "Trying to declare the whole parent action EH-only would invite maximum scrutiny. The lower-scrutiny route is to make every escape channel pay a sourced PPN/R10 bound, one family at a time.",
            "claim_status": "ROUTE_SELECTION",
            "next_required_move": "Use PROJ4086_1 and PROJ4086_2 to turn R2/Ricci/Weyl/projector stress into explicit gamma/beta bound rows.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4086_0_EH_signature",
            "claim": "MTS parent action forces EH/EC locally",
            "allowed": "False",
            "why_not": "The Lovelock/EH selector is exact conditional, but the parent has not yet signed all ladder rungs P1-P8.",
            "minimum_unlock": "All parent signature rungs signed, or every failed rung projected and bounded below 4085/R10 limits.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4086_1_local_GR",
            "claim": "MTS passes local GR/PPN",
            "allowed": "False",
            "why_not": "4085 PPN zero is conditional on EH/no-extra-R11 and same-source closure; 4086 does not yet prove those globally.",
            "minimum_unlock": "EH ladder plus DeltaE_nonEH=0 through 2PN, or componentwise residual vector below sourced bounds.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4086_2_forward_progress",
            "claim": "4086 advances the route",
            "allowed": "True_private_checkpoint",
            "why_not": "Not a public physics claim; it is a stronger internal derivation gate.",
            "minimum_unlock": "N/A",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4086_0",
            "next_target": "4087-Y5-R2FR-first-nonEH-R11-projection-fill-gamma-beta-bound.md",
            "script": "scripts/Y5_R2FR_4087_first_nonEH_R11_projection_fill_gamma_beta_bound.py",
            "why": "4086 selects the lower-scrutiny path: make a live non-EH family pay the 4085 PPN bounds. Start with the tracefree gamma/beta projection because 3918 and 4085 already provide formulas and empirical bounds.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4086_1",
            "next_target": "parent_signature_ladder_parallel",
            "script": "defer_until_specific_parent_clause_sources_are_selected",
            "why": "The broad EH proof remains useful, but should be attacked by concrete rungs P4/P5/P6 rather than a global assertion.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4086",
            "status": "private_nonclaim_checkpoint_complete",
            "decision": DECISION,
            "public_claim": "False",
            "github_action": "False",
            "formalization_workbench_modified_by_script": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def validation_rows(output_paths: Iterable[Path]) -> List[dict]:
    paths = list(output_paths)
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        add(
            f"VAL4086_SRC_{source_id}",
            "local source exists and contains needle",
            bool(exists and contains),
            f"{path} | needle={needle} | role={role}",
        )

    for path in paths:
        rows = parse_csv(path)
        add(
            f"VAL4086_CSV_{path.stem}",
            "generated CSV parses and is non-empty",
            bool(rows),
            f"{path} rows={len(rows)}",
        )

    theorem_results = {row["result"] for row in eh_signature_rows()}
    required_results = {
        "EXACT_CONDITIONAL_LOVELOCK_EH_SIGNATURE",
        "NON_EH_PPN_PROJECTION_FORMULAS_SELECTED",
        "CONDITIONAL_LOCAL_GR_UNLOCK_IF_PARENT_SIGNATURE_SIGNED",
    }
    add(
        "VAL4086_EH_THEOREM_CORE",
        "EH signature theorem and fallback projection are present",
        required_results.issubset(theorem_results),
        f"missing={sorted(required_results - theorem_results)}",
    )

    adz_results = {row["result"] for row in auxiliary_double_zero_rows()}
    add(
        "VAL4086_DOUBLE_ZERO_LEMMA",
        "auxiliary double-zero lemma is present",
        "EXACT_CONDITIONAL_AUXILIARY_DOUBLE_ZERO_LEMMA" in adz_results and "NO_SINGLE_ZERO_SHORTCUT" in adz_results,
        f"results={sorted(adz_results)}",
    )

    family_names = {row["operator_family"] for row in family_route_rows()}
    required_families = {
        "boundary_topological_terms",
        "R2_fR_scalar_mode",
        "Ricci_Weyl_squared",
        "scalar_tensor_class_metric",
        "vector_preferred_frame",
        "torsion_nonmetricity",
        "bulk_X_force_law",
        "nonlocal_memory_kernel",
        "source_normalization_operator",
        "projector_domain_stress",
    }
    add(
        "VAL4086_R11_FAMILY_COVERAGE",
        "all retained R11 family classes are routed to closure or projection",
        required_families.issubset(family_names),
        f"missing={sorted(required_families - family_names)} count={len(family_names)}",
    )

    projection_ids = {row["projection_id"] for row in projection_formula_rows()}
    required_projection_ids = {f"PROJ4086_{index}" for index in range(7)}
    projection_prefixes = {"_".join(projection_id.split("_")[:2]) for projection_id in projection_ids}
    add(
        "VAL4086_PROJECTION_FORMULAS",
        "gamma beta preferred-frame conservation Gdot and range formulas are present",
        required_projection_ids.issubset(projection_prefixes),
        f"missing={sorted(required_projection_ids - projection_prefixes)}",
    )

    outputs_inside_post_checkpoint = all(is_under(path, ROOT) for path in paths) and is_under(DOC_PATH, ROOT)
    outputs_outside_formalization = all(not is_under(path, FORMALIZATION) for path in paths) and not is_under(DOC_PATH, FORMALIZATION)
    add(
        "VAL4086_SCOPE",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        bool(outputs_inside_post_checkpoint and outputs_outside_formalization),
        f"doc={DOC_PATH}; csv_count={len(paths)}",
    )

    no_public_claim = all(row.get("valid_for_claim", "False") != "True" for row in eh_signature_rows())
    no_public_claim = no_public_claim and all(row.get("allowed") != "True" for row in claim_gate_rows() if row["claim_id"] != "CLAIM4086_2_forward_progress")
    add(
        "VAL4086_NO_LOCAL_GR_CLAIM",
        "4086 does not promote local GR/EH-only claim",
        no_public_claim,
        "claim gates keep EH/local-GR false",
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4086_SCRIPT_COMPILES", "generator script compiles", compile_ok, compile_detail)

    return checks


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4086 - Parent EH Operator Signature Or Non-EH R11 Projection

- Timestamp: `{TIMESTAMP}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/EH-only claim: `false`
- GitHub action: `false`

## Result

4086 turns the 4085 handoff into a hard fork:

```text
Route A: parent signs the EH/EC operator ladder.
Route B: every unsigned escape channel becomes a non-EH/R11 PPN projection residual.
```

No more fog. If the parent branch is truly local, 4D, diffeomorphism-invariant, metric/coframe-only, Levi-Civita, second-order through PPN order, boundary-silent and same-source, then the observed field equation is forced into:

```text
E_obs^{{mu nu}} = A_* G^{{mu nu}}[g_obs] + B_* g_obs^{{mu nu}}
```

That is the EH signature route.

## What Was Derived

The operator theorem is exact conditional:

```text
P1 observed metric/coframe owner
P2 local product chart
P3 Ward/Bianchi identity
P4 Levi-Civita connection
P5 no independent extra fields
P6 no higher-derivative/nonlocal metric operators through 2PN
P7 boundary/topological/projector silence
P8 same Hilbert source and constant kappa/G

P1...P8 => EH/EC local operator
EH/EC + 4085 => gamma=beta=1, alpha_i=xi=zeta_i=0, Gdot/G=0
```

This is not claimed for MTS yet because the parent has not signed every rung.

## Double-Zero Mechanism

4086 also writes the useful decoupling lemma:

```text
C_i(X0)=0
partial_A C_i(X0)=0
H_AB(X0)>0
linear readout/projector coupling = 0
```

then the auxiliary/non-EH operator has no linear local PPN source. A single zero is not enough; the first derivative and readout must vanish too, or the operator goes into the residual vector.

## Non-EH Projection Vector

If the EH ladder fails at any rung:

```text
DeltaE_nonEH^{{mu nu}}
  = sum_i c_i E_i^{{mu nu}}
  + E_q^{{mu nu}}
  + E_projector^{{mu nu}}
  + E_boundary^{{mu nu}}
  + E_readout^{{mu nu}}
```

The projections are now fixed:

```text
delta_gamma_nonEH ~ -(kappa_ref/(C_TF U)) nabla^{{-2}} P_TF[DeltaE_nonEH_ij]
delta_beta_nonEH  := Pi_beta[DeltaE_nonEH_00 at 2PN]
alpha_i, xi       := Pi_alpha_i/Pi_xi[vector/domain/coframe/projector markers]
zeta_i            := Pi_zeta_i[nabla_mu DeltaE_nonEH^{{mu nu}} - kappa_ref DeltaJ_source^nu]
Gdot/G            := partial_t kappa_eff/kappa_eff
alpha(lambda)     := finite-range tail if an extra mode survives
```

That is the forward path: not circling, but forcing the extra pieces to either disappear by theorem or pay a bound.

## Route Selection

The broad EH-only parent assertion is too expensive to claim right now. The better route is:

```text
first fill one live non-EH projection row
compare it against 4085 gamma/beta bounds
then repeat family-by-family
```

The first target is the tracefree spatial/gamma-beta projection because 3918 already derived the gamma map and 4085 has real bounds.

## Decision

```text
EH signature theorem = exact conditional
auxiliary double-zero decoupling = exact conditional
non-EH/R11 PPN projection formulas = selected
local GR claim = still false
next gate = first non-EH R11 projection fill against gamma/beta
```

## Sources

- David Lovelock, *The Einstein Tensor and Its Generalizations*, Journal of Mathematical Physics 12, 498 (1971).
- 4085 source-stable PPN theorem and bound table.
- 3906/4019/4042 R11 and EH-selector corpus checkpoints.

## Next

```text
4087-Y5-R2FR-first-nonEH-R11-projection-fill-gamma-beta-bound.md
```

This is the clean Mayweather route: do not need a knockout claim; make each escape channel step into the ring and score it fairly.
""",
        encoding="utf-8",
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "P8_Y5_R2FR_4086_SOURCE_REGISTER.csv": source_register_rows(),
        "P8_Y5_R2FR_4086_WEB_PROVENANCE.csv": WEB_SOURCES,
        "P8_Y5_R2FR_4086_EH_SIGNATURE_THEOREM.csv": eh_signature_rows(),
        "P8_Y5_R2FR_4086_PARENT_SIGNATURE_LADDER.csv": ladder_rows(),
        "P8_Y5_R2FR_4086_AUX_DOUBLE_ZERO_LEMMA.csv": auxiliary_double_zero_rows(),
        "P8_Y5_R2FR_4086_NONEH_PPN_PROJECTION_FORMULAS.csv": projection_formula_rows(),
        "P8_Y5_R2FR_4086_R11_FAMILY_TO_PPN_ROUTE.csv": family_route_rows(),
        "P8_Y5_R2FR_4086_DECISION_GATE.csv": decision_rows(),
        "P8_Y5_R2FR_4086_CLAIM_GATE.csv": claim_gate_rows(),
        "P8_Y5_R2FR_4086_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4086_STATUS.csv": status_rows(),
    }

    output_paths: List[Path] = []
    for name, rows in outputs.items():
        path = SOURCE_DIR / name
        write_csv(path, rows)
        output_paths.append(path)

    write_doc()

    validation = validation_rows(output_paths)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4086_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    shutil.rmtree(SCRIPT_PATH.parent / "__pycache__", ignore_errors=True)

    failures = [row for row in validation if row["passed"] != "True"]
    if failures:
        for failure in failures:
            print(f"VALIDATION_FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)

    print(f"4086 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
