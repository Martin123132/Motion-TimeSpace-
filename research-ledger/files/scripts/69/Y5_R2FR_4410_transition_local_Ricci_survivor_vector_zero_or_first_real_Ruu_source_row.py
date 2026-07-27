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

from lambda_curvature_source_gate import evaluate_bound_rows as evaluate_lambda_bound_rows  # noqa: E402
from lambda_curvature_source_gate import read_csv, write_csv  # noqa: E402
from ricci_survivor_vector_gate import evaluate_aggregate_rows, evaluate_component_rows  # noqa: E402
from ricci_uu_source_bound_runner import evaluate_bound_rows as evaluate_ricci_bound_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4410"
CLAIM_ID = "L-251"
MARKER = "PPC4161_TRANSITION_LOCAL_RICCI_SURVIVOR_VECTOR_ZERO_OR_FIRST_REAL_RUU_SOURCE_ROW_4410"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_LOCAL_RICCI_SURVIVOR_VECTOR_ZERO_OR_FIRST_REAL_RUU_SOURCE_ROW_4410"
DECISION = "LOCAL_RICCI_SURVIVOR_VECTOR_EXACT_CONTRACT_AND_RUNNER_READY_PARENT_ZERO_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4411-Y5-R2FR-transition-parent-Ward-nohair-for-Ricci-survivor-vector-or-first-real-Ruu-row.md"

FORMAL_PATH = FORMAL / "426-PPC4161-transition-local-Ricci-survivor-vector-zero-or-first-real-Ruu-source-row.md"
DOC_PATH = POST / "4410-Y5-R2FR-transition-local-Ricci-survivor-vector-zero-or-first-real-Ruu-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4410_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SURVIVOR_GATE_PATH = SCRIPT_DIR / "ricci_survivor_vector_gate.py"
LOCAL_GATE_PATH = SCRIPT_DIR / "local_cosmological_residual_gate.py"
RICCI_RUNNER_PATH = SCRIPT_DIR / "ricci_uu_source_bound_runner.py"
LAMBDA_GATE_PATH = SCRIPT_DIR / "lambda_curvature_source_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4410_transition_local_Ricci_survivor_vector_zero_or_first_real_Ruu_source_row.py"

