from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from srng_naturality_or_projective_kernel_values_gate import (  # noqa: E402
    evaluate_kernel_value_rows,
    evaluate_naturality_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4416"
CLAIM_ID = "L-257"
MARKER = "PPC4161_TRANSITION_SOURCE_READOUT_SRNG_NATURALITY_OR_PROJECTIVE_KERNEL_VALUES_4416"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_READOUT_SRNG_NATURALITY_OR_PROJECTIVE_KERNEL_VALUES_4416"
DECISION = "SRNG_CHAIN_RULE_PRIVATE_BRANCH_SHARPENED_PROJECTOR_COMMUTATOR_AND_PROJECTIVE_KERNEL_VALUES_OPEN_NONCLAIM"
NEXT_TARGET = "4417-Y5-R2FR-transition-readout-projector-commutator-zero-or-Kprojective-values.md"

FORMAL_PATH = FORMAL / "432-PPC4161-transition-source-readout-SRNG-naturality-or-projective-kernel-values.md"
DOC_PATH = POST / "4416-Y5-R2FR-transition-source-readout-SRNG-naturality-or-projective-kernel-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4416_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4416_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4416_DERIVATION_ROWS.csv"
NATURALITY_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4416_SRNG_NATURALITY_INPUT.csv"
NATURALITY_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4416_SRNG_NATURALITY_OUTPUT.csv"
KERNEL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4416_PROJECTIVE_KERNEL_VALUE_INPUT.csv"
KERNEL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4416_PROJECTIVE_KERNEL_VALUE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4416_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4416_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4416_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4416_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "srng_naturality_or_projective_kernel_values_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4416_transition_source_readout_SRNG_naturality_or_projective_kernel_values.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4415 = SOURCE_DIR / "P8_Y5_R2FR_4415_NEXT_TARGET.csv"
FORMAL_431 = FORMAL / "431-PPC4161-transition-owned-coframe-LC-selector-or-source-readout-kernel.md"
POST_2336 = POST / "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md"
POST_2542 = POST / "2542-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md"
POST_2122 = POST / "2122-Y5-R2FR-CMSM-live-drop-validator-or-source-readout-owner-lemma.md"
POST_2121 = POST / "2121-Y5-R2FR-source-readout-theorem-closure-or-CMSM-manual-export-workflow.md"
POST_2120 = POST / "2120-Y5-R2FR-MICROSCOPE-numeric-source-readout-kernel-acquisition.md"
POST_2118 = POST / "2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md"
POST_2335 = POST / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md"
POST_1031 = POST / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md"
POST_2099 = POST / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4416_00_4415_next": (
        NEXT_4415,
        "4416-Y5-R2FR-transition-source-readout-SRNG-naturality-or-projective-kernel-values.md",
        "4415 handoff to SRNG naturality or projective kernel values.",
    ),
    "SRC4416_01_4415_formal": (
        FORMAL_431,
        "SRNG/source-readout naturality",
        "LC selector product gate names SRNG as the live source/readout factor.",
    ),
    "SRC4416_02_2336_downstream": (
        POST_2336,
        "readouts are downstream natural functors",
        "first downstream observation functor naturality audit.",
    ),
    "SRC4416_03_2542_private_public": (
        POST_2542,
        "The downstream observation route is now cleanly framed",
        "private SRNG branch is usable but public proof debt remains.",
    ),
    "SRC4416_04_2122_commutator": (
        POST_2122,
        "delta(Pi J)=Pi delta J",
        "source/readout owner lemma exposes the projector commutator obstruction.",
    ),
    "SRC4416_05_2121_live_arrays": (
        POST_2121,
        "No live official CMSM readout arrays are present yet",
        "official numeric fallback remains unavailable.",
    ),
    "SRC4416_06_2120_numeric_gap": (
        POST_2120,
        "no verified CMSM numeric arrays",
        "MICROSCOPE/CMSM acquisition has provenance but no runnable arrays.",
    ),
    "SRC4416_07_2118_projective_kernel": (
        POST_2118,
        "KSR2118_6_projective_trace_kernel",
        "projective trace source/readout kernel fallback.",
    ),
    "SRC4416_08_2335_SRNG_contract": (
        POST_2335,
        "SRNG source-readout no-Gamma contract is now explicit",
        "SRNG contract and limits before derivation.",
    ),
    "SRC4416_09_1031_terminal_limit": (
        POST_1031,
        "ordinary matter/readout functors are also parent-restricted",
        "terminal public metric alone does not sign the matter/readout interface.",
    ),
    "SRC4416_10_2099_projective_map": (
        POST_2099,
        "DGM2099_6_projective",
        "projective component map to WEP/source/clock/orbital residuals.",
    ),
    "SRC4416_11_gate": (
        GATE_PATH,
        "def evaluate_naturality_row",
        "new SRNG naturality and projective kernel-value gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    body = text(path)
    if not body or needle not in body:
        return False, -1
    return True, body[: body.index(needle)].count("\n") + 1


def bool_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "SRNG4416_0_chain_rule_identity",
            "claim": "Downstream readout naturality gives vertical silence by the chain rule.",
            "derivation": "For a vertical variation v in ker(Dq), a downstream readout O_i=Obar_i(q(Phi),e_obs(q(Phi)),theta) has delta_v O_i = DObar_i[Dq(v),De_obs(Dq(v))]=0. This proves the readout-map half only when q is fixed before readout and e_obs descends from q.",
            "consequence": "This is a real theorem shape, not a vibe: the observed readout functional cannot see vertical Gamma_ind motion if its whole domain is q/e_obs.",
            "status": "CHAIN_RULE_DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SRNG4416_1_source_current_term",
            "claim": "The Pi delta J term closes if the source current itself descends through q/e_obs.",
            "derivation": "For source/readout object Pi_i J_i, the chain rule gives delta_v J_i=0 if J_i=Jbar_i(q,e_obs,theta) is selected after the action solve on the same tau/worldtube support, with apparatus backreaction counted as matter or residual.",
            "consequence": "The current branch gets a private SRNG theorem for Pi_i delta J_i, but only under same-support downstream source ownership.",
            "status": "PRIVATE_SOURCE_TERM_READY_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SRNG4416_2_projector_commutator_obstruction",
            "claim": "The public source/readout theorem is blocked by the projector/support commutator.",
            "derivation": "delta_v(Pi_i J_i)=Pi_i delta_v J_i+(delta_v Pi_i)J_i. The first term can be zeroed by SRNG; the second requires Pi_i, masks, weights, boundaries and finite source supports to be q/e_obs-natural.",
            "consequence": "This is the exact next proof target: prove delta_v Pi_i=0 or keep a finite commutator/projective kernel.",
            "status": "PUBLIC_OBSTRUCTION_EXACT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SRNG4416_3_projective_trace_separation",
            "claim": "SRNG does not automatically erase projective trace coupling.",
            "derivation": "Downstream readout naturality forbids an independent Gamma_ind readout slot, but projective trace remains live unless every relevant source/readout sector is trace-gauge invariant or the trace mode is fixed before coupling.",
            "consequence": "Projective trace stays as a separate fallback row, not hidden inside SRNG language.",
            "status": "PROJECTIVE_LIMIT_EXPLICIT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SRNG4416_4_kernel_value_fallback",
            "claim": "If the commutator/projective clauses are unsigned, the fallback is numeric kernel values.",
            "derivation": "A runnable fallback needs Delta_projective^arena=P_projective^arena K_trace J_trace on the same support, with official source arrays, parent coefficient provenance, units, comparator bounds and a no-cancellation guard.",
            "consequence": "No R10/WEP/PPN/clock/orbital/local-GR claim is possible from placeholders.",
            "status": "KERNEL_VALUE_SCHEMA_RETAINED",
            "valid_for_claim": False,
        },
    ]


