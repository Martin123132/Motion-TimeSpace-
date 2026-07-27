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

from action_measure_current_owner_gate import evaluate_owner_rows, evaluate_tail_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4441"
CLAIM_ID = "L-282"
MARKER = "PPC4161_ACTION_MEASURE_CURRENT_OWNER_AFTER_EM_ZERO_OR_REQ_TAILS_4441"
PACKET_MARKER = "PPC4161_PACKET_ACTION_MEASURE_CURRENT_OWNER_AFTER_EM_ZERO_4441"
DECISION = "FIXED_EM_OWNER_SUBCONTRACT_CLOSED_NONEM_ACTION_MEASURE_CURRENT_AND_REQ_TAILS_REMAIN_NONCLAIM"
NEXT_TARGET = "4442-Y5-R2FR-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md"

FORMAL_PATH = FORMAL / "457-PPC4161-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md"
DOC_PATH = POST / "4441-Y5-R2FR-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4441_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4441_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4441_DERIVATION_ROWS.csv"
OWNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4441_ACTION_MEASURE_CURRENT_OWNER_INPUT.csv"
OWNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4441_ACTION_MEASURE_CURRENT_OWNER_OUTPUT.csv"
TAIL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4441_REQ_BZERO_TAIL_INPUT.csv"
TAIL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4441_REQ_BZERO_TAIL_OUTPUT.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4441_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4441_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4441_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4441_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4441_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "action_measure_current_owner_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4441_action_measure_current_owner_contract_after_EM_zero_or_Req_tail_values.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4440 = SOURCE_DIR / "P8_Y5_R2FR_4440_NEXT_TARGET.csv"
FORMAL_456 = FORMAL / "456-PPC4161-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md"
FORMAL_436 = FORMAL / "436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md"
FORMAL_437 = FORMAL / "437-PPC4161-single-phase-action-owner-from-MTS-time-flow-or-first-Deltaw-tau-Req-values.md"
FORMAL_438 = FORMAL / "438-PPC4161-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
FORMAL_440 = FORMAL / "440-PPC4161-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md"
FORMAL_451 = FORMAL / "451-PPC4161-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
FORMAL_452 = FORMAL / "452-PPC4161-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md"
FORMAL_454 = FORMAL / "454-PPC4161-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"
OUTPUT_4420_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4420_ACTION_MEASURE_OWNER_OUTPUT.csv"
OUTPUT_4420_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4420_DELTAW_TAU_REQ_BOUND_OUTPUT.csv"
OUTPUT_4438_KLEG = SOURCE_DIR / "P8_Y5_R2FR_4438_K_ACTION_SOURCE_LEG_OUTPUT.csv"

