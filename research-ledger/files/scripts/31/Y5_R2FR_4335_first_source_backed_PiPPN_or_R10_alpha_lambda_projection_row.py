from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4335"
CLAIM_ID = "L-176"
BRANCH = "MTS_R2FR_Y5_FIRST_SOURCE_BACKED_PIPPN_OR_R10_ALPHA_LAMBDA_PROJECTION_ROW_4335"
DECISION = "STANDARD_ZERO_PPN_SMOKE_ROW_SOURCE_BACKED_NONCLAIM_OPEN_TAIL_PIPPN_AND_R10_REMAIN_BLOCKED"
MARKER = "PPC4161_FIRST_SOURCE_BACKED_PIPPN_OR_R10_ALPHA_LAMBDA_PROJECTION_ROW_4335"
PACKET_MARKER = "PPC4161_PACKET_FIRST_SOURCE_BACKED_PIPPN_OR_R10_ALPHA_LAMBDA_PROJECTION_ROW_4335"
NEXT_TARGET = "4336-Y5-R2FR-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md"

FORMAL_PATH = FORMAL / "351-PPC4161-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md"
DOC_PATH = POST / "4335-Y5-R2FR-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4335_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4335_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4334_NEXT_TARGET.csv",
        "genuine nonclaim smoke score",
        "4334 handoff asking whether one projection row can be made scoreable.",
    ),
    (
        "SRC4335_01_4334_PPN_gate",
        FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md",
        "score_PPN only if Pi_PPN maps T_open",
        "4334 open-tail PPN scoring gate.",
    ),
    (
        "SRC4335_02_4333_closure",
        FORMAL / "349-PPC4161-standard-branch-source-readout-rollup-or-open-tail-test-pack.md",
        "=> epsilon_source_readout=0.",
        "4333 standard branch closure implication.",
    ),
    (
        "SRC4335_03_PPN_gamma",
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "gamma = 1.",
        "Formal PPN readout gamma value in closed private packet.",
    ),
    (
        "SRC4335_04_PPN_beta",
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "beta = 1.",
        "Formal PPN readout beta value in closed private packet.",
    ),
    (
        "SRC4335_05_PPN_vector",
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "Full PPN residual vector definition.",
    ),
    (
        "SRC4335_06_gamma_bound",
        FORMAL / "59-local-ppn-branch-framework.md",
        "`delta_gamma` | `<= 1e-5`",
        "Internal conservative PPN gamma bound used for dry gate.",
    ),
    (
        "SRC4335_07_beta_bound",
        FORMAL / "59-local-ppn-branch-framework.md",
        "`delta_beta` | `<= 1e-4`",
        "Internal conservative PPN beta bound used for dry gate.",
    ),
    (
        "SRC4335_08_open_metric_block",
        FORMAL / "60-local-ppn-branch-first-results.md",
        "Current real branch has no metric tensor solution.",
        "Existing warning that open-tail PPN still needs a metric solution.",
    ),
    (
        "SRC4335_09_R10_563",
        POST / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "MTS alpha rows require Z_X, M_X^2, numerator coefficients",
        "R10 alpha(lambda) is blocked by parent coefficient absence.",
    ),
    (
        "SRC4335_10_R10_982",
        SOURCE_DIR / "P8_Y5_R10_982_PROJECTION_MATRIX_SKELETON.csv",
        "PMAT982_4_R10_alpha_lambda",
        "Existing R10 alpha(lambda) projection skeleton.",
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


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                "4335 fills the first scoreable nonclaim local-test row by separating the standard-zero PPN branch from the open-tail projection problem. In the closed PPC4161 standard branch, the sourced private PPN readout has gamma=1, beta=1 and R_PPN=0, so a dry gamma/beta smoke row gives delta_gamma=0<=1e-5 and delta_beta=0<=1e-4. This is source-backed by the internal PPN readout and PPN gate documents, but it remains valid_for_claim=false because it only tests the branch closure, not the open-tail metric-transfer matrix. Open-tail Pi_PPN remains blocked by MISSING_LOCAL_METRIC_TRANSFER_MATRIX, and R10 alpha(lambda) remains blocked by missing Z_X, M_X^2, numerator coefficients and full claim-valid bound curve inputs.",
                "4335 source register, candidate decision rows, standard-zero PPN projection/smoke rows, open-tail blocker rows, R10 blocker rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_standard_zero_PPN_smoke_pass_open_tail_projection_blocked_nonclaim",
                "Derive the open-tail Pi_PPN metric-transfer matrix from K_tr,loc/q_loc data, or fill R10 parent alpha(lambda) coefficients plus real bound curve inputs.",
                "Using the zero-branch PPN smoke as an empirical local-GR claim; applying gamma=beta=1 to open-tail branches; using identity Pi_PPN for real tails; or scoring R10 while parent alpha coefficients or bound curve rows remain missing.",
            ]
        )


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, path, needle, role in SOURCES:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "line_number": find_line(path, needle),
                "role": role,
            }
        )
    return rows


def candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "CAND4335_0_PPN_standard_zero",
            "arena": "PPN gamma/beta",
            "candidate_route": "closed standard branch PPN readout",
            "available_sources": "188 gamma=1 beta=1 R_PPN=0; 59 gamma/beta bounds; 4333 closure",
            "result": "RUN_NONCLAIM_ZERO_BRANCH_SMOKE",
            "reason": "branch-zero residual vector is source-backed enough for a dry sanity score",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAND4335_1_PPN_open_tail",
            "arena": "PPN open-tail transfer",
            "candidate_route": "Pi_PPN T_open",
            "available_sources": "4334 matrix contract; 59/60 PPN framework",
            "result": "BLOCKED",
            "reason": "metric transfer matrix from T_open/K_tr,loc/q_loc to gamma/beta is missing",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "CAND4335_2_R10_alpha_lambda",
            "arena": "R10 alpha(lambda)",
            "candidate_route": "Pi_R10(lambda) T_open or K_X Qbar_XH qbar_XT alpha row",
            "available_sources": "563 anchor smoke; 982 skeleton",
            "result": "BLOCKED",
            "reason": "parent alpha coefficients and full claim-valid bound curve inputs remain missing",
            "valid_for_claim": "False",
        },
    ]


def ppn_zero_row() -> List[Dict[str, str]]:
    return [
        {
            "projection_id": "PIPPN4335_0_standard_zero_gamma_beta",
            "arena": "PPN/Cassini/local solar tests",
            "branch": "closed_standard_PPC4161_private_packet",
            "tail_vector_condition": "T_open=0 and 4333 standard branch closure clauses hold",
            "projection_statement": "R_PPN_standard=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G)=0",
            "numeric_matrix_present": "not_required_for_zero_tail_vector",
            "source_status": "SOURCE_BACKED_DERIVED_ZERO_BRANCH",
            "scoreable_nonclaim": "True",
            "valid_for_claim": "False",
        }
    ]


def ppn_smoke_rows() -> List[Dict[str, str]]:
    return [
        {
            "smoke_id": "PPN4335_0_delta_gamma",
            "quantity": "delta_gamma",
            "predicted_value": "0.0",
            "bound_value": "1.0e-5",
            "bound_units": "dimensionless",
            "pass_nonclaim": "True",
            "source_basis": "188 gamma=1; 59 delta_gamma internal bound",
            "valid_for_claim": "False",
        },
        {
            "smoke_id": "PPN4335_1_delta_beta",
            "quantity": "delta_beta",
            "predicted_value": "0.0",
            "bound_value": "1.0e-4",
            "bound_units": "dimensionless",
            "pass_nonclaim": "True",
            "source_basis": "188 beta=1; 59 delta_beta internal bound",
            "valid_for_claim": "False",
        },
    ]