def naturality_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NAT4416_0_current_private_chain_rule_branch",
            "branch": "current_downstream_q_eobs_private_branch",
            "q_fixed_before_readout": True,
            "eobs_descends_from_q": True,
            "action_varied_before_readout": True,
            "readouts_maps_on_solutions": True,
            "apparatus_backreaction_in_matter_or_residual": True,
            "source_current_descends": True,
            "projector_support_descends": False,
            "no_gamma_ind_readout_slot": True,
            "no_projective_trace_readout_slot": False,
            "same_tau_worldtube_support": True,
            "boundary_improvement_separate": True,
            "parent_observation_policy_signed": False,
            "source_path": str(POST_2122),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "This is the strongest honest current result: Pi delta J is chain-rule silent, but delta Pi and projective trace policy are not signed.",
        },
        {
            "row_id": "NAT4416_1_future_public_contract",
            "branch": "future_parent_signed_SRNG_contract",
            "q_fixed_before_readout": True,
            "eobs_descends_from_q": True,
            "action_varied_before_readout": True,
            "readouts_maps_on_solutions": True,
            "apparatus_backreaction_in_matter_or_residual": True,
            "source_current_descends": True,
            "projector_support_descends": True,
            "no_gamma_ind_readout_slot": True,
            "no_projective_trace_readout_slot": True,
            "same_tau_worldtube_support": True,
            "boundary_improvement_separate": True,
            "parent_observation_policy_signed": True,
            "source_path": str(POST_2542),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "A complete contract row: it would close SRNG publicly if parent-owned, but is nonclaim here.",
        },
        {
            "row_id": "NAT4416_2_live_projective_or_readout_counterbranch",
            "branch": "live_counterbranch_projective_trace_or_non_natural_readout",
            "q_fixed_before_readout": False,
            "eobs_descends_from_q": False,
            "action_varied_before_readout": False,
            "readouts_maps_on_solutions": False,
            "apparatus_backreaction_in_matter_or_residual": False,
            "source_current_descends": False,
            "projector_support_descends": False,
            "no_gamma_ind_readout_slot": False,
            "no_projective_trace_readout_slot": False,
            "same_tau_worldtube_support": False,
            "boundary_improvement_separate": True,
            "parent_observation_policy_signed": False,
            "source_path": str(POST_2118),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Counterbranch retained so the proof cannot pretend non-natural source/readout projectors vanished.",
        },
    ]


