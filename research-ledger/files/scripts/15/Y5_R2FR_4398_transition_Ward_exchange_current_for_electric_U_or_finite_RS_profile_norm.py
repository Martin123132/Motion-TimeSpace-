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

from electric_u_ward_exchange_gate import evaluate_ward_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4398"
CLAIM_ID = "L-239"
MARKER = "PPC4161_TRANSITION_WARD_EXCHANGE_CURRENT_FOR_ELECTRIC_U_OR_FINITE_RS_PROFILE_NORM_4398"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_WARD_EXCHANGE_CURRENT_FOR_ELECTRIC_U_OR_FINITE_RS_PROFILE_NORM_4398"
DECISION = "WARD_FORMULA_DERIVED_PARENT_US_EQUATIONS_AND_PAYLOAD_BOUNDS_UNSIGNED"
NEXT_TARGET = "4399-Y5-R2FR-transition-parent-US-equations-or-finite-Ward-payload-bound.md"

FORMAL_PATH = FORMAL / "414-PPC4161-transition-Ward-exchange-current-for-electric-U-or-finite-RS-profile-norm.md"
DOC_PATH = POST / "4398-Y5-R2FR-transition-Ward-exchange-current-for-electric-U-or-finite-RS-profile-norm.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4398_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

WARD_INPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4398_WARD_EXCHANGE_INPUT.csv"
WARD_OUTPUT_PATH = SOURCE_DIR / "P8_Y5_R2FR_4398_WARD_EXCHANGE_OUTPUT.csv"
WARD_GATE_PATH = SCRIPT_DIR / "electric_u_ward_exchange_gate.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

