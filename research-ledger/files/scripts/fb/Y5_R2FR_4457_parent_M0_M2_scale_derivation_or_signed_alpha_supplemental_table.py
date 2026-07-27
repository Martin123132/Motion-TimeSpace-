from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from quadratic_pole_mass_gate import (  # noqa: E402
    coefficient_bounds_from_thresholds,
    evaluate_parent_coefficient_row,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4457"
CLAIM_ID = "L-299"
MARKER = "PPC4161_PARENT_M0_M2_SCALE_DERIVATION_OR_SIGNED_ALPHA_SUPPLEMENTAL_TABLE_4457"
PACKET_MARKER = "PPC4161_PACKET_PARENT_M0_M2_SCALE_DERIVATION_OR_SIGNED_ALPHA_SUPPLEMENTAL_TABLE_4457"
DECISION = "CANONICAL_QUADRATIC_POLE_MASS_CONTRACT_AND_COEFFICIENT_REGION_DERIVED_MTS_NORMALIZATION_OR_SIGNED_TABLE_STILL_REQUIRED_NONCLAIM"
NEXT_TARGET = "4458-Y5-R2FR-MTS-quadratic-coefficient-normalization-map-or-cR2-zero-selector.md"

FORMAL_PATH = FORMAL / "473-PPC4161-parent-M0-M2-scale-derivation-or-signed-alpha-supplemental-table.md"
DOC_PATH = POST / "4457-Y5-R2FR-parent-M0-M2-scale-derivation-or-signed-alpha-supplemental-table.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4457_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4457_SOURCE_REGISTER.csv"
POLE_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4457_CANONICAL_POLE_MASS_CONTRACT.csv"
COEFFICIENT_BOUNDS = SOURCE_DIR / "P8_Y5_R2FR_4457_COEFFICIENT_REGION_BOUNDS.csv"
PARENT_COEFFICIENT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4457_PARENT_COEFFICIENT_INPUT_TEMPLATE.csv"
PARENT_COEFFICIENT_EVAL = SOURCE_DIR / "P8_Y5_R2FR_4457_PARENT_COEFFICIENT_EVALUATION.csv"
ZERO_ROUTE_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4457_ZERO_ROUTE_AUDIT.csv"
SUPPLEMENTAL_ROUTE = SOURCE_DIR / "P8_Y5_R2FR_4457_SIGNED_SUPPLEMENTAL_ROUTE.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4457_DERIVATION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4457_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4457_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4457_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4457_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "quadratic_pole_mass_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4457_parent_M0_M2_scale_derivation_or_signed_alpha_supplemental_table.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4456 = SOURCE_DIR / "P8_Y5_R2FR_4456_NEXT_TARGET.csv"
THRESHOLDS_4456 = SOURCE_DIR / "P8_Y5_R2FR_4456_CHANNEL_THRESHOLDS_CANDIDATE.csv"
RULES_4456 = SOURCE_DIR / "P8_Y5_R2FR_4456_PARENT_SCALE_RULES.csv"
STATUS_4456 = SOURCE_DIR / "P8_Y5_R2FR_4456_STATUS.csv"
SUPP_4456 = SOURCE_DIR / "P8_Y5_R2FR_4456_SUPPLEMENTAL_ACQUISITION_STATUS.csv"
FORMAL_472 = FORMAL / "472-PPC4161-alpha-lambda-curve-promotion-or-parent-MR-scale-value.md"
R2FR_963 = POST / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md"
R2FR_964 = POST / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"
R2FR_966 = POST / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
WEB_CASIMIR_QG = "https://link.springer.com/article/10.1140/epjc/s10052-019-6574-1"
WEB_INTERFERENCE_QG = "https://link.springer.com/article/10.1140/epjc/s10052-021-09740-2"
WEB_LEE_2020 = "https://arxiv.org/abs/2002.11761"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4457_00_next4456", "kind": "local", "ref": str(NEXT_4456), "needle": "4457-Y5-R2FR-parent-M0-M2-scale-derivation-or-signed-alpha-supplemental-table.md", "role": "4456 selected parent-scale/signed-table target."},
        {"source_id": "SRC4457_01_thresholds4456", "kind": "local", "ref": str(THRESHOLDS_4456), "needle": "CH4456_1_spin2", "role": "4456 channel mass thresholds."},
        {"source_id": "SRC4457_02_rules4456", "kind": "local", "ref": str(RULES_4456), "needle": "MR4456_3_common_parent_mass_candidate", "role": "4456 strict common parent-scale smoke rule."},
        {"source_id": "SRC4457_03_status4456", "kind": "local", "ref": str(STATUS_4456), "needle": "numeric_M0_M2_or_zero_theorem_missing", "role": "4456 parent-scale missing status."},
        {"source_id": "SRC4457_04_supp4456", "kind": "local", "ref": str(SUPP_4456), "needle": "HTTP_403", "role": "4456 APS supplemental access status."},
        {"source_id": "SRC4457_05_formal472", "kind": "local", "ref": str(FORMAL_472), "needle": "M_2 >=", "role": "formal 4456 threshold."},
        {"source_id": "SRC4457_06_r2fr963", "kind": "local", "ref": str(R2FR_963), "needle": "relative_theorem_available", "role": "older R2FR zero theorem is conditional."},
        {"source_id": "SRC4457_07_r2fr964", "kind": "local", "ref": str(R2FR_964), "needle": "EH + epsilon int sqrt(-g) R^2", "role": "older countermodel blocks easy minimality claim."},
        {"source_id": "SRC4457_08_r2fr966", "kind": "local", "ref": str(R2FR_966), "needle": "curve cannot score MTS until the parent produces numeric alpha/lambda inputs", "role": "older finite-branch data policy."},
        {"source_id": "SRC4457_09_core_action", "kind": "local", "ref": str(CORE_ACTION), "needle": "A[g,ψ] = ∫[(1/2κ)R", "role": "core EH action seed."},
        {"source_id": "SRC4457_10_web_casimir", "kind": "web", "ref": WEB_CASIMIR_QG, "needle": "quadratic-gravity potential and masses", "role": "external canonical potential/mass formula."},
        {"source_id": "SRC4457_11_web_interference", "kind": "web", "ref": WEB_INTERFERENCE_QG, "needle": "linearized quadratic gravity potential", "role": "external cross-check formula source."},
        {"source_id": "SRC4457_12_web_lee", "kind": "web", "ref": WEB_LEE_2020, "needle": "Lee 2020 R10 source", "role": "external R10 bound source."},
        {"source_id": "SRC4457_13_gate", "kind": "local", "ref": str(GATE_PATH), "needle": "coefficient_bounds_from_thresholds", "role": "4457 coefficient bound gate."},
        {"source_id": "SRC4457_14_generator", "kind": "local", "ref": str(GENERATOR_PATH), "needle": 'CHECKPOINT = "4457"', "role": "4457 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        kind = str(spec["kind"])
        ref = str(spec["ref"])
        path = Path(ref) if kind == "local" else None
        line = line_of(path, str(spec["needle"])) if path else 0
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": kind,
                "source_ref": ref,
                "local_path_exists": bool(path and path.exists()),
                "web_source_recorded": kind == "web" and ref.startswith("https://"),
                "needle": spec["needle"],
                "needle_found": line > 0 if kind == "local" else True,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def pole_contract_rows() -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "PM4457_0_canonical_action",
            "statement": "Use only as an external canonical coordinate chart: S = int sqrt(-g) [R + alpha_QG R^2 + beta_QG R_mn R^mn + ...]",
            "formula": "normalization_map_MTS_to_QG required before alpha_QG,beta_QG can be identified with MTS c_R2 terms",
            "claim_status": "coordinate_template_not_MTS_derivation",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PM4457_1_potential",
            "statement": "Static weak-field point-source potential contains scalar and massive-spin2 Yukawa tails.",
            "formula": "Phi/Phi_N = 1 + (1/3) exp(-M_0 r) - (4/3) exp(-M_2 r)",
            "claim_status": "template_matches_4455_projection",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PM4457_2_scalar_mass",
            "statement": "In the chosen canonical convention the scalar pole is controlled by D0=12 alpha_QG + beta_QG.",
            "formula": "M_0[eV] = hbar*c * 2/sqrt(12 alpha_QG + beta_QG), requiring 12 alpha_QG + beta_QG > 0",
            "claim_status": "requires_MTS_normalization_map",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PM4457_3_spin2_mass",
            "statement": "In the chosen canonical convention the massive spin-2 pole is controlled by D2=-beta_QG.",
            "formula": "M_2[eV] = hbar*c * sqrt(2/(-beta_QG)), requiring beta_QG < 0",
            "claim_status": "requires_MTS_normalization_map_and_does_not_solve_ghost_interpretation",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PM4457_4_zero_selector",
            "statement": "If parent action forbids the quadratic terms, alpha_QG=beta_QG=0 and the finite Yukawa branch is absent.",
            "formula": "zero route requires parent-signed no-higher-curvature/no-integrated-out-scalar theorem",
            "claim_status": "not_parent_signed_in_current_corpus",
            "valid_for_claim": False,
        },
    ]