def kernel_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "kernel_id": "KPV4416_0_projective_trace_common_kernel",
            "residual_component": "projective_trace_current",
            "arena": "WEP_CLOCK_SOURCE_ORBITAL_COMMON",
            "observable": "eta_AB;delta_nu_over_nu;source_charge_residual;orbital_GM_tail",
            "K_trace": "MISSING_K_TRACE_VALUE",
            "K_trace_units": "projective_trace_current_per_source_readout_unit",
            "P_projective": "MISSING_P_PROJECTIVE_ARENA",
            "P_projective_units": "observable_per_projective_trace_current",
            "J_trace_norm": "MISSING_SOURCE_TRACE_NORM",
            "support_certificate": "same_q_eobs_tau_worldtube_support_required",
            "comparator_bound": "MISSING_WEP_CLOCK_SOURCE_ORBITAL_BOUND",
            "source_path": str(POST_2118),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Projective trace fallback retained; no parent coefficient, projection matrix, official arrays or comparator bound.",
        },
        {
            "kernel_id": "KPV4416_1_projector_commutator_kernel",
            "residual_component": "readout_projector_commutator",
            "arena": "FINITE_SOURCE_MASK_BOUNDARY_RESPONSE",
            "observable": "delta(Pi J)_source;WEP_mask_tail;clock_window_tail;orbit_boundary_tail",
            "K_trace": "MISSING_K_COMMUTATOR_VALUE",
            "K_trace_units": "readout_projection_variation_per_source_unit",
            "P_projective": "MISSING_P_COMMUTATOR_ARENA",
            "P_projective_units": "observable_per_commutator_residual",
            "J_trace_norm": "MISSING_FINITE_SOURCE_J_NORM",
            "support_certificate": "projector_mask_weight_boundary_q_eobs_naturality_required",
            "comparator_bound": "MISSING_FINITE_SOURCE_READOUT_BOUND",
            "source_path": str(POST_2122),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Exact commutator obstruction row; either prove delta Pi=0 or source finite kernel values.",
        },
        {
            "kernel_id": "KPV4416_2_CMSM_official_numeric_fallback",
            "residual_component": "official_WEP_source_readout_arrays",
            "arena": "MICROSCOPE_CMSM",
            "observable": "eta_AB_kernel_projection",
            "K_trace": "MISSING_CMSM_KERNEL_COEFFICIENT",
            "K_trace_units": "eta_per_projective_or_commutator_unit",
            "P_projective": "MISSING_OFFICIAL_DESIGN_MATRIX",
            "P_projective_units": "dimensionless_design_projection",
            "J_trace_norm": "MISSING_OFFICIAL_SOURCE_NORM",
            "support_certificate": "official_CMSM_arrays_and_source_worldtube_normalization_required",
            "comparator_bound": "MISSING_MICROSCOPE_COMPARATOR_BOUND",
            "source_path": str(POST_2120),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Acquisition row only: provenance/templates/surrogates are not official numeric evidence.",
        },
    ]


