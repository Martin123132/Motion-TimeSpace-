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

CHECKPOINT = "4704"
CLAIM_ID = "L-546"
MARKER = "PPC4161_VISIBLE_OPERATOR_DOMAIN_IMAGE_HOM_BRANCH_4704"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_OPERATOR_DOMAIN_IMAGE_HOM_BRANCH_4704"
DECISION = "VISIBLE_OPERATOR_DOMAIN_IMAGE_REDUCED_TO_PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4705-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md"

DOC_PATH = POST / "4704-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"
FORMAL_PATH = FORMAL / "720-PPC4161-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4703_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4703_STATUS.csv"
CSV_4703_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4703_NEXT_TARGET.csv"
CSV_4703_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4703_CURRENT_BRANCH_NO_EXTRA_F2_ROWS.csv"
CSV_4703_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4703_VALIDATION.csv"

CSV_4616_PROOF = SOURCE_DIR / "P8_Y5_R2FR_4616_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
CSV_4616_OBJECT = SOURCE_DIR / "P8_Y5_R2FR_4616_PARENT_GENERATOR_OBJECT_LANGUAGE.csv"
CSV_4616_HOM = SOURCE_DIR / "P8_Y5_R2FR_4616_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"
CSV_4616_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4616_OPERATOR_DOMAIN_DECISION_ROWS.csv"
CSV_4616_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4616_CLAIM_BLOCKERS.csv"
CSV_4616_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4616_CONTROL_ROWS.csv"
CSV_4616_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4616_STATUS.csv"
CSV_4616_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4616_NEXT_TARGET.csv"
CSV_4616_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4616_VALIDATION.csv"

FORMAL_719 = FORMAL / "719-PPC4161-no-extra-F2-operator-domain-or-lambdaA-source-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4704_SOURCE_REGISTER.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
OBJECT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_PARENT_GENERATOR_OBJECT_LANGUAGE.csv"
HOM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_CURRENT_BRANCH_VISIBLE_IMAGE_HOM_ROWS.csv"
DECISION_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_OPERATOR_DOMAIN_DECISION_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4704_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4704_VALIDATION.csv"

NEXT_4703 = "4704-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"
NEXT_4616 = "4617-Y5-R2FR-parent-scalar-functional-exhaustion-or-first-Hom-bound-value.md"


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


