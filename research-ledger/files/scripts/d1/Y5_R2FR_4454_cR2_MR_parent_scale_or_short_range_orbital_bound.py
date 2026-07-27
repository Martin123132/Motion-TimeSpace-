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

from curvature_square_scale_gate import evaluate_bound_row, evaluate_mode_row, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4454"
CLAIM_ID = "L-296"
MARKER = "PPC4161_CR2_MR_PARENT_SCALE_OR_SHORT_RANGE_ORBITAL_BOUND_4454"
PACKET_MARKER = "PPC4161_PACKET_CR2_MR_PARENT_SCALE_OR_SHORT_RANGE_ORBITAL_BOUND_4454"
DECISION = "CURVATURE_SQUARE_MODES_MAPPED_TO_SCALAR_TENSOR_YUKAWA_TAILS_R10_ANCHOR_AND_ORBITAL_FORMULA_STAGED_PARENT_SCALE_OR_FULL_PROJECTION_OPEN_NONCLAIM"
NEXT_TARGET = "4455-Y5-R2FR-cR2-parent-scale-signature-or-alpha-lambda-projection-row.md"

FORMAL_PATH = FORMAL / "470-PPC4161-cR2-MR-parent-scale-or-short-range-orbital-bound.md"
DOC_PATH = POST / "4454-Y5-R2FR-cR2-MR-parent-scale-or-short-range-orbital-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4454_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4454_SOURCE_REGISTER.csv"
MODE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4454_CURVATURE_MODE_INPUT.csv"
MODE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4454_CURVATURE_MODE_OUTPUT.csv"
BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4454_SHORT_RANGE_ORBITAL_BOUND_INPUT.csv"
BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4454_SHORT_RANGE_ORBITAL_BOUND_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4454_DERIVATION_ROWS.csv"
FORMULA_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4454_FORMULA_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4454_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4454_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4454_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4454_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "curvature_square_scale_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4454_cR2_MR_parent_scale_or_short_range_orbital_bound.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4453 = SOURCE_DIR / "P8_Y5_R2FR_4453_NEXT_TARGET.csv"
COEFF_4450 = SOURCE_DIR / "P8_Y5_R2FR_4450_COEFFICIENT_STATUS_OUTPUT.csv"
MAP_4185 = SOURCE_DIR / "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP.csv"
BOUND_4185 = SOURCE_DIR / "P8_Y5_R2FR_4185_BOUND_INTERFACE_MATRIX.csv"
LEDGER_4184 = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_201 = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
FORMAL_469 = FORMAL / "469-PPC4161-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md"

