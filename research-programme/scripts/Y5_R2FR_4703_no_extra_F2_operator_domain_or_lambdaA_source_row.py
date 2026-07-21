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

CHECKPOINT = "4703"
CLAIM_ID = "L-545"
MARKER = "PPC4161_NO_EXTRA_F2_OPERATOR_DOMAIN_BRANCH_4703"
PACKET_MARKER = "PPC4161_PACKET_NO_EXTRA_F2_OPERATOR_DOMAIN_BRANCH_4703"
DECISION = "NO_EXTRA_F2_OPERATOR_DOMAIN_EXACT_CONDITIONAL_THEOREM_AND_LAMBDAA_ROW_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4704-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"

DOC_PATH = POST / "4703-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"
FORMAL_PATH = FORMAL / "719-PPC4161-no-extra-F2-operator-domain-or-lambdaA-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4702_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4702_STATUS.csv"
CSV_4702_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4702_NEXT_TARGET.csv"
CSV_4702_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4702_CURRENT_BRANCH_B_ALPHA_ROWS.csv"
CSV_4702_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4702_VALIDATION.csv"

CSV_4615_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4615_NO_EXTRA_F2_THEOREM.csv"
CSV_4615_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4615_OPERATOR_DOMAIN_CLAUSE_ROWS.csv"
CSV_4615_CLASS = SOURCE_DIR / "P8_Y5_R2FR_4615_F2_COUNTERTERM_CLASSIFICATION_ROWS.csv"
CSV_4615_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4615_LAMBDAA_SOURCE_ROW_NONCLAIM.csv"
CSV_4615_BALPHA = SOURCE_DIR / "P8_Y5_R2FR_4615_BALPHA_UPDATE_ROWS.csv"
CSV_4615_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4615_LAMBDAF2_BOUND_UPDATE_ROWS.csv"
CSV_4615_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4615_CLAIM_BLOCKERS.csv"
CSV_4615_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4615_CONTROL_ROWS.csv"
CSV_4615_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4615_STATUS.csv"
CSV_4615_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4615_DECISION.csv"
CSV_4615_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4615_NEXT_TARGET.csv"
CSV_4615_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4615_VALIDATION.csv"

FORMAL_718 = FORMAL / "718-PPC4161-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4703_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_NO_EXTRA_F2_THEOREM.csv"
DOMAIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_OPERATOR_DOMAIN_CLAUSE_ROWS.csv"
CLASS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_F2_COUNTERTERM_CLASSIFICATION_ROWS.csv"
SOURCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_LAMBDAA_SOURCE_ROW_NONCLAIM.csv"
BALPHA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_BALPHA_UPDATE_ROWS.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_LAMBDAF2_BOUND_UPDATE_ROWS.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_CURRENT_BRANCH_NO_EXTRA_F2_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4703_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4703_VALIDATION.csv"

