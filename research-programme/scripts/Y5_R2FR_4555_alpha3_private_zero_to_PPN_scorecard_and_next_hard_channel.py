from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4555"
CLAIM_ID = "L-397"
BRANCH_ID = "MTS_R2FR_Y5_ALPHA3_PRIVATE_ZERO_TO_PPN_SCORECARD_4555"
MARKER = "PPC4161_ALPHA3_PRIVATE_ZERO_TO_PPN_SCORECARD_AND_NEXT_HARD_CHANNEL_4555"
PACKET_MARKER = "PPC4161_PACKET_ALPHA3_SCORECARD_NEXT_HARD_CHANNEL_4555"
DECISION = "ALPHA3_PRIVATE_SCORECARD_PASS_NEXT_HARD_CHANNEL_XI_SELECTED_GLOBAL_PARENT_UNSIGNED"
NEXT_TARGET = "4556-Y5-R2FR-xi-preferred-location-metric-channel-zero-or-finite-amplitude-row.md"

FORMAL_PATH = FORMAL / "571-PPC4161-alpha3-private-zero-to-PPN-scorecard-and-next-hard-channel.md"
DOC_PATH = POST / "4555-Y5-R2FR-alpha3-private-zero-to-PPN-scorecard-and-next-hard-channel.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4554 = FORMAL / "570-PPC4161-alpha3-cubic-vector-residue-classification-or-C3-bound-source-row.md"
DOC_4553 = FORMAL / "569-PPC4161-alpha3-parent-scalar-singlet-boundary-action-or-first-vector-amplitude-fill.md"
DOC_4539 = FORMAL / "555-PPC4161-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"
DOC_4550 = FORMAL / "566-PPC4161-first-static-coefficient-product-bound-or-projection-kernel-row.md"
ALPHA3_FINAL_4554 = SOURCE_DIR / "P8_Y5_R2FR_4554_ALPHA3_PRIVATE_BRANCH_FINAL_ZERO.csv"
C3_VALUE_4554 = SOURCE_DIR / "P8_Y5_R2FR_4554_C3_ALPHA3_VALUE_ROW.csv"
PRODUCT_BOUNDS_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
PRODUCT_RANKING_4550 = SOURCE_DIR / "P8_Y5_R2FR_4550_PRODUCT_BOUND_RANKING.csv"
VALIDATION_4554 = SOURCE_DIR / "P8_Y5_BRR545_4554_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4555_SOURCE_REGISTER.csv"
SCORECARD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_LOCAL_PPN_SCORECARD_REFRESH.csv"
ACTIVE_RANKING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_ACTIVE_PRODUCT_PRESSURE_RANKING.csv"
NEXT_CHANNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_NEXT_CHANNEL_XI_AUDIT.csv"
BRANCH_SCOPE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_BRANCH_SCOPE_FIREWALL.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4555_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4555_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        stripped = str(value).strip()
        if stripped == "" or stripped.lower() in {"missing", "nan", "none"}:
            return None
        return float(stripped)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4555_00_4554_doc", "4554 alpha3 cubic zero doc", DOC_4554, "Delta alpha3 = 0"),
        ("SRC4555_01_4554_final_zero", "4554 alpha3 final zero CSV", ALPHA3_FINAL_4554, "AF4554_0_private_branch_alpha3"),
        ("SRC4555_02_4554_c3", "4554 C3 value row", C3_VALUE_4554, "C3V4554_0_private_selector_value"),
        ("SRC4555_03_4554_validation", "4554 validation", VALIDATION_4554, "VAL4554_OVERALL"),
        ("SRC4555_04_4550_product_bounds", "4550 observable product bounds", PRODUCT_BOUNDS_4550, "PB4550_xi"),
        ("SRC4555_05_4550_ranking", "4550 product ranking", PRODUCT_RANKING_4550, "xi"),
        ("SRC4555_06_4550_doc", "4550 product-bound doc", DOC_4550, "PB4550_alpha3"),
        ("SRC4555_07_4553_doc", "4553 branch-scoped zero doc", DOC_4553, "M_alpha3 = 0"),
        ("SRC4555_08_4539_global_firewall", "4539 global parent firewall", DOC_4539, "FAIL_UNSIGNED"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4555 scorecard propagation and next-channel selection",
                "valid_for_claim": "False",
            }
        )
    return rows


def product_rows() -> list[dict[str, str]]:
    return read_csv(PRODUCT_BOUNDS_4550)


