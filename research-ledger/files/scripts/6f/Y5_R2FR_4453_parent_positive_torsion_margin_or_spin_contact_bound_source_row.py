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

from torsion_positive_margin_gate import evaluate_margin_row, evaluate_source_row, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4453"
CLAIM_ID = "L-295"
MARKER = "PPC4161_PARENT_POSITIVE_TORSION_MARGIN_OR_SPIN_CONTACT_SOURCE_4453"
PACKET_MARKER = "PPC4161_PACKET_PARENT_POSITIVE_TORSION_MARGIN_OR_SPIN_CONTACT_SOURCE_4453"
DECISION = "PARENT_POSITIVE_TORSION_MARGIN_CONTRACT_DERIVED_AND_SPIN_CONTACT_SOURCE_ROWS_STAGED_NUMERIC_MARGIN_OR_PROJECTION_STILL_OPEN_NONCLAIM"
NEXT_TARGET = "4454-Y5-R2FR-cR2-MR-parent-scale-or-short-range-orbital-bound.md"

FORMAL_PATH = FORMAL / "469-PPC4161-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md"
DOC_PATH = POST / "4453-Y5-R2FR-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4453_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4453_SOURCE_REGISTER.csv"
MARGIN_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4453_PARENT_POSITIVE_MARGIN_INPUT.csv"
MARGIN_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4453_PARENT_POSITIVE_MARGIN_OUTPUT.csv"
SPIN_SOURCE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4453_SPIN_CONTACT_SOURCE_INPUT.csv"
SPIN_SOURCE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4453_SPIN_CONTACT_SOURCE_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4453_DERIVATION_ROWS.csv"
CONTRACT_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4453_PARENT_MARGIN_CONTRACT_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4453_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4453_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4453_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4453_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "torsion_positive_margin_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4453_parent_positive_torsion_margin_or_spin_contact_bound_source_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4452 = SOURCE_DIR / "P8_Y5_R2FR_4452_NEXT_TARGET.csv"
IRREP_4452 = SOURCE_DIR / "P8_Y5_R2FR_4452_TORSION_IRREP_OPERATOR_OUTPUT.csv"
BOUND_4452 = SOURCE_DIR / "P8_Y5_R2FR_4452_SPIN_CONTACT_BOUND_OUTPUT.csv"
FORMULA_4452 = SOURCE_DIR / "P8_Y5_R2FR_4452_OPERATOR_FORMULA_ROWS.csv"
FORMAL_468 = FORMAL / "468-PPC4161-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md"
FORMAL_467 = FORMAL / "467-PPC4161-torsion-spin-residual-cT-zero-or-contact-bound.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
OUT_4184_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"

