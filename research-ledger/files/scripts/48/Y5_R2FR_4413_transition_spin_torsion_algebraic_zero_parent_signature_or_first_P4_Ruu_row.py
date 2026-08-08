from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from spin_torsion_algebraic_zero_gate import evaluate_p4_rows, evaluate_signature_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4413"
CLAIM_ID = "L-254"
MARKER = "PPC4161_TRANSITION_SPIN_TORSION_ALGEBRAIC_ZERO_PARENT_SIGNATURE_OR_FIRST_P4_RUU_ROW_4413"
PACKET_MARKER = "PPC4161_PACKET_SPIN_TORSION_ALGEBRAIC_ZERO_PARENT_SIGNATURE_OR_FIRST_P4_RUU_ROW_4413"
DECISION = "SPIN_TORSION_ALGEBRAIC_ZERO_CONTRACT_SHARPENED_SELECTOR_PROJECTIVE_BOUNDARY_OPEN_P4_ROW_READY_NONCLAIM"
NEXT_TARGET = "4414-Y5-R2FR-transition-projective-boundary-guard-for-spin-torsion-zero-or-first-P4-row-fill.md"

FORMAL_PATH = FORMAL / "429-PPC4161-transition-spin-torsion-algebraic-zero-parent-signature-or-first-P4-Ruu-row.md"
DOC_PATH = POST / "4413-Y5-R2FR-transition-spin-torsion-algebraic-zero-parent-signature-or-first-P4-Ruu-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4413_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SIGNATURE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4413_SPIN_TORSION_SIGNATURE_INPUT.csv"
SIGNATURE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4413_SPIN_TORSION_SIGNATURE_OUTPUT.csv"
P4_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4413_P4_RUU_COMPONENT_INPUT.csv"
P4_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4413_P4_RUU_COMPONENT_OUTPUT.csv"

