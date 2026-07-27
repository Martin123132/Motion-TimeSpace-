from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3019"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3019-Y5-R2FR-beta-square-law-source-normalization-gate-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3019_00_3018_doc": ROOT / "3018-Y5-R2FR-gamma-coefficient-fill-AST-or-beta-square-law-branch-under-AX1090.md",
    "SRC3019_01_3018_beta_handoff": RESIDUALS / "P8_Y5_R2FR_3018_BETA_SQUARE_LAW_HANDOFF.csv",
    "SRC3019_02_3018_next": RESIDUALS / "P8_Y5_R2FR_3018_NEXT_TARGET.csv",
    "SRC3019_03_2920_doc": ROOT / "2920-Y5-R2FR-beta-source-normalization-second-order-kernel-or-parent-square-law-under-AX1090.md",
    "SRC3019_04_2920_square_audit": RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv",
    "SRC3019_05_2920_beta_kernel": RESIDUALS / "P8_Y5_R2FR_2920_BETA_SECOND_ORDER_SOURCE_NORMALIZATION_KERNEL.csv",
    "SRC3019_06_2920_newton_queue": RESIDUALS / "P8_Y5_R2FR_2920_SOURCE_NORMALIZED_NEWTON_GAUSS_ORBITAL_SCORECARD_QUEUE.csv",
    "SRC3019_07_2929_doc": ROOT / "2929-Y5-R2FR-beta-source-normalization-square-law-or-finite-source-residual-under-AX1090.md",
    "SRC3019_08_2929_residual_vector": RESIDUALS / "P8_Y5_R2FR_2929_BETA_FINITE_RESIDUAL_VECTOR.csv",
    "SRC3019_09_2930_doc": ROOT / "2930-Y5-R2FR-source-owner-Hcore-to-beta-denominator-binding-or-finite-local-residual-first-value-under-AX1090.md",
    "SRC3019_10_2930_denominator": RESIDUALS / "P8_Y5_R2FR_2930_DENOMINATOR_BINDING_CONTRACT.csv",
    "SRC3019_11_2930_coefficients": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "SRC3019_12_2893_beta_law": RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv",
    "SRC3019_13_2896_beta_components": RESIDUALS / "P8_Y5_R2FR_2896_BETA_ENVELOPE_COMPONENTS.csv",
    "SRC3019_14_2896_newton_gate": RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_NORMALIZED_NEWTON_PRECONDITION_GATE.csv",
    "SRC3019_15_2574_beta_gate": RESIDUALS / "P8_Y5_PPN_VECTOR_2574_BETA_SECOND_ORDER_COUPLING_GATE.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3019_SOURCE_REGISTER.csv",
    "proof": RESIDUALS / "P8_Y5_R2FR_3019_BETA_SQUARE_LAW_PROOF_ATTEMPT.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3019_SECOND_ORDER_FIELD_EQUATION_CONTRACT.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_3019_BETA_RESIDUAL_DECOMPOSITION.csv",
    "queue": RESIDUALS / "P8_Y5_R2FR_3019_FIRST_COEFFICIENT_FILL_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3019_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3019_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3019_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3019_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3019_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_copy": LOCAL_BOUNDS / "beta_square_law_proof_attempt_3019_NONCLAIM.csv",
    "contract_copy": LOCAL_BOUNDS / "second_order_field_equation_contract_3019_NONCLAIM.csv",
    "residual_copy": LOCAL_BOUNDS / "beta_residual_decomposition_3019_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3019_SECOND_ORDER_FIELD_EQUATION_COEFFICIENT_MAP_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3019_00_3018_doc": "3018 selected beta square-law source-normalization gate",
    "SRC3019_01_3018_beta_handoff": "machine-readable beta_eff and square-law handoff",
    "SRC3019_02_3018_next": "3019 target and guardrails",
    "SRC3019_03_2920_doc": "prior beta extraction law and failed parent square-law audit",
    "SRC3019_04_2920_square_audit": "parent square-law audit rows",
    "SRC3019_05_2920_beta_kernel": "beta second-order source-normalization kernel rows",
    "SRC3019_06_2920_newton_queue": "Newton/Gauss/orbital source-mass queue",
    "SRC3019_07_2929_doc": "reentry rule: do not rerun 2920 as a fresh proof",
    "SRC3019_08_2929_residual_vector": "finite beta residual vector",
    "SRC3019_09_2930_doc": "source-owner/Hcore denominator binding obstruction",
    "SRC3019_10_2930_denominator": "denominator binding contract",
    "SRC3019_11_2930_coefficients": "A_source/B_source/source coefficient ledger",
    "SRC3019_12_2893_beta_law": "source-normalized beta extraction law",
    "SRC3019_13_2896_beta_components": "beta envelope components including q_loc diagnostic",
    "SRC3019_14_2896_newton_gate": "source-normalized Newton precondition gate",
    "SRC3019_15_2574_beta_gate": "beta second-order coupling/readout gate",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

