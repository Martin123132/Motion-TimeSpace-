from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4042_SOURCE_REGISTER.csv",
    "decoupling_classes": SOURCE_DIR / "P8_Y5_R2FR_4042_NONEH_DECOUPLING_CLASSES.csv",
    "family_classification": SOURCE_DIR / "P8_Y5_R2FR_4042_R11_FAMILY_CLASSIFICATION.csv",
    "theorem_contract": SOURCE_DIR / "P8_Y5_R2FR_4042_NONEH_THEOREM_CONTRACT.csv",
    "ppn_bound_vector": SOURCE_DIR / "P8_Y5_R2FR_4042_PPN_BOUND_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4042_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4042_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4042_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4042_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4042_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4042_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4042_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for item in rows:
        for key in item:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        (
            "SRC4042_0",
            ROOT / "4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md",
            "Remaining live local residuals: `Delta_cZ_envelope`, `Delta_cnorm_envelope`, `c_nonEH`",
            "immediate predecessor residual vector",
        ),
        (
            "SRC4042_1",
            SOURCE_DIR / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv",
            "DeltaE_MTS^{(1)}=DeltaE_MTS^{(2)}=0",
            "operator-domain theorem target",
        ),
        (
            "SRC4042_2",
            SOURCE_DIR / "P8_Y5_R2FR_4019_EH_ONLY_R11_ADOPTION_CLAUSES.csv",
            "Allowed(O_R11^{<=2PN})",
            "allowed local operator grammar",
        ),
        (
            "SRC4042_3",
            SOURCE_DIR / "P8_Y5_R2FR_4019_PPN_RESIDUAL_SCORER_ROWS.csv",
            "Pi_gamma[DeltaE_R11^{(1)}]",
            "fallback PPN scorer rows",
        ),
        (
            "SRC4042_4",
            SOURCE_DIR / "P8_Y5_R2FR_4020_LOCAL_GR_ROLLUP_CHAIN.csv",
            "S_loc^{<=2PN}=S_EH+S_matter+S_EM+dB_proper+S_topological",
            "conditional local-GR rollup",
        ),
        (
            "SRC4042_5",
            SOURCE_DIR / "P8_Y5_R2FR_4020_FIRST_EXECUTABLE_PPN_SCORE_ROWS.csv",
            "Delta_PPN_abs_4020",
            "first executable PPN score vector",
        ),
        (
            "SRC4042_6",
            SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "Every non-EH coupling that can alter the metric charge has a double zero",
            "fixed-point double-zero contract",
        ),
        (
            "SRC4042_7",
            SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "g_readout = g_obs + O((Phi-Phi0)^2)",
            "metric readout and extra-field silence block",
        ),
        (
            "SRC4042_8",
            SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv",
            "F_1 or partial_A C_i(Phi0) is nonzero",
            "failure mode for linear non-EH leakage",
        ),
        (
            "SRC4042_9",
            SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv",
            "R2_fR_scalar_mode",
            "existing R11 operator family ledger",
        ),
        (
            "SRC4042_10",
            SOURCE_DIR / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_nonEH",
            "mass/charge equality non-EH residual",
        ),
        (
            "SRC4042_11",
            SOURCE_DIR / "P8_LOCAL_ZERO_COUNTEREXAMPLE_LEDGER.csv",
            "X_D=0 implies R11/EH-only silence",
            "counterexample guard against overclaiming",
        ),
        (
            "SRC4042_12",
            SOURCE_DIR / "P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv",
            "no R11/source-normalization row promotes local GR without all source and stress rows closed",
            "R11/source-normalization promotion guard",
        ),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def decoupling_class_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "class_id": "NED4042_0_topological_or_exact",
            "class_name": "topological_or_exact",
            "mathematical_condition": "O_i=dB_i or O_i is topological and delta_g O_i=0 in the compact local exterior",
            "result": "no local Euler/PPN stress from this operator class",
            "residual_if_unsigned": "boundary_or_reference_flux_bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "class_id": "NED4042_1_absent_from_selected_packet",
            "class_name": "direct_operator_absence",
            "mathematical_condition": "S_loc^{<=2PN}=S_EH+S_matter+S_EM+dB_proper+S_topological+auxiliary/selector terms only",
            "result": "independent R2/Ricci2/Weyl2/vector/torsion operators have no direct local coefficient in the selected packet",
            "residual_if_unsigned": "Delta_nonEH_direct_bound_vector",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "class_id": "NED4042_2_auxiliary_double_zero",
            "class_name": "auxiliary_double_zero",
            "mathematical_condition": "C_i(Phi0)=0 and partial_A C_i(Phi0)=0 with positive local Hessian/operator gap",
            "result": "delta_g[C_i O_i] has no O(U) or O(U^2) PPN source on the fixed local branch",
            "residual_if_unsigned": "F1_or_mass_gap_bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "class_id": "NED4042_3_rerouted_existing_envelope",
            "class_name": "rerouted_existing_envelope",
            "mathematical_condition": "operator family is not independent; it enters through c_Z tail/wall, c_norm derivative hair, or already isolated boundary/EM channels",
            "result": "remove standalone c_nonEH duplication and carry the named upstream envelope",
            "residual_if_unsigned": "Delta_cZ_envelope_or_Delta_cnorm_envelope",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "class_id": "NED4042_4_live_ppn_bound_vector",
            "class_name": "live_ppn_bound_vector",
            "mathematical_condition": "none of the decoupling classes is parent-signed for a family",
            "result": "project that family into gamma, beta, alpha_i, xi, zeta_i, Gdot/G, and R10 alpha(lambda) components with no cancellation credit",
            "residual_if_unsigned": "Delta_PPN_abs_nonEH",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def family_classification_rows(ts: str) -> List[Dict[str, object]]:
    r11_path = SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv"
    source_rows_r11 = read_csv(r11_path)
    route_map = {
        "boundary_topological_terms": ("topological_or_exact", "covered by 4038 boundary/reference/no-flux route if fixed source-blind reference holds", "boundary_or_reference_flux_bound"),
        "R2_fR_scalar_mode": ("direct_operator_absence_or_auxiliary_double_zero", "independent R2/f(R) is absent from selected local packet; if generated by an auxiliary scalar, require C_i(Phi0)=partial_A C_i(Phi0)=0 plus mass gap", "delta_gamma_R11;delta_beta_R11;alpha(lambda)"),
        "Ricci_Weyl_squared": ("direct_operator_absence", "independent Ricci^2/Weyl^2 is not in the selected local packet through 2PN", "delta_gamma_R11;xi;wave_sector_bound"),
        "scalar_tensor_class_metric": ("rerouted_existing_envelope", "constant prefactor routes to kappa_obs; nonconstant scalar hair routes to 4030 tracefree/delta_phi plus 4041 Gdot/source-normalization envelopes", "delta_gamma_R11;delta_beta_R11;Gdot/G;alpha(lambda)"),
        "vector_preferred_frame": ("live_ppn_bound_vector", "not killed by scalar local-zero alone; needs no-vector/domain-selector theorem or alpha_i/xi products", "alpha1;alpha2;alpha3;xi"),
        "torsion_nonmetricity": ("direct_operator_absence", "selected observed local branch uses Levi-Civita metric connection and observed Hodge sector; independent torsion/nonmetricity is absent unless parent reintroduces it", "WEP;clock;lightcone;spin_source"),
        "bulk_X_force_law": ("auxiliary_double_zero_or_rerouted_existing_envelope", "bulk X force is silent only if source current and linear coupling vanish with positive mass gap; otherwise it is the finite-range/R10 branch", "eta_source_AB;gamma_minus_1;beta_minus_1;alpha(lambda)"),
        "nonlocal_memory_kernel": ("rerouted_existing_envelope", "compact local memory leakage is the 4040 c_Z tail/wall envelope, not a separate direct c_nonEH slot", "alpha3;Gdot/G;alpha(lambda);Delta_cZ_envelope"),
        "source_normalization_operator": ("rerouted_existing_envelope", "4041 split routes common mode to G_obs and retains only derivative/source hair", "Delta_cnorm_envelope;alpha_i;xi"),
        "projector_domain_stress": ("live_ppn_bound_vector", "projector/domain stress is not killed by X_D=0 alone; it requires topological/metric-independent parent ownership or explicit PPN products", "alpha1;alpha2;alpha3;xi;zeta_i"),
    }
    rows: List[Dict[str, object]] = []
    for source in source_rows_r11:
        family = source["operator_family"]
        route_class, route_reason, live_projection = route_map.get(
            family,
            ("live_ppn_bound_vector", "unclassified R11 row defaults to explicit PPN projection", "Delta_PPN_abs_nonEH"),
        )
        direct_zero_in_selected_packet = route_class in {
            "topological_or_exact",
            "direct_operator_absence",
            "direct_operator_absence_or_auxiliary_double_zero",
        }
        rows.append(
            {
                "family_id": f"R11F4042_{len(rows):02d}",
                "operator_family": family,
                "coefficient_symbol": source["coefficient_symbol"],
                "prior_coefficient_value": source["coefficient_value"],
                "prior_status": source["derivation_status"],
                "route_class": route_class,
                "route_reason": route_reason,
                "direct_zero_in_selected_packet": direct_zero_in_selected_packet,
                "live_projection_if_unsigned": live_projection,
                "source_file": str(r11_path),
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def theorem_contract_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "NTC4042_0_action_domain",
            "requirement": "local operator domain has no independent non-EH metric operators through 2PN",
            "formula": "S_loc^{<=2PN}=S_EH[g_obs]+S_matter[g_obs]+S_EM[g_obs,A]+dB_proper+S_topological+S_aux,double-zero+S_selector,silent",
            "why_needed": "prevents R2/Ricci2/Weyl2/vector/torsion slots from re-entering as free local coefficients",
            "current_status": "conditional_on_selected_packet_adoption",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NTC4042_1_double_zero",
            "requirement": "all auxiliary/non-EH couplings have a fixed-point double zero",
            "formula": "C_i(Phi0)=0 and partial_A C_i(Phi0)=0; hence delta_g(C_i O_i)|Phi0 has no linear PPN source",
            "why_needed": "kills F_1 leakage rather than tuning it small",
            "current_status": "required_not_globally_proved",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NTC4042_2_mass_gap",
            "requirement": "non-gauge extra modes have positive local source-free operator",
            "formula": "H_AB=-delta_A delta_B S_aux|Phi0 positive; m_A^2>0; no tachyonic or massless local hair",
            "why_needed": "prevents long-range scalar/vector/tensor tails after the direct slot is removed",
            "current_status": "required_for_full_zero_else_R10_PPN_bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NTC4042_3_readout_silence",
            "requirement": "observed metric and mass projector have no linear extra-field readout",
            "formula": "g_readout=g_obs+O((Phi-Phi0)^2), Pi_M=Pi_EH+O((Phi-Phi0)^2)",
            "why_needed": "prevents a formally silent operator from reappearing in measured gamma/beta/GM",
            "current_status": "present_as_minimal_block_not_final_parent_proof",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NTC4042_4_ppn_projector_fallback",
            "requirement": "every unsigned family maps to an explicit no-cancellation PPN residual",
            "formula": "Delta_PPN_abs_nonEH=sum_j |Pi_j[sum_i c_i E_i^nonEH]| <= sum_{i,j}|c_i| ||Pi_j E_i^nonEH||",
            "why_needed": "turns nonEH uncertainty into scoreable components instead of a vague blocker",
            "current_status": "bound_vector_ready_nonclaim",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def ppn_bound_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "PBN4042_0_delta_gamma_R11",
            "quantity": "delta_gamma_R11",
            "projector": "Pi_gamma[DeltaE_nonEH^(1)]",
            "no_cancellation_bound": "abs(delta_gamma_R11) <= sum_i abs(c_i)*K_gamma_i",
            "required_input": "c_i values or theorem-zero certificates for all spatial-stress operator families",
            "status": "scoreable_template_nonclaim",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "PBN4042_1_delta_beta_R11",
            "quantity": "delta_beta_R11",
            "projector": "Pi_beta[DeltaE_nonEH^(2)]",
            "no_cancellation_bound": "abs(delta_beta_R11) <= sum_i abs(c_i)*K_beta_i",
            "required_input": "second-order nonEH source/operator coefficients or double-zero proof",
            "status": "scoreable_template_nonclaim",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "PBN4042_2_preferred_frame",
            "quantity": "alpha1, alpha2, alpha3, xi",
            "projector": "Pi_alpha_xi[vector/domain/projector/memory selectors]",
            "no_cancellation_bound": "sum(abs(alpha_i))+abs(xi) <= sum_i abs(c_i)*K_alpha_xi_i",
            "required_input": "no-vector theorem or coefficient products for vector/domain/projector families",
            "status": "live_until_selector_stress_owned",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "PBN4042_3_conservation",
            "quantity": "zeta_i",
            "projector": "Pi_zeta[non-Hilbert stress/nonconservation]",
            "no_cancellation_bound": "sum_i abs(zeta_i) <= sum_k abs(c_k)*K_zeta_k",
            "required_input": "Bianchi/Hilbert-current proof or explicit nonconservation coefficients",
            "status": "scoreable_template_nonclaim",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "PBN4042_4_range_clock",
            "quantity": "alpha(lambda), Gdot/G, clock/lightcone residuals",
            "projector": "Pi_range_clock[scalar/torsion/memory/source-normalization]",
            "no_cancellation_bound": "abs(alpha(lambda))+abs(Gdot/G)+clock <= sum_i abs(c_i)*K_range_clock_i",
            "required_input": "mass gaps, kernel norms, torsion/nonmetricity absence, and 4041 Gdot/source rows",
            "status": "mostly_rerouted_to_cZ_cnorm_else_bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "PBN4042_5_master",
            "quantity": "Delta_PPN_abs_nonEH",
            "projector": "master absolute residual vector",
            "no_cancellation_bound": "Delta_PPN_abs_nonEH=sum(abs(PBN4042_0..4))",
            "required_input": "all theorem-zero certificates or numeric coefficient rows",
            "status": "local_GR_claim_blocking_until_zero_or_scored",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str, classifications: List[Dict[str, object]]) -> List[Dict[str, object]]:
    direct_zero_count = sum(1 for item in classifications if item["direct_zero_in_selected_packet"] is True)
    rerouted_count = sum(1 for item in classifications if "rerouted" in str(item["route_class"]))
    live_count = sum(1 for item in classifications if item["route_class"] == "live_ppn_bound_vector")
    return [
        {
            "case_id": "CASE4042_0_selected_packet",
            "verdict": "STANDALONE_C_NONEH_DECOMPOSED",
            "result": "In the selected local packet, direct non-EH metric operators are not free primitive coefficients; they are absent, exact/topological, auxiliary-double-zero, or rerouted.",
            "direct_zero_or_absent_families": direct_zero_count,
            "rerouted_families": rerouted_count,
            "live_ppn_families": live_count,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4042_1_if_parent_adoption_unsigned",
            "verdict": "PPN_BOUND_VECTOR_REQUIRED",
            "result": "If the selected packet is not accepted as parent-owned, every unsigned family must be scored through the PPN bound vector with no cancellation credit.",
            "direct_zero_or_absent_families": direct_zero_count,
            "rerouted_families": rerouted_count,
            "live_ppn_families": live_count,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4042_0_forward_movement",
            "decision": "replace standalone c_nonEH with an operator-family route map",
            "reason": "a single c_nonEH symbol hid too many physics channels; route classes make each channel derivable or boundable",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4042_1_selected_branch",
            "decision": "treat direct R11 operator coefficients as absent only inside the private selected local packet",
            "reason": "4037/4019/4020 already define an EH + matter + EM + topological/exact/auxiliary/selector grammar",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4042_2_no_overclaim",
            "decision": "do not promote local GR until parent adoption, double-zero, mass-gap, readout, and PPN projector clauses are signed",
            "reason": "local-zero and EH-looking first order do not by themselves remove R11/operator re-entry",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4042_3_next",
            "decision": "attack live preferred-frame/projector stress first",
            "reason": "after c_Z and c_norm routing, vector/domain/projector stress is the sharpest remaining route into alpha_i/xi",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4042_0_standalone_c_nonEH_reduced",
            "claim": "standalone c_nonEH has been decomposed into route classes and PPN projectors",
            "allowed": True,
            "public_claim_allowed": False,
            "scope": "private internal framework hygiene",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4042_1_direct_nonEH_zero",
            "claim": "direct non-EH operator coefficients vanish in the selected local packet",
            "allowed": True,
            "public_claim_allowed": False,
            "scope": "conditional on selected parent packet; not yet final parent action proof",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4042_2_full_local_GR",
            "claim": "MTS derives full local GR/PPN pass",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "blocked until live PPN/projector/source residuals are zeroed or scored",
            "timestamp_utc": ts,
        },
    ]


def remaining_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4042_0_cZ",
            "symbol": "Delta_cZ_envelope",
            "residual": "memory tail / selector wall / hidden current envelope",
            "current_route": "carried from 4040; absorbs nonlocal memory re-entry from the old R11 ledger",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4042_1_cnorm",
            "symbol": "Delta_cnorm_envelope",
            "residual": "nonconstant source-normalization derivative hair",
            "current_route": "carried from 4041; absorbs source-normalization operator re-entry from the old R11 ledger",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4042_2_ppn_projector_stress",
            "symbol": "Delta_PPN_projector_stress",
            "residual": "vector/preferred-frame/projector-domain stress components",
            "current_route": "next derivation target: prove topological/metric-independent selector stress silence or score alpha_i/xi",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4042_3_nonEH_bound_vector",
            "symbol": "Delta_PPN_abs_nonEH",
            "residual": "fallback no-cancellation PPN bound vector for any unsigned non-EH family",
            "current_route": "not a fog coefficient anymore; each family has a named projector and bound interface",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4042_0",
            "next_doc": "4043-Y5-R2FR-projector-domain-stress-silence-or-alpha-xi-bound-vector.md",
            "next_script": "scripts/Y5_R2FR_4043_projector_domain_stress_silence_or_alpha_xi_bound_vector.py",
            "why": "the live nonEH route is no longer generic; it is mostly alpha_i/xi projector/domain stress unless the parent selector is metric-independent/topological",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4042",
            "status": "STANDALONE_C_NONEH_DECOMPOSED_DIRECT_BRANCH_CONDITIONAL_PPN_BOUND_VECTOR_ACTIVE",
            "local_GR_claim": False,
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]], classifications: List[Dict[str, object]]) -> str:
    direct_zero_count = sum(1 for item in classifications if item["direct_zero_in_selected_packet"] is True)
    rerouted_count = sum(1 for item in classifications if "rerouted" in str(item["route_class"]))
    live_count = sum(1 for item in classifications if item["route_class"] == "live_ppn_bound_vector")
    source_hits = sum(1 for item in sources if item["exists"] and item["needle_found"])
    return "\n".join(
        [
            "# 4042 - nonEH Operator Decoupling Or PPN Bound Vector",
            "",
            f"- Timestamp: `{ts}`",
            "- Status: `private_nonclaim_checkpoint`",
            "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
            f"- Source needles found: `{source_hits}/{len(sources)}`.",
            "",
            "## What Actually Moved",
            "",
            "4042 breaks the old fog-symbol `c_nonEH` into operator families. In the selected local packet, direct non-EH metric operators are not independent primitive coefficients: they are absent from the packet, exact/topological, auxiliary double-zero, or rerouted into already named envelopes.",
            "",
            "The local decoupling condition is:",
            "",
            "`C_i(Phi0)=0`, `partial_A C_i(Phi0)=0`, positive local mass/operator gap, and `g_readout=g_obs+O((Phi-Phi0)^2)`.",
            "",
            "Then `delta_g[C_i O_i]` has no first-order or second-order PPN source on the fixed local branch. If any clause is unsigned, it does not get hidden; it goes to the PPN projector vector.",
            "",
            "## Family Routing",
            "",
            f"- Direct zero/absence in selected packet: `{direct_zero_count}` R11 families.",
            f"- Rerouted into `Delta_cZ_envelope` or `Delta_cnorm_envelope`: `{rerouted_count}` R11 families.",
            f"- Still live as preferred-frame/projector PPN stress: `{live_count}` R11 families.",
            "",
            "## Fallback Bound Vector",
            "",
            "`Delta_PPN_abs_nonEH=sum_j |Pi_j[sum_i c_i E_i^nonEH]| <= sum_{i,j}|c_i| ||Pi_j E_i^nonEH||`.",
            "",
            "Components: `delta_gamma_R11`, `delta_beta_R11`, `alpha1/alpha2/alpha3/xi`, `zeta_i`, `alpha(lambda)`, `Gdot/G`, clock/lightcone residuals.",
            "",
            "## Current Verdict",
            "",
            "- Current evaluator result: `STANDALONE_C_NONEH_DECOMPOSED`.",
            "- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4042`.",
            "- Remaining live local residuals: `Delta_cZ_envelope`, `Delta_cnorm_envelope`, `Delta_PPN_projector_stress`, `Delta_PPN_abs_nonEH`.",
            "",
            "## Next Target",
            "",
            "- `4043-Y5-R2FR-projector-domain-stress-silence-or-alpha-xi-bound-vector.md`",
            "- `scripts/Y5_R2FR_4043_projector_domain_stress_silence_or_alpha_xi_bound_vector.py`",
            "",
        ]
    )


