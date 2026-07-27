from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from Pleak_first_two_component_gate import evaluate_bound_rows, evaluate_zero_rows, read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4405"
CLAIM_ID = "L-246"
MARKER = "PPC4161_TRANSITION_CGAMMA_PLEAK_FIRST_TWO_COMPONENTS_OR_PROFILE_BOUND_4405"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_CGAMMA_PLEAK_FIRST_TWO_COMPONENTS_OR_PROFILE_BOUND_4405"
DECISION = "FIRST_TWO_PLEAK_COMPONENTS_ZERO_ON_COMPACT_PRIVATE_BRANCH_OPEN_RAW_SOURCE_HAIR_NONCLAIM"
NEXT_TARGET = "4406-Y5-R2FR-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"

FORMAL_PATH = FORMAL / "421-PPC4161-transition-cGamma-Pleak-first-two-components-or-profile-bound.md"
DOC_PATH = POST / "4405-Y5-R2FR-transition-cGamma-transition-shell-Pleak-first-two-components-or-profile-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4405_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

GATE_PATH = SCRIPT_DIR / "Pleak_first_two_component_gate.py"
ZERO_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4405_PLEAK_FIRST_TWO_ZERO_INPUT.csv"
ZERO_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4405_PLEAK_FIRST_TWO_ZERO_OUTPUT.csv"
BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4405_PLEAK_FIRST_TWO_BOUND_INPUT.csv"
BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4405_PLEAK_FIRST_TWO_BOUND_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4404 = SOURCE_DIR / "P8_Y5_R2FR_4404_NEXT_TARGET.csv"
FORMAL_420 = FORMAL / "420-PPC4161-transition-cGamma-first-live-profile-row-or-parent-memory-nohair-proof.md"
FORMAL_355 = FORMAL / "355-PPC4161-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md"
FORMAL_356 = FORMAL / "356-PPC4161-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md"
FORMAL_358 = FORMAL / "358-PPC4161-KL-generator-for-KGamma-and-CRI-CDeltaKdiv-zero-branch.md"
FORMAL_359 = FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md"
FORMAL_368 = FORMAL / "368-PPC4161-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md"
FORMAL_369 = FORMAL / "369-PPC4161-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md"
FORMAL_370 = FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4405_00_4404_next": (NEXT_4404, "P_nonHilbert_action_domain", "4404 selected the first two transition-shell P_leak components."),
    "SRC4405_01_4404_formal": (FORMAL_420, "transition-shell P_leak components", "cGamma transition shells reduce to P_leak rather than generic cGamma smallness."),
    "SRC4405_02_4339_components": (FORMAL_355, "P_nonHilbert_action_domain q_tr", "4339 names and reduces the first two P_leak channels."),
    "SRC4405_03_4340_worldtube": (FORMAL_356, "P_off_worldtube_readout_order=0", "4340 proves the full-domain-before-readout zero branch."),
    "SRC4405_04_4342_KGamma": (FORMAL_358, "C_RI^flat=0", "4342 constructs the fixed-flat KGamma right-inverse route."),
    "SRC4405_05_4343_owner": (FORMAL_359, "S_RI = int_U", "4343 writes the concrete KGamma owner action candidate."),
    "SRC4405_06_4352_tail": (FORMAL_368, "B_RI = 0", "4352 kills RI boundary/incoming legs on the compact clean branch."),
    "SRC4405_07_4353_clean": (FORMAL_369, "epsilon_owner_tail_Kperp=0", "4353 deletes the owner-tail/Kperp channel from the private clean vector."),
    "SRC4405_08_4354_source": (FORMAL_370, "D_A ln kappa_eff = 0", "4354 identifies source charge and calibrated coupling as the next gate."),
    "SRC4405_09_gate": (GATE_PATH, "def evaluate_zero_rows", "Executable first-two-Pleak zero/bound gate."),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    if not path.exists():
        return False, -1
    for index, line in enumerate(text(path).splitlines(), 1):
        if needle in line:
            return True, index
    return False, -1


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line = locate(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": found,
            "line_number": line,
            "role": role,
            "valid_for_claim": False,
        })
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "PL4405_0_first_component_clean_branch",
            "object": "P_nonHilbert_action_domain q_tr",
            "statement": "The 4339 vertical-response problem is routed through the 4342 KGamma right-inverse, the 4343 multiplier owner, and the 4353 clean owner-tail/Kperp deletion.",
            "result": "On the compact private clean branch, this first P_leak component is zero as an owner-tail/Kperp channel; public authority remains false.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PL4405_1_second_component_clean_branch",
            "object": "P_off_worldtube_readout_order q_tr",
            "statement": "4340 gives N_inner=0 when the source is varied on the smooth full Hilbert domain before exterior restriction/readout.",
            "result": "On the same-worldtube full-domain-before-readout branch, the off-worldtube readout-order component is zero; exterior-first branches retain the trace-defect bound.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PL4405_2_first_two_bound_vector",
            "object": "first two P_leak fallback",
            "statement": "epsilon_first2 <= |Pi|(|epsilon_owner_tail_Kperp| + |N_inner| + |epsilon_tr_hair|), with no cancellation credit.",
            "result": "If either clean branch opens, the runner demands real owner-tail, trace-defect and source-hair rows before any PPN/R10/clock/orbital scoring.",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PL4405_3_next_gate",
            "object": "remaining local-GR route",
            "statement": "After the first two P_leak channels are compact-private-zeroed, 4353/4354 make source charge, source-blind calibrated coupling, transition hair and empirical projection constants the next high-leverage gates.",
            "result": "4406 should import or rebuild the epsilon_Gsrc runner in the current 440x chain.",
            "valid_for_claim": False,
        },
    ]