proof_attempt = [
    base(
        {
            "proof_id": "BSP3019_0_extraction_law",
            "claim_tested": "source-normalized PPN beta extraction",
            "derivation": "g00=-1+2 A_source W/c^2-2 B_source W^2/c^4 and U=A_source W imply beta_eff=B_source/A_source^2",
            "result": "PROVED_KINEMATIC_FROM_2893_2920",
            "owned_by_mts_parent": True,
            "missing_for_claim": "not_missing_for_extraction_only",
            "claim_effect": "gives the comparison grammar but not beta=1",
        }
    ),
    base(
        {
            "proof_id": "BSP3019_1_square_law_target",
            "claim_tested": "beta_eff=1 iff parent square law holds",
            "derivation": "delta_beta_source=B_source/A_source^2-1, so delta_beta_source=0 iff B_source=A_source^2 with A_source nonzero",
            "result": "TARGET_EQUIVALENCE_PROVED",
            "owned_by_mts_parent": True,
            "missing_for_claim": "MISSING_PARENT_PROOF_THAT_B_SOURCE_EQUALS_A_SOURCE_SQUARED",
            "claim_effect": "defines the exact theorem needed for GR-like beta",
        }
    ),
    base(
        {
            "proof_id": "BSP3019_2_lapse_exponential_route",
            "claim_tested": "single-potential lapse route to square law",
            "derivation": "if N=sqrt(-g00)=exp(-A_source W/c^2)+O(W^3), then g00=-exp(-2A_source W/c^2)=-1+2A_source W/c^2-2A_source^2 W^2/c^4+O(W^3)",
            "result": "CONDITIONAL_PROOF_ROUTE_FOUND",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_PARENT_LAPSE_EXPONENTIAL_OR_EQUIVALENT_SECOND_ORDER_NORMAL_FORM",
            "claim_effect": "would prove B_source=A_source^2 if the parent action derives this lapse normal form",
        }
    ),
    base(
        {
            "proof_id": "BSP3019_3_lapse_quadratic_route",
            "claim_tested": "quadratic lapse coefficient condition",
            "derivation": "if N=1-A_source W/c^2+(A_source^2/2)W^2/c^4+O(W^3), then g00=-N^2=-1+2A_source W/c^2-2A_source^2 W^2/c^4+O(W^3)",
            "result": "EQUIVALENT_LOCAL_NORMAL_FORM_CONDITION",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_PARENT_SECOND_ORDER_LAPSE_COEFFICIENT",
            "claim_effect": "turns beta square-law into a concrete O(W^2) coefficient target",
        }
    ),
    base(
        {
            "proof_id": "BSP3019_4_extra_sector_decomposition",
            "claim_tested": "all beta deviations are explicit parent residuals",
            "derivation": "write B_source=A_source^2+Delta_B_parent, then beta_eff-1=Delta_B_parent/A_source^2; Delta_B_parent splits into operator, source-current/coupling, boundary/domain, readout and denominator terms",
            "result": "RESIDUAL_DECOMPOSITION_DERIVED",
            "owned_by_mts_parent": True,
            "missing_for_claim": "MISSING_ZERO_OR_BOUNDS_FOR_DELTA_B_COMPONENTS",
            "claim_effect": "prevents hidden calibration/cancellation; beta remains nonclaim until components close",
        }
    ),
    base(
        {
            "proof_id": "BSP3019_5_EH_control_lane",
            "claim_tested": "GR/EH exterior implies beta=1",
            "derivation": "EH plus Hilbert source, no extra modes, boundary silence and fixed readout reproduces the Schwarzschild/PPN beta=1 control lane",
            "result": "EXACT_CONDITIONAL_CONTROL_NOT_MTS_PROOF",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_PARENT_EH_OWNER; MISSING_SOURCE_CLOSURE; MISSING_NO_EXTRA_MODES; MISSING_READOUT_FIXED_BEFORE_COMPARISON",
            "claim_effect": "useful comparator only; cannot be imported as an MTS derivation",
        }
    ),
    base(
        {
            "proof_id": "BSP3019_6_verdict",
            "claim_tested": "current MTS proves beta_eff=1",
            "derivation": "the square-law route is mathematically clear, but the parent action has not yet supplied the second-order lapse/field-equation coefficient map",
            "result": "BETA_SQUARE_LAW_NOT_PARENT_SIGNED",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_SECOND_ORDER_PARENT_FIELD_EQUATION_COEFFICIENT_MAP",
            "claim_effect": "no beta, PPN, Newton or local-GR claim; move to coefficient-map target",
        }
    ),
]