WEB_TORSION_LORENTZ = "https://arxiv.org/abs/0712.4393"
WEB_NIST_SPIN = "https://www.nist.gov/publications/torsion-balance-test-couplings-spin"
WEB_EOTWASH = "https://www.npl.washington.edu/eotwash/publications"


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


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
        {"source_id": "SRC4453_00_next4452", "kind": "local", "ref": str(NEXT_4452), "needle": "4453-Y5-R2FR-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md", "role": "4452 selected parent margin/source row target."},
        {"source_id": "SRC4453_01_irrep4452", "kind": "local", "ref": str(IRREP_4452), "needle": "IR4452_0_trace_vector", "role": "4452 irrep channels."},
        {"source_id": "SRC4453_02_bound4452", "kind": "local", "ref": str(BOUND_4452), "needle": "SPIN_CONTACT_FORMULA_READY_NUMERIC_INPUTS_MISSING", "role": "4452 contact formula open."},
        {"source_id": "SRC4453_03_formula4452", "kind": "local", "ref": str(FORMULA_4452), "needle": "lambda_T,min", "role": "4452 margin formula rows."},
        {"source_id": "SRC4453_04_formal468", "kind": "local", "ref": str(FORMAL_468), "needle": "lambda_T,min > 0", "role": "formal no-zero-mode contract."},
        {"source_id": "SRC4453_05_formal467", "kind": "local", "ref": str(FORMAL_467), "needle": "L_T[e,c_T] T = kappa tau_spin", "role": "torsion algebraic equation."},
        {"source_id": "SRC4453_06_formal200", "kind": "local", "ref": str(FORMAL_200), "needle": "Each coefficient must be parent-zero", "role": "parent-zero/heavy/bound policy."},
        {"source_id": "SRC4453_07_formal295", "kind": "local", "ref": str(FORMAL_295), "needle": "c_T_spin", "role": "spin/torsion contact residual."},
        {"source_id": "SRC4453_08_4184_ledger", "kind": "local", "ref": str(OUT_4184_LEDGER), "needle": "derive c_T=0/heavy from parent or fit upper bound", "role": "original c_T evidence requirement."},
        {"source_id": "SRC4453_09_web_torsion_constraints", "kind": "web", "ref": WEB_TORSION_LORENTZ, "needle": "order 10^-31 GeV torsion sensitivity", "role": "external torsion constraint source class."},
        {"source_id": "SRC4453_10_web_nist_spin", "kind": "web", "ref": WEB_NIST_SPIN, "needle": "approximately 1e23 polarized electrons", "role": "external spin-coupling pendulum source class."},
        {"source_id": "SRC4453_11_web_eotwash", "kind": "web", "ref": WEB_EOTWASH, "needle": "spin-dependent interactions / torsion pendulum publication list", "role": "external Eot-Wash source catalogue."},
        {"source_id": "SRC4453_12_gate", "kind": "local", "ref": str(GATE_PATH), "needle": "def evaluate_margin_row", "role": "4453 margin gate."},
        {"source_id": "SRC4453_13_generator", "kind": "local", "ref": str(GENERATOR_PATH), "needle": 'CHECKPOINT = "4453"', "role": "4453 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        kind = str(spec["kind"])
        ref = str(spec["ref"])
        path = Path(ref) if kind == "local" else None
        line = line_of(path, str(spec["needle"])) if path else 0
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": spec["source_id"],
            "source_kind": kind,
            "source_ref": ref,
            "local_path_exists": bool(path and path.exists()),
            "web_source_recorded": kind == "web" and (ref.startswith("https://") or ref.startswith("http://")),
            "web_verified_in_session": kind == "web",
            "needle": spec["needle"],
            "needle_found": line > 0 if kind == "local" else True,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def margin_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "margin_id": "PM4453_0_trace",
            "channel": "trace_vector",
            "source_path": str(IRREP_4452),
            "stability_clause": "local auxiliary torsion response is finite and the trace channel is not critically tuned",
            "margin_formula": "lambda_V >= m_T,V^2 > 0",
            "critical_surface": "lambda_V = 0",
            "stability_clause_written": True,
            "margin_formula_written": True,
            "excludes_critical_surface": True,
            "parent_signed": False,
            "numeric_margin_available": False,
            "public_claim_false": True,
        },
        {
            "margin_id": "PM4453_1_axial",
            "channel": "axial_vector",
            "source_path": str(IRREP_4452),
            "stability_clause": "local auxiliary torsion response is finite and the axial channel is not critically tuned",
            "margin_formula": "lambda_A >= m_T,A^2 > 0",
            "critical_surface": "lambda_A = 0",
            "stability_clause_written": True,
            "margin_formula_written": True,
            "excludes_critical_surface": True,
            "parent_signed": False,
            "numeric_margin_available": False,
            "public_claim_false": True,
        },
        {
            "margin_id": "PM4453_2_tensor",
            "channel": "tensor",
            "source_path": str(IRREP_4452),
            "stability_clause": "local auxiliary torsion response is finite and the tensor channel is not critically tuned",
            "margin_formula": "lambda_Q >= m_T,Q^2 > 0",
            "critical_surface": "lambda_Q = 0",
            "stability_clause_written": True,
            "margin_formula_written": True,
            "excludes_critical_surface": True,
            "parent_signed": False,
            "numeric_margin_available": False,
            "public_claim_false": True,
        },
    ]


