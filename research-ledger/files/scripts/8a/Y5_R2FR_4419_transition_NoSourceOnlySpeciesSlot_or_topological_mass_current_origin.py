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

from source_slot_topological_current_gate import (  # noqa: E402
    evaluate_source_slot_rows,
    evaluate_topological_current_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4419"
CLAIM_ID = "L-260"
MARKER = "PPC4161_TRANSITION_NOSOURCEONLYSPECIES_OR_TOPOLOGICAL_MASS_CURRENT_ORIGIN_4419"
PACKET_MARKER = "PPC4161_PACKET_NOSOURCEONLYSPECIES_OR_TOPOLOGICAL_MASS_CURRENT_ORIGIN_4419"
DECISION = "SOURCE_COUPLING_REDUCED_TO_PARENT_ACTION_MEASURE_AND_SAME_CURRENT_CONTRACT_NONCLAIM"
NEXT_TARGET = "4420-Y5-R2FR-parent-action-measure-current-owner-or-Req-moment-bound.md"

FORMAL_PATH = FORMAL / "435-PPC4161-transition-NoSourceOnlySpeciesSlot-or-topological-mass-current-origin.md"
DOC_PATH = POST / "4419-Y5-R2FR-transition-NoSourceOnlySpeciesSlot-or-topological-mass-current-origin.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4419_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4419_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4419_DERIVATION_ROWS.csv"
SOURCE_SLOT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4419_SOURCE_SLOT_THEOREM_INPUT.csv"
SOURCE_SLOT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4419_SOURCE_SLOT_THEOREM_OUTPUT.csv"
TOPO_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4419_TOPOLOGICAL_CURRENT_INPUT.csv"
TOPO_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4419_TOPOLOGICAL_CURRENT_OUTPUT.csv"
PARENT_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4419_PARENT_ACTION_CONTRACT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4419_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4419_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4419_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4419_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "source_slot_topological_current_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4419_transition_NoSourceOnlySpeciesSlot_or_topological_mass_current_origin.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4418 = SOURCE_DIR / "P8_Y5_R2FR_4418_NEXT_TARGET.csv"
FORMAL_434 = FORMAL / "434-PPC4161-transition-mass-flux-GM-common-mode-closure-or-source-profile-bound.md"
POST_2772 = POST / "2772-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row-under-AX1090.md"
POST_2773 = POST / "2773-Y5-R2FR-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width-under-AX1090.md"
POST_2881 = POST / "2881-Y5-R2FR-JR-matter-source-current-or-matter-descent-zero-under-AX1090.md"
POST_4376 = POST / "4376-Y5-R2FR-transition-source-shadow-ban-or-Eprofile-first-source-density-row.md"
POST_4377 = POST / "4377-Y5-R2FR-transition-parent-grammar-no-source-shadow-or-topological-profile-equality.md"
POST_3573 = POST / "3573-Y5-R2FR-PiM-flux-closure-Ward-Euler-or-Meff-drift-bound.md"
POST_1013 = POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
POST_2900 = POST / "2900-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill-under-AX1090.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists():
        return 0
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if needle in line:
            return index
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
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4419_00_4418_next",
            "path": NEXT_4418,
            "needle": "4419-Y5-R2FR-transition-NoSourceOnlySpeciesSlot-or-topological-mass-current-origin.md",
            "role": "4418 handoff into source-slot/topological mass-current proof.",
        },
        {
            "source_id": "SRC4419_01_434_formal",
            "path": FORMAL_434,
            "needle": "NoSourceOnlySpeciesSlot",
            "role": "current local-GR/Newton source-coupling bottleneck.",
        },
        {
            "source_id": "SRC4419_02_2772_grammar",
            "path": POST_2772,
            "needle": "no-source-only-slot parent grammar theorem",
            "role": "prior no-source-only species grammar theorem attempt.",
        },
        {
            "source_id": "SRC4419_03_2773_action_scale",
            "path": POST_2773,
            "needle": "common action-scale normalization",
            "role": "action-scale/measure owner obstruction for w_A.",
        },
        {
            "source_id": "SRC4419_04_2881_minimal_coupling",
            "path": POST_2881,
            "needle": "MCA2526 gives S_A[psi_A;q(Phi),theta_A]",
            "role": "least-scrutiny minimal matter-coupling contract.",
        },
        {
            "source_id": "SRC4419_05_4376_source_shadow",
            "path": POST_4376,
            "needle": "Noether limitation",
            "role": "Noether exchange does not kill source-only functionals.",
        },
        {
            "source_id": "SRC4419_06_4377_profile",
            "path": POST_4377,
            "needle": "source-density object exists except Hilbert",
            "role": "typed Hilbert-only density theorem and distributional profile gate.",
        },
        {
            "source_id": "SRC4419_07_3573_topological",
            "path": POST_3573,
            "needle": "J_M^top exists and equals Pi_M J_H on shell",
            "role": "topological mass-current route to d(Pi_M J_H)=0.",
        },
        {
            "source_id": "SRC4419_08_1013_warning",
            "path": POST_1013,
            "needle": "A closed topological mass current is insufficient unless it equals Pi_M J_H",
            "role": "closed-wrong-current guard and R_eq residual.",
        },
        {
            "source_id": "SRC4419_09_2900_same_object",
            "path": POST_2900,
            "needle": "Pi_M J_H = J_M_top + dB_zero",
            "role": "source-worldtube/current-complex same-object gate.",
        },
        {
            "source_id": "SRC4419_10_gate",
            "path": GATE_PATH,
            "needle": "def evaluate_source_slot_row",
            "role": "4419 source-slot/topological current gate.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "NST4419_0_source_slot_exclusion_theorem",
            "claim": "NoSourceOnlySpeciesSlot is exact if the parent ordinary matter action has one typed Hilbert-source owner.",
            "derivation": "Let S_m be a single parent functional of q(Phi), ordinary matter fields and measured representation data, with one universal action measure. Variation before readout gives T_H by the Hilbert derivative. A species scalar w_A that changes only T_source and no spectrum, charge/current, representation, geometry or gauge datum is not an admissible parent argument; a common w is calibration only. Therefore relative Delta_w_AB vanish.",
            "consequence": "This would close the common-mode source-coupling branch without hiding relative weights inside measured G.",
            "status": "EXACT_CONDITIONAL_ACTION_MEASURE_OWNER_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NST4419_1_action_scale_obstruction",
            "claim": "The remaining w_A countermodel is not classical dynamics; it is action-scale/Hilbert-stress ownership.",
            "derivation": "Multiplying a matter-sector action by w_A can leave isolated classical equations formally similar while rescaling Hilbert stress, statistical/path-integral weight and active gravitational source. Field normalization or Noether exchange cannot remove this unless the parent proves one universal action-scale and species-blind measure/coframe descent.",
            "consequence": "The proof target is now the universal action-measure/source-current owner, not another fitted local-test parameter.",
            "status": "COUNTERMODEL_LOCALIZED_TO_ACTION_MEASURE_OWNER",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "TMC4419_0_topological_mass_current_theorem",
            "claim": "A closed topological mass current closes flux only if it is the same Hilbert mass current.",
            "derivation": "If a parent-owned current J_M^top is closed on shell and Pi_M J_H = J_M^top + dB_zero + R_eq with R_eq=0 distributionally and zero boundary-improvement flux, then d(Pi_M J_H)=0 on the compact local exterior. If R_eq or boundary flux survives, the closed current may be the wrong object.",
            "consequence": "The topological route is not dead, but equality to Pi_M J_H is the theorem, not total charge or closure by itself.",
            "status": "EXACT_CONDITIONAL_REQ_AND_BOUNDARY_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "JNT4419_0_joint_source_newton_gate",
            "claim": "First-order Newton source coupling closes if both source-slot and same-current gates close.",
            "derivation": "NoSourceOnlySpeciesSlot kills non-common source weights; same-current topology gives d(Pi_M J_H)=0; H_ref/M_H and constant G_ref then inherit the 4418 Poisson/Gauss bridge without using observed orbital GM as source input.",
            "consequence": "This is the cleanest local-GR/Newton route currently available, but it remains nonclaim until the parent action contract is signed.",
            "status": "JOINT_THEOREM_WRITTEN_PARENT_SIGNATURE_OPEN",
            "valid_for_claim": False,
        },
    ]


