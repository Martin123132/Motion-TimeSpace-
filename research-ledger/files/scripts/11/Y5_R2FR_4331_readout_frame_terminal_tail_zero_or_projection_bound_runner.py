from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4331"
CLAIM_ID = "L-172"
BRANCH = "MTS_R2FR_Y5_READOUT_FRAME_TERMINAL_TAIL_ZERO_OR_PROJECTION_BOUND_4331"
DECISION = "QUOTIENT_NATURAL_PURE_READOUT_ZERO_IMPORTED_TERMINAL_SHORTCUT_REJECTED_REDUCED_GEOMETRY_CORE_HANDS_TO_XI_NONCLAIM"
MARKER = "PPC4161_READOUT_FRAME_TERMINAL_TAIL_ZERO_OR_PROJECTION_BOUND_4331"
PACKET_MARKER = "PPC4161_PACKET_READOUT_FRAME_TERMINAL_TAIL_ZERO_OR_PROJECTION_BOUND_4331"
NEXT_TARGET = "4332-Y5-R2FR-Xi-src-hidden-zero-or-source-label-tail-bound.md"

FORMAL_PATH = FORMAL / "347-PPC4161-readout-frame-terminal-tail-zero-or-projection-bound.md"
DOC_PATH = POST / "4331-Y5-R2FR-readout-frame-terminal-tail-zero-or-explicit-projection-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4331_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4331_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4330_NEXT_TARGET.csv",
        "readout-frame",
        "4330 handoff selecting readout-frame/terminal projection tails.",
    ),
    (
        "SRC4331_01_4330_core",
        FORMAL / "346-PPC4161-coefficient-drift-zero-or-source-backed-tail-bound.md",
        "epsilon_readout_frame",
        "4330 reduced geometry core still contains readout-frame and terminal tails.",
    ),
    (
        "SRC4331_02_quotient",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "Ordinary matter, EM stress, clocks, rods and source readouts must also factor through q",
        "Quotient-natural readout/action-domain theorem.",
    ),
    (
        "SRC4331_03_readout_counter",
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "post-readout projection after X already coupled",
        "Countermodel: readout after hidden coupling is not a zero route.",
    ),
    (
        "SRC4331_04_terminal_reject",
        FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md",
        "That shortcut fails.",
        "Terminal public metric/coframe alone is rejected.",
    ),
    (
        "SRC4331_05_terminal_object",
        FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md",
        "terminal public metric/coframe object e_pub exists",
        "The tempting terminal-object route being firewalled.",
    ),
    (
        "SRC4331_06_4328_tails",
        FORMAL / "344-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md",
        "epsilon_readout_frame",
        "4328 named readout-frame and terminal residuals.",
    ),
    (
        "SRC4331_07_source_readout",
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Dq_source_readout = 0",
        "Earlier standard-branch source-readout zero, guarded against coefficient/readout reentry.",
    ),
    (
        "SRC4331_08_EM_pure_readout",
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "If readout is pure postprocessing:",
        "EM readout/coupling guard used as sector-specific support.",
    ),
    (
        "SRC4331_09_4277_guard",
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "Dq_source_readout = 0",
        "4277 guard row lists source-readout silence as a required escape blocker.",
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
                "4331 imports the quotient-naturality/pure-readout theorem into the 4330-reduced geometry core. If ordinary matter, EM stress, clocks, rods, source readouts, and local test readouts factor through q before variation, and the readout maps are pure postprocessing with no action-domain or effective-frame reentry, then epsilon_readout_frame=0. The terminal public metric/coframe shortcut remains explicitly rejected: epsilon_terminal=0 only when terminal/public geometry is the quotient-owned action-domain geometry, not merely because a terminal object exists. Under that stronger branch, epsilon_terminal=0 and the reduced geometry core no longer carries standard readout-frame/terminal tails. Open readout reentry, post-fit projector choices, terminal-object shortcuts, and arena projection matrices remain explicit finite rows. No local GR/R10/PPN/clock/orbital claim fires.",
                "4331 source register, readout-terminal audit, zero rows, projection-tail bound rows, geometry/source-readout update formulas, runner, firewall, decision, status, next-target and validation CSV.",
                "private_quotient_natural_readout_terminal_tail_zero_nonclaim",
                "Attack Xi_src_hidden/source-label tail next, while retaining open projection rows for nonstandard readout or terminal shortcut branches.",
                "Using terminal public metric as a no-shadow proof; applying readout zero after hidden coupling has already entered the action; hiding post-fit projector choices; treating local projection rows as claim-valid without source-backed matrices; or claiming local GR/R10/PPN/clock pass while Xi/open projection gates remain.",
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


def audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "AUD4331_0_quotient_readout",
            "gate": "quotient-natural readout",
            "clause": "readout maps factor through q before variation",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "vertical Hperp representative motion cannot create a readout-frame force",
        },
        {
            "audit_id": "AUD4331_1_pure_postprocessing",
            "gate": "pure postprocessing",
            "clause": "readout is not an argument of S_parent or S_eff and does not regenerate frame/Hodge/coefficient slots",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "epsilon_readout_frame=0 inside standard branch",
        },
        {
            "audit_id": "AUD4331_2_terminal_reject",
            "gate": "terminal shortcut",
            "clause": "terminal public metric/coframe alone does not exclude pre-readout frame slots",
            "status": "REJECTED_SHORTCUT",
            "effect": "terminality cannot be used as no-shadow proof",
        },
        {
            "audit_id": "AUD4331_3_terminal_action_domain",
            "gate": "terminal/public geometry action-domain ownership",
            "clause": "e_obs/g_obs are quotient-owned action-domain geometry and no separate terminal-to-matter frame map exists",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "epsilon_terminal=0 under the stronger action-domain clause",
        },
        {
            "audit_id": "AUD4331_4_projection_open",
            "gate": "projection/readout reentry",
            "clause": "post-fit projectors, source-readout reentry, terminal shortcuts or arena projection matrices survive",
            "status": "BOUND_RETAINED_OUTSIDE_BRANCH",
            "effect": "epsilon_projection_open is retained for local tests",
        },
    ]


