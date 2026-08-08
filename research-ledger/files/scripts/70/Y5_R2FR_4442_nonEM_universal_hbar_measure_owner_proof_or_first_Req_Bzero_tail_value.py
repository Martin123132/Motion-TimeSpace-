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

from nonem_classical_source_owner_gate import evaluate_route_rows, evaluate_tail_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4442"
CLAIM_ID = "L-283"
MARKER = "PPC4161_NONEM_CLASSICAL_SOURCE_OWNER_ROUTE_SPLIT_OR_REQ_BZERO_TAIL_4442"
PACKET_MARKER = "PPC4161_PACKET_NONEM_CLASSICAL_SOURCE_OWNER_ROUTE_SPLIT_4442"
DECISION = "NONEM_CLASSICAL_SOURCE_OWNER_ROUTE_SPLIT_DERIVED_HBAR_DEMOTED_TO_QUANTUM_GUARD_REQ_BZERO_HTAU_REMAIN_NONCLAIM"
NEXT_TARGET = "4443-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"

FORMAL_PATH = FORMAL / "458-PPC4161-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md"
DOC_PATH = POST / "4442-Y5-R2FR-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4442_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4442_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4442_DERIVATION_ROWS.csv"
ROUTE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4442_NONEM_SOURCE_ROUTE_INPUT.csv"
ROUTE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4442_NONEM_SOURCE_ROUTE_OUTPUT.csv"
TAIL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4442_REQ_BZERO_FIRST_TAIL_INPUT.csv"
TAIL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4442_REQ_BZERO_FIRST_TAIL_OUTPUT.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4442_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4442_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4442_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4442_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4442_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "nonem_classical_source_owner_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4442_nonEM_universal_hbar_measure_owner_proof_or_first_Req_Bzero_tail_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4441 = SOURCE_DIR / "P8_Y5_R2FR_4441_NEXT_TARGET.csv"
FORMAL_457 = FORMAL / "457-PPC4161-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md"
FORMAL_456 = FORMAL / "456-PPC4161-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md"
FORMAL_436 = FORMAL / "436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md"
FORMAL_377 = FORMAL / "377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md"
FORMAL_438 = FORMAL / "438-PPC4161-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
FORMAL_440 = FORMAL / "440-PPC4161-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md"
FORMAL_450 = FORMAL / "450-PPC4161-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
POST_3574 = POST / "3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md"
OUTPUT_4434_HBAR = SOURCE_DIR / "P8_Y5_R2FR_4434_HBAR_MEASURE_OWNER_OUTPUT.csv"
OUTPUT_4434_GRAPH = SOURCE_DIR / "P8_Y5_R2FR_4434_CONNECTED_GRAPH_OUTPUT.csv"
OUTPUT_4441_ROUTE = SOURCE_DIR / "P8_Y5_R2FR_4441_ACTION_MEASURE_CURRENT_OWNER_OUTPUT.csv"
OUTPUT_4441_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4441_REQ_BZERO_TAIL_OUTPUT.csv"

