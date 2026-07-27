from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4346"
CLAIM_ID = "L-187"
BRANCH = "MTS_R2FR_Y5_FILL_REAL_OWNER_TAIL_KPERP_VALUES_OR_ADOPT_CLEAN_SECTOR_4346"
DECISION = "KPERP_CLEAN_SECTOR_ADOPTED_PRIVATE_REAL_OWNER_TAIL_VALUES_MISSING_NONCLAIM"
MARKER = "PPC4161_FILL_REAL_OWNER_TAIL_KPERP_VALUES_OR_ADOPT_CLEAN_SECTOR_4346"
PACKET_MARKER = "PPC4161_PACKET_FILL_REAL_OWNER_TAIL_KPERP_VALUES_OR_ADOPT_CLEAN_SECTOR_4346"
NEXT_TARGET = "4347-Y5-R2FR-owner-tail-zero-signature-or-real-lambda-bound-runner.md"

FORMAL_PATH = FORMAL / "362-PPC4161-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md"
DOC_PATH = POST / "4346-Y5-R2FR-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4346_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

ARENA_GATES = [
    ("delta_phi_fraction", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:112"),
    ("delta_gamma", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:113"),
    ("delta_beta", "1.0e-4", "dimensionless", "59-local-ppn-branch-framework.md:114"),
    ("alpha1", "1.0e-4", "dimensionless", "59-local-ppn-branch-framework.md:115"),
    ("alpha2", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:116"),
    ("eta_AB", "1.0e-13", "dimensionless", "59-local-ppn-branch-framework.md:117"),
    ("Gdot_over_G", "4.0e-14", "per_year", "59-local-ppn-branch-framework.md:118"),
    ("chi_local_leak_fraction", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:119"),
    ("clock_delta_z", "1.0e-16", "dimensionless", "59-local-ppn-branch-framework.md:120"),
]

SOURCES = [
    (
        "SRC4346_00_4345_next",
        FORMAL / "361-PPC4161-first-source-backed-owner-tail-or-Kperp-score-row.md",
        "4346-Y5-R2FR-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md",
        "4345 handoff selecting real values or clean sector.",
    ),
    (
        "SRC4346_01_250_private_kextra_absent",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "K_extra_source   -> absent",
        "Private selector says no independent static Kperp source.",
    ),
    (
        "SRC4346_02_250_kperp_zero",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "Private Kperp contribution vanishes in compact selector.",
    ),
    (
        "SRC4346_03_221_six_clause_gate",
        FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
        "same observed coframe for matter, EM, clocks and rods;",
        "Six-clause EH/coframe gate source.",
    ),
    (
        "SRC4346_04_220_sector_split",
        FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md",
        "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.",
        "Kperp four-sector placement rule.",
    ),
    (
        "SRC4346_05_219_no_pole",
        FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md",
        "if parent-signed, `W_i^K=0`",
        "No-extra-pole route for static local PPN.",
    ),
    (
        "SRC4346_06_193_vertical_silence",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0.",
        "Vertical representative directions do not source ordinary local readouts.",
    ),
    (
        "SRC4346_07_222_calibrated_coupling",
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "G_N^obs := G_cal.",
        "Universal calibrated coupling clause for the private selector.",
    ),
    (
        "SRC4346_08_360_owner_tail",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "Y_owner_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI",
        "Owner-tail finite score formula.",
    ),
    (
        "SRC4346_09_360_lambda_input",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "IN4344_0_lambda_RI",
        "lambda_RI remains a required physical input.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
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


def clean_sector_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "KC4346_0_same_coframe",
            "clause": "same observed coframe for matter, EM, clocks and rods",
            "private_selector_truth": "True",
            "public_parent_truth": "False",
            "source": "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
            "effect": "permits K_metric_TT to be counted in g_obs rather than as extra force",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "KC4346_1_EH_spin2_block",
            "clause": "EH/Palatini spin-2 principal block",
            "private_selector_truth": "True",
            "public_parent_truth": "False",
            "source": "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
            "effect": "routes ordinary TT to the GR/EH sector",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "KC4346_2_no_independent_TT_source",
            "clause": "no independent static MTS TT source projection",
            "private_selector_truth": "True",
            "public_parent_truth": "False",
            "source": "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
            "effect": "sets K_extra_source=0 inside the compact selector",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "KC4346_3_vertical_quotient_silence",
            "clause": "vertical quotient silence",
            "private_selector_truth": "True",
            "public_parent_truth": "False",
            "source": "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
            "effect": "sets W_i^K=0 for q-vertical representatives",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "KC4346_4_boundary_radiation_routing",
            "clause": "boundary/radiation routing",
            "private_selector_truth": "True",
            "public_parent_truth": "False",
            "source": "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
            "effect": "prevents boundary/radiative Kperp from becoming hidden local bulk force",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "KC4346_5_universal_calibrated_coupling",
            "clause": "kappa_eff = 8*pi*G_N/c^4 after source calibration",
            "private_selector_truth": "True",
            "public_parent_truth": "False",
            "source": "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
            "effect": "keeps local reduction GR-like without claiming numeric G_N prediction",
            "valid_for_claim": "False",
        },
    ]


def kperp_sector_rows() -> List[Dict[str, str]]:
    return [
        {
            "sector_id": "KS4346_0_metric_TT",
            "sector": "K_metric_TT",
            "private_disposition": "ordinary EH/GR TT already counted in g_obs",
            "private_Kperp_residual": "0",
            "public_fallback": "requires global EH/coframe/no-extra-TT parent signature",
            "source": "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "KS4346_1_vertical",
            "sector": "K_vertical",
            "private_disposition": "q-vertical/gauge representative; Dq=0; ordinary readout descends",
            "private_Kperp_residual": "0",
            "public_fallback": "prove q-basic action/readout before variation globally",
            "source": "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "KS4346_2_boundary",
            "sector": "K_boundary",
            "private_disposition": "Hamiltonian/radiation boundary charge, not local bulk stress",
            "private_Kperp_residual": "0",
            "public_fallback": "retain finite boundary row if routing fails",
            "source": "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
            "valid_for_claim": "False",
        },
        {
            "sector_id": "KS4346_3_extra_source",
            "sector": "K_extra_source",
            "private_disposition": "absent because the private local action has no independent TT source functional",
            "private_Kperp_residual": "0",
            "public_fallback": "reopen finite tensor score R_i^K <= |W_i^K| N_T/D_T if global clause fails",
            "source": "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
            "valid_for_claim": "False",
        },
    ]


def owner_tail_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "OT4346_0_lambda_RI",
            "symbol": "lambda_RI",
            "definition": "Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI",
            "current_status": "FORMULA_DERIVED_PHYSICAL_VALUE_UNSOURCED",
            "needed_for_next": "real collar spectrum, mass floor and correction bound",
            "source": "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
            "can_score_now": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "OT4346_1_B_Lambda_B_RI",
            "symbol": "B_Lambda, B_RI",
            "definition": "adjoint and owner-block boundary/corner stress",
            "current_status": "CONDITIONAL_ZERO_ROUTE_EXISTS_VALUE_UNSIGNED",
            "needed_for_next": "fixed Dirichlet/decay/routed boundary certificate for S_RI",
            "source": "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
            "can_score_now": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "OT4346_2_I_RI",
            "symbol": "I_RI",
            "definition": "incoming/hyperbolic adjoint mode not killed by static elliptic proof",
            "current_status": "STATIC_COLLAR_ROUTE_EXISTS_HYPERBOLIC_SILENCE_UNSIGNED",
            "needed_for_next": "local branch certificate that no incoming homogeneous adjoint mode contributes",
            "source": "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
            "can_score_now": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "OT4346_3_R_Lambda",
            "symbol": "R_Lambda",
            "definition": "residual forcing in L_RI^dagger Lambda=R_Lambda",
            "current_status": "ZERO_BRANCH_PREFERRED_FINITE_VALUE_UNSOURCED",
            "needed_for_next": "prove exact adjoint equation or source finite residual envelope",
            "source": "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
            "can_score_now": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "OT4346_4_projection",
            "symbol": "Pi_a^RI, Pi_a^BRI, Pi_a^I",
            "definition": "owner-tail transfer constants to each local arena",
            "current_status": "MISSING_ARENA_PROJECTION_CONSTANTS",
            "needed_for_next": "source or derive projection constants before any PPN/R10/clock/orbital score",
            "source": "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
            "can_score_now": "False",
            "valid_for_claim": "False",
        },
        {
            "input_id": "OT4346_5_C_Lambda",
            "symbol": "C_Lambda",
            "definition": "adjoint inverse constant for finite owner-tail branch",
            "current_status": "DERIVED_SHAPE_VALUE_UNSOURCED",
            "needed_for_next": "derive from lambda_RI and boundary/domain constants or keep zero branch",
            "source": "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
            "can_score_now": "False",
            "valid_for_claim": "False",
        },
    ]


def reduced_score_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for observable, bound, units, source in ARENA_GATES:
        rows.append(
            {
                "score_id": f"RED4346_{observable}",
                "arena": observable,
                "arena_bound": bound,
                "units": units,
                "source": source,
                "private_Kperp_contribution": "0",
                "remaining_score_formula": "Y_a = Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI",
                "acceptance_condition": "remaining owner-tail expression <= arena_bound",
                "status": "KPERP_ZERO_PRIVATE_OWNER_TAIL_OPEN",
                "claim_valid": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4346_0_current_private",
            "branch_input": "current corpus through 4345 plus 4234 private Kperp selector",
            "action": "ADOPT_PRIVATE_KPERP_CLEAN_SECTOR_KEEP_OWNER_TAIL_OPEN",
            "output": "Y_a reduces to owner-tail branch only inside private compact selector",
            "claim_policy": "no public local-GR/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4346_1_public_fallback",
            "branch_input": "global/public parent action without no-independent-TT-source signature",
            "action": "RETAIN_KPERP_FINITE_SCORE_ROW",
            "output": "R_i^K <= |W_i^K| N_T/D_T remains the public fallback",
            "claim_policy": "score only after real source-backed W_i^K,N_T,D_T rows",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4346_2_next_owner_tail",
            "branch_input": "Kperp private clean; owner-tail inputs open",
            "action": "TRY_OWNER_TAIL_ZERO_SIGNATURE_OR_REAL_LAMBDA_BOUND",
            "output": NEXT_TARGET,
            "claim_policy": "claim only if lambda_RI, boundary, incoming mode and projections are signed",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4346_0",
            "forbidden_shortcut": "Promoting private Kperp clean sector to public/global local-GR proof",
            "reason": "4234 explicitly keeps the public no-independent-TT-source parent clause unsigned.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4346_1",
            "forbidden_shortcut": "Treating Kperp removal as owner-tail removal",
            "reason": "lambda_RI, B_RI, I_RI, R_Lambda and arena projections remain open.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4346_2",
            "forbidden_shortcut": "Using 4345 smoke lambda as physical collar value",
            "reason": "4345 was a normalized dry run, not the physical collar spectrum.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4346_3",
            "forbidden_shortcut": "Erasing hyperbolic/incoming modes with a static elliptic proof",
            "reason": "the static collar argument does not by itself kill I_RI.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4346_0",
            "decision": DECISION,
            "reason": "the corpus has a source-backed private clean-sector Kperp identity from 4234, but no physical real owner-tail numeric rows yet",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4346_0",
            "item": "Kperp private branch",
            "status": "CLEAN_SECTOR_ADOPTED_PRIVATE",
            "notes": "K_metric_TT/vertical/boundary/extra-source split gives private Kperp residual zero in compact selector.",
        },
        {
            "status_id": "STAT4346_1",
            "item": "Kperp public branch",
            "status": "FINITE_SCORE_RETAINED",
            "notes": "public no-independent-TT-source parent clause remains unsigned.",
        },
        {
            "status_id": "STAT4346_2",
            "item": "owner-tail branch",
            "status": "SOLE_CURRENT_LOCAL_SCORE_BOTTLENECK",
            "notes": "lambda_RI, B_RI, I_RI, R_Lambda and projection constants are the next live targets.",
        },
        {
            "status_id": "STAT4346_3",
            "item": "next target",
            "status": "OWNER_TAIL_ZERO_OR_REAL_BOUND",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4346_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the owner-tail block be made genuinely zero, or must it be bounded with real lambda_RI/boundary/incoming/projection rows?",
            "preferred_route": "prove S_RI parent adoption plus adjoint gap, fixed/routed boundary and no incoming mode so Lambda=B_RI=I_RI=0",
            "fallback_route": "fill real lambda_RI, R_Lambda, B_RI, I_RI, C_Lambda and Pi_a rows and run reduced owner-tail score table",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "clean": clean_sector_rows(),
        "kperp": kperp_sector_rows(),
        "owner": owner_tail_input_rows(),
        "reduced": reduced_score_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 362 PPC4161 fill real owner-tail Kperp values or adopt clean sector

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, source coupling closure, or a fundamental prediction of `G_N`.

## Result

4346 takes the 4345 fork seriously instead of circling it.

The **real owner-tail numeric rows are still not source-backed**: physical `lambda_RI`, `B_RI`, `I_RI`, `R_Lambda`, `C_Lambda`, and arena projections remain open.

But the **Kperp branch can be simplified inside the private compact selector** by importing the source-backed 4234 identity:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source
K_metric_TT    -> ordinary EH/GR TT already counted in g_obs
K_vertical     -> Dq=0, W_i^K=0
K_boundary     -> routed Hamiltonian/radiation charge
K_extra_source -> absent in the private local action
```

Therefore inside this private selector:

```text
N_T = |S_T| + |B_T| + |I_T| + |Z_Tmode| = 0
R_i^K = |W_i^K| N_T/D_T = 0.
```

So the current private local score reduces from:

```text
Y_a = Y_owner_a + Y_Kperp_a
```

to:

```text
Y_a = Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI.
```

That is a real narrowing: the live private local blocker is no longer Kperp; it is the owner-tail/adjoin-boundary-incoming block. Public/global promotion still keeps the finite Kperp fallback row until a global no-independent-TT-source parent clause is signed.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Clean-Sector Clause Audit

{md_table(tables["clean"], ["clause_id", "clause", "private_selector_truth", "public_parent_truth", "source", "effect", "valid_for_claim"])}

## Kperp Sector Disposition

{md_table(tables["kperp"], ["sector_id", "sector", "private_disposition", "private_Kperp_residual", "public_fallback", "source", "valid_for_claim"])}

## Owner-Tail Input Ledger

{md_table(tables["owner"], ["input_id", "symbol", "definition", "current_status", "needed_for_next", "source", "can_score_now", "valid_for_claim"])}

## Reduced Private Score Rows

{md_table(tables["reduced"], ["score_id", "arena", "arena_bound", "units", "private_Kperp_contribution", "remaining_score_formula", "acceptance_condition", "status", "claim_valid", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4346 Y5-R2FR fill real owner-tail Kperp values or adopt clean sector

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4346 adopts the private clean-sector route for `Kperp` and refuses to pretend the owner-tail values are filled.

```text
private Kperp contribution = 0
public Kperp fallback      = retained
remaining private score    = Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI
```

This means the next serious local-GR/Newton step is not another Kperp loop. It is the owner-tail zero proof or a real reduced score runner with physical `lambda_RI`, boundary, incoming-mode and projection rows.

## Handoff

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
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4346 resolves the 4345 real-values-or-clean-sector fork for the private compact selector. "
                    "No physical owner-tail numeric rows are promoted: lambda_RI, B_RI, I_RI, R_Lambda, C_Lambda and arena projections remain open. "
                    "However, importing the source-backed 4234 private Kperp EH/coframe identity lets the private local branch set Kperp's independent static contribution to zero: K_metric_TT is ordinary EH/GR already counted in g_obs, K_vertical has W_i^K=0 by quotient silence, K_boundary is routed, and K_extra_source is absent in the private action. "
                    "Thus the private score narrows to the owner-tail expression alone, while the public/global finite Kperp fallback remains retained until no-independent-TT-source is parent-signed."
                ),
                "4346 source register, clean-sector clause audit, Kperp sector disposition, owner-tail input ledger, reduced private score rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_Kperp_clean_sector_adopted_owner_tail_bottleneck_nonclaim",
                "Prove S_RI owner-tail zero through parent adoption, adjoint gap, fixed/routed boundary and no incoming mode, or fill real reduced owner-tail rows.",
                "Promoting private Kperp clean sector to public local-GR proof; treating Kperp removal as owner-tail removal; using smoke lambda as physical collar spectrum.",
            ]
        )


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4346_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4346_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4346_six_clauses", "six clean-sector clauses are present", len(tables["clean"]) == 6, "clean")
    add("VAL4346_private_clean_true", "all clean-sector clauses are true inside private selector", all(row["private_selector_truth"] == "True" for row in tables["clean"]), "clean")
    add("VAL4346_public_not_promoted", "public parent truth is false for all clean clauses", all(row["public_parent_truth"] == "False" for row in tables["clean"]), "clean")
    add("VAL4346_kperp_sectors", "four Kperp sectors are dispositioned", len(tables["kperp"]) == 4, "kperp")
    add("VAL4346_kperp_zero_private", "all Kperp sectors have zero private residual", all(row["private_Kperp_residual"] == "0" for row in tables["kperp"]), "kperp")
    add("VAL4346_owner_inputs_open", "owner-tail inputs remain not score-ready", all(row["can_score_now"] == "False" for row in tables["owner"]), "owner")
    add("VAL4346_reduced_rows", "reduced rows cover all arenas", len(tables["reduced"]) == len(ARENA_GATES), "reduced")
    add("VAL4346_no_claim_flags", "all generated claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4346_runner_next", "next runner targets owner-tail zero or real lambda bound", any(NEXT_TARGET in row["output"] or NEXT_TARGET in row.get("next_target", "") for row in tables["runner"] + tables["next"]), "runner_next")
    add("VAL4346_docs_exist", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4346_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4346_post_marker", "post marker exists", MARKER in read_text(DOC_PATH), "post")
    add("VAL4346_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4346_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4346_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4346_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4346_SOURCE_REGISTER.csv",
        "clean": SOURCE_DIR / "P8_Y5_R2FR_4346_CLEAN_SECTOR_CLAUSES.csv",
        "kperp": SOURCE_DIR / "P8_Y5_R2FR_4346_KPERP_SECTOR_DISPOSITION.csv",
        "owner": SOURCE_DIR / "P8_Y5_R2FR_4346_OWNER_TAIL_INPUT_LEDGER.csv",
        "reduced": SOURCE_DIR / "P8_Y5_R2FR_4346_REDUCED_PRIVATE_SCORE_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4346_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4346_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4346_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4346_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4346_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = build_tables()
    for key, table_rows in tables.items():
        write_csv(paths[key], table_rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4346 private Kperp clean-sector adoption

Marker: `{MARKER}`

4346 resolves the immediate 4345 fork: it does not find or promote real physical owner-tail values, but it does adopt the source-backed 4234 private Kperp clean-sector identity. Inside the private compact selector, `Kperp` contributes no independent static local force, so the live private local score reduces to:

```text
Y_a = Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI.
```

Public/global promotion still retains the finite Kperp fallback until no-independent-TT-source is signed. The next target is `{NEXT_TARGET}`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4346 packet private Kperp clean-sector adoption

Marker: `{PACKET_MARKER}`

Packet update: the private compact local packet now routes `Kperp` out of the independent static-force budget using the 4234 EH/coframe/vertical/boundary/no-extra-source identity. This does not finish local GR. It moves the active private blocker to the owner-tail row: `lambda_RI`, `B_RI`, `I_RI`, `R_Lambda`, `C_Lambda`, and arena projections.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