def zero_rows() -> List[Dict[str, str]]:
    return [
        {
            "zero_id": "ZERO4331_0_readout_frame",
            "symbol": "epsilon_readout_frame",
            "zero_statement": "epsilon_readout_frame=0",
            "branch_conditions": "readout functor is quotient-natural and pure postprocessing; no action-domain/effective-frame reentry",
            "status": "CONDITIONAL_ZERO_IMPORTED_INTO_REDUCED_GEOMETRY_CORE",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4331_1_terminal",
            "symbol": "epsilon_terminal",
            "zero_statement": "epsilon_terminal=0",
            "branch_conditions": "terminal/public geometry is the quotient-owned action-domain geometry; terminal object is not used as a shortcut",
            "status": "CONDITIONAL_ZERO_NOT_TERMINAL_SHORTCUT",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4331_2_Dq_source_readout_standard",
            "symbol": "Dq_source_readout[Hperp]",
            "zero_statement": "independent readout-frame leg is zero; dependent source-readout terms are inherited through q-owned matter/geometry/tau/boundary/theta/Xi",
            "branch_conditions": "standard branch plus prior 4321-4330 reductions",
            "status": "DEPENDENCY_ZERO_NOT_BLANKET_ZERO",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4331_3_terminal_shortcut",
            "symbol": "terminal_metric_shortcut",
            "zero_statement": "terminal public metric alone gives no zero",
            "branch_conditions": "unconditional firewall",
            "status": "REJECTED",
            "valid_for_claim": "False",
        },
    ]