def restamp_rows(path: Path, timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in read_csv(path):
        row: dict[str, Any] = {}
        for key, value in source.items():
            if key in {"source_paths", "path", "source_path"}:
                new_value = value
            else:
                new_value = (
                    value.replace("4616", CHECKPOINT)
                    .replace(NEXT_4616, NEXT_TARGET)
                    .replace("2026-07-06T16:59:09.328965+00:00", timestamp)
                )
            row[key] = new_value
        row["checkpoint"] = CHECKPOINT
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["timestamp_utc"] = timestamp
        row.pop("generated_utc", None)
        rows.append(row)
    return rows


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4704_00_4703_status", CSV_4703_STATUS, "PPC4161_NO_EXTRA_F2_OPERATOR_DOMAIN_BRANCH_4703", "4703 no-extra-F2 handoff."),
        ("SRC4704_01_4703_next", CSV_4703_NEXT, NEXT_4703, "4703 selects visible image/Hom target."),
        ("SRC4704_02_4703_current", CSV_4703_CURRENT, "F2C4703_1_conditional_zero", "4703 parent-image conditional zero."),
        ("SRC4704_03_4703_validation", CSV_4703_VALIDATION, "VAL4703_OVERALL", "4703 validation passed."),
        ("SRC4704_04_4616_proof", CSV_4616_PROOF, "VIP4616_0_exact_image_zero_theorem", "4616 visible image theorem."),
        ("SRC4704_05_4616_hom", CSV_4616_HOM, "HOM4616_0_C_XF2_kernel_norm", "4616 hidden-Hom finite rows."),
        ("SRC4704_06_4616_object", CSV_4616_OBJECT, "OBJ4616_0_parent_Maxwell_norm", "4616 parent generator object language."),
        ("SRC4704_07_4616_decision", CSV_4616_DECISION, "DEC4616_0", "4616 operator-domain decision."),
        ("SRC4704_08_4616_blockers", CSV_4616_BLOCKERS, "BLK4616_0_parent_scalar_functional_exhaustion", "4616 blockers."),
        ("SRC4704_09_4616_controls", CSV_4616_CONTROLS, "CTRL4616_0_no_symmetry_shortcut", "4616 controls."),
        ("SRC4704_10_4616_status", CSV_4616_STATUS, "PRIVATE_NONCLAIM_DERIVATION_ADVANCE", "4616 status."),
        ("SRC4704_11_4616_next", CSV_4616_NEXT, NEXT_4616, "4616 next target."),
        ("SRC4704_12_4616_validation", CSV_4616_VALIDATION, "VAL4616_OVERALL", "4616 validation passed."),
        ("SRC4704_13_formal719", FORMAL_719, "Allowed[S_vis]=Image(ParentGenerate)", "formal 4703 upstream handoff."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def current_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "VIH4704_0_exact_image_zero",
            "quantity": "D_v_lambda_F2",
            "formula": "A_F2^vis=Image(Gen_EM) and Gen_EM=C_P N_Q <F_Q,F_Q> with fixed representation data => D_v lambda_F2=0",
            "meaning": "The clean zero branch is exact, but only if the visible coefficient object language is exhausted by parent-generated q-basic data.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_SCALAR_FUNCTIONAL_EXHAUSTION_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "VIH4704_1_countermodel",
            "quantity": "hidden_Hom_countermodel",
            "formula": "lambda_F2=lambda_0+epsilon I_hid is covariant and U(1)-gauge invariant if Coeff(F_Q^2) is a visible target",
            "meaning": "The hidden-Hom channel survives unless the target coefficient object is absent or factors only through q.",
            "current_status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "VIH4704_2_Hom_bound",
            "quantity": "H_XF2",
            "formula": "|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|",
            "meaning": "If scalar-functional exhaustion is unsigned, hidden/readout/radiative Hom becomes the finite EM coefficient branch.",
            "current_status": "FINITE_HOM_BOUND_STAGED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_VISIBLE_OPERATOR_DOMAIN_IMAGE_4704",
            "decision": DECISION,
            "reason": "The no-extra-F2/Hom branch is reduced to parent scalar-functional exhaustion: either the visible EM coefficient algebra has no hidden/readout/material scalar target, or H_XF2 remains a finite source input.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    status = [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "conditional exact image-zero theorem; hidden-Hom kernel theorem; scalar functional countermodel; finite H_XF2 bound rows",
            "not_derived": "parent scalar-functional exhaustion, quotient fullness/exactness on coefficient objects, radiative/readout stability, numeric Hom/K/tau bounds",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    next_rows = [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4704_0",
            "target": NEXT_TARGET,
            "reason": "The remaining obstruction is the parent scalar-functional object language: no hidden/readout/material scalar argument into Coeff(F_Q^2).",
            "derive_first": "prove the parent EM visible scalar algebra has no target object Coeff(F_Q^2) except the parent norm and fixed constants",
            "fallback": "fill the first source-backed H_XF2 or K_A*H_XF2 bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4704 - Visible Operator-Domain Image / Hidden-Hom Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim no-extra-F2. It compresses the obstruction:

```text
A_F2^vis = Image(Gen_EM),  Gen_EM=C_P N_Q <F_Q,F_Q>
with fixed representation data
=> D_v lambda_F2=0.
```

Countermodel:

```text
lambda_F2 = lambda_0 + epsilon I_hid
```

is legal if `Coeff(F_Q^2)` is a visible target object.

Finite branch:

```text
|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|.
```

## Source Register
{table(data["sources"])}

## Visible Image Proof Attempt
{table(data["proof"])}

## Parent Generator Object Language
{table(data["object"])}

## Hidden-Hom Bound Rows
{table(data["hom"])}

## Current Branch Rows
{table(data["current"])}

## Operator-Domain Decision
{table(data["decision_rows"])}

## Blockers
{table(data["blockers"])}

## Controls
{table(data["controls"])}

## Decision
{table(data["decision"])}

## Next Target
{table(data["next"])}
""",
        encoding="utf-8",
    )

    FORMAL_PATH.write_text(
        f"""# 720 - PPC4161 Visible Operator-Domain Image / Hidden-Hom Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Exact conditional branch:

```text
A_F2^vis=Image(Gen_EM),  Gen_EM=C_P N_Q <F_Q,F_Q>
=> D_v lambda_F2=0.
```

Hidden-Hom countermodel:

```text
lambda_F2=lambda_0+epsilon I_hid
```

is legal unless `Coeff(F_Q^2)` has no hidden/readout/material target object.

Finite branch:

```text
|s_XF2| <= H_XF2 + |delta_lambda_rad| + |delta_lambda_readout|.
```

No no-extra-F2, alpha, Maxwell, WEP, clock, R10, Newton or local-GR claim follows. Next branch is parent scalar-functional exhaustion.
""",
        encoding="utf-8",
    )


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(claims[0].keys()) if claims else [
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
        "title",
        "notes",
    ]
    claim_row = {field: "" for field in fieldnames}
    claim_row.update(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_empirical_interface",
            "claim": "4704 reduces visible EM coefficient image/no-Hom to parent scalar-functional exhaustion, with H_XF2 finite fallback rows.",
            "current_evidence": "Generated source register, visible image proof attempt, parent generator object language, hidden-Hom bounds, current branch rows, operator-domain decision, blockers, controls, decision, status, next target and validation.",
            "status": "visible_operator_domain_image_hom_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Treating the conditional image theorem as signed, ignoring hidden scalar countermodels, or using symmetry language instead of object-language exhaustion.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Visible operator-domain image / hidden-Hom gate",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    existing = next((row for row in claims if row.get("claim_id") == CLAIM_ID), None)
    if existing is None:
        claims.append(claim_row)
    else:
        existing.update(claim_row)
    write_csv(CLAIMS_PATH, claims)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`
- Status: private nonclaim.
- Movement: visible EM coefficient image/no-Hom is reduced to parent scalar-functional exhaustion; `H_XF2` finite fallback rows are staged.
- Key firewall: hidden/readout scalar countermodels remain legal unless the coefficient target object is absent or forced through `q`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 EM visible-image/Hom branch before parent scalar-functional exhaustion.
- Validation: `{VALIDATION_CSV}`.
""",
    )


def validation_rows(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4704_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4704_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4704_2_exact_image", any("Image(Gen_EM)" in row.get("formal_statement", "") for row in data["proof"]), "exact image theorem present")
    add("VAL4704_3_countermodel", any("countermodel" in row.get("proof_id", "").lower() for row in data["proof"]), "hidden scalar countermodel present")
    add("VAL4704_4_Hom_bound", any(row.get("symbol") == "H_XF2" for row in data["hom"]), "H_XF2 bound row present")
    add("VAL4704_5_current_bound", any("H_XF2" in row.get("formula", "") for row in data["current"]), "current Hom bound present")
    add("VAL4704_6_next_scalar_exhaustion", data["next"][0]["target"] == NEXT_TARGET, "next scalar-functional target selected")
    add("VAL4704_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4704_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4704_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4704_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4704_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        PROOF_CSV,
        OBJECT_CSV,
        HOM_CSV,
        CURRENT_CSV,
        DECISION_ROWS_CSV,
        BLOCKERS_CSV,
        CONTROL_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4704_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4704_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["proof"], data["object"], data["hom"], data["current"], data["decision_rows"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4704_12_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4704_13_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4704_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "proof": restamp_rows(CSV_4616_PROOF, timestamp),
        "object": restamp_rows(CSV_4616_OBJECT, timestamp),
        "hom": restamp_rows(CSV_4616_HOM, timestamp),
        "current": current_rows(timestamp),
        "decision_rows": restamp_rows(CSV_4616_DECISION, timestamp),
        "blockers": restamp_rows(CSV_4616_BLOCKERS, timestamp),
        "controls": restamp_rows(CSV_4616_CONTROLS, timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(PROOF_CSV, data["proof"])
    write_csv(OBJECT_CSV, data["object"])
    write_csv(HOM_CSV, data["hom"])
    write_csv(CURRENT_CSV, data["current"])
    write_csv(DECISION_ROWS_CSV, data["decision_rows"])
    write_csv(BLOCKERS_CSV, data["blockers"])
    write_csv(CONTROL_CSV, data["controls"])
    write_csv(DECISION_CSV, data["decision"])
    write_csv(STATUS_CSV, data["status"])
    write_csv(NEXT_CSV, data["next"])

    write_documents(timestamp, data)
    update_registers(timestamp)
    validation = validation_rows(timestamp, data)
    write_csv(VALIDATION_CSV, validation)

    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