GATE_PATH = SCRIPT_DIR / "spin_torsion_algebraic_zero_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4413_transition_spin_torsion_algebraic_zero_parent_signature_or_first_P4_Ruu_row.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_428 = FORMAL / "428-PPC4161-transition-positive-operator-sector-map-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"
NEXT_4412 = SOURCE_DIR / "P8_Y5_R2FR_4412_NEXT_TARGET.csv"
POST_3494 = POST / "3494-Y5-R2FR-ordinary-matter-coframe-owned-spin-proof-or-axial-torsion-tail.md"
POST_4101 = POST / "4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md"
POST_4102 = POST / "4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md"
POST_3565 = POST / "3565-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md"
POST_1835 = POST / "1835-Y5-R2FR-DeltaGamma-component-map-to-P4-observables.md"
POST_2378 = POST / "2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md"
POST_960 = POST / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md"
FORMAL_422 = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4413_00_4412_next": (
        NEXT_4412,
        "owned-coframe/no-independent-connection branch",
        "4412 selected spin/torsion algebraic zero or first P4 row.",
    ),
    "SRC4413_01_4412_formal": (
        FORMAL_428,
        "spin/torsion has a stronger algebraic zero route",
        "4412 proof-type map.",
    ),
    "SRC4413_02_3494_spin": (
        POST_3494,
        "owned-coframe candidate branch gives `xi_A=0`",
        "owned-coframe spin branch and counterbranch.",
    ),
    "SRC4413_03_4101_fork": (
        POST_4101,
        "local LC/no-independent-affine branch",
        "LC/no-independent-affine selector gap.",
    ),
    "SRC4413_04_4102_selector": (
        POST_4102,
        "NoAffineGenerator",
        "local LC branch selector and product gate.",
    ),
    "SRC4413_05_3565_fork": (
        POST_3565,
        "STH3565_0_connection_fork",
        "spin/torsion structural fork.",
    ),
    "SRC4413_06_1835_p4": (
        POST_1835,
        "DGOM1835_0_spin",
        "DeltaGamma/P4 observable map.",
    ),
    "SRC4413_07_2378_projective": (
        POST_2378,
        "Projective trace is zero only inside the private owned-coframe",
        "private projective zero and public fallback.",
    ),
    "SRC4413_08_960_torsion_lc": (
        POST_960,
        "torsion/nonmetricity: LC routes known, parent proof/bounds missing.",
        "torsion/nonmetricity LC gate and fallback rows.",
    ),
    "SRC4413_09_gate": (
        GATE_PATH,
        "def evaluate_signature_rows",
        "new spin/torsion algebraic-zero gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    if not path.exists():
        return False, -1
    for line_number, line in enumerate(text(path).splitlines(), 1):
        if needle in line:
            return True, line_number
    return False, -1


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def markdown_table(rows: List[Dict[str, object]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    write_text(path, current.rstrip() + "\n\n" + block.strip() + "\n")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    current = text(path)
    if f"\n{claim_id}," in current:
        return
    if current and not current.endswith("\n"):
        current += "\n"
    write_text(path, current + csv_line(row))


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line_number = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line_number,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "STZ4413_0_variable_absence_zero",
            "statement": "If ordinary matter/spin/readout actions have no independent `Gamma_ind` or contorsion argument, their hypermomentum into torsion is zero by variable absence.",
            "derivation": "For `S_i=Sbar_i[e_obs,omega_LC[e_obs],Psi,A,theta,...]`, the derivative with respect to an absent independent affine variable is zero on the reduced configuration space. Spin backreaction then belongs to the coframe/Hilbert equation, not an independent torsion source.",
            "new_information": "This is stronger than a positive no-hair theorem for the spin/torsion slot.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "STZ4413_1_public_selector_gap",
            "statement": "The current branch is not yet public because the parent has not excluded the independent torsionful/metric-affine counterbranch.",
            "derivation": "4101/4102 leave `B_LC_selector` open: if a sector retains `Gamma_ind`, `omega_ind`, contorsion, projective trace, boundary current or readout affine transport, the algebraic zero theorem no longer covers that sector.",
            "new_information": "The blocker is now branch selection/projective-boundary guard, not the algebra itself.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "STZ4413_2_P4_Ruu_fallback",
            "statement": "If the selector gap stays open, the torsion slot must enter the first real `R_uu` row through P4 channels.",
            "derivation": "The P4 route decomposes connection residuals into axial spin torsion, projective trace, torsion trace/nonmetricity and boundary/improvement components. Each needs `uu`/trace projection, units, source path, support certificate and no-cancellation guard.",
            "new_information": "Spin/torsion is now source-row-ready rather than a symbolic survivor.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "STZ4413_3_projective_guard_priority",
            "statement": "Projective trace/boundary/readout guard is the next narrow target.",
            "derivation": "The owned-coframe private branch kills projective trace by variable absence, but public sectors can still couple to projective trace through source, clocks, WEP, light, orbital readout or boundary/domain maps. This guard blocks promotion of the algebraic zero.",
            "new_information": "4414 should attack projective/boundary guard before broader P4 source acquisition.",
            "valid_for_claim": False,
        },
    ]


def signature_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "signature_id": "STSIG4413_0_current_owned_coframe_branch",
            "branch": "current_private_owned_coframe_LC_branch",
            "ordinary_matter_factors_through_e_obs": True,
            "spin_connection_is_omega_LC": True,
            "no_Gamma_ind_argument": True,
            "no_contorsion_argument": True,
            "no_hypermomentum_source": False,
            "EM_Hilbert_no_affine_source": True,
            "clocks_light_orbits_downstream_metric": False,
            "projective_trace_guard": False,
            "boundary_readout_no_torsion_current": False,
            "same_tau_coframe_support": False,
            "counterbranch_excluded": False,
            "parent_selector_signed": False,
            "source_path": str(POST_3494),
            "input_valid_for_claim": False,
            "notes": "Strong private algebraic branch, but public selector/projective/boundary/readout guards remain open.",
        },
        {
            "signature_id": "STSIG4413_1_future_public_zero_schema",
            "branch": "future_public_parent_signature",
            "ordinary_matter_factors_through_e_obs": True,
            "spin_connection_is_omega_LC": True,
            "no_Gamma_ind_argument": True,
            "no_contorsion_argument": True,
            "no_hypermomentum_source": True,
            "EM_Hilbert_no_affine_source": True,
            "clocks_light_orbits_downstream_metric": True,
            "projective_trace_guard": True,
            "boundary_readout_no_torsion_current": True,
            "same_tau_coframe_support": True,
            "counterbranch_excluded": True,
            "parent_selector_signed": True,
            "source_path": str(POST_4102),
            "input_valid_for_claim": False,
            "notes": "Control row for the full parent-signature theorem; intentionally nonclaim.",
        },
        {
            "signature_id": "STSIG4413_2_metric_affine_counterbranch",
            "branch": "independent_connection_counterbranch",
            "ordinary_matter_factors_through_e_obs": False,
            "spin_connection_is_omega_LC": False,
            "no_Gamma_ind_argument": False,
            "no_contorsion_argument": False,
            "no_hypermomentum_source": False,
            "EM_Hilbert_no_affine_source": False,
            "clocks_light_orbits_downstream_metric": False,
            "projective_trace_guard": False,
            "boundary_readout_no_torsion_current": False,
            "same_tau_coframe_support": False,
            "counterbranch_excluded": False,
            "parent_selector_signed": False,
            "source_path": str(POST_3565),
            "input_valid_for_claim": False,
            "notes": "Counterbranch row proves why torsion cannot be silently deleted if independent connection is admitted.",
        },
    ]