def source_slot_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SSG4419_0_object_language_route",
            "branch": "typed_Hilbert_only_matter_source",
            "single_parent_matter_functional": True,
            "object_language_typed": True,
            "universal_action_scale_owner": False,
            "variation_before_readout": True,
            "hilbert_current_owner": True,
            "no_source_only_scalar_target": True,
            "species_blind_measure_coframe": False,
            "measured_parameters_only": True,
            "common_mode_calibration_guard": True,
            "no_hidden_hom": True,
            "no_post_readout_selector": True,
            "source_path": str(POST_2773),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Object-language exclusion is sharp; universal action-scale and measure/coframe owner remain unsigned.",
        },
        {
            "row_id": "SSG4419_1_MCA2526_contract",
            "branch": "least_scrutiny_minimal_coupling_contract",
            "single_parent_matter_functional": True,
            "object_language_typed": True,
            "universal_action_scale_owner": False,
            "variation_before_readout": True,
            "hilbert_current_owner": True,
            "no_source_only_scalar_target": True,
            "species_blind_measure_coframe": False,
            "measured_parameters_only": True,
            "common_mode_calibration_guard": True,
            "no_hidden_hom": True,
            "no_post_readout_selector": True,
            "source_path": str(POST_2881),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "MCA2526 is the right contract but still not derived from MTS core.",
        },
        {
            "row_id": "SSG4419_2_future_parent_contract",
            "branch": "future_parent_action_measure_owner",
            "single_parent_matter_functional": True,
            "object_language_typed": True,
            "universal_action_scale_owner": True,
            "variation_before_readout": True,
            "hilbert_current_owner": True,
            "no_source_only_scalar_target": True,
            "species_blind_measure_coframe": True,
            "measured_parameters_only": True,
            "common_mode_calibration_guard": True,
            "no_hidden_hom": True,
            "no_post_readout_selector": True,
            "source_path": str(POST_2772),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact contract row: if the parent signs these clauses, NoSourceOnlySpeciesSlot and Delta_w_AB=0 follow. Nonclaim because input_valid=false.",
        },
    ]


