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

from quadratic_basis_normalization_gate import (  # noqa: E402
    basis_map_rows,
    coefficient_region_rows,
    evaluate_parent_basis_row,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4458"
CLAIM_ID = "L-300"
MARKER = "PPC4161_MTS_QUADRATIC_COEFFICIENT_NORMALIZATION_MAP_OR_CR2_ZERO_SELECTOR_4458"
PACKET_MARKER = "PPC4161_PACKET_MTS_QUADRATIC_COEFFICIENT_NORMALIZATION_MAP_OR_CR2_ZERO_SELECTOR_4458"
DECISION = "MTS_QUADRATIC_BASIS_TO_CANONICAL_POLE_MAP_DERIVED_PARENT_VALUES_OR_ZERO_SELECTOR_STILL_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4459-Y5-R2FR-primitive-deficit-action-law-or-first-cR2-coefficient-owner-value.md"

FORMAL_PATH = FORMAL / "474-PPC4161-MTS-quadratic-coefficient-normalization-map-or-cR2-zero-selector.md"
DOC_PATH = POST / "4458-Y5-R2FR-MTS-quadratic-coefficient-normalization-map-or-cR2-zero-selector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4458_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4458_SOURCE_REGISTER.csv"
BASIS_MAP = SOURCE_DIR / "P8_Y5_R2FR_4458_QUADRATIC_BASIS_NORMALIZATION_MAP.csv"
REGION_MAP = SOURCE_DIR / "P8_Y5_R2FR_4458_MTS_BASIS_COEFFICIENT_REGION.csv"
PARENT_BASIS_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4458_PARENT_BASIS_INPUT_TEMPLATE.csv"
PARENT_BASIS_EVAL = SOURCE_DIR / "P8_Y5_R2FR_4458_PARENT_BASIS_EVALUATION.csv"
ZERO_SELECTOR = SOURCE_DIR / "P8_Y5_R2FR_4458_ZERO_SELECTOR_CLAUSE_GATE.csv"
GB_GUARD = SOURCE_DIR / "P8_Y5_R2FR_4458_GAUSS_BONNET_GUARD.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4458_DERIVATION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4458_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4458_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4458_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4458_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "quadratic_basis_normalization_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4458_MTS_quadratic_coefficient_normalization_map_or_cR2_zero_selector.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4457 = SOURCE_DIR / "P8_Y5_R2FR_4457_NEXT_TARGET.csv"
CONTRACT_4457 = SOURCE_DIR / "P8_Y5_R2FR_4457_CANONICAL_POLE_MASS_CONTRACT.csv"
BOUNDS_4457 = SOURCE_DIR / "P8_Y5_R2FR_4457_COEFFICIENT_REGION_BOUNDS.csv"
STATUS_4457 = SOURCE_DIR / "P8_Y5_R2FR_4457_STATUS.csv"
FORMAL_473 = FORMAL / "473-PPC4161-parent-M0-M2-scale-derivation-or-signed-alpha-supplemental-table.md"
FORMAL_201 = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
ZERO_3300 = SOURCE_DIR / "P8_Y5_R2FR_3300_CURVATURE_SQUARED_CONDITIONAL_ZERO_PROOF.csv"
VAR_3300 = SOURCE_DIR / "P8_Y5_R2FR_3300_R2_RICCI2_VARIATION_AUDIT.csv"
POT_3302 = SOURCE_DIR / "P8_Y5_R2FR_3302_NEWTON_YUKAWA_POTENTIAL_TEMPLATE.csv"
AMP_3303 = SOURCE_DIR / "P8_Y5_R2FR_3303_AMPLITUDE_IMPORT_CONTRACT.csv"
OWNER_1822 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1822_R2FR_COEFFICIENT_OWNER_ROW.csv"
HOLONOMY_1822 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1822_LINEAR_HOLONOMY_PARENT_AXIOM_ATTEMPT.csv"
DOC_964 = POST / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"


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
        {"source_id": "SRC4458_00_next4457", "kind": "local", "ref": str(NEXT_4457), "needle": "4458-Y5-R2FR-MTS-quadratic-coefficient-normalization-map-or-cR2-zero-selector.md", "role": "4457 selected normalization/zero target."},
        {"source_id": "SRC4458_01_contract4457", "kind": "local", "ref": str(CONTRACT_4457), "needle": "D0=12 alpha_QG + beta_QG", "role": "canonical pole contract."},
        {"source_id": "SRC4458_02_bounds4457", "kind": "local", "ref": str(BOUNDS_4457), "needle": "QB4457_1_spin2_D2", "role": "candidate D0/D2 bounds."},
        {"source_id": "SRC4458_03_status4457", "kind": "local", "ref": str(STATUS_4457), "needle": "candidate_D0_D2_bounds_written_MTS_normalization_missing", "role": "4457 status."},
        {"source_id": "SRC4458_04_formal473", "kind": "local", "ref": str(FORMAL_473), "needle": "D2 = -beta_QG", "role": "formal 4457 map."},
        {"source_id": "SRC4458_05_formal201", "kind": "local", "ref": str(FORMAL_201), "needle": "c_R2 or M_R curvature-square finite-range tail", "role": "formal residual coefficient label."},
        {"source_id": "SRC4458_06_formal200", "kind": "local", "ref": str(FORMAL_200), "needle": "curvature squares", "role": "Palatini selector residual family."},
        {"source_id": "SRC4458_07_zero3300", "kind": "local", "ref": str(ZERO_3300), "needle": "CZ3300_4_gauss_bonnet_guard", "role": "conditional zero and GB guard."},
        {"source_id": "SRC4458_08_var3300", "kind": "local", "ref": str(VAR_3300), "needle": "VAR3300_5_Gauss_Bonnet", "role": "operator variation guard."},
        {"source_id": "SRC4458_09_pot3302", "kind": "local", "ref": str(POT_3302), "needle": "pure_metric_quadratic_template", "role": "quadratic finite potential template."},
        {"source_id": "SRC4458_10_amp3303", "kind": "local", "ref": str(AMP_3303), "needle": "AIC3303_3_canonical_mode_normalization", "role": "amplitude import blocker."},
        {"source_id": "SRC4458_11_owner1822", "kind": "local", "ref": str(OWNER_1822), "needle": "CO1822_1_visible_c2", "role": "coefficient-owner row."},
        {"source_id": "SRC4458_12_holonomy1822", "kind": "local", "ref": str(HOLONOMY_1822), "needle": "LHA1822_4_deficit_action_law", "role": "best zero-selector proof route."},
        {"source_id": "SRC4458_13_doc964", "kind": "local", "ref": str(DOC_964), "needle": "EH + epsilon int sqrt(-g) R^2", "role": "countermodel against easy zero."},
        {"source_id": "SRC4458_14_gate", "kind": "local", "ref": str(GATE_PATH), "needle": "def basis_map_rows", "role": "4458 normalization gate."},
        {"source_id": "SRC4458_15_generator", "kind": "local", "ref": str(GENERATOR_PATH), "needle": 'CHECKPOINT = "4458"', "role": "4458 generator script."},
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
                "needle": spec["needle"],
                "needle_found": line > 0 if kind == "local" else True,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def parent_basis_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "candidate_id": "PB4458_0_required_parent_basis_row",
            "c_R2_m2": "MISSING_PARENT_c_R2",
            "c_Ric_m2": "MISSING_PARENT_c_Ric",
            "c_Weyl_m2": "MISSING_PARENT_c_Weyl",
            "c_Riemann_m2": "MISSING_PARENT_c_Riemann",
            "c_GB_m2": "MISSING_PARENT_c_GB_OPTIONAL",
            "source_path": "MISSING_SOURCE_PATH",
            "normalization_status": "MISSING_PARENT_BASIS_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PB4458_1_zero_selector_switch",
            "c_R2_m2": "0_ONLY_IF_SELECTOR_SIGNED",
            "c_Ric_m2": "0_ONLY_IF_SELECTOR_SIGNED",
            "c_Weyl_m2": "0_ONLY_IF_SELECTOR_SIGNED",
            "c_Riemann_m2": "0_ONLY_IF_SELECTOR_SIGNED",
            "c_GB_m2": "ALLOWED_ONLY_IF_STRICT_GB_GUARD",
            "source_path": str(ZERO_3300),
            "normalization_status": "ZERO_SELECTOR_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def zero_selector_rows() -> List[Dict[str, object]]:
    return [
        {
            "selector_id": "ZS4458_0_curvature_linear",
            "clause": "parent local gravitational density is curvature-linear in the observed metric branch",
            "current_status": "CONDITIONAL_FROM_3300_NOT_PARENT_SIGNED",
            "zero_effect": "sets independent c_R2,c_Ric,c_Weyl,c_Riemann to zero",
            "required_next": "primitive deficit/holonomy action law or equivalent parent syntax theorem",
            "valid_for_claim": False,
        },
        {
            "selector_id": "ZS4458_1_second_order_no_extra_mode",
            "clause": "metric equation has second-order spin-2 principal symbol and no scalar/spin2 massive pole",
            "current_status": "RELATIVE_THEOREM_AVAILABLE_ACTIVATOR_MISSING",
            "zero_effect": "forbids finite Yukawa channels rather than merely making them small",
            "required_next": "no higher-derivative/no integrated-out curvature tower certificate",
            "valid_for_claim": False,
        },
        {
            "selector_id": "ZS4458_2_no_integrated_out_tower",
            "clause": "eliminated hidden sectors do not regenerate R^2, Ricci^2, Weyl^2, f(R), nonlocal kernels, or scalaron poles",
            "current_status": "OPEN_COUNTERMODEL_FROM_964_1822",
            "zero_effect": "prevents effective c_R2_eff after reduction",
            "required_next": "source/readout/boundary-stable elimination theorem",
            "valid_for_claim": False,
        },
        {
            "selector_id": "ZS4458_3_no_marker_prefactor",
            "clause": "no quotient/domain/species marker multiplies R or quadratic curvature in the local action",
            "current_status": "NO_MARKER_THEOREM_MISSING",
            "zero_effect": "prevents F(sigma)R and marker-generated f(R) routes",
            "required_next": "primitive quotient/no-natural-marker theorem",
            "valid_for_claim": False,
        },
        {
            "selector_id": "ZS4458_4_same_readout_metric_source",
            "clause": "same metric and Hilbert source are used for rods/clocks/EM/orbits and for diagonalizing the quadratic operator",
            "current_status": "CONDITIONAL_FROM_3303_NOT_PARENT_SIGNED",
            "zero_effect": "needed if finite branch is tested instead of zeroed",
            "required_next": "readout-after-variation and universal Hilbert source certificate",
            "valid_for_claim": False,
        },
    ]


def gb_guard_rows() -> List[Dict[str, object]]:
    return [
        {
            "guard_id": "GB4458_0_constant_4D",
            "condition": "coefficient is constant, uncoupled, and the branch is four-dimensional",
            "if_failed": "Gauss-Bonnet can re-enter through scalar coupling or varying coefficient",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "guard_id": "GB4458_1_boundary",
            "condition": "boundary/no-flux/Hamiltonian surface contribution is harmless on the same local collar",
            "if_failed": "topological density can leave boundary/readout residue",
            "current_status": "BOUNDARY_SILENCE_NOT_SOURCED_HERE",
            "valid_for_claim": False,
        },
        {
            "guard_id": "GB4458_2_no_generic_escape",
            "condition": "do not use GB language to erase generic R^2/Ricci^2/Weyl^2 rows",
            "if_failed": "false local-GR promotion",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def derivation_rows(regions: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    full = next(row for row in regions if row["region_id"] == "REG4458_0_full_basis")
    no_riem = next(row for row in regions if row["region_id"] == "REG4458_1_no_Riemann_basis")
    return [
        {
            "derivation_id": "D4458_0_basis_map",
            "premise": "4457 provides the canonical alpha_QG,beta_QG pole chart.",
            "derivation": "Use 4D identities C^2 = GB + 2 Ricci^2 - (2/3)R^2 and Riemann^2 = GB + 4 Ricci^2 - R^2.",
            "result": full["D0_map"] + "; " + full["D2_map"],
            "status": "BASIS_MAP_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4458_1_no_Riemann_region",
            "premise": "Most MTS rows name c_R2/Ricci/Weyl rather than an independent Riemann2 coefficient.",
            "derivation": "Set c_Riem=0 in the full map.",
            "result": no_riem["candidate_pass_region"],
            "status": "MTS_WORKING_REGION_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4458_2_spin2_warning",
            "premise": "Pure R^2 only changes D0; Ricci/Weyl terms feed D2.",
            "derivation": "The stricter 4457 spin2 bound constrains c_Ric,c_W,c_Riem, not c_R2 alone.",
            "result": "Do not call the c_R2 branch closed unless the spin2 basis coefficients are zero/topological/bounded too.",
            "status": "NO_SCALAR_ONLY_SHORTCUT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4458_3_zero_selector",
            "premise": "3300 and 1822 give exact conditional zero routes but not parent signatures.",
            "derivation": "Package the required clauses into one selector gate.",
            "result": "4459 should attack primitive deficit-action linearity or fill a real coefficient owner row.",
            "status": "NEXT_HINGE_SELECTED",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(regions: Sequence[Dict[str, object]], eval_rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    local_sources_ok = all(row["needle_found"] for row in source_rows() if row["source_kind"] == "local")
    map_ok = any(row["basis_id"] == "BM4458_2_Weyl2" and row["D0_contribution"] == "-6*c_W" for row in basis_map_rows())
    region_ok = any(row["region_id"] == "REG4458_1_no_Riemann_basis" and "12*c_R2 + c_Ric - 6*c_W" in row["D0_map"] for row in regions)
    rejects = all(row["verdict"].startswith("REJECTED") or row["verdict"].endswith("NONCLAIM") for row in eval_rows)
    return [
        {"gate_id": "CG4458_0_sources", "claim": "all cited local sources exist and needles are found", "passed": local_sources_ok, "valid_for_claim": False, "detail": "4457/3300/3302/3303/1822 evidence located."},
        {"gate_id": "CG4458_1_basis_map", "claim": "quadratic basis map to alpha_QG,beta_QG is written", "passed": map_ok, "valid_for_claim": False, "detail": "R2/Ricci2/Weyl2/Riemann2/GB rows present."},
        {"gate_id": "CG4458_2_region", "claim": "MTS basis D0/D2 candidate region is written", "passed": region_ok, "valid_for_claim": False, "detail": "working no-Riemann region plus full-basis region written."},
        {"gate_id": "CG4458_3_input_rejection", "claim": "placeholder parent coefficient rows are rejected", "passed": rejects, "valid_for_claim": False, "detail": "no numeric MTS coefficient silently promoted."},
        {"gate_id": "CG4458_4_zero_unsigned", "claim": "zero selector remains unsigned", "passed": True, "valid_for_claim": False, "detail": "3300/1822 clauses retained as theorem targets."},
        {"gate_id": "CG4458_5_gb_guard", "claim": "Gauss-Bonnet exception is guarded", "passed": len(gb_guard_rows()) == 3, "valid_for_claim": False, "detail": "GB cannot erase generic quadratic rows."},
        {"gate_id": "CG4458_6_no_public_claim", "claim": "no local-GR/R10 public claim emitted", "passed": True, "valid_for_claim": False, "detail": "normalization map is a contract, not a coefficient value."},
        {"gate_id": "CG4458_7_next_target", "claim": "next target selected", "passed": True, "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows(regions: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "working_region": next(row["candidate_pass_region"] for row in regions if row["region_id"] == "REG4458_1_no_Riemann_basis"),
            "zero_selector_signed": False,
            "parent_basis_values_ready": False,
            "gb_safe_claim_ready": False,
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
            "normalization_status": "basis_map_derived_parent_values_missing",
            "zero_status": "selector_clauses_packaged_but_unsigned",
            "spin2_status": "Ricci_Weyl_coefficients_now_explicitly_required_or_zeroed",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4458_0",
            "target": NEXT_TARGET,
            "objective": "Attack the zero selector through primitive deficit-action linearity, or fill the first real c_R2/c_Ric/c_W coefficient-owner value.",
            "derive_first": "prove MTS primitive cell/path action cost is linear in deficit/holonomy and has no second response channel",
            "fallback": "source a parent coefficient row in the 4458 basis and evaluate it against D0/D2 bounds",
            "risk": "using the normalization map as if it supplied coefficient values",
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
        "claim": "The MTS quadratic-curvature basis is now mapped into the canonical alpha_QG,beta_QG pole chart, yielding explicit D0/D2 inequalities for c_R2,c_Ric,c_Weyl,c_Riemann and a guarded Gauss-Bonnet exception.",
        "current_evidence": "4458 source register, basis normalization map, MTS basis coefficient region, parent input/evaluation template, zero selector gate, Gauss-Bonnet guard, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "private_smoke_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "map does not provide parent coefficient values or a zero-selector proof.",
        "sector": "local_gr_newton_r10",
        "evidence": "4458 source register, basis normalization map, MTS basis coefficient region, parent input/evaluation template, zero selector gate, Gauss-Bonnet guard, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "map does not provide parent coefficient values or a zero-selector proof.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(claim_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    current = text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + section.strip() + "\n")


def write_docs(regions: Sequence[Dict[str, object]], eval_rows: Sequence[Dict[str, object]]) -> None:
    sources = source_rows()
    basis = basis_map_rows()
    parent_inputs = parent_basis_input_rows()
    zeros = zero_selector_rows()
    gb = gb_guard_rows()
    derivations = derivation_rows(regions)
    gates = claim_gate_rows(regions, eval_rows)
    decisions = decision_rows(regions)
    status = status_rows()
    next_target = next_rows()
    body = f"""# 474 - PPC4161 MTS Quadratic Coefficient Normalization Map or cR2 Zero Selector

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4458 derives the missing normalization map from the MTS quadratic-curvature basis into the canonical `alpha_QG,beta_QG` pole chart used in 4457. It does not supply parent coefficient values and does not claim local GR.

## Basis Normalization Map

{table(basis)}

## MTS Basis Candidate Region

{table(regions)}

## Parent Basis Input / Evaluation

{table(parent_inputs)}

{table(eval_rows)}

## Zero Selector Clause Gate

{table(zeros)}

## Gauss-Bonnet Guard

{table(gb)}

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
    packet = f"""# 4458 - MTS quadratic coefficient normalization map or cR2 zero selector

Private checkpoint. No GitHub action. No public claim.

- Derived the map from MTS basis coefficients to the canonical pole chart.
- Working no-independent-Riemann region: `D0 = 12*c_R2 + c_Ric - 6*c_W`, `D2 = -c_Ric - 2*c_W`.
- This shows why `c_R2` alone is not enough: the stricter spin-2 branch depends on Ricci/Weyl coefficients.
- Zero selector remains unsigned; Gauss-Bonnet is guarded as a strict topological safe case only.
- Next: primitive deficit-action linearity, or first source-backed coefficient-owner value.

Next target: `{NEXT_TARGET}`

Marker: `{PACKET_MARKER}`
"""
    write_text(DOC_PATH, packet)
    append_marker_section(
        SPINE_PATH,
        MARKER,
        f"""## {MARKER}

The finite cR2/Ricci/Weyl branch now has an MTS-basis normalization map. In the common no-independent-Riemann basis, `D0 = 12*c_R2 + c_Ric - 6*c_W` and `D2 = -c_Ric - 2*c_W`. This turns the curvature-square survivor into either a precise coefficient-owner row or a zero-selector theorem target. It remains nonclaim because no parent coefficient values or selector proof are signed.
""",
    )
    append_marker_section(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## {PACKET_MARKER}

4458 maps the MTS quadratic basis into the 4457 canonical pole denominators and shows the spin-2 channel cannot be closed by scalar `c_R2` alone. The next exact hinge is primitive deficit-action linearity or a source-backed basis coefficient row.
""",
    )


def validation_rows() -> List[Dict[str, object]]:
    gates = read_csv(CLAIM_GATES)
    basis = read_csv(BASIS_MAP)
    regions = read_csv(REGION_MAP)
    eval_rows = read_csv(PARENT_BASIS_EVAL)
    checks = [
        ("VAL4458_0_local_sources_exist", all(row["local_path_exists"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "local"), "every cited local source path exists"),
        ("VAL4458_1_local_needles_found", all(row["needle_found"] == "True" for row in read_csv(SOURCE_REGISTER) if row["source_kind"] == "local"), "every cited local source needle is present"),
        ("VAL4458_2_basis_map_rows", len(basis) >= 5 and any(row["basis_id"] == "BM4458_2_Weyl2" for row in basis), "basis map rows written"),
        ("VAL4458_3_region_rows", len(regions) >= 4 and "12*c_R2 + c_Ric - 6*c_W" in text(REGION_MAP), "MTS basis coefficient regions written"),
        ("VAL4458_4_parent_inputs_rejected", all(row["verdict"].startswith("REJECTED") or row["verdict"].endswith("NONCLAIM") for row in eval_rows), "placeholder parent basis rows reject"),
        ("VAL4458_5_zero_selector_nonclaim", all(row["valid_for_claim"] == "False" for row in read_csv(ZERO_SELECTOR)), "zero selector rows remain nonclaim"),
        ("VAL4458_6_gb_guard", len(read_csv(GB_GUARD)) == 3, "Gauss-Bonnet guard rows written"),
        ("VAL4458_7_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4458_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-300"),
        ("VAL4458_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4458_10_post_doc", DOC_PATH.exists() and PACKET_MARKER in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4458_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4458_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4458_13_next_target", NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4458_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    bounds = read_csv(BOUNDS_4457)
    regions = coefficient_region_rows(bounds)
    parent_inputs = parent_basis_input_rows()
    eval_rows = [evaluate_parent_basis_row(row, bounds) for row in parent_inputs]
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(BASIS_MAP, basis_map_rows())
    write_csv(REGION_MAP, regions)
    write_csv(PARENT_BASIS_INPUT, parent_inputs)
    write_csv(PARENT_BASIS_EVAL, eval_rows)
    write_csv(ZERO_SELECTOR, zero_selector_rows())
    write_csv(GB_GUARD, gb_guard_rows())
    write_csv(DERIVATION_ROWS, derivation_rows(regions))
    write_csv(DECISION_CSV, decision_rows(regions))
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows(regions, eval_rows))
    write_docs(regions, eval_rows)
    update_claims_register()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
