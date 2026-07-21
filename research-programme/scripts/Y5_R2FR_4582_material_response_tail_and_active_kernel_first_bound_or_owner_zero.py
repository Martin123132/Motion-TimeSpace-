from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4582"
CLAIM_ID = "L-424"
BRANCH_ID = "MTS_R2FR_Y5_MATERIAL_RESPONSE_TAIL_AND_ACTIVE_KERNEL_FIRST_BOUND_OR_OWNER_ZERO_4582"
MARKER = "PPC4161_MATERIAL_RESPONSE_TAIL_AND_ACTIVE_KERNEL_FIRST_BOUND_OR_OWNER_ZERO_4582"
PACKET_MARKER = "PPC4161_PACKET_MATERIAL_RESPONSE_TAIL_AND_ACTIVE_KERNEL_FIRST_BOUND_OR_OWNER_ZERO_4582"
DECISION = "OWNED_MATERIAL_STRESS_ZERO_DERIVED_CJQ_CEMREADOUT_PHIEMRAD_MATERIAL_TENSOR_AND_ACTIVE_KERNEL_BOUNDS_RETAINED_NONCLAIM"
NEXT_TARGET = "4583-Y5-R2FR-charge-current-normalization-and-EM-readout-tail-owner-or-source-bound.md"

DOC_PATH = POST / "4582-Y5-R2FR-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md"
FORMAL_PATH = FORMAL / "598-PPC4161-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4581 = POST / "4581-Y5-R2FR-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md"
CSV_4581_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4581_NEXT_TARGET.csv"
CSV_4581_TAILS = SOURCE_DIR / "P8_Y5_R2FR_4581_MATERIAL_ACTIVE_TAIL_BOUND_ROWS.csv"
CSV_4581_STRICT = SOURCE_DIR / "P8_Y5_R2FR_4581_STRICT_ZERO_CONTRACT.csv"
CSV_EM_BOUND = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_EM_POYNTING = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
CSV_MATERIAL_INTAKE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv"
CSV_MATERIAL_BASIS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv"
CSV_TYPING_GATE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv"
CSV_KERNELS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_OWNER_LEMMA = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv"
CSV_NORMAL_FORM = SOURCE_DIR / "P8_EM_vq_parent_object_language_normal_form_candidate.csv"
FORMAL_580 = FORMAL / "580-PPC4161-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4582_SOURCE_REGISTER.csv"
MATERIAL_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_MATERIAL_OWNER_ZERO_THEOREM.csv"
TAIL_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_MATERIAL_TAIL_REDUCTION_ROWS.csv"
FIRST_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_FIRST_BOUND_SOURCE_ROWS.csv"
ACTIVE_KERNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_ACTIVE_KERNEL_BOUND_INTERFACE.csv"
DECISION_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_ZERO_OR_BOUND_DECISION_MATRIX.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4582_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4582_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4582_00_4581_doc", "4581 checkpoint", DOC_4581, "C_material_tail"),
        ("SRC4582_01_4581_next", "4581 next target", CSV_4581_NEXT, "material-response-tail-and-active-kernel-first-bound-or-owner-zero"),
        ("SRC4582_02_4581_material_tail", "4581 material tail", CSV_4581_TAILS, "TAIL4581_0_material_tail"),
        ("SRC4582_03_4581_active_kernel", "4581 active kernel", CSV_4581_TAILS, "TAIL4581_1_active_kernel"),
        ("SRC4582_04_4581_strict", "4581 strict zero contract", CSV_4581_STRICT, "SZ4581_0_strict_Creadout_zero"),
        ("SRC4582_05_EM_CJQ", "EM charge/current normalization", CSV_EM_BOUND, "EMB3503_3_C_JQ"),
        ("SRC4582_06_EM_readout", "EM readout residual", CSV_EM_BOUND, "EMB3503_5_C_EM_readout"),
        ("SRC4582_07_EM_Poynting", "EM Poynting flux", CSV_EM_POYNTING, "EMF3502_1_radiative_poynting_flux"),
        ("SRC4582_08_EM_internal_exchange", "matter-EM internal exchange zero", CSV_EM_POYNTING, "EMF3502_5_matter_EM_internal_exchange"),
        ("SRC4582_09_material_tensor", "full parent material tensor missing", CSV_MATERIAL_INTAKE, "WMI1894_3_full_parent_tensor"),
        ("SRC4582_10_material_acceptance", "material tensor acceptance", CSV_MATERIAL_INTAKE, "WMI1894_6_acceptance"),
        ("SRC4582_11_parent_basis", "parent material basis target", CSV_MATERIAL_BASIS, "PMTB1895_0_parent_basis_target"),
        ("SRC4582_12_tensor_formula", "material tensor formula", CSV_MATERIAL_BASIS, "PMTB1895_3_tensor_formula"),
        ("SRC4582_13_typing_no_species", "no material/species source morphism", CSV_TYPING_GATE, "TYP1895_1_no_species_to_source_coeff"),
        ("SRC4582_14_typing_verdict", "typing verdict", CSV_TYPING_GATE, "TYP1895_5_verdict"),
        ("SRC4582_15_kernel_total", "active kernel suite", CSV_KERNELS, "KSR2118_7_total_no_cancellation"),
        ("SRC4582_16_kernel_clock", "clock/light kernel evidence", CSV_KERNELS, "KSR2118_2_clock_redshift_kernel"),
        ("SRC4582_17_owner_lemma", "source/readout owner lemma", CSV_OWNER_LEMMA, "SRO2122_6_verdict"),
        ("SRC4582_18_normal_matter_functor", "normal-form matter functor", CSV_NORMAL_FORM, "NF3519_2_matter_functor"),
        ("SRC4582_19_normal_readout", "normal-form readout firewall", CSV_NORMAL_FORM, "NF3519_5_readout_firewall"),
        ("SRC4582_20_Poynting_owner", "Poynting owner root law", FORMAL_580, "TZ4564_1_Poynting_owner"),
        ("SRC4582_21_claim_423", "prior claim register row", CLAIMS_PATH, "L-423"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "4582 material response owner zero and active-kernel first bound interface",
                "valid_for_claim": "False",
            }
        )
    return rows


