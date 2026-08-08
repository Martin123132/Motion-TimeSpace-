from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3974"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3974-Y5-R2FR-parent-boundary-action-scalar-marker-free-contract-or-coefficient-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3974_SOURCE_REGISTER.csv",
    "contract": SRC / "P8_Y5_R2FR_3974_PARENT_BOUNDARY_ACTION_CONTRACT.csv",
    "variation": SRC / "P8_Y5_R2FR_3974_BOUNDARY_VARIATION_ZERO_PROOF.csv",
    "ownership": SRC / "P8_Y5_R2FR_3974_BOUNDARY_PREMISE_OWNERSHIP_AUDIT.csv",
    "coefficient_values": SRC / "P8_Y5_R2FR_3974_BOUNDARY_COEFFICIENT_VALUE_REQUIREMENTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3974_BOUNDARY_ACTION_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3974_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3974_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3974_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3974_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3974_VALIDATION.csv",
}

NEXT_DOC = "3975-Y5-R2FR-boundary-scalar-singlet-selection-or-coefficient-acquisition.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3975_boundary_scalar_singlet_selection_or_coefficient_acquisition.py"


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
        ("SRC3974_00_3973_next", SRC / "P8_Y5_R2FR_3973_NEXT_TARGET.csv", "NEXT3973_0", "3973 handoff"),
        ("SRC3974_01_3973_zero", SRC / "P8_Y5_R2FR_3973_BOUNDARY_HAIR_ZERO_ATTEMPT.csv", "BHZ3973_0_conditional_nohair_lemma", "3973 conditional lemma"),
        ("SRC3974_02_3973_coeffs", SRC / "P8_Y5_R2FR_3973_BOUNDARY_HAIR_COEFFICIENT_ROWS.csv", "BHC3973_0_total_boundary_hair", "3973 coefficient vector"),
        ("SRC3974_03_3973_claim", SRC / "P8_Y5_R2FR_3973_CLAIM_GATE.csv", "CLG3973_1_zero", "3973 zero claim gate"),
        ("SRC3974_04_owner_O0", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O0_representation_zero", "scalar singlet owner attempt"),
        ("SRC3974_05_owner_O1", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O1_homogeneous_scalar_action", "homogeneous scalar action attempt"),
        ("SRC3974_06_owner_O2", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O2_scalar_not_enough_warning", "scalar-not-enough warning"),
        ("SRC3974_07_owner_O4", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O4_no_marker_fields", "no marker owner gap"),
        ("SRC3974_08_owner_O5", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O5_Ward_flux_closure", "Ward flux closure gap"),
        ("SRC3974_09_owner_O6", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O6_constant_monopole", "constant monopole gap"),
        ("SRC3974_10_owner_O7", SRC / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv", "O7_parent_owner_verdict", "owner verdict"),
        ("SRC3974_11_repair_R0", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R0_parent_scalar_boundary_action", "repair scalar boundary action"),
        ("SRC3974_12_repair_R1", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R1_no_marker_exclusion", "repair marker exclusion"),
        ("SRC3974_13_repair_R2", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R2_full_boundary_variation", "repair full variation"),
        ("SRC3974_14_repair_R3", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R3_stationary_collar_equations", "repair stationary collar"),
        ("SRC3974_15_repair_R4", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R4_flux_zero", "repair flux zero"),
        ("SRC3974_16_repair_R5", SRC / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R5_constant_monopole_derivative_silence", "repair derivative silence"),
        ("SRC3974_17_alpha3_gate", SRC / "P8_ALPHA3_THEOREM_ZERO_GATE.csv", "TG_boundary_zero", "alpha3 theorem-zero gate"),
        ("SRC3974_18_stack_T1", SRC / "P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv", "T1_boundary_scalar_no_flux", "boundary stress theorem stack"),
        ("SRC3974_19_stack_T6", SRC / "P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv", "T6_channel_guard", "channel guard"),
        ("SRC3974_20_action_A3", SRC / "P8_source_owner_parent_action_terms_CONTRACT.csv", "A3_boundary_class_topological", "source-owner boundary action term"),
        ("SRC3974_21_localzero_P1", SRC / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv", "P1_boundary_scalar_no_flux", "local-zero boundary premise"),
        ("SRC3974_22_premise_P0", SRC / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv", "P0_scalar_only_boundary_data", "premise scalar-only data"),
        ("SRC3974_23_premise_P1", SRC / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv", "P1_no_material_boundary_marker", "premise no marker"),
        ("SRC3974_24_premise_P4", SRC / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv", "P4_Ward_flux_closure", "premise Ward flux"),
        ("SRC3974_25_premise_P5", SRC / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv", "P5_constant_monopole_calibration", "premise constant monopole"),
        ("SRC3974_26_minimal_contract", SRC / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv", "MAC545_4_boundary_no_vector_tensor_hair", "minimal no-hair contract"),
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


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BAC3974_0_safe_boundary_action",
            "parent safe boundary action",
            "S_B = int_{partial M} sqrt(|gamma|) F_B(Y_I, c_top)",
            "Y_I are scalar zero-mode/class data with D_A Y_I=0 and delta Y_I/delta gamma^{AB}=lambda_I gamma_AB or 0; c_top is fixed topological data",
            "trace-only tangential stress if varied before readout",
        ),
        (
            "BAC3974_1_not_any_scalar",
            "scalar-not-enough guard",
            "arbitrary F(R_gamma, phi, D_A phi, K_AB K^AB) is unsafe",
            "tangential gradients, Hessians, K_TF, or angularly varying curvature can produce trace-free stress",
            "prevents smuggling shear/vector leakage behind the word scalar",
        ),
        (
            "BAC3974_2_marker_exclusion",
            "marker-free boundary state",
            "partial S_B/partial s_A = partial S_B/partial v_A = partial S_B/partial spin_A = partial S_B/partial frame_A = 0",
            "no tangent vector, spin marker, active-domain velocity, or preferred-frame label is an argument of S_B",
            "kills V_B and alpha1/alpha2/alpha3 preferred-frame slots if the premise is parent-owned",
        ),
        (
            "BAC3974_3_normal_exchange_zero",
            "normal exchange silence",
            "n_mu P_loc^nu_rho K_B^{mu rho}=0",
            "the boundary Euler/Ward law must set normal exchange to zero or exact parent cancellation before scoring",
            "kills J_B and the direct alpha3 boundary product",
        ),
        (
            "BAC3974_4_derivative_silence",
            "constant universal monopole",
            "partial_t mu_B = partial_r mu_B = partial_frame mu_B = partial_species mu_B = 0",
            "any remaining scalar boundary trace is a fixed calibration, not local time/radial/species hair",
            "kills Gdot, radial mass drift, and source-normalization leakage from the boundary trace",
        ),
        (
            "BAC3974_5_certificate",
            "boundary hair certificate",
            "Z_B := Z_scalar_zero_mode * Z_no_marker * Z_full_variation * Z_no_normal_exchange * Z_derivative_silence",
            "Z_B=1 implies V_B=Pi_B=J_B=D_B=0; any unsigned factor activates the coefficient branch",
            "turns the closure route into an explicit yes/no parent-action certificate",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_form": mathematical_form,
            "required_content": required_content,
            "effect_if_parent_owned": effect,
            "current_status": "CONTRACT_READY_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, clause, mathematical_form, required_content, effect in specs
    ]


def variation_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "BVP3974_0_trace_variation",
            "step": "trace-only metric variation",
            "mathematical_form": "delta S_B = 1/2 int sqrt(|gamma|) tau gamma_AB delta gamma^{AB} when delta Y_I/delta gamma^{AB}=lambda_I gamma_AB or 0",
            "derived_output": "T_B^{TF}=0",
            "status": "DERIVED_IF_BAC3974_0_AND_BAC3974_1_HOLD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "BVP3974_1_vector_absence",
            "step": "no vector representation",
            "mathematical_form": "if S_B has no boundary vector/marker/coframe argument, then delta S_B/delta v_A=0 and no B_0i/preferred-frame vector is sourced",
            "derived_output": "V_B=0",
            "status": "DERIVED_IF_BAC3974_2_HOLDS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "BVP3974_2_normal_flux",
            "step": "normal projected flux",
            "mathematical_form": "for pure tangential trace K_B^{mu nu}=k h^{mu nu}, n_mu P_loc^nu_rho K_B^{mu rho}=0; any separate normal exchange must be zero by BAC3974_3",
            "derived_output": "J_B=0",
            "status": "DERIVED_IF_TRACE_AND_NO_NORMAL_EXCHANGE_HOLD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "BVP3974_3_derivative",
            "step": "derivative silence",
            "mathematical_form": "partial_t,r,frame,species mu_B=0 gives D_B=0",
            "derived_output": "D_B=0",
            "status": "DERIVED_IF_BAC3974_4_HOLDS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "BVP3974_4_total",
            "step": "boundary hair zero theorem",
            "mathematical_form": "Z_B=1 => epsilon_boundary_vector_tensor_normal_abs=0 and W_boundary_alpha1=W_boundary_alpha2=W_boundary_alpha3=W_boundary_xi=W_boundary_beta=dln_mu_boundary_dt=0 on this channel",
            "derived_output": "boundary hair vector killed without coefficient fitting",
            "status": "CONDITIONAL_THEOREM_READY_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ownership_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BAO3974_0_scalar_zero_mode", "BAC3974_0_safe_boundary_action", "missing", "old O1 is conditional; parent action does not yet derive F_B or homogeneity", "derive scalar-singlet parent selection"),
        ("BAO3974_1_scalar_guard", "BAC3974_1_not_any_scalar", "policy_pass", "O2 warning is now explicit; unsafe scalar terms must be excluded or bounded", "audit candidate boundary invariants"),
        ("BAO3974_2_marker_free", "BAC3974_2_marker_exclusion", "missing", "O4/P1 no-marker premise is not derived", "prove scalar singlet representation or keep vector coefficients"),
        ("BAO3974_3_full_variation", "BAC3974_0_safe_boundary_action", "structural_policy_only", "boundary stress must be varied, not dropped; old ledger marks this as policy not theorem", "write full variation for candidate S_B"),
        ("BAO3974_4_normal_exchange", "BAC3974_3_normal_exchange_zero", "missing", "Ward ownership does not prove absence of normal flux", "derive boundary Euler no-flux or fill alpha3 product"),
        ("BAO3974_5_derivative_silence", "BAC3974_4_derivative_silence", "missing", "constant universal boundary monopole is not parent-derived", "derive stationarity/calibration or fill beta/Gdot/xi rows"),
        ("BAO3974_6_certificate", "BAC3974_5_certificate", "not_signed", "at least one required factor is missing, so Z_B cannot be set to 1", "go to scalar-singlet selection or coefficient acquisition"),
    ]
    return [
        {
            "audit_id": audit_id,
            "contract_clause": clause,
            "ownership_status": status,
            "current_evidence": evidence,
            "repair_or_next_test": repair,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, clause, status, evidence, repair in specs
    ]


def coefficient_value_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BCV3974_0_ZB", "Z_B", "binary_certificate", "all BAC3974 clauses parent-owned", "if true set all boundary hair coefficient products to zero", "missing_parent_signature", "not_claimable"),
        ("BCV3974_1_total", "epsilon_boundary_vector_tensor_normal_abs", "dimensionless", "|J_B|/M_H_ref + |V_B|/M_H_ref + |Pi_B|/M_H_ref + D_B", "source-backed component norms and same-frame M_H_ref", "missing_values", "not_claimable"),
        ("BCV3974_2_alpha3", "W_boundary_alpha3_epsilon_boundary_normal", "dimensionless", "alpha3_boundary = W_boundary_alpha3 epsilon_boundary_normal_flux", "zero certificate or numeric product below alpha3 lock", "missing_value_or_zero_certificate", "not_claimable"),
        ("BCV3974_3_xi", "W_boundary_xi_epsilon_boundary_TF", "dimensionless", "xi_boundary = W_boundary_xi epsilon_boundary_tracefree_tensor", "zero certificate or numeric product below xi lock", "missing_value_or_zero_certificate", "not_claimable"),
        ("BCV3974_4_Gdot", "dln_mu_boundary_dt", "yr^-1_or_declared_time_unit", "partial_t ln(mu_B) plus readout/coupling drift", "zero derivative certificate or sourced local time-drift value", "missing_value_or_zero_certificate", "not_claimable"),
    ]
    return [
        {
            "value_id": value_id,
            "symbol": symbol,
            "units": units,
            "formula": formula,
            "promotion_requirement": requirement,
            "current_status": status,
            "claim_status": claim_status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for value_id, symbol, units, formula, requirement, status, claim_status in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BAF3974_0_zero_route",
            "target": "epsilon_boundary_vector_tensor_normal_abs",
            "update_formula": "Z_B=1 => epsilon_boundary_vector_tensor_normal_abs=0",
            "meaning": "the parent-boundary action certificate would kill the whole 3973 hair vector at once",
            "status": "CONDITIONAL_THEOREM_READY_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BAF3974_1_coefficient_route",
            "target": "boundary_coefficient_values",
            "update_formula": "if Z_B!=1, fill epsilon_boundary_vector_tensor_normal_abs, W_boundary_alpha3, W_boundary_xi, W_boundary_beta, and dln_mu_boundary_dt with sourced values",
            "meaning": "failure of the proof route has an explicit empirical/math fallback instead of handwaving",
            "status": "FALLBACK_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BAF3974_2_local_GR",
            "target": "Delta_PPN_source_abs",
            "update_formula": "boundary contribution to Delta_PPN_source_abs is zero only if Z_B=1; otherwise coefficient rows feed alpha_i, xi, beta, and Gdot",
            "meaning": "local-GR promotion now has a crisp boundary certificate requirement",
            "status": "LOCAL_GR_GATE_SHARPENED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BAF3974_3_next",
            "target": "scalar_singlet_selection",
            "update_formula": "attempt to derive the scalar-zero-mode/no-marker selection from local boundary symmetry and parent configuration grammar",
            "meaning": "next route attacks the largest unsigned factor in Z_B, not another bookkeeping pass",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3974_0_contract",
            "status": "EXACT_BOUNDARY_ACTION_CONTRACT_WRITTEN",
            "meaning": "safe boundary action means scalar zero-mode/topological and trace-only under full variation; scalar words alone are rejected",
            "claim_status": "contract_nonclaim",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3974_1_conditional_theorem",
            "status": "BOUNDARY_HAIR_ZERO_THEOREM_CONDITIONAL",
            "meaning": "Z_B=1 would imply V_B=Pi_B=J_B=D_B=0 and zero the 3973 boundary coefficient products",
            "claim_status": "blocked_by_unsigned_premises",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3974_2_next",
            "status": "SCALAR_SINGLET_SELECTION_NEXT",
            "meaning": "the largest non-smuggled leap is proving the boundary sector has only scalar singlet data on the compact local branch",
            "claim_status": "private_derivation_continues",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3974_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3974_1_ZB",
            "gate": "boundary zero certificate",
            "requirement": "Z_B=1 from parent-owned scalar zero-mode, no marker, full variation, no normal exchange, derivative silence",
            "status": "BLOCKED_ZB_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3974_2_coefficients",
            "gate": "coefficient fallback",
            "requirement": "source-backed coefficient values or zero certificates for active boundary rows",
            "status": "VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3974_3_local_GR",
            "gate": "local GR",
            "requirement": "boundary certificate plus PiM/domain/EH/source-coupling/readout gates closed",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3974_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive scalar singlet/no-marker boundary selection from parent local symmetry and configuration grammar; if it fails, begin coefficient acquisition for active boundary rows",
            "success_condition": "either BAC3974_0 and BAC3974_2 become parent-owned, or the boundary coefficient fallback receives sourced values/zero certificates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PARENT_BOUNDARY_ACTION_CONTRACT_AND_ZB_CERTIFICATE_READY_NONCLAIM",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "safe boundary no-hair now requires an explicit Z_B parent certificate; scalar-only language is narrowed to scalar zero-mode/topological trace-only variation, otherwise coefficient values remain active",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3974 - Parent Boundary Action Scalar Marker-Free Contract Or Coefficient Values

Timestamp: `{timestamp}`

## Result

3974 sharpens the boundary no-hair route into an exact parent-action certificate:

```text
Z_B := Z_scalar_zero_mode
     * Z_no_marker
     * Z_full_variation
     * Z_no_normal_exchange
     * Z_derivative_silence
```

If `Z_B=1`, then:

```text
V_B = Pi_B = J_B = D_B = 0
epsilon_boundary_vector_tensor_normal_abs = 0
```

The safe boundary action is **not** arbitrary scalar language. It must be scalar-zero-mode/topological and trace-only under full variation:

```text
S_B = int_boundary sqrt(|gamma|) F_B(Y_I, c_top)
D_A Y_I = 0
delta Y_I / delta gamma^{{AB}} proportional gamma_AB or 0
no tangent marker, spin marker, domain velocity, preferred frame, K_TF, normal exchange, or derivative drift
```

## Current Verdict

The theorem is real but conditional. The current corpus does not yet parent-sign `Z_B=1`, so no local-GR/boundary pass is claimed.

## Why This Matters

This is the non-smuggled route to killing the whole 3973 boundary hair vector in one move. If it fails, the fallback is no longer vague:

```text
epsilon_boundary_vector_tensor_normal_abs
W_boundary_alpha3_epsilon_boundary_normal
W_boundary_xi_epsilon_boundary_TF
W_boundary_beta_epsilon_boundary_hair
dln_mu_boundary_dt
```

must receive sourced values or zero certificates.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3974 - Parent Boundary Action Contract And ZB Certificate

- Timestamp: `{timestamp}`
- Status: `PARENT_BOUNDARY_ACTION_CONTRACT_AND_ZB_CERTIFICATE_READY_NONCLAIM`
- Safe route:
  `Z_B=Z_scalar_zero_mode Z_no_marker Z_full_variation Z_no_normal_exchange Z_derivative_silence`.
- Conditional theorem:
  `Z_B=1 => V_B=Pi_B=J_B=D_B=0` and the 3973 boundary hair vector vanishes.
- Important guard:
  arbitrary scalar boundary language is not safe; only scalar-zero-mode/topological trace-only variation is safe.
- Current claim status: nonclaim, because `Z_B` is not parent-signed.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3974 - Parent Boundary Action Contract And ZB Certificate"
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
        "contract": contract_rows(timestamp),
        "variation": variation_rows(timestamp),
        "ownership": ownership_rows(timestamp),
        "coefficient_values": coefficient_value_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    contract = rows["contract"]
    variation = rows["variation"]
    ownership = rows["ownership"]
    values = rows["coefficient_values"]
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

    contract_ids = {row["clause_id"] for row in contract}
    proof_outputs = {row["derived_output"] for row in variation}
    ownership_statuses = {row["ownership_status"] for row in ownership}
    value_symbols = {row["symbol"] for row in values}
    feed_targets = {row["target"] for row in feed}

    return [
        val("VAL3974_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3974_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3974_02_contract_core", {"BAC3974_0_safe_boundary_action", "BAC3974_1_not_any_scalar", "BAC3974_5_certificate"} <= contract_ids, "safe action, scalar guard, and Z_B certificate clauses present"),
        val("VAL3974_03_variation_outputs", {"T_B^{TF}=0", "V_B=0", "J_B=0", "D_B=0", "boundary hair vector killed without coefficient fitting"} <= proof_outputs, "variation proof covers tensor, vector, normal, derivative, and total hair"),
        val("VAL3974_04_ownership_audit", "not_signed" in ownership_statuses and "missing" in ownership_statuses, "ownership audit keeps Z_B unsigned"),
        val("VAL3974_05_value_requirements", {"Z_B", "epsilon_boundary_vector_tensor_normal_abs", "W_boundary_alpha3_epsilon_boundary_normal", "W_boundary_xi_epsilon_boundary_TF", "dln_mu_boundary_dt"} <= value_symbols, "coefficient value requirements include certificate and active rows"),
        val("VAL3974_06_feed", {"epsilon_boundary_vector_tensor_normal_abs", "boundary_coefficient_values", "Delta_PPN_source_abs", "scalar_singlet_selection"} <= feed_targets, "feeds include zero route, fallback, PPN, and next target"),
        val("VAL3974_07_decision", any(row["status"] == "EXACT_BOUNDARY_ACTION_CONTRACT_WRITTEN" for row in decisions), "decision records exact boundary action contract"),
        val("VAL3974_08_claim_gate_ZB", any(row["status"] == "BLOCKED_ZB_NOT_PARENT_SIGNED" for row in claims), "claim gate blocks unsigned Z_B"),
        val("VAL3974_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to scalar-singlet selection"),
        val("VAL3974_10_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3974_11_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3974_12_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3974_13_spine_updated", SPINE_PATH.exists() and "3974 - Parent Boundary Action Contract And ZB Certificate" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3974_14_csv_parse", parsed, parse_detail),
        val("VAL3974_15_script_compile", True, "script compiled before validation write"),
        val("VAL3974_16_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["contract"], rows["contract"])
    write_csv(OUTPUTS["variation"], rows["variation"])
    write_csv(OUTPUTS["ownership"], rows["ownership"])
    write_csv(OUTPUTS["coefficient_values"], rows["coefficient_values"])
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
        raise SystemExit(f"3974 validation failed: {failed}")

    print(f"3974 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Parent boundary-action Z_B contract assembled; no local-GR claim promoted")


if __name__ == "__main__":
    run()
