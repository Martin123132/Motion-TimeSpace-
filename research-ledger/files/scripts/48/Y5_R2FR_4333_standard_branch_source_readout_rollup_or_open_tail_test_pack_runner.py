from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4333"
CLAIM_ID = "L-174"
BRANCH = "MTS_R2FR_Y5_STANDARD_SOURCE_READOUT_ROLLUP_OR_OPEN_TAIL_TEST_PACK_4333"
DECISION = "STANDARD_BRANCH_SOURCE_READOUT_CLOSURE_CONTRACT_DERIVED_OPEN_TAIL_TEST_PACK_RETAINED_NONCLAIM"
MARKER = "PPC4161_STANDARD_SOURCE_READOUT_ROLLUP_OR_OPEN_TAIL_TEST_PACK_4333"
PACKET_MARKER = "PPC4161_PACKET_STANDARD_SOURCE_READOUT_ROLLUP_OR_OPEN_TAIL_TEST_PACK_4333"
NEXT_TARGET = "4334-Y5-R2FR-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"

FORMAL_PATH = FORMAL / "349-PPC4161-standard-branch-source-readout-rollup-or-open-tail-test-pack.md"
DOC_PATH = POST / "4333-Y5-R2FR-standard-branch-source-readout-rollup-or-open-tail-test-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4333_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4333_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4332_NEXT_TARGET.csv",
        "source-readout/local-GR closure contract",
        "4332 handoff selecting standard-branch rollup and open-tail test pack.",
    ),
    (
        "SRC4333_01_Xi_rollup",
        FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md",
        "if Xi_src_hidden=0 and epsilon_geom_core_after_projection=0, then epsilon_source_readout=0",
        "4332 closure implication.",
    ),
    (
        "SRC4333_02_Xi_open",
        FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md",
        "Xi_open <= C_w",
        "4332 open source-label tail bound.",
    ),
    (
        "SRC4333_03_geometry_core",
        FORMAL / "347-PPC4161-readout-frame-terminal-tail-zero-or-projection-bound.md",
        "epsilon_geom_core <= C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum",
        "4331 reduced geometry core.",
    ),
    (
        "SRC4333_04_projection_tail",
        FORMAL / "347-PPC4161-readout-frame-terminal-tail-zero-or-projection-bound.md",
        "epsilon_projection_open <=",
        "4331 open projection/readout envelope.",
    ),
    (
        "SRC4333_05_coeff_open",
        FORMAL / "346-PPC4161-coefficient-drift-zero-or-source-backed-tail-bound.md",
        "epsilon_coeff_open no-cancellation envelope",
        "4330 dynamic coefficient fallback.",
    ),
    (
        "SRC4333_06_EM_open",
        FORMAL / "345-PPC4161-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md",
        "epsilon_EM_open_boundary receives Phi_EM_rad",
        "4329 open radiation/constitutive fallback.",
    ),
    (
        "SRC4333_07_tail_guard",
        FORMAL / "344-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md",
        "tail_guard_sum",
        "4328 residual guard retained outside the standard branch.",
    ),
    (
        "SRC4333_08_tau_lock",
        FORMAL / "341-PPC4161-Dq-tau-reference-Hperp-zero-or-clock-tail-bound.md",
        "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout",
        "4325 one-parent-time lock used by the standard branch.",
    ),
    (
        "SRC4333_09_boundary_noflux",
        FORMAL / "342-PPC4161-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md",
        "epsilon_boundary_projector=0",
        "4326 q-basic no-flux domain condition used by the standard branch.",
    ),
    (
        "SRC4333_10_claim_gate",
        FORMAL / "343-PPC4161-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md",
        "source-readout closes only if epsilon_geom_core=0 and Xi_src_hidden=0",
        "4327 claim gate being sharpened into an explicit contract.",
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
                "4333 rolls the 4325-4332 standard-branch reductions into an explicit source-readout closure contract. If the single-parent-time lock, q-basic no-flux boundary/projector domain, ordinary matter action-domain descent, same-Hodge closed-collar EM branch, fixed/calibrated coefficient branch, quotient-natural readout/terminal action-domain branch, and source-label-forgetting Hilbert-owner Xi branch all hold, then Xi_src_hidden=0 and epsilon_geom_core_after_projection=0, hence epsilon_source_readout=0. This is a branch-local closure contract, not a public local-GR claim. Outside the branch, the open-tail test pack retains Xi_open, epsilon_EM_open_boundary, epsilon_coeff_open, epsilon_projection_open, tau/domain reopen tails and tail_guard_sum as source-backed local-test inputs for R10, PPN, clocks, orbital and EM checks.",
                "4333 source register, closure-contract rows, implication formulas, open-tail test-pack matrix, arena projection requirements, runner, firewall, decision, status, next-target and validation CSV.",
                "private_standard_branch_source_readout_closure_contract_with_open_tail_test_pack_nonclaim",
                "Build the local-test projection-matrix source contract and first R10/PPN smoke runner using only source-backed open-tail rows.",
                "Presenting branch-local source-readout closure as local GR; deleting open tails without source-backed zeros; mixing standard and nonstandard branch clauses; using fitted projection matrices after residuals; or running R10/PPN/clock/orbital claims without arena-specific transfer constants.",
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


def contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "contract_id": "CON4333_0_tau",
            "clause": "single parent-owned time/reference frame",
            "imported_zero": "epsilon_tau=0",
            "source_checkpoint": "4325",
            "failure_tail": "epsilon_tau_open",
            "status": "STANDARD_BRANCH_INPUT",
        },
        {
            "contract_id": "CON4333_1_boundary",
            "clause": "q-basic no-flux boundary/projector domain",
            "imported_zero": "epsilon_boundary_projector=0",
            "source_checkpoint": "4326",
            "failure_tail": "epsilon_boundary_projector_open",
            "status": "STANDARD_BRANCH_INPUT",
        },
        {
            "contract_id": "CON4333_2_matter",
            "clause": "ordinary matter action-domain descent through g_obs(q), theta_obs(q)",
            "imported_zero": "ordinary matter g_X=b_dis=0",
            "source_checkpoint": "4328",
            "failure_tail": "ordinary_matter_shadow_open",
            "status": "STANDARD_BRANCH_INPUT",
        },
        {
            "contract_id": "CON4333_3_EM",
            "clause": "visible same-Hodge static closed-collar EM branch",
            "imported_zero": "epsilon_EM_Hodge_frame=0",
            "source_checkpoint": "4329",
            "failure_tail": "epsilon_EM_open_boundary",
            "status": "STANDARD_BRANCH_INPUT_WITH_OPEN_BRANCH",
        },
        {
            "contract_id": "CON4333_4_coefficients",
            "clause": "fixed parent/calibrated coefficients with no hidden-field drift",
            "imported_zero": "epsilon_coeff=0",
            "source_checkpoint": "4330",
            "failure_tail": "epsilon_coeff_open",
            "status": "STANDARD_BRANCH_INPUT_WITH_OPEN_BRANCH",
        },
        {
            "contract_id": "CON4333_5_readout_terminal",
            "clause": "quotient-natural pure readout and terminal action-domain ownership",
            "imported_zero": "epsilon_readout_frame=epsilon_terminal=0",
            "source_checkpoint": "4331",
            "failure_tail": "epsilon_projection_open",
            "status": "STANDARD_BRANCH_INPUT_WITH_OPEN_BRANCH",
        },
        {
            "contract_id": "CON4333_6_Xi",
            "clause": "source-label-forgetting Hilbert-owner source data",
            "imported_zero": "Xi_src_hidden=0",
            "source_checkpoint": "4332",
            "failure_tail": "Xi_open",
            "status": "STANDARD_BRANCH_INPUT_WITH_OPEN_BRANCH",
        },
        {
            "contract_id": "CON4333_7_guard",
            "clause": "no remaining unsourced local projection/tail residual",
            "imported_zero": "tail_guard_sum=0",
            "source_checkpoint": "4328-4332",
            "failure_tail": "tail_guard_sum",
            "status": "NOT_AUTOMATICALLY_SIGNED",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4333_0_reduced_geometry",
            "name": "4331 reduced geometry core",
            "formula": "epsilon_geom_core_after_projection <= C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum",
            "status": "IMPORTED",
        },
        {
            "formula_id": "F4333_1_Xi_reduced_source_readout",
            "name": "4332 reduced source-readout",
            "formula": "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_projection + Xi_open",
            "status": "IMPORTED",
        },
        {
            "formula_id": "F4333_2_standard_geometry_zero",
            "name": "standard geometry zero condition",
            "formula": "epsilon_EM_open_boundary=epsilon_coeff_open=epsilon_projection_open=tail_guard_sum=0 => epsilon_geom_core_after_projection=0",
            "status": "DERIVED_BRANCH_CONTRACT",
        },
        {
            "formula_id": "F4333_3_standard_source_readout_zero",
            "name": "standard source-readout closure",
            "formula": "Xi_src_hidden=0 and epsilon_geom_core_after_projection=0 => epsilon_source_readout=0",
            "status": "DERIVED_BRANCH_CONTRACT",
        },
        {
            "formula_id": "F4333_4_open_tail_envelope",
            "name": "open branch source-readout envelope",
            "formula": "epsilon_source_readout_open <= (L_T L_mg + L_g)(C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum) + Xi_open",
            "status": "TEST_PACK_INPUT",
        },
        {
            "formula_id": "F4333_5_local_arena_projection",
            "name": "arena residual projection contract",
            "formula": "R_arena <= Pi_arena^Xi Xi_open + Pi_arena^EM epsilon_EM_open_boundary + Pi_arena^coeff epsilon_coeff_open + Pi_arena^proj epsilon_projection_open + Pi_arena^guard tail_guard_sum + Pi_arena^tau epsilon_tau_open + Pi_arena^domain epsilon_boundary_projector_open",
            "status": "SOURCE_MATRIX_REQUIRED",
        },
        {
            "formula_id": "F4333_6_claim_gate",
            "name": "local claim gate",
            "formula": "local claim requires all standard-zero clauses signed, all open tails zero or source-bounded, and all Pi_arena transfer constants fixed before scoring",
            "status": "CLAIM_BLOCKED",
        },
    ]


