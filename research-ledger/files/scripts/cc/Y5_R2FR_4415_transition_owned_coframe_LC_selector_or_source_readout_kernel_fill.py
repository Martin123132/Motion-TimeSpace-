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

from lc_selector_or_projective_kernel_gate import evaluate_kernel_rows, evaluate_selector_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4415"
CLAIM_ID = "L-256"
MARKER = "PPC4161_TRANSITION_OWNED_COFRAME_LC_SELECTOR_OR_PROJECTIVE_KERNEL_4415"
PACKET_MARKER = "PPC4161_PACKET_OWNED_COFRAME_LC_SELECTOR_OR_PROJECTIVE_KERNEL_4415"
DECISION = "LC_SELECTOR_REDUCED_TO_EXACT_PRODUCT_GATE_CORE_BRANCH_READY_SOURCE_READOUT_KERNEL_STAGED_NONCLAIM"
NEXT_TARGET = "4416-Y5-R2FR-transition-source-readout-SRNG-naturality-or-projective-kernel-values.md"

FORMAL_PATH = FORMAL / "431-PPC4161-transition-owned-coframe-LC-selector-or-source-readout-kernel.md"
DOC_PATH = POST / "4415-Y5-R2FR-transition-owned-coframe-LC-selector-or-source-readout-kernel-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4415_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4415_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4415_DERIVATION_ROWS.csv"
SELECTOR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4415_LC_SELECTOR_INPUT.csv"
SELECTOR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4415_LC_SELECTOR_OUTPUT.csv"
KERNEL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4415_PROJECTIVE_SOURCE_READOUT_KERNEL_INPUT.csv"
KERNEL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4415_PROJECTIVE_SOURCE_READOUT_KERNEL_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4415_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4415_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4415_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4415_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "lc_selector_or_projective_kernel_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4415_transition_owned_coframe_LC_selector_or_source_readout_kernel_fill.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4414 = SOURCE_DIR / "P8_Y5_R2FR_4414_NEXT_TARGET.csv"
FORMAL_430 = FORMAL / "430-PPC4161-transition-projective-boundary-readout-guard-or-first-P4-row.md"
POST_1963 = POST / "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md"
POST_1964 = POST / "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md"
POST_2117 = POST / "2117-Y5-R2FR-canonical-owned-coframe-action-promotion-or-sector-exceptions-ledger.md"
POST_2118 = POST / "2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md"
POST_2335 = POST / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md"
POST_3571 = POST / "3571-Y5-R2FR-parent-LC-branch-selector-theorem-or-source-owner-bound.md"
POST_4102 = POST / "4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md"
POST_4092 = POST / "4092-Y5-R2FR-parent-adoption-axiom-free-qbasic-selector-or-source-denominator-promotion.md"
POST_2099 = POST / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4415_00_4414_next": (
        NEXT_4414,
        "4415-Y5-R2FR-transition-owned-coframe-LC-selector-or-source-readout-kernel-fill.md",
        "4414 selected LC selector or source/readout projective kernel.",
    ),
    "SRC4415_01_4414_formal": (
        FORMAL_430,
        "parent selector and affine/source-readout counterbranch exclusion remain unsigned",
        "4414 handoff into selector product.",
    ),
    "SRC4415_02_1963_branch": (
        POST_1963,
        "delta S_parent divided by delta Gamma_ind is vacuous",
        "minimal owned-coframe branch/no-Gamma theorem.",
    ),
    "SRC4415_03_1964_legitimacy": (
        POST_1964,
        "parent map `e_obs=E[q(Phi_MTS)]` is missing",
        "owned coframe legitimacy but q->e map missing.",
    ),
    "SRC4415_04_2117_exceptions": (
        POST_2117,
        "PROMOTION_BLOCKED_BY_SECTOR_EXCEPTIONS",
        "canonical promotion blocked by named sector exceptions.",
    ),
    "SRC4415_05_2335_SRNG": (
        POST_2335,
        "SRNG source-readout no-Gamma contract is now explicit",
        "source/readout no-Gamma contract.",
    ),
    "SRC4415_06_3571_product": (
        POST_3571,
        "B_LC_selector = product_s I_s",
        "LC selector exact finite product theorem.",
    ),
    "SRC4415_07_4102_no_affine": (
        POST_4102,
        "NoAffineGenerator",
        "local LC selector/no vertical affine slot.",
    ),
    "SRC4415_08_4092_parent_normal_form": (
        POST_4092,
        "Args(S_parent^loc) subset",
        "candidate parent-action normal form.",
    ),
    "SRC4415_09_2118_projective_kernel": (
        POST_2118,
        "KSR2118_6_projective_trace_kernel",
        "projective trace source/readout kernel requirements.",
    ),
    "SRC4415_10_2099_projective_map": (
        POST_2099,
        "DGM2099_6_projective",
        "DeltaGamma projective component map.",
    ),
    "SRC4415_11_gate": (
        GATE_PATH,
        "def evaluate_selector_rows",
        "new LC selector/product and kernel gate.",
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
            "derivation_id": "SEL4415_0_product_selector",
            "claim": "The public LC selector is an exact no-cancellation product gate.",
            "derivation": "Let I_s=1 only when sector s has no independent affine action slot and no downstream source/readout reentry, or when its residual is separately zero/bounded. Then B_LC_selector=prod_s I_s. One open sector makes the public selector false without relying on cancellations.",
            "consequence": "The owned-coframe/LC branch can be worked as a theorem branch, but public promotion requires every active factor or a leakage-bound fallback.",
            "status": "DERIVED_PRODUCT_GATE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SEL4415_1_no_affine_core",
            "claim": "Inside the candidate branch, no affine generator means C=Gamma-Gamma_LC has no field-domain slot.",
            "derivation": "If compact local fields are q->e_obs->g_obs plus visible matter/EM/downstream readouts, and Gamma_ind/omega_ind are not arguments of S_parent^loc, then delta_Gamma S_parent^loc is vacuous in the reduced domain.",
            "consequence": "Matter/spin/projective-Ruu pieces are core-branch clean; this is stronger than fitting torsion small.",
            "status": "CORE_BRANCH_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SEL4415_2_source_readout_SRNG",
            "claim": "SRNG is the minimal source/readout clause needed to make the selector product public.",
            "derivation": "Source support, clocks, light, orbits and readout maps must be downstream functors of solved q/e_obs fields, not action/source arguments containing Gamma_ind or projective trace.",
            "consequence": "If SRNG is derived from quotient/naturality, source/readout factors close together; otherwise the projective kernel must be filled.",
            "status": "CONDITIONAL_THEOREM_TARGET",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SEL4415_3_poynting_policy",
            "claim": "Poynting/EM is not ignored: it is Hilbert/Noether source energy or a collar-flux residual.",
            "derivation": "Maxwell stress built from A_owned and g_obs has no affine slot; Poynting flux affects H_tau/source-worldtube bookkeeping, not independent Gamma, unless a boundary/collar flux survives.",
            "consequence": "The selector product needs poynting_flux_owned_or_bounded=true before public promotion.",
            "status": "EM_POLICY_DERIVED_BOUND_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SEL4415_4_kernel_fallback",
            "claim": "If SRNG/projective source-readout is unsigned, the first projective kernel is the honest fallback.",
            "derivation": "Delta_projective^arena = P_projective^arena K_trace J_trace on the same support. Score requires coefficient, units, projection matrix, support certificate, comparator bound and no-cancellation guard.",
            "consequence": "4415 stages the row so the next step can derive SRNG or fill real values instead of reopening the whole torsion argument.",
            "status": "PROJECTIVE_KERNEL_SCHEMA_STAGED",
            "valid_for_claim": False,
        },
    ]