SMOKE_BOUND = 1.0e-5
SMOKE_PASS_VALUE = 4.0e-7
SMOKE_FAIL_VALUE = 3.0e-3


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
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4442_00_4441_next", "path": NEXT_4441, "needle": "4442-Y5-R2FR-nonEM", "role": "4441 handoff."},
        {"source_id": "SRC4442_01_457_nonEM", "path": FORMAL_457, "needle": "AMCO4441_1_nonEM_owner_contract", "role": "post-EM nonEM owner target."},
        {"source_id": "SRC4442_02_4361_scalar", "path": FORMAL_377, "needle": "TH4361_0_scalar_naturality", "role": "connected scalar action-weight naturality theorem."},
        {"source_id": "SRC4442_03_4361_full", "path": FORMAL_377, "needle": "TH4361_3_full_owner_no_wA", "role": "full owner/no-wA conditional theorem."},
        {"source_id": "SRC4442_04_4422_hbar", "path": FORMAL_438, "needle": "UHM4422_1_exact_owner_contract", "role": "hbar/measure theorem and countermodel."},
        {"source_id": "SRC4442_05_4423_action_density", "path": FORMAL_439, "needle": "ADL4423_3_action_density_owner_theorem", "role": "typed action-density owner theorem."},
        {"source_id": "SRC4442_06_4424_constructor", "path": FORMAL_440, "needle": "CEX4424_2_Hom_no_slot_result", "role": "constructor exhaustion/no-Hom result."},
        {"source_id": "SRC4442_07_4434_graph", "path": FORMAL_450, "needle": "GRC4434_0_connected_graph_contract", "role": "parent-owned connected matter graph contract."},
        {"source_id": "SRC4442_08_4434_hbar_csv", "path": OUTPUT_4434_HBAR, "needle": "HMO4434_0_future_owner_contract", "role": "machine hbar/measure owner row."},
        {"source_id": "SRC4442_09_4434_graph_csv", "path": OUTPUT_4434_GRAPH, "needle": "GRC4434_0_connected_graph_contract", "role": "machine connected graph row."},
        {"source_id": "SRC4442_10_4420_joint", "path": FORMAL_436, "needle": "AMR4420_0_joint_contract", "role": "joint phase/measure/R_eq source route."},
        {"source_id": "SRC4442_11_4440_gsrc", "path": FORMAL_456, "needle": "epsilon_Gsrc_perp", "role": "physical source-coupling tail after common-mode split."},
        {"source_id": "SRC4442_12_4441_route_csv", "path": OUTPUT_4441_ROUTE, "needle": "AMCO4441_0_current_after_EM_subcontract", "role": "fixed EM subcontract machine row."},
        {"source_id": "SRC4442_13_4441_tail_csv", "path": OUTPUT_4441_TAIL, "needle": "TAIL4441_1_Req_live_contract", "role": "R_eq/B_zero live tail precedent."},
        {"source_id": "SRC4442_14_gate", "path": GATE_PATH, "needle": "def evaluate_route_row", "role": "4442 route/tail gate."},
        {"source_id": "SRC4442_15_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4442"', "role": "4442 generator."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "NEM4442_0_route_split",
            "claim": "Classical local source coupling does not need hbar as its first lock.",
            "derivation": "For Newton/local-GR source coupling the dangerous object is a pre-variation relative action/source weight w_A in S_matter. If the classical parent action has one measure, one action-density/current owner, no Hom(SpeciesLabel,Coeff_active_source), constructor exhaustion, no readout re-entry and a connected parent-owned ordinary-matter graph, scalar naturality forces w_A=w_* before any quantum hbar argument is used. Universal hbar/quantum measure remains necessary for the quantum-statistical interpretation, but it is not the shortest classical source-coupling lock.",
            "consequence": "The least-scrutiny local-GR route is now a classical parent action-density/current/graph/no-Hom theorem plus R_eq/B_zero/H_tau locks, with hbar retained as a quantum guard rather than the first local-source bottleneck.",
            "status": "DERIVED_ROUTE_SPLIT_CLASSICAL_OWNER_NOT_HBAR_FIRST",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEM4442_1_scalar_naturality_reused",
            "claim": "Connected parent-owned nonEM matter graph collapses natural scalar weights.",
            "derivation": "For every nonzero parent-owned edge f:A->B, naturality of scalar action weights gives w_B F(f)=F(f) w_A. Since F(f) is nonzero on a connected graph, w_A=w_B along every edge, hence w_A=w_* on the whole connected ordinary-matter component.",
            "consequence": "Relative Delta_w_AB is killed by parent-owned connectedness plus no-Hom/no-reentry; disconnected components are the exact countermodel.",
            "status": "EXACT_CONDITIONAL_NATURALITY_THEOREM_IMPORTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEM4442_2_common_mode_calibration",
            "claim": "The surviving common w_* is calibration, not a material/source residual, only if derivative-silent.",
            "derivation": "If w_* is common over species/material/source labels and D_time, D_frame, D_range and D_readout variations vanish on the tested branch, it multiplies the same Hilbert source and is absorbed into G_cal/GM. If any derivative or readout dependence survives, it is an explicit finite source-coupling tail.",
            "consequence": "This prevents hiding relative source weights in measured G while allowing one true common calibration mode.",
            "status": "COMMON_MODE_CALIBRATION_LAW_SHARPENED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEM4442_3_local_closure_remaining",
            "claim": "Even a classical owner/no-wA theorem is not local GR by itself.",
            "derivation": "After Delta_w/Xi source weights are zeroed, the source current used by Newton/PPN must still be the same distributional Hilbert/Hamiltonian current: Pi_M J_H=J_M^top+dB_zero+R_eq with R_eq=0 and zero boundary flux on the same H_tau/MHref worldtube branch.",
            "consequence": "The next finite fallback is not another coupling word: it is one R_eq compact-test/multipole value or one B_zero boundary flux value with projection coefficient and arena bound.",
            "status": "REQ_BZERO_HTAU_STILL_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEM4442_4_public_firewall",
            "claim": "No public local-GR/Newton/PPN claim follows from 4442.",
            "derivation": "Current rows do not parent-sign constructor exhaustion, hidden/readout no-reentry, parent-owned connected nonEM graph, total source-current owner, same-current R_eq=0, B_zero flux silence or H_tau/MHref locks. The hbar-free route split is a proof-order improvement, not a completed source law.",
            "consequence": NEXT_TARGET,
            "status": "PUBLIC_CLAIM_BLOCKED_NEXT_GRAPH_EDGE_OR_REQ_VALUE",
            "valid_for_claim": False,
        },
    ]


