from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3973"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3973-Y5-R2FR-boundary-vector-tensor-normal-flux-zero-or-coefficient-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3973_SOURCE_REGISTER.csv",
    "decomposition": SRC / "P8_Y5_R2FR_3973_BOUNDARY_HAIR_DECOMPOSITION.csv",
    "zero_attempt": SRC / "P8_Y5_R2FR_3973_BOUNDARY_HAIR_ZERO_ATTEMPT.csv",
    "coefficients": SRC / "P8_Y5_R2FR_3973_BOUNDARY_HAIR_COEFFICIENT_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3973_BOUNDARY_HAIR_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3973_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3973_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3973_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3973_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3973_VALIDATION.csv",
}

NEXT_DOC = "3974-Y5-R2FR-parent-boundary-action-scalar-marker-free-contract-or-coefficient-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3974_parent_boundary_action_scalar_marker_free_contract_or_coefficient_values.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3973_00_3972_next", SRC / "P8_Y5_R2FR_3972_NEXT_TARGET.csv", "NEXT3972_0", "3972 handoff"),
        ("SRC3973_01_3972_feed", SRC / "P8_Y5_R2FR_3972_BOUNDARY_FEED_UPDATE.csv", "BRF3972_4_next", "boundary hair feed"),
        ("SRC3973_02_3972_claim", SRC / "P8_Y5_R2FR_3972_CLAIM_GATE.csv", "CLG3972_3_local_GR", "local-GR boundary gate"),
        ("SRC3973_03_boundary_alpha3_target", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T0_target_projection", "alpha3 normal flux target"),
        ("SRC3973_04_scalar_boundary", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T1_scalar_boundary_action", "scalar boundary lemma"),
        ("SRC3973_05_normal_flux", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T2_no_normal_flux_from_tangential_trace", "normal flux lemma"),
        ("SRC3973_06_preferred_vector", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T3_no_preferred_vector", "preferred vector lemma"),
        ("SRC3973_07_derivative_caveat", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T4_mass_monopole_allowed", "constant monopole caveat"),
        ("SRC3973_08_parent_owner", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T5_parent_owner_audit", "parent ownership failure"),
        ("SRC3973_09_numeric_fallback", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T6_numeric_fallback", "numeric fallback"),
        ("SRC3973_10_conclusion", SRC / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T7_conclusion", "alpha3 conclusion"),
        ("SRC3973_11_cohom_target", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_0_target_certificate", "cohomology/no-hair target"),
        ("SRC3973_12_cohom_scalar", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_3_scalar_homogeneous_nohair", "scalar homogeneous no-hair"),
        ("SRC3973_13_volume_fail", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_4_volume_no_flux_not_alpha3_no_flux", "volume no-flux caveat"),
        ("SRC3973_14_derivative_silence", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_5_derivative_silence", "derivative silence"),
        ("SRC3973_15_cohom_verdict", SRC / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv", "BCT549_6_certificate_verdict", "cohomology verdict"),
        ("SRC3973_16_minimal_nohair", SRC / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv", "MAC545_4_boundary_no_vector_tensor_hair", "minimal no-hair contract"),
        ("SRC3973_17_obstruction", SRC / "P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv", "BRO543_2_vector_tensor_boundary_hair", "vector/tensor obstruction"),
        ("SRC3973_18_localzero", SRC / "P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv", "I2_boundary_alpha3_preferred_momentum", "local zero boundary caveat"),
        ("SRC3973_19_flux_fill", SRC / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv", "FB549_0_boundary_flux_bound", "boundary flux fill row"),
        ("SRC3973_20_flux_eval", SRC / "P8_Y5_BRR545_BOUNDARY_FLUX_EVALUATOR.csv", "FB549_0_boundary_flux_bound", "boundary flux evaluator"),
        ("SRC3973_21_alpha3_product_input", SRC / "P8_ALPHA3_BOUND_PRODUCT_INPUT.csv", "A3_boundary", "alpha3 product input"),
        ("SRC3973_22_alpha3_template", SRC / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv", "A3_BOUNDARY_NUMERIC_OR_ZERO", "alpha3 numeric template"),
        ("SRC3973_23_boundary_closure", SRC / "P8_BOUNDARY_ALPHA3_CLOSURE_STATUS.csv", "boundary_channel_total", "boundary closure status"),
        ("SRC3973_24_ppn_alpha1", SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv", "DPPN3967_6_alpha1", "PPN alpha1 component"),
        ("SRC3973_25_ppn_alpha2", SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv", "DPPN3967_7_alpha2", "PPN alpha2 component"),
        ("SRC3973_26_ppn_alpha3", SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv", "DPPN3967_8_alpha3", "PPN alpha3 component"),
        ("SRC3973_27_ppn_xi", SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv", "DPPN3967_9_xi", "PPN xi component"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decomposition_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BHD3973_0_decomposition",
            "object": "boundary exchange tensor",
            "definition": "decompose K_B^{mu nu} on the local boundary using n_mu, the tangential projector h^mu_nu, and the observed-frame spatial projector P_loc",
            "mathematical_form": "K_B = K_trace h + K_TF + 2 n_(mu J_B_nu) + V_B + derivative/reference pieces",
            "local_GR_risk": "only the pure tangential scalar trace is automatically harmless; vector, trace-free, normal, and drift pieces feed local PPN/source residuals",
            "status": "DECOMPOSITION_LAW_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHD3973_1_normal_flux",
            "object": "J_B^nu",
            "definition": "normal projected boundary momentum/source exchange",
            "mathematical_form": "J_B^nu := n_mu P_loc^nu_rho K_B^{mu rho}",
            "local_GR_risk": "alpha3/source-exchange and hidden exterior monopole",
            "status": "FINITE_OR_ZERO_COMPONENT_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHD3973_2_vector",
            "object": "V_B^a",
            "definition": "tangential preferred-frame/vector boundary hair after removing scalar trace",
            "mathematical_form": "V_B := P_vector(K_B - K_trace h - K_TF - normal pieces)",
            "local_GR_risk": "alpha1, alpha2, alpha3, source frame drift",
            "status": "FINITE_OR_ZERO_COMPONENT_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHD3973_3_tracefree_tensor",
            "object": "Pi_B^ab",
            "definition": "trace-free anisotropic/shear boundary stress",
            "mathematical_form": "Pi_B^{ab} := K_B^{<ab>} on the boundary tangential slice",
            "local_GR_risk": "xi/preferred-location anisotropy and beta/readout leakage",
            "status": "FINITE_OR_ZERO_COMPONENT_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHD3973_4_derivative_drift",
            "object": "D_B",
            "definition": "time/radial/frame derivative of any surviving scalar boundary monopole",
            "mathematical_form": "D_B := |partial_t ln mu_B| tau_PPN + |partial_r ln mu_B| L_PPN + |partial_frame ln mu_B|",
            "local_GR_risk": "Gdot, radial mass drift, beta/source-normalization drift",
            "status": "FINITE_OR_ZERO_COMPONENT_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_attempt_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BHZ3973_0_conditional_nohair_lemma",
            "claim_piece": "pure scalar stationary boundary no-hair",
            "mathematical_form": "S_B=int_boundary sqrt(|gamma|) F(scalars), D_A scalars=0, no marker vector/current/shear label, fixed observed coframe, no normal exchange, derivative silence => V_B=Pi_B=J_B=D_B=0",
            "derivation_status": "MATHEMATICAL_LEMMA_UNDER_LISTED_PREMISES",
            "why_not_claim": "the current parent action has not proved the boundary action is scalar-only, homogeneous, marker-free, normal-exchange-free, and derivative-silent",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHZ3973_1_tangential_trace_step",
            "claim_piece": "normal flux vanishes for pure tangential trace",
            "mathematical_form": "K_B^{mu nu}=k h^{mu nu} gives n_mu P_loc^nu_rho K_B^{mu rho}=k n_mu h^{mu rho} P_loc^nu_rho=0",
            "derivation_status": "ALGEBRAIC_PASS_IF_PURE_TRACE",
            "why_not_claim": "the pure-trace premise is not parent-owned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHZ3973_2_vector_tensor_step",
            "claim_piece": "vector and trace-free tensor vanish for homogeneous scalar boundary data",
            "mathematical_form": "delta int sqrt(|gamma|)F(Y_scalar) / delta gamma_AB = tau gamma_AB when no tangential gradients, marker vectors, or shear labels exist",
            "derivation_status": "VARIATIONAL_PASS_IF_SCALAR_HOMOGENEOUS",
            "why_not_claim": "the parent boundary sector may still contain marker/current/shear/reference data",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHZ3973_3_derivative_step",
            "claim_piece": "constant monopole derivative silence",
            "mathematical_form": "partial_t mu_B=partial_r mu_B=partial_frame mu_B=0 => D_B=0",
            "derivation_status": "TAUTOLOGICAL_PASS_IF_CONSTANT_UNIVERSAL_MONOPOLE",
            "why_not_claim": "constant/universal boundary monopole is not derived from the current parent action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHZ3973_4_current_verdict",
            "claim_piece": "current MTS boundary vector/tensor/normal zero",
            "mathematical_form": "current corpus !=> V_B=Pi_B=J_B=D_B=0",
            "derivation_status": "ZERO_CLAIM_REJECTED_FOR_NOW",
            "why_not_claim": "conditional no-hair route exists, but the necessary boundary-action premises are not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BHC3973_0_total_boundary_hair",
            "epsilon_boundary_vector_tensor_normal_abs",
            "all_boundary_hair",
            "|J_B|/M_H_ref + |V_B|/M_H_ref + |Pi_B|/M_H_ref + D_B",
            "dimensionless",
            "J_B;V_B;Pi_B;D_B;M_H_ref;source_path;normalization",
            "epsilon_boundary;epsilon_mu_extra_total;Delta_B_single_mass;Delta_PPN_source_abs",
        ),
        (
            "BHC3973_1_alpha1",
            "W_boundary_alpha1_epsilon_boundary_vector",
            "alpha1",
            "alpha1_boundary = W_boundary_alpha1 * epsilon_boundary_vector",
            "dimensionless",
            "W_boundary_alpha1;epsilon_boundary_vector;coframe;source_path;no_cancellation_policy",
            "alpha1_source",
        ),
        (
            "BHC3973_2_alpha2",
            "W_boundary_alpha2_epsilon_boundary_vector",
            "alpha2",
            "alpha2_boundary = W_boundary_alpha2 * epsilon_boundary_vector",
            "dimensionless",
            "W_boundary_alpha2;epsilon_boundary_vector;spin/precession projection;source_path;no_cancellation_policy",
            "alpha2_source",
        ),
        (
            "BHC3973_3_alpha3",
            "W_boundary_alpha3_epsilon_boundary_normal",
            "alpha3",
            "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_normal_flux",
            "dimensionless",
            "W_boundary_alpha3;epsilon_boundary_normal_flux;M_H_ref;source path;normalization;no_cancellation_policy",
            "alpha3_source",
        ),
        (
            "BHC3973_4_xi",
            "W_boundary_xi_epsilon_boundary_TF",
            "xi",
            "xi_boundary = W_boundary_xi * epsilon_boundary_tracefree_tensor",
            "dimensionless",
            "W_boundary_xi;epsilon_boundary_tracefree_tensor;external-frame anisotropy projection;source_path",
            "xi_source",
        ),
        (
            "BHC3973_5_beta",
            "W_boundary_beta_epsilon_boundary_hair",
            "beta_minus_1",
            "delta_beta_boundary = W_boundary_beta * epsilon_boundary_vector_tensor_normal_abs",
            "dimensionless",
            "W_boundary_beta;epsilon_boundary_vector_tensor_normal_abs;fixed-GM convention;source_path",
            "delta_beta_boundary_domain",
        ),
        (
            "BHC3973_6_Gdot",
            "dln_mu_boundary_dt",
            "Gdot_over_G",
            "Gdot_boundary/G = partial_t ln(mu_B) + readout/coupling drift terms",
            "yr^-1_or_declared_time_unit",
            "partial_t ln(mu_B);local clock convention;source_path;readout lock",
            "Gdot_over_G",
        ),
    ]
    return [
        {
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "observable": observable,
            "formula": formula,
            "units": units,
            "required_inputs": required_inputs,
            "feeds": feeds,
            "current_status": "COEFFICIENT_ROW_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, observable, formula, units, required_inputs, feeds in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BHF3973_0_boundary",
            "target": "epsilon_boundary",
            "update_formula": "epsilon_boundary = epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + epsilon_boundary_derivative_abs",
            "meaning": "3972 scalar/reference row is now joined to explicit vector/tensor/normal/derivative boundary hair",
            "status": "BOUNDARY_TOTAL_FEED_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHF3973_1_extra_monopole",
            "target": "epsilon_mu_extra_total",
            "update_formula": "epsilon_mu_extra_total <= epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + |Delta_PiM| + |epsilon_domain_projector| + remaining_channels_abs",
            "meaning": "boundary hair is now an explicit addend in the hidden exterior monopole budget",
            "status": "EXTRA_MONOPOLE_FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHF3973_2_PPN",
            "target": "Delta_PPN_source_abs",
            "update_formula": "Delta_PPN_boundary_abs includes |W_alpha1 eps_V|+|W_alpha2 eps_V|+|W_alpha3 eps_J|+|W_xi eps_TF|+|W_beta eps_Bhair|+|dln_mu_B/dt|tau",
            "meaning": "preferred-frame, preferred-location, beta, and Gdot boundary risks are now separated rather than hidden inside epsilon_boundary",
            "status": "PPN_FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHF3973_3_single_mass",
            "target": "Delta_B_single_mass",
            "update_formula": "|Delta_B_single_mass|/A_source^2 <= C_mu (epsilon_boundary_reference_abs + epsilon_boundary_vector_tensor_normal_abs + |Delta_PiM| + |epsilon_domain_projector| + remaining_channels_abs)",
            "meaning": "vector/tensor/normal boundary hair can obstruct the single-exterior-mass beta route unless zeroed or bounded",
            "status": "BETA_FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BHF3973_4_next",
            "target": "parent_boundary_action_premises",
            "update_formula": "try to parent-own scalar-only homogeneous marker-free boundary action with fixed coframe and no normal exchange; otherwise fill coefficient values",
            "meaning": "the next leap is not another list: it is the exact parent-action premise that would kill the whole boundary hair vector in one stroke",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3973_0_decomposition",
            "status": "BOUNDARY_HAIR_DECOMPOSED",
            "meaning": "the remaining boundary obstruction is split into normal flux, vector hair, trace-free tensor hair, and derivative drift",
            "claim_status": "symbolic_nonclaim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3973_1_zero_attempt",
            "status": "CONDITIONAL_NOHAIR_LEMMA_ONLY",
            "meaning": "the no-hair proof works under scalar homogeneous marker-free stationary boundary premises, but those premises are not parent-owned",
            "claim_status": "zero_claim_blocked",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3973_2_coefficient_rows",
            "status": "BOUNDARY_HAIR_COEFFICIENT_ROWS_CREATED",
            "meaning": "alpha1, alpha2, alpha3, xi, beta, and Gdot now have boundary coefficient/product rows to fill if zero proof fails",
            "claim_status": "values_or_zero_certificates_missing",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3973_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3973_1_zero",
            "gate": "boundary vector/tensor/normal zero promotion",
            "requirement": "parent-owned scalar homogeneous marker-free stationary boundary action, fixed coframe, no normal exchange, and derivative silence",
            "status": "BLOCKED_PREMISES_NOT_PARENT_OWNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3973_2_coefficients",
            "gate": "finite coefficient promotion",
            "requirement": "numeric/source-backed coefficients or theorem-zero certificates for alpha1, alpha2, alpha3, xi, beta, and Gdot boundary rows",
            "status": "ROWS_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3973_3_local_GR",
            "gate": "local GR",
            "requirement": "boundary hair, PiM/domain, EH dominance, fixed readout, and source coupling all closed or bounded below empirical locks",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3973_4_next",
            "gate": "next target",
            "requirement": "parent boundary action premise ownership or coefficient values",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3973_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "try to derive the parent boundary action as scalar-only, homogeneous, marker-free, fixed-coframe, no-normal-exchange, and derivative-silent; if not, start filling the boundary coefficient rows with sourced values or lower-bound estimates",
            "success_condition": "either the boundary hair vector V_B, Pi_B, J_B, D_B becomes parent-zero, or the coefficient rows become source-backed nonclaim values that can be compared to PPN/Gdot locks",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "BOUNDARY_HAIR_DECOMPOSITION_AND_COEFFICIENT_ROWS_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "boundary vector/tensor/normal/derivative hair now has an exact conditional no-hair lemma and finite coefficient/product rows feeding PPN, Gdot, beta, and hidden-monopole budgets",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3973 - Boundary Vector Tensor Normal Flux Zero Or Coefficient Row

Timestamp: `{timestamp}`

## Result

3973 decomposes the remaining boundary hair instead of leaving it as a single foggy blocker:

```text
K_B = K_trace h + K_TF + 2 n_(mu J_B_nu) + V_B + derivative/reference pieces
```

The harmless case is now sharp:

```text
S_B = int_boundary sqrt(|gamma|) F(scalars)
D_A scalars = 0
no marker vector/current/shear label
fixed observed coframe
no normal exchange
derivative silence

=> V_B = Pi_B = J_B = D_B = 0
```

That is a real conditional lemma, not a closure axiom. It is **not** promoted because the current parent action does not yet own those premises.

## Coefficient Fallback

If the parent-action proof fails, the boundary hair now has fillable rows:

```text
epsilon_boundary_vector_tensor_normal_abs
W_boundary_alpha1_epsilon_boundary_vector
W_boundary_alpha2_epsilon_boundary_vector
W_boundary_alpha3_epsilon_boundary_normal
W_boundary_xi_epsilon_boundary_TF
W_boundary_beta_epsilon_boundary_hair
dln_mu_boundary_dt
```

These feed:

```text
epsilon_boundary
epsilon_mu_extra_total
Delta_B_single_mass
Delta_PPN_source_abs
```

## Decision

No local-GR claim is made. But the next target is now more ambitious and cleaner: parent-own the boundary action premises, because that would kill the whole boundary hair vector rather than chasing one coefficient at a time.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3973 - Boundary Hair Decomposition And Coefficient Rows

- Timestamp: `{timestamp}`
- Status: `BOUNDARY_HAIR_DECOMPOSITION_AND_COEFFICIENT_ROWS_READY`
- Conditional no-hair lemma:
  scalar-only homogeneous marker-free stationary boundary action with fixed coframe, no normal exchange, and derivative silence gives `V_B=Pi_B=J_B=D_B=0`.
- Current claim status: nonclaim, because the parent action has not yet signed those premises.
- Fallback rows:
  `W_boundary_alpha1`, `W_boundary_alpha2`, `W_boundary_alpha3`, `W_boundary_xi`, `W_boundary_beta`, and `dln_mu_boundary_dt`.
- Feed:
  boundary hair now enters `epsilon_boundary`, `epsilon_mu_extra_total`, `Delta_B_single_mass`, and `Delta_PPN_source_abs` explicitly.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3973 - Boundary Hair Decomposition And Coefficient Rows"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    return {
        "sources": sources,
        "decomposition": decomposition_rows(timestamp),
        "zero_attempt": zero_attempt_rows(timestamp),
        "coefficients": coefficient_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    decomposition = rows["decomposition"]
    zero_attempt = rows["zero_attempt"]
    coefficients = rows["coefficients"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    coeff_observables = {row["observable"] for row in coefficients}
    feed_targets = {row["target"] for row in feed}
    component_objects = {row["object"] for row in decomposition}

    return [
        val("VAL3973_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3973_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3973_02_decomposition", {"J_B^nu", "V_B^a", "Pi_B^ab", "D_B"} <= component_objects, "boundary decomposition includes normal, vector, tensor, and derivative pieces"),
        val("VAL3973_03_conditional_lemma", any(row["row_id"] == "BHZ3973_0_conditional_nohair_lemma" for row in zero_attempt), "conditional no-hair lemma row present"),
        val("VAL3973_04_rejection_verdict", any(row["row_id"] == "BHZ3973_4_current_verdict" and row["derivation_status"] == "ZERO_CLAIM_REJECTED_FOR_NOW" for row in zero_attempt), "zero claim rejected for current corpus"),
        val("VAL3973_05_coefficients", {"all_boundary_hair", "alpha1", "alpha2", "alpha3", "xi", "beta_minus_1", "Gdot_over_G"} <= coeff_observables, "boundary coefficient rows cover all intended locks"),
        val("VAL3973_06_score_ready", all(row["score_ready"] for row in coefficients), "all coefficient rows are score-ready symbolic forms"),
        val("VAL3973_07_feed", {"epsilon_boundary", "epsilon_mu_extra_total", "Delta_PPN_source_abs", "Delta_B_single_mass", "parent_boundary_action_premises"} <= feed_targets, "feeds reach boundary, hidden mass, PPN, beta, and next premise target"),
        val("VAL3973_08_decision", any(row["status"] == "BOUNDARY_HAIR_COEFFICIENT_ROWS_CREATED" for row in decisions), "decision creates boundary coefficient rows"),
        val("VAL3973_09_claim_gate_zero", any(row["status"] == "BLOCKED_PREMISES_NOT_PARENT_OWNED" for row in claims), "claim gate blocks no-hair promotion"),
        val("VAL3973_10_claim_gate_local", any(row["status"] == "LOCAL_GR_STILL_OPEN" for row in claims), "local GR remains open"),
        val("VAL3973_11_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to parent boundary action premise ownership"),
        val("VAL3973_12_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3973_13_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3973_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3973_15_spine_updated", SPINE_PATH.exists() and "3973 - Boundary Hair Decomposition And Coefficient Rows" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3973_16_csv_parse", parsed, parse_detail),
        val("VAL3973_17_script_compile", True, "script compiled before validation write"),
        val("VAL3973_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["decomposition"], rows["decomposition"])
    write_csv(OUTPUTS["zero_attempt"], rows["zero_attempt"])
    write_csv(OUTPUTS["coefficients"], rows["coefficients"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3973 validation failed: {failed}")

    print(f"3973 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Boundary hair decomposed; conditional no-hair lemma and coefficient rows assembled")


if __name__ == "__main__":
    run()