field_contract = [
    base(
        {
            "contract_id": "FEC3019_0_source_potential",
            "object": "W",
            "required_statement": "W is defined before measured-GM fitting by a same-frame Hilbert/source density: nabla^2 W=4*pi*G_ref*rho_H",
            "current_status": "DENOMINATOR_CONTRACT_PRESENT_UNSIGNED",
            "source_link": "2930 DBC2930_0/DBC2930_1",
            "failure_if_missing": "A_source and B_source have no common denominator",
            "next_action": "derive Hcore/source density and positive M_H_ref in the same frame",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_1_A_source",
            "object": "A_source",
            "required_statement": "linear coefficient in g00=-1+2 A_source W/c^2+O(W^2)",
            "current_status": "MISSING_PARENT_LINEAR_COEFFICIENT_MAP",
            "source_link": "2930 SCL2930_0",
            "failure_if_missing": "Newton denominator can be a fitted calibration rather than a derived source map",
            "next_action": "extract A_source from parent first-order Hamiltonian/field equation",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_2_B_source",
            "object": "B_source",
            "required_statement": "quadratic coefficient in g00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(W^3)",
            "current_status": "MISSING_PARENT_SECOND_ORDER_COEFFICIENT_MAP",
            "source_link": "2930 SCL2930_1",
            "failure_if_missing": "beta cannot be scored",
            "next_action": "extract B_source from parent second-order field equation",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_3_self_energy_square",
            "object": "Delta_B_square",
            "required_statement": "parent self-coupling or lapse normal form gives B_source-A_source^2=0",
            "current_status": "CONDITIONAL_ROUTE_FOUND_UNSIGNED",
            "source_link": "3019 BSP3019_2/BSP3019_3",
            "failure_if_missing": "delta_beta_source remains active",
            "next_action": "prove exponential/quadratic lapse normal form from the parent action",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_4_operator_nohair",
            "object": "Delta_B_operator",
            "required_statement": "R11, R2/fR, scalar/vector/tensor and auxiliary curvature operators have zero beta projection or finite sourced coefficients",
            "current_status": "MISSING_R11_COMPONENT_VALUES_OR_EH_NOHAIR",
            "source_link": "2896 ENV2896_2; 2920 B2K2920_1",
            "failure_if_missing": "operator hair can shift beta even if the source square law holds",
            "next_action": "derive no-hair or fill finite operator coefficient rows",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_5_source_current_coupling",
            "object": "Delta_B_source_current",
            "required_statement": "kappa_MTS, ell_J, source-prefactor and non-Hilbert current do not re-enter at O(U^2)",
            "current_status": "MISSING_SOURCE_COUPLING_SECOND_ORDER_CLOSURE",
            "source_link": "2574 BETA2574_2; 2930 DBC2930_6/DBC2930_7",
            "failure_if_missing": "coupling drift can make beta a source-normalization artefact",
            "next_action": "prove constant local coupling/source-current owner or keep finite residual",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_6_boundary_domain",
            "object": "Delta_B_boundary_domain",
            "required_statement": "boundary/domain/projector quadratic stress has zero beta projection or finite coefficient map",
            "current_status": "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP",
            "source_link": "2896 ENV2896_4; 2920 B2K2920_3",
            "failure_if_missing": "boundary terms can shift beta and also endanger alpha3/xi",
            "next_action": "derive boundary/domain silence at O(U^2)",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_7_readout",
            "object": "Delta_B_readout",
            "required_statement": "observed coframe/readout and isotropic PPN gauge are fixed before comparison through O(U^2)",
            "current_status": "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "source_link": "2574 BETA2574_3; 2896 ENV2896_5",
            "failure_if_missing": "readout choice can create or hide beta residual",
            "next_action": "derive second-order readout/gauge transfer",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_8_orbital_denominator",
            "object": "epsilon_SN",
            "required_statement": "mu_obs=G_eff M_H in the same source frame, with no orbital-GM circular denominator",
            "current_status": "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD",
            "source_link": "2896 ENV2896_6; 2920 scorecard queue",
            "failure_if_missing": "measured-GM calibration can hide source mismatch",
            "next_action": "fill Gauss/orbital/source-current scorecard",
        }
    ),
    base(
        {
            "contract_id": "FEC3019_9_verdict",
            "object": "beta square-law contract",
            "required_statement": "all FEC3019_0 through FEC3019_8 close together",
            "current_status": "CONTRACT_READY_PARENT_VALUES_MISSING",
            "source_link": "3019 aggregate",
            "failure_if_missing": "no beta/local-GR pass",
            "next_action": "3020 should map the second-order parent field equation coefficients",
        }
    ),
]