def selector_input_rows() -> List[Dict[str, object]]:
    base = {"input_valid": False, "valid_for_claim": False}
    return [
        {
            "selector_id": "LCS4415_0_current_owned_coframe_core",
            "branch": "current_owned_coframe_lc_core",
            "no_affine_generator": True,
            "q_to_eobs_signed": False,
            "matter_no_gamma": True,
            "spin_no_gamma": True,
            "em_hilbert_no_affine": True,
            "poynting_flux_owned_or_bounded": False,
            "source_readout_srng_signed": False,
            "clock_light_orbit_downstream": False,
            "boundary_href_gm_locked": False,
            "projective_ruu_closed": True,
            "projective_source_readout_closed": False,
            "affine_counterbranch_excluded": False,
            "leakage_bound_ready": False,
            "source_path": str(POST_4102),
            "notes": "Core branch is mathematically clean, but source/readout, boundary, Poynting collar and counterbranch factors keep B_LC public false.",
            **base,
        },
        {
            "selector_id": "LCS4415_1_SRNG_future_public_contract",
            "branch": "future_SRNG_parent_signed_owned_coframe_lc",
            "no_affine_generator": True,
            "q_to_eobs_signed": True,
            "matter_no_gamma": True,
            "spin_no_gamma": True,
            "em_hilbert_no_affine": True,
            "poynting_flux_owned_or_bounded": True,
            "source_readout_srng_signed": True,
            "clock_light_orbit_downstream": True,
            "boundary_href_gm_locked": True,
            "projective_ruu_closed": True,
            "projective_source_readout_closed": True,
            "affine_counterbranch_excluded": True,
            "leakage_bound_ready": False,
            "source_path": str(POST_2335),
            "notes": "Future schema: if SRNG and support locks are parent-derived, B_LC_selector=1; still nonclaim here because this row is only a contract.",
            **base,
        },
        {
            "selector_id": "LCS4415_2_affine_fallback_bounded_route",
            "branch": "affine_counterbranch_with_explicit_bounds",
            "no_affine_generator": False,
            "q_to_eobs_signed": False,
            "matter_no_gamma": False,
            "spin_no_gamma": False,
            "em_hilbert_no_affine": True,
            "poynting_flux_owned_or_bounded": False,
            "source_readout_srng_signed": False,
            "clock_light_orbit_downstream": False,
            "boundary_href_gm_locked": False,
            "projective_ruu_closed": True,
            "projective_source_readout_closed": False,
            "affine_counterbranch_excluded": False,
            "leakage_bound_ready": False,
            "source_path": str(POST_2099),
            "notes": "Fallback exists only as residual kernels; not score-ready until coefficients/projections/bounds are real.",
            **base,
        },
    ]


