from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_action_zero_certificate_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    parent_action_certificate_rows,
    read_csv,
    refinement_certificate_rows,
    rollup_rows,
    source_silence_audit_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4467"
CLAIM_ID = "L-309"
MARKER = "PPC4161_PARENT_ACTION_SOURCE_SILENCE_OR_REFINEMENT_CR2_ZERO_CERTIFICATE_4467"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_SOURCE_SILENCE_OR_REFINEMENT_CR2_ZERO_CERTIFICATE_4467"
DECISION = "PARENT_ACTION_ZERO_CERTIFICATE_AUDITED_SOURCE_SILENCE_AND_CR2_ZERO_UNSIGNED_FINITE_BRANCH_RETAINED_NONCLAIM"
NEXT_TARGET = "4468-Y5-R2FR-parent-action-normal-form-no-Achi-no-second-channel-proof-or-finite-scalar-pack.md"

FORMAL_PATH = FORMAL / "483-PPC4161-parent-action-source-silence-or-refinement-cR2-zero-certificate.md"
DOC_PATH = POST / "4467-Y5-R2FR-parent-action-source-silence-or-refinement-cR2-zero-certificate.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4467_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4467_SOURCE_REGISTER.csv"
PARENT_CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_PARENT_ACTION_CERTIFICATE.csv"
SOURCE_SILENCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_SOURCE_SILENCE_AUDIT.csv"
REFINEMENT_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_REFINEMENT_ZERO_CERTIFICATE.csv"
ROLLUP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_SIGNED_VS_UNSIGNED_ROLLUP.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4467_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_action_zero_certificate_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4467_parent_action_source_silence_or_refinement_cR2_zero_certificate.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4466 = SOURCE_DIR / "P8_Y5_R2FR_4466_NEXT_TARGET.csv"
FORMAL_482 = FORMAL / "482-PPC4161-common-mode-scalar-decoupling-or-cR2-zero-against-R10-pressure.md"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
QVC_1023_DOC = POST / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
QVC_1023_CSV = SOURCE_DIR / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
NO_POLE_670_CSV = SOURCE_DIR / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
MATTER_4277_DOC = POST / "4277-Y5-R2FR-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"
MATTER_4277_CSV = SOURCE_DIR / "P8_Y5_R2FR_4277_MATTER_INTERFACE_DESCENT_THEOREM.csv"
XI_4332_CSV = SOURCE_DIR / "P8_Y5_R2FR_4332_XI_CLAUSE_AUDIT.csv"
REFINEMENT_4459_CSV = SOURCE_DIR / "P8_Y5_R2FR_4459_REFINEMENT_LINEARITY_THEOREM.csv"
REFINEMENT_4460_CSV = SOURCE_DIR / "P8_Y5_R2FR_4460_PARENT_REFINEMENT_SIGNATURE_CONTRACT.csv"
OWNER_4461_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_OWNER_COMPATIBILITY_THEOREM.csv"


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


