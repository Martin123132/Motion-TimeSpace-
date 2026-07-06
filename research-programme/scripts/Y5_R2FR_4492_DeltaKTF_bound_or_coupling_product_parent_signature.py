from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltak_bound_gate import (  # noqa: E402
    allowance_requirement_rows,
    bprime_leakage_bound_rows,
    claim_gate_rows,
    coupling_product_signature_rows,
    decision_ledger_rows,
    read_csv,
    write_csv,
    zero_theorem_audit_rows,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4492"
CLAIM_ID = "L-334"
MARKER = "PPC4161_DELTAKTF_BOUND_OR_COUPLING_PRODUCT_PARENT_SIGNATURE_4492"
PACKET_MARKER = "PPC4161_PACKET_DELTAKTF_BOUND_OR_COUPLING_PRODUCT_PARENT_SIGNATURE_4492"
DECISION = "DELTAKTF_EXACT_ZERO_FAILS_FOR_MATCHED_BRANCH_FINITE_BPRIME_BOUND_REQUIRED_NONCLAIM"
NEXT_TARGET = "4493-Y5-R2FR-Bprime-leakage-norm-computation-or-parent-projection-zero.md"

FORMAL_PATH = FORMAL / "508-PPC4161-DeltaKTF-bound-or-coupling-product-parent-signature.md"
DOC_PATH = POST / "4492-Y5-R2FR-DeltaKTF-bound-or-coupling-product-parent-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4492_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4492_SOURCE_REGISTER.csv"
ZERO_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_DELTAKTF_ZERO_THEOREM_AUDIT.csv"
BPRIME_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_BPRIME_LEAKAGE_BOUND.csv"
ALLOWANCE_REQ_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_ALLOWANCE_REQUIREMENTS.csv"
COUPLING_SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_COUPLING_PRODUCT_SIGNATURE.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4492_DECISION.csv"

FORMAL_507 = FORMAL / "507-PPC4161-transfer-bound-input-pack-or-coupling-zero-theorem.md"
ALLOWANCE_4491 = SOURCE_DIR / "P8_Y5_R2FR_4491_DELTAKTF_ALLOWANCE.csv"
ZERO_4491 = SOURCE_DIR / "P8_Y5_R2FR_4491_COUPLING_ZERO_AUDIT.csv"
LEAKAGE_4486 = SOURCE_DIR / "P8_Y5_R2FR_4486_DELTAKTF_LEAKAGE_INPUT_ROW.csv"
M2K2_4486 = SOURCE_DIR / "P8_Y5_R2FR_4486_FIRST_M2K2_INPUT_ROW.csv"
PROJECTION_3179 = SOURCE_DIR / "P8_Y5_R2FR_3179_HESSIAN_PROJECTION_DERIVATION.csv"
READOUT_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_HESSIAN_METRIC_READOUT.csv"
PROFILE_4489 = SOURCE_DIR / "P8_Y5_R2FR_4489_PROFILE_SELECTION_ROWS.csv"
GATE_PATH = SCRIPT_DIR / "deltak_bound_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4492_DeltaKTF_bound_or_coupling_product_parent_signature.py"

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
        ("SRC4492_00_formal507", FORMAL_507, "A_total_l2 <= |A_slip_surface| + |A_DeltaKTF_surface|", "4491 no-cancellation scorer handoff."),
        ("SRC4492_01_allowance4491", ALLOWANCE_4491, "DA4491_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09", "4491 DeltaKTF allowance rows."),
        ("SRC4492_02_zero4491", ZERO_4491, "Z4491_3_DeltaKTF", "4491 open DeltaKTF zero row."),
        ("SRC4492_03_leakage4486", LEAKAGE_4486, "DTF4486_1_Bprime_condition", "4486 Bprime leakage condition."),
        ("SRC4492_04_m2k24486", M2K2_4486, "M2I4486_3_recast_hessian_product_bound", "4486 projected Hessian product bound."),
        ("SRC4492_05_projection3179", PROJECTION_3179, "HP3179_1_auxiliary_B", "3179 Hessian projection and B(r) rewrite."),
        ("SRC4492_06_readout4487", READOUT_4487, "HMR4487_2_metric_null_verdict", "4487 metric-null verdict."),
        ("SRC4492_07_profile4489", PROFILE_4489, "PSEL4489_1_balanced_Fpp_jump", "4489 profile selection rows."),
        ("SRC4492_08_gate", GATE_PATH, "def bprime_leakage_bound_rows", "4492 bound helper."),
        ("SRC4492_09_generator", GENERATOR_PATH, 'CHECKPOINT = "4492"', "4492 generator script."),
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


def status_rows(bprime_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    smooth_1e9 = [
        row
        for row in bprime_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    smooth_1e11 = [
        row
        for row in bprime_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+11"
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "zero_theorem_result": "failed_for_profile_only_matched_branch",
            "smoothstep_1e9_required_CDeltaKTF_NBprime_max": smooth_1e9[0]["required_CDeltaKTF_times_NBprime_max"] if smooth_1e9 else "",
            "smoothstep_1e11_required_CDeltaKTF_NBprime_max": smooth_1e11[0]["required_CDeltaKTF_times_NBprime_max"] if smooth_1e11 else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "C_DeltaKTF_or_N_Bprime_or_parent_public_metric_projection_zero",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4492_0",
            "target": NEXT_TARGET,
            "objective": "Compute the actual profile leakage norm N_Bprime for the candidate finite profiles, or prove the parent public metric projection kills DeltaKTF before it reaches observables.",
            "derive_first": "parent projection/solder theorem C_DeltaKTF=0, or profile-level N_Bprime calculation from F(r)",
            "fallback": "source a conservative bound on C_DeltaKTF*N_Bprime and rerun the no-cancellation scorer",
            "risk": "promoting the local branch while DeltaKTF is merely assumed silent",
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
            "proof_result": "Bprime/profile-only exact zero route is rejected for a nonzero matched exterior; parent projection zero remains open but unsigned",
            "fallback_result": "DeltaKTF leakage is converted into numeric requirements on C_DeltaKTF*N_Bprime, with smoothstep 1e9 requiring <=1.376467175318575e-22",
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
        "domain": "local_gr_newton_r10_deltaKTF_source_coupling",
        "claim": "4492 rejects the profile-only DeltaKTF exact-zero route for a nonzero matched exterior and converts the surviving leakage branch into numeric no-cancellation requirements on C_DeltaKTF*N_Bprime.",
        "current_evidence": "4492 source register, DeltaKTF zero audit, Bprime leakage bounds, allowance requirements, coupling-product signature rows, claim gates, status and validation.",
        "status": "private_deltaKTF_bound_requirement_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "C_DeltaKTF, N_Bprime, parent projection/solder map and arena transfer coefficients remain unsigned.",
        "sector": "local_gr_newton_r10_deltaKTF_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "treating DeltaKTF silence as proven before either parent projection zero or finite Bprime leakage bound is derived",
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
    zero_rows: Sequence[Mapping[str, object]],
    bprime_rows: Sequence[Mapping[str, object]],
    requirements: Sequence[Mapping[str, object]],
    signatures: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 508 PPC4161 - DeltaKTF Bound Or Coupling Product Parent Signature

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4492 takes the live `DeltaKTF` problem head-on. The exact-zero attempt does **not** close from the matched profile alone:

```text
B(r) := (3/2) F(r) / r^2
F_core = A r^2       => B' = 0
F_ext  = C r^-3      => B' = -(15/2) C r^-6
```

So a nonzero exterior `r^-3` branch cannot make `B'=0` globally. The profile-only silence route is rejected unless the parent action proves that the public metric readout projects away the non-`Y_a` tensor footprint.

The useful movement is the fallback inequality:

```text
A_DeltaKTF_surface <= C_DeltaKTF * |s_K2*kappa_STF| * N_Bprime
C_DeltaKTF * N_Bprime <= remaining_A_DeltaKTF_allowance / |s_K2*kappa_STF|
```

That turns the next step into a real target. For the moderate smoothstep `|s_K2*kappa_STF|=1e9` cell, the required product is `1.376467175318575e-22`. For the smoothstep `1e11` cell, the no-cancellation allowance is already zero under the beta=1 tight J2 proxy, so no finite `DeltaKTF` leakage can rescue it.

This remains a private nonclaim. It is progress because the branch is no longer vague: either prove `C_DeltaKTF=0` from the parent public-metric projection, or compute/source `N_Bprime` and fit the inequality.

## DeltaKTF Zero Theorem Audit

{table(zero_rows)}

## Bprime Leakage Bound Rows

{table(bprime_rows)}

## Allowance Requirements

{table(requirements)}

## Coupling Product Signature

{table(signatures)}

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
    zero_rows: Sequence[Mapping[str, object]],
    bprime_rows: Sequence[Mapping[str, object]],
    requirements: Sequence[Mapping[str, object]],
    signatures: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4492 Y5/R2FR - DeltaKTF Bound Or Coupling Product Parent Signature

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4492 rejects the profile-only `DeltaKTF=0` route for a nonzero matched exterior and replaces it with hard target numbers. The live condition is now:

`C_DeltaKTF*N_Bprime <= allowance/|s_K2*kappa_STF|`.

## The Squeeze

{table(bprime_rows)}

## Zero Attempt And Signature Rows

{table(zero_rows)}

{table(signatures)}

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
    zero_rows: Sequence[Mapping[str, object]],
    bprime_rows: Sequence[Mapping[str, object]],
    requirements: Sequence[Mapping[str, object]],
    signatures: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    one_e9 = [
        row
        for row in bprime_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    one_e11 = [
        row
        for row in bprime_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+11"
    ]
    add("VAL4492_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4492_1_zero_theorem_rejected_for_matched_branch", any(row.get("status") == "EXACT_ZERO_NOT_PROVEN_FINITE_BOUND_REQUIRED" for row in zero_rows), "profile-only exact zero not claimed")
    add("VAL4492_2_bprime_bound_rows_written", len(bprime_rows) >= 4, f"{len(bprime_rows)} Bprime leakage rows")
    add("VAL4492_3_smoothstep_1e9_target_number", bool(one_e9) and one_e9[0].get("required_CDeltaKTF_times_NBprime_max") == "1.376467175318575e-22", "smoothstep 1e9 requires C_DeltaKTF*N_Bprime <= 1.376467175318575e-22")
    add("VAL4492_4_smoothstep_1e11_zero_allowance", bool(one_e11) and one_e11[0].get("required_CDeltaKTF_times_NBprime_max") == "0.000000000000000e+00", "smoothstep 1e11 has zero no-cancellation allowance")
    add("VAL4492_5_allowance_requirements_written", len(requirements) == len(bprime_rows), "one requirement row per bound row")
    add("VAL4492_6_signature_formula_written", any(row.get("status") == "FORMULA_DERIVED_NUMERIC_COEFFICIENTS_MISSING" for row in signatures), "coupling product bound formula derived")
    add("VAL4492_7_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4492_8_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4492_9_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add(
        "VAL4492_10_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, zero_rows, bprime_rows, requirements, signatures, ledger, gates, statuses, next_targets]
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
    add("VAL4492_11_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4492_12_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4492_13_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-334")
    add("VAL4492_14_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4492 markers")
    add("VAL4492_15_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    allowance_rows = read_csv(ALLOWANCE_4491)
    zero_rows = zero_theorem_audit_rows()
    bprime_rows = bprime_leakage_bound_rows(allowance_rows)
    requirements = allowance_requirement_rows(bprime_rows)
    signatures = coupling_product_signature_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, zero_rows, bprime_rows, requirements, signatures)
    statuses = status_rows(bprime_rows)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT_CSV, zero_rows)
    write_csv(BPRIME_BOUND_CSV, bprime_rows)
    write_csv(ALLOWANCE_REQ_CSV, requirements)
    write_csv(COUPLING_SIGNATURE_CSV, signatures)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, zero_rows, bprime_rows, requirements, signatures, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, zero_rows, bprime_rows, requirements, signatures, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4492 DeltaKTF Bound Or Coupling Product Parent Signature",
        "4492 rejects the profile-only `DeltaKTF=0` route for a nonzero matched exterior because `B(r)=(3/2)F/r^2` has `B'=0` in the quadratic core but `B'=-(15/2)C r^-6` in the exterior. It converts the surviving lane into the no-cancellation requirement `C_DeltaKTF*N_Bprime <= allowance/|s_K2*kappa_STF|`; the smoothstep `1e9` cell requires `<=1.376467175318575e-22`, while smoothstep `1e11` has zero allowance under the tight J2 proxy.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4492 Packet Integration",
        "The local branch now has a concrete `DeltaKTF` squeeze. The next best route is either a parent public-metric projection theorem giving `C_DeltaKTF=0`, or an actual `N_Bprime` computation from the profile families before any local-GR claim is allowed.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        ZERO_AUDIT_CSV,
        BPRIME_BOUND_CSV,
        ALLOWANCE_REQ_CSV,
        COUPLING_SIGNATURE_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, zero_rows, bprime_rows, requirements, signatures, ledger, gates, statuses, next_targets, csv_paths)
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