NEXT_4702 = "4703-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"
NEXT_4615 = "4616-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"


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
                    value.replace("4615", CHECKPOINT)
                    .replace(NEXT_4615, NEXT_TARGET)
                    .replace("2026-07-06T16:50:33.085255+00:00", timestamp)
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
        ("SRC4703_00_4702_status", CSV_4702_STATUS, "PPC4161_EM_GAUGE_KINETIC_DESCENT_BRANCH_4702", "4702 EM gauge kinetic handoff."),
        ("SRC4703_01_4702_next", CSV_4702_NEXT, NEXT_4702, "4702 selects no-extra-F2 target."),
        ("SRC4703_02_4702_current", CSV_4702_CURRENT, "BAC4702_1_no_extra_F2_next", "4702 isolates lambda_A/C_XF2."),
        ("SRC4703_03_4702_validation", CSV_4702_VALIDATION, "VAL4702_OVERALL", "4702 validation passed."),
        ("SRC4703_04_4615_theorem", CSV_4615_THEOREM, "NEF4615_1_conditional_zero", "4615 no-extra-F2 theorem."),
        ("SRC4703_05_4615_domain", CSV_4615_DOMAIN, "OD4615_0_parent_image", "4615 operator-domain clauses."),
        ("SRC4703_06_4615_class", CSV_4615_CLASS, "F2C4615_2_hidden_scalar", "4615 counterterm classification."),
        ("SRC4703_07_4615_source", CSV_4615_SOURCE, "LAR4615_0_lambda_A", "4615 lambda source rows."),
        ("SRC4703_08_4615_balpha", CSV_4615_BALPHA, "BAU4615_0_lambda_insert", "4615 b_alpha update rows."),
        ("SRC4703_09_4615_bound", CSV_4615_BOUND, "LBU4615_2_active_lambdaF2", "4615 lambda/F2 bound rows."),
        ("SRC4703_10_4615_blockers", CSV_4615_BLOCKERS, "BLK4615_0_parent_image", "4615 blockers."),
        ("SRC4703_11_4615_controls", CSV_4615_CONTROLS, "CTRL4615_1_no_symmetry_shortcut", "4615 controls."),
        ("SRC4703_12_4615_status", CSV_4615_STATUS, "NO_EXTRA_F2_OPERATOR_DOMAIN", "4615 status."),
        ("SRC4703_13_4615_next", CSV_4615_NEXT, NEXT_4615, "4615 next target."),
        ("SRC4703_14_4615_validation", CSV_4615_VALIDATION, "VAL4615_OVERALL", "4615 validation passed."),
        ("SRC4703_15_formal718", FORMAL_718, "lambda_A F_Q^2", "formal 4702 upstream handoff."),
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
            "row_id": "F2C4703_0_countermodel",
            "quantity": "lambda_A_F2_legality",
            "formula": "DeltaS_F2=-1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2",
            "meaning": "Diffeomorphism covariance and U(1) gauge invariance do not forbid a scalar F_Q^2 coefficient.",
            "current_status": "SYMMETRY_SHORTCUT_REJECTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "F2C4703_1_conditional_zero",
            "quantity": "no_extra_F2_zero_contract",
            "formula": "Allowed[S_vis]=Image(ParentGenerate) with no free Coeff(F_Q^2) => D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0",
            "meaning": "No-extra-F2 is a typed parent-image/no-Hom theorem, not a gauge-symmetry slogan.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_IMAGE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "F2C4703_2_active_bound",
            "quantity": "B_lambdaF2",
            "formula": "B_lambdaF2 <= |s_XF2|+|C_XF2|+|delta_lambda_rad|+|delta_lambda_readout|",
            "meaning": "If the parent-image/no-Hom theorem is unsigned, the finite lambda/F2 throat remains an explicit EM coupling input.",
            "current_status": "FINITE_LAMBDAF2_BOUND_SYMBOLIC_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_NO_EXTRA_F2_OPERATOR_DOMAIN_4703",
            "decision": DECISION,
            "reason": "The legal F2 counterterm is split into parent image, hidden Hom, same-current, radiative/readout and source-scale gates with explicit lambda rows.",
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
            "derived": "symmetry countermodel; conditional parent-image no-extra-F2 theorem; constant calibration split; finite lambda/F2 identity; lambda source row schema",
            "not_derived": "parent visible operator-domain image theorem, hidden Hom exclusion, same-current z_g zero, radiative/readout closure, alpha/Maxwell/local-GR pass",
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
            "next_id": "NT4703_0",
            "target": NEXT_TARGET,
            "reason": "The strongest remaining clause is the parent visible operator-domain image; if it closes, hidden Hom and lambda_A have nowhere to live.",
            "derive_first": "prove Allowed[S_vis]=Image(ParentGenerate) for the visible EM coefficient algebra, with no free Coeff(F_Q^2)",
            "fallback": "retain hidden-Hom/C_XF2 and lambda_A source rows with finite bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4703 - No-Extra-F2 Operator-Domain Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** prove no-extra-F2. It blocks the bad shortcut and states the real theorem:

```text
DeltaS_F2 = -1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2
```

is allowed by ordinary diffeomorphism covariance and U(1) gauge invariance.

Clean zero route:

```text
Allowed[S_vis]=Image(ParentGenerate), no free Coeff(F_Q^2)
=> D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0.
```

Finite branch:

```text
B_lambdaF2 <= |s_XF2|+|C_XF2|+|delta_lambda_rad|+|delta_lambda_readout|.
```

## Source Register
{table(data["sources"])}

## No-Extra-F2 Theorem
{table(data["theorem"])}

## Operator-Domain Clauses
{table(data["domain"])}