ADOPTION_THEOREMS_4389 = SOURCE_DIR / "P8_Y5_R2FR_4389_ADOPTION_THEOREMS.csv"
COMPONENT_PAYLOADS_4389 = SOURCE_DIR / "P8_Y5_R2FR_4389_COMPONENT_PAYLOADS.csv"
ACTION_TEMPLATES_4388 = SOURCE_DIR / "P8_Y5_R2FR_4388_ACTION_TEMPLATES.csv"
U_THEOREMS_4390 = SOURCE_DIR / "P8_Y5_R2FR_4390_U_CONSTRUCTION_THEOREMS.csv"
U_PROJECTIONS_4390 = SOURCE_DIR / "P8_Y5_R2FR_4390_COMPONENT_PROJECTIONS.csv"
SOURCE_OWNER_4397 = SOURCE_DIR / "P8_Y5_R2FR_4397_SOURCE_OWNER_IMPROVEMENT_OUTPUT.csv"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4398_0_4397_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4397_NEXT_TARGET.csv",
        "4398-Y5-R2FR-transition-Ward-exchange-current-for-electric-U-or-finite-RS-profile-norm.md",
        "4397 handoff to Ward/exchange current or finite payload bounds.",
    ),
    "SRC4398_1_4389_ward": (
        ADOPTION_THEOREMS_4389,
        "AD4389_2_bianchi_ward_payload",
        "4389 conservation gate for U action adoption.",
    ),
    "SRC4398_2_4389_payload": (
        COMPONENT_PAYLOADS_4389,
        "PAY4389_5_conservation",
        "4389 retained nabla_mu DeltaT payload.",
    ),
    "SRC4398_3_4388_action": (
        ACTION_TEMPLATES_4388,
        "ACT4388_0_curvature_coupled_improvement",
        "4388 curvature-coupled U action template.",
    ),
    "SRC4398_4_4390_U": (
        U_THEOREMS_4390,
        "U4390_3_owner_not_optional",
        "4390 owner-not-optional theorem for electric U.",
    ),
    "SRC4398_5_4390_projection": (
        U_PROJECTIONS_4390,
        "PROJ4390_0_electric_U",
        "4390 electric U projection payload split.",
    ),
    "SRC4398_6_4397_source_owner": (
        SOURCE_OWNER_4397,
        "SO4397_0_electric_U_improvement_route",
        "4397 source-owner improvement route remains conservation unsigned.",
    ),
    "SRC4398_7_ward_gate": (
        WARD_GATE_PATH,
        "def evaluate_ward_rows",
        "New executable Ward/exchange-current gate.",
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


def ward_derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "WARD4398_0_noether_identity",
            "statement": "For a diffeomorphism-invariant parent action S_U[g,U,Phi]=1/2 int sqrt(-g) U^{mu alpha nu beta}[Phi] R_{mu alpha nu beta}, the metric Hilbert tensor obeys a Noether identity: nabla_mu DeltaT_U^{mu nu} is cancelled by Euler-Lagrange terms for U/Phi plus boundary symplectic flux.",
            "derivation": "Under delta_xi g_{mu nu}=2 nabla_(mu xi_{nu)} and delta_xi U=L_xi U, diffeomorphism invariance gives 0=delta_xi S_U=int sqrt(-g)[-xi_nu nabla_mu DeltaT_U^{mu nu}+E_U L_xi U+E_Phi L_xi Phi]+boundary after integrating by parts.",
            "new_information": "The Ward route is formula-ready: conservation follows only on shell with owned U/Phi equations and silent boundary flux.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "WARD4398_1_exchange_current_definition",
            "statement": "If U/S is not on shell, define the retained exchange payload by J_U^nu:=nabla_mu DeltaT_U^{mu nu}; claim safety requires J_U^nu=0 or a parent sector with opposite divergence.",
            "derivation": "The Noether identity moves nonzero E_U L_xi U and E_Phi L_xi Phi terms into the divergence equation. These are not ignorable; they are the source exchange between the electric improvement and the parent fields.",
            "new_information": "Fixed or post-readout U is not a harmless improvement; it produces a measurable Bianchi payload unless bounded.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "WARD4398_2_electric_branch_ceiling",
            "statement": "For the electric projector, the density slot can stay useful while Ward safety depends on parent S/u equations, tau/coframe variation, boundary flux silence, curvature payload, pressure/aniso payload, and EM overlap guard.",
            "derivation": "4390 gives U^{0i0j}=S^{ij}; 4389 says adopting the action brings every Hilbert component and the Ward identity, not just density. Therefore the electric branch is safe only as a complete parent sector or as a finite residual vector.",
            "new_information": "The next gate is not another R_S algebra row; it is the parent U/S dynamics or finite Ward/payload bounds.",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "WARD4398_3_finite_fallback",
            "statement": "If parent U/S equations do not close, the finite fallback vector is |R_S| plus |J_U|, pressure/aniso, curvature, boundary, lambda, kernel and EM-overlap payloads on one W_H/tau/coframe support.",
            "derivation": "Bianchi, PPN and local Newton tests see the total retained payload, so cancellation between unknown branches is forbidden. Every component must be zero by theorem or bounded by sourced rows.",
            "new_information": "The fallback is now a finite vector, not a vague local-GR failure.",
            "valid_for_claim": "False",
        },
    ]


