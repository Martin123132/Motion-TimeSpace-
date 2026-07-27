from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from electric_u_parent_equation_gate import evaluate_equation_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4399"
CLAIM_ID = "L-240"
MARKER = "PPC4161_TRANSITION_PARENT_US_EQUATIONS_OR_FINITE_WARD_PAYLOAD_BOUND_4399"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_PARENT_US_EQUATIONS_OR_FINITE_WARD_PAYLOAD_BOUND_4399"
DECISION = "PURE_LINEAR_US_ACTION_OVERCONSTRAINS_COMPOSITE_OR_AUXILIARY_ROUTE_REQUIRED"
NEXT_TARGET = "4400-Y5-R2FR-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md"

FORMAL_PATH = FORMAL / "415-PPC4161-transition-parent-US-equations-or-finite-Ward-payload-bound.md"
DOC_PATH = POST / "4399-Y5-R2FR-transition-parent-US-equations-or-finite-Ward-payload-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4399_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

EQUATION_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4399_PARENT_US_EQUATION_INPUT.csv"
EQUATION_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4399_PARENT_US_EQUATION_OUTPUT.csv"
EQUATION_GATE_PATH = SCRIPT_DIR / "electric_u_parent_equation_gate.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4398 = SOURCE_DIR / "P8_Y5_R2FR_4398_NEXT_TARGET.csv"
WARD_OUTPUT_4398 = SOURCE_DIR / "P8_Y5_R2FR_4398_WARD_EXCHANGE_OUTPUT.csv"
ACTION_TEMPLATES_4388 = SOURCE_DIR / "P8_Y5_R2FR_4388_ACTION_TEMPLATES.csv"
ADOPTION_THEOREMS_4389 = SOURCE_DIR / "P8_Y5_R2FR_4389_ADOPTION_THEOREMS.csv"
U_THEOREMS_4390 = SOURCE_DIR / "P8_Y5_R2FR_4390_U_CONSTRUCTION_THEOREMS.csv"
U_OWNER_OUTPUT_4390 = SOURCE_DIR / "P8_Y5_R2FR_4390_U_OWNER_GATE_OUTPUT.csv"
STATIC_GATE_4391 = SOURCE_DIR / "P8_Y5_R2FR_4391_STATIC_TIME_GATE_OUTPUT.csv"
SOURCE_OWNER_4397 = SOURCE_DIR / "P8_Y5_R2FR_4397_SOURCE_OWNER_IMPROVEMENT_OUTPUT.csv"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4399_0_4398_next": (
        NEXT_4398,
        "4399-Y5-R2FR-transition-parent-US-equations-or-finite-Ward-payload-bound.md",
        "4398 handoff to parent U/S equations or finite Ward payload bounds.",
    ),
    "SRC4399_1_4398_ward": (
        WARD_OUTPUT_4398,
        "WG4398_0_noether_formula_ready",
        "4398 Ward gate output: formula ready, parent equations unsigned.",
    ),
    "SRC4399_2_4388_action": (
        ACTION_TEMPLATES_4388,
        "ACT4388_0_curvature_coupled_improvement",
        "4388 linear curvature-coupled U action template.",
    ),
    "SRC4399_3_4389_adoption": (
        ADOPTION_THEOREMS_4389,
        "AD4389_2_bianchi_ward_payload",
        "4389 Bianchi/Ward payload theorem.",
    ),
    "SRC4399_4_4390_U": (
        U_THEOREMS_4390,
        "U4390_3_owner_not_optional",
        "4390 owner-not-optional theorem.",
    ),
    "SRC4399_5_4390_owner_gate": (
        U_OWNER_OUTPUT_4390,
        "UOWN4390_0_electric_projector_candidate",
        "4390 U owner gate output.",
    ),
    "SRC4399_6_4391_static": (
        STATIC_GATE_4391,
        "ST4391_0_tau_coframe_formula",
        "4391 static/time gate output.",
    ),
    "SRC4399_7_4397_source_owner": (
        SOURCE_OWNER_4397,
        "SO4397_0_electric_U_improvement_route",
        "4397 source-owner improvement output.",
    ),
    "SRC4399_8_equation_gate": (
        EQUATION_GATE_PATH,
        "def evaluate_equation_rows",
        "New parent U/S equation gate.",
    ),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + block)


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
        write_text(path, text)
    with path.open("a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(row)


def source_register_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(text and needle in text)),
                "valid_for_claim": "False",
            }
        )
    return rows


