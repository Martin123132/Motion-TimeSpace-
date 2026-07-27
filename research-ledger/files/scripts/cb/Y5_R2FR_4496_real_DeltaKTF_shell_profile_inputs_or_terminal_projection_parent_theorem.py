from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import (  # noqa: E402
    branch_verdict_rows,
    claim_gate_rows,
    closure_crosswalk_rows,
    decision_ledger_rows,
    read_csv,
    shell_input_import_rows,
    shell_projection_comparator_rows,
    terminal_projection_theorem_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4496"
CLAIM_ID = "L-338"
MARKER = "PPC4161_REAL_DELTAKTF_SHELL_PROFILE_INPUTS_OR_TERMINAL_PROJECTION_PARENT_THEOREM_4496"
PACKET_MARKER = "PPC4161_PACKET_REAL_DELTAKTF_SHELL_PROFILE_INPUTS_OR_TERMINAL_PROJECTION_PARENT_THEOREM_4496"
DECISION = "STANDARD_MATTER_DESCENT_CONDITIONAL_GENERIC_SHELL_PROFILE_FAILS_NONLOCAL_OWNER_OR_EXPLICIT_PROJECTION_REQUIRED_NONCLAIM"
NEXT_TARGET = "4497-Y5-R2FR-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md"

FORMAL_PATH = FORMAL / "512-PPC4161-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md"
DOC_PATH = POST / "4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4496_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4496_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_TERMINAL_PROJECTION_THEOREM_AUDIT.csv"
SHELL_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_SHELL_INPUT_IMPORT.csv"
SHELL_COMPARATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_SHELL_PROJECTION_COMPARATOR.csv"
CROSSWALK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_SHELL_CDELTAKTF_CROSSWALK.csv"
BRANCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_BRANCH_VERDICTS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4496_DECISION.csv"

FORMAL_511 = FORMAL / "511-PPC4161-Ward-cohomology-public-projection-theorem-or-CDeltaKTF-closure-comparator.md"
POST_4277 = POST / "4277-Y5-R2FR-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"
THEOREM_4277 = SOURCE_DIR / "P8_Y5_R2FR_4277_MATTER_INTERFACE_DESCENT_THEOREM.csv"
STATUS_4277 = SOURCE_DIR / "P8_Y5_R2FR_4277_STATUS.csv"
POST_4284 = POST / "4284-Y5-R2FR-real-transition-shell-profile-calculator-and-threshold-comparator.md"
SHELL_INPUTS_4284 = SOURCE_DIR / "P8_Y5_R2FR_4284_SOLAR_SHELL_INPUTS.csv"
PROFILE_RESULTS_4284 = SOURCE_DIR / "P8_Y5_R2FR_4284_PROFILE_COMPARATOR_RESULTS.csv"
SUPPRESSION_4284 = SOURCE_DIR / "P8_Y5_R2FR_4284_SUPPRESSION_REQUIREMENTS.csv"
CLOSURE_4494 = SOURCE_DIR / "P8_Y5_R2FR_4494_CDELTAKTF_CLOSURE_CONTRACT.csv"
COUNTER_4276 = SOURCE_DIR / "P8_Y5_R2FR_4276_TERMINALITY_COUNTERMODEL_AUDIT.csv"
POST_803 = POST / "803-Y5-R10-transition-shell-exact-cancellation-projector-or-quarantine.md"
GATE_PATH = SCRIPT_DIR / "deltaktf_shell_profile_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4496_real_DeltaKTF_shell_profile_inputs_or_terminal_projection_parent_theorem.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


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


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4496_00_formal511", FORMAL_511, "generic DeltaKTF transition shell: no zero theorem yet", "4495 handoff."),
        ("SRC4496_01_post4277", POST_4277, "STANDARD_BRANCH_MATTER_INTERFACE_DESCENT_DERIVES_GX_ZERO_CONDITIONAL_NONCLAIM", "4277 standard matter descent checkpoint."),
        ("SRC4496_02_theorem4277", THEOREM_4277, "AD4277_5_canonical_zero", "4277 descent theorem rows."),
        ("SRC4496_03_status4277", STATUS_4277, "standard-branch matter-interface descent derives g_X=b_dis=0", "4277 status."),
        ("SRC4496_04_post4284", POST_4284, "fails by 2.2821012202909584e+16", "4284 direct shell profile result."),
        ("SRC4496_05_inputs4284", SHELL_INPUTS_4284, "SHELL4284_U_B", "4284 real shell source inputs."),
        ("SRC4496_06_results4284", PROFILE_RESULTS_4284, "COMP4284_0_bare", "4284 profile comparator rows."),
        ("SRC4496_07_suppression4284", SUPPRESSION_4284, "REQ4284_2_nonlocal", "4284 suppression requirements."),
        ("SRC4496_08_closure4494", CLOSURE_4494, "CDC4494_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09", "4494 DeltaKTF closure scale."),
        ("SRC4496_09_counter4276", COUNTER_4276, "CM4276_0_terminal_but_E_visible", "4276 terminality countermodels."),
        ("SRC4496_10_post803", POST_803, "transition shell still blocks derived local GR", "803 transition shell obstruction."),
        ("SRC4496_11_gate", GATE_PATH, "def shell_projection_comparator_rows", "4496 helper."),
        ("SRC4496_12_generator", GENERATOR_PATH, 'CHECKPOINT = "4496"', "4496 generator script."),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        line_number = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_kind": "local",
                "source_ref": str(path),
                "local_path_exists": path.exists(),
                "needle": needle,
                "needle_found": bool(line_number),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def status_rows(shell_rows: Sequence[Mapping[str, object]], branch_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    bare = [row for row in shell_rows if row.get("source_comparator_id") == "COMP4284_0_bare"]
    generic = [row for row in branch_rows if row.get("branch_id") == "BV4496_2_generic_transition_shell"]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "standard_matter_descent_status": "conditional_component_zero_not_generic_shell_zero",
            "generic_shell_status": generic[0]["verdict"] if generic else "",
            "bare_shell_required_projection_factor": bare[0]["required_projection_factor_to_pass"] if bare else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "parent_nonlocal_owner_kernel_or_explicit_shell_projection_factor",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4496_0",
            "target": NEXT_TARGET,
            "objective": "Either derive the parent nonlocal owner/kernel that removes the real transition shell from local metric response, or build an arena transfer matrix consuming explicit shell projection factors for J2, PPN, clocks, orbital and R10 rows.",
            "derive_first": "nonlocal owner/kernel theorem for transition shell metric response",
            "fallback": "explicit shell projection arena transfer matrix with no local-GR promotion",
            "risk": "confusing standard matter-interface descent or support-separated collar zero with generic shell safety",
            "valid_for_claim": False,
        }
    ]


