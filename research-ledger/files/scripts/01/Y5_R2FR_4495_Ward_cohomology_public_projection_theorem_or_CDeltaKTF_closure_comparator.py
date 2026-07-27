from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ward_cohomology_projection_gate import (  # noqa: E402
    claim_gate_rows,
    closure_trial_rows,
    comparator_summary_rows,
    conditional_zero_rows,
    decision_ledger_rows,
    read_csv,
    theorem_attempt_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4495"
CLAIM_ID = "L-337"
MARKER = "PPC4161_WARD_COHOMOLOGY_PUBLIC_PROJECTION_OR_CDELTAKTF_CLOSURE_COMPARATOR_4495"
PACKET_MARKER = "PPC4161_PACKET_WARD_COHOMOLOGY_PUBLIC_PROJECTION_OR_CDELTAKTF_CLOSURE_COMPARATOR_4495"
DECISION = "SUPPORT_SEPARATED_CONDITIONAL_ZERO_GENERIC_DELTAKTF_CLOSURE_COMPARATOR_READY_NONCLAIM"
NEXT_TARGET = "4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md"

FORMAL_PATH = FORMAL / "511-PPC4161-Ward-cohomology-public-projection-theorem-or-CDeltaKTF-closure-comparator.md"
DOC_PATH = POST / "4495-Y5-R2FR-Ward-cohomology-public-projection-theorem-or-CDeltaKTF-closure-comparator.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4495_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4495_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_WARD_COHOMOLOGY_THEOREM_ATTEMPT.csv"
CONDITIONAL_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_CONDITIONAL_ZERO_SCOPE.csv"
CLOSURE_TRIAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_CDELTAKTF_CLOSURE_TRIALS.csv"
CLOSURE_SUMMARY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_CDELTAKTF_COMPARATOR_SUMMARY.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4495_DECISION.csv"

FORMAL_510 = FORMAL / "510-PPC4161-parent-public-metric-projection-CDeltaKTF-zero-or-local-branch-demotion.md"
CLOSURE_4494 = SOURCE_DIR / "P8_Y5_R2FR_4494_CDELTAKTF_CLOSURE_CONTRACT.csv"
FORMAL_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
POST_4176 = POST / "4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md"
POST_4276 = POST / "4276-Y5-R2FR-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md"
COUNTER_4276 = SOURCE_DIR / "P8_Y5_R2FR_4276_TERMINALITY_COUNTERMODEL_AUDIT.csv"
POST_4288 = POST / "4288-Y5-R2FR-finite-margin-AJ-zero-domain-split-and-transition-frontier.md"
FORMAL_143 = FORMAL / "143-boundary-topological-backup-gate.md"
FORMAL_299 = FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md"
GATE_PATH = SCRIPT_DIR / "ward_cohomology_projection_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4495_Ward_cohomology_public_projection_theorem_or_CDeltaKTF_closure_comparator.py"

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
        ("SRC4495_00_formal510", FORMAL_510, "explicit closure-only unless a genuinely new parent theorem is added", "4494 handoff."),
        ("SRC4495_01_closure4494", CLOSURE_4494, "CDC4494_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09", "4494 closure maxima."),
        ("SRC4495_02_formal192", FORMAL_192, "J_tr^nu = 0 through <=2PN", "192 no-flux theorem."),
        ("SRC4495_03_post4176", POST_4176, "LOCAL_BOUNDARY_NO_FLUX_THEOREM_CLOSES_TRANSITION_CURRENT_PRIVATE_SELECTOR", "4176 no-flux checkpoint."),
        ("SRC4495_04_post4276", POST_4276, "terminal metric exists => g_X=0", "4276 terminality rejection."),
        ("SRC4495_05_counter4276", COUNTER_4276, "CM4276_0_terminal_but_E_visible", "4276 terminality countermodels."),
        ("SRC4495_06_post4288", POST_4288, "A_J,eff_private=0", "4288 support-separated AJ zero import."),
        ("SRC4495_07_formal143", FORMAL_143, "boundary_topological_backup_fails_transition_branch_demoted_closure_only", "143 generic backup failure."),
        ("SRC4495_08_formal299", FORMAL_299, "generic boundary/topological route fails as a derivation", "299/4283 generic superpotential failure."),
        ("SRC4495_09_gate", GATE_PATH, "def closure_trial_rows", "4495 helper."),
        ("SRC4495_10_generator", GENERATOR_PATH, 'CHECKPOINT = "4495"', "4495 generator script."),
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


def status_rows(summary_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    smooth_1e9 = [
        row
        for row in summary_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "support_separated_zero": "conditional_private_selector_only",
            "generic_DeltaKTF_status": "explicit_CDeltaKTF_closure_or_real_shell_profiles_required",
            "smoothstep_1e9_largest_passing_trial_CDeltaKTF": smooth_1e9[0]["largest_passing_trial_CDeltaKTF"] if smooth_1e9 else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "real_DeltaKTF_shell_profile_or_parent_matter_interface_projection_theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4495_0",
            "target": NEXT_TARGET,
            "objective": "Either source/build real DeltaKTF transition-shell profile inputs for the comparator, or derive the stronger parent matter-interface/terminal-projection theorem that sets the coefficient to zero.",
            "derive_first": "parent matter-interface action-domain descent with Dg_public[DeltaK_TF]=0 and no shadow labels",
            "fallback": "real shell/profile rows feeding C_DeltaKTF comparator across J2/PPN/clock/orbital arenas",
            "risk": "using the support-separated collar zero outside its domain",
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
            "proof_result": "support-separated no-flux/cohomology branch gives a conditional private zero; generic Ward/public-projection theorem remains not derived",
            "fallback_result": "C_DeltaKTF closure comparator generated from 4494 maxima and trial coefficients",
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
        "domain": "local_gr_newton_r10_deltaKTF_ward_cohomology_closure",
        "claim": "4495 separates the support-separated compact-collar conditional zero from the generic DeltaKTF transition shell, and builds an explicit CDeltaKTF closure comparator from the 4494 maxima.",
        "current_evidence": "4495 source register, Ward/cohomology theorem attempt, conditional zero scope rows, CDeltaKTF closure trials, comparator summary, claim gates, status and validation.",
        "status": "private_conditional_zero_plus_closure_comparator_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "using support-separated no-flux zero outside its compact collar domain, or treating closure coefficients as derived.",
        "sector": "local_gr_newton_r10_deltaKTF_ward_cohomology_closure",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "generic DeltaKTF shell still needs real profile inputs or a parent matter-interface projection theorem",
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
    zero_rows: Sequence[Mapping[str, object]],
    trial_rows: Sequence[Mapping[str, object]],
    summary_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 511 PPC4161 - Ward/Cohomology/Public Projection Theorem Or CDeltaKTF Closure Comparator

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4495 makes the distinction that matters:

```text
support-separated compact local collar: conditional zero survives;
generic DeltaKTF transition shell: no zero theorem yet.
```

The positive result is real but scoped. The 192/4176 no-flux theorem plus the 4288 finite-margin import allow an effective local zero when the transition support is outside the compact local collar, side/interface pullbacks vanish, and boundary Hamiltonian terms are fixed, zero, or routed.

The generic route still does not close: no transition Ward/anomaly identity is derived, terminal public metric alone is rejected by 4276 countermodels, and the stronger matter-interface action-domain descent remains unsigned.

So the fallback is now executable rather than vague: `C_DeltaKTF` is kept visible and scored against the 4494 maxima.

## Ward/Cohomology Theorem Attempt

{table(theorem_rows)}

## Conditional Zero Scope

{table(zero_rows)}

## CDeltaKTF Comparator Summary

{table(summary_rows)}

## CDeltaKTF Closure Trials

{table(trial_rows)}

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
    zero_rows: Sequence[Mapping[str, object]],
    trial_rows: Sequence[Mapping[str, object]],
    summary_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4495 Y5/R2FR - Ward/Cohomology/Public Projection Theorem Or CDeltaKTF Closure Comparator

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4495 keeps the good theorem but cages it properly: support-separated compact collars get conditional zero; generic `DeltaKTF` shell gets an explicit comparator, not a pretend theorem.

## Theorem And Comparator

{table(theorem_rows)}

{table(zero_rows)}

{table(summary_rows)}

{table(trial_rows)}

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
    zero_rows: Sequence[Mapping[str, object]],
    trial_rows: Sequence[Mapping[str, object]],
    summary_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    smooth_1e9 = [
        row
        for row in summary_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    add("VAL4495_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4495_1_conditional_zero_scoped", any(row.get("sets_C_DeltaKTF_zero") is True for row in zero_rows) and any(row.get("sets_C_DeltaKTF_zero") is False for row in zero_rows), "conditional zero and generic nonzero rows both present")
    add("VAL4495_2_generic_theorem_not_promoted", any(row.get("derivation_status") == "NOT_DERIVED" for row in theorem_rows) and any(row.get("derivation_status") == "REJECTED" for row in theorem_rows), "generic Ward/public projection theorem is not promoted")
    add("VAL4495_3_comparator_rows_written", len(trial_rows) >= 32 and len(summary_rows) >= 4, f"{len(trial_rows)} trial rows and {len(summary_rows)} summary rows")
    add("VAL4495_4_smoothstep_1e9_trial_scale", bool(smooth_1e9) and str(smooth_1e9[0].get("unit_CDeltaKTF_passes")).lower() == "false" and float(smooth_1e9[0].get("largest_passing_trial_CDeltaKTF", "0")) >= 1.0e-23, "smoothstep 1e9 comparator allows tiny trial but rejects unit coefficient")
    add("VAL4495_5_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4495_6_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4495_7_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add(
        "VAL4495_8_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, theorem_rows, zero_rows, trial_rows, summary_rows, ledger, gates, statuses, next_targets]
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
    add("VAL4495_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4495_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4495_11_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-337")
    add("VAL4495_12_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4495 markers")
    add("VAL4495_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    theorem_rows = theorem_attempt_rows()
    zero_rows = conditional_zero_rows()
    trial_rows = closure_trial_rows(read_csv(CLOSURE_4494))
    summary_rows = comparator_summary_rows(trial_rows)
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, theorem_rows, zero_rows, trial_rows, summary_rows)
    statuses = status_rows(summary_rows)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_ATTEMPT_CSV, theorem_rows)
    write_csv(CONDITIONAL_ZERO_CSV, zero_rows)
    write_csv(CLOSURE_TRIAL_CSV, trial_rows)
    write_csv(CLOSURE_SUMMARY_CSV, summary_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, zero_rows, trial_rows, summary_rows, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, theorem_rows, zero_rows, trial_rows, summary_rows, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4495 Ward/Cohomology/Public Projection Or CDeltaKTF Closure Comparator",
        "4495 separates a real conditional zero from the generic shell problem. In support-separated compact collars, 192/4176 no-flux plus 4288 finite-margin import gives an effective local zero. Outside that restricted branch, no Ward/cohomology/public-projection theorem is derived; terminal public metric alone is rejected by 4276, so generic `DeltaKTF` uses an explicit `C_DeltaKTF` closure comparator built from the 4494 maxima.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4495 Packet Integration",
        "The packet now has a clean split: conditional no-flux zero for support-separated collars, explicit `C_DeltaKTF` comparator for generic transition shell. Next work should source real shell/profile inputs or derive the stronger parent matter-interface/public-projection theorem.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_ATTEMPT_CSV,
        CONDITIONAL_ZERO_CSV,
        CLOSURE_TRIAL_CSV,
        CLOSURE_SUMMARY_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, theorem_rows, zero_rows, trial_rows, summary_rows, ledger, gates, statuses, next_targets, csv_paths)
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