def claim_gate_rows(
    naturality_output: List[Mapping[str, str]],
    kernel_output: List[Mapping[str, str]],
) -> List[Dict[str, object]]:
    nat = {row["row_id"]: row for row in naturality_output}
    kernels = {row["kernel_id"]: row for row in kernel_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in naturality_output + kernel_output)
    return [
        {
            "gate_id": "CG4416_0_chain_rule_identity",
            "claim": "downstream readout chain-rule identity is derived conditionally",
            "passed": bool_true(nat["NAT4416_0_current_private_chain_rule_branch"].get("chain_rule_ready")),
            "valid_for_claim": False,
            "detail": "For v in ker(Dq), downstream O_i(q,e_obs) has delta_v O_i=0.",
        },
        {
            "gate_id": "CG4416_1_private_SRNG_branch",
            "claim": "private SRNG source-current term is ready",
            "passed": bool_true(nat["NAT4416_0_current_private_chain_rule_branch"].get("private_srng_ready")),
            "valid_for_claim": False,
            "detail": "Pi delta J is silent under same-worldtube q/e_obs source descent.",
        },
        {
            "gate_id": "CG4416_2_projector_commutator_zero",
            "claim": "delta_v Pi_i=0 for finite projectors/supports",
            "passed": False,
            "valid_for_claim": False,
            "detail": "Not signed; exact obstruction is (delta_v Pi_i)J_i.",
        },
        {
            "gate_id": "CG4416_3_projective_kernel_values",
            "claim": "projective/source-readout kernel fallback has values",
            "passed": kernels["KPV4416_0_projective_trace_common_kernel"].get("current_status")
            == "PROJECTIVE_KERNEL_VALUES_READY",
            "valid_for_claim": False,
            "detail": "K_trace, P_projective, official source norm and comparator bounds are missing.",
        },
        {
            "gate_id": "CG4416_4_no_claim_outputs",
            "claim": "no local-GR/Newton/PPN/R10/clock/orbital claim fires",
            "passed": no_claims,
            "valid_for_claim": False,
            "detail": "All rows remain nonclaim until commutator/projective clauses close or real kernel values exist.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4416_0",
            "decision": DECISION,
            "summary": "4416 turns SRNG from a loose slogan into an exact split. The downstream q/e_obs chain rule closes the private Pi delta J term. Public source/readout silence is still blocked by the projector/support commutator (delta Pi)J and by projective-trace source/readout coupling. Numeric fallback rows remain blocked because parent coefficients, official readout/source arrays and comparator projections are missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "best_result": "SRNG_chain_rule_private_branch_ready_for_Pi_delta_J",
            "still_missing": "delta_v_Pi_zero; projector_support_weight_boundary_q_eobs_naturality; projective_trace_readout_policy; K_trace; P_projective; official_CMSM_arrays; comparator_bounds",
            "valid_for_claim": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4416_0",
            "target": NEXT_TARGET,
            "objective": "Prove delta_v Pi_i=0 for source/readout projectors, supports, weights, boundaries and finite response operators from q/e_obs naturality, or fill the finite K_projective/K_commutator kernel values.",
            "derive_first": "show every Pi_i = Pi_bar_i(q,e_obs,theta) with same tau/worldtube support and boundary/response maps fixed after the solved fields, so delta_v(Pi_i J_i)=0 without cancellation.",
            "fallback": "fill K_trace/K_commutator, P_projective/P_commutator, J_norm, official numeric arrays, units and comparator bounds.",
            "avoid": "treating private SRNG as public proof; deleting projective trace; using CMSM templates/surrogates as data; fitted-G absorption.",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: Iterable[Mapping[str, object]]) -> str:
    materialized = [dict(row) for row in rows]
    if not materialized:
        return ""
    headers: List[str] = []
    for row in materialized:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in materialized:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source_register: List[Dict[str, object]],
    naturality_output: List[Dict[str, str]],
    kernel_output: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 432 PPC4161 transition: source/readout SRNG naturality or projective kernel values

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4416 makes the source/readout wall sharper:

- The downstream q/e_obs chain-rule argument is valid as a conditional theorem.
- The private SRNG branch closes `Pi_i delta J_i` when the source current is selected after the action solve on the same tau/worldtube support.
- The public theorem is not closed because `delta_v(Pi_i J_i)=Pi_i delta_v J_i+(delta_v Pi_i)J_i`, and `(delta_v Pi_i)J_i` remains unsigned.
- Projective trace source/readout coupling remains separate; it is not erased by saying "downstream readout".
- The fallback kernel rows are source-ready schemas only; no parent-owned numeric values are present.

## Source Register

{markdown_table(source_register)}

## Derivation Rows

{markdown_table(rows_from(DERIVATION_ROWS))}

## SRNG Naturality Gate

{markdown_table(naturality_output)}

## Projective / Commutator Kernel Values

{markdown_table(kernel_output)}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4416 - Y5/R2FR transition source/readout SRNG naturality or projective kernel values

Private checkpoint for the local-GR route.

Main result: SRNG now has an exact split. The chain rule really does kill downstream q/e_obs readout variation along ker(Dq), and it closes the private `Pi delta J` half when source currents descend on the same worldtube. But the public route still fails until the finite readout/projector/support maps satisfy `delta Pi=0`, and until projective trace coupling is fixed or bounded.

No local-GR/Newton/PPN/R10/clock/orbital claim fires. The fallback rows deliberately retain missing `K_trace`, `P_projective`, official numeric arrays and comparator bounds.

- Formal mirror: `{FORMAL_PATH}`
- Gate: `{GATE_PATH}`
- Generator: `{GENERATOR_PATH}`
- Validation: `{VALIDATION_PATH}`
- Next: `{NEXT_TARGET}`
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    body = text(path)
    block = f"\n{start}\n{section.rstrip()}\n{end}\n"
    if start in body and end in body:
        prefix = body[: body.index(start)]
        suffix = body[body.index(end) + len(end) :]
        write_text(path, prefix.rstrip() + block + suffix.lstrip("\n"))
    else:
        write_text(path, body.rstrip() + "\n" + block)


def update_claims_register() -> None:
    fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
    rows: List[Dict[str, str]] = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames:
                fieldnames = reader.fieldnames
            rows = [row for row in reader if row.get("claim_id") != CLAIM_ID]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "sector": "local_gr",
        "claim": "4416 sharpens SRNG/source-readout naturality. The downstream q/e_obs chain rule closes the private Pi_i delta J_i term for source currents selected after the action solve on the same support, but public source/readout silence is blocked by the projector/support commutator (delta_v Pi_i)J_i and by projective trace source/readout coupling. Fallback kernel-value rows are staged but lack K_trace, P_projective, official numeric source arrays and comparator bounds. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
        "current_evidence": "4416 source register, derivation rows, SRNG naturality output, projective kernel-value output, claim gates, decision, status, next target and validation CSV.",
        "evidence": "4416 source register, derivation rows, SRNG naturality output, projective kernel-value output, claim gates, decision, status, next target and validation CSV.",
        "status": "SRNG_chain_rule_private_branch_ready_commutator_projective_values_open_nonclaim",
        "next_test": "Prove delta_v Pi_i=0 for finite source/readout projectors/supports/weights/boundaries from q/e_obs naturality, or fill finite K_projective/K_commutator values.",
        "next_action": "Prove delta_v Pi_i=0 for finite source/readout projectors/supports/weights/boundaries from q/e_obs naturality, or fill finite K_projective/K_commutator values.",
        "key_risk": "Promoting private SRNG as public proof; hiding the (delta Pi)J commutator; deleting projective trace; using templates/surrogates as official numeric evidence.",
        "risk": "Promoting private SRNG as public proof; hiding the (delta Pi)J commutator; deleting projective trace; using templates/surrogates as official numeric evidence.",
    }
    for key in claim_row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4416 local spine update: SRNG chain rule split from projector commutator

