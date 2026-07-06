from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bprime_leakage_norm_gate import (  # noqa: E402
    bprime_norm_rows,
    claim_gate_rows,
    decision_ledger_rows,
    deltak_requirement_scorer_rows,
    parent_projection_audit_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4493"
CLAIM_ID = "L-335"
MARKER = "PPC4161_BPRIME_LEAKAGE_NORM_COMPUTATION_OR_PARENT_PROJECTION_ZERO_4493"
PACKET_MARKER = "PPC4161_PACKET_BPRIME_LEAKAGE_NORM_COMPUTATION_OR_PARENT_PROJECTION_ZERO_4493"
DECISION = "BPRIME_PROFILE_NORMS_ORDER_UNITY_PARENT_PROJECTION_ZERO_OR_TINY_CDELTA_REQUIRED_NONCLAIM"
NEXT_TARGET = "4494-Y5-R2FR-parent-public-metric-projection-CDeltaKTF-zero-or-local-branch-demotion.md"

FORMAL_PATH = FORMAL / "509-PPC4161-Bprime-leakage-norm-computation-or-parent-projection-zero.md"
DOC_PATH = POST / "4493-Y5-R2FR-Bprime-leakage-norm-computation-or-parent-projection-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4493_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4493_SOURCE_REGISTER.csv"
BPRIME_NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_BPRIME_PROFILE_NORMS.csv"
DELTAK_SCORER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_DELTAKTF_REQUIREMENT_SCORER.csv"
PARENT_PROJECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_PARENT_PROJECTION_AUDIT.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4493_DECISION.csv"

FORMAL_508 = FORMAL / "508-PPC4161-DeltaKTF-bound-or-coupling-product-parent-signature.md"
BPRIME_4492 = SOURCE_DIR / "P8_Y5_R2FR_4492_BPRIME_LEAKAGE_BOUND.csv"
PROFILE_4489 = SOURCE_DIR / "P8_Y5_R2FR_4489_PROFILE_SELECTION_ROWS.csv"
SCRIPT_3192 = SCRIPT_DIR / "Y5_R2FR_3192_solve_quadratic_profile_EL_or_upgrade_slip_transfer_bound.py"
PROJECTION_3179 = SOURCE_DIR / "P8_Y5_R2FR_3179_HESSIAN_PROJECTION_DERIVATION.csv"
READOUT_4487 = SOURCE_DIR / "P8_Y5_R2FR_4487_HESSIAN_METRIC_READOUT.csv"
GATE_PATH = SCRIPT_DIR / "bprime_leakage_norm_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4493_Bprime_leakage_norm_computation_or_parent_projection_zero.py"

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
        ("SRC4493_00_formal508", FORMAL_508, "C_DeltaKTF * N_Bprime <=", "4492 inequality and next target."),
        ("SRC4493_01_bprime4492", BPRIME_4492, "BP4492_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09", "4492 finite leakage requirement rows."),
        ("SRC4493_02_profile4489", PROFILE_4489, "PSEL4489_1_balanced_Fpp_jump", "4489 active profile rows."),
        ("SRC4493_03_script3192", SCRIPT_3192, "def stationary_coefficients", "3192 exact-EL profile coefficients."),
        ("SRC4493_04_projection3179", PROJECTION_3179, "B(r):=(3/2)F(r)/r^2", "3179 B rewrite."),
        ("SRC4493_05_readout4487", READOUT_4487, "METRIC_NULL_FAILS_ON_IDENTITY_READOUT", "4487 public metric readout warning."),
        ("SRC4493_06_gate", GATE_PATH, "def profile_norm", "4493 profile norm helper."),
        ("SRC4493_07_generator", GENERATOR_PATH, 'CHECKPOINT = "4493"', "4493 generator script."),
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


def status_rows(norm_rows: Sequence[Mapping[str, object]], score_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    smooth_1e9 = [
        row
        for row in score_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    best_norm = min(norm_rows, key=lambda row: float(row["N_Bprime_gate"]))
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "best_profile_by_N_Bprime_gate": best_norm["profile_id"],
            "best_N_Bprime_gate": best_norm["N_Bprime_gate"],
            "smoothstep_1e9_required_CDeltaKTF_max": smooth_1e9[0]["required_CDeltaKTF_max_given_profile_norm"] if smooth_1e9 else "",
            "local_GR_claim": False,
            "sharpest_open_clause": "prove_C_DeltaKTF_zero_or_derive_tiny_parent_readout_coefficient",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4493_0",
            "target": NEXT_TARGET,
            "objective": "Attack the parent public-metric projection map: prove the non-Y_a Hessian footprint is vertical/gauge/improvement silent, or demote the local branch to a finite-coefficient closure requiring a tiny C_DeltaKTF.",
            "derive_first": "C_DeltaKTF=0 theorem from parent readout/solder map",
            "fallback": "derive a nonzero C_DeltaKTF and rerun the scorer; if it is not tiny enough, local branch stays closure-only",
            "risk": "continuing profile tuning despite order-unity Bprime leakage norms",
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
            "proof_result": "profile-only Bprime leakage suppression is not enough; active candidate norms are order unity or larger",
            "fallback_result": "finite route now requires a parent-owned C_DeltaKTF at roughly the 1e-23 scale for the smoothstep 1e9 row, or exact C_DeltaKTF=0",
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
        "domain": "local_gr_newton_r10_deltaKTF_profile_leakage",
        "claim": "4493 computes actual Bprime leakage norms for the active profile cells and shows profile shaping alone does not suppress DeltaKTF enough; parent projection zero or a tiny C_DeltaKTF is required.",
        "current_evidence": "4493 source register, Bprime profile norm rows, DeltaKTF requirement scorer, parent projection audit, claim gates, status and validation.",
        "status": "private_profile_norm_squeeze_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "assuming DeltaKTF public-metric silence without a parent projection theorem or numeric C_DeltaKTF.",
        "sector": "local_gr_newton_r10_deltaKTF_profile_leakage",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "profile-only suppression is order unity, so local-GR closure now depends on the parent public metric map",
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
    norm_rows: Sequence[Mapping[str, object]],
    score_rows: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 509 PPC4161 - Bprime Leakage Norm Computation Or Parent Projection Zero

Private checkpoint: `{CHECKPOINT}`
Marker: `{MARKER}`
Decision: `{DECISION}`
Generated UTC: `{STAMP}`

## Result

4493 computes the actual profile-side leakage norm instead of leaving `N_Bprime` as a symbol.

The definition used here is:

```text
B(x) = (3/2) F(x) / x^2
N_Bprime measures |x B'(x)| across the transition collar plus the analytic r^-3 exterior tail.
```

This closes one escape hatch: the active profile families do **not** make `DeltaKTF` tiny by themselves. The balanced exact-EL branch is the best of the tested rows, but its `N_Bprime_gate` is still order unity. The min-`N4` exact branch is bad for this channel because pushing the left edge close to zero creates a large `B'` spike.

So the route now narrows sharply:

```text
A_DeltaKTF_surface <= C_DeltaKTF |s_K2*kappa_STF| N_Bprime
```

With actual `N_Bprime` inserted, the moderate smoothstep `|s_K2*kappa_STF|=1e9` row already needs a parent-owned `C_DeltaKTF` at roughly the `1e-23` scale. That is not something profile smoothing can honestly provide. The serious route is now to derive `C_DeltaKTF=0` from the parent public-metric projection/solder map, or explicitly demote this local branch to closure-only.

## Bprime Profile Norms

{table(norm_rows)}

## DeltaKTF Requirement Scorer

{table(score_rows)}

## Parent Projection Audit

{table(parent_rows)}

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
    norm_rows: Sequence[Mapping[str, object]],
    score_rows: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4493 Y5/R2FR - Bprime Leakage Norm Computation Or Parent Projection Zero

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4493 turns `N_Bprime` into computed rows. The answer is not profile magic: the norms are order unity or larger, so the route must now be parent projection zero or a very tiny parent readout coefficient.

## Norms And Scorer

{table(norm_rows)}

{table(score_rows)}

## Projection Route

{table(parent_rows)}

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
    norm_rows: Sequence[Mapping[str, object]],
    score_rows: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
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
        for row in score_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    balanced = [row for row in norm_rows if row.get("profile_id") == "PSEL4489_1_balanced_Fpp_jump"]
    add("VAL4493_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4493_1_norm_rows_written", len(norm_rows) >= 3 and all(float(row["N_Bprime_gate"]) > 0.0 for row in norm_rows), f"{len(norm_rows)} norm rows")
    add("VAL4493_2_balanced_norm_order_unity", bool(balanced) and 1.0 < float(balanced[0]["N_Bprime_gate"]) < 2.0, "balanced exact-EL Bprime gate norm is order unity")
    add("VAL4493_3_smoothstep_1e9_Cdelta_bound_tiny", bool(smooth_1e9) and float(smooth_1e9[0]["required_CDeltaKTF_max_given_profile_norm"]) < 4.0e-23, "smoothstep 1e9 requires C_DeltaKTF below 4e-23")
    add("VAL4493_4_no_unit_Cdelta_pass", all(str(row.get("pass_if_CDeltaKTF_equals_one")).lower() == "false" for row in score_rows), "unit C_DeltaKTF fails every finite row")
    add("VAL4493_5_parent_projection_audit_written", len(parent_rows) >= 3 and any(row.get("verdict") == "OPEN_NOT_PROVEN" for row in parent_rows), "parent projection route remains open but unproven")
    add("VAL4493_6_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4493_7_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4493_8_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET and bool(ledger), NEXT_TARGET)
    add(
        "VAL4493_9_all_generated_rows_nonclaim",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, norm_rows, score_rows, parent_rows, ledger, gates, statuses, next_targets]
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
    add("VAL4493_10_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4493_11_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4493_12_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-335")
    add("VAL4493_13_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4493 markers")
    add("VAL4493_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    norm_rows = bprime_norm_rows(read_csv(PROFILE_4489))
    score_rows = deltak_requirement_scorer_rows(read_csv(BPRIME_4492), norm_rows)
    parent_rows = parent_projection_audit_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, norm_rows, score_rows, parent_rows)
    statuses = status_rows(norm_rows, score_rows)
    next_targets = next_rows()
    decisions = decision_row()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BPRIME_NORM_CSV, norm_rows)
    write_csv(DELTAK_SCORER_CSV, score_rows)
    write_csv(PARENT_PROJECTION_CSV, parent_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)
    write_csv(DECISION_CSV, decisions)

    write_text(FORMAL_PATH, formal_body(sources, norm_rows, score_rows, parent_rows, ledger, gates, statuses, next_targets, decisions))
    write_text(DOC_PATH, post_body(sources, norm_rows, score_rows, parent_rows, ledger, gates, statuses, next_targets, decisions))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4493 Bprime Leakage Norm Computation Or Parent Projection Zero",
        "4493 computes `N_Bprime` for the active profile cells using `B=(3/2)F/x^2` and `|xB'|` across the transition collar plus the analytic `r^-3` exterior tail. The profile norms are order unity or larger, so profile shaping alone cannot close `DeltaKTF`; the moderate smoothstep `1e9` row now requires a parent readout coefficient `C_DeltaKTF` below the `1e-23` scale, or an exact parent projection zero.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4493 Packet Integration",
        "The local branch has reached the projection fork. Since computed `Bprime` leakage is not tiny, 4494 should prove `C_DeltaKTF=0` from the parent public-metric projection/solder map or explicitly demote the branch to closure-only unless a tiny nonzero `C_DeltaKTF` is derived.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        BPRIME_NORM_CSV,
        DELTAK_SCORER_CSV,
        PARENT_PROJECTION_CSV,
        DECISION_LEDGER_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    validations = validate(sources, norm_rows, score_rows, parent_rows, ledger, gates, statuses, next_targets, csv_paths)
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
