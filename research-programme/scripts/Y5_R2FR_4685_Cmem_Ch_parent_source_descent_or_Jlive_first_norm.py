from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4685"
CLAIM_ID = "L-527"
MARKER = "PPC4161_CMEM_CH_QBASIC_SOURCE_DESCENT_CURRENT_BRANCH_4685"
PACKET_MARKER = "PPC4161_PACKET_CMEM_CH_QBASIC_SOURCE_DESCENT_CURRENT_BRANCH_4685"
DECISION = "CMEM_CH_QBASIC_SOURCE_DESCENT_SUBTERM_ZERO_CXLIVE_VECTOR_RETAINED_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4686-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md"

DOC_PATH = POST / "4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md"
FORMAL_PATH = FORMAL / "701-PPC4161-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4684_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4684_NEXT_TARGET.csv"
CSV_4684_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4684_STATUS.csv"
CSV_4597_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_QBASIC_SPLIT_LAW.csv"
CSV_4597_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4597_CMEM_CH_DESCENT_ZERO_BRANCH.csv"
CSV_4597_BODY = SOURCE_DIR / "P8_Y5_R2FR_4597_BODY_CHARGE_ENVELOPE_CX_LIVE_UPDATE.csv"
CSV_4597_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_LIVE_COEFFICIENT_ROWS.csv"
CSV_4597_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4597_STATUS.csv"
CSV_4597_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4597_NEXT_TARGET.csv"
CSV_4597_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4597_VALIDATION.csv"
CSV_4598_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4598_STATUS.csv"
CSV_4598_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4598_NEXT_TARGET.csv"
CSV_4598_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4598_VALIDATION.csv"
FORMAL_613 = FORMAL / "613-PPC4161-Cmem-Ch-qbasic-source-descent-or-live-leakage-bound.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4685_SOURCE_REGISTER.csv"
SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_CX_QBASIC_SPLIT_LAW.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_CMEM_CH_DESCENT_ZERO_BRANCH.csv"
BODY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_BODY_CHARGE_ENVELOPE_CX_LIVE_UPDATE.csv"
COEFF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_CX_LIVE_COEFFICIENT_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4685_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4685_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4685_00_4684_next", CSV_4684_NEXT, "4685-Y5-R2FR-Cmem-Ch-parent-source-descent-or-Jlive-first-norm.md", "4684 selected Cmem/Ch target."),
        ("SRC4685_01_4684_status", CSV_4684_STATUS, "STRICT_SOURCE_KERNEL_INSERTED", "4684 status."),
        ("SRC4685_02_4597_split", CSV_4597_SPLIT, "CS4597_0_common_decomposition", "C_X q-basic/live split law."),
        ("SRC4685_03_4597_zero", CSV_4597_ZERO, "DZ4597_0_memory", "memory/fibre q-basic zero branch."),
        ("SRC4685_04_4597_body", CSV_4597_BODY, "CBU4597_0_memory", "A_mem/A_h C_live update."),
        ("SRC4685_05_4597_coeff", CSV_4597_COEFF, "CX4597_7_live_total", "C_X live coefficient rows."),
        ("SRC4685_06_4597_status", CSV_4597_STATUS, "CMEM_CH_QBASIC_SOURCE_DESCENT", "4597 status."),
        ("SRC4685_07_4597_next", CSV_4597_NEXT, "4598-Y5-R2FR-constant-standard-source-weight-zero-or-CXlive-first-norm.md", "4597 next target."),
        ("SRC4685_08_4597_validation", CSV_4597_VALIDATION, "VAL4597_OVERALL", "4597 validation passed."),
        ("SRC4685_09_4598_status", CSV_4598_STATUS, "CONSTANT_STANDARD_AND_SOURCE_WEIGHT_ZERO", "4598 next rung exists."),
        ("SRC4685_10_4598_next", CSV_4598_NEXT, "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md", "4598 next target."),
        ("SRC4685_11_4598_validation", CSV_4598_VALIDATION, "VAL4598_OVERALL", "4598 validation passed."),
        ("SRC4685_12_formal613", FORMAL_613, "C_X^live = C_X^std", "formal Cmem/Ch q-basic split."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def split_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "split_id": "CS4685_0_common_decomposition",
            "target": "C_X for X in {mem,h}",
            "formula": "C_X = C_X^qbasic + C_X^std + C_X^weight + C_X^label + C_X^Hodge + C_X^support_readout + C_X^boundary + C_X^nonHilbert",
            "zero_subterm": "C_X^qbasic=0 if S_src=Sbar_src[q(Phi),Psi,A,theta_0] and v_X in ker(Dq)",
            "live_bound": "|C_X^live| <= |C_X^std|+|C_X^weight|+|C_X^label|+|C_X^Hodge|+|C_X^support_readout|+|C_X^boundary|+|C_X^nonHilbert|",
            "status": "QBASIC_SUBTERM_ZERO_LIVE_VECTOR_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "split_id": "CS4685_1_chain_rule",
            "target": "q-basic source action",
            "formula": "delta_X S_src = (delta Sbar_src/delta q) Dq[v_X] + sum_a (delta S_src/delta theta_a) delta_X theta_a + boundary/readout/nonHilbert terms",
            "zero_subterm": "Dq[v_X]=0 kills only the quotient-pullback term",
            "live_bound": "standards, weights, labels, Hodge/support/readout, boundary and non-Hilbert tails remain absolute",
            "status": "NO_CANCELLATION_CHAIN_RULE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DZ4685_0_memory", "C_mem", "C_mem^qbasic=0", "v_m in ker(Dq); observed geometry/coframe/connection and source action descend through q; constants/material labels fixed; no source weights; Hodge/current/support/readout q-basic", "C_mem_live = C_mem^std+C_mem^weight+C_mem^label+C_mem^Hodge+C_mem^support_readout+C_mem^boundary+C_mem^nonHilbert", "MEMORY_QBASIC_SUBTERM_ZERO_NOT_FULL_CMEM_ZERO"),
        ("DZ4685_1_fibre", "C_h", "C_h^qbasic=0", "h absent from the source grammar or h vertical to q; same fixed constants/Hodge/support/readout clauses as memory", "C_h_live = C_h^std+C_h^weight+C_h^label+C_h^Hodge+C_h^support_readout+C_h^boundary+C_h^nonHilbert", "FIBRE_QBASIC_SUBTERM_ZERO_NOT_FULL_CH_ZERO"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": branch_id,
            "coefficient": coefficient,
            "zero_branch": zero_branch,
            "antecedents": antecedents,
            "live_replacement": live_replacement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for branch_id, coefficient, zero_branch, antecedents, live_replacement, status in data
    ]