def equation_derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "EQ4399_0_pure_linear_U_no_go",
            "statement": "If U^{mu alpha nu beta} is an independent field and the only U-dependent term is S_U=1/2 int sqrt(-g) U^{mu alpha nu beta}R_{mu alpha nu beta}, then variation with respect to U imposes the corresponding Riemann projection as an equation of motion.",
            "derivation": "delta_U S_U = 1/2 int sqrt(-g) delta U^{mu alpha nu beta} R_{mu alpha nu beta}. For arbitrary independent delta U in the allowed algebraic class, the Euler equation is projected R_{mu alpha nu beta}=0.",
            "new_information": "Pure linear independent U is a curvature multiplier, not a harmless improvement owner.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "EQ4399_1_electric_S_no_go",
            "statement": "For the electric projector with independent S^{ij}, the pure linear action makes the S equation the electric curvature slot E_{ij}=R_{0i0j}=0, up to projection terms.",
            "derivation": "Because U^{0i0j}=S^{ij}, varying S in the linear U·R action selects the electric curvature. Setting it to zero is not compatible with ordinary nonzero Newtonian curvature unless extra source/constitutive terms are present.",
            "new_information": "The electric route cannot use pure independent S as a multiplier and still recover local gravity.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "EQ4399_2_composite_route",
            "statement": "A viable low-post-hoc route is U=U[Phi] or S=S[Phi] as a composite parent functional, so the variation belongs to Phi equations rather than an independent curvature-killing U equation.",
            "derivation": "If U is composite, delta S_U/delta Phi contains R·delta U/delta Phi and contributes to parent Phi dynamics. The Ward identity can close on shell if those parent equations are signed and boundary flux is controlled.",
            "new_information": "Composite U/S avoids the curvature multiplier no-go but still needs a parent functional and equations.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "EQ4399_3_auxiliary_constitutive_route",
            "statement": "A second viable route is an auxiliary/constitutive U or S sector with quadratic, constraint, or source terms, so the U/S equation relates electric curvature to parent source data instead of setting it to zero.",
            "derivation": "Adding terms such as Q[U,S,Phi], lambda constraints, or source couplings changes E_U=R+delta Q/delta U=0 into a constitutive equation. This introduces extra coefficients and payloads that must be derived or bounded.",
            "new_information": "Auxiliary U/S can be viable, but it becomes a coefficient/payload problem rather than a free theorem-zero.",
            "valid_for_claim": "False",
        },
    ]