def tail_rows() -> List[Dict[str, str]]:
    return [
        {
            "tail_id": "TAIL4331_0_post_action_reentry",
            "symbol": "R_post_action_reentry",
            "meaning": "readout/postprocessing map re-enters S_parent or S_eff after hidden coupling",
            "bound_contribution": "|R_post_action_reentry|",
            "observable_links": "PPN; clocks; source readout; R10; orbital",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4331_1_terminal_shortcut",
            "symbol": "R_terminal_shortcut",
            "meaning": "terminal object used as no-shadow proof without action-domain exclusion",
            "bound_contribution": "|R_terminal_shortcut|",
            "observable_links": "common frame coupling; PPN gamma; WEP; clocks",
            "status": "REJECTED_AS_ZERO_RETAINED_AS_BOUND_IF_USED",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4331_2_projector_fit",
            "symbol": "R_projector_fit",
            "meaning": "local projector or arena projection matrix selected after seeing residuals",
            "bound_contribution": "|R_projector_fit|",
            "observable_links": "PPN; R10; clock; orbital scoring",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4331_3_source_readout_reentry",
            "symbol": "R_source_readout_reentry",
            "meaning": "source readout changes mass/current/charge normalization after variation",
            "bound_contribution": "|R_source_readout_reentry|",
            "observable_links": "Newtonian mass; WEP; orbital GM; clock/source coupling",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4331_4_arena_projection",
            "symbol": "Pi_arena_tail",
            "meaning": "PPN/R10/clock/orbital projection constants are not sourced",
            "bound_contribution": "sum_a |Pi_a R_a|",
            "observable_links": "R10; PPN; clocks; orbital systems",
            "status": "RETAINED_FOR_LOCAL_TEST_RUNNERS",
            "valid_for_claim": "False",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4331_0_readout_zero",
            "name": "quotient-natural readout zero",
            "formula": "R_obs(Phi)=Rbar(q(Phi)) and Hperp in ker(Dq) => D_Hperp R_obs = DRbar[Dq(Hperp)] = 0",
            "status": "CONDITIONAL_ZERO_DERIVED",
        },
        {
            "formula_id": "F4331_1_pure_postprocessing_guard",
            "name": "no readout reentry",
            "formula": "readout_after_variation and no readout slot in S_parent/S_eff => epsilon_readout_frame=0",
            "status": "CONDITIONAL_ZERO_DERIVED",
        },
        {
            "formula_id": "F4331_2_terminal_reject",
            "name": "terminal shortcut rejection",
            "formula": "terminal e_pub exists does not imply no A_g/B_dis/h_perp/readout frame slot in S_matter or S_EM",
            "status": "REJECTED_SHORTCUT",
        },
        {
            "formula_id": "F4331_3_terminal_action_domain_zero",
            "name": "terminal/action-domain zero",
            "formula": "e_obs=e_bar(q) used in the action domain and no separate terminal-to-matter frame map => epsilon_terminal=0",
            "status": "CONDITIONAL_ZERO_DERIVED_NOT_SHORTCUT",
        },
        {
            "formula_id": "F4331_4_projection_bound",
            "name": "open projection/readout envelope",
            "formula": "epsilon_projection_open <= |R_post_action_reentry| + |R_terminal_shortcut| + |R_projector_fit| + |R_source_readout_reentry| + sum_a |Pi_a R_a|",
            "status": "BOUND_RETAINED_OUTSIDE_BRANCH",
        },
        {
            "formula_id": "F4331_5_geometry_core_update",
            "name": "geometry core after readout-terminal reduction",
            "formula": "epsilon_geom_core <= C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum",
            "status": "REDUCED_BUT_OPEN",
        },
        {
            "formula_id": "F4331_6_source_readout_update",
            "name": "source-readout after readout-terminal reduction",
            "formula": "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_projection + Xi_src_hidden",
            "status": "NONCLAIM_HANDOFF_TO_XI",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4331_0_quotient_readout_branch",
            "branch_input": "q-natural action-domain readout plus pure postprocessing",
            "action": "ALLOW_READOUT_TERMINAL_ZERO",
            "output": "epsilon_readout_frame=epsilon_terminal=0",
            "claim_policy": "private nonclaim; Xi/open projection gates remain",
        },
        {
            "runner_id": "RUN4331_1_terminal_shortcut",
            "branch_input": "terminal public metric/coframe exists but action-domain exclusion is missing",
            "action": "REJECT",
            "output": "no terminal/no-shadow zero",
            "claim_policy": "firewall",
        },
        {
            "runner_id": "RUN4331_2_projection_open",
            "branch_input": "readout reentry, post-fit projector, or unsourced arena projection constants",
            "action": "KEEP_PROJECTION_BOUND",
            "output": "epsilon_projection_open finite tail",
            "claim_policy": "source-backed matrices required before local tests",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4331_0_terminal_shortcut",
            "forbidden_shortcut": "terminal public metric/coframe proves no-shadow frame",
            "reason": "terminality is not an action-domain exclusion",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4331_1_post_readout",
            "forbidden_shortcut": "project away a coupling after it entered the action",
            "reason": "post-readout projection after hidden coupling is a countermodel, not a zero theorem",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4331_2_projector_fit",
            "forbidden_shortcut": "choose local projector or arena matrix after seeing residuals",
            "reason": "projection constants must be source-backed and fixed before scoring",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4331_3_blanket_source_readout",
            "forbidden_shortcut": "treat Dq_source_readout[Hperp]=0 as a blanket zero",
            "reason": "4321 keeps dependent geometry/Xi/source-tail inheritance explicit",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4331_4_local_claim",
            "forbidden_shortcut": "claim local GR/R10/PPN/clock pass from readout closure",
            "reason": "Xi_src_hidden and open projection/nonstandard tails remain",
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
            "summary": "Readout-frame and terminal tails are zero only in the quotient-natural action-domain plus pure-postprocessing branch. The terminal object shortcut is rejected and open projection/readout reentry rows remain finite tails.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4331_0_readout",
            "item": "epsilon_readout_frame",
            "status": "CONDITIONAL_ZERO_IN_Q_NATURAL_BRANCH",
            "notes": "pure postprocessing and no action-domain/effective-frame reentry",
        },
        {
            "status_id": "STAT4331_1_terminal",
            "item": "epsilon_terminal",
            "status": "CONDITIONAL_ZERO_WITH_TERMINAL_SHORTCUT_FIREWALL",
            "notes": "zero uses action-domain quotient ownership, not terminal object alone",
        },
        {
            "status_id": "STAT4331_2_projection",
            "item": "epsilon_projection_open",
            "status": "BOUND_RETAINED",
            "notes": "unsourced arena projection/readout reentry rows remain outside standard branch",
        },
        {
            "status_id": "STAT4331_3_geometry_core",
            "item": "epsilon_geom_core",
            "status": "REDUCED_BUT_OPEN",
            "notes": "standard branch now mostly hands to Xi_src_hidden plus open nonstandard tails",
        },
        {
            "status_id": "STAT4331_4_next",
            "item": "Xi_src_hidden",
            "status": "NEXT_TARGET",
            "notes": "source-label/hidden prefactor tail is now the cleanest remaining local-GR bottleneck",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4331_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Xi_src_hidden be zeroed by source-label forgetting, Hilbert source ownership and no hidden source-prefactor slots, or must it become a finite multi-arena source-label tail?",
            "preferred_route": "prove no hidden source weights, no source normalization reentry, no direct matter-X vertex and no environment/source-label selector in the parent/effective action",
            "fallback_route": "write explicit Xi components for hidden weights, source normalization, no-direct-matter-charge, environment selector and local projection transfer",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 347 - PPC4161 readout-frame terminal tail zero or projection bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4331 does **not** prove public local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, or a global no-shadow theorem.

It removes a live tail only inside a precise branch: quotient-natural readout, action-domain ownership, and pure postprocessing. It explicitly rejects the terminal public metric shortcut.

## Branch Law

```text
R_obs(Phi)=Rbar(q(Phi)),
Hperp in ker(Dq)
=> D_Hperp R_obs = 0

readout_after_variation,
no readout slot in S_parent or S_eff
=> epsilon_readout_frame = 0

e_obs=e_bar(q) used in the action domain,
no separate terminal-to-matter frame map
=> epsilon_terminal = 0

terminal object alone
=> no zero
```

Open projection/reentry cases remain finite tails.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Readout-Terminal Audit

{md_table(tables["audit"], ["audit_id", "gate", "clause", "status", "effect"])}

## Zero Rows

{md_table(tables["zeros"], ["zero_id", "symbol", "zero_statement", "branch_conditions", "status", "valid_for_claim"])}

## Projection Tail Bound

{md_table(tables["tails"], ["tail_id", "symbol", "meaning", "bound_contribution", "observable_links", "status"])}

## Formula Updates

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
    post = f"""# 4331 Y5-R2FR readout-frame terminal tail zero or explicit projection bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

`epsilon_readout_frame` and `epsilon_terminal` are now branch-resolved. The zero route is quotient-natural readout plus action-domain ownership, not terminal-object rhetoric.

## Reduced Geometry Core

{md_table(tables["formulas"], ["formula_id", "formula", "status"])}

## Remaining Projection Tails

{md_table(tables["tails"], ["tail_id", "symbol", "observable_links", "status"])}

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

    add("VAL4331_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4331_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4331_readout_zero", "epsilon_readout_frame zero row exists", any(r["symbol"] == "epsilon_readout_frame" for r in tables["zeros"]), "zeros")
    add("VAL4331_terminal_zero", "epsilon_terminal zero row exists", any(r["symbol"] == "epsilon_terminal" and "SHORTCUT" in r["status"] for r in tables["zeros"]), "zeros")
    add("VAL4331_terminal_reject", "terminal shortcut is rejected", any(r["symbol"] == "terminal_metric_shortcut" and r["status"] == "REJECTED" for r in tables["zeros"]) and any("terminal public metric" in r["forbidden_shortcut"] for r in tables["firewall"]), "zeros/firewall")
    add("VAL4331_quotient_formula", "quotient readout formula present", any("Rbar(q(Phi))" in r["formula"] and "ker(Dq)" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4331_projection_bound", "projection/reentry bound retained", any("epsilon_projection_open <=" in r["formula"] and "R_projector_fit" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4331_geometry_formula_reduced", "geometry formula no longer carries standard readout/terminal tails", any(r["formula_id"] == "F4331_5_geometry_core_update" and "epsilon_readout_frame" not in r["formula"] and "epsilon_terminal" not in r["formula"] and "epsilon_projection_open" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4331_post_readout_firewall", "post-readout projection after coupling blocked", any("project away a coupling" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4331_blanket_source_firewall", "blanket source-readout zero blocked", any("blanket zero" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4331_runner_modes", "runner has zero, reject and bound modes", {"ALLOW_READOUT_TERMINAL_ZERO", "REJECT", "KEEP_PROJECTION_BOUND"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4331_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4331_next_Xi", "next target is Xi_src_hidden", any("Xi-src-hidden" in r["next_target"] and "Xi_src_hidden" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4331_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4331_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4331_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4331_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4331_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4331_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4331_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4331_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4331_READOUT_TERMINAL_AUDIT.csv",
        "zeros": SOURCE_DIR / "P8_Y5_R2FR_4331_READOUT_TERMINAL_ZERO_ROWS.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4331_PROJECTION_TAIL_BOUND.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4331_GEOMETRY_UPDATE_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4331_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4331_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4331_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4331_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4331_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "zeros": zero_rows(),
        "tails": tail_rows(),
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
## PPC4161 4331 readout-frame terminal tail zero or projection bound

Marker: `{MARKER}`

4331 imports quotient-naturality/pure-readout ownership into the 4330-reduced geometry core. In the standard branch, `R_obs(Phi)=Rbar(q(Phi))` and `Hperp in ker(Dq)` give `epsilon_readout_frame=0`; terminal/public geometry gives `epsilon_terminal=0` only when it is the quotient-owned action-domain geometry, not from terminal-object existence alone. The terminal shortcut remains firewalled. The reduced geometry core now hands mainly to open projection rows and `Xi_src_hidden`, with nonstandard EM/coefficient tails retained outside the branch.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4331 packet readout-frame terminal tail zero

Marker: `{PACKET_MARKER}`

Packet update: readout/terminal frame leakage is now branch-resolved. Pure quotient-natural postprocessing closes the standard readout-frame tail; terminality alone remains rejected. The next private bottleneck is `Xi_src_hidden` and source-label/source-prefactor leakage.
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