COMPONENT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_RICCI_SURVIVOR_COMPONENT_INPUT.csv"
COMPONENT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_RICCI_SURVIVOR_COMPONENT_OUTPUT.csv"
AGGREGATE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_RICCI_SURVIVOR_AGGREGATE_INPUT.csv"
AGGREGATE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_RICCI_SURVIVOR_AGGREGATE_OUTPUT.csv"
RICCI_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_RICCI_SOURCE_BOUND_INPUT.csv"
RICCI_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_RICCI_SOURCE_BOUND_OUTPUT.csv"
LAMBDA_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_LAMBDA_FROM_RUU_INPUT.csv"
LAMBDA_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4410_LAMBDA_FROM_RUU_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4409 = SOURCE_DIR / "P8_Y5_R2FR_4409_NEXT_TARGET.csv"
FORMAL_425 = FORMAL / "425-PPC4161-transition-lambda-curvature-payload-cancellation-or-first-real-density-profile-row.md"
FORMAL_419 = FORMAL / "419-PPC4161-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"
DECISION_4404 = SOURCE_DIR / "P8_Y5_R2FR_4404_DECISION.csv"
DECISION_4405 = SOURCE_DIR / "P8_Y5_R2FR_4405_DECISION.csv"
DECISION_4406 = SOURCE_DIR / "P8_Y5_R2FR_4406_DECISION.csv"
DECISION_4407 = SOURCE_DIR / "P8_Y5_R2FR_4407_DECISION.csv"
DECISION_4408 = SOURCE_DIR / "P8_Y5_R2FR_4408_DECISION.csv"
DECISION_4409 = SOURCE_DIR / "P8_Y5_R2FR_4409_DECISION.csv"
FORMAL_420 = FORMAL / "420-PPC4161-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"
FORMAL_421 = FORMAL / "421-PPC4161-transition-cGamma-Pleak-first-two-components-or-profile-bound.md"
FORMAL_422 = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
FORMAL_423 = FORMAL / "423-PPC4161-transition-density-profile-owner-or-Eprofile-source-shadow-gate.md"
FORMAL_424 = FORMAL / "424-PPC4161-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4410_00_4409_next": (
        NEXT_4409,
        "local Ricci survivor vector",
        "4409 handoff to local Ricci survivor vector.",
    ),
    "SRC4410_01_4409_formal": (
        FORMAL_425,
        "Ricci-normal payload R_uu",
        "4409 narrows lambda source to Ricci-normal payload.",
    ),
    "SRC4410_02_4403_formal": (
        FORMAL_419,
        "Retained local survivor vector",
        "4403 retained survivor vector and R_uu payload law.",
    ),
    "SRC4410_03_4404_decision": (
        DECISION_4404,
        "CGAMMA_SPLIT_INTO_MEMORY_NOHAIR_PRODUCT_AND_AJ_PRESSURE_GATES",
        "4404 splits c_Gamma into executable lanes.",
    ),
    "SRC4410_04_4405_decision": (
        DECISION_4405,
        "FIRST_TWO_PLEAK_COMPONENTS_ZERO_ON_COMPACT_PRIVATE_BRANCH",
        "4405 classifies first two P_leak components.",
    ),
    "SRC4410_05_4406_decision": (
        DECISION_4406,
        "EPSILON_GSRC_SOURCE_BRIDGE_IMPORTED",
        "4406 imports source-charge/coupling bridge.",
    ),
    "SRC4410_06_4407_decision": (
        DECISION_4407,
        "EPROFILE_SOURCE_SHADOW_GRAMMAR",
        "4407 makes profile shadow executable.",
    ),
    "SRC4410_07_4408_decision": (
        DECISION_4408,
        "SIGMAS_ELECTRIC_U_OWNER_CONTRACT_DERIVED",
        "4408 derives sigma/electric owner contract.",
    ),
    "SRC4410_08_4409_decision": (
        DECISION_4409,
        "LAMBDA_CURVATURE_SOURCE_REBASED_TO_RICCI_UU",
        "4409 current-chain lambda/Ricci decision.",
    ),
    "SRC4410_09_survivor_gate": (
        SURVIVOR_GATE_PATH,
        "def evaluate_aggregate_rows",
        "New executable survivor-vector gate.",
    ),
    "SRC4410_10_local_gate": (
        LOCAL_GATE_PATH,
        "def evaluate_payload_rows",
        "Existing local residual payload gate.",
    ),
    "SRC4410_11_ricci_runner": (
        RICCI_RUNNER_PATH,
        "def evaluate_bound_rows",
        "Existing Ricci_uu source-bound runner.",
    ),
    "SRC4410_12_lambda_gate": (
        LAMBDA_GATE_PATH,
        "def evaluate_bound_rows",
        "Existing lambda curvature bound runner.",
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
            "derivation_id": "RSV4410_0_survivor_vector_contract",
            "statement": "The current local-Ricci obstruction is an explicit survivor vector, not an unnamed residual blob.",
            "derivation": "Combine 4402 trace reversal, 4403 residual factorization, 4404-4408 component gates and 4409 trace-electric rebase. In local matter vacuum the live source is bounded by |R_uu| <= sum_j(|S_j,uu| + 1/2 |S_j,tr|) + |Lambda_eff| + |B_projector|, where S_j runs over c_Gamma/P_leak, c_R2/M_R, spin/torsion, source-charge/profile shadow and any remaining boundary/projector hair.",
            "new_information": "Every remaining local-GR obstruction now has to enter one row of a finite vector; it cannot hide in generic E_res language.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RSV4410_1_clean_zero_theorem_contract",
            "statement": "A clean R_uu=0 proof needs parent-signed zero for every survivor component on the same tau/coframe/worldtube support.",
            "derivation": "Private selector zeros and compact-branch silences are usable only inside their branch. A public/local-GR claim requires parent_zero_signed, same_worldtube_support, same_tau_coframe_support, projection_closed, boundary_closed and coupling_closed for each component, plus Lambda_eff and projector silence.",
            "new_information": "This is the exact contract a future parent action must satisfy before local GR can be claimed.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RSV4410_2_first_real_Ruu_row_contract",
            "statement": "If the clean zero theorem cannot be signed, the next legitimate route is a first real R_uu source row with component-level uu/trace bounds.",
            "derivation": "For each survivor component, the row must supply |S_j,uu| and |S_j,tr| on the same support, plus |Lambda_eff|, |B_projector|, |K_E c^2| and an arena threshold. The aggregate then feeds the Ricci_uu and lambda-curvature runners without hidden cancellation.",
            "new_information": "The finite route is now source-acquisition-ready rather than merely symbolic.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RSV4410_3_no_Weyl_escape_guard",
            "statement": "The 4410 branch must not reclassify Weyl/tidal curvature as the source of the lambda payload.",
            "derivation": "4409 showed the trace-electric source is Ricci-normal. Weyl curvature can affect geodesic deviation, but the scalar trace-electric lambda source used here is R_uu plus projector/extrinsic/boundary terms.",
            "new_information": "The next derivation must attack Ricci survivors, not broaden the target back to generic curvature.",
            "valid_for_claim": False,
        },
    ]