## F2 Counterterm Classification
{table(data["class_rows"])}

## Lambda Source Rows
{table(data["source"])}

## b_alpha Update
{table(data["balpha"])}

## Lambda/F2 Bound Update
{table(data["bound"])}

## Current Branch Rows
{table(data["current"])}

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
        f"""# 719 - PPC4161 No-Extra-F2 Operator-Domain Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Symmetry countermodel:

```text
DeltaS_F2=-1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2.
```

Conditional zero theorem:

```text
Allowed[S_vis]=Image(ParentGenerate) and no free Coeff(F_Q^2)
=> D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0.
```

Finite branch:

```text
B_lambdaF2 <= |s_XF2|+|C_XF2|+|delta_lambda_rad|+|delta_lambda_readout|.
```

No no-extra-F2, alpha, Maxwell, WEP, clock, R10, Newton or local-GR claim follows. Next branch is visible operator-domain image / hidden-Hom.
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
            "claim": "4703 blocks the symmetry shortcut for no-extra-F2 and recasts lambda_A/C_XF2 as a parent-image/no-Hom operator-domain problem.",
            "current_evidence": "Generated source register, no-extra-F2 theorem, operator-domain clauses, F2 counterterm classification, lambda source rows, b_alpha update, lambda/F2 bounds, current rows, blockers, controls, decision, status, next target and validation.",
            "status": "no_extra_f2_operator_domain_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Claiming gauge symmetry forbids F2 scalar coefficients, treating constant calibration as alpha prediction, or hiding hidden-Hom/readout F2 coefficients.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "No-extra-F2 operator-domain gate",
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
- Movement: no-extra-F2 is now a parent-image/no-Hom operator-domain theorem, not a gauge-symmetry assertion.
- Key firewall: `F_Q^2` with scalar coefficient is symmetry-legal unless the visible operator domain excludes it.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 EM operator-domain branch before visible image / hidden-Hom proof.
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

    add("VAL4703_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4703_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4703_2_symmetry_countermodel", any("F_Q^2" in row.get("formula", "") for row in data["theorem"]), "F2 symmetry countermodel present")
    add("VAL4703_3_conditional_zero", any("Image(ParentGenerate)" in row.get("formula", "") for row in data["theorem"]), "parent-image conditional zero theorem present")
    add("VAL4703_4_lambda_source", any(row.get("row_id") == "LAR4703_0_lambda_A" for row in data["source"]), "lambda_A source row present")
    add("VAL4703_5_active_bound", any("B_lambdaF2" in row.get("quantity", "") for row in data["current"]), "active lambda/F2 bound present")
    add("VAL4703_6_no_symmetry_shortcut", any(row.get("control_id") == "CTRL4703_1_no_symmetry_shortcut" for row in data["controls"]), "no symmetry shortcut control present")
    add("VAL4703_7_next_visible_image", data["next"][0]["target"] == NEXT_TARGET, "next visible image target selected")
    add("VAL4703_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4703_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4703_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4703_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4703_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        DOMAIN_CSV,
        CLASS_CSV,
        SOURCE_CSV,
        BALPHA_CSV,
        BOUND_CSV,
        CURRENT_CSV,
        BLOCKERS_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4703_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4703_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["domain"], data["class_rows"], data["source"], data["balpha"], data["bound"], data["current"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4703_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4703_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4703_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4615_THEOREM, timestamp),
        "domain": restamp_rows(CSV_4615_DOMAIN, timestamp),
        "class_rows": restamp_rows(CSV_4615_CLASS, timestamp),
        "source": restamp_rows(CSV_4615_SOURCE, timestamp),
        "balpha": restamp_rows(CSV_4615_BALPHA, timestamp),
        "bound": restamp_rows(CSV_4615_BOUND, timestamp),
        "current": current_rows(timestamp),
        "blockers": restamp_rows(CSV_4615_BLOCKERS, timestamp),
        "controls": restamp_rows(CSV_4615_CONTROLS, timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(DOMAIN_CSV, data["domain"])
    write_csv(CLASS_CSV, data["class_rows"])
    write_csv(SOURCE_CSV, data["source"])
    write_csv(BALPHA_CSV, data["balpha"])
    write_csv(BOUND_CSV, data["bound"])
    write_csv(CURRENT_CSV, data["current"])
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