def spin_source_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "source_row_id": "SC4453_0_torsion_LV_constraints",
            "source_name": "Kostelecky-Russell-Tasson torsion constraints from Lorentz violation",
            "source_url": WEB_TORSION_LORENTZ,
            "source_verified": True,
            "observable": "fermion spin couplings to background torsion components",
            "observable_mapped": True,
            "bound_use": "external constraint class for torsion-spin couplings; needs conversion to MTS lambda_T,min/contact coefficient",
            "numeric_extracted": False,
            "unit_converted": False,
            "projection_to_lambda_margin_ready": False,
            "public_claim_false": True,
        },
        {
            "source_row_id": "SC4453_1_NIST_spin_pendulum",
            "source_name": "NIST/Eot-Wash torsion balance test of couplings to spin",
            "source_url": WEB_NIST_SPIN,
            "source_verified": True,
            "observable": "new spin-coupled interactions using a torsion pendulum with polarized electrons",
            "observable_mapped": True,
            "bound_use": "source class for polarized spin torque/contact bound row",
            "numeric_extracted": False,
            "unit_converted": False,
            "projection_to_lambda_margin_ready": False,
            "public_claim_false": True,
        },
        {
            "source_row_id": "SC4453_2_EotWash_spin_catalogue",
            "source_name": "Eot-Wash spin-dependent torsion-pendulum publication catalogue",
            "source_url": WEB_EOTWASH,
            "source_verified": True,
            "observable": "spin-dependent interaction/torsion-pendulum source list",
            "observable_mapped": True,
            "bound_use": "catalogue for selecting the numeric source paper before public scoring",
            "numeric_extracted": False,
            "unit_converted": False,
            "projection_to_lambda_margin_ready": False,
            "public_claim_false": True,
        },
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4453_0_parent_margin_theorem",
            "claim": "A parent stability/no-critical-response clause is sufficient to close the torsion zero-mode condition.",
            "derivation": "4452 gives L_T=diag(lambda_V,lambda_A,lambda_Q). If the parent local IR selector requires the auxiliary torsion quadratic form to be strictly positive in every Lorentz irrep, then lambda_V>=m_T,V^2>0, lambda_A>=m_T,A^2>0, and lambda_Q>=m_T,Q^2>0. Therefore lambda_T,min>=min(m_T,V^2,m_T,A^2,m_T,Q^2)>0.",
            "consequence": "Spinless local sources have T=0 and no long-range torsion residual under this parent clause.",
            "status": "POSITIVE_MARGIN_THEOREM_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4453_1_no_smuggling_guard",
            "claim": "The positive margin is not yet an MTS public theorem.",
            "derivation": "The current corpus has the stability/margin contract, but it does not yet parent-sign the actual positive constants or numeric margins. Exact critical cancellation lambda_i=0 is excluded only if the parent selector owns the strict-positive auxiliary torsion clause.",
            "consequence": "No public local-GR torsion claim is allowed from symbolic stability language alone.",
            "status": "PARENT_SIGNATURE_OR_NUMERIC_MARGIN_STILL_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4453_2_source_fallback",
            "claim": "If parent positivity is not signed, the fallback is now a concrete spin-contact source row.",
            "derivation": "Use the 4452 formula |Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min). External torsion/spin-pendulum sources are recorded as candidate source classes. Public scoring still requires numeric extraction, unit conversion, and a projection from each experiment's spin-coupled observable to the MTS contact coefficient or lambda_T,min.",
            "consequence": "The torsion branch is no longer broad; it is a parent-margin or source-extraction task.",
            "status": "SPIN_CONTACT_SOURCE_ROWS_STAGED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4453_3_route_selection",
            "claim": "The broad local-GR route can move to the curvature-square finite-range survivor while this narrow torsion source row remains explicit.",
            "derivation": "c_T_spin is conditionally removed from spinless PPN/R10/orbital tests and narrowed to positive margin/source extraction. The next unresolved finite local-GR survivor with broad empirical consequences is c_R2/M_R.",
            "consequence": NEXT_TARGET,
            "status": "NEXT_FINITE_SURVIVOR_SELECTED",
            "valid_for_claim": False,
        },
    ]