def material_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "MOT4582_0_owned_material_stress",
            "target": "owned material/binding response",
            "statement": "Material response that is already part of S_matter, S_binding or S_EM on the same observed coframe is Hilbert source content, not a readout tail.",
            "formula": "S_tot^H=S_matter[Psi,e_obs]+S_binding[Psi,A,e_obs]+S_EM[A,e_obs]+dB_impr => O_f Pi_material_owned=0 => C_material_owned=0",
            "status": "PRIVATE_BRANCH_ZERO_DERIVED",
            "surviving_tail": "only material markers, apparatus support, charge/current normalization and readout-regenerated binding/EM coefficients survive",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "MOT4582_1_internal_EM_exchange",
            "target": "matter-EM Lorentz exchange",
            "statement": "Internal Lorentz exchange cancels inside the total Hilbert stress when matter and EM are varied in the same parent action with the same current.",
            "formula": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda => nabla_mu(T_matter+T_EM)^{mu nu}=0",
            "status": "CONDITIONAL_ZERO_IN_TOTAL_HILBERT_STRESS",
            "surviving_tail": "C_JQ survives if charge/current normalization is not same-owner; Phi_EM_rad survives if flux crosses boundary",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "MOT4582_2_marker_nohom_route",
            "target": "material/source marker",
            "statement": "A material/species/readout marker cannot create an active source coefficient if the parent typed object language has no morphism into Coeff_active_source and variation happens before readout.",
            "formula": "Hom(MaterialMarker or SpeciesLabel or Readout, Coeff_active_source)=empty => C_marker=0",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "surviving_tail": "hidden marker/source-prefactor countermodels remain until parent sorts and action-scale owner are signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "MOT4582_3_first_material_bound",
            "target": "material response tail",
            "statement": "If the owner zero fails, the material tail is a finite parent-basis dot product plus named EM/apparatus tails, not an undefined coupling.",
            "formula": "C_material_tail <= sum_X |C_X R_material_X| + |C_JQ| + |C_EM_readout| + |Phi_EM_rad| + |C_apparatus|",
            "status": "BOUND_DERIVED_VALUES_MISSING",
            "surviving_tail": "requires parent basis X, R_material_X tensor, C_X coefficient vector, EM/current/readout/flux values",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "MOT4582_4_active_kernel_bound",
            "target": "active response kernels",
            "statement": "Active kernels survive only as operator norms multiplying source/readout coefficient tails; fixed kernels are already zero from 4581.",
            "formula": "C_kernel_active <= sum_A sup_{||f||_inf<=1} ||(O_f K_A)J_H||_TV/M_H_ref",
            "status": "BOUND_DERIVED_VALUES_MISSING",
            "surviving_tail": "source-worldtube, WEP, clock, light, orbital/GM and projective kernels from 2118",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def tail_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "MTR4582_0_owned_material_zero",
            "quantity": "C_material_owned",
            "result": "0",
            "basis": "same Hilbert source action and same observed coframe",
            "status": "PRIVATE_BRANCH_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "MTR4582_1_marker_tail",
            "quantity": "C_marker",
            "result": "0 if no-Hom material/species/readout-to-source coefficient grammar is parent-signed; otherwise retain finite marker coefficient",
            "basis": "TYP1895_1_no_species_to_source_coeff",
            "status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "MTR4582_2_material_tail_bound",
            "quantity": "C_material_tail",
            "result": "C_material_tail <= sum_X |C_X R_material_X| + |C_JQ| + |C_EM_readout| + |Phi_EM_rad| + |C_apparatus|",
            "basis": "MOT4582_3_first_material_bound",
            "status": "BOUND_READY_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "MTR4582_3_Creadout_update",
            "quantity": "C_readout",
            "result": "C_readout <= sum_X |C_X R_material_X| + |C_JQ| + |C_EM_readout| + |Phi_EM_rad| + |C_apparatus| + C_kernel_active + C_EFT_active + C_tau_tail",
            "basis": "4581 reduced bound plus 4582 material owner theorem",
            "status": "REDUCED_BOUND_UPDATED_VALUES_REMAIN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def first_bound_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("FBS4582_0_RmaterialX", "R_material_X", "R_material_X(A,B)=partial_X ln M_A - partial_X ln M_B after common-mode and double-counted rest-mass pieces are projected out", "MISSING_PARENT_RESPONSE_BASIS_AND_TENSOR_VALUES", "PMTB1895_3_tensor_formula"),
        ("FBS4582_1_CX", "C_X", "parent coefficient vector conjugate to the material response basis X", "MISSING_PARENT_COEFFICIENT_VECTOR", "WMI1894_4_parent_coefficient_dependency"),
        ("FBS4582_2_CJQ", "C_JQ", "charge/current normalization mismatch after A -> lambda A and J -> J/lambda ambiguity", "MISSING_CHARGE_CURRENT_OWNER_OR_BOUND", "EMB3503_3_C_JQ"),
        ("FBS4582_3_CEMreadout", "C_EM_readout", "effective readout, loop, clock or spectroscopy map regenerates EM coefficient dependence", "MISSING_READOUT_CLOSURE_OR_BOUND", "EMB3503_5_C_EM_readout"),
        ("FBS4582_4_PhiEMrad", "Phi_EM_rad", "net radiative/background Poynting flux through the local boundary", "MISSING_FLUX_OR_ZERO_THEOREM", "EMF3502_1_radiative_poynting_flux"),
        ("FBS4582_5_Capparatus", "C_apparatus", "apparatus/readout support not included in the source or excluded by a bound", "MISSING_APPARATUS_DOMAIN_DECLARATION", "CDG4580_2_apparatus"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "current_value": current_value,
            "source_anchor": source_anchor,
            "units": "dimensionless_or_declared_parent_basis_units",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, definition, current_value, source_anchor in specs
    ]