def component_input_rows() -> List[Dict[str, object]]:
    live = [
        ("RSV4410_LIVE", "RSVC4410_0_cGamma_Pleak", "c_Gamma/P_leak", "connection_memory", FORMAL_420, "4404/4405 split exists but raw transition-shell source hair is not parent-zeroed or numeric."),
        ("RSV4410_LIVE", "RSVC4410_1_cR2_MR", "c_R2/M_R", "higher_curvature", FORMAL_419, "Higher-curvature survivor lacks parent decoupling scale or numeric local row."),
        ("RSV4410_LIVE", "RSVC4410_2_spin_torsion", "spin/torsion", "Einstein_Cartan_contact", FORMAL_419, "Spin/torsion contact branch remains a retained local survivor."),
        ("RSV4410_LIVE", "RSVC4410_3_source_profile_shadow", "epsilon_Gsrc/E_profile", "source_charge_density", FORMAL_422, "Source-charge bridge and profile shadow are executable but not parent-zeroed or sourced as a live row."),
    ]
    rows: List[Dict[str, object]] = []
    for group_id, component_id, component, sector, source, notes in live:
        rows.append(
            {
                "group_id": group_id,
                "component_id": component_id,
                "component": component,
                "sector": sector,
                "route": "current_chain_live_unresolved_component",
                "parent_zero_signed": False,
                "private_zero_usable": False,
                "same_worldtube_support": False,
                "same_tau_coframe_support": False,
                "projection_closed": False,
                "boundary_closed": False,
                "coupling_closed": False,
                "uu_abs": "MISSING_REAL_UU_BOUND",
                "trace_abs": "MISSING_REAL_TRACE_BOUND",
                "source_path": str(source),
                "support_certificate_path": "MISSING_SAME_SUPPORT_CERTIFICATE",
                "input_valid_for_claim": False,
                "notes": notes,
            }
        )
    zero_components = [
        ("RSVC4410_Z0_cGamma_Pleak", "c_Gamma/P_leak", "connection_memory"),
        ("RSVC4410_Z1_cR2_MR", "c_R2/M_R", "higher_curvature"),
        ("RSVC4410_Z2_spin_torsion", "spin/torsion", "Einstein_Cartan_contact"),
        ("RSVC4410_Z3_source_profile_shadow", "epsilon_Gsrc/E_profile", "source_charge_density"),
    ]
    for component_id, component, sector in zero_components:
        rows.append(
            {
                "group_id": "RSV4410_ZERO_SMOKE",
                "component_id": component_id,
                "component": component,
                "sector": sector,
                "route": "future_parent_zero_schema_smoke",
                "parent_zero_signed": True,
                "private_zero_usable": False,
                "same_worldtube_support": True,
                "same_tau_coframe_support": True,
                "projection_closed": True,
                "boundary_closed": True,
                "coupling_closed": True,
                "uu_abs": 0.0,
                "trace_abs": 0.0,
                "source_path": str(FORMAL_PATH),
                "support_certificate_path": str(FORMAL_PATH),
                "input_valid_for_claim": False,
                "notes": "Schema-control row only; no parent signature is asserted.",
            }
        )
    fail_components = [
        ("RSVC4410_F0_cGamma_Pleak", "c_Gamma/P_leak", "connection_memory", 0.06, 0.02),
        ("RSVC4410_F1_cR2_MR", "c_R2/M_R", "higher_curvature", 0.04, 0.02),
        ("RSVC4410_F2_spin_torsion", "spin/torsion", "Einstein_Cartan_contact", 0.02, 0.02),
        ("RSVC4410_F3_source_profile_shadow", "epsilon_Gsrc/E_profile", "source_charge_density", 0.02, 0.02),
    ]
    for component_id, component, sector, uu_abs, trace_abs in fail_components:
        rows.append(
            {
                "group_id": "RSV4410_FAIL_CONTROL",
                "component_id": component_id,
                "component": component,
                "sector": sector,
                "route": "finite_bound_fail_control",
                "parent_zero_signed": False,
                "private_zero_usable": False,
                "same_worldtube_support": True,
                "same_tau_coframe_support": True,
                "projection_closed": True,
                "boundary_closed": True,
                "coupling_closed": True,
                "uu_abs": uu_abs,
                "trace_abs": trace_abs,
                "source_path": str(FORMAL_PATH),
                "support_certificate_path": str(FORMAL_PATH),
                "input_valid_for_claim": False,
                "notes": "Failure-control row to prove threshold rejection remains live.",
            }
        )
    return rows


