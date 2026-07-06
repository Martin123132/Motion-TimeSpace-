from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_projection_zero_gate import (  # noqa: E402
    claim_gate_rows,
    closure_contract_rows,
    decision_ledger_rows,
    projection_theorem_clause_rows,
    read_csv,
    rescue_route_rows,
    route_verdict_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4494"
CLAIM_ID = "L-336"
MARKER = "PPC4161_PARENT_PUBLIC_METRIC_PROJECTION_CDELTAKTF_ZERO_OR_LOCAL_BRANCH_DEMOTION_4494"
PACKET_MARKER = "PPC4161_PACKET_PARENT_PUBLIC_METRIC_PROJECTION_CDELTAKTF_ZERO_OR_LOCAL_BRANCH_DEMOTION_4494"
DECISION = "CDELTAKTF_ZERO_NOT_DERIVED_DELTAKTF_BRANCH_EXPLICIT_CLOSURE_ONLY_NONCLAIM"
NEXT_TARGET = "4495-Y5-R2FR-Ward-cohomology-public-projection-theorem-or-CDeltaKTF-closure-comparator.md"

FORMAL_PATH = FORMAL / "510-PPC4161-parent-public-metric-projection-CDeltaKTF-zero-or-local-branch-demotion.md"
DOC_PATH = POST / "4494-Y5-R2FR-parent-public-metric-projection-CDeltaKTF-zero-or-local-branch-demotion.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4494_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4494_SOURCE_REGISTER.csv"
CLAUSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_PROJECTION_ZERO_CLAUSE_AUDIT.csv"
ROUTE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_PUBLIC_METRIC_ROUTE_VERDICTS.csv"
CLOSURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_CDELTAKTF_CLOSURE_CONTRACT.csv"
RESCUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_RESCUE_ROUTE_TARGETS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4494_DECISION.csv"

FORMAL_509 = FORMAL / "509-PPC4161-Bprime-leakage-norm-computation-or-parent-projection-zero.md"
SCORER_4493 = SOURCE_DIR / "P8_Y5_R2FR_4493_DELTAKTF_REQUIREMENT_SCORER.csv"
FORMAL_136 = FORMAL / "136-metric-response-kernel-theorem.md"
FORMAL_138 = FORMAL / "138-metric-null-action-block-contract.md"
FORMAL_140 = FORMAL / "140-doubled-open-system-metric-null-theorem.md"
FORMAL_142 = FORMAL / "142-owner-spacetime-solder-map-theorem.md"
FORMAL_143 = FORMAL / "143-boundary-topological-backup-gate.md"
FORMAL_299 = FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md"
READOUT_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_HESSIAN_METRIC_READOUT.csv"
GATE_PATH = SCRIPT_DIR / "parent_projection_zero_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4494_parent_public_metric_projection_CDeltaKTF_zero_or_local_branch_demotion.py"

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
        ("SRC4494_00_formal509", FORMAL_509, "derive `C_DeltaKTF=0`", "4493 handoff to parent projection fork."),
        ("SRC4494_01_scorer4493", SCORER_4493, "DBS4493_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09", "4493 CDeltaKTF scorer rows."),
        ("SRC4494_02_kernel136", FORMAL_136, "Current parent v1 proves none of these", "136 metric response kernel obstruction."),
        ("SRC4494_03_contract138", FORMAL_138, "contract written; not derived", "138 metric-null contract status."),
        ("SRC4494_04_doubled140", FORMAL_140, "fail_hidden_metric_dependence", "140 doubled route obstruction."),
        ("SRC4494_05_solder142", FORMAL_142, "owner_spacetime_solder_map_bulk_hybrid_fails_boundary_topological_backup_open", "142 solder route failure."),
        ("SRC4494_06_backup143", FORMAL_143, "boundary_topological_backup_fails_transition_branch_demoted_closure_only", "143 boundary/topological demotion."),
        ("SRC4494_07_runner299", FORMAL_299, "generic boundary/topological route fails as a derivation", "299/4283 generic superpotential route failure."),
        ("SRC4494_08_readout4487", READOUT_4487, "METRIC_NULL_FAILS_ON_IDENTITY_READOUT", "4487 identity readout non-nullity."),
        ("SRC4494_09_gate", GATE_PATH, "def projection_theorem_clause_rows", "4494 helper."),
        ("SRC4494_10_generator", GENERATOR_PATH, 'CHECKPOINT = "4494"', "4494 generator script."),
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


def status_rows(closure_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    smooth_1e9 = [
        row
        for row in closure_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "C_DeltaKTF_zero_derived": False,
            "DeltaKTF_branch_status": "explicit_closure_only_until_new_parent_projection_theorem",
            "smoothstep_1e9_required_CDeltaKTF_max": smooth_1e9[0]["required_CDeltaKTF_max"] if smooth_1e9 else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "new_Ward_cohomology_or_terminal_public_projection_theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4494_0",
            "target": NEXT_TARGET,
            "objective": "Either introduce and prove a genuinely new parent Ward/cohomology/terminal-public-projection theorem for DeltaKTF silence, or build a transparent closure comparator using sourced C_DeltaKTF values.",
            "derive_first": "Ward/cohomology/public-projection theorem with ordinary matter GR preserved",
            "fallback": "explicit C_DeltaKTF closure comparator; no derived local-GR claim",
            "risk": "calling an explicit closure coefficient a derivation",
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
            "proof_result": "C_DeltaKTF=0 is not derived by current metric response, metric-null contract, doubled, solder, or boundary/topological routes",
            "fallback_result": "DeltaKTF local branch is demoted to an explicit closure coefficient with 4493 numeric maxima",
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
        "domain": "local_gr_newton_r10_deltaKTF_parent_projection",
        "claim": "4494 attempts the parent public-metric projection route for C_DeltaKTF=0 and finds it is not derived in the current corpus; the DeltaKTF branch is demoted to explicit closure-only unless a new Ward/cohomology/public-projection theorem is built.",
        "current_evidence": "4494 source register, projection-zero clause audit, route verdicts, CDeltaKTF closure contract, rescue-route targets, claim gates, status and validation.",
        "status": "private_CDeltaKTF_zero_not_derived_closure_only_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "resurrecting failed metric-null/solder/topological routes as if they derived DeltaKTF silence.",
        "sector": "local_gr_newton_r10_deltaKTF_parent_projection",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "explicit CDeltaKTF closure coefficient could be mistaken for a derived local-GR theorem",
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
    clauses: Sequence[Mapping[str, object]],
    routes: Sequence[Mapping[str, object]],
    closures: Sequence[Mapping[str, object]],
    rescues: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 510 PPC4161 - Parent Public Metric Projection CDeltaKTF Zero Or Local Branch Demotion

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4494 attempts the hard parent-projection move:

```text
C_DeltaKTF = 0
```

meaning the parent public metric must annihilate the non-`Y_a` Hessian footprint before it reaches local observables.

The verdict is blunt: this is **not derived** in the current corpus.

Why:

```text
identity readout -> nonzero metric footprint unless coefficient zero;
metric-null action block -> contract written, not derived;
doubled route -> hidden metric dependence fails;
owner-spacetime solder -> reintroduces g_loc / breaks covariance / needs new geometry;
boundary-topological backup -> generic route failed and was demoted;
profile shaping -> 4493 showed N_Bprime is order unity or larger.
```

Therefore the `DeltaKTF` local branch is now explicit closure-only unless a genuinely new parent theorem is added. That is not a failure of the whole MTS programme; it is a hygiene rule: this lane cannot be called derived local GR while `C_DeltaKTF` is an inserted silence coefficient.

## Projection-Zero Clause Audit

{table(clauses)}

## Public Metric Route Verdicts

{table(routes)}

## Explicit CDeltaKTF Closure Contract

{table(closures)}

## Rescue Route Targets

{table(rescues)}

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
    clauses: Sequence[Mapping[str, object]],
    routes: Sequence[Mapping[str, object]],
    closures: Sequence[Mapping[str, object]],
    rescues: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4494 Y5/R2FR - Parent Public Metric Projection CDeltaKTF Zero Or Local Branch Demotion

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4494 does the parent-projection audit and stops the `DeltaKTF` route from pretending to be derived. Current evidence does not prove `C_DeltaKTF=0`; the branch is explicit closure-only unless a new Ward/cohomology/public-projection theorem is built.

## Audit Tables

{table(clauses)}

{table(routes)}

{table(closures)}

{table(rescues)}

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
    clauses: Sequence[Mapping[str, object]],
    routes: Sequence[Mapping[str, object]],
    closures: Sequence[Mapping[str, object]],
    rescues: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4494_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4494_1_zero_not_derived", any(row.get("current_verdict") == "NOT_DERIVED" for row in clauses) and not any(row.get("current_verdict") == "DERIVED" for row in clauses), "C_DeltaKTF=0 is not claimed")
    add("VAL4494_2_failed_routes_carried", any(row.get("verdict") == "BULK_HYBRID_FAILS" for row in routes) and any(row.get("verdict") == "FAILED_FOR_GENERIC_ROUTE" for row in routes), "solder and boundary/topological failures carried")
    add("VAL4494_3_closure_rows_written", len(closures) >= 4 and all(row.get("closure_status") == "EXPLICIT_CLOSURE_COEFFICIENT_REQUIRED" for row in closures), "closure rows are explicit")
    add("VAL4494_4_rescue_routes_future_only", len(rescues) >= 3 and not any(str(row.get("current_status")) == "DERIVED" for row in rescues), "rescue routes are future theorem targets")
    add("VAL4494_5_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4494_6_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false" and str(statuses[0].get("C_DeltaKTF_zero_derived")).lower() == "false", "local_GR_claim and C_DeltaKTF_zero_derived remain false")
    add("VAL4494_7_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add(
        "VAL4494_8_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, clauses, routes, closures, rescues, ledger, gates, statuses, next_targets]
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
    add("VAL4494_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4494_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4494_11_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-336")
    add("VAL4494_12_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4494 markers")
    add("VAL4494_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    clauses = projection_theorem_clause_rows()
    routes = route_verdict_rows()
    closures = closure_contract_rows(read_csv(SCORER_4493))
    rescues = rescue_route_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, clauses, routes, closures, rescues)
    statuses = status_rows(closures)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CLAUSE_CSV, clauses)
    write_csv(ROUTE_CSV, routes)
    write_csv(CLOSURE_CSV, closures)
    write_csv(RESCUE_CSV, rescues)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, clauses, routes, closures, rescues, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, clauses, routes, closures, rescues, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4494 Parent Public Metric Projection CDeltaKTF Zero Or Local Branch Demotion",
        "4494 attempts to promote `C_DeltaKTF=0` through the parent public metric projection route and rejects it as currently derived. Existing metric-response, metric-null contract, doubled, owner-solder, and boundary/topological gates do not prove the zero. The `DeltaKTF` lane is now explicit closure-only unless a new Ward/cohomology/terminal-public-projection theorem is built or a tiny sourced `C_DeltaKTF` passes the 4493 scorer.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4494 Packet Integration",
        "The local branch must now treat `C_DeltaKTF` as an explicit closure coefficient, not a hidden theorem. Next serious work is either a genuinely new parent Ward/cohomology/public-projection theorem or a transparent closure comparator; no local-GR/J2/PPN claim is allowed from this lane.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        CLAUSE_CSV,
        ROUTE_CSV,
        CLOSURE_CSV,
        RESCUE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, clauses, routes, closures, rescues, ledger, gates, statuses, next_targets, csv_paths)
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