def zero_inputs() -> List[Dict[str, object]]:
    base_false = {
        "parent_selector_private": False,
        "kgamma_owner_constructed": False,
        "adjoint_gap_positive": False,
        "boundary_silent": False,
        "no_incoming_RI": False,
        "kperp_clean_sector": False,
        "same_worldtube": False,
        "full_domain_before_readout": False,
        "no_inner_boundary": False,
        "trace_defect_zero": False,
        "public_authority": False,
        "input_valid_for_claim": False,
    }
    rows = []
    row = dict(base_false)
    row.update({
        "component_id": "PZ4405_0_PnonHilbert_compact_private",
        "component": "P_nonHilbert_action_domain",
        "branch": "compact_private_clean_owner_tail",
        "source_path": str(FORMAL_369),
        "parent_selector_private": True,
        "kgamma_owner_constructed": True,
        "adjoint_gap_positive": True,
        "boundary_silent": True,
        "no_incoming_RI": True,
        "kperp_clean_sector": True,
    })
    rows.append(row)
    row = dict(base_false)
    row.update({
        "component_id": "PZ4405_1_offworldtube_full_domain",
        "component": "P_off_worldtube_readout_order",
        "branch": "same_worldtube_full_domain_before_readout",
        "source_path": str(FORMAL_356),
        "parent_selector_private": True,
        "same_worldtube": True,
        "full_domain_before_readout": True,
        "no_inner_boundary": True,
        "trace_defect_zero": True,
    })
    rows.append(row)
    row = dict(base_false)
    row.update({
        "component_id": "PZ4405_2_PnonHilbert_raw_open",
        "component": "P_nonHilbert_action_domain",
        "branch": "raw_transition_open_or_public",
        "source_path": str(FORMAL_355),
        "kgamma_owner_constructed": True,
    })
    rows.append(row)
    row = dict(base_false)
    row.update({
        "component_id": "PZ4405_3_offworldtube_exterior_first",
        "component": "P_off_worldtube_readout_order",
        "branch": "exterior_first_or_worldtube_excision",
        "source_path": str(FORMAL_355),
        "same_worldtube": True,
    })
    rows.append(row)
    return rows