def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
    return {"check_id": check_id, "passed": passed, "detail": detail}


def all_private(*tables: Iterable[Dict[str, object]]) -> bool:
    return all(item.get("valid_for_public_claim") is False for table in tables for item in table)


def validation_rows(
    sources: List[Dict[str, object]],
    classes: List[Dict[str, object]],
    classifications: List[Dict[str, object]],
    contract: List[Dict[str, object]],
    bounds: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    remaining: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH)]
    return [
        row("VAL4042_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4042_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4042_02_class_topological", any(item["class_id"] == "NED4042_0_topological_or_exact" for item in classes), "topological/exact class present"),
        row("VAL4042_03_class_absent", any(item["class_id"] == "NED4042_1_absent_from_selected_packet" for item in classes), "direct absence class present"),
        row("VAL4042_04_class_double_zero", any(item["class_id"] == "NED4042_2_auxiliary_double_zero" for item in classes), "double-zero class present"),
        row("VAL4042_05_class_ppn", any(item["class_id"] == "NED4042_4_live_ppn_bound_vector" for item in classes), "PPN fallback class present"),
        row("VAL4042_06_r11_family_count", len(classifications) == 10, "all ten R11 families classified"),
        row("VAL4042_07_r2_classified", any(item["operator_family"] == "R2_fR_scalar_mode" for item in classifications), "R2/fR family classified"),
        row("VAL4042_08_source_norm_rerouted", any(item["operator_family"] == "source_normalization_operator" and "rerouted" in str(item["route_class"]) for item in classifications), "source normalization rerouted"),
        row("VAL4042_09_memory_rerouted", any(item["operator_family"] == "nonlocal_memory_kernel" and "rerouted" in str(item["route_class"]) for item in classifications), "memory kernel rerouted"),
        row("VAL4042_10_live_projector", any(item["operator_family"] == "projector_domain_stress" and item["route_class"] == "live_ppn_bound_vector" for item in classifications), "projector stress remains live"),
        row("VAL4042_11_contract_domain", any(item["contract_id"] == "NTC4042_0_action_domain" for item in contract), "action-domain contract present"),
        row("VAL4042_12_contract_double_zero", any(item["contract_id"] == "NTC4042_1_double_zero" for item in contract), "double-zero contract present"),
        row("VAL4042_13_contract_mass_gap", any(item["contract_id"] == "NTC4042_2_mass_gap" for item in contract), "mass-gap contract present"),
        row("VAL4042_14_contract_projector", any(item["contract_id"] == "NTC4042_4_ppn_projector_fallback" for item in contract), "PPN fallback contract present"),
        row("VAL4042_15_gamma_bound", any(item["bound_id"] == "PBN4042_0_delta_gamma_R11" for item in bounds), "gamma R11 bound present"),
        row("VAL4042_16_beta_bound", any(item["bound_id"] == "PBN4042_1_delta_beta_R11" for item in bounds), "beta R11 bound present"),
        row("VAL4042_17_alpha_xi_bound", any(item["bound_id"] == "PBN4042_2_preferred_frame" for item in bounds), "preferred-frame bound present"),
        row("VAL4042_18_master_bound", any(item["bound_id"] == "PBN4042_5_master" for item in bounds), "master nonEH bound present"),
        row("VAL4042_19_evaluator_decomposed", any(item["verdict"] == "STANDALONE_C_NONEH_DECOMPOSED" for item in evaluator), "decomposition evaluator present"),
        row("VAL4042_20_decision_next", any(item["decision_id"] == "DEC4042_3_next" for item in decisions), "next decision present"),
        row("VAL4042_21_claim_decompose_internal", any(item["claim_id"] == "CLAIM4042_0_standalone_c_nonEH_reduced" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "decomposition claim scoped internal"),
        row("VAL4042_22_no_local_gr_claim", any(item["claim_id"] == "CLAIM4042_2_full_local_GR" and item["allowed"] is False for item in claims), "full local-GR claim blocked"),
        row("VAL4042_23_remaining_projector", any(item["symbol"] == "Delta_PPN_projector_stress" for item in remaining), "projector stress residual carried"),
        row("VAL4042_24_remaining_nonEH_bound", any(item["symbol"] == "Delta_PPN_abs_nonEH" for item in remaining), "nonEH bound vector carried"),
        row("VAL4042_25_next_target", bool(next_target and "4043" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4042_26_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4042_27_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4042_28_script_compiles", compile_ok, "script compiles"),
        row("VAL4042_29_private_guard", all_private(classes, classifications, contract, bounds, evaluator, decisions, remaining), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    classes = decoupling_class_rows(ts)
    classifications = family_classification_rows(ts)
    contract = theorem_contract_rows(ts)
    bounds = ppn_bound_rows(ts)
    evaluator = evaluator_rows(ts, classifications)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    remaining = remaining_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources, classifications), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["decoupling_classes"], classes)
    write_csv(OUTPUTS["family_classification"], classifications)
    write_csv(OUTPUTS["theorem_contract"], contract)
    write_csv(OUTPUTS["ppn_bound_vector"], bounds)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["remaining_residuals"], remaining)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(
        sources,
        classes,
        classifications,
        contract,
        bounds,
        evaluator,
        decisions,
        claims,
        remaining,
        next_target,
        compile_ok,
    )
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4042 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
