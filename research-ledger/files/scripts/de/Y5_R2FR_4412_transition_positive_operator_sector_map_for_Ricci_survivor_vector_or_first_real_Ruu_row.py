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

from ricci_positive_operator_sector_gate import evaluate_sector_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4412"
CLAIM_ID = "L-253"
MARKER = "PPC4161_TRANSITION_POSITIVE_OPERATOR_SECTOR_MAP_FOR_RICCI_SURVIVOR_VECTOR_OR_FIRST_REAL_RUU_ROW_4412"
PACKET_MARKER = "PPC4161_PACKET_POSITIVE_OPERATOR_SECTOR_MAP_FOR_RICCI_SURVIVOR_VECTOR_OR_FIRST_REAL_RUU_ROW_4412"
DECISION = "RICCI_SURVIVOR_VECTOR_SPLIT_BY_ROUTE_OPERATOR_ALGEBRAIC_GRAMMAR_FINITE_ROW_NONCLAIM"
NEXT_TARGET = "4413-Y5-R2FR-transition-spin-torsion-algebraic-zero-parent-signature-or-first-P4-Ruu-row.md"

FORMAL_PATH = FORMAL / "428-PPC4161-transition-positive-operator-sector-map-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"
DOC_PATH = POST / "4412-Y5-R2FR-transition-positive-operator-sector-map-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4412_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SECTOR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4412_POSITIVE_OPERATOR_SECTOR_INPUT.csv"
SECTOR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4412_POSITIVE_OPERATOR_SECTOR_OUTPUT.csv"
FIRST_RUU_ROW_REQUIREMENTS = SOURCE_DIR / "P8_Y5_R2FR_4412_FIRST_REAL_RUU_ROW_REQUIREMENTS.csv"

SECTOR_GATE_PATH = SCRIPT_DIR / "ricci_positive_operator_sector_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4412_transition_positive_operator_sector_map_for_Ricci_survivor_vector_or_first_real_Ruu_row.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_426 = FORMAL / "426-PPC4161-transition-local-Ricci-survivor-vector-zero-or-first-real-Ruu-source-row.md"
FORMAL_427 = FORMAL / "427-PPC4161-transition-parent-Ward-nohair-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"
FORMAL_419 = FORMAL / "419-PPC4161-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"
FORMAL_420 = FORMAL / "420-PPC4161-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"
FORMAL_422 = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
FORMAL_423 = FORMAL / "423-PPC4161-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"
NEXT_4411 = SOURCE_DIR / "P8_Y5_R2FR_4411_NEXT_TARGET.csv"
RUU_TEMPLATE_4411 = SOURCE_DIR / "P8_Y5_R2FR_4411_FIRST_REAL_RUU_ROW_TEMPLATE.csv"
POST_2728 = POST / "2728-Y5-R2FR-memory-positive-operator-local-silence-or-residual-row-under-AX1090-closure.md"
POST_960 = POST / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md"
POST_3494 = POST / "3494-Y5-R2FR-ordinary-matter-coframe-owned-spin-proof-or-axial-torsion-tail.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4412_00_4411_next": (
        NEXT_4411,
        "positive self-adjoint parent operator sector",
        "4411 handoff to positive-operator sector map.",
    ),
    "SRC4412_01_4411_formal": (
        FORMAL_427,
        "Ward/Bianchi identity can own/conserve",
        "4411 Ward/no-hair split.",
    ),
    "SRC4412_02_4410_vector": (
        FORMAL_426,
        "c_R2/M_R",
        "4410 survivor-vector slot list.",
    ),
    "SRC4412_03_memory_operator": (
        POST_2728,
        "positive operator with zero source/boundary kills",
        "memory positive-operator theorem contract.",
    ),
    "SRC4412_04_R2_torsion": (
        POST_960,
        "R2/fR: filter works",
        "R2/fR scalar-mode and torsion/LC gate.",
    ),
    "SRC4412_05_spin": (
        POST_3494,
        "owned-coframe candidate branch gives `xi_A=0`",
        "spin/torsion algebraic zero branch.",
    ),
    "SRC4412_06_source_coupling": (
        FORMAL_422,
        "epsilon_Gsrc_perp",
        "source-charge/profile component route.",
    ),
    "SRC4412_07_profile": (
        FORMAL_423,
        "rho_eff(y) = rho_H(y) on W_H",
        "density-profile grammar/source route.",
    ),
    "SRC4412_08_4411_template": (
        RUU_TEMPLATE_4411,
        "MISSING_REAL_COMPONENT_ROW",
        "first-real-Ruu row template from 4411.",
    ),
    "SRC4412_09_sector_gate": (
        SECTOR_GATE_PATH,
        "def evaluate_sector_rows",
        "new sector-map gate.",
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
            "derivation_id": "POS4412_0_route_split",
            "statement": "The 4410 survivor vector is not one mathematical species.",
            "derivation": "`c_Gamma/P_leak` and `c_R2/M_R` are positive-operator candidates; `spin/torsion` is better treated as an algebraic connection/no-hypermomentum route; `epsilon_Gsrc/E_profile` is a source-grammar/profile-equality route, not a positive operator field.",
            "new_information": "The no-hair theorem cannot be forced uniformly; each slot now has the correct proof weapon or finite-row fallback.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "POS4412_1_operator_slots",
            "statement": "A positive-operator slot needs parent variable ownership, quadratic/linearized action, self-adjoint positive operator, gap/zero-mode control, zero source, zero boundary and metric-response projection.",
            "derivation": "The 2728 energy identity gives the form. If any source, boundary, gap, or metric-response clause fails, the field is not zero; it contributes a finite `R_uu` component row.",
            "new_information": "This supplies the exact promotion checklist for memory and R2-like slots.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "POS4412_2_algebraic_torsion_slot",
            "statement": "Spin/torsion should not be shoehorned into the elliptic no-hair proof when an algebraic zero route is stronger.",
            "derivation": "If the parent uses the owned coframe/Levi-Civita spin connection and ordinary matter has no independent `Gamma_ind`/contorsion argument, hypermomentum into torsion is zero by variable absence. If an independent torsionful spin connection is admitted, the P4 torsion row survives.",
            "new_information": "This identifies spin/torsion as the highest-leverage next target because it may close by parent signature rather than numeric bounding.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "POS4412_3_source_profile_slot",
            "statement": "`epsilon_Gsrc/E_profile` is a source object, so its clean route is Hilbert-source grammar/profile equality rather than a positive operator.",
            "derivation": "It disappears only if the same Hilbert density/source charge is used on the same worldtube before readout and the source-shadow/topological/readout profile clauses close. Otherwise it must be a finite density/source row.",
            "new_information": "This prevents a false no-hair proof from hiding source-profile errors.",
            "valid_for_claim": False,
        },
    ]