def equation_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "PEQ4399_0_pure_linear_independent_U",
            "route": "independent_U_in_pure_linear_UdotR_action",
            "parent_action_declared": "True",
            "variation_kind": "independent_linear_U",
            "U_independence_resolved": "False",
            "E_U_or_E_S_equation_written": "True",
            "no_curvature_multiplier_overconstraint": "False",
            "equation_has_source_or_constitutive_term": "False",
            "compatible_with_nonzero_local_curvature": "False",
            "Ward_exchange_formula_linked": "True",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_vector_declared": "True",
            "EM_double_count_guard": "False",
            "finite_bound_fallback_declared": "True",
            "parent_authority": "NO_AUTHORITY_PURE_LINEAR_CURVATURE_MULTIPLIER",
            "source_path": str(ACTION_TEMPLATES_4388),
            "input_valid_for_claim": "False",
            "notes": "Pure linear independent U imposes curvature projection zero.",
        },
        {
            "candidate_id": "PEQ4399_1_pure_linear_independent_S_electric",
            "route": "independent_S_in_electric_projector_UdotR_action",
            "parent_action_declared": "True",
            "variation_kind": "independent_linear_S_electric",
            "U_independence_resolved": "False",
            "E_U_or_E_S_equation_written": "True",
            "no_curvature_multiplier_overconstraint": "False",
            "equation_has_source_or_constitutive_term": "False",
            "compatible_with_nonzero_local_curvature": "False",
            "Ward_exchange_formula_linked": "True",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_vector_declared": "True",
            "EM_double_count_guard": "False",
            "finite_bound_fallback_declared": "True",
            "parent_authority": "NO_AUTHORITY_ELECTRIC_CURVATURE_MULTIPLIER",
            "source_path": str(U_THEOREMS_4390),
            "input_valid_for_claim": "False",
            "notes": "Pure electric S equation imposes E_ij=0 unless extra constitutive/source terms exist.",
        },
        {
            "candidate_id": "PEQ4399_2_composite_U_parent_functional",
            "route": "composite_U_of_parent_fields",
            "parent_action_declared": "True",
            "variation_kind": "composite_U_of_Phi",
            "U_independence_resolved": "True",
            "E_U_or_E_S_equation_written": "False",
            "no_curvature_multiplier_overconstraint": "True",
            "equation_has_source_or_constitutive_term": "False",
            "compatible_with_nonzero_local_curvature": "True",
            "Ward_exchange_formula_linked": "True",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_vector_declared": "True",
            "EM_double_count_guard": "False",
            "finite_bound_fallback_declared": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_COMPOSITE_U_FUNCTIONAL",
            "source_path": str(SOURCE_OWNER_4397),
            "input_valid_for_claim": "False",
            "notes": "Best theorem route if a parent U[Phi] functional and Phi equations can be signed.",
        },
        {
            "candidate_id": "PEQ4399_3_auxiliary_constitutive_US",
            "route": "auxiliary_or_constitutive_US_with_source_terms",
            "parent_action_declared": "True",
            "variation_kind": "auxiliary_constitutive_U_or_S",
            "U_independence_resolved": "True",
            "E_U_or_E_S_equation_written": "True",
            "no_curvature_multiplier_overconstraint": "True",
            "equation_has_source_or_constitutive_term": "True",
            "compatible_with_nonzero_local_curvature": "True",
            "Ward_exchange_formula_linked": "True",
            "boundary_flux_terms_declared": "False",
            "pressure_curvature_payload_vector_declared": "True",
            "EM_double_count_guard": "False",
            "finite_bound_fallback_declared": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_AUXILIARY_US_CONSTITUTIVE_LAW",
            "source_path": str(ACTION_TEMPLATES_4388),
            "input_valid_for_claim": "False",
            "notes": "Viable if coefficients/source terms are derived; otherwise finite-payload route.",
        },
    ]