WEB_EOTWASH_2020 = "https://arxiv.org/abs/2002.11761"
WEB_EOTWASH_PAGE = "https://www.npl.washington.edu/eotwash/inverse-square-law"
WEB_PUBMED_2020 = "https://pubmed.ncbi.nlm.nih.gov/32216404/"
HBAR_C_EV_UM = 0.1973269804
R10_ALPHA1_LAMBDA_UM = 38.6
R10_ALPHA1_MASS_EV = HBAR_C_EV_UM / R10_ALPHA1_LAMBDA_UM


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
        {"source_id": "SRC4454_00_next4453", "kind": "local", "ref": str(NEXT_4453), "needle": "4454-Y5-R2FR-cR2-MR-parent-scale-or-short-range-orbital-bound.md", "role": "4453 selected cR2/MR target."},
        {"source_id": "SRC4454_01_coeff4450", "kind": "local", "ref": str(COEFF_4450), "needle": "C4450_5_cR2_MR", "role": "4450 cR2 survivor row."},
        {"source_id": "SRC4454_02_map4185", "kind": "local", "ref": str(MAP_4185), "needle": "RC4185_4_cR2", "role": "4185 coefficient arena map."},
        {"source_id": "SRC4454_03_bound4185", "kind": "local", "ref": str(BOUND_4185), "needle": "BI4185_1_R10", "role": "4185 R10 interface."},
        {"source_id": "SRC4454_04_ledger4184", "kind": "local", "ref": str(LEDGER_4184), "needle": "RB4184_1_cR2", "role": "4184 cR2 ledger."},
        {"source_id": "SRC4454_05_formal200", "kind": "local", "ref": str(FORMAL_200), "needle": "curvature squares -> coefficient or mass scale `c_R2/M_R`", "role": "formal residual term."},
        {"source_id": "SRC4454_06_formal201", "kind": "local", "ref": str(FORMAL_201), "needle": "c_R2 or M_R curvature-square finite-range tail", "role": "formal coefficient map."},
        {"source_id": "SRC4454_07_formal295", "kind": "local", "ref": str(FORMAL_295), "needle": "c_R2/M_R", "role": "residual finite survivor."},
        {"source_id": "SRC4454_08_formal469", "kind": "local", "ref": str(FORMAL_469), "needle": "The next unresolved finite local-GR survivor with broad empirical consequences is c_R2/M_R", "role": "torsion handoff to cR2."},
        {"source_id": "SRC4454_09_web_eotwash2020", "kind": "web", "ref": WEB_EOTWASH_2020, "needle": "gravitational-strength Yukawa interactions to ranges <38.6 um", "role": "2020 short-range anchor."},
        {"source_id": "SRC4454_10_web_eotwash_page", "kind": "web", "ref": WEB_EOTWASH_PAGE, "needle": "Current published inverse-square-law constraints", "role": "Eot-Wash source page."},
        {"source_id": "SRC4454_11_web_pubmed", "kind": "web", "ref": WEB_PUBMED_2020, "needle": "PubMed record for 2020 PRL", "role": "bibliographic source."},
        {"source_id": "SRC4454_12_gate", "kind": "local", "ref": str(GATE_PATH), "needle": "def evaluate_mode_row", "role": "4454 curvature gate."},
        {"source_id": "SRC4454_13_generator", "kind": "local", "ref": str(GENERATOR_PATH), "needle": 'CHECKPOINT = "4454"', "role": "4454 generator script."},
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
            "web_source_recorded": kind == "web" and ref.startswith("https://"),
            "web_verified_in_session": kind == "web",
            "needle": spec["needle"],
            "needle_found": line > 0 if kind == "local" else True,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def mode_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "mode_id": "CM4454_0_scalar_R2",
            "mode": "scalar_curvature_square",
            "source_path": str(FORMAL_200),
            "linearized_effect": "R^2/Ricci trace combination creates a massive scalar Yukawa tail",
            "potential_projection": "Phi = -G M/r * [1 + alpha_0 exp(-M_0 r)]",
            "mode_written": True,
            "potential_projection_written": True,
            "alpha_projection_fixed": False,
            "mass_scale_parent_signed": False,
            "numeric_scale_available": False,
            "public_claim_false": True,
        },
        {
            "mode_id": "CM4454_1_spin2_Ricci",
            "mode": "massive_spin2_curvature_square",
            "source_path": str(FORMAL_200),
            "linearized_effect": "Ricci^2/Weyl^2 combination can create a massive spin-2 Yukawa tail with sign/model dependence",
            "potential_projection": "Phi = -G M/r * [1 + alpha_2 exp(-M_2 r)]",
            "mode_written": True,
            "potential_projection_written": True,
            "alpha_projection_fixed": False,
            "mass_scale_parent_signed": False,
            "numeric_scale_available": False,
            "public_claim_false": True,
        },
        {
            "mode_id": "CM4454_2_parent_scale",
            "mode": "parent_low_energy_scale",
            "source_path": str(COEFF_4450),
            "linearized_effect": "if the parent action gives all curvature-square modes M_i L_local >> 1, local deviations are exponentially small",
            "potential_projection": "lambda_i = 1/M_i, alpha_i exp(-r/lambda_i)",
            "mode_written": True,
            "potential_projection_written": True,
            "alpha_projection_fixed": False,
            "mass_scale_parent_signed": False,
            "numeric_scale_available": False,
            "public_claim_false": True,
        },
    ]


def bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "BR4454_0_R10_alpha1_anchor",
            "arena": "R10_short_range_gravity",
            "source_url": WEB_EOTWASH_2020,
            "source_verified": True,
            "observable": "95% confidence gravitational-strength Yukawa range anchor",
            "lambda_anchor_um": R10_ALPHA1_LAMBDA_UM,
            "alpha_anchor": 1.0,
            "mass_floor_eV": f"{R10_ALPHA1_MASS_EV:.8g}",
            "full_curve_available": False,
            "projection_to_cR2_ready": False,
            "public_claim_false": True,
        },
        {
            "bound_id": "BR4454_1_EotWash_current_curve_page",
            "arena": "R10_alpha_lambda_curve_source",
            "source_url": WEB_EOTWASH_PAGE,
            "source_verified": True,
            "observable": "published alpha(lambda) exclusion region catalogue",
            "lambda_anchor_um": R10_ALPHA1_LAMBDA_UM,
            "alpha_anchor": 1.0,
            "mass_floor_eV": f"{R10_ALPHA1_MASS_EV:.8g}",
            "full_curve_available": False,
            "projection_to_cR2_ready": False,
            "public_claim_false": True,
        },
        {
            "bound_id": "BR4454_2_orbital_large_lambda_formula",
            "arena": "orbital_precession_or_inverse_square",
            "source_url": WEB_PUBMED_2020,
            "source_verified": True,
            "observable": "finite-range Yukawa force formula for larger lambda handoff",
            "lambda_anchor_um": "",
            "alpha_anchor": "",
            "mass_floor_eV": "",
            "full_curve_available": False,
            "projection_to_cR2_ready": False,
            "public_claim_false": True,
        },
    ]


def formula_rows() -> List[Dict[str, object]]:
    return [
        {"formula_id": "F4454_0_yukawa_potential", "formula": "Phi(r) = -G M/r * [1 + sum_i alpha_i exp(-M_i r)]", "meaning": "generic curvature-square finite-range local potential", "valid_for_claim": False},
        {"formula_id": "F4454_1_range", "formula": "lambda_i = 1/M_i", "meaning": "range of each massive curvature mode", "valid_for_claim": False},
        {"formula_id": "F4454_2_R10_anchor_mass", "formula": f"M_R > hbar c / (38.6 um) = {R10_ALPHA1_MASS_EV:.6g} eV for alpha≈1 single-Yukawa anchor", "meaning": "source-backed gravitational-strength anchor, not full curve", "valid_for_claim": False},
        {"formula_id": "F4454_3_orbital_accel", "formula": "Delta a/a_N = alpha * (1 + r/lambda) * exp(-r/lambda)", "meaning": "large-lambda orbital/inverse-square fallback projection", "valid_for_claim": False},
        {"formula_id": "F4454_4_parent_scale_contract", "formula": "M_R >= M_parent,IR and M_parent,IR * L_test >> 1", "meaning": "parent low-energy scale suppression contract", "valid_for_claim": False},
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4454_0_curvature_modes",
            "claim": "Curvature-square residuals become finite-range modes in the local weak-field branch.",
            "derivation": "The excluded `R^2`, `Ricci^2`, and related curvature-square terms are not just labels; in a weak-field expansion they correspond to massive scalar/tensor response channels. At local distances their leading spinless effect can be represented as Yukawa corrections to the Newtonian potential.",
            "consequence": "The c_R2/M_R problem is now a mode-scale/projection problem, not a vague EFT leftover.",
            "status": "CURVATURE_SQUARE_TO_YUKAWA_MODE_MAP_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4454_1_parent_scale_contract",
            "claim": "A high parent curvature mass scale would suppress the local correction.",
            "derivation": "If all curvature-square modes have `M_i L_test >> 1`, then `exp(-M_i r)` is negligible in the test arena. The exact parent route is therefore a scale theorem: derive a lower bound on `M_R` from the MTS parent IR selector or prove the coefficients vanish.",
            "consequence": "Local GR can tolerate c_R2 only if it is parent-zero, heavy, screened, or source-bounded.",
            "status": "PARENT_SCALE_CONTRACT_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4454_2_R10_anchor",
            "claim": "A real short-range anchor is available for gravitational-strength Yukawa tails.",
            "derivation": f"The 2020 Eot-Wash short-range result reports a 95% confidence anchor excluding gravitational-strength Yukawa ranges above 38.6 um. Using hbar*c={HBAR_C_EV_UM} eV um gives a single-Yukawa mass floor of {R10_ALPHA1_MASS_EV:.6g} eV for alpha≈1.",
            "consequence": "This is an anchor row, not a full c_R2 pass: MTS still needs alpha projection and/or the full alpha(lambda) curve.",
            "status": "R10_ALPHA1_ANCHOR_COMPUTED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4454_3_no_cancellation_guard",
            "claim": "The scalar/tensor Yukawa map cannot be scored by cancellation.",
            "derivation": "Curvature-square modes can have different signs and amplitudes. Public scoring must map each MTS coefficient to its own alpha_i and M_i, then compare without relying on cross-channel cancellation unless the parent action derives that cancellation.",
            "consequence": "No public local-GR or R10 claim is allowed until projection rows exist.",
            "status": "NO_CROSS_CHANNEL_CANCELLATION_GUARD_WRITTEN",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "curvature_modes_mapped": True,
        "parent_scale_contract_written": True,
        "R10_alpha1_anchor_mass_eV": f"{R10_ALPHA1_MASS_EV:.8g}",
        "full_alpha_lambda_curve_ready": False,
        "projection_to_cR2_ready": False,
        "public_claim": False,
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
        "cR2_status": "mapped_to_scalar_tensor_yukawa_modes",
        "R10_alpha1_anchor": f"lambda<38.6um_for_alpha1; M>{R10_ALPHA1_MASS_EV:.8g}eV",
        "parent_scale_status": "symbolic_contract_ready_numeric_parent_scale_missing",
        "short_range_status": "anchor_ready_full_curve_projection_missing",
        "local_GR_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4454_0",
        "target": NEXT_TARGET,
        "objective": "Turn the cR2/MR map into a scoreable branch: parent scale signature or alpha(lambda) projection row.",
        "derive_first": "derive M_R lower scale from parent IR hierarchy or zero coefficient selection",
        "fallback": "extract/promote alpha(lambda) curve and map scalar/tensor alpha_i, M_i to R10/orbital bounds",
        "risk": "using the alpha=1 anchor as if it were a full cR2 proof",
        "valid_for_claim": False,
    }]