def test_pack_rows() -> List[Dict[str, str]]:
    return [
        {
            "pack_id": "TP4333_0_R10",
            "arena": "R10 short-range fifth-force",
            "residual_vector": "R_R10",
            "tail_inputs": "Xi_open; epsilon_projection_open; epsilon_coeff_open; tail_guard_sum; epsilon_boundary_projector_open",
            "required_sources": "lambda profile; alpha transfer; lab-composition coupling; boundary/domain support; valid bound curve",
            "projection_contract": "Pi_R10 fixed before fit and sourced row-by-row",
            "status": "NOT_READY_FOR_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "TP4333_1_PPN",
            "arena": "PPN/Cassini/local solar tests",
            "residual_vector": "R_PPN",
            "tail_inputs": "epsilon_projection_open; Xi_open; epsilon_coeff_open; tail_guard_sum; epsilon_tau_open",
            "required_sources": "gamma/beta transfer; preferred-frame map; range profile; clock/reference convention",
            "projection_contract": "Pi_PPN fixed before scoring, not post-fit",
            "status": "NOT_READY_FOR_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "TP4333_2_clocks",
            "arena": "clock/redshift/atomic standards",
            "residual_vector": "R_clock",
            "tail_inputs": "epsilon_tau_open; epsilon_coeff_open; Xi_open; epsilon_EM_open_boundary",
            "required_sources": "clock species map; alpha/mass sensitivity; tau reference; EM/radiative collar policy",
            "projection_contract": "Pi_clock fixed by metrology source, not by residual minimization",
            "status": "NOT_READY_FOR_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "TP4333_3_orbital",
            "arena": "orbital/ephemeris/binary dynamics",
            "residual_vector": "R_orbital",
            "tail_inputs": "epsilon_tau_open; epsilon_projection_open; Xi_open; tail_guard_sum",
            "required_sources": "GM convention; orbital frame; range/time transfer; source support and no-flux domain",
            "projection_contract": "Pi_orbital fixed before using ephemeris residuals",
            "status": "NOT_READY_FOR_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "TP4333_4_EM",
            "arena": "EM/stress/Poynting/radiation",
            "residual_vector": "R_EM",
            "tail_inputs": "epsilon_EM_open_boundary; epsilon_coeff_open; Xi_open",
            "required_sources": "open radiation flux; constitutive deformation; source current normalization; Hodge ownership",
            "projection_contract": "Pi_EM separates Hilbert EM flux from extra force tail",
            "status": "NOT_READY_FOR_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "TP4333_5_WEP_source",
            "arena": "WEP/source-composition",
            "residual_vector": "R_WEP",
            "tail_inputs": "Xi_open; epsilon_projection_open; ordinary_matter_shadow_open",
            "required_sources": "composition charge map; source labels; matter action-domain ownership; material selector policy",
            "projection_contract": "Pi_WEP source-composition transfer fixed before comparison",
            "status": "NOT_READY_FOR_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4333_0_standard_all_clauses",
            "branch_input": "all CON4333 standard clauses signed and open tails zero",
            "action": "ALLOW_SOURCE_READOUT_ZERO",
            "output": "epsilon_source_readout=0",
            "claim_policy": "branch-local closure only; no public local-GR claim",
        },
        {
            "runner_id": "RUN4333_1_open_tail_present",
            "branch_input": "any Xi/EM/coefficient/projection/tau/domain/guard tail survives",
            "action": "USE_OPEN_TAIL_TEST_PACK",
            "output": "R_arena projection rows required",
            "claim_policy": "valid_for_claim=false until sourced",
        },
        {
            "runner_id": "RUN4333_2_branch_mixed",
            "branch_input": "standard zero for one sector mixed with unsourced nonstandard sector",
            "action": "REJECT_MIXED_CLOSURE",
            "output": "retain corresponding open tail",
            "claim_policy": "firewall",
        },
        {
            "runner_id": "RUN4333_3_projection_fit",
            "branch_input": "Pi_arena chosen after seeing residuals",
            "action": "REJECT_POSTFIT_PROJECTION",
            "output": "projection invalid for claim",
            "claim_policy": "firewall",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4333_0_local_GR_claim",
            "forbidden_shortcut": "present source-readout closure as local GR/Newton/PPN pass",
            "reason": "closure is branch-local and arena projection matrices remain unsourced",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4333_1_delete_open_tails",
            "forbidden_shortcut": "delete Xi_open, EM, coefficient, projection, tau/domain or guard tails without a zero theorem/source bound",
            "reason": "open-tail pack is the empirical contract, not clutter",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4333_2_branch_mix",
            "forbidden_shortcut": "mix standard and nonstandard branch assumptions in one local claim",
            "reason": "each arena score must declare which tails are zero and which are bounded",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4333_3_postfit_projection",
            "forbidden_shortcut": "choose Pi_R10/Pi_PPN/Pi_clock/Pi_orbital after seeing residuals",
            "reason": "projection matrices must be sourced and frozen before scoring",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4333_4_data_claim",
            "forbidden_shortcut": "run an R10/PPN/clock/orbital claim with placeholder transfer constants",
            "reason": "test pack rows are source-contract rows until numeric/source-backed matrices exist",
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
            "summary": "The standard source-readout closure contract is now explicit: all standard-zero clauses imply Xi=0 and reduced geometry core=0, hence epsilon_source_readout=0. This is not local GR yet; outside that branch the open-tail test pack defines exactly what R10/PPN/clock/orbital/EM projections must source.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4333_0_source_readout",
            "item": "epsilon_source_readout",
            "status": "BRANCH_LOCAL_CLOSURE_CONTRACT_DERIVED",
            "notes": "closes only if all standard-zero clauses and open-tail zeros hold",
        },
        {
            "status_id": "STAT4333_1_local_GR",
            "item": "local GR/Newton/PPN",
            "status": "NOT_CLAIMED",
            "notes": "needs arena projection matrices and source-backed tail magnitudes",
        },
        {
            "status_id": "STAT4333_2_test_pack",
            "item": "open-tail test pack",
            "status": "READY_AS_SOURCE_CONTRACT",
            "notes": "R10/PPN/clock/orbital/EM rows identify required inputs",
        },
        {
            "status_id": "STAT4333_3_next",
            "item": "local projection matrix source contract",
            "status": "NEXT_TARGET",
            "notes": "build first numeric/sourced runner only after transfer constants are fixed",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4333_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the open-tail test pack be converted into source-backed local projection matrices and a first nonclaim R10/PPN smoke runner?",
            "preferred_route": "source or define Pi_R10, Pi_PPN, Pi_clock, Pi_orbital and Pi_EM before scoring; keep placeholder rows invalid for claim",
            "fallback_route": "if matrices cannot be sourced, write a blocker table and keep the local branch as closure-contract-only",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 349 - PPC4161 standard branch source-readout rollup or open-tail test pack

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4333 does **not** prove public local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, Maxwell/QED, charge normalization, or a numerical value of `G_N`.

It does something useful and sharper: it converts the 4325-4332 ladder into a single closure contract, and it names the exact open-tail rows that must be sourced before local tests mean anything.

## Closure Contract

```text
epsilon_geom_core_after_projection
 <= C_EMopen epsilon_EM_open_boundary
  + C_coeff_open epsilon_coeff_open
  + C_proj epsilon_projection_open
  + tail_guard_sum.

epsilon_source_readout
 <= (L_T L_mg + L_g) epsilon_geom_core_after_projection
  + Xi_open.

Standard branch:
Xi_src_hidden=0,
epsilon_EM_open_boundary=0,
epsilon_coeff_open=0,
epsilon_projection_open=0,
tail_guard_sum=0
=> epsilon_geom_core_after_projection=0
=> epsilon_source_readout=0.
```

This is a branch-local closure theorem. It is not a local-GR claim until the arena projection rows are source-backed.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Standard Branch Contract Rows

{md_table(tables["contract"], ["contract_id", "clause", "imported_zero", "source_checkpoint", "failure_tail", "status"])}

## Formula Rollup

{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Open-Tail Local-Test Pack

{md_table(tables["test_pack"], ["pack_id", "arena", "residual_vector", "tail_inputs", "required_sources", "projection_contract", "status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4333 Y5-R2FR standard branch source-readout rollup or open-tail test pack

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

The local source-readout chain now has a clean branch-local closure contract: all standard-zero clauses imply `epsilon_source_readout=0`. The nonstandard route is no longer vague; it is the open-tail test pack below.

## Rollup

{md_table(tables["formulas"], ["formula_id", "formula", "status"])}

## Test Pack

{md_table(tables["test_pack"], ["arena", "tail_inputs", "required_sources", "projection_contract", "status"])}

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

    add("VAL4333_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4333_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4333_contract_all_inputs", "contract includes core standard inputs", {"epsilon_tau=0", "epsilon_boundary_projector=0", "ordinary matter g_X=b_dis=0", "epsilon_EM_Hodge_frame=0", "epsilon_coeff=0", "epsilon_readout_frame=epsilon_terminal=0", "Xi_src_hidden=0", "tail_guard_sum=0"}.issubset({r["imported_zero"] for r in tables["contract"]}), "contract")
    add("VAL4333_geometry_formula", "reduced geometry formula contains open tails", any("epsilon_geom_core_after_projection <=" in r["formula"] and "epsilon_EM_open_boundary" in r["formula"] and "epsilon_projection_open" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4333_source_readout_zero", "source-readout zero implication present", any(r["formula_id"] == "F4333_3_standard_source_readout_zero" and "epsilon_source_readout=0" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4333_open_envelope", "open-tail envelope present", any(r["formula_id"] == "F4333_4_open_tail_envelope" and "Xi_open" in r["formula"] and "tail_guard_sum" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4333_arena_projection_formula", "arena projection formula includes Pi terms", any("Pi_arena^Xi" in r["formula"] and "Pi_arena^tau" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4333_test_pack_arenas", "test pack covers main local arenas", {"R10 short-range fifth-force", "PPN/Cassini/local solar tests", "clock/redshift/atomic standards", "orbital/ephemeris/binary dynamics", "EM/stress/Poynting/radiation", "WEP/source-composition"}.issubset({r["arena"] for r in tables["test_pack"]}), "test_pack")
    add("VAL4333_all_test_rows_nonclaim", "all test pack rows invalid for claim", all(r["valid_for_claim"] == "False" and r["status"] == "NOT_READY_FOR_CLAIM" for r in tables["test_pack"]), "test_pack")
    add("VAL4333_runner_modes", "runner has closure, open-tail and reject modes", {"ALLOW_SOURCE_READOUT_ZERO", "USE_OPEN_TAIL_TEST_PACK", "REJECT_MIXED_CLOSURE", "REJECT_POSTFIT_PROJECTION"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4333_firewall_local_claim", "local GR shortcut blocked", any("source-readout closure as local GR" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4333_firewall_projection", "post-fit projection blocked", any("Pi_R10" in r["forbidden_shortcut"] and "after seeing residuals" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4333_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4333_next_projection_contract", "next target is projection-matrix source contract", any("projection-matrix" in r["next_target"] and "R10/PPN" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4333_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4333_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4333_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4333_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4333_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4333_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4333_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4333_SOURCE_REGISTER.csv",
        "contract": SOURCE_DIR / "P8_Y5_R2FR_4333_STANDARD_BRANCH_CONTRACT.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4333_SOURCE_READOUT_ROLLUP_FORMULAS.csv",
        "test_pack": SOURCE_DIR / "P8_Y5_R2FR_4333_OPEN_TAIL_LOCAL_TEST_PACK.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4333_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4333_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4333_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4333_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4333_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "contract": contract_rows(),
        "formulas": formula_rows(),
        "test_pack": test_pack_rows(),
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
## PPC4161 4333 standard source-readout closure rollup

Marker: `{MARKER}`

4333 combines the 4325-4332 standard-branch reductions into a single closure contract. If the tau/reference lock, q-basic no-flux boundary, ordinary matter descent, same-Hodge closed-collar EM branch, calibrated coefficient branch, quotient-natural readout/terminal branch and source-label-forgetting Xi branch all hold, then `epsilon_geom_core_after_projection=0` and `Xi_src_hidden=0`, hence `epsilon_source_readout=0`. This is a branch-local theorem, not a local-GR claim. The nonstandard route is now an open-tail local-test pack requiring source-backed `Pi_R10`, `Pi_PPN`, `Pi_clock`, `Pi_orbital`, `Pi_EM` and `Pi_WEP` matrices before empirical scoring.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4333 packet standard source-readout rollup

Marker: `{PACKET_MARKER}`

Packet update: the local branch now has a clean source-readout closure contract and an explicit open-tail test pack. The next job is not more circling; it is sourcing/fixing the arena projection matrices before any R10/PPN/clock/orbital smoke scoring.
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
