from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4351"
CLAIM_ID = "L-192"
BRANCH = "MTS_R2FR_Y5_RI_OWNER_TAIL_ZERO_APPLICATION_OR_FINITE_BOUND_RUNNER_4351"
DECISION = "OWNER_TAIL_ZERO_APPLIES_ONLY_ON_FULL_CLEAN_BRANCH_OTHERWISE_FINITE_BOUND_WITH_4350_DENOMINATOR_NONCLAIM"
MARKER = "PPC4161_RI_OWNER_TAIL_ZERO_APPLICATION_OR_FINITE_BOUND_RUNNER_4351"
PACKET_MARKER = "PPC4161_PACKET_RI_OWNER_TAIL_ZERO_APPLICATION_OR_FINITE_BOUND_RUNNER_4351"
NEXT_TARGET = "4352-Y5-R2FR-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md"

FORMAL_PATH = FORMAL / "367-PPC4161-RI-owner-tail-zero-application-or-finite-bound-runner.md"
DOC_PATH = POST / "4351-Y5-R2FR-RI-owner-tail-zero-application-or-finite-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4351_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4351_00_4350_next": (
        FORMAL / "366-PPC4161-RI-boundary-anchor-and-EtaRI-correction-bound.md",
        "4351-Y5-R2FR-RI-owner-tail-zero-application-or-finite-bound-runner.md",
        "4350 handoff selecting owner-tail application or finite bound.",
    ),
    "SRC4351_01_4350_gap": (
        FORMAL / "366-PPC4161-RI-boundary-anchor-and-EtaRI-correction-bound.md",
        "=> homogeneous RI adjoint multiplier Lambda = 0.",
        "4350 clean branch supplies the positive gap and Lambda=0 leg.",
    ),
    "SRC4351_02_4347_zero": (
        FORMAL / "363-PPC4161-owner-tail-zero-signature-or-real-lambda-bound-runner.md",
        "C_RI=0,",
        "4347 exact owner-tail zero signature.",
    ),
    "SRC4351_03_4347_bound": (
        FORMAL / "363-PPC4161-owner-tail-zero-signature-or-real-lambda-bound-runner.md",
        "|Y_a| <=",
        "4347 no-cancellation fallback bound.",
    ),
    "SRC4351_04_4346_reduced": (
        FORMAL / "362-PPC4161-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md",
        "Y_a = Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI.",
        "4346 reduces the private score to owner-tail only after Kperp clean sector.",
    ),
    "SRC4351_05_216_guard": (
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Incoming-mode firewall remains separate from the static elliptic gap.",
    ),
    "SRC4351_06_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "Physical boundary flux must be routed rather than erased.",
    ),
    "SRC4351_07_250_kperp": (
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "K_extra_source   -> absent because the private local action has no independent TT source functional.",
        "Private clean Kperp sector already imported by 4346.",
    ),
    "SRC4351_08_4349_neumann": (
        FORMAL / "365-PPC4161-ZRI-MRI-EtaRI-source-or-domain-spectrum-row.md",
        "do not use no-flux alone as lambda proof",
        "No-flux alone cannot be used as the owner-tail zero proof.",
    ),
    "SRC4351_09_4350_firewall": (
        FORMAL / "366-PPC4161-RI-boundary-anchor-and-EtaRI-correction-bound.md",
        "Do not set Eta_RI,total=0 unless all zero clauses hold in the same collar.",
        "Same-collar requirement prevents mixed-branch cancellation.",
    ),
}