SMOKE_BOUND = 1.0e-5
SMOKE_PASS_VALUE = 5.0e-7
SMOKE_FAIL_VALUE = 2.0e-3


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
        {"source_id": "SRC4441_00_4440_next", "path": NEXT_4440, "needle": "action-measure/current owner", "role": "4440 handoff."},
        {"source_id": "SRC4441_01_456_source_owner", "path": FORMAL_456, "needle": "RC4440_2_source_owner", "role": "4440 source-owner reduction."},
        {"source_id": "SRC4441_02_436_phase", "path": FORMAL_436, "needle": "AMO4420_0_phase_hbar_owner_lemma", "role": "phase/hbar obstruction reduction."},
        {"source_id": "SRC4441_03_437_time_seed", "path": FORMAL_437, "needle": "MTS_TIME_FLOW_SUPPLIES_PHASE_LINE_SEED", "role": "single-phase seed from MTS time flow."},
        {"source_id": "SRC4441_04_438_hbar", "path": FORMAL_438, "needle": "HMO4422_3_future_universal_hbar_measure_contract", "role": "universal hbar/measure contract."},
        {"source_id": "SRC4441_05_439_action_density", "path": FORMAL_439, "needle": "ADLO4423_4_future_action_density_owner_contract", "role": "action-density owner contract."},
        {"source_id": "SRC4441_06_440_constructor", "path": FORMAL_440, "needle": "PARENT_CONSTRUCTOR_ATLAS_READY", "role": "constructor exhaustion status."},
        {"source_id": "SRC4441_07_451_graph", "path": FORMAL_451, "needle": "EDGE4435_1_L_parent_to_EM_visible_domain", "role": "first action-density edge reduction."},
        {"source_id": "SRC4441_08_452_EM_edge", "path": FORMAL_452, "needle": "VEM4436_0_standard_visible_branch_edge_signature", "role": "fixed visible EM owner edge."},
        {"source_id": "SRC4441_09_454_EM_tail", "path": FORMAL_454, "needle": "KLEG4438_0_total_fixed_branch_EM_product_zero", "role": "fixed EM action-scale tail zero."},
        {"source_id": "SRC4441_10_4420_owner_csv", "path": OUTPUT_4420_OWNER, "needle": "AOC4420_0_phase_hbar_owner_attempt", "role": "machine-readable owner gate precedent."},
        {"source_id": "SRC4441_11_4420_tail_csv", "path": OUTPUT_4420_TAIL, "needle": "ARB4420_1_Req_moment_bound", "role": "machine-readable R_eq/B_zero tail precedent."},
        {"source_id": "SRC4441_12_4438_kleg_csv", "path": OUTPUT_4438_KLEG, "needle": "KLEG4438_0_total_fixed_branch_EM_product_zero", "role": "machine-readable fixed EM zero."},
        {"source_id": "SRC4441_13_gate", "path": GATE_PATH, "needle": "def evaluate_owner_row", "role": "4441 owner/tail gate."},
        {"source_id": "SRC4441_14_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4441\"", "role": "4441 generator."},
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
            "derivation_id": "AMCO4441_0_fixed_EM_subcontract",
            "claim": "The fixed visible EM branch now supplies a closed action-measure/current subcontract.",
            "derivation": "4436 signs the Maxwell-Hodge EM edge inside the standard visible/private local branch; 4437 fixes the q-basic F2/current/alpha scale-current throat; 4438 closes the readout/radiative fixed-branch EM action-scale product; 4439-4440 remove that fixed EM tail from epsilon_Gsrc. Therefore EM is not the live relative action-scale owner obstruction in this fixed branch.",
            "consequence": "The action-measure/current owner problem is reduced to non-EM ordinary matter hbar/measure/constructor/current ownership plus R_eq/B_zero, while open/global EM remains separately retained.",
            "status": "FIXED_EM_OWNER_SUBCONTRACT_CLOSED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "AMCO4441_1_nonEM_owner_contract",
            "claim": "The remaining clean proof is a non-EM universal hbar/measure/current theorem.",
            "derivation": "A relative matter-sector action weight w_A is equivalent to a species action quantum hbar_A=hbar_parent/w_A unless a single parent phase/hbar/measure owner, species-blind Jacobian, connected matter graph, constructor exhaustion, no Hom(SpeciesLabel,Coeff_active_source), and no readout re-entry all hold.",
            "consequence": "The proof target is now exact: derive the parent non-EM action-measure/current owner or carry Delta_w/tau_WEP/R_eq/B_zero tails.",
            "status": "NONEM_OWNER_THEOREM_EXACT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "AMCO4441_2_same_current_req",
            "claim": "A closed current is not enough; it must be the same Hilbert/Hamiltonian current.",
            "derivation": "If J_M^top is closed but Pi_M J_H = J_M^top + dB_zero + R_eq with nonzero R_eq or boundary flux, then the closed current can be the wrong source. The required theorem is distributional R_eq=0 and zero-flux improvement on the same worldtube before readout.",
            "consequence": "R_eq compact-test/multipole rows and B_zero flux rows are the first finite fallback, not observed GM backfill.",
            "status": "REQ_BZERO_CONTRACT_SHARPENED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "AMCO4441_3_public_firewall",
            "claim": "No local GR/Newton public claim follows from the EM subcontract.",
            "derivation": "The fixed EM owner subcontract is branch-local. Universal non-EM hbar/measure ownership, constructor exhaustion, total source current ownership, H_tau/MHref locks, R_eq/B_zero and arena projection values remain open.",
            "consequence": NEXT_TARGET,
            "status": "PUBLIC_CLAIM_BLOCKED_NEXT_NONEM_OWNER_OR_REQ_VALUES",
            "valid_for_claim": False,
        },
    ]


def owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "owner_id": "AMCO4441_0_current_after_EM_subcontract",
            "branch": "fixed clean visible-EM subcontract closed branch",
            "single_phase_seed": True,
            "universal_hbar_parent": False,
            "universal_measure_owner": False,
            "action_density_owner": False,
            "constructor_exhaustion": False,
            "hom_species_to_source_empty": False,
            "connected_matter_graph": False,
            "total_source_current_owner": False,
            "fixed_EM_edge_signed": True,
            "fixed_EM_tail_zero": True,
            "same_current_Req_zero": False,
            "boundary_improvement_zero_flux": False,
            "Htau_MHref_locks": False,
            "no_readout_reentry": False,
            "source_path": str(FORMAL_456),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "owner_id": "AMCO4441_1_future_nonEM_full_owner_contract",
            "branch": "future nonEM action-measure/current owner clean branch",
            "single_phase_seed": True,
            "universal_hbar_parent": True,
            "universal_measure_owner": True,
            "action_density_owner": True,
            "constructor_exhaustion": True,
            "hom_species_to_source_empty": True,
            "connected_matter_graph": True,
            "total_source_current_owner": True,
            "fixed_EM_edge_signed": True,
            "fixed_EM_tail_zero": True,
            "same_current_Req_zero": True,
            "boundary_improvement_zero_flux": True,
            "Htau_MHref_locks": True,
            "no_readout_reentry": True,
            "source_path": str(FORMAL_439),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "owner_id": "AMCO4441_2_open_global_or_dynamic_EM_branch",
            "branch": "global/dynamic EM or unselected matter branch",
            "single_phase_seed": True,
            "universal_hbar_parent": False,
            "universal_measure_owner": False,
            "action_density_owner": False,
            "constructor_exhaustion": False,
            "hom_species_to_source_empty": False,
            "connected_matter_graph": False,
            "total_source_current_owner": False,
            "fixed_EM_edge_signed": False,
            "fixed_EM_tail_zero": False,
            "same_current_Req_zero": False,
            "boundary_improvement_zero_flux": False,
            "Htau_MHref_locks": False,
            "no_readout_reentry": False,
            "source_path": str(FORMAL_454),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
    ]