def kernel_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "kernel_id": "KPR4415_0_projective_source_readout_kernel",
            "residual_component": "projective_trace_current",
            "arena": "WEP_CLOCK_SOURCE_ORBITAL_COMMON",
            "observable": "eta_AB;delta_nu_over_nu;source_charge_residual;orbital_GM_tail",
            "kernel_formula": "Delta_projective^arena = P_projective^arena * K_trace * J_trace[source,clock,WEP,orbit]",
            "coefficient": "MISSING_K_TRACE_VALUE",
            "coefficient_units": "projective_current_per_source_readout_unit",
            "projection_matrix": "MISSING_P_PROJECTIVE_ARENA",
            "support_certificate": "same_q_eobs_tau_worldtube_support_required",
            "comparator_bound": "MISSING_WEP_CLOCK_SOURCE_ORBITAL_BOUND",
            "source_path": str(POST_2118),
            "no_cancellation_guard": True,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "First executable schema row; numeric coefficient, projection and comparator bound still need derivation or source acquisition.",
        },
        {
            "kernel_id": "KPR4415_1_poynting_collar_flux_kernel",
            "residual_component": "epsilon_Poynting_worldtube",
            "arena": "EM_SOURCE_WORLDTUBE_BOUNDARY",
            "observable": "source_energy_flux;H_tau_tail;GM_transfer_tail",
            "kernel_formula": "epsilon_Poynting = |int_collar S_EM^n dA dt| / |H_tau_source|",
            "coefficient": "MISSING_EM_COLLAR_FLUX_VALUE",
            "coefficient_units": "dimensionless_energy_flux_ratio",
            "projection_matrix": "MISSING_H_TAU_TO_GM_OR_PPN_PROJECTION",
            "support_certificate": "MISSING_EM_COLLAR_SUPPORT_OR_NO_FLUX_THEOREM",
            "comparator_bound": "MISSING_SOURCE_DENOMINATOR_MARGIN",
            "source_path": str(POST_3571),
            "no_cancellation_guard": True,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Poynting is retained as Hilbert/source flux; this row prevents deleting it by language.",
        },
    ]