def bound_inputs() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "PB4405_0_missing_live_raw_bound",
            "branch": "raw_transition_real_row_required",
            "arena": "PPN_gamma",
            "source_path": str(FORMAL_355),
            "owner_tail_bound": "MISSING_OWNER_TAIL_ROW",
            "trace_defect_bound": "MISSING_TRACE_DEFECT_ROW",
            "source_hair_bound": "MISSING_SOURCE_HAIR_ROW",
            "projection_factor": "MISSING_PI_A",
            "arena_bound": "0.0002739826487147268",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "PB4405_1_compact_private_zero_smoke",
            "branch": "compact_private_clean_smoke",
            "arena": "PPN_gamma",
            "source_path": str(FORMAL_369),
            "owner_tail_bound": "0",
            "trace_defect_bound": "0",
            "source_hair_bound": "0",
            "projection_factor": "1",
            "arena_bound": "0.0002739826487147268",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "PB4405_2_small_nonclaim_bound_smoke",
            "branch": "finite_bound_schema_smoke",
            "arena": "clock_delta_z",
            "source_path": str(GATE_PATH),
            "owner_tail_bound": "1e-18",
            "trace_defect_bound": "1e-18",
            "source_hair_bound": "1e-18",
            "projection_factor": "1",
            "arena_bound": "1e-16",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "PB4405_3_source_hair_fail_smoke",
            "branch": "finite_bound_failure_control",
            "arena": "clock_delta_z",
            "source_path": str(GATE_PATH),
            "owner_tail_bound": "0",
            "trace_defect_bound": "0",
            "source_hair_bound": "1e-14",
            "projection_factor": "1",
            "arena_bound": "1e-16",
            "input_valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "PG4405_0_first_two_private_zero", "gate": "first_two_Pleak_private_branch", "claim_allowed": False, "reason": "both first components can be zero only inside private compact/same-worldtube branches."},
        {"gate_id": "PG4405_1_raw_transition_bound", "gate": "raw_transition_or_public_branch", "claim_allowed": False, "reason": "raw/open branches still need real owner-tail, trace-defect and source-hair bound rows."},
        {"gate_id": "PG4405_2_source_charge_coupling", "gate": "Htau_MHref_kappa_eff", "claim_allowed": False, "reason": "after first-two Pleak cleanup, source charge and source-blind coupling remain decisive."},
        {"gate_id": "PG4405_3_local_GR_Newton", "gate": "local_GR_Newton_PPN_R10", "claim_allowed": False, "reason": "remaining nonowner residuals, projections and empirical rows are not closed."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "decision_id": "DEC4405_0",
        "decision": DECISION,
        "summary": "4405 reconciles the 4404 cGamma/Pleak handoff with the 4340-4353 proof ladder. The first two P_leak components are zero on the compact private clean/same-worldtube branches, but raw/public transition shells still require source-backed no-cancellation bound rows. The next current-chain target is source charge/coupling hair, not another generic cGamma loop.",
        "claim_allowed": False,
        "valid_for_claim": False,
    }]


def next_target_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4405_0",
        "target": NEXT_TARGET,
        "question": "Can the 4354 source-charge/coupling fork be imported into the current 440x chain as an epsilon_Gsrc runner with real theorem-zero or finite rows?",
        "preferred_route": "derive same-worldtube H_tau/M_Hdress ownership plus D_A ln kappa_eff=0 on the same private local branch.",
        "fallback_route": "build finite no-cancellation epsilon_Gsrc rows for source charge, reference, tau/frame/surface, boundary flux, PiH glue, species/frame/range/readout drift and projection constants.",
        "avoid": "reopening cGamma or Pleak first-two channels after they have been branch-classified.",
        "valid_for_claim": False,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4405_0", "item": "P_nonHilbert_action_domain", "status": "PRIVATE_CLEAN_ZERO_BRANCH_IMPORTED", "notes": "4342-4353 route deletes owner-tail/Kperp in compact private branch."},
        {"status_id": "STAT4405_1", "item": "P_off_worldtube_readout_order", "status": "FULL_DOMAIN_READOUT_ZERO_BRANCH_IMPORTED", "notes": "exterior-first branches retain trace-defect finite rows."},
        {"status_id": "STAT4405_2", "item": "raw/public transition", "status": "FINITE_BOUND_ROWS_REQUIRED", "notes": "owner-tail, trace-defect and source-hair rows remain mandatory outside the clean branch."},
        {"status_id": "STAT4405_3", "item": "next route", "status": "SOURCE_CHARGE_COUPLING_GATE", "notes": NEXT_TARGET},
    ]