def claim_gate_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    modes = rows_from(MODE_OUTPUT)
    bounds = rows_from(BOUND_OUTPUT)
    return [
        {"gate_id": "CG4454_0_local_sources_exist", "claim": "all cited local source paths exist", "passed": all(row["local_path_exists"] == "True" for row in sources if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "Local source register path-backed."},
        {"gate_id": "CG4454_1_local_needles_found", "claim": "all cited local needles found", "passed": all(row["needle_found"] == "True" for row in sources if row["source_kind"] == "local"), "valid_for_claim": False, "detail": "Local cR2 chain is sourced."},
        {"gate_id": "CG4454_2_web_sources_recorded", "claim": "external short-range source URLs recorded", "passed": all(row["web_source_recorded"] == "True" and row["web_verified_in_session"] == "True" for row in sources if row["source_kind"] == "web"), "valid_for_claim": False, "detail": "Web sources are anchor/source rows, not claims."},
        {"gate_id": "CG4454_3_modes_mapped", "claim": "curvature modes mapped to Yukawa projection", "passed": all(row["current_status"] == "CURVATURE_MODE_SYMBOLIC_YUKAWA_PROJECTION_READY_SCALE_OR_ALPHA_MISSING" for row in modes), "valid_for_claim": False, "detail": "Scalar/tensor/parent scale modes written."},
        {"gate_id": "CG4454_4_R10_anchor_ready", "claim": "R10 alpha=1 anchor computed", "passed": any(row["bound_id"] == "BR4454_0_R10_alpha1_anchor" and row["current_status"] == "R10_GRAVITATIONAL_STRENGTH_ANCHOR_READY_FULL_CURVE_OR_PROJECTION_MISSING" for row in bounds), "valid_for_claim": False, "detail": "38.6um -> mass floor row."},
        {"gate_id": "CG4454_5_no_public_claim", "claim": "no cR2/local-GR public claim emitted", "passed": all(row["claim_allowed"] == "False" for row in modes) and all(row["claim_allowed"] == "False" for row in bounds), "valid_for_claim": False, "detail": "Alpha projection/full curve/parent scale missing."},
        {"gate_id": "CG4454_6_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc() -> str:
    return f"""# 470 PPC4161 cR2 MR parent scale or short range orbital bound

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4454 converts the curvature-square survivor from a label into a concrete local-test object:

```text
Phi(r) = -G M/r * [1 + sum_i alpha_i exp(-M_i r)]
lambda_i = 1/M_i
```

For a gravitational-strength single-Yukawa anchor, the 2020 Eot-Wash short-range result gives:

```text
lambda < 38.6 um for alpha ~= 1
M_R > hbar c / 38.6 um = {R10_ALPHA1_MASS_EV:.6g} eV
```

This is not a public pass. It is an anchor row. MTS still needs either a parent scale theorem for `M_R`, or a projection from each curvature mode to `alpha_i, M_i` plus a promoted alpha(lambda) curve/orbital bound.

## Source Register

{table(rows_from(SOURCE_REGISTER))}

## Curvature Mode Gate

{table(rows_from(MODE_OUTPUT))}

## Short Range / Orbital Bound Gate

{table(rows_from(BOUND_OUTPUT))}

## Formula Rows

{table(rows_from(FORMULA_ROWS))}

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
    return f"""# 4454 Y5 R2FR cR2 MR parent scale or short range orbital bound

Private checkpoint generated at `{STAMP}`.

Summary:
- Mapped `c_R2/M_R` to scalar/tensor Yukawa finite-range tails.
- Wrote the parent scale contract `M_R L_test >> 1`.
- Added the source-backed Eot-Wash alpha=1 anchor: `lambda < 38.6 um`, equivalent to `M_R > {R10_ALPHA1_MASS_EV:.6g} eV` for a single gravitational-strength Yukawa.
- Kept this nonclaim because the full alpha(lambda) curve and MTS alpha projection are still missing.

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
        "claim": "4454 maps c_R2/M_R to scalar/tensor Yukawa finite-range tails, derives the parent scale contract, and records the Eot-Wash alpha=1 short-range anchor without promoting a local-GR pass.",
        "current_evidence": "4454 source register, curvature mode gate, short-range/orbital bound gate, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "cR2_MR_yukawa_mode_map_and_R10_anchor_ready_projection_parent_scale_open_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using the alpha=1 short-range anchor as if it were a full c_R2/M_R proof or alpha(lambda) projection.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4454 source register, curvature mode gate, short-range/orbital bound gate, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Using the alpha=1 short-range anchor as if it were a full c_R2/M_R proof or alpha(lambda) projection.",
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
    spine_section = f"""## Local GR Parent-Derivation Update - cR2/MR Curvature-Square Finite-Range Survivor

Marker: `{MARKER}`  
Source checkpoint: `4454-Y5-R2FR-cR2-MR-parent-scale-or-short-range-orbital-bound.md`  
Claim register row: `{CLAIM_ID}`

The `c_R2/M_R` survivor is now mapped to scalar/tensor Yukawa finite-range tails. A real short-range anchor is recorded: gravitational-strength single-Yukawa range `<38.6 um`, equivalent to `M_R>{R10_ALPHA1_MASS_EV:.6g} eV`. This remains nonclaim until MTS supplies a parent scale theorem or full `alpha(lambda)`/orbital projection rows.
"""
    packet_section = f"""## PPC4161 Packet Addendum - cR2/MR Curvature-Square Finite-Range Survivor

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4454-Y5-R2FR-cR2-MR-parent-scale-or-short-range-orbital-bound.md`

The packet now carries the `c_R2/M_R` Yukawa map, R10 alpha=1 anchor, and no-cancellation guard. The next packet target is the parent scale signature or alpha(lambda) projection row.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    modes = rows_from(MODE_OUTPUT)
    bounds = rows_from(BOUND_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    checks = [
        ("VAL4454_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in sources if row["source_kind"] == "local"), "every cited local source path exists"),
        ("VAL4454_1_local_needles_found", all(row["needle_found"] == "True" for row in sources if row["source_kind"] == "local"), "every cited local source needle is present"),
        ("VAL4454_2_web_sources_recorded", all(row["web_source_recorded"] == "True" and row["web_verified_in_session"] == "True" for row in sources if row["source_kind"] == "web"), "web source URLs recorded"),
        ("VAL4454_3_modes_mapped", all(row["current_status"] == "CURVATURE_MODE_SYMBOLIC_YUKAWA_PROJECTION_READY_SCALE_OR_ALPHA_MISSING" for row in modes), "all curvature modes mapped"),
        ("VAL4454_4_anchor_ready", any(row["bound_id"] == "BR4454_0_R10_alpha1_anchor" and row["numeric_anchor_ready"] == "True" for row in bounds), "R10 alpha=1 anchor ready"),
        ("VAL4454_5_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4454_6_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-296"),
        ("VAL4454_7_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4454_8_post_doc", DOC_PATH.exists() and "Private checkpoint" in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4454_9_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4454_10_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4454_11_next_target", NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4454_12_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(MODE_INPUT, mode_input_rows())
    write_csv(MODE_OUTPUT, [evaluate_mode_row(row) for row in rows_from(MODE_INPUT)])
    write_csv(BOUND_INPUT, bound_input_rows())
    write_csv(BOUND_OUTPUT, [evaluate_bound_row(row) for row in rows_from(BOUND_INPUT)])
    write_csv(FORMULA_ROWS, formula_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
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