def p4_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "P4R4413_0_missing_axial_spin",
            "p4_component": "axial_torsion_spin",
            "p4_channel": "spin_hypermomentum_to_Ruu",
            "uu_abs": "MISSING_AXIAL_TORSION_UU",
            "trace_abs": "MISSING_AXIAL_TORSION_TRACE",
            "units": "curvature_or_residual_stress_units_to_match_R_uu",
            "projection_matrix": "MISSING_P_spin_to_Ruu",
            "arena_targets": "spin_torsion;clock;WEP;PPN;R10",
            "source_path": str(POST_1835),
            "support_certificate_path": "MISSING_SAME_SUPPORT_CERTIFICATE",
            "no_cancellation_guard": True,
            "input_valid_for_claim": False,
            "notes": "First live axial spin-torsion P4 row if algebraic zero fails.",
        },
        {
            "row_id": "P4R4413_1_missing_projective_trace",
            "p4_component": "projective_trace",
            "p4_channel": "projective_trace_to_Ruu",
            "uu_abs": "MISSING_PROJECTIVE_UU",
            "trace_abs": "MISSING_PROJECTIVE_TRACE",
            "units": "curvature_or_residual_stress_units_to_match_R_uu",
            "projection_matrix": "MISSING_P_projective_to_Ruu",
            "arena_targets": "source_charge;clock;WEP;light;orbital",
            "source_path": str(POST_2378),
            "support_certificate_path": "MISSING_SAME_SUPPORT_CERTIFICATE",
            "no_cancellation_guard": True,
            "input_valid_for_claim": False,
            "notes": "Projective trace fallback unless all-sector projective guard closes.",
        },
        {
            "row_id": "P4R4413_2_missing_torsion_nonmetricity_shear",
            "p4_component": "torsion_nonmetricity_shear",
            "p4_channel": "connection_shear_to_Ruu",
            "uu_abs": "MISSING_CONNECTION_SHEAR_UU",
            "trace_abs": "MISSING_CONNECTION_SHEAR_TRACE",
            "units": "curvature_or_residual_stress_units_to_match_R_uu",
            "projection_matrix": "MISSING_P_connection_shear_to_Ruu",
            "arena_targets": "lightcone;PPN;clock;WEP",
            "source_path": str(POST_960),
            "support_certificate_path": "MISSING_SAME_SUPPORT_CERTIFICATE",
            "no_cancellation_guard": True,
            "input_valid_for_claim": False,
            "notes": "Nonmetricity/shear torsion fallback if LC compatibility fails.",
        },
        {
            "row_id": "P4R4413_3_zero_schema_nonclaim",
            "p4_component": "spin_torsion_zero_control",
            "p4_channel": "schema_control",
            "uu_abs": 0.0,
            "trace_abs": 0.0,
            "units": "curvature_or_residual_stress_units_to_match_R_uu",
            "projection_matrix": "identity_zero_control",
            "arena_targets": "schema_control",
            "source_path": str(GATE_PATH),
            "support_certificate_path": str(GATE_PATH),
            "no_cancellation_guard": True,
            "input_valid_for_claim": False,
            "notes": "Control row proving zero P4 schema remains nonclaim.",
        },
    ]


def source_register_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4413_SOURCE_REGISTER.csv"


def derivation_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4413_DERIVATIONS.csv"