def aggregate_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "group_id": "RSV4410_LIVE",
            "aggregate_id": "RSVA4410_0_live_current_chain",
            "arena": "local_GR_Newton_PPN_R10_clock_orbital",
            "Lambda_eff_abs": "MISSING_LOCAL_LAMBDA_BOUND",
            "projector_boundary_abs": "MISSING_PROJECTOR_BOUND",
            "K_E_c2_abs": "MISSING_KEC2",
            "F_E_threshold": "MISSING_ARENA_THRESHOLD",
            "source_path": str(COMPONENT_OUTPUT),
            "support_certificate_path": "MISSING_SAME_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": False,
            "notes": "Live row intentionally blocked until every survivor component has parent-zero or real numeric bound.",
        },
        {
            "group_id": "RSV4410_ZERO_SMOKE",
            "aggregate_id": "RSVA4410_1_zero_schema_nonclaim",
            "arena": "schema_control",
            "Lambda_eff_abs": 0.0,
            "projector_boundary_abs": 0.0,
            "K_E_c2_abs": 1.0,
            "F_E_threshold": 0.01,
            "source_path": str(COMPONENT_OUTPUT),
            "support_certificate_path": str(COMPONENT_OUTPUT),
            "input_valid_for_claim": False,
            "notes": "Zero-control row proves the clean branch wiring without claiming the parent theorem.",
        },
        {
            "group_id": "RSV4410_FAIL_CONTROL",
            "aggregate_id": "RSVA4410_2_large_payload_fail_control",
            "arena": "threshold_guard",
            "Lambda_eff_abs": 0.02,
            "projector_boundary_abs": 0.02,
            "K_E_c2_abs": 1.0,
            "F_E_threshold": 0.05,
            "source_path": str(COMPONENT_OUTPUT),
            "support_certificate_path": str(COMPONENT_OUTPUT),
            "input_valid_for_claim": False,
            "notes": "Large finite row must fail the threshold so the runner cannot rubber-stamp payloads.",
        },
    ]