def topological_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "TCG4419_0_closed_wrong_current_guard",
            "branch": "closed_topological_current_without_Hilbert_equality",
            "parent_owned_current": True,
            "same_hilbert_functional": False,
            "stationary_tau_generator": True,
            "PiM_chain_map": False,
            "on_shell_noether_constraint": True,
            "topological_current_closed": True,
            "distributional_R_eq_zero": False,
            "boundary_improvement_zero_flux": False,
            "fixed_worldtube_support": False,
            "common_Mref_lock": False,
            "no_measured_GM_backfill": True,
            "source_path": str(POST_1013),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Closure alone is not enough; this row encodes the closed-wrong-current failure mode.",
        },
        {
            "row_id": "TCG4419_1_same_current_future_contract",
            "branch": "future_Jtop_equals_PiM_JH_contract",
            "parent_owned_current": True,
            "same_hilbert_functional": True,
            "stationary_tau_generator": True,
            "PiM_chain_map": True,
            "on_shell_noether_constraint": True,
            "topological_current_closed": True,
            "distributional_R_eq_zero": True,
            "boundary_improvement_zero_flux": True,
            "fixed_worldtube_support": True,
            "common_Mref_lock": True,
            "no_measured_GM_backfill": True,
            "source_path": str(POST_2900),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact contract row: if parent-owned, d(Pi_M J_H)=0 follows. Nonclaim because input_valid=false.",
        },
        {
            "row_id": "TCG4419_2_profile_moment_gate",
            "branch": "topological_Hilbert_distributional_profile_equality",
            "parent_owned_current": False,
            "same_hilbert_functional": True,
            "stationary_tau_generator": True,
            "PiM_chain_map": True,
            "on_shell_noether_constraint": False,
            "topological_current_closed": False,
            "distributional_R_eq_zero": False,
            "boundary_improvement_zero_flux": True,
            "fixed_worldtube_support": True,
            "common_Mref_lock": False,
            "no_measured_GM_backfill": True,
            "source_path": str(POST_4377),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Same total mass is only monopole; distributional/moment equality remains the live proof or bound row.",
        },
    ]


