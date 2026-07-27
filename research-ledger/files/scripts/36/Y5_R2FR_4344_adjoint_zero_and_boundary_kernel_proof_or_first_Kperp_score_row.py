from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4344"
CLAIM_ID = "L-185"
BRANCH = "MTS_R2FR_Y5_ADJOINT_ZERO_AND_BOUNDARY_KERNEL_PROOF_OR_FIRST_KPERP_SCORE_ROW_4344"
DECISION = "ADJOINT_ZERO_COERCIVE_STATIC_COLLAR_ROUTE_DERIVED_BOUNDARY_AND_KPERP_SCORE_ROWS_RETAINED_NONCLAIM"
MARKER = "PPC4161_ADJOINT_ZERO_AND_BOUNDARY_KERNEL_PROOF_OR_FIRST_KPERP_SCORE_ROW_4344"
PACKET_MARKER = "PPC4161_PACKET_ADJOINT_ZERO_AND_BOUNDARY_KERNEL_PROOF_OR_FIRST_KPERP_SCORE_ROW_4344"
NEXT_TARGET = "4345-Y5-R2FR-first-source-backed-owner-tail-or-Kperp-score-row.md"

FORMAL_PATH = FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md"
DOC_PATH = POST / "4344-Y5-R2FR-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4344_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

Y_GAMMA_LIMIT = 0.0002739826487147268
Y_BETA_LIMIT = 0.0009529831259642674
Y_CLOCK_LIMIT = 0.0006134828873394971


SOURCES = [
    (
        "SRC4344_00_4343_next",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "4344-Y5-R2FR-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "4343 handoff selecting adjoint zero or Kperp score row.",
    ),
    (
        "SRC4344_01_4343_adjoint",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "L_RI^dagger Lambda_nu = 0 plus boundary/corner terms",
        "Adjoint equation to be attacked.",
    ),
    (
        "SRC4344_02_4343_total_vector",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "Y_a^4343 <= Pi_a^RI C_RI_curved + Pi_a^BRI B_RI + W_a^K C_T(S_T+B_T+I_T+Z_T)",
        "Finite local vector to inherit if zero route fails.",
    ),
    (
        "SRC4344_03_218_LT_coercivity",
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "<K,L_TK> >= (Z_T lambda_D + M_T^2)||K||^2.",
        "Existing coercive-operator template.",
    ),
    (
        "SRC4344_04_218_Kperp_inverse",
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "||K_perp|| <= (|S_T|+|B_T|+|I_T|+|Z_Tmode|)/(Z_T lambda_D + M_T^2).",
        "Kperp inverse bound used for score-row shape.",
    ),
    (
        "SRC4344_05_327_lambda_floor",
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "lambda_* := Z_min lambda_1(D_loc) + M2_min - Eta_H.",
        "Collar positivity template for lambda_RI.",
    ),
    (
        "SRC4344_06_327_poincare_branch",
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "Poincare/Dirichlet collar gap",
        "Boundary/gap branch precedent.",
    ),
    (
        "SRC4344_07_216_boundary_warning",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Firewall for using static collar proof too broadly.",
    ),
    (
        "SRC4344_08_216_bound",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "||K_perp||_E <= C_T (||S_T|| + ||B_T|| + ||I_T|| + ||Z_T||).",
        "Kperp finite bound.",
    ),
    (
        "SRC4344_09_217_score",
        FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md",
        "|W_i^K| C_T (|S_T|+|B_T|+|I_T|+|Z_T|) <= bound_i.",
        "Kperp score inequality.",
    ),
    (
        "SRC4344_10_138_C7",
        FORMAL / "138-metric-null-action-block-contract.md",
        "The metric-null transition block must be covariant without hidden metric stress.",
        "Hidden-stress firewall.",
    ),
    (
        "SRC4344_11_138_C9",
        FORMAL / "138-metric-null-action-block-contract.md",
        "Even if `q_tr` is metric-null:",
        "Kperp remains separate even after owner metric-nullity.",
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
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


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
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
            }
        )
    return rows


