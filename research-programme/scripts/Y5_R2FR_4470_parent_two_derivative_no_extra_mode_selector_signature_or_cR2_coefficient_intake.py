from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_selector_signature_gate import (  # noqa: E402
    claim_gate_rows,
    decision_rows as gate_decision_rows,
    derived_implication_rows,
    finite_coefficient_intake_request_rows,
    parent_selector_signature_audit_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4470"
CLAIM_ID = "L-312"
MARKER = "PPC4161_PARENT_TWO_DERIVATIVE_NO_EXTRA_MODE_SELECTOR_SIGNATURE_OR_CR2_INTAKE_4470"
PACKET_MARKER = "PPC4161_PACKET_PARENT_TWO_DERIVATIVE_NO_EXTRA_MODE_SELECTOR_SIGNATURE_OR_CR2_INTAKE_4470"
DECISION = "PARENT_SELECTOR_SIGNATURE_CONTRACT_COMPACTED_NOT_SIGNED_FINITE_CR2_INTAKE_REQUEST_STAGED_NONCLAIM"
NEXT_TARGET = "4471-Y5-R2FR-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"

FORMAL_PATH = FORMAL / "486-PPC4161-parent-two-derivative-no-extra-mode-selector-signature-or-cR2-coefficient-intake.md"
DOC_PATH = POST / "4470-Y5-R2FR-parent-two-derivative-no-extra-mode-selector-signature-or-cR2-coefficient-intake.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4470_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4470_SOURCE_REGISTER.csv"
SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_PARENT_SELECTOR_SIGNATURE_AUDIT.csv"
IMPLICATIONS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_DERIVED_IMPLICATIONS.csv"
INTAKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_FINITE_COEFFICIENT_INTAKE_REQUEST.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4470_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_selector_signature_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4470_parent_two_derivative_no_extra_mode_selector_signature_or_cR2_coefficient_intake.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4469 = SOURCE_DIR / "P8_Y5_R2FR_4469_NEXT_TARGET.csv"
FORMAL_485 = FORMAL / "485-PPC4161-second-curvature-channel-forbidden-or-finite-cR2-parent-coefficient-pack.md"
THEOREM_4469 = SOURCE_DIR / "P8_Y5_R2FR_4469_SECOND_ORDER_THEOREM_AUDIT.csv"
COEFFICIENT_4469 = SOURCE_DIR / "P8_Y5_R2FR_4469_FINITE_COEFFICIENT_PACK.csv"
FORMAL_196 = FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
POST_4459 = POST / "4459-Y5-R2FR-primitive-deficit-action-law-or-first-cR2-coefficient-owner-value.md"
FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
REFINEMENT_4460 = SOURCE_DIR / "P8_Y5_R2FR_4460_PARENT_REFINEMENT_SIGNATURE_CONTRACT.csv"
METRIC_SECOND_ORDER_SCRIPT = SCRIPT_DIR / "metric_only_second_order_sector_reduction_attempt.py"


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
            "source_id": "SRC4470_00_next4469",
            "ref": NEXT_4469,
            "needle": "4470-Y5-R2FR-parent-two-derivative-no-extra-mode-selector-signature",
            "role": "4469 selected the parent selector signature target.",
        },
        {
            "source_id": "SRC4470_01_formal485",
            "ref": FORMAL_485,
            "needle": "strict second-order/no-extra-mode local selector forbids",
            "role": "4469 writes the conditional second-order/no-extra-mode theorem.",
        },
        {
            "source_id": "SRC4470_02_theorem4469",
            "ref": THEOREM_4469,
            "needle": "SOT4469_0_strict_metric_second_order",
            "role": "machine-readable second-order selector theorem row.",
        },
        {
            "source_id": "SRC4470_03_coefficients4469",
            "ref": COEFFICIENT_4469,
            "needle": "FC4469_0_D0_scalar_basis",
            "role": "machine-readable finite coefficient pack still blocked.",
        },
        {
            "source_id": "SRC4470_04_action196",
            "ref": FORMAL_196,
            "needle": "EH/local metric principal block: hard root, not globally parent-derived",
            "role": "minimal parent action adoption matrix says EH origin is not globally parent-derived.",
        },
        {
            "source_id": "SRC4470_05_palatini_two_derivative",
            "ref": FORMAL_200,
            "needle": "leading low-energy/two-derivative order",
            "role": "two-derivative selector clause.",
        },
        {
            "source_id": "SRC4470_06_palatini_no_extra_modes",
            "ref": FORMAL_200,
            "needle": "no extra unscreened light modes",
            "role": "no extra unscreened modes selector clause.",
        },
        {
            "source_id": "SRC4470_07_palatini_unsigned",
            "ref": FORMAL_200,
            "needle": "selector_assumptions_parent_derived = false",
            "role": "selector is not yet parent-derived.",
        },
        {
            "source_id": "SRC4470_08_palatini_residual",
            "ref": FORMAL_200,
            "needle": "curvature squares -> coefficient",
            "role": "curvature-square residual coefficient remains active.",
        },
        {
            "source_id": "SRC4470_09_refinement4459",
            "ref": POST_4459,
            "needle": "S_n(delta)=n Phi(delta/n)",
            "role": "same-channel refinement linearity theorem.",
        },
        {
            "source_id": "SRC4470_10_owner4461",
            "ref": FORMAL_477,
            "needle": "OCT4461_4_refinement_linearity",
            "role": "owner compatibility row for refinement linearity.",
        },
        {
            "source_id": "SRC4470_11_scalaron4461",
            "ref": FORMAL_477,
            "needle": "SM4461_1_c2_to_cR2",
            "role": "c2 to c_R2_eff finite map.",
        },
        {
            "source_id": "SRC4470_12_refinement_contract",
            "ref": REFINEMENT_4460,
            "needle": "RGC4460_5_no_second_channel",
            "role": "no-second-channel clause remains open.",
        },
        {
            "source_id": "SRC4470_13_metric_second_order_script",
            "ref": METRIC_SECOND_ORDER_SCRIPT,
            "needle": "no parent theorem forbids R2/fR/Ricci/Weyl/nonlocal operators",
            "role": "previous script states the missing parent theorem explicitly.",
        },
        {
            "source_id": "SRC4470_14_gate",
            "ref": GATE_PATH,
            "needle": "def parent_selector_signature_audit_rows",
            "role": "4470 selector signature gate.",
        },
        {
            "source_id": "SRC4470_15_generator",
            "ref": GENERATOR_PATH,
            "needle": 'CHECKPOINT = "4470"',
            "role": "4470 generator script.",
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
            "selector_signature_result": "exact parent-selector contract compacted into six clauses plus verdict",
            "parent_status": "not parent-signed; no-grain and no-auxiliary clauses remain decisive open routes",
            "conditional_zero_result": "if all clauses sign, D0=D2=c_R2_eff=C_metric_pole=C_hidden_source=0 in the local branch",
            "fallback_result": "finite c_R2/C_total intake request rows staged with MISSING markers and no claim promotion",
            "local_GR_claim": False,
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
            "selector_contract_status": "compacted",
            "parent_signature_status": "not_signed",
            "sharpest_open_clause": "no_local_length_scale_or_grain",
            "finite_intake_status": "staged_nonclaim_missing_parent_inputs",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4470_0",
            "target": NEXT_TARGET,
            "objective": "Try to prove no physical local length/grain/cutoff can survive in the tested local vacuum branch; if that fails, source the first c_R2_eff intake row.",
            "derive_first": "show parent local action has no dimensionful grain slot capable of multiplying a quadratic curvature response",
            "fallback": "create first source-ready c2_visible/ell_cell/xi_shape/N_EH row with valid_for_claim=false",
            "risk": "mistaking continuum coarse-graining or low-energy truncation for an exact parent no-grain theorem",
            "valid_for_claim": False,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body}\n"
    write_text(path, current.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_newton_r10_scalar_source_coupling",
            "claim": "4470 compacts the local-GR route into an explicit parent selector signature contract: if object-language, refinement-linearity, no-grain, no-auxiliary, connection-resolution and no-extra-mode clauses all sign, the local branch reduces to EH plus Lambda/topological/boundary terms and finite c_R2 scalar channels vanish.",
            "current_evidence": "4470 source register, parent selector signature audit, derived implications, finite coefficient intake request, claim gates, decision/status/next CSVs and validation.",
            "status": "private_nonclaim_checkpoint",
            "next_test": NEXT_TARGET,
            "key_risk": "using a compact selector contract as if the parent had already signed no-grain and no-auxiliary clauses.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "finite c_R2_eff/C_total survives unless no local grain and no hidden auxiliary integration are parent-derived",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    signature_rows: Sequence[Mapping[str, object]],
    implications: Sequence[Mapping[str, object]],
    intake: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 486 PPC4161 - Parent Two-Derivative No-Extra-Mode Selector Signature Or `c_R2` Coefficient Intake

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4470 takes the local-GR route forward by compressing the problem into a finite parent-signature contract.

If MTS parent-signs the local object language, first-order refinement linearity, no physical local grain/length, no auxiliary integration, connection resolution and no extra unscreened modes, then the local branch has only `S_EH + Lambda + topological/boundary` geometry. In that case `D0=0`, `D2=0`, `c_R2_eff=0`, `C_metric_pole=0`, `C_hidden_source=0`, and the finite R10 scalar branch is inactive.

The contract is not signed today. The decisive open clause is the no-local-length/no-grain theorem: without a surviving local length, `c_R2_eff` cannot be built from a quadratic grain response; with one, it must be source-backed and bounded. So 4470 does not claim local GR, but it gives the next exact target rather than circling the whole problem.

## Parent Selector Signature Audit

{table(signature_rows)}

## Derived Implications

{table(implications)}

## Finite Coefficient Intake Request

{table(intake)}

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
    signature_rows: Sequence[Mapping[str, object]],
    implications: Sequence[Mapping[str, object]],
    intake: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4470 Y5/R2FR - Parent Two-Derivative No-Extra-Mode Selector Signature Or `c_R2` Coefficient Intake

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

The local-GR problem is no longer one giant fog bank. 4470 turns it into a signed-contract problem: either prove the parent has no local grain/auxiliary second channel, or stop pretending the scalar branch is gone and fill finite `c_R2_eff/C_total` rows.

## Selector Signature Audit

{table(signature_rows)}

## Conditional Implications

{table(implications)}

## Finite Intake Fallback

{table(intake)}

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
    signature_rows: Sequence[Mapping[str, object]],
    implications: Sequence[Mapping[str, object]],
    intake: Sequence[Mapping[str, object]],
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
        "VAL4470_0_sources_exist_and_needles_found",
        all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
        "every cited source path exists and its needle is found",
    )
    add(
        "VAL4470_1_signature_contract_written",
        any(row.get("clause_id") == "SIG4470_6_signature_verdict" for row in signature_rows),
        "selector signature verdict row exists",
    )
    add(
        "VAL4470_2_parent_signature_not_overclaimed",
        all(row.get("parent_signed") is False for row in signature_rows),
        "all selector clauses remain unsigned unless parent proof exists",
    )
    add(
        "VAL4470_3_decisive_no_grain_clause_present",
        any(row.get("clause_id") == "SIG4470_2_no_local_length_scale_or_grain" for row in signature_rows),
        "no-local-length/no-grain clause is explicit",
    )
    add(
        "VAL4470_4_conditional_zero_implications_present",
        all(any(row.get("derived_law", "").startswith(prefix) for row in implications) for prefix in ["D0=0", "c_R2_eff=0", "C_metric_pole=0"]),
        "conditional D0/c_R2/C-metric-pole zero implications exist",
    )
    add(
        "VAL4470_5_finite_intake_has_missing_markers",
        any("MISSING" in str(row.get("source_request")) for row in intake) and all(row.get("valid_for_claim") is False for row in intake),
        "finite intake remains source-request/nonclaim with missing markers",
    )
    add(
        "VAL4470_6_claim_gates_block_local_GR",
        all(str(row.get("claim_allowed")).lower() == "false" for row in gates)
        and any(row.get("gate_id") == "CG4470_2_all_signature_clauses_parent_signed" and str(row.get("gate_pass")).lower() == "false" for row in gates),
        "claim gates block local-GR scalar closure",
    )
    add(
        "VAL4470_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, signature_rows, implications, intake, gates, decisions, statuses, next_targets]
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
    add("VAL4470_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4470_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add(
        "VAL4470_10_claim_register_updated",
        any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)),
        "claims register contains L-312",
    )
    add(
        "VAL4470_11_next_target_selected",
        bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4470_12_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    signature_rows = parent_selector_signature_audit_rows()
    implications = derived_implication_rows()
    intake = finite_coefficient_intake_request_rows()
    ledger = gate_decision_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, signature_rows, implications, intake)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SIGNATURE_CSV, signature_rows)
    write_csv(IMPLICATIONS_CSV, implications)
    write_csv(INTAKE_CSV, intake)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, signature_rows, implications, intake, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, signature_rows, implications, intake, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4470 Parent Selector Signature Contract",
        "4470 turns the local-GR reduction into a compact parent-signature contract. If MTS signs local object language, refinement-linearity, no local grain/length, no auxiliary integration, connection resolution and no extra unscreened modes, the local branch reduces to EH plus Lambda/topological/boundary terms and `D0`, `D2`, `c_R2_eff`, `C_metric_pole` and `C_hidden_source` vanish. The contract is not signed today; the next decisive target is the no-local-length/no-grain clause.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4470 Packet Integration",
        "The private packet now records the exact local-GR fork: either prove the parent has no surviving local grain/length or auxiliary second channel, or source finite `D0/D2/c_R2_eff/C_total` rows before R10/PPN/local-GR scoring. No public local-GR claim is created by this checkpoint.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        SIGNATURE_CSV,
        IMPLICATIONS_CSV,
        INTAKE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, signature_rows, implications, intake, gates, decisions, statuses, next_targets, csv_paths)
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