def claim_gate_rows(selector_output: List[Mapping[str, str]], kernel_output: List[Mapping[str, str]]) -> List[Dict[str, object]]:
    selector_status = {row["selector_id"]: row["current_status"] for row in selector_output}
    kernel_status = {row["kernel_id"]: row["current_status"] for row in kernel_output}
    return [
        {
            "gate_id": "CG4415_0_product_gate",
            "claim": "LC selector reduced to finite product gate",
            "passed": True,
            "valid_for_claim": False,
            "detail": "B_LC_selector=product_s I_s; no cancellation shortcut allowed",
        },
        {
            "gate_id": "CG4415_1_core_branch_ready",
            "claim": "owned-coframe LC core branch is ready",
            "passed": selector_status.get("LCS4415_0_current_owned_coframe_core")
            == "LC_SELECTOR_CORE_BRANCH_READY_SECTOR_PRODUCT_OPEN",
            "valid_for_claim": False,
            "detail": "core branch ready, but sector product open",
        },
        {
            "gate_id": "CG4415_2_public_selector",
            "claim": "B_LC_selector=1 publicly",
            "passed": False,
            "valid_for_claim": False,
            "detail": "q->e_obs, SRNG, Poynting/boundary/Href/GM/readout and counterbranch factors are unsigned",
        },
        {
            "gate_id": "CG4415_3_projective_kernel_staged",
            "claim": "first projective source/readout kernel row is staged",
            "passed": kernel_status.get("KPR4415_0_projective_source_readout_kernel")
            == "PROJECTIVE_SOURCE_READOUT_KERNEL_SCHEMA_STAGED_NONCLAIM",
            "valid_for_claim": False,
            "detail": "schema exists but coefficient/projection/bound are missing",
        },
        {
            "gate_id": "CG4415_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN follows",
            "passed": False,
            "valid_for_claim": False,
            "detail": "selector product and kernel values are still nonclaim, and EH/GM/PPN stack remains open",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4415_0",
            "decision": DECISION,
            "summary": "4415 consolidates the LC branch selector into an exact product gate. The owned-coframe/no-affine core is ready as a theorem branch, but public B_LC_selector=1 is blocked by q->e_obs signing, SRNG/source-readout naturality, Poynting/boundary/Href/GM support locks and affine-counterbranch exclusion. The first projective source/readout kernel schema is staged as fallback.",
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
            "best_result": "LC_selector_exact_product_gate_and_core_branch_ready",
            "still_missing": "q_to_eobs_parent_signature; SRNG_naturality; projective_kernel_values; poynting_boundary_Href_GM_locks; affine_counterbranch_exclusion",
            "valid_for_claim": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4415_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive SRNG/source-readout naturality from q/e_obs functoriality; if that fails, fill K_trace, P_projective and comparator bounds for the projective source/readout kernel.",
            "derive_first": "prove source, clocks, light, orbits and readouts are downstream natural functors of q/e_obs and cannot be variational Gamma_ind/projective-trace source terms.",
            "fallback": "supply coefficient, units, support, projection matrix and comparator bound for KPR4415_0; keep no-cancellation guard active.",
            "avoid": "claiming B_LC_selector=1 from the core branch alone; deleting Poynting/collar flux; absorbing projective trace into fitted G/GM.",
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
    selector_output: List[Dict[str, str]],
    kernel_output: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 431 PPC4161 transition: owned-coframe LC selector or source/readout kernel

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4415 is the selector checkpoint:

- The LC selector is now an exact product gate: `B_LC_selector = prod_s I_s`.
- The owned-coframe/no-affine core branch is ready as a nonclaim theorem branch.
- Public `B_LC_selector=1` is not proved because source/readout SRNG, q-to-e_obs signing, boundary/H_ref/GM/Poynting locks and affine-counterbranch exclusion are still unsigned.
- The first projective source/readout kernel schema is staged so the fallback is executable rather than rhetorical.

## Source Register

{markdown_table(source_register)}

## Derivation Rows

{markdown_table(rows_from(DERIVATION_ROWS))}

## LC Selector Product Gate

{markdown_table(selector_output)}

## Projective Source/Readout Kernel

{markdown_table(kernel_output)}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4415 - Y5/R2FR transition owned-coframe LC selector or source/readout kernel fill

Private checkpoint for the local-GR route.

Main result: `B_LC_selector` is not a vibe. It is an exact product over sector indicators. The core owned-coframe/no-affine branch is ready, but the public selector is still false until source/readout SRNG, q->e_obs, Poynting/boundary/H_ref/GM and counterbranch clauses close or are bounded.

Fallback staged: first projective source/readout kernel row with formula, units target, support requirement, no-cancellation guard and missing numeric/source inputs.

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
        "claim": "4415 reduces the owned-coframe/LC selector to an exact finite product gate B_LC_selector=prod_s I_s. The no-affine owned-coframe core branch is ready as a theorem branch, but public B_LC_selector=1 is blocked by q->e_obs signing, SRNG/source-readout naturality, Poynting/boundary/H_ref/GM locks and affine-counterbranch exclusion. The first projective source/readout kernel row is staged as fallback. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
        "current_evidence": "4415 source register, derivation rows, selector output, projective kernel output, claim gates, decision, status, next target and validation CSV.",
        "evidence": "4415 source register, derivation rows, selector output, projective kernel output, claim gates, decision, status, next target and validation CSV.",
        "status": "LC_selector_product_gate_core_branch_ready_kernel_staged_nonclaim",
        "next_test": "Derive SRNG/source-readout naturality from q/e_obs functoriality, or fill K_trace, P_projective and comparator bounds for the projective source/readout kernel.",
        "next_action": "Derive SRNG/source-readout naturality from q/e_obs functoriality, or fill K_trace, P_projective and comparator bounds for the projective source/readout kernel.",
        "key_risk": "Claiming B_LC_selector=1 from the core branch alone; deleting Poynting/collar flux; absorbing projective/source-readout residuals into fitted G or GM.",
        "risk": "Claiming B_LC_selector=1 from the core branch alone; deleting Poynting/collar flux; absorbing projective/source-readout residuals into fitted G or GM.",
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
    spine_section = """## 4415 local spine update: LC selector is a product gate

4415 turns the owned-coframe/LC selector into the exact finite gate `B_LC_selector=prod_s I_s`. The core branch is real: no affine generator, matter/spin no-Gamma, EM Hilbert stress and projective `R_uu` silence make the branch mathematically clean. Public promotion still fails because q->e_obs signing, SRNG/source-readout naturality, Poynting/collar flux, boundary/H_ref/GM locks and affine-counterbranch exclusion are not all signed. The fallback is now an executable projective source/readout kernel row rather than another verbal blocker."""
    packet_section = """## 4415 packet update: selector product, not vibes

The LC branch is now controlled by a product: every sector indicator must be 1 or the selector is not public. This protects the theory from smuggling. The next best move is SRNG naturality: prove source/readout objects are downstream functors of q/e_obs, or fill the first projective source/readout kernel with real coefficient/projection/bound inputs."""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    source_register = rows_from(SOURCE_REGISTER)
    selector_output = rows_from(SELECTOR_OUTPUT)
    kernel_output = rows_from(KERNEL_OUTPUT)
    claim_gates = rows_from(CLAIM_GATES)
    selector_status = {row["selector_id"]: row["current_status"] for row in selector_output}
    kernel_status = {row["kernel_id"]: row["current_status"] for row in kernel_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in selector_output + kernel_output + claim_gates)
    checks = [
        ("VAL4415_0_sources_exist", all(row["path_exists"] == "True" for row in source_register), "every cited source path exists"),
        ("VAL4415_1_source_needles_found", all(row["needle_found"] == "True" for row in source_register), "every cited source needle was found"),
        (
            "VAL4415_2_core_branch_ready",
            selector_status.get("LCS4415_0_current_owned_coframe_core")
            == "LC_SELECTOR_CORE_BRANCH_READY_SECTOR_PRODUCT_OPEN",
            "core owned-coframe selector branch is ready but sector product remains open",
        ),
        (
            "VAL4415_3_future_contract_nonclaim",
            selector_status.get("LCS4415_1_SRNG_future_public_contract") == "LC_SELECTOR_CONTRACT_READY_NONCLAIM",
            "future SRNG selector contract remains nonclaim",
        ),
        (
            "VAL4415_4_affine_fallback_blocked",
            selector_status.get("LCS4415_2_affine_fallback_bounded_route") == "LC_SELECTOR_BLOCKED",
            "affine fallback is not bounded/score-ready",
        ),
        (
            "VAL4415_5_projective_kernel_staged",
            kernel_status.get("KPR4415_0_projective_source_readout_kernel")
            == "PROJECTIVE_SOURCE_READOUT_KERNEL_SCHEMA_STAGED_NONCLAIM",
            "first projective source/readout kernel schema is staged",
        ),
        (
            "VAL4415_6_poynting_kernel_staged",
            kernel_status.get("KPR4415_1_poynting_collar_flux_kernel")
            == "PROJECTIVE_SOURCE_READOUT_KERNEL_SCHEMA_STAGED_NONCLAIM",
            "Poynting/collar flux schema is staged",
        ),
        ("VAL4415_7_no_claim_outputs", no_claims, "no generated gate row is valid for claim"),
        ("VAL4415_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-256"),
        ("VAL4415_9_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4415_10_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4415_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4415_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4415_13_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4415_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
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
    write_csv(SELECTOR_INPUT, selector_input_rows())
    write_csv(KERNEL_INPUT, kernel_input_rows())
    write_csv(SELECTOR_OUTPUT, evaluate_selector_rows(SELECTOR_INPUT))
    write_csv(KERNEL_OUTPUT, evaluate_kernel_rows(KERNEL_INPUT))
    selector_output = rows_from(SELECTOR_OUTPUT)
    kernel_output = rows_from(KERNEL_OUTPUT)
    claim_gates = claim_gate_rows(selector_output, kernel_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    source_register = rows_from(SOURCE_REGISTER)
    write_text(FORMAL_PATH, build_doc(source_register, selector_output, kernel_output, claim_gates))
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