def body_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CBU4685_0_memory", "A_mem", "|A_mem| <= [exp(R/lambda_mem) int (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem_live||)dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)", "|A_mem| <= [exp(R/lambda_mem) int (||B_mem_eff||||R_obs||+||C_mem_live||||T||+||J_mem_live||)dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)", "q-basic source-descent subterm removed; live standard/weight/label/Hodge/support/readout/boundary/non-Hilbert leakage remains"),
        ("CBU4685_1_fibre", "A_h", "|A_h| <= [exp(R/lambda_h) int (||B_h||||R_obs||+||C_h||||T||+||J_h_live||)dV + ||Q_boundary_h||]/(4*pi||Z_h||)", "|A_h| <= [exp(R/lambda_h) int (||B_h||||R_obs||+||C_h_live||||T||+||J_h_live||)dV + ||Q_boundary_h||]/(4*pi||Z_h||)", "q-basic/h-blind source-descent subterm removed; live leakage remains"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "target": target,
            "before": before,
            "after": after,
            "claim_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, target, before, after, effect in data
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CX4685_0_std", "C_X^std", "masses, charges, alpha_EM, clock/material standards vary with X", "constant superselection or parent fixed standards", "J_constants_bound / |C_X^std|"),
        ("CX4685_1_weight", "C_X^weight", "source-only prefactors w_A or kappa_A vary with X", "no pre-action source prefactor theorem", "source-weight norm"),
        ("CX4685_2_label", "C_X^label", "species/material labels survive source coupling", "source-label forgetting before coupling selection", "species/material label charge vector"),
        ("CX4685_3_hodge", "C_X^Hodge", "EM Hodge/current owner varies with X", "same Maxwell-Hodge/current owner and q-basic EM action", "Hodge/current leakage norm"),
        ("CX4685_4_support_readout", "C_X^support_readout", "support, clock, orbit, PPN or readout map re-enters after variation", "variation-before-readout plus one q-basic readout functor", "support/readout leakage norm"),
        ("CX4685_5_boundary", "C_X^boundary", "source boundary/reference charge varies with X", "fixed no-flux/topological boundary and neutral reference", "boundary derivative norm"),
        ("CX4685_6_nonHilbert", "C_X^nonHilbert", "retained non-Hilbert source covector", "no shadow/non-Hilbert labelled current theorem", "non-Hilbert source norm"),
        ("CX4685_7_live_total", "C_X^live", "total live matter-trace coupling after q-basic zero", "all live pieces zero in same branch", "sum of absolute live pieces"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "meaning": meaning,
            "derive_first": derive_first,
            "finite_fallback": finite_fallback,
            "current_status": "LIVE_VECTOR_ROW_READY_VALUE_MISSING" if symbol != "C_X^live" else "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, meaning, derive_first, finite_fallback in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4685_0_CX_qbasic", "C_X q-basic source descent", "q-basic subterm zero imported", "do not call full C_X zero"),
        ("SURV4685_1_CX_live", "C_X live leakage vector", "std/weight/label/Hodge/support/boundary/nonHilbert rows remain", NEXT_TARGET),
        ("SURV4685_2_A_mem_A_h", "body-charge envelopes", "A_mem/A_h updated to use C_mem_live/C_h_live", NEXT_TARGET),
        ("SURV4685_3_Jlive", "J_X live current", "unchanged live vector from 4684", "return after C_X live vector if still dominant"),
        ("SURV4685_4_global_parent", "EH/global parent/material projection", "unchanged public blockers", "keep promotion firewall active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4685": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4685_0", "Dq[v_X]=0 kills only the quotient-pullback term, not standards, labels, Hodge, support, boundary or non-Hilbert leakage."),
        ("CTRL4685_1", "Do not claim C_mem=C_h=0; only C_X^qbasic=0 is imported."),
        ("CTRL4685_2", "A_mem/A_h must use C_mem_live/C_h_live until every live component is parent-zero or bounded."),
        ("CTRL4685_3", "No cancellation credit among C_X live components; keep absolute-sum accounting."),
        ("CTRL4685_4", "Next target is constants/standards/source-weight live rows."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4685 imports the 4597 Cmem/Ch q-basic split into the current branch. The q-basic source-descent subterm is zero by the chain rule when S_src descends through q and v_X is vertical, but this does not set C_mem or C_h to zero. The live C_X vector contains standards, source weights, labels, Hodge, support/readout, boundary and non-Hilbert pieces. A_mem/A_h are updated to use C_mem_live/C_h_live.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "C_X q-basic source-descent subterm zero; C_mem/C_h live leakage vector; A_mem/A_h envelope updated with C_mem_live/C_h_live; finite coefficient rows",
            "not_derived": "full C_mem=C_h=0; parent-signed constant/source-weight/label/Hodge/support/readout/boundary/non-Hilbert zeros; numeric C_live values; local-GR/R10/PPN scoring",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4685_0",
            "target": NEXT_TARGET,
            "reason": "After the q-basic subterm is removed, the largest C_X risk is constants/standards and source weights because they can alter the trace coupling while preserving ordinary-looking Hilbert matter.",
            "derive_first": "prove constant-standard superselection and no source-only prefactor in the parent source grammar",
            "fallback": "fill the first finite C_X_live norm row for standards or source weights and insert into A_mem/A_h",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4685 - Y5/R2FR Cmem/Ch Parent Source Descent Or Jlive First Norm

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4685 imports the q-basic source-descent split:

```text
C_X = C_X^qbasic + C_X^live
S_src = Sbar_src[q(Phi), Psi, A, theta_0], v_X in ker(Dq)
=> C_X^qbasic = 0
```

The live part is retained:

```text
C_X^live = C_X^std + C_X^weight + C_X^label + C_X^Hodge
         + C_X^support_readout + C_X^boundary + C_X^nonHilbert.
```

So this narrows `C_mem/C_h`; it does not erase them.

## Source Register

{table(rows["sources"])}

## C_X q-Basic Split Law

{table(rows["split"])}

## Cmem / Ch Descent Zero Branch

{table(rows["zero"])}

## Body-Charge Envelope C_X Live Update

{table(rows["body"])}

## C_X Live Coefficient Rows

{table(rows["coefficients"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4685 - Y5/R2FR", "# 701 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4685 imports the Cmem/Ch q-basic source-descent split into the current branch. C_X^qbasic=0 follows when S_src descends through q and v_X is vertical, but C_X^live remains as standards, source weights, labels, Hodge, support/readout, boundary and non-Hilbert leakage; A_mem/A_h are updated to use C_mem_live/C_h_live.",
                "current_evidence": "Generated source register, C_X q-basic split law, Cmem/Ch zero branch, body-charge envelope C_live update, C_X live coefficient rows, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Calling full C_mem/C_h zero when only the q-basic subterm was killed, or allowing cancellation across live C_X components.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Cmem/Ch q-Basic Split

Marker: `{MARKER}`

4685 imports the q-basic source-descent split:

```text
C_X = C_X^qbasic + C_X^live,
C_X^qbasic = 0,
C_X^live = C_X^std + C_X^weight + C_X^label + C_X^Hodge
         + C_X^support_readout + C_X^boundary + C_X^nonHilbert.
```

This narrows the memory/fibre matter-trace coupling without overclaiming full `C_mem=C_h=0`. The next target is constants/standards/source-weight live rows.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Cmem/Ch q-Basic Split

Marker: `{PACKET_MARKER}`

The packet now carries `C_X^qbasic=0` and the live leakage vector. `A_mem/A_h` must use `C_mem_live/C_h_live` until standards, source weights, labels, Hodge, support/readout, boundary and non-Hilbert pieces are zeroed or bounded.

- split csv: `{SPLIT_CSV.name}`
- coefficient csv: `{COEFF_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4685_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4685_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4685_2_qbasic_split", any(row["split_id"] == "CS4685_0_common_decomposition" for row in rows["split"]), "C_X q-basic split written"),
        ("VAL4685_3_zero_branch", len(rows["zero"]) == 2, "Cmem/Ch zero branches present"),
        ("VAL4685_4_body_update", len(rows["body"]) == 2, "A_mem/A_h use C_live"),
        ("VAL4685_5_live_coeff_rows", any(row["symbol"] == "C_X^live" for row in rows["coefficients"]), "C_X live coefficient total present"),
        ("VAL4685_6_next_standard_weight", rows["next"][0]["target"] == NEXT_TARGET, "next constant/weight target selected"),
        ("VAL4685_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-527"),
        ("VAL4685_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4685_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4685_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4685_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4685_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4685_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4685_12_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4685_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4685_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "split": split_rows(timestamp),
        "zero": zero_rows(timestamp),
        "body": body_rows(timestamp),
        "coefficients": coefficient_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        SPLIT_CSV: rows["split"],
        ZERO_CSV: rows["zero"],
        BODY_CSV: rows["body"],
        COEFF_CSV: rows["coefficients"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