def claim_gate_rows(signature_rows: List[Dict[str, str]], p4_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    current = next(row for row in signature_rows if row["signature_id"] == "STSIG4413_0_current_owned_coframe_branch")
    return [
        {
            "gate_id": "CG4413_0_private_algebraic_zero",
            "claim": "spin/torsion zero inside private owned-coframe branch",
            "claim_allowed": False,
            "reason": f"current status is {current['current_status']}; selector/projective/boundary/readout guards are open.",
        },
        {
            "gate_id": "CG4413_1_public_parent_signature",
            "claim": "spin/torsion zero as public parent theorem",
            "claim_allowed": False,
            "reason": "future schema row is wired but nonclaim; no parent selector/counterbranch exclusion is signed.",
        },
        {
            "gate_id": "CG4413_2_P4_Ruu_row",
            "claim": "P4 torsion R_uu row score-ready",
            "claim_allowed": False,
            "reason": "axial/projective/shear P4 rows lack numeric uu/trace projections and support certificates.",
        },
        {
            "gate_id": "CG4413_3_local_GR",
            "claim": "local GR/Newton/PPN/R10 pass",
            "claim_allowed": False,
            "reason": "spin/torsion is only one survivor slot and remains nonclaim.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4413_0",
            "decision": DECISION,
            "summary": "4413 sharpens the spin/torsion slot. The algebraic theorem is real: if ordinary matter, spin, EM and readouts factor through e_obs and omega_LC[e_obs] with no Gamma_ind/contorsion argument, independent torsion hypermomentum is zero by variable absence. Current MTS has that as a strong private branch, but public promotion is blocked by parent selector, projective trace, boundary/readout current and counterbranch exclusion. The P4 fallback now has axial, projective and shear/nonmetricity R_uu component rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "claim_id": CLAIM_ID,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4413_0",
            "target": NEXT_TARGET,
            "question": "Can the projective trace and boundary/readout guards close the spin/torsion algebraic zero branch, or must the first P4 component row be filled?",
            "preferred_route": "derive all-sector projective invariance/gauge-fixing plus boundary/readout no torsion-current on the same tau/coframe/worldtube support.",
            "fallback_route": "fill axial/projective/shear P4 R_uu rows with numeric uu/trace projections, units, source path, support certificate and no-cancellation guard.",
            "avoid": "treating private owned-coframe zero as public proof, ignoring projective trace, or using torsion-free language without parent branch selection.",
            "valid_for_claim": False,
        }
    ]


def compact_rows(rows: List[Dict[str, str]], fields: List[str]) -> List[Dict[str, str]]:
    return [{field: row.get(field, "") for field in fields} for row in rows]


def render_document(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    signatures: List[Dict[str, str]],
    p4_rows: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 429 PPC4161 transition: spin/torsion algebraic zero parent signature or first P4 Ruu row

Marker: `{MARKER}`

Generated: `{STAMP}`

Decision: `{DECISION}`

## Result

4413 gets a real algebraic win, but keeps it honest:

- Inside an owned-coframe/LC branch, spin/torsion hypermomentum is zero by variable absence.
- Publicly, that is blocked until the parent selector excludes independent torsionful/metric-affine counterbranches.
- The remaining guard is projective trace plus boundary/readout torsion-current silence.
- If that guard fails, the P4 fallback rows are now explicit `R_uu` component rows.

## Source Audit

{markdown_table(sources)}

## Derivations

{markdown_table(derivations)}

## Algebraic-Zero Signature Gate

{markdown_table(compact_rows(signatures, ["signature_id", "branch", "current_status", "action_factorization_ready", "affine_safety_ready", "selector_ready", "zero_schema_ready", "valid_for_claim"]))}

## P4 Ruu Component Gate

{markdown_table(compact_rows(p4_rows, ["row_id", "p4_component", "current_status", "numeric_ready", "projection_ready", "ricci_component_bound", "valid_for_claim"]))}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_target_rows())}
"""


def append_spine() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4413 local spine update: spin/torsion algebraic zero sharpened

Marker: `{MARKER}`

4413 shows the spin/torsion survivor can be zeroed by variable absence inside an owned-coframe/Levi-Civita branch: ordinary matter and spin depend on `e_obs` and `omega_LC[e_obs]`, not `Gamma_ind` or contorsion. Public promotion remains blocked by parent branch selection, projective trace, boundary/readout torsion-current silence and counterbranch exclusion. The fallback is now explicit P4 `R_uu` rows for axial spin torsion, projective trace and connection shear/nonmetricity.
""",
    )


def append_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4413 packet update: spin/torsion zero is algebraic, not fitted

Marker: `{PACKET_MARKER}`