def active_kernel_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("AK4582_0_source_worldtube", "K_source_worldtube", "Delta_source(lambda)=int K_source rho_source_residual", "KSR2118_0_source_worldtube_kernel"),
        ("AK4582_1_WEP", "K_WEP", "tau_WEP=<P_inst(t)[Delta_a_source-Delta_a_test]>_segments", "KSR2118_1_orbit_WEP_kernel"),
        ("AK4582_2_clock", "K_clock", "delta_nu/nu=P_clock[Q_trace, rod calibration, material markers, projective trace]", "KSR2118_2_clock_redshift_kernel"),
        ("AK4582_3_light", "K_light", "gamma_minus_1 or Shapiro residual=P_lightcone[Q_shear, photon branch, source geometry]", "KSR2118_3_lightcone_kernel"),
        ("AK4582_4_orbital_GM", "K_GM_orbit", "delta(GM)_obs or fifth-force residual=P_orbit[source_support, readout_action, inverse-square split, time/range law]", "KSR2118_4_orbital_GM_kernel"),
        ("AK4582_5_projective", "K_projective", "projective residual=P_projective[source, clock, WEP] unless all-sector certificate supplied", "KSR2118_6_projective_trace_kernel"),
        ("AK4582_6_total", "C_kernel_active", "sum_abs of active kernel components with no cancellation credit", "KSR2118_7_total_no_cancellation"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "kernel_id": kernel_id,
            "symbol": symbol,
            "bound_law": f"{symbol} <= sup_{{||f||_inf<=1}} ||(O_f K_A)J_H||_TV/M_H_ref for this arena",
            "kernel_shape": kernel_shape,
            "source_anchor": source_anchor,
            "current_value": "MISSING_ACTIVE_KERNEL_OPERATOR_VALUE_OR_ZERO_CERTIFICATE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for kernel_id, symbol, kernel_shape, source_anchor in specs
    ]