residuals = [
    base(
        {
            "residual_id": "BRD3019_0_square_gap",
            "symbol": "Delta_B_parent",
            "definition": "B_source-A_source^2",
            "formula_or_bound": "beta_minus_1=Delta_B_parent/A_source^2",
            "current_status": "ACTIVE_NONCLAIM",
            "component_value": "MISSING_SECOND_ORDER_COEFFICIENT_MAP",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "main beta square-law gap",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_1_operator",
            "symbol": "Delta_B_operator",
            "definition": "R11/non-EH/auxiliary second-order operator contribution",
            "formula_or_bound": "abs(Delta_B_operator/A_source^2)",
            "current_status": "MISSING_R11_COMPONENT_VALUES_OR_EH_NOHAIR",
            "component_value": "MISSING",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "blocks beta even if source square law is later derived",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_2_source_current",
            "symbol": "Delta_B_source_current",
            "definition": "kappa_MTS, ell_J, source-prefactor or non-Hilbert current leakage into U^2",
            "formula_or_bound": "abs(Delta_B_source_current/A_source^2)",
            "current_status": "MISSING_SOURCE_CURRENT_COUPLING_ZERO",
            "component_value": "MISSING",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "the coupling wound remains live",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_3_boundary_domain",
            "symbol": "Delta_B_boundary_domain",
            "definition": "boundary/domain/projector quadratic stress beta projection",
            "formula_or_bound": "abs(Delta_B_boundary_domain/A_source^2)",
            "current_status": "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP",
            "component_value": "MISSING",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "also links to alpha3/xi safety",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_4_readout",
            "symbol": "Delta_B_readout",
            "definition": "second-order source metric to observed PPN readout mismatch",
            "formula_or_bound": "abs(Delta_B_readout/A_source^2)",
            "current_status": "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "component_value": "MISSING",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "prevents coordinate/readout-safe beta claim",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_5_epsilon_SN",
            "symbol": "epsilon_SN",
            "definition": "(mu_obs-G_eff M_H)/(G_eff M_H)",
            "formula_or_bound": "abs(epsilon_SN) must be bounded in the same source frame",
            "current_status": "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD",
            "component_value": "MISSING",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "prevents measured-GM denominator from hiding source mismatch",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_6_q_loc_diagnostic",
            "symbol": "delta_beta_q_loc",
            "definition": "physical U2 projection of P_loc(nabla Gamma_eff-div Khat)",
            "formula_or_bound": "7.432631961576971e-06 diagnostic from 2896, valid only if same normalization is proved",
            "current_status": "PROVISIONAL_DIAGNOSTIC_NOT_CLAIMABLE",
            "component_value": "7.432631961576971e-06_DIAGNOSTIC_ONLY",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "interesting but cannot rescue beta without normalization proof",
        }
    ),
    base(
        {
            "residual_id": "BRD3019_7_total_abs",
            "symbol": "Delta_beta_total_abs",
            "definition": "no-cancellation absolute beta envelope",
            "formula_or_bound": "sum_abs(Delta_B_parent/A_source^2, operator, source_current, boundary_domain, readout, epsilon_SN, allowed q_loc)",
            "current_status": "TOTAL_NOT_SCORE_READY",
            "component_value": "MISSING_MULTIPLE_COMPONENTS",
            "beta_bound_abs": BETA_BOUND_ABS,
            "claim_effect": "beta remains blocked until every active head is zero or finite-bounded",
        }
    ),
]