def parent_contract_rows() -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "PAC4419_0_single_action_measure",
            "clause": "One universal parent action measure and hbar/action-scale owner applies to all ordinary matter sectors.",
            "closes": "source-only w_A action multipliers",
            "current_status": "OPEN_PARENT_SIGNATURE",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC4419_1_typed_source_object",
            "clause": "Ordinary source object is the Hilbert derivative of S_m[q(Phi), Psi, theta_meas] before readout.",
            "closes": "non-Hilbert/source-shadow current slots",
            "current_status": "CONDITIONAL_PACKET_SUPPORTED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC4419_2_species_blind_measure_coframe",
            "clause": "Measure, coframe, boundary and connection descent are species blind in the local transition branch.",
            "closes": "hidden measure/coframe spurions mimicking source weights",
            "current_status": "OPEN_PARENT_SIGNATURE",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC4419_3_same_current_topology",
            "clause": "Parent topological/Hamiltonian mass current is the same distributional object as Pi_M J_H up to zero-flux exact improvement.",
            "closes": "closed-wrong-current and R_eq profile residual",
            "current_status": "OPEN_R_EQ_AND_BOUNDARY_FLUX",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC4419_4_no_GM_backfill",
            "clause": "M_H, H_ref and G_ref are fixed before orbital/PPN readout; observed GM is only a comparator.",
            "closes": "circular Newton calibration",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows_out: Sequence[Mapping[str, str]],
    topo_rows_out: Sequence[Mapping[str, str]],
) -> List[Dict[str, object]]:
    source_by_id = {row["row_id"]: row for row in source_rows_out}
    topo_by_id = {row["row_id"]: row for row in topo_rows_out}
    no_claim = not any(row.get("valid_for_claim") == "True" for row in source_rows_out) and not any(
        row.get("valid_for_claim") == "True" for row in topo_rows_out
    )
    return [
        {
            "gate_id": "CG4419_0_source_slot_theorem_sharp",
            "claim": "NoSourceOnlySpeciesSlot theorem is mathematically exact once action-measure owner is signed",
            "passed": True,
            "valid_for_claim": False,
            "detail": "w_A is localized to an inadmissible source-only action-scale scalar, not ordinary dynamics.",
        },
        {
            "gate_id": "CG4419_1_action_measure_owner",
            "claim": "universal action-scale/measure owner is parent-signed",
            "passed": False,
            "valid_for_claim": False,
            "detail": "2773 action-scale owner remains the open parent signature.",
        },
        {
            "gate_id": "CG4419_2_future_source_contract",
            "claim": "future NoSourceOnlySpeciesSlot contract row is executable",
            "passed": source_by_id["SSG4419_2_future_parent_contract"].get("current_status")
            == "NO_SOURCE_ONLY_SPECIES_SLOT_CONTRACT_READY_NONCLAIM",
            "valid_for_claim": False,
            "detail": "contract row closes internally but remains nonclaim through input_valid=false.",
        },
        {
            "gate_id": "CG4419_3_closed_wrong_current_guard",
            "claim": "closed topological current alone is not promoted",
            "passed": topo_by_id["TCG4419_0_closed_wrong_current_guard"].get("current_status")
            == "CLOSED_TOPOLOGICAL_CURRENT_READY_EQUALITY_OPEN",
            "valid_for_claim": False,
            "detail": "R_eq, boundary flux, worldtube and M_ref equality remain required.",
        },
        {
            "gate_id": "CG4419_4_future_topological_contract",
            "claim": "future same-current topological contract row is executable",
            "passed": topo_by_id["TCG4419_1_same_current_future_contract"].get("current_status")
            == "TOPOLOGICAL_MASS_CURRENT_CONTRACT_READY_NONCLAIM",
            "valid_for_claim": False,
            "detail": "contract row would close d(Pi_M J_H)=0 but is not parent-signed.",
        },
        {
            "gate_id": "CG4419_5_joint_Newton_source_leg",
            "claim": "Newton/local-GR source leg is public",
            "passed": False,
            "valid_for_claim": False,
            "detail": "requires both action-measure owner and same-current R_eq/boundary/worldtube closure.",
        },
        {
            "gate_id": "CG4419_6_no_claim_outputs",
            "claim": "4419 generated no claim-ready row",
            "passed": no_claim,
            "valid_for_claim": False,
            "detail": "this is a parent-action contract/derivation checkpoint, not a public local-GR pass.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4419_0",
            "decision": DECISION,
            "summary": "4419 does take the leap: the source-coupling problem is compressed to an explicit parent-action contract. NoSourceOnlySpeciesSlot follows if ordinary matter has one typed Hilbert-source action with one universal action-scale/measure owner; d(Pi_M J_H)=0 follows if the parent topological/Hamiltonian mass current is distributionally the same object as Pi_M J_H up to zero-flux improvement. Current MTS has not signed the action-measure owner or R_eq/boundary/worldtube equality, so no local-GR/Newton claim fires.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4419_0_best_result",
            "status": "PARENT_ACTION_CONTRACT_EXACT",
            "detail": "The route is no longer vague coupling talk: it is PAC4419 action-measure owner plus same-current topology.",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT4419_1_remaining_derivation",
            "status": "ACTION_MEASURE_OWNER_AND_REQ_ZERO_OPEN",
            "detail": "Need to derive one universal action-scale/measure source owner and R_eq=0 with zero boundary flux/worldtube lock.",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT4419_2_bound_fallback",
            "status": "FINITE_ROWS_IF_PARENT_CONTRACT_FAILS",
            "detail": "If proof fails, fill Delta_w/tau_WEP plus R_eq/moment/source-profile/material response rows rather than fitting GM.",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4419_0",
            "target": NEXT_TARGET,
            "objective": "Prove the universal action-measure/current owner that makes S_m one Hilbert-source object and simultaneously attack R_eq=0/boundary flux for J_M^top=Pi_M J_H; otherwise instantiate the first finite Delta_w/tau_WEP plus R_eq moment-bound rows.",
            "derive_first": "derive one parent action-scale/measure owner from the MTS quotient/object language, then use same functional variation/Iyer-Wald/Hamiltonian identity to lock the topological current to the Hilbert current distributionally.",
            "fallback": "fill source-backed nonclaim rows for Delta_w_AB, tau_WEP, R_eq compact-test/multipole moments, B_zero_flux and source-worldtube/material response.",
            "avoid": "declaring minimal coupling by taste; using Noether closure alone; using total mass as profile equality; using observed GM as source input.",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    source_out: Sequence[Mapping[str, str]],
    topo_out: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 435 PPC4161 transition: NoSourceOnlySpeciesSlot or topological mass-current origin

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4419 is a genuine narrowing of the coupling problem:

- `NoSourceOnlySpeciesSlot` is now an exact parent-action theorem if MTS signs one universal action-scale/measure owner for ordinary matter.
- The surviving `w_A` countermodel is not vague: it is specifically a source-only action-scale/Hilbert-stress scalar.
- A closed topological current is not enough; the required theorem is `J_M^top = Pi_M J_H - dB_zero` distributionally with zero boundary flux and fixed worldtube.
- The two proof routes meet in one parent contract: one Hilbert-source action owner plus same-current topology.
- No Newton/local-GR claim fires; the next move is the action-measure/current owner proof or finite `Delta_w/tau_WEP/R_eq` rows.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Source-Slot Theorem Gate

{table(source_out)}

## Topological Current Gate

{table(topo_out)}

## Parent Action Contract

{table(parent_contract_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4419 - transition NoSourceOnlySpeciesSlot or topological mass-current origin

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Turned the loose coupling problem into the explicit `PAC4419` parent-action contract.
- Proved the conditional no-source-slot route: typed Hilbert matter source plus universal action measure kills relative `w_A`.
- Proved the conditional topological route: closed `J_M^top` only helps when distributionally equal to `Pi_M J_H` up to zero-flux improvement.
- Kept all local-GR/Newton/WEP/PPN claims false until the parent signs the action-measure owner and `R_eq`/boundary/worldtube clauses.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        sep = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + sep + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = rows[0].keys() if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "4419 compresses the calibrated source-coupling problem into an exact parent-action contract. NoSourceOnlySpeciesSlot follows from one typed Hilbert-source ordinary matter action plus universal action-scale/measure owner; d(Pi_M J_H)=0 follows from a parent topological/Hamiltonian mass current distributionally equal to Pi_M J_H up to zero-flux improvement. The branch remains nonclaim because action-measure ownership and R_eq/boundary/worldtube equality are not parent-signed.",
            "current_evidence": "4419 source register, derivation rows, source-slot output, topological-current output, parent-action contract, claim gates, decision, status, next target and validation CSV.",
            "status": "source_coupling_reduced_to_action_measure_and_same_current_contract_nonclaim",
            "next_test": "Derive universal action-measure/current owner and R_eq=0 boundary/worldtube lock, or fill Delta_w/tau_WEP/R_eq finite rows.",
            "key_risk": "Treating minimal coupling as taste, topological closure as equality, total mass as profile equality, or fitted GM as source calibration.",
            "sector": "local_gr",
            "evidence": "4419 source register, derivation rows, source-slot output, topological-current output, parent-action contract, claim gates, decision, status, next target and validation CSV.",
            "next_action": "Derive universal action-measure/current owner and R_eq=0 boundary/worldtube lock, or fill Delta_w/tau_WEP/R_eq finite rows.",
            "risk": "Treating minimal coupling as taste, topological closure as equality, total mass as profile equality, or fitted GM as source calibration.",
        }
    )
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4419 local spine update: coupling becomes a parent-action contract

4419 compresses the live source-coupling obstruction into two exact but unsigned certificates. First, `NoSourceOnlySpeciesSlot` follows if ordinary matter is one typed Hilbert-source action with one universal action-scale/measure owner; this kills relative `w_A` rather than burying it in measured `G`. Second, `d(Pi_M J_H)=0` follows if the parent topological/Hamiltonian mass current is distributionally the same current as `Pi_M J_H` up to zero-flux improvement. Thus the local Newton route is no longer foggy coupling language: it is `PAC4419` plus `R_eq=0`. The branch remains nonclaim until those parent signatures or finite `Delta_w/tau_WEP/R_eq` bounds exist.
"""
    packet_section = f"""## 4419 packet update: source coupling contract

`{PACKET_MARKER}`

Private packet result: the source-coupling leg has a clean contract. If the parent action owns a single Hilbert matter source, a universal action measure, species-blind measure/coframe descent, and a same-current topological/Hamiltonian representative, then the 4418 Poisson/Gauss/Newton bridge can inherit calibrated source coupling without orbital-GM backfill. Current packet status is nonclaim: action-scale owner and `R_eq`/boundary/worldtube equality remain open.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    source_out = {row["row_id"]: row for row in rows_from(SOURCE_SLOT_OUTPUT)}
    topo_out = {row["row_id"]: row for row in rows_from(TOPO_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in source_out.values()) and not any(
        row.get("valid_for_claim") == "True" for row in topo_out.values()
    )
    checks = [
        (
            "VAL4419_0_sources_exist",
            all(row["path_exists"] == "True" for row in sources),
            "every cited source path exists",
        ),
        (
            "VAL4419_1_needles_found",
            all(row["needle_found"] == "True" for row in sources),
            "every cited source needle is present",
        ),
        (
            "VAL4419_2_object_language_action_owner_open",
            source_out["SSG4419_0_object_language_route"].get("current_status")
            == "SOURCE_SLOT_OBJECT_LANGUAGE_READY_ACTION_OWNER_OPEN",
            "typed object-language route is sharp but action owner remains open",
        ),
        (
            "VAL4419_3_future_source_contract",
            source_out["SSG4419_2_future_parent_contract"].get("current_status")
            == "NO_SOURCE_ONLY_SPECIES_SLOT_CONTRACT_READY_NONCLAIM",
            "future no-source-only-slot contract is executable nonclaim",
        ),
        (
            "VAL4419_4_closed_wrong_current_guard",
            topo_out["TCG4419_0_closed_wrong_current_guard"].get("current_status")
            == "CLOSED_TOPOLOGICAL_CURRENT_READY_EQUALITY_OPEN",
            "closed topological current alone is blocked by equality clauses",
        ),
        (
            "VAL4419_5_future_topological_contract",
            topo_out["TCG4419_1_same_current_future_contract"].get("current_status")
            == "TOPOLOGICAL_MASS_CURRENT_CONTRACT_READY_NONCLAIM",
            "future same-current topological contract is executable nonclaim",
        ),
        ("VAL4419_6_no_claim_outputs", no_claims, "no generated theorem row is claim-ready"),
        (
            "VAL4419_7_claim_gates",
            any(row["gate_id"] == "CG4419_6_no_claim_outputs" and row["passed"] == "True" for row in gates),
            "claim gates explicitly block public source-coupling claim",
        ),
        ("VAL4419_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-260"),
        ("VAL4419_9_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4419_10_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4419_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4419_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4419_13_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4419_14_parent_contract", PARENT_CONTRACT.exists() and "PAC4419_0_single_action_measure" in text(PARENT_CONTRACT), "parent action contract exists"),
        ("VAL4419_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
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
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SOURCE_SLOT_INPUT, source_slot_input_rows())
    write_csv(TOPO_INPUT, topological_input_rows())
    write_csv(SOURCE_SLOT_OUTPUT, evaluate_source_slot_rows(SOURCE_SLOT_INPUT))
    write_csv(TOPO_OUTPUT, evaluate_topological_current_rows(TOPO_INPUT))
    source_output = rows_from(SOURCE_SLOT_OUTPUT)
    topo_output = rows_from(TOPO_OUTPUT)
    write_csv(PARENT_CONTRACT, parent_contract_rows())
    claim_gates = claim_gate_rows(source_output, topo_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), source_output, topo_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(
        VALIDATION_PATH,
        validation_rows(
            {
                "formal": FORMAL_PATH,
                "post": DOC_PATH,
                "next": NEXT_CSV,
            }
        ),
    )


if __name__ == "__main__":
    main()