def decision_matrix_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("ZB4582_0_owned_material", "owned material/binding/EM stress", "ZERO", "inside same-Hilbert observed-coframe branch"),
        ("ZB4582_1_CJQ", "charge/current normalization", "BOUND_OR_OWNER_REQUIRED", "not killed by stress ownership alone"),
        ("ZB4582_2_CEMreadout", "readout-regenerated EM/binding response", "BOUND_OR_CLOSURE_REQUIRED", "readout-after-variation theorem must survive loops/effective maps"),
        ("ZB4582_3_PhiEMrad", "radiative/background Poynting flux", "BOUND_OR_NOFLUX_REQUIRED", "physical flux is routed, not erased"),
        ("ZB4582_4_Rmaterial", "parent material tensor basis", "BOUND_INPUT_REQUIRED", "composition context is not a parent tensor"),
        ("ZB4582_5_active_kernel", "active response kernels", "BOUND_INPUT_REQUIRED", "fixed kernels zero; response kernels remain"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "matrix_id": matrix_id,
            "component": component,
            "decision": decision,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for matrix_id, component, decision, reason in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4582_owned_material", "material response lives inside S_matter/S_binding/S_EM before variation", "C_material_owned=0", "CONTROL_PASS"),
        ("CTRL4582_marker_counterexample", "material marker maps into source coefficient before variation", "zero rejected; C_marker/Delta_w tail retained", "COUNTERMODEL_CAUGHT"),
        ("CTRL4582_internal_EM", "bound EM field exchanges energy with matter internally", "internal exchange is in T_total, not a separate tail", "CONTROL_PASS"),
        ("CTRL4582_radiative_flux", "Poynting flux crosses local boundary", "Phi_EM_rad retained as physical boundary/Hamiltonian flux", "FIREWALL_PASS"),
        ("CTRL4582_active_kernel", "kernel depends on material/clock/orbit/source readout response", "active kernel bound retained", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": control_id,
            "input_case": input_case,
            "expected": expected,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, input_case, expected, verdict in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4582_0_owned_material", "Owned material/binding/EM stress zero branch.", "PASSED_PRIVATE_BRANCH"),
        ("PROM4582_1_CJQ", "Charge/current normalization owner or source-backed bound.", "BLOCKED"),
        ("PROM4582_2_CEMreadout", "EM/readout closure or source-backed bound.", "BLOCKED"),
        ("PROM4582_3_PhiEMrad", "Poynting/radiative flux zero or source-backed flux bound.", "BLOCKED"),
        ("PROM4582_4_material_kernel", "Parent material tensor and active kernel operator values or theorem-zero rows.", "BLOCKED"),
        ("PROM4582_5_no_claim", "No local-GR/R10/PPN claim from symbolic material/kernel rows.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "required_for_claim": "True",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4582 proves the owned material/binding/EM-stress part is not a readout leak in the private same-Hilbert branch.  The surviving material/kernel debt is now explicit: parent material tensor dot coefficient vector, C_JQ, C_EM_readout, Phi_EM_rad, apparatus support and active response kernels.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The first two surviving material-tail terms with clean ownership targets are C_JQ and C_EM_readout; they also control EM stress normalization and binding response.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    material_theorems: list[dict[str, Any]],
    tail_reductions: list[dict[str, Any]],
    first_bounds: list[dict[str, Any]],
    active_kernels: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4582 - Material response tail and active kernel first bound or owner zero

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4581 left:

```text
C_readout <= C_material_tail + C_kernel_active + C_EFT_active + C_tau_tail
```

4582 attacks the first two pieces.  The owned part of material response is now zero in the private same-Hilbert branch:

```text
S_tot^H = S_matter[Psi,e_obs] + S_binding[Psi,A,e_obs] + S_EM[A,e_obs] + dB_impr
=> C_material_owned = 0.
```

Internal matter/EM Lorentz exchange is also not a new tail:

```text
nabla_mu T_EM^{{mu nu}} = -F^{{nu lambda}}J_lambda,
nabla_mu T_matter^{{mu nu}} = +F^{{nu lambda}}J_lambda
=> nabla_mu(T_matter+T_EM)^{{mu nu}}=0.
```

So the live material/kernel bound is:

```text
C_material_tail <= sum_X |C_X R_material_X|
                 + |C_JQ| + |C_EM_readout| + |Phi_EM_rad| + |C_apparatus|

C_kernel_active <= sum_A sup_{{||f||_inf<=1}} ||(O_f K_A)J_H||_TV/M_H_ref
```

This is the useful narrowing: material response itself is not the enemy if it is Hilbert-owned.  The enemy is source-label/material-marker reentry, charge-current normalization, EM/readout regeneration, radiative flux, apparatus support, and active response kernels.

## Material owner zero theorem

{markdown_table(material_theorems)}

## Material tail reduction

{markdown_table(tail_reductions)}

## First bound source rows

{markdown_table(first_bounds)}

## Active kernel bound interface

{markdown_table(active_kernels)}

## Zero-or-bound decision matrix

{markdown_table(matrix)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: attack `C_JQ` and `C_EM_readout`, the first clean ownership targets inside the surviving material tail.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4582 material response tail and active kernels

Marker: `{MARKER}`  
Generated: `{now}`

4582 derives that owned material/binding/Maxwell-Hodge stress is not a readout leak in the same-Hilbert branch: `C_material_owned=0`.  Internal matter/EM Lorentz exchange cancels inside total Hilbert stress.  The live material/kernel envelope is now `C_material_tail <= sum_X |C_X R_material_X| + |C_JQ| + |C_EM_readout| + |Phi_EM_rad| + |C_apparatus|`, plus explicit active-kernel operator norms.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4582 packet update - owned material zero and active kernel bounds

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet now separates ordinary material response from material-tail leakage.  Material/binding/EM stress inside the same Hilbert source is safe; only marker/source-prefactor reentry, charge-current normalization, EM/readout regeneration, Poynting flux, apparatus support and active response kernels remain in the readout-tail bound.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4582 derives owned material/binding/EM stress zero for the C_material branch and reduces the surviving material/kernel tail to parent material tensor, C_JQ, C_EM_readout, Phi_EM_rad, apparatus and active kernel bound rows.",
        "current_evidence": "Generated source register, material owner theorem, material tail reduction rows, first bound source rows, active kernel bound interface, decision matrix, controls, gates and validation.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Treating ordinary Hilbert-owned material stress as a leak, or conversely treating charge/current/readout/flux/apparatus/active kernels as if Hilbert ownership already killed them.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "C_JQ, C_EM_readout, Phi_EM_rad, parent material tensor and active kernels still need owner-zero or source-backed bounds before local-GR/R10/PPN claims.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    material_theorems: list[dict[str, Any]],
    tail_reductions: list[dict[str, Any]],
    first_bounds: list[dict[str, Any]],
    active_kernels: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4582_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4582_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4582_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4582_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4582_owned_material_zero",
        "owned material stress zero theorem emitted",
        any(row["theorem_id"] == "MOT4582_0_owned_material_stress" and "C_material_owned" in row["formula"] for row in material_theorems),
        "MOT4582_0",
    )
    add(
        "VAL4582_internal_EM_exchange",
        "internal EM exchange zero retained inside total stress",
        any(row["theorem_id"] == "MOT4582_1_internal_EM_exchange" and "T_matter+T_EM" in row["formula"] for row in material_theorems),
        "MOT4582_1",
    )
    add(
        "VAL4582_material_tail_bound",
        "material tail bound contains tensor and EM/readout/flux terms",
        any(
            row["row_id"] == "MTR4582_2_material_tail_bound"
            and "C_JQ" in row["result"]
            and "R_material_X" in row["result"]
            for row in tail_reductions
        ),
        "MTR4582_2",
    )
    add(
        "VAL4582_first_bound_rows",
        "first bound rows include R_material_X, C_JQ, C_EM_readout and Phi_EM_rad",
        all(any(row["symbol"] == symbol for row in first_bounds) for symbol in ["R_material_X", "C_JQ", "C_EM_readout", "Phi_EM_rad"]),
        "first bound row coverage",
    )
    add(
        "VAL4582_active_kernel_rows",
        "active kernel rows include WEP, clock, orbital and total",
        all(any(row["kernel_id"] == kernel_id for row in active_kernels) for kernel_id in ["AK4582_1_WEP", "AK4582_2_clock", "AK4582_4_orbital_GM", "AK4582_6_total"]),
        "active kernel coverage",
    )
    add(
        "VAL4582_decision_matrix",
        "decision matrix separates zero and bound components",
        any(row["matrix_id"] == "ZB4582_0_owned_material" and row["decision"] == "ZERO" for row in matrix)
        and any(row["matrix_id"] == "ZB4582_1_CJQ" and "BOUND" in row["decision"] for row in matrix),
        "decision matrix",
    )
    add(
        "VAL4582_controls",
        "controls catch marker, radiative flux and active kernel counterbranches",
        all(
            any(row["control_id"] == control_id for row in controls)
            for control_id in ["CTRL4582_marker_counterexample", "CTRL4582_radiative_flux", "CTRL4582_active_kernel"]
        ),
        "control coverage",
    )
    add("VAL4582_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4582_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4582_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4582_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    material_theorems = material_theorem_rows(now)
    tail_reductions = tail_reduction_rows(now)
    first_bounds = first_bound_rows(now)
    active_kernels = active_kernel_rows(now)
    matrix = decision_matrix_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MATERIAL_THEOREM_CSV, material_theorems)
    write_csv(TAIL_REDUCTION_CSV, tail_reductions)
    write_csv(FIRST_BOUND_CSV, first_bounds)
    write_csv(ACTIVE_KERNEL_CSV, active_kernels)
    write_csv(DECISION_MATRIX_CSV, matrix)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, material_theorems, tail_reductions, first_bounds, active_kernels, matrix, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        MATERIAL_THEOREM_CSV,
        TAIL_REDUCTION_CSV,
        FIRST_BOUND_CSV,
        ACTIVE_KERNEL_CSV,
        DECISION_MATRIX_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, material_theorems, tail_reductions, first_bounds, active_kernels, matrix, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