def route_input_rows() -> List[Dict[str, object]]:
    base_false = {
        "one_classical_parent_action": False,
        "common_classical_measure": False,
        "variation_before_readout": False,
        "action_density_owner": False,
        "typed_no_source_hom": False,
        "constructor_exhaustion": False,
        "hidden_readout_no_reentry": False,
        "parent_connected_graph": False,
        "derivative_silent_common_mode": False,
        "total_hilbert_current_owner": False,
        "fixed_EM_subcontract_removed": False,
        "same_current_Req_zero": False,
        "B_zero_flux_silent": False,
        "Htau_MHref_locks": False,
        "universal_hbar_parent": False,
        "quantum_measure_owner": False,
        "public_authority": False,
        "input_valid_for_claim": False,
    }
    return [
        {
            **base_false,
            "row_id": "NEM4442_0_current_post_EM_branch",
            "branch": "current fixed-EM-removed nonEM source-owner branch",
            "one_classical_parent_action": True,
            "variation_before_readout": True,
            "fixed_EM_subcontract_removed": True,
            "source_path": str(FORMAL_457),
        },
        {
            **base_false,
            "row_id": "NEM4442_1_future_classical_local_source_contract",
            "branch": "future hbar-free classical local source contract",
            "one_classical_parent_action": True,
            "common_classical_measure": True,
            "variation_before_readout": True,
            "action_density_owner": True,
            "typed_no_source_hom": True,
            "constructor_exhaustion": True,
            "hidden_readout_no_reentry": True,
            "parent_connected_graph": True,
            "derivative_silent_common_mode": True,
            "total_hilbert_current_owner": True,
            "fixed_EM_subcontract_removed": True,
            "same_current_Req_zero": True,
            "B_zero_flux_silent": True,
            "Htau_MHref_locks": True,
            "source_path": str(FORMAL_377),
        },
        {
            **base_false,
            "row_id": "NEM4442_2_future_full_quantum_plus_classical_contract",
            "branch": "future full hbar/measure plus classical local source contract",
            "one_classical_parent_action": True,
            "common_classical_measure": True,
            "variation_before_readout": True,
            "action_density_owner": True,
            "typed_no_source_hom": True,
            "constructor_exhaustion": True,
            "hidden_readout_no_reentry": True,
            "parent_connected_graph": True,
            "derivative_silent_common_mode": True,
            "total_hilbert_current_owner": True,
            "fixed_EM_subcontract_removed": True,
            "same_current_Req_zero": True,
            "B_zero_flux_silent": True,
            "Htau_MHref_locks": True,
            "universal_hbar_parent": True,
            "quantum_measure_owner": True,
            "source_path": str(FORMAL_438),
        },
        {
            **base_false,
            "row_id": "NEM4442_3_hbar_only_counterroute",
            "branch": "hbar measure owner without classical graph/current",
            "universal_hbar_parent": True,
            "quantum_measure_owner": True,
            "source_path": str(FORMAL_438),
        },
    ]