def ward_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "WG4398_0_noether_formula_ready",
            "route": "diffeomorphism_noether_identity_for_parent_U_action",
            "diffeomorphism_invariant_parent_action": "True",
            "metric_hilbert_variation_included": "True",
            "U_or_S_field_equations_owned": "False",
            "tau_coframe_variation_owned": "False",
            "exchange_current_formula_written": "True",
            "divergence_cancels_on_shell": "False",
            "boundary_symplectic_flux_silent": "False",
            "curvature_commutator_payload_bounded": "False",
            "pressure_aniso_payload_bounded": "False",
            "EM_double_count_guard": "False",
            "same_support_as_R_S_row": "False",
            "no_fixed_post_readout_U": "True",
            "parent_authority": "CONDITIONAL_NOETHER_IDENTITY_PARENT_EQUATIONS_UNSIGNED",
            "source_path": str(ADOPTION_THEOREMS_4389),
            "input_valid_for_claim": "False",
            "notes": "Noether formula is derived, but U/S parent equations and payload bounds are unsigned.",
        },
        {
            "candidate_id": "WG4398_1_fixed_U_trap",
            "route": "fixed_or_post_readout_U_adoption",
            "diffeomorphism_invariant_parent_action": "False",
            "metric_hilbert_variation_included": "True",
            "U_or_S_field_equations_owned": "False",
            "tau_coframe_variation_owned": "False",
            "exchange_current_formula_written": "False",
            "divergence_cancels_on_shell": "False",
            "boundary_symplectic_flux_silent": "False",
            "curvature_commutator_payload_bounded": "False",
            "pressure_aniso_payload_bounded": "False",
            "EM_double_count_guard": "False",
            "same_support_as_R_S_row": "False",
            "no_fixed_post_readout_U": "False",
            "parent_authority": "NO_PARENT_AUTHORITY_FIXED_U",
            "source_path": str(COMPONENT_PAYLOADS_4389),
            "input_valid_for_claim": "False",
            "notes": "Deliberate trap: fixed post-readout U creates an exchange payload instead of proving conservation.",
        },
        {
            "candidate_id": "WG4398_2_future_parent_exchange_template",
            "route": "future_parent_US_equations_and_exchange_current",
            "diffeomorphism_invariant_parent_action": "True",
            "metric_hilbert_variation_included": "True",
            "U_or_S_field_equations_owned": "False",
            "tau_coframe_variation_owned": "False",
            "exchange_current_formula_written": "True",
            "divergence_cancels_on_shell": "False",
            "boundary_symplectic_flux_silent": "False",
            "curvature_commutator_payload_bounded": "False",
            "pressure_aniso_payload_bounded": "False",
            "EM_double_count_guard": "False",
            "same_support_as_R_S_row": "False",
            "no_fixed_post_readout_U": "True",
            "parent_authority": "MISSING_PARENT_SIGNED_US_EQUATIONS_AND_EXCHANGE",
            "source_path": str(ACTION_TEMPLATES_4388),
            "input_valid_for_claim": "False",
            "notes": "Template for 4399: sign parent U/S equations or fill finite exchange-current bounds.",
        },
    ]