def tail_input_rows() -> List[Dict[str, object]]:
    return [
        {"tail_id": "TAIL4441_0_Deltaw_live_contract", "tail": "Delta_w_AB", "arena": "WEP_R10_PPN_source_weight", "normal_form": "P_WEP=|Delta_w_AB*tau_WEP| or P_arena Delta_w_AB", "projection_coeff": "MISSING_P_DELTAW", "tail_value": "MISSING_DELTA_W_AB", "arena_bound": "MISSING_ARENA_BOUND", "units": "dimensionless", "source_path": str(FORMAL_436), "input_valid_for_claim": False},
        {"tail_id": "TAIL4441_1_Req_live_contract", "tail": "R_eq_harmonic_moment", "arena": "Newton_PPN_orbital_source_profile", "normal_form": "delta a_l/a_N <= P_l |R_eq_l|", "projection_coeff": "MISSING_P_REQ", "tail_value": "MISSING_REQ_MOMENT", "arena_bound": "MISSING_ARENA_BOUND", "units": "dimensionless", "source_path": str(FORMAL_436), "input_valid_for_claim": False},
        {"tail_id": "TAIL4441_2_Bzero_live_contract", "tail": "B_zero_flux", "arena": "source_flux_Gdot_radial_Newton", "normal_form": "epsilon_Bzero_flux = |int_boundary dB_zero|/M_H_ref", "projection_coeff": "MISSING_P_BZERO", "tail_value": "MISSING_BZERO_FLUX", "arena_bound": "MISSING_ARENA_BOUND", "units": "dimensionless", "source_path": str(FORMAL_436), "input_valid_for_claim": False},
        {"tail_id": "TAIL4441_3_zero_smoke", "tail": "R_eq_harmonic_moment", "arena": "schema_smoke", "normal_form": "P_tail*tail <= bound", "projection_coeff": "1", "tail_value": "0", "arena_bound": f"{SMOKE_BOUND:.12g}", "units": "dimensionless", "source_path": str(OUTPUT_4420_TAIL), "input_valid_for_claim": False},
        {"tail_id": "TAIL4441_4_small_smoke", "tail": "R_eq_harmonic_moment", "arena": "schema_smoke", "normal_form": "P_tail*tail <= bound", "projection_coeff": "1", "tail_value": f"{SMOKE_PASS_VALUE:.12g}", "arena_bound": f"{SMOKE_BOUND:.12g}", "units": "dimensionless", "source_path": str(OUTPUT_4420_TAIL), "input_valid_for_claim": False},
        {"tail_id": "TAIL4441_5_fail_control", "tail": "R_eq_harmonic_moment", "arena": "schema_smoke", "normal_form": "P_tail*tail <= bound", "projection_coeff": "1", "tail_value": f"{SMOKE_FAIL_VALUE:.12g}", "arena_bound": f"{SMOKE_BOUND:.12g}", "units": "dimensionless", "source_path": str(OUTPUT_4420_TAIL), "input_valid_for_claim": False},
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {"reduction_id": "RED4441_0_fixed_EM_subcontract", "object": "fixed visible EM action-measure/current", "status": "CLOSED_INSIDE_STANDARD_VISIBLE_BRANCH", "remaining": "open/global EM retained separately", "source_path": str(FORMAL_454), "valid_for_claim": False},
        {"reduction_id": "RED4441_1_nonEM_owner", "object": "nonEM ordinary matter action-measure/current owner", "status": "EXACT_CONDITIONAL_UNSIGNED", "remaining": "universal hbar/measure, constructor exhaustion, connected graph, no readout re-entry", "source_path": str(FORMAL_439), "valid_for_claim": False},
        {"reduction_id": "RED4441_2_same_current", "object": "J_M^top = Pi_M J_H + dB_zero + R_eq", "status": "REQ_BZERO_OPEN", "remaining": "distributional R_eq=0 and zero boundary improvement flux", "source_path": str(FORMAL_436), "valid_for_claim": False},
        {"reduction_id": "RED4441_3_finite_tail", "object": "Delta_w/tau_WEP/R_eq/B_zero tails", "status": "SCHEMA_READY_VALUES_MISSING", "remaining": "source-backed values, units, projections and arena bounds", "source_path": str(OUTPUT_4420_TAIL), "valid_for_claim": False},
    ]