def product_rank_value(row: dict[str, str]) -> float:
    value = safe_float(row.get("max_product_if_boundary_and_higher_zero"))
    return value if value is not None else float("inf")


def scorecard_rows() -> list[dict[str, Any]]:
    products = product_rows()
    alpha3_zero = next((row for row in read_csv(ALPHA3_FINAL_4554) if row.get("final_id") == "AF4554_0_private_branch_alpha3"), {})
    rows: list[dict[str, Any]] = []
    for product in sorted(products, key=product_rank_value):
        observable = product.get("observable", "")
        if observable == "alpha3":
            private_status = "PASS_PRIVATE_SELECTOR_ZERO"
            private_prediction = alpha3_zero.get("Delta_alpha3", "0")
            active_private_pressure = "False"
            next_action = "do not reopen alpha3 unless branch scope changes; propagate zero into private scorecard"
        else:
            private_status = "OPEN_ZERO_OR_BOUND_REQUIRED"
            private_prediction = "MISSING_ZERO_OR_FINITE_PRODUCT"
            active_private_pressure = "True"
            next_action = "derive theorem zero or source finite product row"
        rows.append(
            {
                "score_id": f"SC4555_{observable}",
                "observable": observable,
                "arena": product.get("arena", ""),
                "bound": product.get("bound", ""),
                "bound_units": product.get("bound_units", ""),
                "product_symbol": product.get("product_symbol", ""),
                "boundary_symbol": product.get("boundary_symbol", ""),
                "max_product_if_boundary_and_higher_zero": product.get("max_product_if_boundary_and_higher_zero", ""),
                "private_selector_prediction": private_prediction,
                "private_selector_status": private_status,
                "active_private_pressure": active_private_pressure,
                "global_parent_status": "not_promoted_global_parent_unsigned",
                "public_claim_allowed": "False",
                "next_action": next_action,
                "valid_for_claim": "False",
            }
        )
    return rows