first_fill_queue = [
    base(
        {
            "queue_id": "FCQ3019_0_lapse_normal_form",
            "target": "second-order lapse normal form",
            "wanted_row": "N=exp(-A_source W/c^2)+O(W^3) or N=1-A_source W/c^2+(A_source^2/2)W^2/c^4+O(W^3)",
            "why_first": "this would prove B_source=A_source^2 directly",
            "required_source": "parent action variation / Hamiltonian constraint through O(W^2)",
            "status": "SELECTED_BEST_DERIVATION_ROUTE",
        }
    ),
    base(
        {
            "queue_id": "FCQ3019_1_A_source",
            "target": "A_source coefficient",
            "wanted_row": "numeric/symbolic linear coefficient from same source-normalized branch",
            "why_first": "needed as denominator for beta_eff and Newton limit",
            "required_source": "parent first-order field equation",
            "status": "MISSING",
        }
    ),
    base(
        {
            "queue_id": "FCQ3019_2_B_source",
            "target": "B_source coefficient",
            "wanted_row": "numeric/symbolic quadratic coefficient from same source-normalized branch",
            "why_first": "direct beta numerator",
            "required_source": "parent second-order field equation",
            "status": "MISSING",
        }
    ),
    base(
        {
            "queue_id": "FCQ3019_3_Delta_B_operator",
            "target": "operator nohair or coefficient rows",
            "wanted_row": "zero theorem or finite beta projection for R11/R2/fR/auxiliary operator sector",
            "why_first": "extra operator hair breaks GR beta even if A/B square",
            "required_source": "parent operator sector variation",
            "status": "MISSING",
        }
    ),
    base(
        {
            "queue_id": "FCQ3019_4_readout_OU2",
            "target": "second-order readout gauge map",
            "wanted_row": "fixed-before-readout transfer through O(U^2)",
            "why_first": "prevents beta from being a coordinate/readout artifact",
            "required_source": "observed coframe and PPN gauge transform",
            "status": "MISSING",
        }
    ),
    base(
        {
            "queue_id": "FCQ3019_5_source_current_coupling",
            "target": "constant coupling/source-current owner",
            "wanted_row": "Dln(kappa_MTS)=0, Dln(ell_J)=0, no source-prefactor/non-Hilbert U2 leakage",
            "why_first": "the coupling issue is the root wound feeding beta and alpha3",
            "required_source": "parent source-current/coupling theorem",
            "status": "MISSING",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3019_0_sources",
            "gate": "every cited local source path exists",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "current-state source audit",
        }
    ),
    base(
        {
            "gate_id": "GATE3019_1_extraction_law",
            "gate": "beta_eff extraction law is proved",
            "result": True,
            "notes": "beta_eff=B_source/A_source^2 is kinematic grammar",
        }
    ),
    base(
        {
            "gate_id": "GATE3019_2_conditional_square_route",
            "gate": "a sufficient square-law route is identified",
            "result": True,
            "notes": "single-potential exponential/quadratic lapse route would force B_source=A_source^2",
        }
    ),
    base(
        {
            "gate_id": "GATE3019_3_parent_square_law",
            "gate": "MTS parent signs B_source=A_source^2",
            "result": False,
            "notes": "parent second-order normal form is not yet sourced",
        }
    ),
    base(
        {
            "gate_id": "GATE3019_4_beta_score",
            "gate": "MTS beta can be scored against comparator",
            "result": False,
            "notes": "no valid A_source/B_source/residual vector values",
        }
    ),
    base(
        {
            "gate_id": "GATE3019_5_local_GR_claim",
            "gate": "local GR / Newtonian limit is claimable",
            "result": False,
            "notes": "beta square law, gamma coefficients, alpha3 theorem, source-current and readout gates remain incomplete",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3019_0_real_derivation_gain",
            "decision": "a concrete sufficient beta square-law mechanism was found",
            "rationale": "single-potential exponential lapse or equivalent quadratic lapse coefficient gives B_source=A_source^2 exactly through O(W^2)",
            "consequence": "the next task can hunt for this normal form in the parent action rather than debating beta abstractly",
        }
    ),
    base(
        {
            "decision_id": "DEC3019_1_no_beta_claim",
            "decision": "do not claim beta=1",
            "rationale": "the sufficient mechanism is not parent-signed and extra operator/source/readout/boundary components remain live",
            "consequence": "all rows remain nonclaim and score_ready=false",
        }
    ),
    base(
        {
            "decision_id": "DEC3019_2_next_target",
            "decision": "select the second-order parent field-equation coefficient map",
            "rationale": "A_source, B_source and the lapse normal form are the minimal data needed to prove or reject the beta square law",
            "consequence": "3020 should attack the parent variation/Hamiltonian constraint through O(W^2)",
        }
    ),
    base(
        {
            "decision_id": "DEC3019_3_overall_status",
            "decision": "GR reduction path gets sharper, not solved",
            "rationale": "gamma is a ratio gate, beta is now a second-order normal-form gate, alpha3 is a current/no-flux gate",
            "consequence": "MTS is moving toward derivability with named locks rather than handwaving local GR",
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3019_0_3020",
            "target_doc": "3020-Y5-R2FR-second-order-parent-field-equation-coefficient-map-or-beta-square-law-rejection-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_second_order_parent_field_equation_coefficient_map_or_beta_square_law_rejection_under_AX1090_3020.py",
            "mission": "derive the parent second-order weak-field coefficient map for A_source and B_source, especially the lapse normal form that would force B_source=A_source^2; if absent, reject the beta square-law route and keep a finite residual ledger",
            "success_condition": "either parent variation signs N=exp(-A_source W/c^2)+O(W^3) or an equivalent B_source=A_source^2 theorem, or the exact missing parent operator/source/readout terms are retained as nonclaim beta residuals",
            "forbidden": "no EH import as MTS proof; no measured-GM absorption shortcut; no gamma-only pass; no cross-component cancellation; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["proof"], proof_attempt)
write_csv(OUTPUTS["contract"], field_contract)
write_csv(OUTPUTS["residuals"], residuals)
write_csv(OUTPUTS["queue"], first_fill_queue)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("proof_copy", "proof"),
    ("contract_copy", "contract"),
    ("residual_copy", "residuals"),
    ("queue_copy", "queue"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3019_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = source_register + proof_attempt + field_contract + residuals + first_fill_queue + promotion_gates + decision + next_target

validation_rows = [
    {
        "validation_id": "VAL3019_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3019_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3019_02_extraction_and_square_equivalence",
        "passed": any(row["proof_id"] == "BSP3019_0_extraction_law" and row["result"].startswith("PROVED") for row in proof_attempt)
        and any(row["proof_id"] == "BSP3019_1_square_law_target" and row["result"] == "TARGET_EQUIVALENCE_PROVED" for row in proof_attempt),
        "requirement": "beta extraction law and square-law equivalence are recorded",
        "evidence": OUTPUTS["proof"].name,
    },
    {
        "validation_id": "VAL3019_03_conditional_lapse_route",
        "passed": any(row["proof_id"] == "BSP3019_2_lapse_exponential_route" and row["result"] == "CONDITIONAL_PROOF_ROUTE_FOUND" for row in proof_attempt)
        and any(row["proof_id"] == "BSP3019_3_lapse_quadratic_route" for row in proof_attempt),
        "requirement": "a concrete sufficient route to B_source=A_source^2 is derived conditionally",
        "evidence": OUTPUTS["proof"].name,
    },
    {
        "validation_id": "VAL3019_04_parent_square_not_claimed",
        "passed": any(row["proof_id"] == "BSP3019_6_verdict" and row["result"] == "BETA_SQUARE_LAW_NOT_PARENT_SIGNED" for row in proof_attempt)
        and any(row["gate_id"] == "GATE3019_3_parent_square_law" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "conditional route is not promoted to MTS beta proof",
        "evidence": f"{OUTPUTS['proof'].name}; {OUTPUTS['gates'].name}",
    },
    {
        "validation_id": "VAL3019_05_field_contract_complete",
        "passed": {"A_source", "B_source", "Delta_B_operator", "Delta_B_readout", "epsilon_SN"}.issubset({row["object"] for row in field_contract}),
        "requirement": "second-order field-equation contract includes source coefficients, operator, readout and denominator gates",
        "evidence": OUTPUTS["contract"].name,
    },
    {
        "validation_id": "VAL3019_06_residual_decomposition_present",
        "passed": any(row["symbol"] == "Delta_B_parent" for row in residuals)
        and any(row["symbol"] == "Delta_beta_total_abs" for row in residuals),
        "requirement": "beta residual decomposition includes square gap and no-cancellation total",
        "evidence": OUTPUTS["residuals"].name,
    },
    {
        "validation_id": "VAL3019_07_first_fill_queue_selected",
        "passed": any(row["queue_id"] == "FCQ3019_0_lapse_normal_form" and row["status"] == "SELECTED_BEST_DERIVATION_ROUTE" for row in first_fill_queue),
        "requirement": "next coefficient-fill route is selected",
        "evidence": OUTPUTS["queue"].name,
    },
    {
        "validation_id": "VAL3019_08_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and all(not boolish(row.get("valid_for_claim")) for row in claim_rows),
        "requirement": "all rows remain nonclaim/private-control rows",
        "evidence": "all 3019 generated ledgers",
    },
    {
        "validation_id": "VAL3019_09_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3019 generated ledgers",
    },
    {
        "validation_id": "VAL3019_10_branch_copies_exist",
        "passed": all(boolish(row["exists"]) for row in branch_rows),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": OUTPUTS["branches"].name,
    },
    {
        "validation_id": "VAL3019_11_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3019_12_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3019_13_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3020-Y5-R2FR-second-order-parent-field-equation-coefficient-map"),
        "requirement": "next target selects parent second-order coefficient map",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3019_99_overall",
        "passed": overall_pass,
        "requirement": "all 3019 validation checks pass",
        "evidence": "aggregate of VAL3019_00 through VAL3019_13",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3019 - Beta Square-Law Source-Normalization Gate under AX1090

Status: `Y5_R2FR_3019_conditional_beta_square_law_route_found_parent_not_signed_3020_next`

## Verdict

3019 makes a real derivation move, but not a claim.

The extraction law is owned:

`g00=-1+2 A_source W/c^2-2 B_source W^2/c^4`, with `U=A_source W`, gives

`beta_eff=B_source/A_source^2`.

Therefore `beta_eff=1` is equivalent to the parent square law:

`B_source=A_source^2`.

The useful new route is the lapse normal-form route. If the local observed lapse obeys

`N=sqrt(-g00)=exp(-A_source W/c^2)+O(W^3)`,

or equivalently

`N=1-A_source W/c^2+(A_source^2/2)W^2/c^4+O(W^3)`,

then

`g00=-N^2=-1+2 A_source W/c^2-2 A_source^2 W^2/c^4+O(W^3)`,

so `B_source=A_source^2` follows exactly through PPN beta order.

That is the cleanest local-GR beta mechanism found here. But current MTS has not yet parent-signed that lapse normal form or the equivalent second-order field-equation coefficient map. Extra operator, source-current/coupling, boundary/domain, denominator, and readout terms remain live.

So 3019 does not claim beta, PPN, Newton, or local GR. It turns the problem into the next exact target: derive the second-order parent field-equation coefficient map, or reject the beta square-law route and keep the residual vector.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Beta Square-Law Proof Attempt

{md_table(proof_attempt, ["proof_id", "claim_tested", "derivation", "result", "owned_by_mts_parent", "missing_for_claim"])}

## Second-Order Field-Equation Contract

{md_table(field_contract, ["contract_id", "object", "required_statement", "current_status", "failure_if_missing", "next_action"])}

## Beta Residual Decomposition

{md_table(residuals, ["residual_id", "symbol", "definition", "formula_or_bound", "current_status", "component_value", "claim_effect"])}

## First Coefficient Fill Queue

{md_table(first_fill_queue, ["queue_id", "target", "wanted_row", "why_first", "required_source", "status"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["proof"]}`
- `{OUTPUTS["contract"]}`
- `{OUTPUTS["residuals"]}`
- `{OUTPUTS["queue"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["proof_copy"]}`
- `{BRANCH_OUTPUTS["contract_copy"]}`
- `{BRANCH_OUTPUTS["residual_copy"]}`
- `{BRANCH_OUTPUTS["queue_copy"]}`

## Hard Guardrails Still Active

- No beta pass without parent-signed `B_source=A_source^2` or a finite source-backed residual vector below the comparator.
- No EH/Schwarzschild import as MTS proof.
- No measured-`GM` absorption shortcut.
- No gamma-only local-GR or PPN pass.
- No cross-component cancellation.
- No `alpha3` pass without source-current/no-flux theorem-zero or an ultratight bound.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