def markdown_table(rows: List[Dict[str, object]]) -> str:
    if not rows:
        return ""
    keys = list(rows[0].keys())
    lines = ["| " + " | ".join(keys) + " |", "| " + " | ".join("---" for _ in keys) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in keys) + " |")
    return "\n".join(lines)


def write_formal_doc(sources, derivations, zero_output, bound_output, gates, decisions, next_targets) -> None:
    FORMAL_PATH.write_text(
        f"""# 421 PPC4161 transition cGamma P_leak first two components or profile bound

Marker: `{MARKER}`

Generated UTC: `{STAMP}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, Maxwell/EM closure, calibrated `G_N`, R10, PPN, clock, orbital, or WEP safety.

## Result

4405 imports the existing 4340-4353 proof ladder into the current 4404 `c_Gamma -> P_leak` handoff.

The useful result is:

```text
P_nonHilbert_action_domain q_tr = 0
```

on the compact private clean owner-tail branch where the `K_Gamma` right-inverse owner, adjoint gap, boundary silence, no-incoming RI data, and private `Kperp` routing all close.

The second useful result is:

```text
P_off_worldtube_readout_order q_tr = 0
```

on the same-worldtube full-domain-before-readout branch. Exterior-first or excised-worldtube branches still keep:

```text
N_inner <= ||mu_tr|| + ||B_src^A||
```

or its no-concentration/lambda reduction.

So the first two `P_leak` channels are no longer generic open fog. They are branch-classified:

```text
clean compact private branch: first two components zero;
raw/open/public branch: owner-tail + trace-defect + source-hair rows required.
```

The next high-leverage work is therefore the 4354 source-charge/coupling fork, imported into the current 440x chain.

## Source Register

{markdown_table(sources)}

## Derivation Rows

{markdown_table(derivations)}

## Zero Gate Output

{markdown_table(zero_output)}

## Bound Gate Output

{markdown_table(bound_output)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def write_post_doc(decisions, next_targets) -> None:
    DOC_PATH.write_text(
        f"""# 4405 transition cGamma P_leak first two components or profile bound

Marker: `{MARKER}`

## Private outcome

4405 stops the current route from circling generic `c_Gamma`.

It imports the older proof ladder:

- 4339 reduced the first two `P_leak` channels to `D_v q_tr` and worldtube trace defect.
- 4340-4343 constructed the `K_Gamma` right-inverse/owner route.
- 4350-4353 killed the RI/Kperp owner-tail on the compact private clean branch.
- 4354 says the next live gate is source charge/coupling, not generic coupling vibes.

## Decision

{markdown_table(decisions)}

## Next

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def update_spine() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## 4405 local spine update: first two P_leak components branch-classified

Marker: `{MARKER}`

Spine update: the 4404 `c_Gamma` transition-shell problem now imports the 4340-4353 ladder. `P_nonHilbert_action_domain q_tr` is zero on the compact private clean owner-tail/Kperp branch, and `P_off_worldtube_readout_order q_tr` is zero on the same-worldtube full-domain-before-readout branch. Raw/open/public transition shells still require no-cancellation owner-tail, trace-defect and source-hair rows. The next current-chain target is source charge/coupling through an `epsilon_Gsrc` gate.
""",
    )


def update_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4405 packet update: first two P_leak components

Marker: `{PACKET_MARKER}`

Packet update: 4405 reconciles the `c_Gamma -> P_leak` handoff with the earlier KGamma/Kperp/source-domain work. The first two P_leak components are zero only on the compact private clean/same-worldtube branches; open branches retain explicit finite bound rows. The packet now routes the local-GR/Newton pressure to source charge and source-blind calibrated coupling.
""",
    )