def finite_payload_rows() -> List[Dict[str, str]]:
    return [
        {
            "payload_id": "FP4398_0_R_S_profile",
            "quantity": "||R_S||_weighted/M_H",
            "source_needed": "source-backed finite R_S profile or PARENT_SIGNED theorem-zero",
            "current_status": "MISSING_NUMERIC_PROFILE_NORM",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4398_1_Ward_exchange",
            "quantity": "||J_U^nu|| or exchange-current cancellation certificate",
            "source_needed": "parent U/S equations or finite Bianchi payload bound",
            "current_status": "WARD_FORMULA_READY_PARENT_EQUATIONS_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4398_2_pressure_aniso",
            "quantity": "DeltaT_U^{ij} PPN stress projection",
            "source_needed": "static theorem or numeric PPN stress bound",
            "current_status": "MISSING_PRESSURE_ANISO_BOUND",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4398_3_curvature_boundary",
            "quantity": "curvature commutator plus boundary symplectic flux",
            "source_needed": "curvature remainder and boundary flux rows on same W_H support",
            "current_status": "MISSING_CURVATURE_BOUNDARY_ROWS",
            "valid_for_claim": "False",
        },
        {
            "payload_id": "FP4398_4_EM_overlap",
            "quantity": "overlap between electric-U stress and Maxwell/Hodge stress",
            "source_needed": "EM double-count guard or disjoint sector theorem",
            "current_status": "MISSING_EM_DOUBLE_COUNT_GUARD",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    reasons = {
        "Ward_exchange": "Noether formula is ready but parent U/S equations, tau/coframe variation and boundary flux silence are unsigned",
        "fixed_U": "fixed or post-readout U creates an exchange payload and is explicitly blocked",
        "finite_payload_vector": "R_S, J_U, pressure/aniso, curvature/boundary and EM-overlap payloads are not numerically bounded",
        "Newton_local_GR": "Bianchi/Ward consistency is not claim-valid, so local GR/Newton reduction remains open",
        "PPN_R10_WEP_clock": "stress, coupling and same-frame projection payloads remain upstream nonclaim",
    }
    return [
        {
            "gate_id": f"CG4398_{index}_{arena}",
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
            "decision_id": "DEC4398_0",
            "decision": DECISION,
            "summary": "4398 derives the Ward/exchange-current formula for the electric U/S route. A diffeomorphism-invariant parent U action conserves its Hilbert stress only on shell, with U/S and parent field equations included and boundary symplectic flux silent. If U is fixed or post-readout, the divergence becomes a real exchange-current payload. The route is now formula-ready but not claim-ready; the next target is parent U/S equations or finite Ward/payload bounds.",
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
            "summary": "Ward formula derived; parent U/S equations and finite payload bounds remain unsigned.",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4398_0",
            "target": NEXT_TARGET,
            "question": "Can parent U/S equations close the Ward identity, or do we need a finite exchange-current/payload bound vector?",
            "preferred_route": "derive parent U/S equations from the curvature-coupled electric U action and show the Noether exchange cancels on shell.",
            "fallback_route": "source finite bounds for J_U, pressure/aniso, curvature/boundary, EM-overlap, lambda/kernel and R_S payloads on one W_H support.",
            "avoid": "using diffeomorphism invariance alone as a conservation proof while U/S equations and boundary flux are unsigned.",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    derivations: List[Dict[str, str]],
    ward_output: List[Dict[str, str]],
    payloads: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# 414 PPC4161 transition: Ward exchange current for electric U or finite R_S profile norm

Marker: `{MARKER}`

## Result

4398 derives the Ward/exchange-current formula for the electric `U/S` route.

For the parent action

`S_U = 1/2 int sqrt(-g) U^{{mu alpha nu beta}} R_{{mu alpha nu beta}}`,

diffeomorphism invariance gives a Noether identity, not a free pass:

`nabla_mu DeltaT_U^{{mu nu}} = J_U^nu`,

where `J_U^nu` is built from unsatisfied parent `U/S/Phi` equations and boundary symplectic flux. Thus conservation closes only if parent `U/S` equations and boundary silence are signed; otherwise `J_U` is a finite payload that must be bounded.

## Source Register

| source | exists | needle found | role |
|---|---:|---:|---|
"""
    for row in sources:
        text += f"| `{row['source_id']}` | {row['path_exists']} | {row['needle_found']} | {row['role']} |\n"
    text += "\n## Ward Derivation\n\n"
    for row in derivations:
        text += f"### {row['derivation_id']}\n\n- Statement: {row['statement']}\n- Derivation: {row['derivation']}\n- New information: {row['new_information']}\n\n"
    text += "## Ward Gate Output\n\n"
    for row in ward_output:
        text += f"- `{row['candidate_id']}`: formula_ready=`{row['formula_ready']}`, on_shell_ready=`{row['on_shell_ready']}`, payload_ready=`{row['payload_ready']}`, ward_certificate_ready=`{row['ward_certificate_ready']}`, authority=`{row['exchange_authority']}`.\n"
    text += "\n## Finite Payload Fallback\n\n"
    for row in payloads:
        text += f"- `{row['payload_id']}`: `{row['quantity']}` needs {row['source_needed']} — status `{row['current_status']}`.\n"
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
        f"""# 4398 Y5 R2FR: Ward exchange current for electric U or finite R_S profile norm

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
## 4398 local spine update: Ward/exchange current for electric U

Marker: `{MARKER}`

Spine update: the electric `U/S` route now has its Ward law. Diffeomorphism invariance gives `nabla_mu DeltaT_U^{{mu nu}}=J_U^nu`, where `J_U` is the exchange payload from unsatisfied `U/S/Phi` equations and boundary symplectic flux. Conservation is claim-safe only if parent `U/S` equations close on shell and boundary flux is silent; otherwise finite `J_U`, pressure/aniso, curvature/boundary, EM-overlap, lambda/kernel and `R_S` payload rows are required.
""",
    )


def write_packet_update() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4398 packet update: Ward/exchange current

Marker: `{PACKET_MARKER}`

Packet update: 4398 derives the Ward/exchange formula and blocks the fixed/post-readout `U` trap. No local-GR claim fires because parent `U/S` equations and finite payload bounds are not signed.
""",
    )


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4398 derives the Ward/exchange-current formula for the electric U/S improvement route. For a diffeomorphism-invariant parent action S_U=1/2 int sqrt(-g) U R, the Hilbert stress is conserved only on shell with parent U/S/Phi equations and silent boundary symplectic flux. If U is fixed or post-readout, nabla_mu DeltaT_U^{mu nu} becomes a real exchange-current payload J_U^nu. This advances the local-GR route by turning Bianchi consistency into an explicit gate and finite fallback vector, but no Newton/GR/PPN/R10 claim fires.",
            "4398 source register, Ward derivation rows, Ward exchange gate input/output, finite payload fallback rows, claim gates, decision, status, next target and validation CSV.",
            "Ward_exchange_formula_derived_parent_US_equations_unsigned_nonclaim",
            "Derive parent U/S equations that close the Ward identity, or source finite J_U/profile/stress payload bounds.",
            "Claiming conservation from diffeomorphism invariance alone, using fixed/post-readout U, ignoring boundary symplectic flux, or cancelling unknown payloads.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4398_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4398_WARD_DERIVATIONS.csv")
    ward_output = read_csv(WARD_OUTPUT_PATH)
    payloads = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4398_FINITE_PAYLOAD_REQUIREMENTS.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4398_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": str(bool(passed)), "detail": detail})

    add("VAL4398_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4398_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited needle resolves")
    add("VAL4398_2_noether_identity_written", any(row["derivation_id"] == "WARD4398_0_noether_identity" for row in derivations), "Noether Ward identity derived")
    add("VAL4398_3_exchange_current_written", any(row["derivation_id"] == "WARD4398_1_exchange_current_definition" for row in derivations), "exchange current definition derived")
    add("VAL4398_4_fallback_vector_written", any(row["derivation_id"] == "WARD4398_3_finite_fallback" for row in derivations), "finite fallback vector derived")
    add("VAL4398_5_ward_gate_nonclaim", all(row["valid_for_claim"] == "False" for row in ward_output), "Ward gate rows remain nonclaim")
    add("VAL4398_6_formula_ready", any(row["candidate_id"] == "WG4398_0_noether_formula_ready" and row["formula_ready"] == "True" for row in ward_output), "Noether formula row is ready")
    add("VAL4398_7_on_shell_unsigned", any(row["candidate_id"] == "WG4398_0_noether_formula_ready" and row["on_shell_ready"] == "False" for row in ward_output), "parent equations remain unsigned")
    add("VAL4398_8_fixed_U_trap_blocked", any(row["candidate_id"] == "WG4398_1_fixed_U_trap" and row["formula_ready"] == "False" and row["valid_for_claim"] == "False" for row in ward_output), "fixed U trap is blocked")
    add("VAL4398_9_payload_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in payloads), "finite payload rows remain nonclaim")
    add("VAL4398_10_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4398_11_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4398_12_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4398_13_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4398_14_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4398_15_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add("VAL4398_16_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4398_17_rows_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows remain nonclaim")
    add("VAL4398_18_ward_gate_exists", WARD_GATE_PATH.exists() and "def evaluate_ward_rows" in read_text(WARD_GATE_PATH), "Ward gate exists")
    add("VAL4398_19_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generator cleanup")
    return validations


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_register_rows()
    derivations = ward_derivation_rows()
    ward_inputs = ward_input_rows()
    payloads = finite_payload_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4398_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4398_WARD_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4398_FINITE_PAYLOAD_REQUIREMENTS.csv": payloads,
        "P8_Y5_R2FR_4398_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4398_DECISION.csv": decisions,
        "P8_Y5_R2FR_4398_STATUS.csv": statuses,
        "P8_Y5_R2FR_4398_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = [WARD_INPUT_PATH]
    write_csv(WARD_INPUT_PATH, ward_inputs)
    ward_output = evaluate_ward_rows(WARD_INPUT_PATH)
    write_csv(WARD_OUTPUT_PATH, ward_output)
    csv_paths.append(WARD_OUTPUT_PATH)

    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, derivations, ward_output, payloads, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