ARENAS = [
    ("delta_phi_fraction", "1.0e-5", "dimensionless"),
    ("delta_gamma", "1.0e-5", "dimensionless"),
    ("delta_beta", "1.0e-4", "dimensionless"),
    ("alpha1", "1.0e-4", "dimensionless"),
    ("alpha2", "1.0e-5", "dimensionless"),
    ("eta_AB", "1.0e-13", "dimensionless"),
    ("Gdot_over_G", "4.0e-14", "per_year"),
    ("chi_local_leak_fraction", "1.0e-5", "dimensionless"),
    ("clock_delta_z", "1.0e-16", "dimensionless"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def application_rows() -> List[Dict[str, str]]:
    return [
        {
            "application_id": "APP4351_0_Kperp_private_clean",
            "needed_clause": "private Kperp clean sector active",
            "input_from": "4346",
            "application": "Y_a reduces to Y_owner_a in the private compact selector",
            "result": "Kperp leg removed only privately",
            "status": "CONDITIONAL_PRIVATE_TRUE_PUBLIC_FALLBACK_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "application_id": "APP4351_1_constraint",
            "needed_clause": "S_RI block adopted and C_RI=0 on shell",
            "input_from": "4347",
            "application": "constraint-proportional metric stress vanishes",
            "result": "constraint leg zero if parent owner block is selected",
            "status": "PRIVATE_CANDIDATE_PARENT_ADOPTION_UNSIGNED_PUBLIC",
            "valid_for_claim": "False",
        },
        {
            "application_id": "APP4351_2_lambda",
            "needed_clause": "4350 compact anchored positive RI gap",
            "input_from": "4350",
            "application": "L_RI^dagger Lambda=0 with lambda_RI>0 implies Lambda=0",
            "result": "Lambda leg closes on clean static anchored branch",
            "status": "CONDITIONAL_CLEAN_BRANCH_APPLIED",
            "valid_for_claim": "False",
        },
        {
            "application_id": "APP4351_3_boundary",
            "needed_clause": "B_Lambda=B_RI=0 or routed outside local bulk",
            "input_from": "4347 and 4350",
            "application": "H_0^1 RI multiplier plus no corner/source injection kills the RI boundary stress leg",
            "result": "boundary leg closes only under same branch; otherwise finite B_RI row survives",
            "status": "CONDITIONAL_BOUNDARY_SILENCE_NOT_GLOBAL",
            "valid_for_claim": "False",
        },
        {
            "application_id": "APP4351_4_no_incoming",
            "needed_clause": "I_RI=0 stationary/no-incoming selector",
            "input_from": "216 guard and 4347",
            "application": "static elliptic positivity is not enough by itself; no-incoming must be signed",
            "result": "incoming leg is the live remaining sharp clause",
            "status": "OPEN_UNLESS_PARENT_STATIONARY_SELECTOR_SIGNS",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    lambda_denominator = "lambda_4350 := pi^2/ell_RI^2 - Eta_RI,total_bound"
    return [
        {
            "bound_id": "BND4351_0_clean_zero",
            "case": "full clean owner-tail branch",
            "formula": "C_RI=0, lambda_4350>0, R_Lambda=0, B_RI=0, I_RI=0 => Y_owner_a=0",
            "denominator": "lambda_4350=pi^2/ell_RI^2",
            "status": "EXACT_ZERO_IF_ALL_BRANCH_CLAUSES_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4351_1_finite_denominator",
            "case": "positive but imperfect branch",
            "formula": "|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350 + |Pi_a^BRI||B_RI| + |Pi_a^I||I_RI|",
            "denominator": lambda_denominator,
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4351_2_denominator_fail",
            "case": "lambda_4350 <= 0 or unsourced",
            "formula": "owner-tail zero/bound runner cannot score the RI inverse term",
            "denominator": lambda_denominator,
            "status": "CLAIM_BLOCKED_REQUIRES_ETA_ELL_ROWS",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4351_3_incoming_fail",
            "case": "I_RI not zero or not bounded",
            "formula": "|Pi_a^I||I_RI| survives even when Lambda=0",
            "denominator": "not controlled by static elliptic gap",
            "status": "NEXT_LIVE_CLAUSE",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, bound, units in ARENAS:
        rows.append(
            {
                "arena_id": f"OT4351_{arena}",
                "arena": arena,
                "arena_bound": bound,
                "units": units,
                "clean_branch_value": "0",
                "fallback_expression": "|Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350 + |Pi_a^BRI||B_RI| + |Pi_a^I||I_RI|",
                "needed_for_claim": "parent signatures or source-backed Pi/R_Lambda/B_RI/I_RI/ell_RI/Eta rows",
                "status": "ZERO_IF_FULL_BRANCH_ELSE_VALUES_MISSING_NONCLAIM",
                "claim_valid": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4351_0_full_clean",
            "input": "4346 Kperp clean + 4347 owner theorem + 4350 anchored Eta-zero gap + no incoming",
            "action": "APPLY_OWNER_TAIL_ZERO",
            "result": "Y_a=0 for the owner-tail/Kperp channel inside the private compact static selector",
            "claim_policy": "not public local GR until parent adoption/source/readout/global clauses are signed",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4351_1_gap_only",
            "input": "4350 positive gap but boundary or incoming clauses unsigned",
            "action": "PARTIAL_CLOSE_LAMBDA_KEEP_BRI_IRI",
            "result": "Lambda leg closes, but B_RI and I_RI remain explicit",
            "claim_policy": "no local claim from Lambda leg alone",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4351_2_bound",
            "input": "lambda_4350 positive but residual values nonzero",
            "action": "RUN_FINITE_OWNER_TAIL_FORMULA",
            "result": "absolute no-cancellation bound ready, numeric/source rows missing",
            "claim_policy": "score only after real projection and residual rows exist",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4351_3_next",
            "input": "application fork recorded",
            "action": "ATTACK_NO_INCOMING_AND_BOUNDARY_SILENCE",
            "result": NEXT_TARGET,
            "claim_policy": "do not confuse static elliptic gap with no-incoming theorem",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4351_0",
            "rule": "Do not claim Y_owner=0 from Lambda=0 alone.",
            "reason": "The owner-tail theorem also requires C_RI=0, B_RI=0 and I_RI=0.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4351_1",
            "rule": "Do not use the static elliptic RI gap to erase incoming modes.",
            "reason": "I_RI is a separate stationary/no-incoming selector clause.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4351_2",
            "rule": "Do not let owner-tail pieces cancel numerically.",
            "reason": "Fallback scoring is absolute componentwise.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4351_3",
            "rule": "Do not promote the private compact selector to global/public MTS.",
            "reason": "Kperp, RI owner adoption, source calibration and readout clauses remain branch-local.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4351_0",
            "decision": DECISION,
            "reason": "4350 is strong enough to close the Lambda leg of the 4347 owner-tail theorem, but the whole owner tail is zero only on the full clean branch with RI constraint adoption, boundary silence/routing and no incoming adjoint modes. Otherwise the finite no-cancellation bound now has the sharper 4350 denominator.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4351_0",
            "item": "Lambda leg",
            "status": "CLOSED_ON_4350_CLEAN_BRANCH",
            "note": "positive RI gap kills homogeneous Lambda in the compact anchored static branch.",
        },
        {
            "status_id": "STAT4351_1",
            "item": "Boundary/incoming legs",
            "status": "STILL_EXPLICIT_UNLESS_SIGNED",
            "note": "B_RI and I_RI are not erased by the Lambda gap alone.",
        },
        {
            "status_id": "STAT4351_2",
            "item": "finite bound",
            "status": "SHARPENED_WITH_4350_DENOMINATOR",
            "note": "fallback denominator is lambda_4350=pi^2/ell_RI^2-Eta_RI,total_bound.",
        },
        {
            "status_id": "STAT4351_3",
            "item": "next target",
            "status": "NO_INCOMING_AND_BOUNDARY_SILENCE",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4351_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can B_RI and I_RI be zeroed in the same compact static selector, or must the owner-tail branch now become a finite residual value runner?",
            "preferred_route": "derive stationary/no-incoming RI selector plus boundary/corner silence for the same anchored RI test space",
            "fallback_route": "fill finite B_RI, I_RI, R_Lambda, C_Lambda, Pi_a and lambda_4350 source rows for arena scoring",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "application": application_rows(),
        "bounds": bound_rows(),
        "arenas": arena_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4351_SOURCE_REGISTER.csv",
        "application": "P8_Y5_R2FR_4351_APPLICATION_ROWS.csv",
        "bounds": "P8_Y5_R2FR_4351_OWNER_TAIL_BOUND_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4351_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4351_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4351_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4351_DECISION.csv",
        "status": "P8_Y5_R2FR_4351_STATUS.csv",
        "next": "P8_Y5_R2FR_4351_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 367 PPC4161 RI owner-tail zero application or finite bound runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint applies the 4350 RI positive-gap theorem to the 4347 owner-tail theorem, but it does not prove public local GR, Newton, R10, PPN, clock, orbital, WEP, Maxwell/QED, or calibrated `G_N`.

## Result

4351 applies the new 4350 denominator instead of circling the old gap.

Full clean branch:

```text
Kperp_private = 0,
C_RI = 0,
lambda_4350 = pi^2/ell_RI^2 > 0,
R_Lambda = 0,
B_RI = 0,
I_RI = 0

=> Lambda = 0
=> Y_owner_a = 0
=> Y_a = 0
```

The important catch is that `Lambda=0` is not the whole owner-tail theorem. Boundary/corner stress and incoming homogeneous adjoint modes are separate legs. If they are unsigned, the honest fallback is:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI|
       + |Pi_a^I||I_RI|,

lambda_4350 := pi^2/ell_RI^2 - Eta_RI,total_bound.
```

So the project did move forward: the old vague `lambda_RI` denominator is now the 4350 anchored/Eta denominator. But the next real teeth are `B_RI` and `I_RI`.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Application Rows

{md_table(tables["application"], ["application_id", "needed_clause", "input_from", "application", "result", "status", "valid_for_claim"])}

## Owner-Tail Bound Rows

{md_table(tables["bounds"], ["bound_id", "case", "formula", "denominator", "status", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "arena_bound", "units", "clean_branch_value", "fallback_expression", "needed_for_claim", "status", "claim_valid", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4351 Y5-R2FR RI owner-tail zero application or finite bound runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4351 uses the 4350 RI gap. Clean branch:

```text
C_RI=0, lambda_4350>0, R_Lambda=0, B_RI=0, I_RI=0
=> Y_owner_a=0.
```

If boundary or incoming clauses are unsigned, the sharpened fallback is:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI|
       + |Pi_a^I||I_RI|.
```

This means the next useful attack is not another lambda pass. It is boundary/corner silence and no-incoming RI mode control.

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        csv.writer(handle).writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4351 applies the 4350 compact anchored RI positive-gap branch to the 4347 owner-tail theorem. The Lambda leg now closes inside the clean branch: lambda_4350=pi^2/ell_RI^2>0 implies Lambda=0 for the homogeneous adjoint equation. The full owner tail is zero only if the parent also signs RI constraint adoption, boundary/corner silence or routing, and stationary/no-incoming I_RI=0 in the same compact static selector. If any leg remains unsigned, the fallback is the sharpened absolute bound |Y_a|<=|Pi_a^RI|C_Lambda|R_Lambda|/lambda_4350+|Pi_a^BRI||B_RI|+|Pi_a^I||I_RI|, with lambda_4350=pi^2/ell_RI^2-Eta_RI,total_bound. No public local-GR/Newton/R10/PPN claim fires."
                ),
                (
                    "4351 source register, application rows, owner-tail bound rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "private_owner_tail_zero_if_full_clean_branch_else_finite_4350_bound_nonclaim",
                (
                    "Derive stationary/no-incoming RI selector plus boundary/corner silence, or fill finite B_RI, I_RI, R_Lambda, C_Lambda, Pi_a and lambda_4350 source rows."
                ),
                (
                    "Claiming owner-tail zero from Lambda=0 alone; using static elliptic positivity to erase incoming modes; allowing owner-tail components to cancel; promoting the private compact selector to public/global MTS."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4351 RI owner-tail zero application or finite bound runner

Marker: `{MARKER}`

4351 applies the 4350 denominator to the owner-tail theorem. On the full clean branch:

```text
C_RI=0, lambda_4350>0, R_Lambda=0, B_RI=0, I_RI=0
=> Y_owner_a=0.
```

If boundary/corner or incoming clauses are unsigned, the owner-tail channel is not zero; it is bounded by:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI|
       + |Pi_a^I||I_RI|.
```

Thus the Lambda leg is substantially improved, but `B_RI` and `I_RI` become the next high-leverage local-GR gates.
"""
    packet_block = f"""

## PPC4161 packet update 4351 owner-tail application

Marker: `{PACKET_MARKER}`

Packet update: the owner-tail route now has a real application fork. The clean compact branch gives `Y_owner=0`; the imperfect branch keeps a finite owner-tail bound with the 4350 denominator. The immediate remaining private blockers are `B_RI` and `I_RI`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in read_text(FORMAL_PATH), MARKER))
    checks.append(("decision_in_formal", DECISION in read_text(FORMAL_PATH), DECISION))
    checks.append(("zero_formula_present", "=> Y_owner_a = 0" in read_text(FORMAL_PATH), "owner zero"))
    checks.append(("finite_bound_present", "|Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350" in read_text(FORMAL_PATH), "finite bound"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("application_rows_present", len(tables["application"]) >= 5, str(len(tables["application"]))))
    checks.append(("bound_rows_present", len(tables["bounds"]) >= 4, str(len(tables["bounds"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("incoming_guard_present", "I_RI" in read_text(FORMAL_PATH) and "incoming" in read_text(FORMAL_PATH), "incoming guard"))
    checks.append(("boundary_guard_present", "B_RI" in read_text(FORMAL_PATH), "boundary guard"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4351_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4351_APPLICATION_ROWS.csv",
        "P8_Y5_R2FR_4351_OWNER_TAIL_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4351_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4351_RUNNER.csv",
        "P8_Y5_R2FR_4351_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4351_DECISION.csv",
        "P8_Y5_R2FR_4351_STATUS.csv",
        "P8_Y5_R2FR_4351_NEXT_TARGET.csv",
    ]:
        path = SOURCE_DIR / filename
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8"))) if path.exists() else []
        checks.append((f"csv_{filename}_parse_rows", bool(rows), f"{len(rows)} rows"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    write_tables(tables)
    write_docs(tables)
    append_claim_once()
    append_spine_and_packet()
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failures = [row for row in validation_rows if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 9 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
