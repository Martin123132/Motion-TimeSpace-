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

CHECKPOINT = "4708"
CLAIM_ID = "L-550"
MARKER = "PPC4161_FIRST_READOUT_TAIL_COEFFICIENT_ZERO_OR_SOURCE_BACKED_BOUND_4708"
PACKET_MARKER = "PPC4161_PACKET_FIRST_READOUT_TAIL_COEFFICIENT_ZERO_OR_SOURCE_BACKED_BOUND_4708"
DECISION = "RADIOUT_NATURALITY_EXACT_CONDITIONAL_BREADOUT_BRAD_FINITE_ROWS_RETAINED_NONCLAIM"
NEXT_TARGET = "4709-Y5-R2FR-clock-readout-tau-map-or-Breadout-first-source-row.md"

DOC_PATH = POST / "4708-Y5-R2FR-first-readout-tail-coefficient-zero-or-source-backed-bound.md"
FORMAL_PATH = FORMAL / "724-PPC4161-first-readout-tail-coefficient-zero-or-source-backed-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

CSV_4707_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4707_NEXT_TARGET.csv"
CSV_4707_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4707_READOUT_TAIL_BOUND_ROWS.csv"
CSV_4707_SIG = SOURCE_DIR / "P8_Y5_R2FR_4707_FACTORIZATION_SIGNATURE_AUDIT.csv"
CSV_4707_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4707_VALIDATION.csv"
CSV_1050_THEOREM = SOURCE_DIR / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
CSV_1050_OBSTRUCTION = SOURCE_DIR / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv"
CSV_1051_OWNER = SOURCE_DIR / "P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv"
CSV_1051_LEMMA = SOURCE_DIR / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
CSV_1051_CLOCK = SOURCE_DIR / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"
CSV_1052_TAU = SOURCE_DIR / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv"
CSV_1052_CLOCK = SOURCE_DIR / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
CSV_1052_R10 = SOURCE_DIR / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"
DOC_3810 = POST / "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md"
DOC_1113 = POST / "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md"
DOC_1219 = POST / "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4708_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_NATURALITY_THEOREM_ROWS.csv"
COUNTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_RADIOUT_COUNTERMODEL_ROWS.csv"
TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_BRAD_BREADOUT_SOURCE_ROWS_NONCLAIM.csv"
TRANSFER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_CLOCK_R10_TRANSFER_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4708_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4708_VALIDATION.csv"


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
        ("SRC4708_00_4707_next", CSV_4707_NEXT, "4708-Y5-R2FR-first-readout-tail-coefficient-zero-or-source-backed-bound.md", "4707 handoff"),
        ("SRC4708_01_4707_tail", CSV_4707_TAIL, "TAIL4707_3_readout_tail", "4707 B_readout target"),
        ("SRC4708_02_4707_sig", CSV_4707_SIG, "FSIG4707_5_observed_readout_closure", "4707 readout signature"),
        ("SRC4708_03_4707_validation", CSV_4707_VALIDATION, "VAL4707_OVERALL", "4707 validation passed"),
        ("SRC4708_04_1050_theorem", CSV_1050_THEOREM, "PFT1050_3_radiative_readout_closure", "1050 product functor radiative/readout clause"),
        ("SRC4708_05_1050_obstruction", CSV_1050_OBSTRUCTION, "OBS1050_4_radiative_readout", "1050 radiative/readout obstruction"),
        ("SRC4708_06_1051_owner", CSV_1051_OWNER, "AOR1051_3_verdict", "1051 alpha owner/radiative verdict"),
        ("SRC4708_07_1051_lemma", CSV_1051_LEMMA, "NMM1051_4_radiative_readout_limit", "1051 radiative/readout limit"),
        ("SRC4708_08_1051_clock", CSV_1051_CLOCK, "BAP1051_2_best_current_product", "1051 clock product bound"),
        ("SRC4708_09_1052_tau", CSV_1052_TAU, "TCN1052_4_verdict", "1052 tau not derived verdict"),
        ("SRC4708_10_1052_clock", CSV_1052_CLOCK, "ACB1052_2", "1052 best clock product"),
        ("SRC4708_11_1052_R10", CSV_1052_R10, "RAP1052_2_clock_to_R10_transfer", "1052 clock-to-R10 transfer warning"),
        ("SRC4708_12_3810_naturality", DOC_3810, "ZRT3810_2_radiative_naturality_extension", "3810 naturality theorem"),
        ("SRC4708_13_1113_radiative", DOC_1113, "POC1113_6_radiative_closure", "1113 radiative closure unsigned"),
        ("SRC4708_14_1219_readout", DOC_1219, "HSC1219_3_clock", "1219 clock/readout counterexample"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RRN4708_0_radiative_naturality_zero",
            "claim_piece": "B_rad zero",
            "formal_statement": "If the bare visible EM coefficient functor is quotient-typed and the RG/threshold/matching map is a natural transformation on quotient objects with fixed q-basic regulator and threshold data, then D_v delta_lambda_rad=0.",
            "proof": "A natural transformation cannot create hidden representative dependence from quotient-only inputs; counterterms remain in the same typed operator image.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_RADIOUT_SIGNATURE_UNSIGNED",
            "failure_mode": "loop or threshold data can regenerate f(I_hid)F_Q^2",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RRN4708_1_observed_readout_zero",
            "claim_piece": "B_readout zero",
            "formal_statement": "If alpha, spectroscopy, clock, material and apparatus readout maps factor through q_obs, Zbar, fixed standards and the same post-variation source branch, then D_v delta_lambda_readout=0.",
            "proof": "The readout derivative is a chain rule through q_obs and fixed readout data; Dq_obs[v]=0 and fixed standards kill the vertical derivative.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_READOUT_FUNCTOR_UNSIGNED",
            "failure_mode": "alpha_read or clock/material response can carry hidden/readout dependence after the bare action is solved",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RRN4708_2_combined_tail_zero",
            "claim_piece": "B_rad+B_readout zero",
            "formal_statement": "If RRN4708_0 and RRN4708_1 hold on the same branch as the 4707 Z_Q_eff factorization, then B_rad=B_readout=0 and the 4707 finite tail collapses to the remaining factorization/Hom/current terms.",
            "proof": "Substitute D_v delta_lambda_rad=D_v delta_lambda_readout=0 into the 4707 tail bound.",
            "current_status": "EXACT_CONDITIONAL_COMPOSITION_NOT_PROMOTED",
            "failure_mode": "using the bare theorem in clocks/R10 without readout functor and tau maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def counter_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "counter_id": "CEX4708_0_threshold_reentry",
            "countermodel": "delta_lambda_rad(mu)=epsilon I_hid log(mu/M_thr(I_hid))",
            "why_it_survives": "A hidden-dependent threshold or matching scale reintroduces visible F2 coefficient drift unless threshold data are q-basic/fixed.",
            "tail_created": "B_rad",
            "blocked_by": "radiative naturality plus fixed q-basic threshold/regulator data",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "counter_id": "CEX4708_1_clock_readout_reentry",
            "countermodel": "nu_i_read = nu_i_bar(q_obs,Zbar) * (1 + epsilon_i I_hid)",
            "why_it_survives": "Observed spectroscopy can depend on apparatus/material/readout maps unless those maps are parent-owned quotient functors.",
            "tail_created": "B_readout",
            "blocked_by": "clock/spectrum/material readout functor factorization",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "counter_id": "CEX4708_2_clock_product_not_standalone",
            "countermodel": "|b_alpha*tau_clock_time| is bounded but b_alpha is not isolated",
            "why_it_survives": "1051/1052 provide product bounds only; tau_clock_time, chi_X normalization and cross-arena maps are not derived.",
            "tail_created": "B_readout*tau_clock product branch",
            "blocked_by": "parent tau_clock/readout map or source-backed finite product row only",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def tail_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TAIL4708_0_Brad",
            "symbol": "B_rad",
            "definition": "radiative, threshold or matching re-entry into the effective Maxwell coefficient",
            "zero_condition": "RG/matching/threshold map is a natural quotient functor with q-basic fixed threshold data",
            "finite_formula": "B_rad := |D_v delta_lambda_rad|/Z_Q_eff_min",
            "source_requirement": "theorem-zero certificate or source-backed threshold/matching derivative with units",
            "status": "DERIVED_ZERO_CONDITIONAL_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TAIL4708_1_Breadout",
            "symbol": "B_readout",
            "definition": "observed alpha/clock/material/apparatus readout re-entry after solving the bare action",
            "zero_condition": "readout maps factor through q_obs, Zbar and fixed standards on the same branch",
            "finite_formula": "B_readout := |D_v delta_lambda_readout|/Z_Q_eff_min",
            "source_requirement": "readout functor theorem or finite clock/material/readout product coefficient",
            "status": "DERIVED_ZERO_CONDITIONAL_VALUE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TAIL4708_2_clock_product",
            "symbol": "B_readout_tau_clock",
            "definition": "clock-bounded product of readout/alpha drift with local clock-time projection",
            "zero_condition": "B_readout=0 or tau_clock_time=0 on a parent-signed local branch",
            "finite_formula": "|B_readout*tau_clock_time| <= 2.1e-18 yr^-1 from the best imported Yb clock product row, if branch-identification assumptions are met",
            "source_requirement": "derive tau_clock_time and chi_X normalization before isolating B_readout",
            "status": "SOURCE_BACKED_PRODUCT_ONLY_NOT_STANDALONE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TAIL4708_3_R10_transfer",
            "symbol": "B_readout_R10_transfer",
            "definition": "attempted transfer from clock/readout alpha drift to R10 short-range alpha(lambda)",
            "zero_condition": "same readout/source/test branch plus tau_R10/K_R10_EM projection maps",
            "finite_formula": "alpha_R10_readout(lambda) <= |K_R10_EM(lambda)|*(B_readout+B_rad+E_F2_Hom_tail)",
            "source_requirement": "K_R10_EM(lambda), tau_R10, material profile and source/test alpha charges",
            "status": "TRANSFER_BLOCKED_MAPS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def transfer_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4708_0_no_clock_to_R10_shortcut",
            "rule": "Do not transfer clock product bounds to R10/WEP without tau_R10, source/test charges and material profile maps.",
            "evidence": "RAP1052_2_clock_to_R10_transfer",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4708_1_no_standalone_balpha",
            "rule": "Clock data bound b_alpha*tau_clock_time, not standalone b_alpha or B_readout.",
            "evidence": "TCN1052_4_verdict;BAP1051_2_best_current_product",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4708_2_no_bare_to_observed_jump",
            "rule": "Bare no-hidden/no-F2 action descent is not an observed alpha/clock theorem until radiative/readout functor closure signs.",
            "evidence": "PFT1050_3;NMM1051_4;HSC1219_3",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_status_next(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_RADIOUT_TAIL_4708",
            "decision": DECISION,
            "reason": "Radiative/readout closure has an exact naturality theorem shape, but the corpus does not sign the EFT/readout functors. B_rad and B_readout therefore remain finite nonclaim rows; clock evidence is product-only.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]
    status = [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "conditional radiative naturality zero; conditional observed readout zero; finite B_rad/B_readout source rows; clock/R10 transfer firewall",
            "not_derived": "parent-owned EFT naturality, readout/spectroscopy/material functor, tau_clock_time normalization, tau_R10/K_R10 maps",
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
            "next_id": "NT4708_0",
            "target": NEXT_TARGET,
            "reason": "The first usable empirical handle is the clock product row, but it needs a parent tau/readout map before it can bound B_readout itself.",
            "derive_first": "derive tau_clock_time and readout functor from the same q_obs/Zbar branch",
            "fallback": "stage B_readout*tau_clock as product-only nonclaim row and refuse R10/WEP transfer",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4708 - First Readout Tail Coefficient Zero Or Source-Backed Bound

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4708 attacks the `B_rad` / `B_readout` wound directly.

Exact zero route:

```text
bare visible coefficient functor quotient-typed
+ EFT/RG/threshold map natural on quotient objects
+ observed alpha/clock/material readout functor factors through q_obs,Zbar
=> B_rad = B_readout = 0.
```

Current evidence does **not** sign those functors. The finite branch is therefore:

```text
B_rad     := |D_v delta_lambda_rad| / Z_Q_eff_min
B_readout := |D_v delta_lambda_readout| / Z_Q_eff_min.
```

The best existing empirical handle is only a product:

```text
|B_readout * tau_clock_time| <= 2.1e-18 yr^-1
```

from the clock product chain. It is not a standalone `B_readout` value and cannot be transferred to R10/WEP without `tau_R10`, source/test charges and material profile maps.

## Source Register
{table(data["sources"])}

## Radiative/Readout Naturality Theorem Rows
{table(data["theorems"])}

## Countermodel Rows
{table(data["counters"])}

## B_rad / B_readout Source Rows
{table(data["tails"])}

## Transfer Firewall Rows
{table(data["firewalls"])}

## Decision
{table(data["decision"])}

## Status
{table(data["status"])}

## Next Target
{table(data["next"])}
""",
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(
        f"""# 724 - PPC4161 First Readout Tail Coefficient Zero Or Source-Backed Bound

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Radiative tail:

```text
B_rad := |D_v delta_lambda_rad| / Z_Q_eff_min.
```

Readout tail:

```text
B_readout := |D_v delta_lambda_readout| / Z_Q_eff_min.
```

Zero branch:

```text
Natural_EFT(q_obs) and Natural_readout(q_obs,Zbar,fixed standards)
=> B_rad = B_readout = 0.
```

Finite branch:

```text
|B_readout * tau_clock_time| <= 2.1e-18 yr^-1
```

is product-only until `tau_clock_time` and the parent readout branch are derived. No R10/WEP/PPN/orbital transfer is allowed without arena maps.
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
            "claim": "4708 derives conditional radiative/readout tail zeros and stages B_rad/B_readout finite nonclaim rows with clock/R10 transfer firewalls.",
            "current_evidence": "Generated source register, radiative/readout theorem rows, countermodels, B_rad/B_readout source rows, transfer firewalls, decision, status, next target and validation.",
            "status": "radiative_readout_naturality_conditional_tail_rows_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Using clock product bounds as standalone B_readout or transferring them to R10/WEP without tau/source maps.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "First readout tail coefficient zero or source-backed bound",
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

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: `B_rad` and `B_readout` are no longer vague; they are zero only under quotient-natural EFT/readout functors, otherwise finite rows.
- Best existing empirical handle: `|B_readout*tau_clock_time| <= 2.1e-18 yr^-1`, product-only.
- Firewall: no standalone `B_readout`, no R10/WEP transfer without `tau_R10`, source/test charges and material profile maps.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: first radiative/readout tail theorem-or-bound checkpoint.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: 2026-07-07

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4708-Y5-R2FR-first-readout-tail-coefficient-zero-or-source-backed-bound.md`

## What Changed

`B_rad` and `B_readout` are now explicit:

```text
B_rad     := |D_v delta_lambda_rad| / Z_Q_eff_min
B_readout := |D_v delta_lambda_readout| / Z_Q_eff_min
```

They are zero only if EFT/RG/threshold and observed readout maps are natural quotient functors on the same branch. The best clock evidence is product-only:

```text
|B_readout * tau_clock_time| <= 2.1e-18 yr^-1.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not use clock product rows as standalone `B_readout`.
- Do not transfer clock alpha/readout bounds to R10/WEP without arena maps.
- Do not push to GitHub unless Martin explicitly asks for a GitHub update.
""",
        encoding="utf-8",
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

    add("VAL4708_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4708_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4708_2_brad_zero", any(row["claim_piece"] == "B_rad zero" for row in data["theorems"]), "B_rad zero theorem row present")
    add("VAL4708_3_breadout_zero", any(row["claim_piece"] == "B_readout zero" for row in data["theorems"]), "B_readout zero theorem row present")
    add("VAL4708_4_countermodels", len(data["counters"]) >= 3, "countermodels retained")
    add("VAL4708_5_tail_rows", any(row["symbol"] == "B_rad" for row in data["tails"]) and any(row["symbol"] == "B_readout" for row in data["tails"]), "B_rad and B_readout rows present")
    add("VAL4708_6_product_only", any("product" in row["status"].lower() for row in data["tails"]), "clock product-only row present")
    add("VAL4708_7_firewalls", len(data["firewalls"]) >= 3, "transfer firewalls present")
    add("VAL4708_8_next_tau", data["next"][0]["target"] == NEXT_TARGET, "next tau/readout target selected")
    add("VAL4708_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4708_10_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4708_11_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4708_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4708_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")
    add("VAL4708_14_resume_updated", NEXT_TARGET in text(RESUME_PATH), "resume bookmark updated")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        COUNTER_CSV,
        TAIL_CSV,
        TRANSFER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4708_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4708_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [
        data["theorems"],
        data["counters"],
        data["tails"],
        data["firewalls"],
        data["decision"],
        data["status"],
        data["next"],
    ]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4708_15_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4708_16_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4708_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "counters": counter_rows(timestamp),
        "tails": tail_rows(timestamp),
        "firewalls": transfer_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorems"])
    write_csv(COUNTER_CSV, data["counters"])
    write_csv(TAIL_CSV, data["tails"])
    write_csv(TRANSFER_CSV, data["firewalls"])
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