def decision_row() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "proof_result": "standard matter-interface descent is conditionally derived for g_X/b_dis/Dq_geom but does not zero generic DeltaKTF shell response",
            "fallback_result": "4284 real transition-shell profile rows are imported and show direct projection fails by huge factors, requiring nonlocal owner/kernel theorem or explicit tiny projection",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body.strip()}\n"
    write_text(path, existing.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r10_deltaKTF_shell_profile",
        "claim": "4496 crosswalks the standard matter-interface descent with real transition-shell profile inputs: 4277 closes g_X/b_dis/Dq_geom conditionally, but 4284 real shell rows show generic direct shell projection fails by huge factors and needs nonlocal owner/kernel or explicit projection.",
        "current_evidence": "4496 source register, terminal projection theorem audit, shell input import, shell projection comparator, shell/CDeltaKTF crosswalk, branch verdicts, claim gates, status and validation.",
        "status": "private_shell_profile_crosswalk_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "using standard matter-interface descent or no-flux collar zero as generic transition-shell safety.",
        "sector": "local_gr_newton_r10_deltaKTF_shell_profile",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "direct shell projection is far above local bounds unless a parent kernel theorem or tiny projection coefficient is added",
    }
    replaced = False
    for index, row in enumerate(rows):
        if row.get("claim_id") == CLAIM_ID:
            rows[index] = new_row
            replaced = True
            break
    if not replaced:
        rows.append(new_row)
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    shell_inputs: Sequence[Mapping[str, object]],
    shell_rows: Sequence[Mapping[str, object]],
    crosswalk_rows: Sequence[Mapping[str, object]],
    branch_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 512 PPC4161 - Real DeltaKTF Shell Profile Inputs Or Terminal Projection Parent Theorem

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4496 crosswalks two things that must not be conflated:

```text
4277 standard matter-interface descent:
  closes g_X, b_dis and Dq_geom conditionally.

generic DeltaKTF / transition shell:
  not closed by that theorem.
```

The real shell side is already in the corpus from 4284. Imported directly, the transition-shell profile fails the local proxy by huge factors:

```text
bare direct projection      -> fails by ~2.28e16
U_B^2 transition projection -> fails by ~2.37e16
wide shell scaling          -> fails by ~2.37e18
```

So the shell branch is now genuinely quantified: it needs either a parent nonlocal owner/kernel theorem that removes it from local metric response, or an explicit projection coefficient below the imported shell thresholds. The standard matter-interface descent remains useful, but it is not a license to erase the generic shell.

## Terminal Projection / Matter Descent Audit

{table(theorem_rows)}

## Real Shell Input Import

{table(shell_inputs)}

## Shell Projection Comparator

{table(shell_rows)}

## Shell To CDeltaKTF Crosswalk