def finite_payload_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "payload_id": "FP4399_0_composite_functional",
            "quantity": "U[Phi] or S[Phi] functional derivative",
            "needed": "parent functional map and Phi equations",
            "status": "MISSING_COMPOSITE_PARENT_FUNCTIONAL",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4399_1_auxiliary_coefficients",
            "quantity": "quadratic/constraint/source coefficients in auxiliary U/S law",
            "needed": "Z_U/M_U/source coupling or sigma/lambda constitutive terms with units",
            "status": "MISSING_AUXILIARY_COEFFICIENTS",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4399_2_Ward_exchange",
            "quantity": "J_U^nu finite norm or on-shell cancellation certificate",
            "needed": "parent equations or finite Bianchi payload bound",
            "status": "MISSING_WARD_PAYLOAD_BOUND",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4399_3_PPN_stress_curvature",
            "quantity": "pressure/aniso and curvature commutator payloads",
            "needed": "same W_H support projection into local PPN/curvature bounds",
            "status": "MISSING_PPN_CURVATURE_PAYLOADS",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4399_4_EM_overlap",
            "quantity": "Maxwell/Hodge stress overlap with U/S sector",
            "needed": "disjoint-sector theorem or finite overlap bound",
            "status": "MISSING_EM_DOUBLE_COUNT_GUARD",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "pure_linear_U": "independent pure U·R action overconstrains curvature",
        "composite_U": "composite parent U[Phi] route is viable but functional and equations are unsigned",
        "auxiliary_US": "auxiliary/constitutive route is viable but coefficients and payload bounds are missing",
        "Ward_payload": "on-shell Ward cancellation or finite J_U bound is not sourced",
        "local_GR_Newton_PPN": "without parent U/S equations or finite payload vector, local GR/Newton/PPN cannot be claimed",
    }
    return [
        {
            "gate_id": f"CG4399_{index}_{arena}",
            "arena": arena,
            "claim_allowed": "False",
            "reason": reason,
            "valid_for_claim": "False",
        }
        for index, (arena, reason) in enumerate(reasons.items())
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4399_0",
            "decision": DECISION,
            "summary": "4399 derives an important no-go: pure independent linear U·R or electric S·E actions make U/S a curvature multiplier and overconstrain local gravity. The viable routes are now sharply separated: composite U/S as parent functionals with signed parent equations, or auxiliary/constitutive U/S with sourced coefficients and finite payload bounds. This blocks a tempting but bad shortcut while preserving two serious field-theory routes.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": DECISION,
            "timestamp_utc": STAMP,
            "summary": "pure linear U/S action no-go derived; composite or auxiliary routes remain open but unsigned.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4399_0",
            "target": NEXT_TARGET,
            "question": "Can we construct a parent composite U/S functional, or should we build the finite payload vector runner now?",
            "preferred_route": "try composite U/S parent functional first, because it avoids curvature-multiplier overconstraint with fewer new coefficients.",
            "fallback_route": "build a finite payload vector runner for R_S, J_U, pressure/aniso, curvature/boundary, lambda/kernel and EM-overlap terms.",
            "avoid": "returning to pure independent linear U·R as if it were a viable local-GR closure action.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    equation_output: List[Dict[str, str]],
    payloads: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 415 PPC4161 transition: parent U/S equations or finite Ward payload bound

Marker: `{MARKER}`

## Result

4399 derives a useful no-go and separates the viable routes.

The tempting parent action

`S_U = 1/2 int sqrt(-g) U^{{mu alpha nu beta}} R_{{mu alpha nu beta}}`

cannot use an independent pure-linear `U` as the whole story: variation with respect to `U` imposes the corresponding curvature projection. In the electric branch, independent pure-linear `S^{{ij}}` imposes the electric curvature slot `R_{{0i0j}}=0`. That is not local gravity; it is an overconstraint.

So the two serious routes are now:

1. composite `U/S = U/S[Phi]`, where Ward closes through parent `Phi` equations;
2. auxiliary/constitutive `U/S`, where extra source or quadratic terms prevent curvature-multiplier overconstraint but introduce coefficients and finite payloads.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Parent U/S Equation Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"
    text += "## Parent Equation Gate Output\n\n"
    for row in equation_output:
        text += f"- `{row['candidate_id']}`: equation_ready=`{row['equation_ready']}`, overconstraint_trap=`{row['overconstraint_trap']}`, ward_ready=`{row['ward_ready']}`, payload_ready=`{row['payload_ready']}`, certificate_ready=`{row['parent_equation_certificate_ready']}`, status=`{row['current_status']}`.\n"
    text += "\n## Finite Payload Contract\n\n"
    for row in payloads:
        text += f"- `{row['payload_id']}`: `{row['quantity']}` needs {row['needed']} — status `{row['status']}`.\n"
    text += "\n## Claim Gates\n\n"
    for row in gates:
        text += f"- `{row['arena']}`: claim_allowed=`{row['claim_allowed']}` because {row['reason']}.\n"
    text += "\n## Decision\n\n"
    text += f"{decisions[0]['summary']}\n\n"
    text += "## Next Target\n\n"
    text += f"- `{next_targets[0]['target']}`: {next_targets[0]['question']}\n"
    write_text(FORMAL_PATH, text)


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    write_text(
        DOC_PATH,
        f"""# 4399 Y5 R2FR: parent U/S equations or finite Ward payload bound

Marker: `{MARKER}`

## Private checkpoint

{decisions[0]['summary']}

## Next

{next_targets[0]['target']}

{next_targets[0]['question']}
""",
    )


def write_spine_update() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4399 local spine update: pure linear U/S no-go

Marker: `{MARKER}`

Spine update: a pure independent linear `U·R` or electric `S·E` action overconstrains curvature and cannot be the local-GR closure action. The viable electric-improvement routes are now either composite `U/S[Phi]` with parent field equations closing Ward, or auxiliary/constitutive `U/S` with derived source terms/coefficient payloads. If neither closes, the correct fallback is a finite payload vector runner.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4399 packet update: parent U/S equation no-go

Marker: `{PACKET_MARKER}`

Packet update: 4399 blocks pure independent linear `U·R` as a curvature-multiplier overconstraint and routes the work to composite `U/S[Phi]` or auxiliary/finite-payload branches.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4399 derives a no-go for the tempting pure independent linear U/S parent action. If U is independent in S_U=1/2 int sqrt(-g) U R, variation with respect to U imposes the corresponding curvature projection; in the electric branch independent S imposes the electric curvature slot R_0i0j=0. This overconstrains local gravity rather than deriving it. The viable routes are now composite U/S[Phi] with signed parent equations, or auxiliary/constitutive U/S with sourced coefficients and finite payload bounds. No local-GR/Newton/PPN/R10 claim fires.",
            "4399 source register, parent U/S equation derivation rows, parent equation gate input/output, finite payload contract rows, claim gates, decision, status, next target and validation CSV.",
            "pure_linear_US_action_overconstrains_composite_or_auxiliary_route_required_nonclaim",
            "Construct composite U/S parent functional or build finite payload vector runner.",
            "Returning to pure independent linear U.R as a closure action, ignoring curvature multiplier equation, or hiding auxiliary coefficients/payloads.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4399_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4399_PARENT_US_EQUATION_DERIVATIONS.csv")
    equation_output = read_csv(EQUATION_OUTPUT_PATH)
    payloads = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4399_FINITE_PAYLOAD_CONTRACT.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4399_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4399_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4399_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4399_2_pure_U_nogo_written", any(row["derivation_id"] == "EQ4399_0_pure_linear_U_no_go" for row in derivations), "pure linear U no-go derived")
    add("VAL4399_3_pure_S_nogo_written", any(row["derivation_id"] == "EQ4399_1_electric_S_no_go" for row in derivations), "pure electric S no-go derived")
    add("VAL4399_4_composite_route_written", any(row["derivation_id"] == "EQ4399_2_composite_route" for row in derivations), "composite route retained")
    add("VAL4399_5_auxiliary_route_written", any(row["derivation_id"] == "EQ4399_3_auxiliary_constitutive_route" for row in derivations), "auxiliary route retained")
    add("VAL4399_6_equation_gate_nonclaim", all(row["valid_for_claim"] == "False" for row in equation_output), "equation gate rows remain nonclaim")
    add("VAL4399_7_pure_U_trap_detected", any(row["candidate_id"] == "PEQ4399_0_pure_linear_independent_U" and row["overconstraint_trap"] == "True" for row in equation_output), "pure U overconstraint trap detected")
    add("VAL4399_8_pure_S_trap_detected", any(row["candidate_id"] == "PEQ4399_1_pure_linear_independent_S_electric" and row["overconstraint_trap"] == "True" for row in equation_output), "pure S overconstraint trap detected")
    add("VAL4399_9_auxiliary_equation_ready", any(row["candidate_id"] == "PEQ4399_3_auxiliary_constitutive_US" and row["equation_ready"] == "True" for row in equation_output), "auxiliary equation form is ready")
    add("VAL4399_10_payload_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in payloads), "finite payload contract remains nonclaim")
    add("VAL4399_11_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4399_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4399_13_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4399_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4399_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4399_16_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4399_17_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4399_18_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4399_19_equation_gate_exists", EQUATION_GATE_PATH.exists() and "def evaluate_equation_rows" in read_text(EQUATION_GATE_PATH), "parent equation gate exists")
    add("VAL4399_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = equation_derivation_rows()
    equation_inputs = equation_input_rows()
    payloads = finite_payload_contract_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4399_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4399_PARENT_US_EQUATION_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4399_FINITE_PAYLOAD_CONTRACT.csv": payloads,
        "P8_Y5_R2FR_4399_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4399_DECISION.csv": decisions,
        "P8_Y5_R2FR_4399_STATUS.csv": statuses,
        "P8_Y5_R2FR_4399_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [EQUATION_INPUT_PATH]
    write_csv(EQUATION_INPUT_PATH, equation_inputs)
    equation_output = evaluate_equation_rows(EQUATION_INPUT_PATH)
    write_csv(EQUATION_OUTPUT_PATH, equation_output)
    csv_paths.append(EQUATION_OUTPUT_PATH)

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, derivations, equation_output, payloads, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