4416 turns source/readout naturality into a precise algebraic split. Downstream q/e_obs readouts are vertically silent by the chain rule, so the private `Pi delta J` source-current term closes when sources are selected after the action solve on the same worldtube. The public theorem is blocked by the finite projector/support commutator `(delta Pi)J` and by projective trace source/readout coupling. This is progress: the missing piece is no longer generic "source coupling", it is `delta_v Pi_i=0` or a finite projective/commutator kernel value row."""
    packet_section = """## 4416 packet update: SRNG is half-won, not won

The SRNG route now has a theorem core: downstream q/e_obs readout maps cannot see vertical q-kernel motion. The unclosed half is the physical readout projector/support/mask/boundary machinery. Next target: prove those operators are q/e_obs-natural too, or fill `K_projective/K_commutator` with real sourced values."""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    source_register = rows_from(SOURCE_REGISTER)
    naturality_output = rows_from(NATURALITY_OUTPUT)
    kernel_output = rows_from(KERNEL_OUTPUT)
    claim_gates = rows_from(CLAIM_GATES)
    naturality_status = {row["row_id"]: row["current_status"] for row in naturality_output}
    kernel_status = {row["kernel_id"]: row["current_status"] for row in kernel_output}
    naturality_private = {
        row["row_id"]: row["private_srng_ready"]
        for row in naturality_output
        if "private_srng_ready" in row
    }
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in naturality_output + kernel_output + claim_gates)
    checks = [
        ("VAL4416_0_sources_exist", all(row["path_exists"] == "True" for row in source_register), "every cited source path exists"),
        ("VAL4416_1_source_needles_found", all(row["needle_found"] == "True" for row in source_register), "every cited source needle was found"),
        (
            "VAL4416_2_chain_rule_private_srng",
            naturality_private.get("NAT4416_0_current_private_chain_rule_branch") == "True",
            "current private branch closes Pi delta J by chain-rule/source descent",
        ),
        (
            "VAL4416_3_public_commutator_open",
            naturality_status.get("NAT4416_0_current_private_chain_rule_branch")
            == "SRNG_NATURALITY_PRIVATE_BRANCH_READY_COMMUTATOR_OR_PARENT_OPEN",
            "public branch remains blocked by commutator/projective/parent clauses",
        ),
        (
            "VAL4416_4_future_contract_nonclaim",
            naturality_status.get("NAT4416_1_future_public_contract")
            == "SRNG_NATURALITY_CONTRACT_READY_NONCLAIM",
            "future fully signed SRNG contract is nonclaim here",
        ),
        (
            "VAL4416_5_projective_kernel_blocked",
            kernel_status.get("KPV4416_0_projective_trace_common_kernel")
            == "PROJECTIVE_KERNEL_VALUES_BLOCKED_MISSING_PARENT_OR_OFFICIAL_INPUT",
            "projective kernel values remain blocked by missing parent/official inputs",
        ),
        (
            "VAL4416_6_commutator_kernel_blocked",
            kernel_status.get("KPV4416_1_projector_commutator_kernel")
            == "PROJECTIVE_KERNEL_VALUES_BLOCKED_MISSING_PARENT_OR_OFFICIAL_INPUT",
            "projector commutator kernel remains blocked by missing values",
        ),
        (
            "VAL4416_7_CMSM_kernel_blocked",
            kernel_status.get("KPV4416_2_CMSM_official_numeric_fallback")
            == "PROJECTIVE_KERNEL_VALUES_BLOCKED_MISSING_PARENT_OR_OFFICIAL_INPUT",
            "CMSM fallback refuses templates/surrogates as official numeric arrays",
        ),
        ("VAL4416_8_no_claim_outputs", no_claims, "no generated gate row is valid for claim"),
        ("VAL4416_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-257"),
        ("VAL4416_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4416_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4416_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4416_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4416_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4416_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(NATURALITY_INPUT, naturality_input_rows())
    write_csv(KERNEL_INPUT, kernel_input_rows())
    write_csv(NATURALITY_OUTPUT, evaluate_naturality_rows(NATURALITY_INPUT))
    write_csv(KERNEL_OUTPUT, evaluate_kernel_value_rows(KERNEL_INPUT))
    naturality_output = rows_from(NATURALITY_OUTPUT)
    kernel_output = rows_from(KERNEL_OUTPUT)
    claim_gates = claim_gate_rows(naturality_output, kernel_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    source_register = rows_from(SOURCE_REGISTER)
    write_text(FORMAL_PATH, build_doc(source_register, naturality_output, kernel_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(
        VALIDATION_PATH,
        validation_rows(
            {
                "formal": FORMAL_PATH,
                "post": DOC_PATH,
                "next": NEXT_CSV,
            }
        ),
    )


if __name__ == "__main__":
    main()