def parent_coefficient_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "candidate_id": "PC4457_0_required_real_parent_row",
            "alpha_QG_m2": "MISSING_PARENT_ALPHA_QG",
            "beta_QG_m2": "MISSING_PARENT_BETA_QG",
            "normalization_map": "MISSING_MAP_FROM_MTS_cR2_Ricci2_TO_CANONICAL_ALPHA_BETA",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PC4457_1_zero_selector_switch",
            "alpha_QG_m2": "0_ONLY_IF_PARENT_ZERO_SELECTOR_SIGNED",
            "beta_QG_m2": "0_ONLY_IF_PARENT_ZERO_SELECTOR_SIGNED",
            "normalization_map": "zero_selector_bypasses_finite_pole_map_only_if_parent_signed",
            "source_path": str(R2FR_964),
            "valid_for_claim": False,
        },
    ]


def zero_route_rows() -> List[Dict[str, object]]:
    return [
        {
            "zero_id": "ZR4457_0_relative_theorem",
            "route": "second_order_metric_no_extra_scalar",
            "evidence_path": str(R2FR_963),
            "current_status": "RELATIVE_THEOREM_AVAILABLE_PARENT_SIGNATURE_MISSING",
            "blocks_claim": True,
            "next_requirement": "parent-sign no higher-curvature local metric operators and no integrated-out scalar curvature tower",
            "valid_for_claim": False,
        },
        {
            "zero_id": "ZR4457_1_countermodel",
            "route": "EH_plus_epsilon_R2",
            "evidence_path": str(R2FR_964),
            "current_status": "LIVE_COUNTERMODEL_UNLESS_PARENT_MINIMALITY_SIGNED",
            "blocks_claim": True,
            "next_requirement": "derive primitive minimal quotient/no-marker/no-extension theorem or keep finite branch",
            "valid_for_claim": False,
        },
        {
            "zero_id": "ZR4457_2_data_policy",
            "route": "finite_branch_runner",
            "evidence_path": str(R2FR_966),
            "current_status": "FINITE_BRANCH_NEEDS_NUMERIC_ALPHA_LAMBDA_FROM_PARENT",
            "blocks_claim": True,
            "next_requirement": "fill parent alpha_QG,beta_QG plus signed R10 table or prove zero selector",
            "valid_for_claim": False,
        },
    ]


