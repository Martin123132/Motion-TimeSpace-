from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_normal_form_noAchi_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    finite_scalar_pack_rows,
    no_Achi_proof_rows,
    no_second_channel_rows,
    parent_normal_form_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4468"
CLAIM_ID = "L-310"
MARKER = "PPC4161_PARENT_ACTION_NORMAL_FORM_NO_ACHI_NO_SECOND_CHANNEL_4468"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_NORMAL_FORM_NO_ACHI_NO_SECOND_CHANNEL_4468"
DECISION = "PARENT_ACTION_NORMAL_FORM_NO_ACHI_PRIVATE_SELECTOR_SIGNED_SECOND_CHANNEL_UNSIGNED_FINITE_SCALAR_RETAINED_NONCLAIM"
NEXT_TARGET = "4469-Y5-R2FR-second-curvature-channel-forbidden-or-finite-cR2-parent-coefficient-pack.md"

FORMAL_PATH = FORMAL / "484-PPC4161-parent-action-normal-form-no-Achi-no-second-channel.md"
DOC_PATH = POST / "4468-Y5-R2FR-parent-action-normal-form-no-Achi-no-second-channel-proof-or-finite-scalar-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4468_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4468_SOURCE_REGISTER.csv"
NORMAL_FORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_PARENT_NORMAL_FORM_AUDIT.csv"
NO_ACHI_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_NO_ACHI_PROOF.csv"
NO_SECOND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_NO_SECOND_CHANNEL_AUDIT.csv"
FINITE_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_FINITE_SCALAR_PACK.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4468_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_normal_form_noAchi_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4468_parent_action_normal_form_no_Achi_no_second_channel.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4467 = SOURCE_DIR / "P8_Y5_R2FR_4467_NEXT_TARGET.csv"
FORMAL_483 = FORMAL / "483-PPC4161-parent-action-source-silence-or-refinement-cR2-zero-certificate.md"
FORMAL_190 = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
FORMAL_196 = FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md"
FORMAL_185 = FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_201 = FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md"
POST_4459 = POST / "4459-Y5-R2FR-primitive-deficit-action-law-or-first-cR2-coefficient-owner-value.md"
FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
SCALARON_4461 = SOURCE_DIR / "P8_Y5_R2FR_4461_C2_SCALARON_OBSERVABLE_MAP.csv"
R10_PRESSURE_4466 = SOURCE_DIR / "P8_Y5_R2FR_4466_R10_PRESSURE_EVALUATION.csv"
PARENT_CERT_4467 = SOURCE_DIR / "P8_Y5_R2FR_4467_PARENT_ACTION_CERTIFICATE.csv"


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
            "source_id": "SRC4468_00_next4467",
            "ref": NEXT_4467,
            "needle": "4468-Y5-R2FR-parent-action-normal-form",
            "role": "4467 selected the no-Achi/no-second-channel normal-form target.",
        },
        {
            "source_id": "SRC4468_01_formal483",
            "ref": FORMAL_483,
            "needle": "no `A(chi)`, no `theta_j(chi)`",
            "role": "4467 proof contract requiring both source silence and no second channel.",
        },
        {
            "source_id": "SRC4468_02_selector190",
            "ref": FORMAL_190,
            "needle": "S_parent|loc =",
            "role": "parent action selector local normal form.",
        },
        {
            "source_id": "SRC4468_03_minimal196",
            "ref": FORMAL_196,
            "needle": "S_min|loc =",
            "role": "minimal local parent-action candidate grammar.",
        },
        {
            "source_id": "SRC4468_04_hilbert185",
            "ref": FORMAL_185,
            "needle": "Independent source weights are not admitted",
            "role": "Hilbert source-measure descent excludes explicit source weights inside the private packet.",
        },
        {
            "source_id": "SRC4468_05_quotient193",
            "ref": FORMAL_193,
            "needle": "delta_v S_matter",
            "role": "quotient-natural chain-rule matter silence theorem.",
        },
        {
            "source_id": "SRC4468_06_palatini200",
            "ref": FORMAL_200,
            "needle": "curvature squares -> coefficient",
            "role": "Palatini selector retains curvature-square residuals unless separately zero/bounded.",
        },
        {
            "source_id": "SRC4468_07_residual201",
            "ref": FORMAL_201,
            "needle": "c_R2 or M_R curvature-square finite-range tail",
            "role": "residual coefficient map keeps c_R2/M_R live.",
        },
        {
            "source_id": "SRC4468_08_refinement4459",
            "ref": POST_4459,
            "needle": "separate second channel",
            "role": "4459 exact same-channel linearity theorem leaves separate channels legal.",
        },
        {
            "source_id": "SRC4468_09_scalaron_formal477",
            "ref": FORMAL_477,
            "needle": "SM4461_3_scalar_coupling",
            "role": "finite scalaron map with alpha_eff=C_matter^2/3.",
        },
        {
            "source_id": "SRC4468_10_scalaron_csv4461",
            "ref": SCALARON_4461,
            "needle": "SM4461_3_scalar_coupling",
            "role": "machine-readable scalar coupling row.",
        },
        {
            "source_id": "SRC4468_11_r10pressure4466",
            "ref": R10_PRESSURE_4466,
            "needle": "R10P4466_0_current_lambda_pressure",
            "role": "current R10 pressure values for universal metric scalar.",
        },
        {
            "source_id": "SRC4468_12_parentcert4467",
            "ref": PARENT_CERT_4467,
            "needle": "PAC4467_4_refinement_cR2_zero",
            "role": "4467 certificate requiring refinement/no-second-channel signature.",
        },
        {
            "source_id": "SRC4468_13_gate",
            "ref": GATE_PATH,
            "needle": "def parent_normal_form_rows",
            "role": "4468 no-Achi/no-second-channel gate.",
        },
        {
            "source_id": "SRC4468_14_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4468"',
            "role": "4468 generator script.",
        },
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["ref"])
        needle = str(spec["needle"])
        line_number = line_of(source_path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(source_path),
                "local_path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": line_number > 0,
                "line_number": line_number,
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
            "no_Achi_result": "explicit A(chi) matter-frame factor is untypeable inside the private PPC4161 selector grammar",
            "coupling_split_result": "no-Achi kills only C_explicit_Achi; a finite metric scalaron can still carry C_metric_pole",
            "no_second_channel_result": "curvature-square/trace-norm/hidden scalar channels are not globally forbidden",
            "finite_scalar_result": "finite scalar pack remains bound-only; universal metric scalar still fails review-candidate R10 pressure",
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
            "no_Achi_status": "private_selector_branch_signed_not_global",
            "metric_scalaron_status": "retained_if_cR2_eff_finite",
            "no_second_channel_status": "unsigned",
            "finite_scalar_status": "pack_staged_bound_only",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4468_0",
            "target": NEXT_TARGET,
            "objective": "Try to forbid the second curvature/scalar channel from the parent grammar; if that fails, fill the finite c_R2_eff/C_total coefficient pack.",
            "derive_first": "prove refinement/no-second-channel forbids R2, Ricci2, Weyl2, trace/norm holonomy, hidden scalar, marker and grain channels",
            "fallback": "finite parent coefficient pack: c_R2_eff, D0/D2, C_total, live alpha(lambda), PPN/lightcone projection",
            "risk": "treating no explicit A(chi) as no scalar force while a metric scalaron remains live",
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
        "claim": "4468 separates explicit matter-frame A(chi) from metric scalaron coupling: no-Achi is signed inside the private selector grammar, but the second curvature channel is still unsigned, so the finite scalar branch remains bound-only.",
        "current_evidence": "4468 source register, parent normal-form audit, no-Achi proof, no-second-channel audit, finite scalar pack, claim gates, decision/status/next CSVs and validation.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "mistaking the absence of an explicit A(chi) matter factor for absence of a metric scalar fifth force.",
        "sector": "local_gr_newton_r10_scalar_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "finite c_R2_eff/C_total survives until no-second-channel or source-backed coefficients close",
    }
    rows.append({fieldname: claim_row.get(fieldname, "") for fieldname in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current_text = text(path)
    if marker in current_text:
        return
    section = f"\n\n<!-- {marker} -->\n## {title}\n\n{body.strip()}\n"
    write_text(path, current_text.rstrip() + section)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    normal_rows: Sequence[Mapping[str, object]],
    no_Achi_rows: Sequence[Mapping[str, object]],
    second_rows: Sequence[Mapping[str, object]],
    finite_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 484 PPC4161 — Parent Action Normal Form: No `A(chi)` Versus No Second Channel

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4468 makes the useful leap and the necessary guard at the same time:

1. Inside the private PPC4161 selector grammar, ordinary matter is typed as `S_matter[psi,g_obs(q),theta(q)]`. An independent matter-frame factor `A(chi)^2 g_obs` is not a legal argument there. So the explicit matter-frame coupling `C_explicit_Achi` is zero in that private branch.
2. That does **not** kill a metric scalaron. If a curvature-square/second-channel scalar survives in the geometry sector, it can still couple through the metric trace. Therefore the true scalar coupling is split as `C_total = C_explicit_Achi + C_metric_pole + C_hidden_source`.
3. The no-second-channel certificate does not sign today. The current corpus still allows curvature-square EFT terms, trace/norm holonomy costs, hidden scalar/marker/grain channels, or finite `c_R2_eff` unless separately forbidden or sourced.

So the work has moved: the explicit `A(chi)` door is branch-locally shut, but the metric-pole door is still open. Local GR is not claimed; the next target is the second-channel theorem or a finite coefficient pack.

## Parent Normal Form Audit

{table(normal_rows)}

## No `A(chi)` Proof

{table(no_Achi_rows)}

## No Second Channel Audit

{table(second_rows)}

## Finite Scalar Pack

{table(finite_rows)}

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
    normal_rows: Sequence[Mapping[str, object]],
    no_Achi_rows: Sequence[Mapping[str, object]],
    second_rows: Sequence[Mapping[str, object]],
    finite_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4468 Y5/R2FR — Parent Action Normal Form: No `A(chi)` Or Finite Scalar Pack

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Changed

This is the anti-circling step: the coupling split is now explicit. The private selector really does forbid an explicit independent `A(chi)` matter-frame factor. But that is not the same as forbidding a metric scalaron from a finite curvature-square channel.

## Normal Form

{table(normal_rows)}

## No `A(chi)`

{table(no_Achi_rows)}

## No Second Channel

{table(second_rows)}

## Finite Scalar Pack

{table(finite_rows)}

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
    normal_rows: Sequence[Mapping[str, object]],
    no_Achi_rows: Sequence[Mapping[str, object]],
    second_rows: Sequence[Mapping[str, object]],
    finite_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
            }
        )

    add(
        "VAL4468_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4468_1_private_no_Achi_signed",
        any(row.get("normal_form_id") == "NF4468_0_private_selector_grammar" and row.get("signed_in_private_selector") is True for row in normal_rows),
        "explicit A(chi) is forbidden inside the private selector grammar",
    )
    add(
        "VAL4468_2_global_no_Achi_not_promoted",
        all(str(row.get("global_parent_signed")).lower() == "false" for row in normal_rows),
        "no normal-form row is promoted as global parent-signed",
    )
    add(
        "VAL4468_3_coupling_split_written",
        any(row.get("proof_id") == "NA4468_3_coupling_split" for row in no_Achi_rows),
        "C_total split prevents no-Achi/scalaron conflation",
    )
    add(
        "VAL4468_4_no_second_channel_unsigned",
        any(row.get("channel_id") == "SC4468_4_verdict" and row.get("current_status") == "NOT_SIGNED" for row in second_rows),
        "no-second-channel verdict remains unsigned",
    )
    add(
        "VAL4468_5_finite_pack_blocked",
        any(row.get("pack_id") == "FSP4468_0_required_scalar_pack" and "MISSING" in str(row.get("current_value")) for row in finite_rows),
        "finite scalar pack keeps missing parent coefficient blocker",
    )
    add(
        "VAL4468_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4468_3_local_GR_scalar_closure" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR scalar closure",
    )
    add(
        "VAL4468_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, normal_rows, no_Achi_rows, second_rows, finite_rows, gates, decisions, statuses, next_targets]
            for row in group
        ),
        "all generated rows remain private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4468_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4468_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4468_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-310",
    )
    add(
        "VAL4468_11_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4468_12_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    normal_rows = parent_normal_form_rows()
    no_Achi_rows = no_Achi_proof_rows()
    second_rows = no_second_channel_rows()
    finite_rows = finite_scalar_pack_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, normal_rows, no_Achi_rows, second_rows, finite_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NORMAL_FORM_CSV, normal_rows)
    write_csv(NO_ACHI_CSV, no_Achi_rows)
    write_csv(NO_SECOND_CSV, second_rows)
    write_csv(FINITE_PACK_CSV, finite_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, normal_rows, no_Achi_rows, second_rows, finite_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, normal_rows, no_Achi_rows, second_rows, finite_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4468 No-Achi Versus Metric Scalaron Split",
        "4468 proves a useful private-branch point: the PPC4161 selector grammar forbids an explicit independent matter-frame `A(chi)` factor, so `C_explicit_Achi=0` in that branch. It also adds the necessary guard: this does not kill a metric scalaron from finite `c_R2_eff`; the second curvature/scalar channel remains unsigned and the finite scalar pack stays bound-only.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4468 Packet Integration",
        "The private packet now separates explicit matter-frame coupling from metric-pole coupling. This avoids the false win where no `A(chi)` is mistaken for no fifth force. The next exact target is to forbid the second curvature/scalar channel or fill finite `c_R2_eff`, `C_total`, live R10 and PPN projection rows.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        NORMAL_FORM_CSV,
        NO_ACHI_CSV,
        NO_SECOND_CSV,
        FINITE_PACK_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, normal_rows, no_Achi_rows, second_rows, finite_rows, gates, decisions, statuses, next_targets, csv_paths)
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