def sector_input_rows() -> List[Dict[str, object]]:
    live = [
        {
            "component_id": "POS4412_0_live_cGamma_Pleak",
            "component": "c_Gamma/P_leak",
            "route_type": "positive_operator",
            "parent_variable_owned": False,
            "action_or_constraint_written": True,
            "maps_to_component": True,
            "self_adjoint_or_algebraic": True,
            "positive_or_invertible": False,
            "mass_gap_or_constraint_rank": False,
            "zero_source_or_no_hypermomentum": False,
            "boundary_no_flux_or_no_boundary": False,
            "metric_response_owned": False,
            "same_support": False,
            "uu_trace_projection_owned": True,
            "source_path": str(POST_2728),
            "input_valid_for_claim": False,
            "notes": "Memory/Pleak positive-operator shape exists, but activation clauses are unsigned.",
        },
        {
            "component_id": "POS4412_1_live_cR2_MR",
            "component": "c_R2/M_R",
            "route_type": "positive_operator",
            "parent_variable_owned": False,
            "action_or_constraint_written": True,
            "maps_to_component": True,
            "self_adjoint_or_algebraic": True,
            "positive_or_invertible": False,
            "mass_gap_or_constraint_rank": False,
            "zero_source_or_no_hypermomentum": False,
            "boundary_no_flux_or_no_boundary": False,
            "metric_response_owned": True,
            "same_support": False,
            "uu_trace_projection_owned": True,
            "source_path": str(POST_960),
            "input_valid_for_claim": False,
            "notes": "R2/fR filter is clean, but coefficient zero, scalar mass/sign and source/boundary rows are missing.",
        },
        {
            "component_id": "POS4412_2_live_spin_torsion",
            "component": "spin/torsion",
            "route_type": "algebraic_zero",
            "parent_variable_owned": False,
            "action_or_constraint_written": True,
            "maps_to_component": True,
            "self_adjoint_or_algebraic": True,
            "positive_or_invertible": True,
            "mass_gap_or_constraint_rank": True,
            "zero_source_or_no_hypermomentum": False,
            "boundary_no_flux_or_no_boundary": False,
            "metric_response_owned": False,
            "same_support": False,
            "uu_trace_projection_owned": True,
            "source_path": str(POST_3494),
            "input_valid_for_claim": False,
            "notes": "Owned-coframe spin gives an exact conditional zero, but the independent torsionful counterbranch is not globally excluded.",
        },
        {
            "component_id": "POS4412_3_live_epsilon_Gsrc_Eprofile",
            "component": "epsilon_Gsrc/E_profile",
            "route_type": "source_grammar",
            "parent_variable_owned": False,
            "action_or_constraint_written": True,
            "maps_to_component": True,
            "self_adjoint_or_algebraic": True,
            "positive_or_invertible": False,
            "mass_gap_or_constraint_rank": True,
            "zero_source_or_no_hypermomentum": False,
            "boundary_no_flux_or_no_boundary": False,
            "metric_response_owned": False,
            "same_support": False,
            "uu_trace_projection_owned": True,
            "source_path": str(FORMAL_423),
            "input_valid_for_claim": False,
            "notes": "Source/profile branch needs grammar and distributional equality, not an elliptic no-hair proof.",
        },
        {
            "component_id": "POS4412_4_live_Lambda_projector",
            "component": "Lambda_eff/projector_boundary",
            "route_type": "finite_source_row",
            "parent_variable_owned": False,
            "action_or_constraint_written": False,
            "maps_to_component": False,
            "self_adjoint_or_algebraic": False,
            "positive_or_invertible": False,
            "mass_gap_or_constraint_rank": False,
            "zero_source_or_no_hypermomentum": False,
            "boundary_no_flux_or_no_boundary": False,
            "metric_response_owned": False,
            "same_support": False,
            "uu_trace_projection_owned": False,
            "source_path": str(FORMAL_419),
            "input_valid_for_claim": False,
            "notes": "Remaining scalar/projector boundary payload must be zeroed separately or supplied as a finite R_uu row.",
        },
    ]
    schema: List[Dict[str, object]] = []
    for component, route_type in [
        ("c_Gamma/P_leak", "positive_operator"),
        ("c_R2/M_R", "positive_operator"),
        ("spin/torsion", "algebraic_zero"),
        ("epsilon_Gsrc/E_profile", "source_grammar"),
    ]:
        schema.append(
            {
                "component_id": f"POS4412_schema_{component.replace('/', '_').replace(' ', '_')}",
                "component": component,
                "route_type": route_type,
                "parent_variable_owned": True,
                "action_or_constraint_written": True,
                "maps_to_component": True,
                "self_adjoint_or_algebraic": True,
                "positive_or_invertible": True,
                "mass_gap_or_constraint_rank": True,
                "zero_source_or_no_hypermomentum": True,
                "boundary_no_flux_or_no_boundary": True,
                "metric_response_owned": True,
                "same_support": True,
                "uu_trace_projection_owned": True,
                "source_path": str(FORMAL_427),
                "input_valid_for_claim": False,
                "notes": "Control row for the theorem shape; intentionally nonclaim.",
            }
        )
    return live + schema