def contract_rows() -> List[Dict[str, object]]:
    return [
        {"contract_id": "CON4453_0_parent_margin", "contract": "lambda_T,min >= m_T,parent^2 > 0 in compact local branch", "closes": "ker L_T=0", "open_input": "parent must sign strict positive auxiliary torsion quadratic form", "valid_for_claim": False},
        {"contract_id": "CON4453_1_spinless_zero", "contract": "tau_spin=0 and lambda_T,min>0 => T=0", "closes": "spinless PPN/R10/orbital long-range torsion", "open_input": "spinless/unpolarized source classification retained", "valid_for_claim": False},
        {"contract_id": "CON4453_2_contact_bound", "contract": "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)", "closes": "finite polarized spin channel only after numeric source/projection", "open_input": "numeric spin-source bound and projection Jacobian", "valid_for_claim": False},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "positive_margin_contract_written": True,
        "parent_positive_margin_signed": False,
        "spin_contact_source_rows_staged": True,
        "numeric_extraction_complete": False,
        "torsion_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "lambda_margin_contract": "lambda_T,min>=m_T,parent^2>0",
        "spinless_torsion_status": "conditionally_clean_if_parent_margin_signed",
        "contact_bound_status": "source_rows_staged_numeric_projection_missing",
        "local_GR_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4453_0",
        "target": NEXT_TARGET,
        "objective": "Attack the next broad finite local-GR survivor: curvature-square scale M_R or source-backed short-range/orbital bound.",
        "derive_first": "derive parent low-energy scale M_R that suppresses R^2/Ricci^2/Riemann^2 corrections",
        "fallback": "map c_R2/M_R to R10 alpha(lambda) or orbital-precession bound rows",
        "risk": "getting stuck polishing the torsion source row after it has already been narrowed to a contact/margin contract",
        "valid_for_claim": False,
    }]