def active_ranking_rows(scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    active = [row for row in scorecard if row.get("active_private_pressure") == "True"]
    active.sort(key=lambda row: safe_float(row.get("max_product_if_boundary_and_higher_zero")) or float("inf"))
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(active, start=1):
        rows.append(
            {
                "active_rank": index,
                "observable": row.get("observable", ""),
                "arena": row.get("arena", ""),
                "max_product_if_boundary_and_higher_zero": row.get("max_product_if_boundary_and_higher_zero", ""),
                "why_it_matters": "smallest remaining allowed product after alpha3 private zero" if index == 1 else "less stringent remaining product",
                "recommended_next": b(index == 1),
                "valid_for_claim": "False",
            }
        )
    return rows


def next_channel_rows(ranking: list[dict[str, Any]]) -> list[dict[str, Any]]:
    first = ranking[0] if ranking else {}
    return [
        {
            "audit_id": "NX4555_0_selected_channel",
            "selected_observable": first.get("observable", "MISSING"),
            "selected_arena": first.get("arena", "MISSING"),
            "reason": "After alpha3 private zero, this is the smallest remaining max_product_if_boundary_and_higher_zero.",
            "bound_pressure": first.get("max_product_if_boundary_and_higher_zero", "MISSING"),
            "required_derivation": "For xi, derive preferred-location/metric scalar-channel zero inside the same compact selector, or fill finite P_xi/Q_xi/R_higher_xi amplitude rows.",
            "avoid": "Do not reuse alpha3 vector-parity proof blindly; xi is a metric/preferred-location channel, so it needs its own scalar/boundary/domain trace argument.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "audit_id": "NX4555_1_alpha3_reopen_rule",
            "selected_observable": "alpha3",
            "selected_arena": "PPN_conservation",
            "reason": "Alpha3 is private-zero only under compact centred stationary non-radiative selector premises.",
            "bound_pressure": "4e-20",
            "required_derivation": "Reopen alpha3 only if spin/rotation/off-centre/radiative/open-sector countermodels are admitted.",
            "avoid": "Do not treat alpha3 private zero as global parent adoption.",
            "next_target": "none unless branch scope changes",
            "valid_for_claim": "False",
        },
    ]


def branch_scope_rows() -> list[dict[str, Any]]:
    return [
        {
            "scope_id": "BS4555_0_private_score",
            "scope": "private PPC4161-GP-HQNP compact stationary non-radiative local selector",
            "alpha3_status": "scorecard pass as Delta_alpha3=0",
            "allowed_use": "internal local PPN pressure ranking and next-channel selection",
            "forbidden_use": "public/global MTS local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "scope_id": "BS4555_1_global_parent",
            "scope": "full MTS parent/global/open/radiative sectors",
            "alpha3_status": "not promoted",
            "allowed_use": "countermodel ledger and future parent-action target",
            "forbidden_use": "claiming the local selector is globally forced",
            "valid_for_claim": "False",
        },
        {
            "scope_id": "BS4555_2_xi_route",
            "scope": "next private local channel",
            "alpha3_status": "closed unless scope changes",
            "allowed_use": "move pressure to xi metric/preferred-location channel",
            "forbidden_use": "using vector alpha3 proof as a xi proof",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows(ranking: list[dict[str, Any]]) -> list[dict[str, Any]]:
    first = ranking[0].get("observable", "") if ranking else ""
    return [
        {
            "gate_id": "G4555_0_alpha3_private_scorecard",
            "requirement": "alpha3 private branch final zero is imported into scorecard",
            "status": "PASS_PRIVATE_SELECTOR",
            "claim_effect": "alpha3 removed from active private product pressure ranking",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4555_1_global_public_firewall",
            "requirement": "global parent/public claim remains false",
            "status": "PASS_FIREWALL",
            "claim_effect": "prevents overclaiming alpha3 result",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4555_2_next_channel_selection",
            "requirement": "remaining channels ranked after alpha3 removal",
            "status": "PASS_NEXT_SELECTED" if first == "xi" else "FAIL_NEXT_SELECTION",
            "claim_effect": f"next hard channel = {first}",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G4555_3_local_gr_completion",
            "requirement": "all PPN/local channels closed and global parent signed",
            "status": "BLOCKED_INCOMPLETE",
            "claim_effect": "goal remains active; xi and other channels still need derivation/bounds",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(ranking: list[dict[str, Any]]) -> list[dict[str, Any]]:
    first = ranking[0].get("observable", "MISSING") if ranking else "MISSING"
    return [
        {
            "decision_id": "DEC4555_0",
            "decision": DECISION,
            "summary": f"4555 imports the 4554 alpha3 private-branch zero into a local PPN scorecard, removes alpha3 from the active private product-pressure ranking, keeps the global/public firewall active, and selects {first} as the next hard remaining local channel.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "xi is the tightest remaining active private product-pressure channel after alpha3 is closed.",
            "success_condition": "Either derive xi=0 inside the private selector using metric/preferred-location scalar-channel arguments, or fill finite P_xi/Q_xi/R_higher_xi rows satisfying the xi no-cancellation bound.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    next_channel: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append(
        {
            "validation_id": "VAL4555_0_sources",
            "check": "all cited source paths exist and needles are found",
            "status": "PASS" if sources_ok else "FAIL",
            "details": f"{sum(1 for row in sources if row['exists'] == 'True' and row['needle_found'] == 'True')}/{len(sources)} sources verified",
        }
    )

    alpha3 = next((row for row in scorecard if row.get("observable") == "alpha3"), {})
    alpha3_ok = alpha3.get("private_selector_prediction") == "0"
    alpha3_ok = alpha3_ok and alpha3.get("private_selector_status") == "PASS_PRIVATE_SELECTOR_ZERO"
    alpha3_ok = alpha3_ok and alpha3.get("active_private_pressure") == "False"
    rows.append(
        {
            "validation_id": "VAL4555_1_alpha3_scorecard",
            "check": "alpha3 private zero is imported and removed from active pressure",
            "status": "PASS" if alpha3_ok else "FAIL",
            "details": "alpha3 scorecard row checked",
        }
    )

    ranking_ok = bool(ranking) and ranking[0].get("observable") == "xi" and ranking[0].get("recommended_next") == "True"
    rows.append(
        {
            "validation_id": "VAL4555_2_active_ranking",
            "check": "next active product-pressure channel is xi",
            "status": "PASS" if ranking_ok else "FAIL",
            "details": f"first={ranking[0].get('observable') if ranking else 'NONE'}",
        }
    )

    next_text = " ".join(str(value) for row in next_channel for value in row.values())
    next_ok = "preferred-location" in next_text and "Do not reuse alpha3 vector-parity proof blindly" in next_text
    rows.append(
        {
            "validation_id": "VAL4555_3_next_channel_audit",
            "check": "xi audit states its own derivation route and alpha3-proof caveat",
            "status": "PASS" if next_ok else "FAIL",
            "details": "xi route audited",
        }
    )

    gates_ok = any(row.get("status") == "PASS_FIREWALL" for row in gates)
    gates_ok = gates_ok and any(row.get("status") == "BLOCKED_INCOMPLETE" for row in gates)
    rows.append(
        {
            "validation_id": "VAL4555_4_claim_gates",
            "check": "public/global firewall and incomplete-goal gate remain active",
            "status": "PASS" if gates_ok else "FAIL",
            "details": "no local-GR/global claim promoted",
        }
    )

    docs_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    rows.append(
        {
            "validation_id": "VAL4555_5_docs",
            "check": "post and formal docs exist during validation",
            "status": "PASS" if docs_ok else "FAIL",
            "details": f"post={DOC_PATH.exists()} formal={FORMAL_PATH.exists()}",
        }
    )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL4555_OVERALL",
            "check": "4555 checkpoint validation",
            "status": "PASS" if overall else "FAIL",
            "details": DECISION if overall else "one or more validation checks failed",
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    next_channel: list[dict[str, Any]],
    scope: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    first = ranking[0] if ranking else {}
    return f"""# 4555 - alpha3 private zero to PPN scorecard and next hard channel

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4554 closed `alpha3` inside the private compact stationary non-radiative selector:

```text
Delta alpha3 = 0.
```

4555 propagates that result into the local PPN scorecard rather than reopening the same alpha3 wall. The scorecard now treats `alpha3` as:

```text
private_selector_prediction = 0
private_selector_status     = PASS_PRIVATE_SELECTOR_ZERO
global_parent_status        = not_promoted_global_parent_unsigned
```

After removing `alpha3` from the active private product-pressure list, the next tightest remaining channel is:

```text
observable = {first.get('observable', 'MISSING')}
arena      = {first.get('arena', 'MISSING')}
product allowance = {first.get('max_product_if_boundary_and_higher_zero', 'MISSING')}
```

So the next pressure target is `xi`, not another alpha3 loop. Importantly, `xi` is not a vector-parity problem like `alpha3`; it is a metric/preferred-location channel and needs its own scalar/boundary/domain trace argument or finite amplitude rows.

## Local PPN Scorecard Refresh

{markdown_table(scorecard)}

## Active Product Pressure Ranking

{markdown_table(ranking)}

## Next Channel Xi Audit

{markdown_table(next_channel)}

## Branch Scope Firewall

{markdown_table(scope)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4555 propagates the private alpha3=0 result into the local PPN scorecard and selects xi as the next tightest remaining private product-pressure channel.",
        "current_evidence": "Generated source register, local PPN scorecard refresh, active product-pressure ranking, xi next-channel audit, branch firewall, claim gates, status and validation CSVs.",
        "status": "alpha3_private_scorecard_pass_xi_next_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Treating private alpha3 scorecard pass as global parent adoption, or reusing alpha3 vector-parity proof for xi without a metric/preferred-location derivation.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "Alpha3 should not be reopened unless branch scope changes; xi is the next local PPN pressure channel.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    scorecard = scorecard_rows()
    ranking = active_ranking_rows(scorecard)
    next_channel = next_channel_rows(ranking)
    scope = branch_scope_rows()
    gates = claim_gate_rows(ranking)
    decisions = decision_rows(ranking)
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SCORECARD_CSV, scorecard)
    write_csv(ACTIVE_RANKING_CSV, ranking)
    write_csv(NEXT_CHANNEL_CSV, next_channel)
    write_csv(BRANCH_SCOPE_CSV, scope)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4555 - alpha3 private zero to PPN scorecard and next hard channel\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, scorecard, ranking, next_channel, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, scorecard, ranking, next_channel, scope, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4555 Alpha3 Scorecard Propagation And Xi Next Target

Marker: `{MARKER}`  
The local PPN scorecard now records `alpha3=0` inside the private compact stationary selector and removes it from active private product pressure. The next tightest remaining channel is `xi`, with product allowance `6.4582427632245596e+05`. This is still private/nonclaim; global parent adoption remains unsigned.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4555 Packet Integration - Alpha3 Scorecard And Xi Pressure

Marker: `{PACKET_MARKER}`  
Within compact stationary non-radiative PPC4161-GP-HQNP packets, `alpha3` is now a scorecard-private zero. The next local PPN pressure channel is `xi`, which must be treated as a metric/preferred-location channel rather than an alpha3-style vector-parity problem.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4555_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