def source_specs() -> List[Dict[str, object]]:
    return [
        {
            "source_id": "SRC4467_00_next4466",
            "ref": NEXT_4466,
            "needle": "parent-action-source-silence-or-refinement-cR2-zero-certificate",
            "role": "4466 selected the parent-action zero certificate as the next target.",
        },
        {
            "source_id": "SRC4467_01_formal482",
            "ref": FORMAL_482,
            "needle": "three honest exits",
            "role": "4466 reduced the common-mode scalar problem to source silence, c_R2 zero, or finite bounds.",
        },
        {
            "source_id": "SRC4467_02_formal193",
            "ref": FORMAL_193,
            "needle": "delta_v S_matter",
            "role": "early quotient-naturality matter-silence theorem language.",
        },
        {
            "source_id": "SRC4467_03_qvc1023_doc",
            "ref": QVC_1023_DOC,
            "needle": "single `q/v_X/action` certificate does not close",
            "role": "1023 failed the global q/v_X/action certificate.",
        },
        {
            "source_id": "SRC4467_04_qvc1023_csv",
            "ref": QVC_1023_CSV,
            "needle": "QVC1023_8_verdict",
            "role": "1023 certificate verdict row.",
        },
        {
            "source_id": "SRC4467_05_no_pole670",
            "ref": NO_POLE_670_CSV,
            "needle": "NQ670_8_no_pole_result",
            "role": "670 no-pole quotient proof chain and unsigned prerequisites.",
        },
        {
            "source_id": "SRC4467_06_matter4277_doc",
            "ref": MATTER_4277_DOC,
            "needle": "delta_v S_matter = 0",
            "role": "4277 standard-branch matter descent theorem.",
        },
        {
            "source_id": "SRC4467_07_matter4277_csv",
            "ref": MATTER_4277_CSV,
            "needle": "AD4277_5_canonical_zero",
            "role": "4277 canonical g_X/b_dis zero row.",
        },
        {
            "source_id": "SRC4467_08_xi4332",
            "ref": XI_4332_CSV,
            "needle": "AUD4332_6_global_parent_gap",
            "role": "4332 hidden source/readout tail gap.",
        },
        {
            "source_id": "SRC4467_09_refinement4459",
            "ref": REFINEMENT_4459_CSV,
            "needle": "RFL4459_0_target",
            "role": "4459 exact refinement-linearity theorem.",
        },
        {
            "source_id": "SRC4467_10_refinement4460",
            "ref": REFINEMENT_4460_CSV,
            "needle": "RGC4460_4_geometry_owner",
            "role": "4460 parent refinement signature contract and owner gap.",
        },
        {
            "source_id": "SRC4467_11_owner4461",
            "ref": OWNER_4461_CSV,
            "needle": "OCT4461_4_refinement_linearity",
            "role": "4461 owner compatibility theorem status.",
        },
        {
            "source_id": "SRC4467_12_gate",
            "ref": GATE_PATH,
            "needle": "def parent_action_certificate_rows",
            "role": "4467 parent-action zero certificate gate.",
        },
        {
            "source_id": "SRC4467_13_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4467"',
            "role": "4467 generator script.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["ref"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(path),
                "local_path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "source_silence_result": "conditional branch theorem only; no global parent-owned no-A(chi)/no-theta/no-Xi-open certificate",
            "refinement_result": "exact linearity math exists; full parent refinement/geometry/no-second-channel signature unsigned",
            "scalar_result": "finite common-mode scalar branch remains retained as bound-only under R10/PPN/orbital pressure",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "source_silence_status": "conditional_standard_branch_not_global_parent_signed",
            "refinement_status": "linearity_math_signed_parent_certificate_unsigned",
            "finite_scalar_status": "retained_bound_only_under_R10_pressure",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4467_0",
            "target": NEXT_TARGET,
            "objective": "Attempt the exact parent action normal form: no A(chi) matter factor and no second curvature-square channel.",
            "derive_first": "inspect parent action grammar for absence of hidden conformal/disformal/source-label slots and second R2 channel",
            "fallback": "finite common-mode scalar source-backed coefficient pack with live R10 curve, parent C_matter and c_R2_eff",
            "risk": "overclaiming branch-local source silence or refinement linearity as full local-GR reduction",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
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
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r10_scalar_source_coupling",
        "claim": "The local-GR common-mode scalar route has two exact zero certificates: parent-signed source silence or parent-signed refinement c_R2 zero; neither signs globally yet, so the finite scalar branch remains bound-only.",
        "current_evidence": "4467 parent action certificate, source silence audit, refinement zero certificate, signed-vs-unsigned rollup, claim gates, decision/status/next CSVs and validation.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "mistaking standard-branch quotient silence or exact refinement-linearity math for a fully parent-signed local-GR reduction.",
        "sector": "local_gr_newton_r10_scalar_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "common-mode fifth force survives if C_matter or c_R2_eff is finite",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    section = f"\n\n<!-- {marker} -->\n## {title}\n\n{body.strip()}\n"
    write_text(path, current.rstrip() + section)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    source_audit: Sequence[Mapping[str, object]],
    refinement_rows_: Sequence[Mapping[str, object]],
    rollup: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 483 PPC4161 — Parent-Action Source Silence Or Refinement `c_R2` Zero Certificate

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

The exact zero routes are now cleanly separated:

1. **Source silence:** if the parent action has no `A(chi)`, no `theta_j(chi)`, no hidden matter/source operator and no source-prefactor slot, then `delta_chi S_matter=0`, `C_matter=0` and `alpha_eff=C_matter^2/3=0`.
2. **Refinement zero:** if the parent refinement action is quotient/cylindrical, parent owns the hinge/connection/coframe channel and no second curvature-square channel survives, then the 4459 linearity theorem kills the visible quadratic channel and gives `c_R2_eff=0`.
3. **Finite branch:** because neither full parent certificate signs today, the common-mode scalar branch remains a finite bound-only branch under R10/PPN/orbital pressure.

This is not a local-GR claim. It is a tighter proof contract: the route to GR/Newton now has to sign either the matter-source silence normal form or the refinement/no-second-channel normal form.

## Parent Action Certificate

{table(parent_rows)}

## Source Silence Audit

{table(source_audit)}

## Refinement Zero Certificate

{table(refinement_rows_)}

## Signed Versus Unsigned Rollup

{table(rollup)}

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
    parent_rows: Sequence[Mapping[str, object]],
    source_audit: Sequence[Mapping[str, object]],
    refinement_rows_: Sequence[Mapping[str, object]],
    rollup: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4467 Y5 R2FR — Parent-Action Source Silence Or Refinement `c_R2` Zero Certificate

Private post-checkpoint mirror for formal document:

`{FORMAL_PATH}`

## What This Actually Moves Forward

This checkpoint does not circle the missing coupling in words; it turns it into a two-door exact certificate:

- Door 1: prove the parent action has no matter/source dependence on the local scalar representative `chi`.
- Door 2: prove the parent refinement geometry kills `c_R2_eff` and no second curvature-square channel exists.

If neither door signs, the local branch is not dead, but it is finite and must be scored against real R10/PPN/orbital bounds. That is the honest boxing scorecard.

## Parent Certificate

{table(parent_rows)}

## Source Silence

{table(source_audit)}

## Refinement Zero

{table(refinement_rows_)}

## Rollup

{table(rollup)}

## Gates

{table(gates)}

## Decisions

{table(ledger)}

{table(decisions)}

## Status And Next Target

{table(statuses)}

{table(next_targets)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    source_audit: Sequence[Mapping[str, object]],
    refinement_rows_: Sequence[Mapping[str, object]],
    rollup: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
            }
        )

    add(
        "VAL4467_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    parent_verdict = [row for row in parent_rows if row.get("certificate_id") == "PAC4467_5_verdict"]
    add(
        "VAL4467_1_parent_certificate_not_signed",
        bool(parent_verdict) and str(parent_verdict[0].get("signed_now")).lower() == "false",
        "parent certificate verdict exists and remains unsigned",
    )
    source_verdict = [row for row in source_audit if row.get("audit_id") == "SSA4467_4_source_silence_verdict"]
    add(
        "VAL4467_2_source_silence_not_signed",
        bool(source_verdict) and "CERTIFICATE_NOT_SIGNED" in str(source_verdict[0].get("evidence_status")),
        "source-silence certificate is explicitly not signed",
    )
    refinement_verdict = [row for row in refinement_rows_ if row.get("refinement_id") == "RC4467_5_refinement_verdict"]
    add(
        "VAL4467_3_refinement_certificate_not_signed",
        bool(refinement_verdict) and "CERTIFICATE_NOT_SIGNED" in str(refinement_verdict[0].get("current_status")),
        "refinement c_R2 certificate is explicitly not signed",
    )
    add(
        "VAL4467_4_rollup_selects_next_target",
        any("4468" in str(row.get("claim_effect")) or "4468" in str(row.get("items")) for row in rollup),
        "signed/unsigned rollup selects the 4468 exact parent-action normal-form target",
    )
    add(
        "VAL4467_5_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4467_1_parent_certificate" for row in gates),
        "claim gates keep local-GR/source-zero claims blocked",
    )
    add(
        "VAL4467_6_no_generated_claim_rows",
        all(str(row.get("valid_for_claim")).lower() == "false" for group in [sources, parent_rows, source_audit, refinement_rows_, rollup, gates, decisions, statuses, next_targets] for row in group),
        "all generated evidence rows are nonclaim/private",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            csv_detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover - validation report path
            csv_ok = False
            csv_detail.append(f"{path.name}:ERROR:{exc}")
    add("VAL4467_7_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4467_8_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4467_9_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-309",
    )
    add(
        "VAL4467_10_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add(
        "VAL4467_11_pycache_removed",
        not (SCRIPT_DIR / "__pycache__").exists(),
        "scripts __pycache__ absent after generation",
    )
    return rows


def main() -> None:
    sources = source_rows()
    parent_rows = parent_action_certificate_rows()
    source_audit = source_silence_audit_rows()
    refinement_rows_ = refinement_certificate_rows()
    rollup = rollup_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, parent_rows, source_audit, refinement_rows_, rollup)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_CERTIFICATE_CSV, parent_rows)
    write_csv(SOURCE_SILENCE_CSV, source_audit)
    write_csv(REFINEMENT_ZERO_CSV, refinement_rows_)
    write_csv(ROLLUP_CSV, rollup)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, parent_rows, source_audit, refinement_rows_, rollup, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, parent_rows, source_audit, refinement_rows_, rollup, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4467 Parent-Action Zero Certificate",
        "4467 separates the local-GR common-mode problem into two exact certificate doors: parent-owned source silence (`C_matter=0`) or parent-owned refinement/no-second-channel zero (`c_R2_eff=0`). Neither global certificate signs yet, so the finite common-mode scalar remains bound-only; the next target is the parent action normal form with no `A(chi)` and no second curvature-square channel.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4467 Packet Integration",
        "The private packet now records the coupling problem as a precise parent-action signature problem, not a vague missing piece. WEP closure and calibrated `G` cannot hide a common-mode scalar; either source silence or the `c_R2` zero selector must be derived, otherwise the finite branch must be bounded.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        PARENT_CERTIFICATE_CSV,
        SOURCE_SILENCE_CSV,
        REFINEMENT_ZERO_CSV,
        ROLLUP_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, parent_rows, source_audit, refinement_rows_, rollup, gates, decisions, statuses, next_targets, csv_paths)
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