{table(crosswalk_rows)}

## Branch Verdicts

{table(branch_rows)}

## Decision Ledger

{table(ledger)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def post_body(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    shell_inputs: Sequence[Mapping[str, object]],
    shell_rows: Sequence[Mapping[str, object]],
    crosswalk_rows: Sequence[Mapping[str, object]],
    branch_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4496 Y5/R2FR - Real DeltaKTF Shell Profile Inputs Or Terminal Projection Parent Theorem

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4496 imports the real 4284 transition-shell profile rows and separates them from the 4277 standard matter-interface descent. Standard matter descent helps one component branch; the generic shell still fails direct local projection by huge factors.

## Tables

{table(theorem_rows)}

{table(shell_inputs)}

{table(shell_rows)}

{table(crosswalk_rows)}

{table(branch_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(statuses)}

{table(next_targets)}

{table(decisions)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    theorem_rows: Sequence[Mapping[str, object]],
    shell_inputs: Sequence[Mapping[str, object]],
    shell_rows: Sequence[Mapping[str, object]],
    crosswalk_rows: Sequence[Mapping[str, object]],
    branch_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    bare = [row for row in shell_rows if row.get("source_comparator_id") == "COMP4284_0_bare"]
    standard = [row for row in theorem_rows if row.get("theorem_id") == "TPT4496_0_standard_matter_descent"]
    add("VAL4496_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4496_1_standard_branch_not_overextended", bool(standard) and standard[0].get("result") == "CONDITIONAL_STANDARD_BRANCH_DERIVED" and standard[0].get("applies_to_DeltaKTF_shell") is False, "4277 standard branch is scoped")
    add("VAL4496_2_shell_inputs_imported", len(shell_inputs) >= 6, f"{len(shell_inputs)} shell inputs imported")
    add("VAL4496_3_bare_shell_fails_huge", bool(bare) and float(bare[0]["PPN_ratio_to_budget"]) > 1.0e16, "bare shell fails by >1e16")
    add("VAL4496_4_crosswalk_rows_written", len(crosswalk_rows) >= 5, "shell projection factors crosswalked to DeltaKTF closure scale")
    add("VAL4496_5_branch_verdicts_written", len(branch_rows) >= 4 and any(row.get("verdict") == "DIRECT_PROFILE_FAILS_LARGE_FACTOR" for row in branch_rows), "branch verdicts separate standard/collar/shell/control")
    add("VAL4496_6_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4496_7_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4496_8_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add(
        "VAL4496_9_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, shell_inputs, shell_rows, crosswalk_rows, branch_rows, ledger, gates, statuses, next_targets]
            for row in group
        ),
        "all generated rows are private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4496_10_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4496_11_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4496_12_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-338")
    add("VAL4496_13_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4496 markers")
    add("VAL4496_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = terminal_projection_theorem_rows()
    shell_inputs = shell_input_import_rows(read_csv(SHELL_INPUTS_4284))
    shell_rows = shell_projection_comparator_rows(read_csv(PROFILE_RESULTS_4284))
    crosswalk_rows = closure_crosswalk_rows(shell_rows, read_csv(CLOSURE_4494))
    branch_rows = branch_verdict_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, shell_rows, crosswalk_rows, branch_rows)
    statuses = status_rows(shell_rows, branch_rows)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem_rows)
    write_csv(SHELL_INPUT_CSV, shell_inputs)
    write_csv(SHELL_COMPARATOR_CSV, shell_rows)
    write_csv(CROSSWALK_CSV, crosswalk_rows)
    write_csv(BRANCH_CSV, branch_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, shell_inputs, shell_rows, crosswalk_rows, branch_rows, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, theorem_rows, shell_inputs, shell_rows, crosswalk_rows, branch_rows, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4496 Real DeltaKTF Shell Profile Inputs Or Terminal Projection Parent Theorem",
        "4496 crosswalks 4277 standard matter-interface descent with 4284 real transition-shell profile rows. The standard branch conditionally closes `g_X`, `b_dis`, and `Dq_geom`, but it does not generically zero `DeltaKTF` shell response. The 4284 shell profile rows show direct projection fails by huge factors, so the generic shell needs a parent nonlocal owner/kernel theorem or an explicit tiny projection coefficient.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4496 Packet Integration",
        "The packet now carries real shell profile inputs for this local branch. Standard matter descent, support-separated collar zero, and generic transition shell are separated; only the first two are conditional zeros. Generic shell local-GR safety remains nonclaim pending owner-kernel theorem or arena transfer matrix.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        SHELL_INPUT_CSV,
        SHELL_COMPARATOR_CSV,
        CROSSWALK_CSV,
        BRANCH_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, theorem_rows, shell_inputs, shell_rows, crosswalk_rows, branch_rows, ledger, gates, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