def adjoint_rows() -> List[Dict[str, str]]:
    return [
        {
            "adjoint_id": "ADJ4344_0_static_operator",
            "name": "static elliptic adjoint collar operator",
            "statement": "On the compact fixed local collar, use the static adjoint problem L_RI^dagger Lambda=0 with Dirichlet/decay/routed boundary data.",
            "formula": "L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI",
            "status": "STATIC_COLLAR_OPERATOR_DEFINED",
            "valid_for_claim": "False",
        },
        {
            "adjoint_id": "ADJ4344_1_energy_identity",
            "name": "adjoint energy identity",
            "statement": "Multiply L_RI^dagger Lambda=0 by Lambda and integrate over the collar.",
            "formula": "0=<Lambda,L_RI^dagger Lambda>=int[Z_RI|D Lambda|^2+(M_RI^2+V_Ric-E_RI)|Lambda|^2]+B_Lambda",
            "status": "DERIVED_ENERGY_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "adjoint_id": "ADJ4344_2_lambda_RI_floor",
            "name": "adjoint no-kernel floor",
            "statement": "If boundary term is zero/nonnegative and the collar Poincare/mass margin is positive, the only homogeneous adjoint solution is zero.",
            "formula": "lambda_RI := Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI > 0 => ||Lambda||=0",
            "status": "CONDITIONAL_ZERO_PROOF_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "adjoint_id": "ADJ4344_3_hyperbolic_guard",
            "name": "static proof guard",
            "statement": "The coercive proof applies to the fixed static/elliptic local collar only.",
            "formula": "hyperbolic/incoming modes require separate I_RI row",
            "status": "FIREWALL_ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def boundary_rows() -> List[Dict[str, str]]:
    return [
        {
            "boundary_id": "BD4344_0_Dirichlet",
            "route": "Dirichlet/decay Lambda boundary",
            "condition": "Lambda|partial U=0 or Lambda decays on the exterior end; collar geometry fixed under variation",
            "result": "B_Lambda=0 and B_RI=0 for the owner block",
            "status": "BOUNDARY_ZERO_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BD4344_1_routed_boundary",
            "route": "Hamiltonian/radiative routed boundary",
            "condition": "boundary term is not bulk local stress and is routed to boundary/Hamiltonian flux ledger",
            "result": "B_RI becomes a boundary row, not an untracked local metric source",
            "status": "BOUNDARY_ROUTE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "boundary_id": "BD4344_2_failure",
            "route": "boundary/corner failure",
            "condition": "moving collar, unfixed Green data, nonzero Lambda boundary value, or corner term survives",
            "result": "B_RI remains in Y_a^4344",
            "status": "FINITE_BOUND_BRANCH_RETAINED",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4344_0_adjoint_zero",
            "claim": "Adjoint zero on static coercive collar",
            "derivation": "If L_RI^dagger Lambda=0, B_Lambda>=0, Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI>0, then 0>=lambda_RI||Lambda||^2, so Lambda=0.",
            "result": "Lambda=0, so the multiplier stress leg vanishes on this branch",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4344_1_owner_metric_null",
            "claim": "Owner metric-nullity follows from constraint+Lambda+boundary zero",
            "derivation": "T_RI is constraint-proportional plus Lambda-proportional plus B_RI; the constraint equation, Lambda=0 and B_RI=0 imply T_RI=0.",
            "result": "KGamma owner stress is silent only on the signed static-boundary branch",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4344_2_tail_bound",
            "claim": "If adjoint zero fails, the failure is finite and scoreable",
            "derivation": "With residual adjoint source R_Lambda or boundary/correction dominance, ||Lambda||<=C_RI_adj R_Lambda/lambda_RI when lambda_RI>0; otherwise keep unsourced failure row.",
            "result": "Y_owner<=Pi_RI(C_Lambda R_Lambda/lambda_RI)+Pi_BRI B_RI",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4344_3_Kperp_score_gate",
            "claim": "Kperp first score row",
            "derivation": "Combine ||K_perp||_E<=C_T(S_T+B_T+I_T+Z_T) with |R_i^K|<=W_i^K||K_perp||_E.",
            "result": "|R_i^K|<=W_i^K C_T(S_T+B_T+I_T+Z_T) must sit below each arena bound",
            "status": "FIRST_SCORE_ROW_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def score_rows() -> List[Dict[str, str]]:
    return [
        {
            "score_id": "SCR4344_0_owner_zero_branch",
            "arena": "all local arenas",
            "residual": "owner_tail",
            "formula": "Y_owner=0 if lambda_RI>0, B_Lambda=0, B_RI=0, and no hyperbolic incoming mode",
            "acceptance": "conditional theorem only; no empirical claim until parent signs inputs",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "score_id": "SCR4344_1_owner_tail",
            "arena": "PPN/R10/clock/orbital/WEP",
            "residual": "owner_tail",
            "formula": "Y_owner_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI",
            "acceptance": f"PPN_gamma<={Y_GAMMA_LIMIT}; PPN_beta<={Y_BETA_LIMIT}; clock<={Y_CLOCK_LIMIT}; R10/orbital/WEP sourced separately",
            "status": "SCORE_ROW_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "score_id": "SCR4344_2_Kperp_first_row",
            "arena": "PPN/R10/clock/orbital/WEP",
            "residual": "K_extra_source",
            "formula": "Y_Kperp_i := |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)",
            "acceptance": "Y_Kperp_i <= bound_i for every local arena i; coefficients fixed before scoring",
            "status": "FIRST_KPERP_SCORE_ROW_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "score_id": "SCR4344_3_combined",
            "arena": "all local arenas",
            "residual": "owner_tail_plus_Kperp",
            "formula": "Y_a^4344 <= Y_owner_a + |W_a^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)",
            "acceptance": "combined residual below each arena gate with no placeholder rows",
            "status": "COMBINED_NONCLAIM_RUNNER_READY",
            "valid_for_claim": "False",
        },
    ]


def input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4344_0_lambda_RI",
            "symbol": "lambda_RI",
            "definition": "Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI",
            "status": "FORMULA_DERIVED_VALUE_UNSOURCED",
            "next_action": "source collar spectrum, mass floor, and correction bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4344_1_boundary",
            "symbol": "B_Lambda, B_RI",
            "definition": "adjoint integration boundary and owner metric boundary/corner stress",
            "status": "MISSING_ZERO_OR_BOUND",
            "next_action": "fix boundary data or route boundary flux to Hamiltonian ledger",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4344_2_incoming",
            "symbol": "I_RI",
            "definition": "hyperbolic/incoming homogeneous adjoint mode not covered by static collar proof",
            "status": "MISSING_ZERO_OR_BOUND",
            "next_action": "prove static collar is the relevant local branch or source incoming-mode bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4344_3_adj_residual",
            "symbol": "R_Lambda",
            "definition": "residual forcing in L_RI^dagger Lambda=R_Lambda if exact adjoint equation is perturbed",
            "status": "MISSING_IF_NONZERO_BRANCH",
            "next_action": "keep zero branch or source finite residual row",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4344_4_Kperp_coefficients",
            "symbol": "C_T,S_T,B_T,I_T,Z_T,W_i^K",
            "definition": "first Kperp score-row coefficients",
            "status": "MISSING_NUMERIC_SOURCE_ROWS",
            "next_action": "fill first source-backed Kperp row or parent-sign clean sector placement",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4344_5_arena_bounds",
            "symbol": "bound_i, Pi_i",
            "definition": "local arena projection constants and observational gates",
            "status": "MISSING_ARENA_PROJECTION_CONSTANTS",
            "next_action": "fix before any R10/PPN/clock/orbital/WEP score",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4344_0_current",
            "branch_input": "current corpus through 4343",
            "action": "ADOPT_ADJOINT_COERCIVITY_THEOREM_KEEP_CLAIM_FALSE",
            "output": "Lambda=0 theorem derived conditionally; boundary/incoming/Kperp values still open",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4344_1_zero_future",
            "branch_input": "lambda_RI>0, B_Lambda=B_RI=I_RI=0, Kperp clean sector",
            "action": "ALLOW_THIS_OWNER_CHANNEL_ZERO",
            "output": "KGamma owner metric stress and Kperp extra-source channel quiet",
            "claim_policy": "still requires remaining local gates and source coupling/EM gates",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4344_2_score_future",
            "branch_input": "source-backed owner-tail and Kperp rows",
            "action": "RUN_FIRST_NONCLAIM_TAIL_SCORE",
            "output": "score Y_a^4344 against local arena gates",
            "claim_policy": "claim only if all inputs source-backed, fixed before scoring, and below gates",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4344_0",
            "forbidden_shortcut": "Using elliptic/static adjoint proof for hyperbolic incoming modes",
            "reason": "216 explicitly separates static elliptic proof from hyperbolic incoming-mode proof.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4344_1",
            "forbidden_shortcut": "Treating lambda_RI positivity as sourced because the formula exists",
            "reason": "lambda_RI needs spectrum, mass floor, and correction bound.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4344_2",
            "forbidden_shortcut": "Dropping boundary/corner stress after integration by parts",
            "reason": "B_Lambda and B_RI are explicit gates.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4344_3",
            "forbidden_shortcut": "Calling the first Kperp score row an empirical pass",
            "reason": "coefficients are source-row placeholders until numeric and fixed before scoring.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4344_4",
            "forbidden_shortcut": "Promoting this owner-channel result to full local GR",
            "reason": "other P_leak/source-readout, Maxwell/EM stress, source coupling, and empirical robustness gates remain separate.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4344_0",
            "decision": DECISION,
            "reason": "the adjoint multiplier can be killed by a coercive static collar theorem if lambda_RI and boundary conditions are signed; otherwise the first owner-tail/Kperp score row is ready",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4344_0",
            "item": "adjoint zero",
            "status": "CONDITIONAL_COERCIVE_STATIC_COLLAR_PROOF_DERIVED",
            "notes": "Lambda=0 follows from lambda_RI>0 plus boundary silence",
        },
        {
            "status_id": "STAT4344_1",
            "item": "boundary stress",
            "status": "B_LAMBDA_B_RI_EXPLICIT",
            "notes": "boundary/corner terms are retained as zero-or-bound rows",
        },
        {
            "status_id": "STAT4344_2",
            "item": "Kperp score",
            "status": "FIRST_SCORE_ROW_FORMULA_READY",
            "notes": "Y_Kperp_i=|W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)",
        },
        {
            "status_id": "STAT4344_3",
            "item": "next target",
            "status": "SOURCE_BACKED_SCORE_OR_SECTOR_ZERO",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4344_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can lambda_RI, B_RI and incoming-mode silence be source-backed, or should the first numeric owner-tail/Kperp score row be filled?",
            "preferred_route": "source/sign lambda_RI>0, B_Lambda=B_RI=0, I_RI=0, then parent-sign Kperp clean sector",
            "fallback_route": "fill first nonclaim score row for Y_owner_a or Y_Kperp_i with C_T,S_T,B_T,I_T,Z_T,W_i^K and arena bounds",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 360 PPC4161 adjoint zero and boundary kernel proof or first Kperp score row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, source coupling closure, or a fundamental prediction of `G_N`.

## Result

4344 attacks the 4343 adjoint condition instead of merely naming it.

On the fixed static local collar, use:

```text
L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI.
```

Multiply:

```text
L_RI^dagger Lambda = 0
```

by `Lambda` and integrate:

```text
0 = <Lambda,L_RI^dagger Lambda>
  = int[Z_RI |D Lambda|^2 + (M_RI^2+V_Ric-E_RI)|Lambda|^2] + B_Lambda.
```

With fixed/routed boundary and positive collar margin:

```text
lambda_RI := Z_RI,min lambda_1(D_RI) + M_RI,min^2 - Eta_RI > 0,
```

we get:

```text
0 >= lambda_RI ||Lambda||^2
=> Lambda = 0.
```

Then the 4343 owner stress condition closes for this channel only if:

```text
constraint = 0,
Lambda = 0,
B_RI = 0.
```

If any of those fail, the failure is scoreable rather than vague:

```text
Y_owner_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI
           + Pi_a^BRI B_RI
           + Pi_a^I I_RI.
```

The first Kperp score row is also now explicit:

```text
Y_Kperp_i := |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)
```

and must be below each local arena bound if the clean Kperp sector placement remains unsigned.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Adjoint Rows

{md_table(tables["adjoint"], ["adjoint_id", "name", "statement", "formula", "status", "valid_for_claim"])}

## Boundary Rows

{md_table(tables["boundary"], ["boundary_id", "route", "condition", "result", "status", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "claim", "derivation", "result", "status", "valid_for_claim"])}

## Score Rows

{md_table(tables["scores"], ["score_id", "arena", "residual", "formula", "acceptance", "status", "valid_for_claim"])}

## Required Inputs

{md_table(tables["inputs"], ["input_id", "symbol", "definition", "status", "next_action", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4344 Y5-R2FR adjoint zero and boundary kernel proof or first Kperp score row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4344 proves the adjoint-zero route conditionally:

```text
lambda_RI := Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI > 0
and B_Lambda=0
=> Lambda=0.
```

The result is not a claim yet because `lambda_RI`, `B_RI`, and incoming modes need source-backed zero/bound rows. The first Kperp score row is now explicit:

```text
Y_Kperp_i = |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|).
```

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
                    "4344 derives the adjoint-zero route for the KGamma owner on a fixed static local collar. "
                    "For L_RI^dagger=-D_i(Z_RI D^i)+M_RI^2+V_Ric-E_RI, the energy identity gives Lambda=0 if boundary terms vanish or are nonnegative and lambda_RI=Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI is positive. "
                    "This closes the multiplier stress leg only on the static elliptic branch with B_RI=0 and no incoming homogeneous mode. "
                    "If those conditions fail, 4344 keeps the finite owner-tail row Y_owner_a<=Pi_a^RI C_Lambda R_Lambda/lambda_RI+Pi_a^BRI B_RI+Pi_a^I I_RI and creates the first explicit Kperp score row Y_Kperp_i=|W_i^K|C_T(|S_T|+|B_T|+|I_T|+|Z_T|)."
                ),
                "4344 source register, adjoint rows, boundary rows, theorem rows, score rows, required inputs, runner, firewall, decision, status, next-target and validation CSV.",
                "private_adjoint_zero_static_collar_and_first_Kperp_score_row_nonclaim",
                "Source/sign lambda_RI>0, B_RI=0 and incoming-mode silence, or fill first numeric owner-tail/Kperp score row.",
                "Using static elliptic proof for hyperbolic modes; treating lambda_RI positivity as sourced; dropping boundary stress; treating the first Kperp score row as an empirical pass; or promoting this owner-channel result to full local GR.",
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

    add("VAL4344_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4344_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4344_lambda_RI", "lambda_RI formula exists", any("lambda_RI" in row["formula"] for row in tables["adjoint"]), "adjoint")
    add("VAL4344_adjoint_zero", "adjoint zero theorem exists", any(row["theorem_id"] == "TH4344_0_adjoint_zero" and "Lambda=0" in row["result"] for row in tables["theorems"]), "theorems")
    add("VAL4344_boundary_rows", "boundary zero and failure rows exist", any(row["status"] == "BOUNDARY_ZERO_CONDITIONAL" for row in tables["boundary"]) and any(row["status"] == "FINITE_BOUND_BRANCH_RETAINED" for row in tables["boundary"]), "boundary")
    add("VAL4344_owner_tail_score", "owner-tail score row exists", any(row["score_id"] == "SCR4344_1_owner_tail" for row in tables["scores"]), "scores")
    add("VAL4344_kperp_score", "first Kperp score row exists", any(row["score_id"] == "SCR4344_2_Kperp_first_row" and "W_i^K" in row["formula"] for row in tables["scores"]), "scores")
    add("VAL4344_static_firewall", "static/hyperbolic firewall exists", any("hyperbolic" in row["forbidden_shortcut"] for row in tables["firewall"]), "firewall")
    add("VAL4344_inputs_unsourced", "lambda_RI value remains unsourced", any(row["symbol"] == "lambda_RI" and "UNSOURCED" in row["status"] for row in tables["inputs"]), "inputs")
    add("VAL4344_no_claim_flags", "all valid_for_claim flags false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4344_current_runner_nonclaim", "current runner keeps claim false", any(row["runner_id"] == "RUN4344_0_current" and "KEEP_CLAIM_FALSE" in row["action"] for row in tables["runner"]), "runner")
    add("VAL4344_next_target", "next target is 4345 source-backed score row", any("4345" in row["next_target"] for row in tables["next"]), "next")
    add("VAL4344_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4344_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4344_post_handoff", "post doc contains handoff", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4344_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4344_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4344_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4344_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4344_SOURCE_REGISTER.csv",
        "adjoint": SOURCE_DIR / "P8_Y5_R2FR_4344_ADJOINT_ROWS.csv",
        "boundary": SOURCE_DIR / "P8_Y5_R2FR_4344_BOUNDARY_ROWS.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4344_THEOREM_ROWS.csv",
        "scores": SOURCE_DIR / "P8_Y5_R2FR_4344_SCORE_ROWS.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4344_REQUIRED_INPUTS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4344_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4344_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4344_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4344_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4344_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "adjoint": adjoint_rows(),
        "boundary": boundary_rows(),
        "theorems": theorem_rows(),
        "scores": score_rows(),
        "inputs": input_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4344 adjoint zero and first Kperp score row

Marker: `{MARKER}`

4344 derives the static-collar adjoint-zero route:

```text
lambda_RI = Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI > 0
and B_Lambda=0
=> Lambda=0.
```

This makes the `S_RI` owner metric-null only if `B_RI=0` and no incoming homogeneous mode survives. The fallback is now scoreable:

```text
Y_Kperp_i = |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|).
```
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4344 packet adjoint zero and first Kperp score row

Marker: `{PACKET_MARKER}`

Packet update: the KGamma owner stress is reduced to a static-collar coercivity problem plus boundary/incoming-mode gates. If those do not close, the first explicit owner-tail/Kperp score row is ready for source-backed values.
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