def first_ruu_requirement_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    if RUU_TEMPLATE_4411.exists():
        for row in read_csv(RUU_TEMPLATE_4411):
            rows.append(
                {
                    **row,
                    "4412_route": "source_this_row_if_sector_zero_route_fails",
                    "additional_requirement": "component must declare whether it came from positive_operator, algebraic_zero, source_grammar, or finite_source_row route",
                    "valid_for_claim": "False",
                }
            )
    return rows


def source_register_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4412_SOURCE_REGISTER.csv"


def derivation_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4412_DERIVATIONS.csv"


def claim_gate_rows(sector_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    live_status = ";".join(
        f"{row['component']}={row['current_status']}"
        for row in sector_rows
        if row["component_id"].startswith("POS4412_") and "_live_" in row["component_id"]
    )
    return [
        {
            "gate_id": "CG4412_0_positive_operator_full_vector",
            "claim": "positive operator no-hair zeros whole Ricci survivor vector",
            "claim_allowed": False,
            "reason": "only c_Gamma/Pleak and c_R2/M_R are positive-operator candidates, and both are activation-blocked.",
        },
        {
            "gate_id": "CG4412_1_spin_torsion_algebraic_zero",
            "claim": "spin/torsion zero by owned coframe/no independent connection",
            "claim_allowed": False,
            "reason": "strong conditional algebraic route exists, but global parent signature and counterbranch exclusion are not signed.",
        },
        {
            "gate_id": "CG4412_2_source_profile_grammar",
            "claim": "epsilon_Gsrc/E_profile zero by source grammar",
            "claim_allowed": False,
            "reason": "source/profile equality is a grammar/distributional theorem, not a positive-operator theorem, and remains unsigned.",
        },
        {
            "gate_id": "CG4412_3_first_Ruu_row",
            "claim": "first real R_uu row can be scored",
            "claim_allowed": False,
            "reason": f"live sector statuses: {live_status}.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4412_0",
            "decision": DECISION,
            "summary": "4412 maps the Ricci survivor vector to the correct proof type per slot. c_Gamma/Pleak and c_R2/M_R are positive-operator candidates but activation/sign/source/boundary clauses remain unsigned. spin/torsion has a stronger algebraic zero route through owned coframe/no independent connection, but the parent signature and counterbranch exclusion are not global. epsilon_Gsrc/E_profile is source-grammar/profile equality, not a no-hair field. Therefore the next best target is spin/torsion algebraic parent signature or the first P4/R_uu row.",
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
            "next_id": "NT4412_0",
            "target": NEXT_TARGET,
            "question": "Can the owned-coframe/no-independent-connection branch parent-sign spin/torsion zero on the same support, or must the first P4/R_uu torsion row be filled?",
            "preferred_route": "derive ordinary matter and spin action factorization through e_obs and omega_LC[e_obs], with no Gamma_ind/contorsion argument, no hypermomentum, same support and no torsion boundary/readout current.",
            "fallback_route": "fill the P4 axial/projective/shear torsion R_uu component row with units, uu/trace projection, source path, support certificate and no-cancellation guard.",
            "avoid": "pretending every survivor is a positive operator, using private owned-coframe spin zero as public proof, or ignoring the independent torsionful counterbranch.",
            "valid_for_claim": False,
        }
    ]


def compact_rows(rows: List[Dict[str, str]], fields: List[str]) -> List[Dict[str, str]]:
    return [{field: row.get(field, "") for field in fields} for row in rows]


def render_document(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    sectors: List[Dict[str, str]],
    first_ruu: List[Dict[str, object]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 428 PPC4161 transition: positive-operator sector map for Ricci survivor vector or first real Ruu row

Marker: `{MARKER}`

Generated: `{STAMP}`

Decision: `{DECISION}`

## Result

4412 says the survivor vector is not one proof problem:

- `c_Gamma/P_leak`: positive-operator candidate, activation blocked.
- `c_R2/M_R`: positive-operator/scalar-mode candidate, sign/mass/source blocked.
- `spin/torsion`: algebraic zero route is stronger than positive no-hair, but parent signature is unsigned.
- `epsilon_Gsrc/E_profile`: source-grammar/profile equality route, not a positive-operator field.
- `Lambda_eff/projector_boundary`: finite zero/bound row still required unless separately parent-silenced.

## Source Audit

{markdown_table(sources)}

## Derivations

{markdown_table(derivations)}

## Sector Map Gate

{markdown_table(compact_rows(sectors, ["component_id", "component", "route_type", "current_status", "map_ready", "operator_core_ready", "zero_schema_ready", "valid_for_claim"]))}

## First Real Ruu Row Requirements

{markdown_table(first_ruu)}

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
## 4412 local spine update: survivor vector split by proof type

Marker: `{MARKER}`

4412 maps the `R_uu` survivor vector into proof classes. `c_Gamma/P_leak` and `c_R2/M_R` are positive-operator candidates but not activated. `spin/torsion` has a stronger algebraic owned-coframe/no-independent-connection route, currently unsigned. `epsilon_Gsrc/E_profile` remains a source-grammar/profile-equality route. The next target is spin/torsion algebraic parent signature or the first P4/R_uu row.
""",
    )


def append_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4412 packet update: proof-type map for Ricci survivors

Marker: `{PACKET_MARKER}`

The local-GR branch now knows which mathematical weapon applies to each survivor slot. This avoids both fake universal no-hair and fake source closure. Best next shot: try to parent-sign the spin/torsion algebraic zero branch, because it may close by variable absence rather than data fitting.
""",
    )


def append_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4412 maps the local Ricci survivor vector by proof type. c_Gamma/Pleak and c_R2/M_R are positive-operator candidates but activation/sign/source/boundary clauses are unsigned. spin/torsion has a stronger algebraic zero route through owned coframe/no independent connection, but parent signature and counterbranch exclusion are not global. epsilon_Gsrc/E_profile is source-grammar/profile equality, not a positive-operator theorem. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4412 source register, derivation rows, positive-operator sector gate, first-real-Ruu row requirements, claim gates, decision, status, next target and validation CSV.",
            "Ricci_survivor_proof_type_map_ready_nonclaim",
            "Parent-sign spin/torsion algebraic zero or fill first P4/R_uu torsion row.",
            "Forcing all survivor slots into one no-hair theorem, using private spin zero as public proof, or leaving source-profile residual outside the vector.",
        ],
    )


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, object]]:
    sources = read_csv(paths["source_register"])
    sectors = read_csv(SECTOR_OUTPUT)
    first_ruu = read_csv(FIRST_RUU_ROW_REQUIREMENTS)
    live = {row["component"]: row for row in sectors if row["component_id"].startswith("POS4412_") and "_live_" in row["component_id"]}
    schema = [row for row in sectors if row["component_id"].startswith("POS4412_schema_")]
    checks = [
        ("VAL4412_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4412_1_source_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle was found"),
        ("VAL4412_2_cGamma_positive_blocked", live["c_Gamma/P_leak"]["current_status"] == "POSITIVE_OPERATOR_ACTIVATION_BLOCKED", "cGamma/Pleak is positive-operator candidate but blocked"),
        ("VAL4412_3_cR2_positive_blocked", live["c_R2/M_R"]["current_status"] == "POSITIVE_OPERATOR_ACTIVATION_BLOCKED", "cR2/MR is positive-operator candidate but blocked"),
        ("VAL4412_4_spin_algebraic_blocked", live["spin/torsion"]["current_status"] == "ALGEBRAIC_ZERO_ROUTE_CONDITIONAL_BLOCKED", "spin/torsion is routed to algebraic zero and remains unsigned"),
        ("VAL4412_5_source_profile_grammar_blocked", live["epsilon_Gsrc/E_profile"]["current_status"] == "SOURCE_GRAMMAR_ROUTE_REQUIRED_BLOCKED", "source/profile slot is grammar route, not operator route"),
        ("VAL4412_6_lambda_projector_finite_row", live["Lambda_eff/projector_boundary"]["current_status"] == "FINITE_SOURCE_ROW_REQUIRED", "Lambda/projector residual still needs finite row or separate silence"),
        ("VAL4412_7_schema_nonclaim", len(schema) == 4 and all(row["current_status"] == "SECTOR_ZERO_SCHEMA_READY_NONCLAIM" for row in schema), "four schema rows are wired but nonclaim"),
        ("VAL4412_8_first_Ruu_rows", len(first_ruu) == 6 and all(row["valid_for_claim"] == "False" for row in first_ruu), "first Ruu requirement rows preserved as nonclaim"),
        ("VAL4412_9_no_output_claims", not any(bool_text(row.get("claim_allowed", "False")) or bool_text(row.get("valid_for_claim", "False")) for row in sectors), "no generated gate output is claim-valid"),
        ("VAL4412_10_claim_row_exists", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claims register contains L-253"),
        ("VAL4412_11_spine_marker_exists", MARKER in text(SPINE_PATH), "spine update marker exists"),
        ("VAL4412_12_packet_marker_exists", PACKET_MARKER in text(PACKET_PATH), "packet update marker exists"),
        ("VAL4412_13_formal_doc_exists", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4412_14_post_doc_exists", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post-checkpoint doc exists with marker"),
        ("VAL4412_15_next_target_exists", paths["next_target"].exists() and NEXT_TARGET in text(paths["next_target"]), "next target file exists"),
        ("VAL4412_16_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
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
        "source_register": SOURCE_DIR / "P8_Y5_R2FR_4412_SOURCE_REGISTER.csv",
        "derivations": SOURCE_DIR / "P8_Y5_R2FR_4412_DERIVATIONS.csv",
        "claim_gates": SOURCE_DIR / "P8_Y5_R2FR_4412_CLAIM_GATES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4412_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4412_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4412_NEXT_TARGET.csv",
    }
    sources = source_rows()
    derivations = derivation_rows()
    first_ruu = first_ruu_requirement_rows()
    write_csv(paths["source_register"], sources)  # type: ignore[arg-type]
    write_csv(paths["derivations"], derivations)  # type: ignore[arg-type]
    write_csv(SECTOR_INPUT, sector_input_rows())  # type: ignore[arg-type]
    sectors = evaluate_sector_rows(SECTOR_INPUT)
    write_csv(SECTOR_OUTPUT, sectors)
    write_csv(FIRST_RUU_ROW_REQUIREMENTS, first_ruu)  # type: ignore[arg-type]
    claim_gates = claim_gate_rows(sectors)
    write_csv(paths["claim_gates"], claim_gates)  # type: ignore[arg-type]
    write_csv(paths["decision"], decision_rows())  # type: ignore[arg-type]
    write_csv(paths["status"], status_rows())  # type: ignore[arg-type]
    write_csv(paths["next_target"], next_target_rows())  # type: ignore[arg-type]

    doc = render_document(sources, derivations, sectors, first_ruu, claim_gates)
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