def tail_input_rows() -> List[Dict[str, object]]:
    return [
        {"tail_id": "TAIL4442_0_Req_compact_test_live", "quantity": "R_eq_compact_test", "target": "Newton_PPN_orbital_same_current", "distributional_definition": "R_eq[varphi]=int_W (Pi_M J_H-J_M_top-dB_zero) varphi", "projection_coeff": "MISSING_P_REQ_COMPACT", "tail_value": "MISSING_REQ_COMPACT_TEST_VALUE", "arena_bound": "MISSING_ARENA_BOUND", "units": "source_current_distribution", "source_path": str(POST_4378), "input_valid_for_claim": False},
        {"tail_id": "TAIL4442_1_Bzero_boundary_flux_live", "quantity": "B_zero_boundary_flux", "target": "Newton_Gdot_orbital_boundary_silence", "distributional_definition": "Phi_B=int_partialW B_zero / M_H_ref", "projection_coeff": "MISSING_P_BZERO_FLUX", "tail_value": "MISSING_BZERO_FLUX_VALUE", "arena_bound": "MISSING_ARENA_BOUND", "units": "dimensionless", "source_path": str(POST_3574), "input_valid_for_claim": False},
        {"tail_id": "TAIL4442_2_Htau_MHref_mismatch_live", "quantity": "Htau_MHref_mismatch", "target": "same_worldtube_mass_charge_lock", "distributional_definition": "epsilon_HM=abs(H_tau[S_link]-H_ref-M_H_ref)/M_H_ref", "projection_coeff": "MISSING_P_HTAU", "tail_value": "MISSING_HTAU_MHREF_MISMATCH", "arena_bound": "MISSING_ARENA_BOUND", "units": "dimensionless", "source_path": str(FORMAL_456), "input_valid_for_claim": False},
        {"tail_id": "TAIL4442_3_zero_smoke", "quantity": "R_eq_compact_test", "target": "schema_smoke", "distributional_definition": "P_tail*tail <= bound", "projection_coeff": "1", "tail_value": "0", "arena_bound": f"{SMOKE_BOUND:.12g}", "units": "dimensionless", "source_path": str(OUTPUT_4441_TAIL), "input_valid_for_claim": False},
        {"tail_id": "TAIL4442_4_small_smoke", "quantity": "R_eq_compact_test", "target": "schema_smoke", "distributional_definition": "P_tail*tail <= bound", "projection_coeff": "1", "tail_value": f"{SMOKE_PASS_VALUE:.12g}", "arena_bound": f"{SMOKE_BOUND:.12g}", "units": "dimensionless", "source_path": str(OUTPUT_4441_TAIL), "input_valid_for_claim": False},
        {"tail_id": "TAIL4442_5_fail_control", "quantity": "R_eq_compact_test", "target": "schema_smoke", "distributional_definition": "P_tail*tail <= bound", "projection_coeff": "1", "tail_value": f"{SMOKE_FAIL_VALUE:.12g}", "arena_bound": f"{SMOKE_BOUND:.12g}", "units": "dimensionless", "source_path": str(OUTPUT_4441_TAIL), "input_valid_for_claim": False},
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {"reduction_id": "RED4442_0_hbar_route_split", "object": "universal hbar/measure owner", "status": "DEMOTED_TO_QUANTUM_GUARD_FOR_LOCAL_CLASSICAL_SOURCE", "remaining": "still required for quantum/statistical branch and species hbar_A countermodel", "source_path": str(FORMAL_438), "valid_for_claim": False},
        {"reduction_id": "RED4442_1_classical_no_wA_route", "object": "nonEM classical source weights", "status": "EXACT_CONDITIONAL_THEOREM", "remaining": "parent-owned connected graph, constructor exhaustion, no reentry and current owner", "source_path": str(FORMAL_377), "valid_for_claim": False},
        {"reduction_id": "RED4442_2_same_current_route", "object": "R_eq/B_zero/H_tau locks", "status": "LIVE_AFTER_CLASSICAL_OWNER", "remaining": "distributional R_eq=0, boundary flux zero, same worldtube H_tau/MHref", "source_path": str(FORMAL_436), "valid_for_claim": False},
        {"reduction_id": "RED4442_3_next_best_target", "object": "least circular next proof", "status": "PARENT_GRAPH_EDGE_OR_REQ_VALUE", "remaining": NEXT_TARGET, "source_path": str(FORMAL_450), "valid_for_claim": False},
    ]