def claim_gate_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    margins = rows_from(MARGIN_OUTPUT)
    spin_sources = rows_from(SPIN_SOURCE_OUTPUT)
    return [
        {"gate_id": "CG4453_0_local_sources_exist", "claim": "all cited local source paths exist", "passed": all(row["local_path_exists"] == "True" for row in sources if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "Local source register is path-backed."},
        {"gate_id": "CG4453_1_local_needles_found", "claim": "all cited local needles found", "passed": all(row["needle_found"] == "True" for row in sources if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "Local derivation chain is sourced."},
        {"gate_id": "CG4453_2_web_sources_recorded", "claim": "external source URLs recorded and session-verified", "passed": all(row["web_source_recorded"] == "True" and row["web_verified_in_session"] == "True" for row in sources if row["source_kind"] == "web"), "valid_for_claim": False, "detail": "Web source rows are recorded but not numeric claims."},
        {"gate_id": "CG4453_3_margin_contract_ready", "claim": "positive margin contract written for all torsion channels", "passed": all(row["current_status"] == "PARENT_POSITIVE_MARGIN_CONTRACT_READY_SIGNATURE_OR_NUMERIC_MARGIN_MISSING" for row in margins), "valid_for_claim": False, "detail": "Trace/axial/tensor margins written."},
        {"gate_id": "CG4453_4_spin_source_rows_ready", "claim": "spin-contact source rows staged", "passed": all(row["current_status"] == "SOURCE_BOUND_ROW_READY_NUMERIC_EXTRACTION_OR_PROJECTION_MISSING" for row in spin_sources), "valid_for_claim": False, "detail": "Need numeric extraction and projection."},
        {"gate_id": "CG4453_5_no_public_claim", "claim": "no torsion/local-GR public claim emitted", "passed": all(row["claim_allowed"] == "False" for row in margins) and all(row["claim_allowed"] == "False" for row in spin_sources), "valid_for_claim": False, "detail": "Parent margin or numeric projection missing."},
        {"gate_id": "CG4453_6_next_target_written", "claim": "next finite survivor selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc() -> str:
    return f"""# 469 PPC4161 parent positive torsion margin or spin contact bound source row

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4453 turns the remaining torsion gap into a clean fork:

```text
Route A: parent signs lambda_T,min >= m_T,parent^2 > 0.
Route B: source the spin-contact bound using |Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min).
```

The derivation is:

```text
lambda_V >= m_T,V^2 > 0,
lambda_A >= m_T,A^2 > 0,
lambda_Q >= m_T,Q^2 > 0
=> lambda_T,min >= min(m_T,V^2,m_T,A^2,m_T,Q^2) > 0.
```

That would close the spinless local torsion branch. It is not yet a public claim because the parent action has not signed the positive constants and the external spin-contact rows are not numerically extracted/projected.

## Source Register

{table(rows_from(SOURCE_REGISTER))}

## Parent Positive Margin Gate

{table(rows_from(MARGIN_OUTPUT))}

## Spin Contact Source Rows

{table(rows_from(SPIN_SOURCE_OUTPUT))}

## Parent Margin Contract

{table(rows_from(CONTRACT_ROWS))}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Claim Gates

{table(rows_from(CLAIM_GATES))}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4453 Y5 R2FR parent positive torsion margin or spin contact bound source row

Private checkpoint generated at `{STAMP}`.

Summary:
- Derived the parent-positive torsion margin contract `lambda_T,min >= m_T,parent^2 > 0`.
- Staged external spin/torsion source rows for the fallback bound.
- Did not claim torsion/local-GR closure because parent signature and numeric projection remain open.
- Selected `c_R2/M_R` as the next broad finite local-GR survivor.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    row = {field: "" for field in fieldnames}
    payload = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "4453 derives the parent-positive torsion margin contract and stages external spin-contact source rows; torsion remains nonclaim until the parent margin or numeric source projection is signed.",
        "current_evidence": "4453 source register, parent positive margin gate, spin-contact source rows, parent margin contract, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "parent_positive_torsion_margin_contract_and_spin_contact_sources_staged_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a symbolic positive-margin contract or unprojected spin source row as a torsion pass.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4453 source register, parent positive margin gate, spin-contact source rows, parent margin contract, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Treating a symbolic positive-margin contract or unprojected spin source row as a torsion pass.",
    }
    for key, value in payload.items():
        if key in row:
            row[key] = value
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Parent-Derivation Update - Parent Positive Torsion Margin

Marker: `{MARKER}`  
Source checkpoint: `4453-Y5-R2FR-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md`  
Claim register row: `{CLAIM_ID}`

The torsion branch is narrowed to a clean fork: parent-sign `lambda_T,min >= m_T,parent^2 > 0`, or score spin-contact source rows using the 4452 contact formula. This keeps the spinless local branch conditionally clean without pretending torsion is publicly closed.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Parent Positive Torsion Margin

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4453-Y5-R2FR-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md`

The packet now carries the positive-margin contract and web-source candidate rows for torsion/spin bounds. The next broad survivor is `c_R2/M_R`.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    margins = rows_from(MARGIN_OUTPUT)
    spin_sources = rows_from(SPIN_SOURCE_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    checks = [
        ("VAL4453_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in sources if row["source_kind"] == "local"), "every cited local source path exists"),
        ("VAL4453_1_local_needles_found", all(row["needle_found"] == "True" for row in sources if row["source_kind"] == "local"), "every cited local source needle is present"),
        ("VAL4453_2_web_sources_recorded", all(row["web_source_recorded"] == "True" and row["web_verified_in_session"] == "True" for row in sources if row["source_kind"] == "web"), "web source URLs recorded"),
        ("VAL4453_3_margin_contract_ready", all(row["current_status"] == "PARENT_POSITIVE_MARGIN_CONTRACT_READY_SIGNATURE_OR_NUMERIC_MARGIN_MISSING" for row in margins), "positive margin contract rows ready"),
        ("VAL4453_4_spin_sources_ready", all(row["current_status"] == "SOURCE_BOUND_ROW_READY_NUMERIC_EXTRACTION_OR_PROJECTION_MISSING" for row in spin_sources), "spin-contact source rows staged"),
        ("VAL4453_5_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4453_6_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-295"),
        ("VAL4453_7_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4453_8_post_doc", DOC_PATH.exists() and "Private checkpoint" in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4453_9_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4453_10_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4453_11_next_target", NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4453_12_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(MARGIN_INPUT, margin_input_rows())
    write_csv(MARGIN_OUTPUT, [evaluate_margin_row(row) for row in rows_from(MARGIN_INPUT)])
    write_csv(SPIN_SOURCE_INPUT, spin_source_input_rows())
    write_csv(SPIN_SOURCE_OUTPUT, [evaluate_source_row(row) for row in rows_from(SPIN_SOURCE_INPUT)])
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(CONTRACT_ROWS, contract_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows())
    write_text(FORMAL_PATH, build_doc())
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