def claim_gate_rows(owner_outputs: Sequence[Mapping[str, str]], tail_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    owner_by_id = {row["owner_id"]: row for row in owner_outputs}
    tail_by_id = {row["tail_id"]: row for row in tail_outputs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owner_outputs) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs)
    return [
        {"gate_id": "CG4441_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4441_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No unsourced import."},
        {"gate_id": "CG4441_2_fixed_EM_subcontract", "claim": "fixed EM owner subcontract closed", "passed": owner_by_id["AMCO4441_0_current_after_EM_subcontract"].get("current_status") == "FIXED_EM_OWNER_SUBCONTRACT_CLOSED_NONEM_OWNER_OPEN", "valid_for_claim": False, "detail": "EM is removed from the fixed-branch action-measure/current bottleneck."},
        {"gate_id": "CG4441_3_future_contract_nonclaim", "claim": "full future owner contract executable", "passed": owner_by_id["AMCO4441_1_future_nonEM_full_owner_contract"].get("current_status") == "ACTION_MEASURE_CURRENT_OWNER_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact theorem contract exists but is not parent/public signed."},
        {"gate_id": "CG4441_4_tail_controls", "claim": "tail gate has pass and fail controls", "passed": tail_by_id["TAIL4441_4_small_smoke"].get("current_status") == "OWNER_TAIL_SCHEMA_PASS_NONCLAIM" and tail_by_id["TAIL4441_5_fail_control"].get("current_status") == "OWNER_TAIL_FAILS_BOUND", "valid_for_claim": False, "detail": "Tail schema catches safe and failing controls."},
        {"gate_id": "CG4441_5_live_tail_contracts", "claim": "Delta_w/R_eq/B_zero live contracts written", "passed": all(key in text(TAIL_OUTPUT) for key in ("TAIL4441_0_Deltaw_live_contract", "TAIL4441_1_Req_live_contract", "TAIL4441_2_Bzero_live_contract")), "valid_for_claim": False, "detail": "Live rows require values/projections."},
        {"gate_id": "CG4441_6_no_public_claim", "claim": "4441 emits no local-GR/Newton/PPN public claim", "passed": no_claims, "valid_for_claim": False, "detail": "All outputs remain nonclaim."},
        {"gate_id": "CG4441_7_next_target_written", "claim": "next target selected", "passed": NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4441_0",
            "decision": DECISION,
            "summary": "4441 integrates the EM progress back into the action-measure/current owner problem. The fixed standard visible EM branch now behaves as a closed owner subcontract: EM action edge signed, scale/current/readout/radiative fixed-tail product zero, and fixed EM removed from epsilon_Gsrc. This does not close the source law. The remaining hard proof is non-EM universal hbar/measure/action-density/current ownership plus constructor exhaustion, connected matter graph, no readout re-entry, same-current R_eq=0, B_zero flux silence and H_tau/MHref locks. First finite Delta_w, R_eq and B_zero tail contracts are executable with smoke/fail controls but live values remain missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4441_0_EM_owner", "object": "fixed visible EM owner subcontract", "status": "CLOSED_BRANCH_CONDITIONAL", "detail": "Closed only inside fixed q-basic same-Hodge static standard-visible branch.", "valid_for_claim": False},
        {"status_id": "STAT4441_1_nonEM_owner", "object": "nonEM universal hbar/measure/current owner", "status": "OPEN_EXACT_CONTRACT", "detail": "This is now the main coupling proof target.", "valid_for_claim": False},
        {"status_id": "STAT4441_2_same_current", "object": "R_eq/B_zero", "status": "OPEN_TAIL_OR_PROOF", "detail": "Need distributional equality or source-backed compact-test/moment values.", "valid_for_claim": False},
        {"status_id": "STAT4441_3_next", "object": "next target", "status": "NONEM_OWNER_OR_FIRST_REQ_BZERO_VALUE", "detail": NEXT_TARGET, "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4441_0",
            "target": NEXT_TARGET,
            "objective": "Attack the non-EM universal hbar/measure owner directly, or fill first real R_eq/B_zero tail values.",
            "derive_first": "prove ordinary non-EM matter lives on one parent hbar/measure/action-density/current owner with constructor exhaustion, no species/source Hom and no readout re-entry",
            "fallback": "fill one R_eq compact-test/multipole moment or B_zero boundary flux row with value, units, source path, projection coefficient and arena bound",
            "avoid": "using the fixed EM subcontract as a global matter proof; using total mass as distributional equality; using observed GM or comparator bounds as source definitions",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], owner_outputs: Sequence[Mapping[str, object]], tail_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 457 PPC4161 action measure current owner contract after EM zero or Req tail values

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4441 makes the coupling target sharper:

```text
fixed visible EM branch:
  L_parent -> EM edge signed
  C_XF2=C_JQ=b_alpha=dlnlambda=C_EM_readout=Phi_EM_rad=Delta_Hodge_EM=0
  => fixed EM action-scale/current tail deleted from epsilon_Gsrc

remaining source-coupling owner:
  nonEM universal hbar/measure/action-density/current owner
  + constructor exhaustion
  + connected matter graph
  + no species/source Hom
  + same-current R_eq=0
  + B_zero flux silence
  + H_tau/MHref locks
```

So the fixed EM branch is no longer the action-measure/current bottleneck. The live bottleneck is non-EM ordinary matter ownership and same-current equality.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Action-Measure / Current Owner Gate

{table(owner_outputs)}

## R_eq / B_zero Tail Gate

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
    return f"""# 4441 Y5 R2FR action measure current owner contract after EM zero or Req tail values

Private checkpoint generated at `{STAMP}`.

Formal mirror: `{FORMAL_PATH}`

Decision: `{DECISION}`

Summary:
- Fixed visible EM is now a closed owner subcontract inside the standard fixed branch.
- Non-EM universal hbar/measure/current ownership and `R_eq/B_zero` remain the live coupling proof.
- Delta_w, R_eq and B_zero fallback rows are executable but nonclaim until sourced values/projections exist.

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
        "claim": "4441 closes the fixed visible EM branch as an action-measure/current subcontract and removes it from the fixed-branch source-coupling bottleneck. The remaining live proof is non-EM universal hbar/measure/current ownership plus R_eq/B_zero/H_tau/MHref locks; finite Delta_w, R_eq and B_zero rows are staged but nonclaim.",
        "current_evidence": "4441 source register, derivation rows, action-measure/current owner gate, R_eq/B_zero tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "fixed_EM_owner_subcontract_closed_nonEM_action_measure_current_and_Req_tails_open_nonclaim",
        "next_test": "Prove non-EM universal hbar/measure/current owner or fill first real R_eq/B_zero tail value.",
        "key_risk": "Globalizing the fixed EM branch; treating closed current as same current; using total mass or observed GM as source equality.",
        "sector": "local_gr_source_coupling",
        "evidence": "4441 source register, derivation rows, action-measure/current owner gate, R_eq/B_zero tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove non-EM universal hbar/measure/current owner or fill first real R_eq/B_zero tail value.",
        "risk": "Globalizing the fixed EM branch; treating closed current as same current; using total mass or observed GM as source equality.",
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
    spine_section = f"""## Local GR Source Coupling Update - Fixed EM Owner Subcontract

Marker: `{MARKER}`  
Source checkpoint: `4441-Y5-R2FR-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md`  
Claim register row: `{CLAIM_ID}`

The fixed standard-visible EM branch is now a closed owner subcontract for the source-coupling spine. It does not prove universal matter coupling. The remaining source-coupling proof is non-EM universal hbar/measure/action-density/current ownership plus `R_eq=0`, `B_zero` flux silence and H_tau/MHref locks.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Fixed EM Owner Subcontract

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4441-Y5-R2FR-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md`

The packet now treats fixed visible EM as closed for action-measure/current purposes inside the standard fixed branch. Open/global EM remains separate. The live local-GR coupling gap is non-EM ordinary matter owner proof and same-current `R_eq/B_zero` closure.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    owners = {row["owner_id"]: row for row in rows_from(OWNER_OUTPUT)}
    tails = {row["tail_id"]: row for row in rows_from(TAIL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owners.values()) and not any(row.get("valid_for_claim") == "True" for row in tails.values())
    checks = [
        ("VAL4441_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4441_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4441_2_EM_subcontract", owners["AMCO4441_0_current_after_EM_subcontract"].get("current_status") == "FIXED_EM_OWNER_SUBCONTRACT_CLOSED_NONEM_OWNER_OPEN", "fixed EM subcontract closed and nonEM owner open"),
        ("VAL4441_3_future_contract", owners["AMCO4441_1_future_nonEM_full_owner_contract"].get("current_status") == "ACTION_MEASURE_CURRENT_OWNER_CONTRACT_READY_NONCLAIM", "future full owner contract executable nonclaim"),
        ("VAL4441_4_tail_smoke_pass", tails["TAIL4441_4_small_smoke"].get("current_status") == "OWNER_TAIL_SCHEMA_PASS_NONCLAIM", "small tail smoke row passes schema nonclaim"),
        ("VAL4441_5_tail_fail_control", tails["TAIL4441_5_fail_control"].get("current_status") == "OWNER_TAIL_FAILS_BOUND", "fail-control tail row fails bound"),
        ("VAL4441_6_live_tail_contracts", all(key in text(TAIL_OUTPUT) for key in ("TAIL4441_0_Deltaw_live_contract", "TAIL4441_1_Req_live_contract", "TAIL4441_2_Bzero_live_contract")), "live Delta_w/R_eq/B_zero rows written"),
        ("VAL4441_7_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4441_8_claim_gate_no_claim", any(row["gate_id"] == "CG4441_6_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4441_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-282"),
        ("VAL4441_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4441_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4441_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4441_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4441_14_next_gate", any(row["gate_id"] == "CG4441_7_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4441_15_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4441_16_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(OWNER_INPUT, owner_input_rows())
    write_csv(OWNER_OUTPUT, evaluate_owner_rows(OWNER_INPUT))
    write_csv(TAIL_INPUT, tail_input_rows())
    write_csv(TAIL_OUTPUT, evaluate_tail_rows(TAIL_INPUT))
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    owner_outputs = rows_from(OWNER_OUTPUT)
    tail_outputs = rows_from(TAIL_OUTPUT)
    gates = claim_gate_rows(owner_outputs, tail_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), owner_outputs, tail_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