def claim_gate_rows(route_outputs: Sequence[Mapping[str, str]], tail_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    route_by_id = {row["row_id"]: row for row in route_outputs}
    tail_by_id = {row["tail_id"]: row for row in tail_outputs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in route_outputs) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs)
    return [
        {"gate_id": "CG4442_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4442_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No unsourced import."},
        {"gate_id": "CG4442_2_current_branch_open", "claim": "current post-EM branch is still open", "passed": route_by_id["NEM4442_0_current_post_EM_branch"].get("current_status") == "CLASSICAL_SOURCE_OWNER_CLAUSES_OPEN_EM_REMOVED", "valid_for_claim": False, "detail": "EM removed, nonEM owner/current locks still open."},
        {"gate_id": "CG4442_3_classical_contract_without_hbar", "claim": "classical local source contract can close without hbar premise", "passed": route_by_id["NEM4442_1_future_classical_local_source_contract"].get("current_status") == "CLASSICAL_LOCAL_SOURCE_OWNER_CONTRACT_READY_HBAR_QUANTUM_GUARD_OPEN_NONCLAIM", "valid_for_claim": False, "detail": "hbar becomes quantum guard, not first classical local-source lock."},
        {"gate_id": "CG4442_4_hbar_only_insufficient", "claim": "hbar owner alone closes local source coupling", "passed": route_by_id["NEM4442_3_hbar_only_counterroute"].get("current_status") == "HBAR_MEASURE_OWNER_ALONE_INSUFFICIENT_FOR_LOCAL_SOURCE", "valid_for_claim": False, "detail": "graph/current/no-Hom/R_eq still needed."},
        {"gate_id": "CG4442_5_tail_controls", "claim": "tail gate has pass and fail controls", "passed": tail_by_id["TAIL4442_4_small_smoke"].get("current_status") == "REQ_BZERO_TAIL_SCHEMA_PASS_NONCLAIM" and tail_by_id["TAIL4442_5_fail_control"].get("current_status") == "REQ_BZERO_TAIL_FAILS_BOUND", "valid_for_claim": False, "detail": "Tail gate catches safe/failing controls."},
        {"gate_id": "CG4442_6_live_tail_targets", "claim": "R_eq, B_zero and H_tau/MHref live tail targets written", "passed": all(key in text(TAIL_OUTPUT) for key in ("TAIL4442_0_Req_compact_test_live", "TAIL4442_1_Bzero_boundary_flux_live", "TAIL4442_2_Htau_MHref_mismatch_live")), "valid_for_claim": False, "detail": "Live rows require values/projections."},
        {"gate_id": "CG4442_7_no_public_claim", "claim": "4442 emits no local-GR/Newton/PPN public claim", "passed": no_claims, "valid_for_claim": False, "detail": "All outputs remain private nonclaim."},
        {"gate_id": "CG4442_8_next_target_written", "claim": "next target selected", "passed": NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4442_0",
            "decision": DECISION,
            "summary": "4442 makes a real proof-order move: for classical Newton/local-GR source coupling, universal hbar is not the first necessary lock. The classical no-wA route is one parent action-density/current owner, common measure, typed no-source Hom, constructor exhaustion, no hidden/readout reentry, derivative-silent common mode and a parent-owned connected nonEM matter graph. Hbar/quantum measure remains a quantum-statistical guard. The current corpus still has the graph/constructor/current/R_eq/B_zero/H_tau locks unsigned, so the next best target is a parent-owned connected nonEM graph edge or one real R_eq compact-test value.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4442_0_route_split", "object": "hbar/measure owner", "status": "QUANTUM_GUARD_NOT_FIRST_CLASSICAL_SOURCE_LOCK", "detail": "Classical source coupling can be attacked via action-density/current/graph/no-Hom first.", "valid_for_claim": False},
        {"status_id": "STAT4442_1_current_branch", "object": "current post-EM nonEM source branch", "status": "EM_REMOVED_NONEM_OWNER_OPEN", "detail": "Fixed EM is not the current bottleneck; nonEM owner/R_eq/H_tau are.", "valid_for_claim": False},
        {"status_id": "STAT4442_2_tail_values", "object": "R_eq/B_zero/H_tau finite branch", "status": "LIVE_TARGETS_VALUES_MISSING", "detail": "Need compact-test value, boundary flux value or H_tau/MHref mismatch value with projection and arena bound.", "valid_for_claim": False},
        {"status_id": "STAT4442_3_next", "object": "next target", "status": "PARENT_GRAPH_EDGE_OR_REQ_COMPACT_TEST", "detail": NEXT_TARGET, "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4442_0",
            "target": NEXT_TARGET,
            "objective": "Close the least-circular classical source owner lock or fill the first real same-current tail value.",
            "derive_first": "parent-sign one nonzero ordinary-matter action-density/current graph edge after fixed EM is removed, preferably lepton/mass or quark/gluon source edge, with no species/source prefactor and no readout re-entry",
            "fallback": "fill R_eq compact-test or B_zero flux with value, units, source path, projection coefficient, arena bound and no-cancellation guard",
            "avoid": "making hbar ownership do classical source work by itself; counting physical graph templates as parent-owned edges; using observed GM or comparator bounds as R_eq values",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], route_outputs: Sequence[Mapping[str, object]], tail_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 458 PPC4161 nonEM universal hbar measure owner proof or first Req Bzero tail value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4442 changes the order of attack:

```text
For classical local GR/Newton source coupling:
  hbar is not the first lock.

Needed first:
  one classical parent action-density/current owner
  + common classical variational measure
  + no Hom(SpeciesLabel, Coeff_active_source)
  + constructor exhaustion and no hidden/readout re-entry
  + parent-owned connected nonEM matter graph
  + derivative-silent common mode
  + same-current R_eq=0, B_zero flux silence, H_tau/MHref locks

Then:
  relative w_A collapses to one common w_*
  common w_* is G_cal/GM calibration only if derivative-silent
```

So hbar/quantum measure is still important, but it is demoted to the quantum/statistical guard. The next least-circular local-GR move is a parent-owned connected nonEM graph/current edge or a real `R_eq/B_zero` tail value.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## NonEM Source Route Gate

{table(route_outputs)}

## First R_eq / B_zero Tail Gate

{table(tail_outputs)}

## Reduction Rows

{table(reduction_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Status

{table(status_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4442 Y5 R2FR nonEM universal hbar measure owner proof or first Req Bzero tail value

Private checkpoint generated at `{STAMP}`.

Formal mirror: `{FORMAL_PATH}`

Decision: `{DECISION}`

Summary:
- Classical local source coupling can be attacked without making `hbar` the first lock.
- The exact route is parent action-density/current + no source-Hom + constructor exhaustion + connected nonEM graph + same-current `R_eq/B_zero/H_tau`.
- Current branch remains nonclaim; live values for `R_eq`, `B_zero`, and `H_tau/MHref` are still missing.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_source_coupling",
        "claim": "4442 derives the proof-order split: universal hbar/measure is not the first lock for classical Newton/local-GR source coupling. The classical route is a parent action-density/current owner, common variational measure, no species/source Hom, constructor exhaustion, no hidden/readout reentry, derivative-silent common mode, parent-owned connected nonEM graph, and same-current R_eq/B_zero/H_tau locks. Current corpus remains nonclaim.",
        "current_evidence": "4442 source register, derivation rows, nonEM source route gate, first R_eq/B_zero tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "nonEM_classical_source_owner_route_split_derived_hbar_quantum_guard_Req_Bzero_Htau_open_nonclaim",
        "next_test": "Parent-sign one connected nonEM action-density/current graph edge or fill first R_eq compact-test/B_zero flux value.",
        "key_risk": "Treating hbar as a classical source-coupling proof; counting graph templates as parent-owned; using observed GM/comparator bounds as R_eq values.",
        "sector": "local_gr_source_coupling",
        "evidence": "4442 source register, derivation rows, nonEM source route gate, first R_eq/B_zero tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Parent-sign one connected nonEM action-density/current graph edge or fill first R_eq compact-test/B_zero flux value.",
        "risk": "Treating hbar as a classical source-coupling proof; counting graph templates as parent-owned; using observed GM/comparator bounds as R_eq values.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(new_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Source Coupling Update - NonEM Classical Route Split

Marker: `{MARKER}`  
Source checkpoint: `4442-Y5-R2FR-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md`  
Claim register row: `{CLAIM_ID}`

The source-coupling bottleneck has been split more cleanly. Universal `hbar`/quantum measure is no longer treated as the first classical local-GR source lock. For Newton/local GR, the least-circular route is now classical: one parent action-density/current owner, no species/source Hom, constructor exhaustion, no hidden/readout re-entry, parent-owned connected nonEM matter graph, derivative-silent common mode, and then `R_eq/B_zero/H_tau` same-current locks.
"""
    packet_section = f"""## PPC4161 Packet Addendum - NonEM Classical Source Route Split

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4442-Y5-R2FR-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md`

The packet now routes classical source-coupling proof through parent action-density/current ownership and connected nonEM graph/no-Hom signatures first. `hbar` remains a quantum/statistical guard, not the first local Newton/GR source-coupling lock. The immediate next target is a parent-owned nonEM graph edge or one real `R_eq/B_zero` tail value.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    routes = {row["row_id"]: row for row in rows_from(ROUTE_OUTPUT)}
    tails = {row["tail_id"]: row for row in rows_from(TAIL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in routes.values()) and not any(row.get("valid_for_claim") == "True" for row in tails.values())
    checks = [
        ("VAL4442_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4442_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4442_2_current_open", routes["NEM4442_0_current_post_EM_branch"].get("current_status") == "CLASSICAL_SOURCE_OWNER_CLAUSES_OPEN_EM_REMOVED", "current branch keeps EM removed but nonEM owner open"),
        ("VAL4442_3_classical_without_hbar", routes["NEM4442_1_future_classical_local_source_contract"].get("current_status") == "CLASSICAL_LOCAL_SOURCE_OWNER_CONTRACT_READY_HBAR_QUANTUM_GUARD_OPEN_NONCLAIM", "classical contract does not require hbar premise"),
        ("VAL4442_4_hbar_only_insufficient", routes["NEM4442_3_hbar_only_counterroute"].get("current_status") == "HBAR_MEASURE_OWNER_ALONE_INSUFFICIENT_FOR_LOCAL_SOURCE", "hbar-only route rejected"),
        ("VAL4442_5_tail_smoke_pass", tails["TAIL4442_4_small_smoke"].get("current_status") == "REQ_BZERO_TAIL_SCHEMA_PASS_NONCLAIM", "small tail smoke row passes schema nonclaim"),
        ("VAL4442_6_tail_fail_control", tails["TAIL4442_5_fail_control"].get("current_status") == "REQ_BZERO_TAIL_FAILS_BOUND", "fail-control tail row fails bound"),
        ("VAL4442_7_live_tail_targets", all(key in text(TAIL_OUTPUT) for key in ("TAIL4442_0_Req_compact_test_live", "TAIL4442_1_Bzero_boundary_flux_live", "TAIL4442_2_Htau_MHref_mismatch_live")), "live R_eq/B_zero/H_tau rows written"),
        ("VAL4442_8_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4442_9_claim_gate_no_claim", any(row["gate_id"] == "CG4442_7_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4442_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-283"),
        ("VAL4442_11_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4442_12_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4442_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4442_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4442_15_next_gate", any(row["gate_id"] == "CG4442_8_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4442_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4442_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(ROUTE_INPUT, route_input_rows())
    write_csv(ROUTE_OUTPUT, evaluate_route_rows(ROUTE_INPUT))
    write_csv(TAIL_INPUT, tail_input_rows())
    write_csv(TAIL_OUTPUT, evaluate_tail_rows(TAIL_INPUT))
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    route_outputs = rows_from(ROUTE_OUTPUT)
    tail_outputs = rows_from(TAIL_OUTPUT)
    gates = claim_gate_rows(route_outputs, tail_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), route_outputs, tail_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