def blocker_rows() -> List[Dict[str, str]]:
    return [
        {
            "blocker_id": "BLK4335_0_open_PiPPN",
            "blocked_route": "Pi_PPN open-tail scoring",
            "missing_input": "MISSING_LOCAL_METRIC_TRANSFER_MATRIX",
            "needed_for_release": "derive or source mapping from T_open/K_tr,loc/q_loc Green solution to gamma,beta,preferred-frame and Gdot components",
            "current_status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4335_1_q_profile",
            "blocked_route": "physical nonzero local PPN branch",
            "missing_input": "MISSING_QLOC_PROFILE_BOUNDARY_AMPLITUDE",
            "needed_for_release": "q_loc(x), boundary conditions and amplitude law sufficient to solve A_loc/K_tr,loc and metric response",
            "current_status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4335_2_R10_parent_alpha",
            "blocked_route": "R10 alpha(lambda) score",
            "missing_input": "MISSING_R10_PARENT_COEFFICIENTS",
            "needed_for_release": "Z_X, M_X^2, K_X, Qbar_XH(lambda), qbar_XT/P_A source-backed rows",
            "current_status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4335_3_R10_bound_curve",
            "blocked_route": "R10 alpha(lambda) claim curve",
            "missing_input": "MISSING_FULL_CLAIM_VALID_ALPHA_LAMBDA_BOUND_CURVE",
            "needed_for_release": "digitized or machine-readable alpha(lambda) curve with QA, not only alpha=1 threshold anchors",
            "current_status": "blocked",
            "valid_for_claim": "False",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4335_0_standard_zero_ppn",
            "name": "closed-branch PPN residual",
            "formula": "gamma=1 and beta=1 in the closed private packet => delta_gamma=0 and delta_beta=0",
            "status": "SOURCE_BACKED_NONCLAIM_SMOKE",
        },
        {
            "formula_id": "F4335_1_gamma_score",
            "name": "gamma dry score",
            "formula": "abs(delta_gamma)=0 <= 1e-5",
            "status": "PASS_NONCLAIM_ZERO_BRANCH_ONLY",
        },
        {
            "formula_id": "F4335_2_beta_score",
            "name": "beta dry score",
            "formula": "abs(delta_beta)=0 <= 1e-4",
            "status": "PASS_NONCLAIM_ZERO_BRANCH_ONLY",
        },
        {
            "formula_id": "F4335_3_open_tail_PiPPN",
            "name": "open-tail PPN requirement",
            "formula": "R_PPN_open=Pi_PPN T_open requires Pi_PPN from metric-transfer/Green-function data before scoring",
            "status": "BLOCKED",
        },
        {
            "formula_id": "F4335_4_R10_requirement",
            "name": "R10 alpha(lambda) requirement",
            "formula": "score_R10 requires numeric alpha_pred(lambda)=K_X Qbar_XH(lambda) qbar_XT/(4*pi*Z_X*G_obs) and claim-valid alpha_bound(lambda)",
            "status": "BLOCKED",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4335_0_standard_zero_PPN",
            "branch_input": "closed standard private packet; T_open=0",
            "action": "RUN_ZERO_BRANCH_SMOKE",
            "output": "delta_gamma=0, delta_beta=0 pass internal dry bounds",
            "claim_policy": "valid_for_claim=false; branch sanity only",
        },
        {
            "runner_id": "RUN4335_1_open_tail_PPN",
            "branch_input": "T_open nonzero or open-tail branch",
            "action": "BLOCK_SCORE",
            "output": "blocked_missing_local_metric_transfer_matrix",
            "claim_policy": "no local claim",
        },
        {
            "runner_id": "RUN4335_2_R10_alpha",
            "branch_input": "R10 alpha(lambda) row",
            "action": "BLOCK_SCORE",
            "output": "blocked_missing_parent_alpha_coefficients_or_bound_curve",
            "claim_policy": "no R10 claim",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4335_0_zero_branch_overclaim",
            "forbidden_shortcut": "use standard-zero PPN smoke as empirical local-GR pass",
            "reason": "it tests only the closed branch readout, not open-tail metric transfer or arena data",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4335_1_apply_zero_to_open",
            "forbidden_shortcut": "apply gamma=beta=1 to open-tail branches",
            "reason": "open tails require Pi_PPN metric-transfer matrix and q_loc/K_tr,loc solution",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4335_2_identity_PiPPN",
            "forbidden_shortcut": "use identity Pi_PPN for real tails",
            "reason": "projection coefficients must be derived/source-backed, not debug assumptions",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4335_3_R10_anchor_overclaim",
            "forbidden_shortcut": "score R10 from alpha=1 anchors or symbolic alpha_pred",
            "reason": "full curve and parent coefficients are required before even nonclaim numeric scoring",
            "status": "BLOCK",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "One source-backed nonclaim smoke row now runs: standard-zero PPN gamma/beta gives zero residuals against internal dry bounds. Open-tail Pi_PPN and R10 alpha(lambda) remain blocked for exactly named reasons.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4335_0_zero_branch",
            "item": "standard-zero PPN gamma/beta",
            "status": "NONCLAIM_SMOKE_PASS",
            "notes": "delta_gamma=0 and delta_beta=0 pass internal dry bounds",
        },
        {
            "status_id": "STAT4335_1_open_PPN",
            "item": "open-tail Pi_PPN",
            "status": "BLOCKED",
            "notes": "metric-transfer matrix from T_open/K_tr,loc/q_loc missing",
        },
        {
            "status_id": "STAT4335_2_R10",
            "item": "R10 alpha(lambda)",
            "status": "BLOCKED",
            "notes": "parent alpha coefficients and full claim-valid curve missing",
        },
        {
            "status_id": "STAT4335_3_next",
            "item": "open-tail metric transfer or R10 coefficient fill",
            "status": "NEXT_TARGET",
            "notes": "derive Pi_PPN first; if blocked, fill R10 parent-alpha inputs",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4335_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the open-tail Pi_PPN metric-transfer matrix be derived from K_tr,loc/q_loc, or should effort pivot to filling R10 parent-alpha coefficient rows?",
            "preferred_route": "derive Pi_PPN gamma/beta transfer from the longitudinal tensor ansatz, Green-function source profile and boundary conditions",
            "fallback_route": "fill R10 Z_X, M_X^2, K_X, Qbar_XH, qbar_XT and alpha_bound(lambda) rows enough for a nonclaim numeric alpha smoke score",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 351 - PPC4161 first source-backed PiPPN or R10 alpha(lambda) projection row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4335 does **not** prove public local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, Maxwell/QED, charge normalization, or a numerical value of `G_N`.

It runs the first honest local-test smoke row that is actually source-backed enough to evaluate: the **closed standard PPN zero branch**. This is not the open-tail `Pi_PPN` matrix. It is the branch-sanity score:

```text
closed standard branch:
gamma = 1,
beta = 1,
R_PPN = 0

abs(delta_gamma)=0 <= 1e-5
abs(delta_beta)=0 <= 1e-4
```

Open-tail `Pi_PPN` and R10 `alpha(lambda)` remain blocked.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Candidate Decision

{md_table(tables["candidates"], ["candidate_id", "arena", "candidate_route", "available_sources", "result", "reason", "valid_for_claim"])}

## Standard-Zero PPN Row

{md_table(tables["ppn_zero"], ["projection_id", "arena", "branch", "tail_vector_condition", "projection_statement", "numeric_matrix_present", "source_status", "scoreable_nonclaim", "valid_for_claim"])}

## PPN Smoke Score

{md_table(tables["ppn_smoke"], ["smoke_id", "quantity", "predicted_value", "bound_value", "bound_units", "pass_nonclaim", "source_basis", "valid_for_claim"])}

## Blockers

{md_table(tables["blockers"], ["blocker_id", "blocked_route", "missing_input", "needed_for_release", "current_status", "valid_for_claim"])}

## Formula Rows

{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4335 Y5-R2FR first source-backed PiPPN or R10 alpha(lambda) projection row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

The closed standard PPN zero branch now has a source-backed nonclaim smoke row. Open-tail `Pi_PPN` and R10 `alpha(lambda)` remain blocked.

## Smoke

{md_table(tables["ppn_smoke"], ["quantity", "predicted_value", "bound_value", "pass_nonclaim", "valid_for_claim"])}

## Blockers

{md_table(tables["blockers"], ["blocked_route", "missing_input", "needed_for_release", "current_status"])}

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


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

    add("VAL4335_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4335_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4335_candidate_split", "PPN zero is run while open PPN and R10 block", {"RUN_NONCLAIM_ZERO_BRANCH_SMOKE", "BLOCKED"}.issubset({r["result"] for r in tables["candidates"]}), "candidates")
    add("VAL4335_zero_row_scoreable", "standard-zero PPN row is scoreable nonclaim", any(r["scoreable_nonclaim"] == "True" and r["source_status"] == "SOURCE_BACKED_DERIVED_ZERO_BRANCH" for r in tables["ppn_zero"]), "ppn_zero")
    add("VAL4335_gamma_pass", "delta_gamma zero passes internal bound", any(r["quantity"] == "delta_gamma" and abs(float(r["predicted_value"])) <= float(r["bound_value"]) and r["pass_nonclaim"] == "True" for r in tables["ppn_smoke"]), "ppn_smoke")
    add("VAL4335_beta_pass", "delta_beta zero passes internal bound", any(r["quantity"] == "delta_beta" and abs(float(r["predicted_value"])) <= float(r["bound_value"]) and r["pass_nonclaim"] == "True" for r in tables["ppn_smoke"]), "ppn_smoke")
    add("VAL4335_open_PiPPN_blocked", "open-tail PiPPN blocker exists", any(r["missing_input"] == "MISSING_LOCAL_METRIC_TRANSFER_MATRIX" for r in tables["blockers"]), "blockers")
    add("VAL4335_R10_blocked", "R10 parent coefficients and bound curve blockers exist", {"MISSING_R10_PARENT_COEFFICIENTS", "MISSING_FULL_CLAIM_VALID_ALPHA_LAMBDA_BOUND_CURVE"}.issubset({r["missing_input"] for r in tables["blockers"]}), "blockers")
    add("VAL4335_formula_scores", "gamma and beta formulas present", any("abs(delta_gamma)=0 <= 1e-5" in r["formula"] for r in tables["formulas"]) and any("abs(delta_beta)=0 <= 1e-4" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4335_runner_modes", "runner has zero branch and blocked open/R10 modes", {"RUN_ZERO_BRANCH_SMOKE", "BLOCK_SCORE"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4335_firewall_zero_overclaim", "zero-branch overclaim blocked", any("standard-zero PPN smoke" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4335_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4335_next_metric_transfer", "next target is open-tail PiPPN or R10 fill", any("open-tail-PiPPN" in r["next_target"] and "R10" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4335_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4335_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4335_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4335_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4335_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4335_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4335_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4335_SOURCE_REGISTER.csv",
        "candidates": SOURCE_DIR / "P8_Y5_R2FR_4335_CANDIDATE_DECISION.csv",
        "ppn_zero": SOURCE_DIR / "P8_Y5_R2FR_4335_STANDARD_ZERO_PIPPN_ROW.csv",
        "ppn_smoke": SOURCE_DIR / "P8_Y5_R2FR_4335_PPN_ZERO_BRANCH_SMOKE_SCORE.csv",
        "blockers": SOURCE_DIR / "P8_Y5_R2FR_4335_OPEN_TAIL_AND_R10_BLOCKERS.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4335_FORMULA_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4335_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4335_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4335_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4335_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4335_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "candidates": candidate_rows(),
        "ppn_zero": ppn_zero_row(),
        "ppn_smoke": ppn_smoke_rows(),
        "blockers": blocker_rows(),
        "formulas": formula_rows(),
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
## PPC4161 4335 first source-backed PPN smoke row

Marker: `{MARKER}`

4335 runs the first source-backed local-test smoke row that is honest enough to evaluate: the closed standard branch PPN zero readout. In that branch, the private packet gives `gamma=1`, `beta=1`, and `R_PPN=0`, so `delta_gamma=0<=1e-5` and `delta_beta=0<=1e-4` in the internal dry gate. This is a branch sanity pass only, with `valid_for_claim=false`. It does not fill the open-tail `Pi_PPN` matrix, which still requires metric-transfer data from `T_open/K_tr,loc/q_loc`; R10 remains blocked by missing parent alpha coefficients and a claim-valid alpha(lambda) curve.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4335 packet first PPN smoke row

Marker: `{PACKET_MARKER}`

Packet update: the closed local branch now has a nonclaim gamma/beta smoke pass. The live frontier is the open-tail `Pi_PPN` metric-transfer derivation; if that fails, R10 needs parent alpha coefficients and a claim-valid bound curve before numeric scoring.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