The spin/torsion route has a genuine theorem shape: no independent connection argument means no independent hypermomentum. But it is still a branch theorem, not a public local-GR claim. Next target is projective/boundary/readout guard or first P4 row fill.
""",
    )


def append_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4413 sharpens the spin/torsion survivor. In an owned-coframe/Levi-Civita branch, ordinary matter and spin actions factor through e_obs and omega_LC[e_obs], so independent torsion hypermomentum is zero by variable absence. Public promotion is blocked because parent branch selection, projective trace, boundary/readout torsion-current silence and counterbranch exclusion are not signed. The fallback now has axial, projective and shear/nonmetricity P4 R_uu component rows. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4413 source register, derivation rows, spin/torsion signature gate, P4 Ruu component gate, claim gates, decision, status, next target and validation CSV.",
            "spin_torsion_algebraic_zero_contract_ready_nonclaim",
            "Close projective/boundary/readout guard or fill first P4 R_uu torsion row.",
            "Using private owned-coframe zero as public proof, ignoring projective trace, or claiming torsion-free geometry without parent branch selection.",
        ],
    )


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, object]]:
    sources = read_csv(paths["source_register"])
    signatures = read_csv(SIGNATURE_OUTPUT)
    p4_rows = read_csv(P4_OUTPUT)
    current = next(row for row in signatures if row["signature_id"] == "STSIG4413_0_current_owned_coframe_branch")
    schema = next(row for row in signatures if row["signature_id"] == "STSIG4413_1_future_public_zero_schema")
    counter = next(row for row in signatures if row["signature_id"] == "STSIG4413_2_metric_affine_counterbranch")
    zero_p4 = next(row for row in p4_rows if row["row_id"] == "P4R4413_3_zero_schema_nonclaim")
    checks = [
        ("VAL4413_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4413_1_source_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle was found"),
        ("VAL4413_2_current_branch_not_public", current["current_status"] == "OWNED_COFRAME_BRANCH_READY_SELECTOR_OR_GUARDS_OPEN", "current owned-coframe branch is useful but not public"),
        ("VAL4413_3_future_schema_nonclaim", schema["current_status"] == "SPIN_TORSION_ZERO_SCHEMA_READY_NONCLAIM", "future public zero schema is wired but nonclaim"),
        ("VAL4413_4_counterbranch_blocks", counter["current_status"] == "SPIN_TORSION_ALGEBRAIC_ZERO_BLOCKED", "metric-affine counterbranch is not silently deleted"),
        ("VAL4413_5_p4_rows_blocked", all(row["current_status"] == "P4_RUU_COMPONENT_ROW_BLOCKED" for row in p4_rows if row["row_id"] != "P4R4413_3_zero_schema_nonclaim"), "live P4 rows require real numeric projections"),
        ("VAL4413_6_zero_p4_nonclaim", zero_p4["current_status"] == "P4_RUU_COMPONENT_SCHEMA_READY_NONCLAIM", "zero P4 schema control stays nonclaim"),
        ("VAL4413_7_no_output_claims", not any(bool_text(row.get("claim_allowed", "False")) or bool_text(row.get("valid_for_claim", "False")) for row in signatures + p4_rows), "no generated gate output is claim-valid"),
        ("VAL4413_8_claim_row_exists", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claims register contains L-254"),
        ("VAL4413_9_spine_marker_exists", MARKER in text(SPINE_PATH), "spine update marker exists"),
        ("VAL4413_10_packet_marker_exists", PACKET_MARKER in text(PACKET_PATH), "packet update marker exists"),
        ("VAL4413_11_formal_doc_exists", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4413_12_post_doc_exists", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post-checkpoint doc exists with marker"),
        ("VAL4413_13_next_target_exists", paths["next_target"].exists() and NEXT_TARGET in text(paths["next_target"]), "next target file exists"),
        ("VAL4413_14_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
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
    paths = {
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4413_SOURCE_REGISTER.csv",
        "derivations": SOURCE_DIR / "P8_Y5_R2FR_4413_DERIVATIONS.csv",
        "claim_gates": SOURCE_DIR / "P8_Y5_R2FR_4413_CLAIM_GATES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4413_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4413_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4413_NEXT_TARGET.csv",
    }
    sources = source_rows()
    derivations = derivation_rows()
    write_csv(paths["source_register"], sources)  # type: ignore[arg-type]
    write_csv(paths["derivations"], derivations)  # type: ignore[arg-type]
    write_csv(SIGNATURE_INPUT, signature_input_rows())  # type: ignore[arg-type]
    signatures = evaluate_signature_rows(SIGNATURE_INPUT)
    write_csv(SIGNATURE_OUTPUT, signatures)
    write_csv(P4_INPUT, p4_input_rows())  # type: ignore[arg-type]
    p4_rows = evaluate_p4_rows(P4_INPUT)
    write_csv(P4_OUTPUT, p4_rows)
    claim_gates = claim_gate_rows(signatures, p4_rows)
    write_csv(paths["claim_gates"], claim_gates)  # type: ignore[arg-type]
    write_csv(paths["decision"], decision_rows())  # type: ignore[arg-type]
    write_csv(paths["status"], status_rows())  # type: ignore[arg-type]
    write_csv(paths["next_target"], next_target_rows())  # type: ignore[arg-type]

    doc = render_document(sources, derivations, signatures, p4_rows, claim_gates)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_spine()
    append_packet()
    append_claim()

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(VALIDATION_PATH, validation_rows(paths))  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