def update_claims() -> None:
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4405 imports the 4340-4353 P_leak proof ladder into the current cGamma route. The first two transition-shell components are branch-classified: P_nonHilbert_action_domain is zero on the compact private clean owner-tail/Kperp branch, and P_off_worldtube_readout_order is zero on the same-worldtube full-domain-before-readout branch. Raw/open/public transition shells still require source-backed no-cancellation owner-tail, trace-defect and source-hair bound rows. No local-GR/Newton/PPN/R10/clock/orbital claim fires.",'
        f'"4405 source register, derivation rows, first-two P_leak zero gate, finite bound gate, claim gates, decision, status, next target and validation CSV.",'
        f'first_two_Pleak_components_private_branch_classified_nonclaim,'
        f'Import/build the 4354 source-charge/coupling epsilon_Gsrc runner in the current 440x chain.,'
        f'"Treating private branch zero as public local GR, using full-domain readout zero in exterior-first solves, or reopening generic cGamma instead of source charge/coupling."\n'
    )
    if f"\n{CLAIM_ID}," not in text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(row)


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, object]]:
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4405_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4405_DERIVATIONS.csv")
    zero_output = read_csv(ZERO_OUTPUT)
    bound_output = read_csv(BOUND_OUTPUT)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4405_CLAIM_GATES.csv")

    rows: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail})

    add("VAL4405_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4405_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add("VAL4405_2_derivations_written", len(derivations) >= 4, "derivation rows written")
    add("VAL4405_3_PnonHilbert_private_zero", any(row["component_id"] == "PZ4405_0_PnonHilbert_compact_private" and row["private_zero"] == "True" for row in zero_output), "P_nonHilbert private zero imported")
    add("VAL4405_4_offworldtube_private_zero", any(row["component_id"] == "PZ4405_1_offworldtube_full_domain" and row["private_zero"] == "True" for row in zero_output), "off-worldtube private zero imported")
    add("VAL4405_5_raw_rows_blocked", all(row["current_status"] == "PLEAK_COMPONENT_ZERO_BLOCKED" for row in zero_output if "raw" in row["component_id"] or "exterior" in row["component_id"]), "raw/open rows remain blocked")
    add("VAL4405_6_zero_rows_nonclaim", all(row["claim_allowed"] == "False" for row in zero_output), "zero rows do not claim public/local pass")
    add("VAL4405_7_missing_bound_blocked", any(row["bound_id"] == "PB4405_0_missing_live_raw_bound" and row["current_status"] == "PLEAK_BOUND_BLOCKED" for row in bound_output), "missing raw finite row blocks")
    add("VAL4405_8_zero_bound_passes_nonclaim", any(row["bound_id"] == "PB4405_1_compact_private_zero_smoke" and row["within_bound"] == "True" and row["claim_allowed"] == "False" for row in bound_output), "zero smoke row passes but remains nonclaim")
    add("VAL4405_9_failure_control_detected", any(row["bound_id"] == "PB4405_3_source_hair_fail_smoke" and row["current_status"] == "PLEAK_BOUND_FAILS" for row in bound_output), "source-hair failure control detected")
    add("VAL4405_10_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "claim gates false")
    add("VAL4405_11_formal_marker", MARKER in text(FORMAL_PATH), "formal marker present")
    add("VAL4405_12_post_marker", MARKER in text(DOC_PATH), "post marker present")
    add("VAL4405_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker present")
    add("VAL4405_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker present")
    add("VAL4405_15_claim_row", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claim row present")
    add("VAL4405_16_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4405_17_generated_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows stay nonclaim")
    add("VAL4405_18_gate_exists", GATE_PATH.exists() and "def evaluate_bound_rows" in text(GATE_PATH), "P_leak gate script exists")
    add("VAL4405_19_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent")
    return rows


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    derivations = derivation_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, object]]] = {
        "P8_Y5_R2FR_4405_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4405_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4405_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4405_DECISION.csv": decisions,
        "P8_Y5_R2FR_4405_STATUS.csv": statuses,
        "P8_Y5_R2FR_4405_NEXT_TARGET.csv": next_targets,
    }
    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_csv(ZERO_INPUT, zero_inputs())
    zero_output = evaluate_zero_rows(ZERO_INPUT)
    write_csv(ZERO_OUTPUT, zero_output)
    csv_paths.extend([ZERO_INPUT, ZERO_OUTPUT])

    write_csv(BOUND_INPUT, bound_inputs())
    bound_output = evaluate_bound_rows(BOUND_INPUT)
    write_csv(BOUND_OUTPUT, bound_output)
    csv_paths.extend([BOUND_INPUT, BOUND_OUTPUT])

    write_formal_doc(sources, derivations, zero_output, bound_output, gates, decisions, next_targets)
    write_post_doc(decisions, next_targets)
    update_spine()
    update_packet()
    update_claims()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
