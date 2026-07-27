from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4352"
CLAIM_ID = "L-193"
BRANCH = "MTS_R2FR_Y5_RI_NO_INCOMING_AND_BOUNDARY_SILENCE_OR_FINITE_TAIL_VALUES_4352"
DECISION = "BRI_IRI_ZERO_ON_STATIONARY_COMPACT_ANCHORED_BRANCH_ELSE_FINITE_TAIL_VALUES_NONCLAIM"
MARKER = "PPC4161_RI_NO_INCOMING_AND_BOUNDARY_SILENCE_OR_FINITE_TAIL_VALUES_4352"
PACKET_MARKER = "PPC4161_PACKET_RI_NO_INCOMING_AND_BOUNDARY_SILENCE_OR_FINITE_TAIL_VALUES_4352"
NEXT_TARGET = "4353-Y5-R2FR-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md"

FORMAL_PATH = FORMAL / "368-PPC4161-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md"
DOC_PATH = POST / "4352-Y5-R2FR-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4352_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4352_00_4351_next": (
        FORMAL / "367-PPC4161-RI-owner-tail-zero-application-or-finite-bound-runner.md",
        "4352-Y5-R2FR-RI-no-incoming-and-boundary-silence-or-finite-tail-values.md",
        "4351 handoff selecting boundary/incoming zero or finite values.",
    ),
    "SRC4352_01_4351_BI": (
        FORMAL / "367-PPC4161-RI-owner-tail-zero-application-or-finite-bound-runner.md",
        "B_RI and I_RI are not erased by the Lambda gap alone.",
        "4351 keeps boundary and incoming legs explicit.",
    ),
    "SRC4352_02_4350_anchor": (
        FORMAL / "366-PPC4161-RI-boundary-anchor-and-EtaRI-correction-bound.md",
        "Lambda in H_0^1(D_RI)",
        "4350 anchored multiplier test space.",
    ),
    "SRC4352_03_4344_boundary": (
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "B_Lambda=0 and B_RI=0 for the owner block",
        "4344 Dirichlet/decay boundary route for RI owner block.",
    ),
    "SRC4352_04_4217_corner": (
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0.",
        "4217 differentiability-owned boundary/corner zero theorem.",
    ),
    "SRC4352_05_192_flux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.",
        "No radiation erasure guard for local collar boundaries.",
    ),
    "SRC4352_06_216_guard": (
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Incoming-mode firewall.",
    ),
    "SRC4352_07_190_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "compact, isolated, ordinary-matter local collar",
        "Parent local selector branch context.",
    ),
    "SRC4352_08_4128_stationary": (
        POST / "4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md",
        "For compact stationary isolated local systems, net exterior Poynting leakage `Phi_EM_rad` is zero.",
        "Stationary isolated closed-collar flux precedent.",
    ),
    "SRC4352_09_3915_contract": (
        POST / "3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md",
        "Branch contract:",
        "Stationary local branch contract and residual-vector promotion guard.",
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


def boundary_rows() -> List[Dict[str, str]]:
    return [
        {
            "boundary_id": "BRI4352_0_multiplier_trace",
            "clause": "Lambda in H_0^1(D_RI) and lambda_4350>0",
            "derivation": "The 4350 gap gives Lambda=0 in the adjoint energy norm; hence trace Lambda and the weak normal trace generated by the RI owner integration-by-parts vanish on the anchored residual boundary.",
            "result": "B_Lambda=0 for multiplier-owned boundary terms",
            "status": "CONDITIONAL_ZERO_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BRI4352_1_fixed_domain",
            "clause": "D_RI, normal, corners, Green data and residual representative fixed before variation",
            "derivation": "Moving-domain and corner variations are absent when the local collar/domain is part of the parent selector rather than varied after readout.",
            "result": "B_RI_move=B_RI_corner=0",
            "status": "CONDITIONAL_ZERO_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BRI4352_2_differentiability_owned_boundary",
            "clause": "RI boundary terms are differentiability/exact/reference terms or routed Hamiltonian flux",
            "derivation": "4217 allows differentiability-owned boundary/corner terms to vanish as independent local curl sources; 192 routes nonzero physical flux instead of hiding it.",
            "result": "B_RI_phys=0 inside local bulk; nonzero physical flux is not erased",
            "status": "CONDITIONAL_ZERO_OR_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BRI4352_3_boundary_zero_theorem",
            "clause": "BRI4352_0 through BRI4352_2 hold in the same collar",
            "derivation": "Every local RI boundary/corner contribution is either multiplier-owned and killed by Lambda=0, fixed/exact, or routed out of the local bulk ledger.",
            "result": "B_RI=0",
            "status": "EXACT_ZERO_IF_BRANCH_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BRI4352_4_boundary_fallback",
            "clause": "any boundary/corner/flux clause unsigned",
            "derivation": "No cancellation is allowed; the local owner-tail receives the absolute boundary envelope.",
            "result": "|B_RI| <= B_trace + B_move + B_corner + B_source_cross + B_rad + B_improvement",
            "status": "FINITE_BOUND_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def incoming_rows() -> List[Dict[str, str]]:
    return [
        {
            "incoming_id": "IRI4352_0_static_not_enough",
            "clause": "static elliptic Lambda gap",
            "derivation": "The 4350 elliptic gap kills homogeneous static adjoint modes only inside the selected elliptic collar.",
            "result": "does not by itself kill hyperbolic incoming memory",
            "status": "FIREWALL_RESTATED",
            "valid_for_claim": "False",
        },
        {
            "incoming_id": "IRI4352_1_stationary_selector",
            "clause": "parent-owned stationary compact local branch",
            "derivation": "If Lie_tau of the RI owner data vanishes, the local domain is compact/isolated, and no incoming boundary data are admitted, the hyperbolic completion has no independent incoming RI datum in the local branch.",
            "result": "I_RI=0 for stationary isolated local selector",
            "status": "CONDITIONAL_ZERO_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "incoming_id": "IRI4352_2_closed_collar_flux",
            "clause": "no imposed incoming radiation/source crossing/open-memory pullback",
            "derivation": "192 and 4128 support the closed-collar treatment: nonzero flux is a boundary/Hamiltonian row, while the compact stationary isolated branch has no net incoming leakage.",
            "result": "incoming flux does not enter the local bulk owner tail",
            "status": "CONDITIONAL_ZERO_OR_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "incoming_id": "IRI4352_3_no_incoming_theorem",
            "clause": "IRI4352_1 plus IRI4352_2 hold with finite-energy regularity",
            "derivation": "The admissible RI tail space is the stationary homogeneous static space already killed by lambda_4350; there is no separate incoming datum to add.",
            "result": "I_RI=0",
            "status": "EXACT_ZERO_IF_BRANCH_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "incoming_id": "IRI4352_4_incoming_fallback",
            "clause": "radiative, driven, nonstationary, source-crossing or open-memory branch",
            "derivation": "The incoming channel is retained as an energy/flux amplitude rather than erased by the static proof.",
            "result": "|I_RI| <= C_in sqrt(E_RI,in) + C_flux |Phi_RI,in| + C_mem |M_open|",
            "status": "FINITE_BOUND_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def tail_value_rows() -> List[Dict[str, str]]:
    return [
        {
            "tail_id": "TAIL4352_0_full_clean",
            "branch": "stationary compact anchored RI clean branch",
            "B_RI": "0",
            "I_RI": "0",
            "R_Lambda": "0",
            "tail_value": "Y_owner_a=0",
            "status": "ZERO_IF_PARENT_BRANCH_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4352_1_boundary_open",
            "branch": "lambda_4350 positive but boundary/corner open",
            "B_RI": "B_trace+B_move+B_corner+B_source_cross+B_rad+B_improvement",
            "I_RI": "0 if stationary no-incoming signed, otherwise I_bound",
            "R_Lambda": "R_Lambda",
            "tail_value": "|Pi_RI|C_Lambda|R_Lambda|/lambda_4350 + |Pi_BRI||B_RI| + |Pi_I||I_RI|",
            "status": "FINITE_BOUND_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4352_2_incoming_open",
            "branch": "lambda_4350 positive but incoming/open-memory/radiative branch",
            "B_RI": "0 if boundary signed, otherwise B_bound",
            "I_RI": "C_in sqrt(E_RI,in)+C_flux|Phi_RI,in|+C_mem|M_open|",
            "R_Lambda": "R_Lambda",
            "tail_value": "|Pi_RI|C_Lambda|R_Lambda|/lambda_4350 + |Pi_BRI||B_RI| + |Pi_I||I_RI|",
            "status": "FINITE_BOUND_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4352_3_denominator_open",
            "branch": "lambda_4350 not positive/source-backed",
            "B_RI": "unscored",
            "I_RI": "unscored",
            "R_Lambda": "unscored",
            "tail_value": "owner-tail runner blocked until lambda_4350>0 or finite inverse row exists",
            "status": "CLAIM_BLOCKED",
            "valid_for_claim": "False",
        },
    ]


def branch_matrix_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "BM4352_0_local_static_closed",
            "branch": "local static closed collar",
            "B_RI_status": "ZERO_IF_BRANCH_SIGNED",
            "I_RI_status": "ZERO_IF_BRANCH_SIGNED",
            "owner_tail_result": "Y_owner=0",
            "claim_policy": "private branch theorem only",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BM4352_1_stationary_but_boundary_flux",
            "branch": "stationary with routed physical boundary flux",
            "B_RI_status": "bulk zero; physical flux routed",
            "I_RI_status": "zero if no incoming datum",
            "owner_tail_result": "local owner tail zero only after routed flux excluded from bulk score",
            "claim_policy": "no erasure of flux",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BM4352_2_open_radiative",
            "branch": "radiative/driven/nonstationary",
            "B_RI_status": "finite boundary envelope",
            "I_RI_status": "finite incoming envelope",
            "owner_tail_result": "finite residual scoring branch",
            "claim_policy": "no local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BM4352_3_public_global",
            "branch": "public/global MTS without branch signatures",
            "B_RI_status": "not zero",
            "I_RI_status": "not zero",
            "owner_tail_result": "retain finite rows",
            "claim_policy": "public promotion blocked",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, bound, units in ARENAS:
        rows.append(
            {
                "arena_id": f"OT4352_{arena}",
                "arena": arena,
                "arena_bound": bound,
                "units": units,
                "clean_branch_owner_tail": "0",
                "finite_tail_expression": "|Pi_a^RI|C_Lambda|R_Lambda|/lambda_4350 + |Pi_a^BRI||B_RI_bound| + |Pi_a^I||I_RI_bound|",
                "remaining_inputs_if_not_clean": "Pi_a, C_Lambda, R_Lambda, lambda_4350, B_RI_bound, I_RI_bound",
                "status": "ZERO_IF_FULL_BRANCH_ELSE_FINITE_VALUES_MISSING",
                "claim_valid": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4352_0_clean",
            "input": "4350 gap + 4351 owner theorem + BRI4352_3 + IRI4352_3",
            "action": "SET_BRI_IRI_ZERO_INSIDE_PRIVATE_STATIC_SELECTOR",
            "result": "full owner-tail branch has Y_owner=0",
            "claim_policy": "private nonclaim; remaining local-GR/source-readout gates still separate",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4352_1_boundary_open",
            "input": "boundary/corner/flux clause unsigned",
            "action": "KEEP_BRI_BOUND",
            "result": "owner-tail finite row retains |Pi_BRI||B_RI_bound|",
            "claim_policy": "score only after sourced finite values",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4352_2_incoming_open",
            "input": "stationary/no-incoming clause unsigned",
            "action": "KEEP_IRI_BOUND",
            "result": "owner-tail finite row retains |Pi_I||I_RI_bound|",
            "claim_policy": "static proof alone not enough",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4352_3_next",
            "input": "B_RI/I_RI zero-or-bound fork recorded",
            "action": "PROPAGATE_FULL_CLEAN_OR_SCORE_FINITE_VECTOR",
            "result": NEXT_TARGET,
            "claim_policy": "carry branch labels into local residual vector",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4352_0",
            "rule": "Do not set B_RI=0 from no-flux alone.",
            "reason": "The RI boundary term is zero only when multiplier traces, fixed domain/corners and differentiability/routing clauses all hold.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4352_1",
            "rule": "Do not set I_RI=0 from the static elliptic energy identity alone.",
            "reason": "Incoming modes require a stationary/no-incoming selector or finite incoming flux bound.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4352_2",
            "rule": "Do not erase physical radiation, source crossing or open-memory pullback.",
            "reason": "Such terms are routed or bounded, not converted into local bulk silence.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4352_3",
            "rule": "Do not mix clean-branch zero rows with open-branch finite rows.",
            "reason": "B_RI=0 and I_RI=0 must hold in the same compact static branch as lambda_4350>0.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4352_0",
            "decision": DECISION,
            "reason": "The same compact anchored stationary selector can close B_RI and I_RI: multiplier traces vanish after the 4350 gap, fixed boundary/corner data remove local boundary stress, and the stationary isolated no-incoming branch leaves no independent hyperbolic RI datum. Open/radiative/nonstationary branches keep finite B_RI and I_RI envelopes.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4352_0",
            "item": "B_RI",
            "status": "ZERO_ON_MULTIPLIER_TRACE_FIXED_BOUNDARY_BRANCH",
            "note": "otherwise finite boundary/corner/flux envelope remains.",
        },
        {
            "status_id": "STAT4352_1",
            "item": "I_RI",
            "status": "ZERO_ON_STATIONARY_NO_INCOMING_BRANCH",
            "note": "otherwise finite incoming/radiative/open-memory envelope remains.",
        },
        {
            "status_id": "STAT4352_2",
            "item": "owner-tail clean branch",
            "status": "FULL_PRIVATE_ZERO_BRANCH_AVAILABLE_CONDITIONALLY",
            "note": "lambda_4350>0, B_RI=0 and I_RI=0 can now be combined only with same-branch labels.",
        },
        {
            "status_id": "STAT4352_3",
            "item": "next target",
            "status": "PROPAGATE_OR_SCORE",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4352_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the full clean owner-tail zero branch be propagated into the local residual vector, or must finite B_RI/I_RI/lambda_4350 values be scored?",
            "preferred_route": "propagate Y_owner=0 through the compact static private selector and identify remaining non-owner local-GR/source-readout gates",
            "fallback_route": "fill finite B_RI_bound, I_RI_bound, R_Lambda, C_Lambda, Pi_a, ell_RI and Eta_RI,total rows for arena scoring",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "boundary": boundary_rows(),
        "incoming": incoming_rows(),
        "tails": tail_value_rows(),
        "branches": branch_matrix_rows(),
        "arenas": arena_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4352_SOURCE_REGISTER.csv",
        "boundary": "P8_Y5_R2FR_4352_BOUNDARY_SILENCE_ROWS.csv",
        "incoming": "P8_Y5_R2FR_4352_NO_INCOMING_ROWS.csv",
        "tails": "P8_Y5_R2FR_4352_FINITE_TAIL_VALUE_ROWS.csv",
        "branches": "P8_Y5_R2FR_4352_BRANCH_MATRIX.csv",
        "arenas": "P8_Y5_R2FR_4352_ARENA_UPDATE_ROWS.csv",
        "runner": "P8_Y5_R2FR_4352_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4352_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4352_DECISION.csv",
        "status": "P8_Y5_R2FR_4352_STATUS.csv",
        "next": "P8_Y5_R2FR_4352_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 368 PPC4161 RI no-incoming and boundary silence or finite tail values

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint closes the owner-tail `B_RI` and `I_RI` legs only inside a compact stationary anchored local selector. It does not prove public local GR, Newton, Maxwell/QED, calibrated `G_N`, R10, PPN, clock, orbital, or WEP safety.

## Result

4352 finishes the clean owner-tail branch conditionally:

```text
lambda_4350 > 0,
Lambda in H_0^1(D_RI),
fixed RI domain/corners/normal,
differentiability-owned or routed boundary terms,
stationary isolated no-incoming local selector

=> B_RI = 0,
=> I_RI = 0,
=> Y_owner_a = 0.
```

The derivation is not "no-flux therefore zero." It is sharper:

```text
B_RI = B_trace[Lambda,D Lambda] + B_move + B_corner + B_phys/routed.
```

The 4350 gap gives `Lambda=0` in the anchored energy domain, so the multiplier-owned trace part vanishes. Fixed domain/corner data remove `B_move` and `B_corner`. Physical radiation/source-crossing is either absent in the stationary closed collar or routed/bounded as a boundary/Hamiltonian term, not hidden as local bulk stress.

For incoming modes:

```text
I_RI = 0
```

only when the parent selector chooses the stationary compact isolated branch with no incoming RI datum. The static elliptic proof alone is not enough.

If any clause fails, the owner-tail branch is finite:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI_bound|
       + |Pi_a^I||I_RI_bound|.
```

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Boundary Silence Rows

{md_table(tables["boundary"], ["boundary_id", "clause", "derivation", "result", "status", "valid_for_claim"])}

## No-Incoming Rows

{md_table(tables["incoming"], ["incoming_id", "clause", "derivation", "result", "status", "valid_for_claim"])}

## Finite Tail Value Rows

{md_table(tables["tails"], ["tail_id", "branch", "B_RI", "I_RI", "R_Lambda", "tail_value", "status", "valid_for_claim"])}

## Branch Matrix

{md_table(tables["branches"], ["branch_id", "branch", "B_RI_status", "I_RI_status", "owner_tail_result", "claim_policy", "valid_for_claim"])}

## Arena Update Rows

{md_table(tables["arenas"], ["arena_id", "arena", "arena_bound", "units", "clean_branch_owner_tail", "finite_tail_expression", "remaining_inputs_if_not_clean", "status", "claim_valid", "valid_for_claim"])}

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
    post = f"""# 4352 Y5-R2FR RI no-incoming and boundary silence or finite tail values

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4352 conditionally closes the two owner-tail legs left by 4351:

```text
B_RI=0 and I_RI=0
```

on the same compact anchored stationary branch as `lambda_4350>0`. If the branch is open/radiative/nonstationary, the fallback is no longer vague:

```text
|Y_a| <= |Pi_a^RI|C_Lambda|R_Lambda|/lambda_4350
       + |Pi_a^BRI||B_RI_bound|
       + |Pi_a^I||I_RI_bound|.
```

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
                    "4352 derives the conditional zero route for the two owner-tail legs left open by 4351. In the same compact anchored stationary selector as the 4350 positive gap, Lambda in H_0^1(D_RI) plus lambda_4350>0 kills multiplier-owned boundary traces, fixed domain/corner data remove moving-boundary and corner stress, and differentiability-owned or routed boundary terms give B_RI=0. The incoming leg I_RI=0 only when the parent selects the stationary isolated no-incoming local branch; static elliptic positivity alone is not used to erase incoming modes. Open/radiative/nonstationary branches retain finite B_RI and I_RI envelopes in the owner-tail score. No public local-GR/Newton/R10/PPN claim fires."
                ),
                (
                    "4352 source register, boundary silence rows, no-incoming rows, finite tail value rows, branch matrix, arena updates, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "private_BRI_IRI_zero_on_stationary_compact_anchored_branch_else_finite_tail_values_nonclaim",
                (
                    "Propagate the full clean owner-tail zero into the local residual vector, or fill finite B_RI_bound, I_RI_bound, R_Lambda, C_Lambda, Pi_a, ell_RI and Eta_RI,total rows for scoring."
                ),
                (
                    "Setting B_RI=0 from no-flux alone; setting I_RI=0 from static elliptic positivity alone; erasing physical radiation/source crossing/open-memory pullback; mixing clean-branch zero rows with open-branch finite rows."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4352 RI no-incoming and boundary silence or finite tail values

Marker: `{MARKER}`

4352 conditionally closes the remaining owner-tail legs. In the compact anchored stationary branch, the 4350 gap gives `Lambda=0` in the residual test space; fixed domain/corner data plus differentiability-owned/routed boundary terms then give `B_RI=0`. If the same parent selector is stationary, isolated, and admits no incoming RI datum, `I_RI=0` as well. Thus the private clean owner-tail branch has:

```text
Y_owner_a=0.
```

Open/radiative/nonstationary branches retain finite `B_RI_bound` and `I_RI_bound` terms with no cancellation credit.
"""
    packet_block = f"""

## PPC4161 packet update 4352 BRI/IRI zero-or-bound fork

Marker: `{PACKET_MARKER}`

Packet update: `B_RI` and `I_RI` now have theorem-zero clauses on the same stationary compact anchored branch as `lambda_4350>0`. The owner-tail is clean only inside that branch; otherwise the finite bound keeps `B_RI_bound` and `I_RI_bound` explicit.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    formal_text = read_text(FORMAL_PATH)
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in formal_text, MARKER))
    checks.append(("decision_in_formal", DECISION in formal_text, DECISION))
    checks.append(("BRI_zero_present", "=> B_RI = 0" in formal_text, "B_RI zero"))
    checks.append(("IRI_zero_present", "=> I_RI = 0" in formal_text, "I_RI zero"))
    checks.append(("finite_bound_present", "|Pi_a^BRI||B_RI_bound|" in formal_text, "finite bound"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("boundary_rows_present", len(tables["boundary"]) >= 5, str(len(tables["boundary"]))))
    checks.append(("incoming_rows_present", len(tables["incoming"]) >= 5, str(len(tables["incoming"]))))
    checks.append(("tail_rows_present", len(tables["tails"]) >= 4, str(len(tables["tails"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("no_flux_firewall_present", "no-flux alone" in formal_text, "no-flux firewall"))
    checks.append(("static_incoming_firewall_present", "static elliptic proof alone is not enough" in formal_text, "incoming firewall"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4352_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4352_BOUNDARY_SILENCE_ROWS.csv",
        "P8_Y5_R2FR_4352_NO_INCOMING_ROWS.csv",
        "P8_Y5_R2FR_4352_FINITE_TAIL_VALUE_ROWS.csv",
        "P8_Y5_R2FR_4352_BRANCH_MATRIX.csv",
        "P8_Y5_R2FR_4352_ARENA_UPDATE_ROWS.csv",
        "P8_Y5_R2FR_4352_RUNNER.csv",
        "P8_Y5_R2FR_4352_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4352_DECISION.csv",
        "P8_Y5_R2FR_4352_STATUS.csv",
        "P8_Y5_R2FR_4352_NEXT_TARGET.csv",
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
    print(f"{CHECKPOINT}: wrote 11 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