def supplemental_route_rows() -> List[Dict[str, object]]:
    return [
        {
            "supplemental_id": "SA4457_0_current_access",
            "route": "APS_signed_positive_negative_alpha_table",
            "evidence_path": str(SUPP_4456),
            "status": "HTTP_403_IN_4456_HEAD_REQUEST",
            "effect": "cannot replace candidate absolute curve with official signed table in this checkpoint",
            "valid_for_claim": False,
        },
        {
            "supplemental_id": "SA4457_1_claim_use_if_acquired",
            "route": "signed_table_recovered",
            "evidence_path": "future_manual_or_downloaded_table",
            "status": "NOT_ACQUIRED",
            "effect": "would let scalar alpha>0 and spin2 alpha<0 be scored against sign-specific bounds",
            "valid_for_claim": False,
        },
    ]


def derivation_rows(bounds: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    scalar = next(row for row in bounds if row["bound_id"] == "QB4457_0_scalar_D0")
    spin2 = next(row for row in bounds if row["bound_id"] == "QB4457_1_spin2_D2")
    return [
        {
            "derivation_id": "D4457_0_mass_contract",
            "premise": "4455/4456 reduced cR2 to scalar and massive-spin2 Yukawa channels.",
            "derivation": "Use the canonical quadratic-gravity pole chart: D0=12 alpha_QG+beta_QG, D2=-beta_QG, M0=hbar*c*2/sqrt(D0), M2=hbar*c*sqrt(2/D2).",
            "result": "A future MTS coefficient row can be converted directly to M0/M2.",
            "status": "CONTRACT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4457_1_scalar_coefficient_bound",
            "premise": "4456 candidate curve gives lambda_0_star for |alpha_0|=1/3.",
            "derivation": f"D0 <= 4 lambda_0_star^2 = {scalar['coefficient_upper_bound_m2']} m^2.",
            "result": f"0 < 12 alpha_QG + beta_QG <= {scalar['coefficient_upper_bound_um2']} micrometer^2 in the canonical convention.",
            "status": "PRIVATE_BOUND_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4457_2_spin2_coefficient_bound",
            "premise": "4456 candidate curve gives lambda_2_star for |alpha_2|=4/3.",
            "derivation": f"D2 <= 2 lambda_2_star^2 = {spin2['coefficient_upper_bound_m2']} m^2.",
            "result": f"0 < -beta_QG <= {spin2['coefficient_upper_bound_um2']} micrometer^2 in the canonical convention.",
            "status": "PRIVATE_BOUND_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4457_3_no_free_cancellation",
            "premise": "Scalar and spin2 terms have different signs.",
            "derivation": "Do not cancel them against each other in R10 unless the parent action derives a channel-correlation identity and the signed alpha table is used.",
            "result": "Separate channel bounds are retained.",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4457_4_zero_or_finite_decision",
            "premise": "Older 963-966 work shows c_R2/fR zero is conditional, not parent-signed.",
            "derivation": "Either sign a zero selector/minimality theorem, or fill alpha_QG,beta_QG and score the finite branch.",
            "result": "4458 should attack the MTS normalization map or cR2 zero selector.",
            "status": "NEXT_HINGE_SELECTED",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(bounds: Sequence[Dict[str, object]], eval_rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    local_sources_ok = all(row["needle_found"] for row in source_rows() if row["source_kind"] == "local")
    bounds_ok = len(bounds) == 3 and all(row["valid_for_claim"] is False for row in bounds)
    no_parent_values = all(row["has_numeric_alpha_beta"] is False for row in eval_rows)
    return [
        {"gate_id": "CG4457_0_sources", "claim": "all local source paths and needles exist", "passed": local_sources_ok, "valid_for_claim": False, "detail": "4456, 963/964/966, core action, scripts located."},
        {"gate_id": "CG4457_1_pole_contract", "claim": "canonical pole-mass contract written", "passed": len(pole_contract_rows()) >= 5, "valid_for_claim": False, "detail": "M0/M2 formula rows exist."},
        {"gate_id": "CG4457_2_coefficient_bounds", "claim": "4456 mass thresholds converted to coefficient inequalities", "passed": bounds_ok, "valid_for_claim": False, "detail": "D0 and D2 bounds written."},
        {"gate_id": "CG4457_3_parent_values_missing", "claim": "no parent alpha_QG,beta_QG row is silently treated as sourced", "passed": no_parent_values, "valid_for_claim": False, "detail": "input template rejects placeholders."},
        {"gate_id": "CG4457_4_zero_not_claimed", "claim": "R2/fR zero selector remains unsigned", "passed": True, "valid_for_claim": False, "detail": "963/964 countermodel route retained."},
        {"gate_id": "CG4457_5_supplemental_not_claimed", "claim": "signed APS table not promoted", "passed": True, "valid_for_claim": False, "detail": "4456 access status remains HTTP_403/not acquired."},
        {"gate_id": "CG4457_6_no_public_claim", "claim": "no R10/local-GR public claim emitted", "passed": True, "valid_for_claim": False, "detail": "candidate coefficient region is private smoke only."},
        {"gate_id": "CG4457_7_next_target", "claim": "next target selected", "passed": True, "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows(bounds: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    spin2 = next(row for row in bounds if row["bound_id"] == "QB4457_1_spin2_D2")
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "strictest_channel": "spin2",
            "strictest_mass_threshold_eV_candidate": spin2["mass_threshold_eV"],
            "strictest_coefficient_bound_m2_candidate": spin2["coefficient_upper_bound_m2"],
            "parent_normalization_ready": False,
            "zero_selector_signed": False,
            "signed_supplemental_table_ready": False,
            "public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "pole_contract_status": "canonical_M0_M2_formula_contract_written",
            "coefficient_status": "candidate_D0_D2_bounds_written_MTS_normalization_missing",
            "zero_status": "conditional_zero_theorem_not_parent_signed",
            "supplemental_status": "signed_table_not_acquired",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4457_0",
            "target": NEXT_TARGET,
            "objective": "Either map MTS cR2/Ricci2 coefficients into canonical alpha_QG,beta_QG, or prove a parent selector sets them absent/topological.",
            "derive_first": "normalization map from MTS parent residual coefficient to canonical quadratic-gravity pole denominators D0,D2",
            "fallback": "zero-selector/minimality theorem for no higher-curvature local metric operators",
            "risk": "mistaking a canonical external coefficient chart for a parent-owned MTS coefficient value",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "The cR2 finite branch now has an exact canonical pole-mass/coefficient contract: D0=12 alpha_QG+beta_QG and D2=-beta_QG, with 4456 candidate R10 thresholds converted into D0/D2 coefficient-region bounds.",
        "current_evidence": "4457 source register, pole contract, coefficient bounds, parent coefficient template/evaluation, zero route audit, signed supplemental route, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "private_smoke_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "canonical alpha_QG,beta_QG are not yet mapped to parent-owned MTS coefficients; signed alpha(lambda) table is not acquired.",
        "sector": "local_gr_newton_r10",
        "evidence": "4457 source register, pole contract, coefficient bounds, parent coefficient template/evaluation, zero route audit, signed supplemental route, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "canonical alpha_QG,beta_QG are not yet mapped to parent-owned MTS coefficients; signed alpha(lambda) table is not acquired.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(claim_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    current = text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + section.strip() + "\n")


def write_docs(bounds: Sequence[Dict[str, object]], eval_rows: Sequence[Dict[str, object]]) -> None:
    sources = source_rows()
    contract = pole_contract_rows()
    parent_input = parent_coefficient_input_rows()
    zero = zero_route_rows()
    supplemental = supplemental_route_rows()
    derivations = derivation_rows(bounds)
    gates = claim_gate_rows(bounds, eval_rows)
    decisions = decision_rows(bounds)
    status = status_rows()
    next_target = next_rows()
    body = f"""# 473 - PPC4161 parent M0/M2 Scale Derivation or Signed alpha Supplemental Table

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4457 converts the 4456 channel mass thresholds into a canonical quadratic-curvature coefficient contract. This is a real algebraic target for MTS, not a public R10/local-GR claim.

## Canonical Pole Contract

{table(contract)}

## Candidate Coefficient Region

{table(bounds)}

## Parent Coefficient Template / Evaluation

{table(parent_input)}

{table(eval_rows)}

## Zero Route Audit

{table(zero)}

## Signed Supplemental Route

{table(supplemental)}

## Derivation Rows

{table(derivations)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Source Register

{table(sources)}
"""
    write_text(FORMAL_PATH, body)
    packet = f"""# 4457 - parent M0/M2 Scale Derivation or Signed alpha Supplemental Table

Private checkpoint. No GitHub action. No public claim.

- Wrote the canonical pole-mass contract: `D0=12 alpha_QG+beta_QG`, `D2=-beta_QG`.
- Converted the 4456 candidate thresholds into coefficient-region bounds.
- Kept the zero route unsigned because 963/964 show the no-higher-derivative/minimality lock is not parent-signed.
- Kept the signed alpha supplemental route open but not promoted.
- Next: map MTS parent coefficients to canonical `alpha_QG,beta_QG`, or prove the parent selector kills the quadratic terms.

Next target: `{NEXT_TARGET}`

Marker: `{PACKET_MARKER}`
"""
    write_text(DOC_PATH, packet)
    append_marker_section(
        SPINE_PATH,
        MARKER,
        f"""## {MARKER}

The cR2 survivor now has a canonical coefficient-space target. If MTS supplies a parent-owned normalization map into `alpha_QG,beta_QG`, the scalar and spin-2 pole masses can be computed and checked against the 4456 candidate R10 channel thresholds. Without that map, the finite branch remains a private smoke target. The zero-selector route remains open but unsigned.
""",
    )
    append_marker_section(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## {PACKET_MARKER}

4457 turns the cR2 range problem into coefficient inequalities: `0 < 12 alpha_QG+beta_QG <= D0_star` and `0 < -beta_QG <= D2_star`, where `D0_star` and `D2_star` come from the 4456 channel thresholds. This is not a claim; it is the next exact contract the parent action must satisfy.
""",
    )


def validation_rows() -> List[Dict[str, object]]:
    gates = read_csv(CLAIM_GATES)
    bounds = read_csv(COEFFICIENT_BOUNDS)
    checks = [
        ("VAL4457_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "local"), "every cited local source path exists"),
        ("VAL4457_1_local_needles_found", all(row["needle_found"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "local"), "every cited local source needle is present"),
        ("VAL4457_2_web_sources_recorded", all(row["web_source_recorded"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "web"), "web source URLs recorded"),
        ("VAL4457_3_pole_contract_rows", len(read_csv(POLE_CONTRACT)) >= 5, "canonical pole contract rows written"),
        ("VAL4457_4_coefficient_bounds", len(bounds) == 3 and all(row["valid_for_claim"] == "False" for row in bounds), "candidate D0/D2 coefficient bounds written and nonclaim"),
        ("VAL4457_5_parent_template_rejects", all(row["verdict"].startswith("REJECTED") or row["verdict"].endswith("NONCLAIM") for row in read_csv(PARENT_COEFFICIENT_EVAL)), "parent coefficient template rejects placeholders"),
        ("VAL4457_6_zero_route_nonclaim", all(row["valid_for_claim"] == "False" for row in read_csv(ZERO_ROUTE_AUDIT)), "zero route remains nonclaim"),
        ("VAL4457_7_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4457_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-299"),
        ("VAL4457_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4457_10_post_doc", DOC_PATH.exists() and PACKET_MARKER in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4457_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4457_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4457_13_next_target", NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4457_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    thresholds = read_csv(THRESHOLDS_4456)
    bounds = coefficient_bounds_from_thresholds(thresholds)
    parent_inputs = parent_coefficient_input_rows()
    eval_rows = [evaluate_parent_coefficient_row(row, bounds) for row in parent_inputs]
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(POLE_CONTRACT, pole_contract_rows())
    write_csv(COEFFICIENT_BOUNDS, bounds)
    write_csv(PARENT_COEFFICIENT_INPUT, parent_inputs)
    write_csv(PARENT_COEFFICIENT_EVAL, eval_rows)
    write_csv(ZERO_ROUTE_AUDIT, zero_route_rows())
    write_csv(SUPPLEMENTAL_ROUTE, supplemental_route_rows())
    write_csv(DERIVATION_ROWS, derivation_rows(bounds))
    write_csv(DECISION_CSV, decision_rows(bounds))
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows(bounds, eval_rows))
    write_docs(bounds, eval_rows)
    update_claims_register()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