def source_register_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4410_SOURCE_REGISTER.csv"


def derivation_path() -> Path:
    return SOURCE_DIR / "P8_Y5_R2FR_4410_DERIVATIONS.csv"


def claim_gate_rows(component_rows: List[Dict[str, str]], aggregate_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    live = next(row for row in aggregate_rows if row["group_id"] == "RSV4410_LIVE")
    return [
        {
            "gate_id": "CG4410_0_clean_zero_route",
            "claim": "R_uu=0 clean local branch",
            "claim_allowed": False,
            "reason": "Every live survivor component lacks parent-signed zero on same tau/coframe/worldtube support.",
        },
        {
            "gate_id": "CG4410_1_finite_Ruu_route",
            "claim": "finite R_uu source row accepted",
            "claim_allowed": False,
            "reason": f"Live aggregate status is {live['current_status']} with unresolved components {live['unresolved_components']}.",
        },
        {
            "gate_id": "CG4410_2_local_GR_Newton_PPN_R10",
            "claim": "local GR/Newton/PPN/R10/clock/orbital pass",
            "claim_allowed": False,
            "reason": "No local claim can fire until the survivor vector is parent-zeroed or source-bounded and then passed through Ricci/lambda gates.",
        },
        {
            "gate_id": "CG4410_3_nonclaim_controls",
            "claim": "runner controls",
            "claim_allowed": False,
            "reason": "Zero schema remains nonclaim and fail control fails threshold, so the runner is discriminating.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4410_0",
            "decision": DECISION,
            "summary": "4410 turns the local Ricci obstruction into a strict survivor-vector contract. The clean route requires parent-signed zero/silence for c_Gamma/P_leak, c_R2/M_R, spin/torsion, source-charge/profile shadow, Lambda_eff and projector/boundary terms on the same support. The finite route requires the first real component-level uu/trace source row. Current live rows remain blocked, but the exact R_uu aggregation and downstream Ricci/lambda runners now execute with zero and fail controls.",
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
            "next_id": "NT4410_0",
            "target": NEXT_TARGET,
            "question": "Can a parent Ward/no-hair identity zero the whole Ricci survivor vector on the same support, or must the first real R_uu component row be sourced?",
            "preferred_route": "derive a single parent identity from Hilbert-only source ownership, Bianchi consistency, stationary memory no-hair, and projection/boundary silence that sets every survivor component in the 4410 vector to zero.",
            "fallback_route": "source the first real same-support R_uu row with component-level uu/trace bounds for c_Gamma/Pleak, c_R2/M_R, spin/torsion, source/profile shadow, Lambda_eff and projector terms.",
            "avoid": "another generic missing-ledger pass, Weyl/tidal source broadening, private-selector zeros treated as public local-GR proof, or cancellation between unrelated survivor components.",
            "valid_for_claim": False,
        }
    ]


def value_or_missing(value: str, missing: str) -> str:
    return value if str(value).strip() else missing


def ricci_input_rows(aggregate_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for aggregate in aggregate_rows:
        rows.append(
            {
                "bound_id": f"RUB4410_from_{aggregate['aggregate_id']}",
                "arena": aggregate["arena"],
                "kappa_eff_abs": 0.0,
                "T_uu_norm": 0.0,
                "T_trace_norm": 0.0,
                "E_res_uu_norm": value_or_missing(aggregate.get("Ruu_abs_bound", ""), "MISSING_RUU_ABS_BOUND"),
                "E_res_trace_norm": 0.0,
                "Lambda_eff_abs": 0.0,
                "projector_boundary_abs": 0.0,
                "K_E_c2_abs": 1.0,
                "F_E_threshold": value_or_missing(aggregate.get("F_E_threshold", ""), "MISSING_THRESHOLD"),
                "source_path": str(AGGREGATE_OUTPUT),
                "support_certificate_path": str(COMPONENT_OUTPUT),
                "input_valid_for_claim": False,
                "notes": "Consumes 4410 aggregate R_uu as a no-cancellation residual source; nonclaim by construction.",
            }
        )
    return rows


def lambda_input_rows(aggregate_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for aggregate in aggregate_rows:
        rows.append(
            {
                "bound_id": f"LCB4410_from_{aggregate['aggregate_id']}",
                "arena": aggregate["arena"],
                "F_E_norm": value_or_missing(aggregate.get("F_E_norm", ""), "MISSING_FE_NORM"),
                "C_poincare": 1.0,
                "C_elliptic_H2": 1.0,
                "K_lambda_stress": 1.0,
                "K_projection": 1.0,
                "arena_threshold": value_or_missing(aggregate.get("F_E_threshold", ""), "MISSING_THRESHOLD"),
                "boundary_condition": "zero_mean_Neumann",
                "zero_mode_fixed": True,
                "boundary_flux_silent": True,
                "source_path": str(AGGREGATE_OUTPUT),
                "support_certificate_path": str(COMPONENT_OUTPUT),
                "input_valid_for_claim": False,
                "notes": "Consumes 4410 F_E from local Ricci survivor vector; nonclaim by construction.",
            }
        )
    return rows


def compact_rows(rows: List[Dict[str, str]], fields: List[str]) -> List[Dict[str, str]]:
    return [{field: row.get(field, "") for field in fields} for row in rows]


def render_document(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    components: List[Dict[str, str]],
    aggregates: List[Dict[str, str]],
    ricci_rows: List[Dict[str, str]],
    lambda_rows: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 426 PPC4161 transition: local Ricci survivor vector zero or first real Ruu source row

Marker: `{MARKER}`

Generated: `{STAMP}`

Decision: `{DECISION}`

## Current-Chain Result

4410 does the thing we actually needed after 4409: it stops letting `R_uu` be a vague symbol. The local Ricci payload is now an explicit vector of survivor components. A clean local-GR route has to zero every component by parent authority on the same support; the finite route has to source component-level `uu` and trace bounds.

## Exact No-Cancellation Law

In local matter vacuum, the current branch uses:

`|R_uu| <= sum_j(|S_j,uu| + 1/2 |S_j,tr|) + |Lambda_eff| + |B_projector|`.

The live `S_j` components are:

- `c_Gamma/P_leak`
- `c_R2/M_R`
- `spin/torsion`
- `epsilon_Gsrc/E_profile`

The scalar trace-electric lambda source is then:

`|F_E| <= |K_E c^2| |R_uu|`.

## Source Audit

{markdown_table(sources)}

## Derivations

{markdown_table(derivations)}

## Survivor Component Gate

{markdown_table(compact_rows(components, ["group_id", "component", "current_status", "contribution_ready", "component_uu_bound", "component_trace_bound", "valid_for_claim"]))}

## Aggregate Ruu Gate

{markdown_table(compact_rows(aggregates, ["group_id", "current_status", "unresolved_components", "Ruu_abs_bound", "F_E_norm", "within_threshold", "valid_for_claim"]))}

## Downstream Ricci Runner

{markdown_table(compact_rows(ricci_rows, ["bound_id", "current_status", "Ruu_abs_bound", "F_E_norm", "within_threshold", "valid_for_claim"]))}

## Downstream Lambda Runner

{markdown_table(compact_rows(lambda_rows, ["bound_id", "current_status", "lambda_curvature_payload_score", "payload_within_threshold", "valid_for_claim"]))}

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
## 4410 local spine update: Ricci survivor vector contract

Marker: `{MARKER}`

4410 converts the local Ricci obstruction into the explicit no-cancellation vector
`|R_uu| <= sum_j(|S_j,uu| + 1/2|S_j,tr|) + |Lambda_eff| + |B_projector|`.
The live survivor slots are `c_Gamma/P_leak`, `c_R2/M_R`, `spin/torsion`, and `epsilon_Gsrc/E_profile`.
No local-GR/Newton/PPN/R10/clock/orbital claim fires: the current live row is blocked until every slot is parent-zeroed on the same support or filled by a real numeric source row.
""",
    )


def append_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4410 packet update: local Ricci survivor vector made executable

Marker: `{PACKET_MARKER}`

The post-4409 branch now has a concrete survivor-vector runner. Clean route: parent Ward/no-hair theorem signs every component zero on the same support. Finite route: source the first real `R_uu` component row and pass it through Ricci/lambda gates. The zero-control and fail-control rows prove the wiring is discriminating, but the live branch remains nonclaim.
""",
    )


def append_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4410 turns the local Ricci obstruction into an explicit survivor-vector contract. A clean R_uu=0 branch requires parent-signed zero/silence for c_Gamma/Pleak, c_R2/M_R, spin/torsion, source-profile shadow, Lambda_eff and projector/boundary terms on the same tau/coframe/worldtube support. The finite branch requires the first real component-level uu/trace R_uu source row and then passes it through Ricci and lambda runners. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",
            "4410 source register, derivation rows, survivor component gate, aggregate R_uu gate, Ricci source-bound output, lambda-bound output, claim gates, decision, status, next target and validation CSV.",
            "local_Ricci_survivor_vector_contract_runner_ready_nonclaim",
            "Derive the parent Ward/no-hair identity for the whole survivor vector or source the first real same-support R_uu row.",
            "Private selector zeros treated as public proof, Weyl/tidal broadening, or cancellation between unrelated survivor components.",
        ],
    )


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, object]]:
    sources = read_csv(paths["source_register"])
    components = read_csv(COMPONENT_OUTPUT)
    aggregates = read_csv(AGGREGATE_OUTPUT)
    ricci_rows = read_csv(RICCI_OUTPUT)
    lambda_rows = read_csv(LAMBDA_OUTPUT)
    all_outputs = components + aggregates + ricci_rows + lambda_rows
    live_aggregate = next(row for row in aggregates if row["group_id"] == "RSV4410_LIVE")
    zero_aggregate = next(row for row in aggregates if row["group_id"] == "RSV4410_ZERO_SMOKE")
    fail_aggregate = next(row for row in aggregates if row["group_id"] == "RSV4410_FAIL_CONTROL")

    checks = [
        ("VAL4410_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4410_1_source_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle was found"),
        ("VAL4410_2_live_components_blocked", all(row["current_status"] == "SURVIVOR_COMPONENT_BLOCKED" for row in components if row["group_id"] == "RSV4410_LIVE"), "live survivor components remain honestly blocked"),
        ("VAL4410_3_zero_schema_nonclaim", zero_aggregate["current_status"] == "RICCI_SURVIVOR_VECTOR_ZERO_SCHEMA_READY_NONCLAIM", "zero-control wiring works but stays nonclaim"),
        ("VAL4410_4_fail_control_rejected", fail_aggregate["current_status"] == "RICCI_SURVIVOR_VECTOR_FAILS_THRESHOLD", "large payload fail-control is rejected"),
        ("VAL4410_5_live_aggregate_blocked", live_aggregate["current_status"] == "RICCI_SURVIVOR_VECTOR_BLOCKED", "live aggregate is blocked until real rows or parent zeros exist"),
        ("VAL4410_6_live_unresolved_named", "c_Gamma/P_leak" in live_aggregate["unresolved_components"] and "epsilon_Gsrc/E_profile" in live_aggregate["unresolved_components"], "live unresolved vector names the hard slots"),
        ("VAL4410_7_ricci_runner_blocks_live", any(row["bound_id"].endswith("RSVA4410_0_live_current_chain") and row["current_status"] == "RICCI_UU_SOURCE_BOUND_BLOCKED" for row in ricci_rows), "Ricci runner blocks live row"),
        ("VAL4410_8_lambda_runner_blocks_live", any(row["bound_id"].endswith("RSVA4410_0_live_current_chain") and row["current_status"] == "LAMBDA_CURVATURE_PAYLOAD_BOUND_BLOCKED" for row in lambda_rows), "lambda runner blocks live row"),
        ("VAL4410_9_ricci_fail_control_rejected", any(row["bound_id"].endswith("RSVA4410_2_large_payload_fail_control") and row["current_status"] == "RICCI_UU_SOURCE_BOUND_FAILS_THRESHOLD" for row in ricci_rows), "Ricci runner rejects large fail-control row"),
        ("VAL4410_10_no_output_claims", not any(bool_text(row.get("claim_allowed", "False")) or bool_text(row.get("valid_for_claim", "False")) for row in all_outputs), "no generated output is claim-valid"),
        ("VAL4410_11_claim_row_exists", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claims register contains L-251"),
        ("VAL4410_12_spine_marker_exists", MARKER in text(SPINE_PATH), "spine update marker exists"),
        ("VAL4410_13_packet_marker_exists", PACKET_MARKER in text(PACKET_PATH), "packet update marker exists"),
        ("VAL4410_14_formal_doc_exists", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4410_15_post_doc_exists", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post-checkpoint doc exists with marker"),
        ("VAL4410_16_next_target_exists", paths["next_target"].exists() and NEXT_TARGET in text(paths["next_target"]), "next target file exists"),
        ("VAL4410_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
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
    rows_to_write: Dict[str, Tuple[Path, List[Dict[str, object]]]] = {
        "source_register": (source_register_path(), source_rows()),
        "derivations": (derivation_path(), derivation_rows()),
        "component_input": (COMPONENT_INPUT, component_input_rows()),
        "aggregate_input": (AGGREGATE_INPUT, aggregate_input_rows()),
    }
    for _, (path, rows) in rows_to_write.items():
        write_csv(path, rows)  # type: ignore[arg-type]

    component_rows = evaluate_component_rows(COMPONENT_INPUT)
    write_csv(COMPONENT_OUTPUT, component_rows)
    aggregate_rows = evaluate_aggregate_rows(AGGREGATE_INPUT, COMPONENT_OUTPUT)
    write_csv(AGGREGATE_OUTPUT, aggregate_rows)

    write_csv(RICCI_INPUT, ricci_input_rows(aggregate_rows))  # type: ignore[arg-type]
    ricci_rows = evaluate_ricci_bound_rows(RICCI_INPUT)
    write_csv(RICCI_OUTPUT, ricci_rows)

    write_csv(LAMBDA_INPUT, lambda_input_rows(aggregate_rows))  # type: ignore[arg-type]
    lambda_rows = evaluate_lambda_bound_rows(LAMBDA_INPUT)
    write_csv(LAMBDA_OUTPUT, lambda_rows)

    claim_gates = claim_gate_rows(component_rows, aggregate_rows)
    decision = decision_rows()
    status = status_rows()
    next_targets = next_target_rows()
    extra_paths = {
        "claim_gates": SOURCE_DIR / "P8_Y5_R2FR_4410_CLAIM_GATES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4410_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4410_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4410_NEXT_TARGET.csv",
    }
    write_csv(extra_paths["claim_gates"], claim_gates)  # type: ignore[arg-type]
    write_csv(extra_paths["decision"], decision)  # type: ignore[arg-type]
    write_csv(extra_paths["status"], status)  # type: ignore[arg-type]
    write_csv(extra_paths["next_target"], next_targets)  # type: ignore[arg-type]

    doc = render_document(
        source_rows(),
        derivation_rows(),
        component_rows,
        aggregate_rows,
        ricci_rows,
        lambda_rows,
        claim_gates,
    )
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_spine()
    append_packet()
    append_claim()

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    paths = {
        "source_register": source_register_path(),
        "next_target": extra_paths["next_target"],
    }
    write_csv(VALIDATION_PATH, validation_rows(paths))  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
